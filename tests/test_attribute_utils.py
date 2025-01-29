# test_string_to_type.py
from typing import Literal

import pytest
from pydantic import BaseModel, ValidationError

from comfyui_structured_outputs.attribute_utils import (
    BaseAttributeModel,
    BaseAttributesModel,
    attributes_to_model,
    string_to_type,
)


@pytest.mark.parametrize(
    "attr_type, expected_type",
    [
        ("str", str),
        ("int", int),
        ("float", float),
        ("bool", bool),
    ],
)
def test_no_options_returns_basic_type(attr_type, expected_type):
    """
    Test that string_to_type returns the correct basic Python type
    when no options_str is provided.
    """
    returned_type = string_to_type(attr_type)
    assert returned_type is expected_type


@pytest.mark.parametrize("invalid_type", ["unknown_type", "object", "somethingelse"])
def test_invalid_attribute_type_raises_value_error(invalid_type):
    """
    Test that a ValueError is raised if an invalid attribute type is passed.
    """
    with pytest.raises(ValueError, match="Invalid attribute type"):
        string_to_type(invalid_type)


@pytest.mark.parametrize(
    "attr_type,options_str,expected_args",
    [
        ("int", "1,2,3", (1, 2, 3)),
        ("float", "1.1 , 2.2,3.3", (1.1, 2.2, 3.3)),
        ("str", "apple, banana,orange ", ("apple", "banana", "orange")),
        ("bool", "True, False", (True, False)),
        ("bool", " true,false", (True, False)),
    ],
)
def test_literal_options(attr_type, options_str, expected_args):
    """
    Test that string_to_type returns a Literal type with the expected args
    when options_str is provided.
    """
    literal_type = string_to_type(attr_type, options_str)
    # Checking the __args__ of the returned Literal
    assert hasattr(literal_type, "__args__"), "Returned type must have __args__."
    assert literal_type.__args__ == expected_args, (
        f"Expected the literal type to have values {expected_args}, "
        f"but got {literal_type.__args__} instead."
    )


def test_pydantic_integration():
    """
    Test that a Pydantic model with a field using the type returned
    by string_to_type validates correctly.
    """
    MyLiteralType = string_to_type("int", "1,2,3")

    class MyModel(BaseModel):
        my_field: MyLiteralType

    # Valid cases
    assert MyModel(my_field=1).my_field == 1
    assert MyModel(my_field=2).my_field == 2
    assert MyModel(my_field=3).my_field == 3

    # Invalid case
    with pytest.raises(ValidationError, match="literal_error"):
        MyModel(my_field=4)


# ---------------------
# Example attribute definitions
# ---------------------
class MyStrAttr(BaseAttributeModel):
    """
    Example attribute with a 'key' and a string value.
    Pydantic v2 example fields usage:
      - If you use model_config or model_fields in your real code, adapt accordingly.
    """

    key: Literal["my_str_attr"] = "my_str_attr"
    value: str


class MyIntAttr(BaseAttributeModel):
    key: Literal["my_int_attr"] = "my_int_attr"
    value: int


class MyBoolAttr(BaseAttributeModel):
    key: Literal["my_bool_attr"] = "my_bool_attr"
    value: bool


# ---------------------
# Tests
# ---------------------


def test_base_attributes_model_init():
    """
    Test that BaseAttributesModel can initialize with a tuple of BaseAttributeModel.
    """
    model = BaseAttributesModel(
        attributes=(
            MyStrAttr(value="hello"),
            MyIntAttr(value=123),
        )
    )
    assert len(model.attributes) == 2
    assert model.attributes[0].value == "hello"
    assert model.attributes[1].value == 123


def test_attributes_to_model_empty():
    """
    Test that attributes_to_model with an empty list produces a model with no fields.
    """
    ReturnModel = attributes_to_model([])
    assert issubclass(ReturnModel, BaseModel)
    assert len(ReturnModel.model_fields) == 0

    # Try instantiating it
    instance = ReturnModel()
    # Should have no attributes
    assert instance.model_dump() == {}


def test_attributes_to_model_single_attribute():
    """
    Test that attributes_to_model with a single attribute
    creates a model with one corresponding field.
    """
    ReturnModel = attributes_to_model([MyStrAttr])
    # The field name should be the default of the 'key' field for MyStrAttr
    assert "my_str_attr" in ReturnModel.model_fields
    assert ReturnModel.model_fields["my_str_attr"].annotation == MyStrAttr

    # Instantiate
    instance = ReturnModel(my_str_attr=MyStrAttr(value="hello"))
    assert instance.my_str_attr.value == "hello"

    # If we pass a type mismatch or no value for 'my_str_attr', we should see a ValidationError
    with pytest.raises(ValidationError):
        ReturnModel(my_str_attr=MyStrAttr(value=123))  # 123 is not a string

    # With no attribute, also should fail validation because it's a required field
    # (unless you made it optional; depends on your design)
    with pytest.raises(ValidationError):
        ReturnModel()


def test_attributes_to_model_multiple_attributes():
    """
    Test that multiple attributes become multiple fields in the returned model.
    """
    ReturnModel = attributes_to_model([MyStrAttr, MyIntAttr, MyBoolAttr])
    expected_fields = {"my_str_attr", "my_int_attr", "my_bool_attr"}
    assert expected_fields == set(ReturnModel.model_fields.keys())

    # Valid instantiation
    instance = ReturnModel(
        my_str_attr=MyStrAttr(value="abc"),
        my_int_attr=MyIntAttr(value=42),
        my_bool_attr=MyBoolAttr(value=True),
    )
    assert instance.my_str_attr.value == "abc"
    assert instance.my_int_attr.value == 42
    assert instance.my_bool_attr.value is True

    # Missing one field => ValidationError (unless you make fields optional)
    with pytest.raises(ValidationError):
        ReturnModel(
            my_str_attr=MyStrAttr(value="xyz"),
            my_int_attr=MyIntAttr(value=24),
            # no my_bool_attr
        )


def test_attributes_to_model_validation_errors():
    """
    More nuanced test for errors in the dynamic model fields.
    """
    ReturnModel = attributes_to_model([MyIntAttr])

    # Attempt to assign a string to 'my_int_attr.value' which is an int
    with pytest.raises(ValidationError) as exc_info:
        ReturnModel(my_int_attr=MyIntAttr(value="not-an-int"))
    # We can look at the error output if needed
    error_msg = str(exc_info.value)
    assert (
        "type_error.integer" in error_msg
        or "Input should be a valid integer" in error_msg
    )


@pytest.mark.parametrize(
    "attrs, expected_field_names",
    [
        ([], []),
        ([MyIntAttr], ["my_int_attr"]),
        ([MyStrAttr, MyBoolAttr], ["my_str_attr", "my_bool_attr"]),
    ],
)
def test_attributes_to_model_param(attrs, expected_field_names):
    """
    Parametrized test to ensure the dynamic model has the right field names.
    """
    ReturnModel = attributes_to_model(attrs)
    actual_fields = list(ReturnModel.model_fields.keys())
    assert actual_fields == expected_field_names
