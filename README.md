# docx-json-replacer

Replace template placeholders in DOCX files with JSON data. Supports text replacement in paragraphs, table cells, and dynamic table generation.

## Features

- Replace `{{placeholder}}` markers in DOCX files with JSON data
- **Handles placeholders in paragraphs AND table cells**
- Supports keys with dots (e.g., `part.borrower_name`)
- Automatic HTML tag cleaning
- Dynamic table generation from JSON arrays
- Table styling support (colors, bold, italic)

## Installation

```bash
pip install docx-json-replacer
```

## Usage

### Command Line

```bash
# Basic usage
docx-json-replacer template.docx data.json -o output.docx

# Without -o flag, creates template_replaced.docx
docx-json-replacer template.docx data.json
```

### Python API

```python
from docx_json_replacer import DocxReplacer

# Create replacer instance
replacer = DocxReplacer('template.docx')

# Replace with JSON data
json_data = {
    "customer_name": "John Doe",
    "date": "2024-01-01",
    "amount": "$1,000.00"
}
replacer.replace_from_json(json_data)

# Save the result
replacer.save('output.docx')
```

## Template Format

In your DOCX file, use double curly braces for placeholders:

```
Dear {{customer_name}},

Your invoice dated {{date}} for {{amount}} is ready.
```

Placeholders work in:
- Regular paragraphs
- Table cells
- Headers and footers

## JSON Data Format

### Simple Text Replacement

```json
{
    "customer_name": "John Doe",
    "date": "2024-01-01",
    "amount": "$1,000.00"
}
```

### Keys with Dots

```json
{
    "part.borrower_name": "ACME Corp",
    "part.borrower_address": "123 Main St"
}
```

### Table Data

For dynamic table generation, use arrays:

```json
{
    "invoice_items": [
        {"cells": ["Item 1", "2", "$50.00"]},
        {"cells": ["Item 2", "3", "$75.00"]}
    ]
}
```

With styling:

```json
{
    "styled_table": [
        {
            "cells": ["Header 1", "Header 2"],
            "style": {"bg": "4472C4", "color": "FFFFFF", "bold": true}
        },
        {
            "cells": ["Data 1", "Data 2"]
        }
    ]
}
```

## Complete Example

### Template (template.docx)
```
Contract Number: {{contract_number}}
Client: {{client.name}}
Address: {{client.address}}

Items:
{{items}}
```

### Data (data.json)
```json
{
    "contract_number": "2024-001",
    "client.name": "ABC Corporation",
    "client.address": "456 Business Ave",
    "items": [
        {"cells": ["Product", "Qty", "Price"], "style": {"bold": true}},
        {"cells": ["Widget A", "10", "$100"]},
        {"cells": ["Widget B", "5", "$200"]}
    ]
}
```

### Command
```bash
docx-json-replacer template.docx data.json -o contract_2024_001.docx
```

## Requirements

- Python 3.7+
- python-docx
- docxtpl

## License

MIT