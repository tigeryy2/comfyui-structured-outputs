from __future__ import annotations

from typing import Literal

from pydantic import Field, create_model

from ..comfyui_structured_outputs.attribute_utils import (
    ATTRIBUTE_TYPES,
    BaseAttributeModel,
    string_to_type,
)
from ..comfyui_structured_outputs.utils.loggable import Loggable


class AttributeNode(Loggable):
    NAME: str = "AttributeNode"
    RETURN_TYPES = ("ATTRIBUTE",)
    RETURN_NAMES = ("attributes",)
    CATEGORY = "structured_output"
    FUNCTION = "init_attribute"

    INPUT_IS_LIST: bool = True
    OUTPUT_IS_LIST: bool = (True,)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "name": ("STRING", {}),
                "attribute_type": (["str", "int", "float", "bool"],),
            },
            "optional": {
                "attributes_in": ("ATTRIBUTE", {}),
                "description": ("STRING", {"multiline": True}),
                "example": ("STRING", {"multiline": True}),
                "options": ("STRING", {"multiline": True}),
            },
        }

    @classmethod
    def VALIDATE_INPUTS(
        cls,
        name: str,
        attribute_type: str,
        attributes_in: [BaseAttributeModel] = None,
        description: str | None = None,
        example: str | None = None,
    ):
        name: str = name[0]
        attribute_type: str = attribute_type[0]

        if not name:
            AttributeNode.log().error(msg := "Attribute name cannot be empty")
            raise ValueError(msg)

        if attribute_type not in ATTRIBUTE_TYPES:
            AttributeNode.log().error(
                msg
                := f"Invalid attribute type: '{attribute_type}' is not in '{ATTRIBUTE_TYPES.keys()}'"
            )
            raise ValueError(msg)

        return True

    def init_attribute(
        self,
        name: [str],
        attribute_type: [str],
        attributes_in: [BaseAttributeModel] = None,
        description: [str] = None,
        example: [str] = None,
        options: [str] = None,
    ):
        # since all inputs are lists and padded to the same length, we can just take the first element
        name: str = name[0]
        attribute_type: str = attribute_type[0]
        description: str = description[0]
        example: str = example[0]
        options: str = options[0]

        # except for attributes, which we want to keep as a list
        if not attributes_in:
            attributes_in = []

        attribute_model = create_model(
            f"{name}Model",
            # force the "key" to be the name of the attribute
            key=(Literal[name], Field(default=name, description="Attribute name")),
            value=(
                string_to_type(attribute_type, options=options),
                Field(description=description, examples=[example]),
            ),
            __base__=BaseAttributeModel,
        )

        # concat the attributes_in and the new attribute_model
        # since outputs are list, we need to return a tuple of list
        return (attributes_in + [attribute_model],)
