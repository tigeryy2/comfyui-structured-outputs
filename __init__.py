from .comfyui_structured_outputs import DOTENV_FILE
from .comfyui_structured_outputs.utils.loggable import Loggable
from .nodes.attribute import AttributeNode
from .nodes.attribute_to_text import AttributeToTextNode
from .nodes.structured_output import StructuredOutputNode

NODE_CLASS_MAPPINGS = {
    AttributeNode.NAME: AttributeNode,
    StructuredOutputNode.NAME: StructuredOutputNode,
    AttributeToTextNode.NAME: AttributeToTextNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    AttributeNode.NAME: "Attribute",
    StructuredOutputNode.NAME: "Structured Output",
    AttributeToTextNode.NAME: "Attribute to Text",
}

__all__ = ["NODE_CLASS_MAPPINGS"]

Loggable.log().info(
    f"[Structured Output] Loaded {len(NODE_CLASS_MAPPINGS)} Structured Output nodes"
)

if not DOTENV_FILE.exists():
    Loggable.log().error(
        f"File '{DOTENV_FILE}' does not exist, please add a .env file with your API keys\n"
        f"See the README for more information"
    )
