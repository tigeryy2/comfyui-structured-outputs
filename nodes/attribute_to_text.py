from ..comfyui_structured_outputs.attribute_utils import BaseAttributeModel


class AttributeToTextNode:
    NAME: str = "AttributeToTextNode"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_out",)
    CATEGORY = "structured_output"
    FUNCTION = "get_text"
    OUTPUT_NODE: bool = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "attribute": ("ATTRIBUTE", {}),
                "format_text": (
                    "STRING",
                    {
                        "multiline": True,
                    },
                ),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    def get_text(
        self,
        attribute: BaseAttributeModel,
        format_text: str,
        extra_pnginfo,
        unique_id,
    ):
        if format_text is None:
            format_text = ""

        # convert attribute to key value pairs
        mapping: dict[str, str] = {attribute.key: str(attribute.value)}

        formatted_text: str = format_text.format(**mapping)

        return [formatted_text]
