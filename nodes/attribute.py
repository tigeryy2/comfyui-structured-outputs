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
    RETURN_NAMES = ("attribute",)
    CATEGORY = "structured_output"
    FUNCTION = "init_attribute"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "name": ("STRING", {}),
                "attribute_type": (["str", "int", "float", "bool"],),
            },
            "optional": {
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
        description: str | None = None,
        example: str | None = None,
    ):
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
        name: str,
        attribute_type: str,
        description: str | None = None,
        example: str | None = None,
        options: str | None = None,
    ):
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
        return [attribute_model]
