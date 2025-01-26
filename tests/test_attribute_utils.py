# test_string_to_type.py
import pytest
from pydantic import BaseModel, ValidationError

from comfyui_structured_outputs.attribute_utils import string_to_type


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
    assert (
        returned_type is expected_type
    ), f"Expected '{attr_type}' to map to {expected_type}, but got {returned_type}."


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
