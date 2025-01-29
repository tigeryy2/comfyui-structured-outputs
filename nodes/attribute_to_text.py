from ..comfyui_structured_outputs.attribute_utils import BaseAttributeModel


class AttributeToTextNode:
    NAME: str = "AttributeToTextNode"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_out",)
    CATEGORY = "structured_output"
    FUNCTION = "get_text"
    OUTPUT_NODE: bool = True

    INPUT_IS_LIST: bool = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "attributes": ("ATTRIBUTE", {}),
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
        attributes: [BaseAttributeModel],
        format_text: [str],
        extra_pnginfo,
        unique_id,
    ):
        # handle padded input lists
        format_text: str = format_text[0]
        if format_text is None:
            format_text = ""

        # convert attribute to key value pairs
        mapping: dict[str, str] = {
            key: value["value"] for key, value in attributes[0].model_dump().items()
        }

        # replace {key} with value
        formatted_text: str = format_text.format(**mapping)
        return (formatted_text,)
