# Documentation Home

## Nodes

- Attribute Node: a single attribute with name, description, type (int, string, select, boolean) examples, and (optional) options
- Prompt Node: Just a text literal (or image literal later on) that is sent as the prompt
- Completion Node: A node used to call the LLM and get the output
- Text Template Node: f-string style template for generating text output, inject attributes into a string