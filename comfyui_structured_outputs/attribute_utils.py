from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, create_model


class BaseAttributeModel(BaseModel):
    key: str
    value: Any
    error: str | None = Field(default=None, description="Error message if any")


ATTRIBUTE_TYPES: dict[str, Any] = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
}


def string_to_type(value: str, options: str | None = None) -> Any:
    if value not in ATTRIBUTE_TYPES:
        raise ValueError(
            f"Invalid attribute type: '{value}' is not in '{list(ATTRIBUTE_TYPES.keys())}'"
        )

    attribute_type = ATTRIBUTE_TYPES[value]
    if not options:
        # No “choice” options were specified; return the basic type
        return attribute_type

    # split and remove leading/trailing whitespace
    options = [opt.strip() for opt in options.split(",")]

    # Convert each option to the underlying type
    if attribute_type is bool:
        # booleans need to be handled differently, since "false" and "False" both evaluate to True
        option_values = [opt.lower() == "true" for opt in options]
    else:
        option_values = [attribute_type(opt) for opt in options]

    # for Python 3.11+:
    #   return Literal[*option_values]
    #
    # Otherwise, use __getitem__ with a tuple:
    return Literal.__getitem__(tuple(option_values))


class BaseAttributesModel(BaseModel):
    attributes: tuple[BaseAttributeModel, ...]


def attributes_to_model(
    attributes: list[type[BaseAttributeModel]],
) -> type[BaseAttributesModel]:
    # Bundles a list of attributes into a single model
    return create_model(
        "ReturnModel",
        **{attr.model_fields["key"].default: (attr, Field()) for attr in attributes},
    )
