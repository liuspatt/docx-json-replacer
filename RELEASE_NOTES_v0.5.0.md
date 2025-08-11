# Release Notes - docx-json-replacer v0.5.0

## 🎉 Major Release: Table Support with Colors and Formatting

### Release Date: January 15, 2025

### Overview
Version 0.5.0 introduces comprehensive table support, allowing users to create professional Word documents with formatted tables directly from JSON data. This release transforms docx-json-replacer from a simple text replacement tool into a powerful document generation system.

## ✨ Key Features

### 📊 Table Creation from JSON
- Create real Word tables, not just text replacements
- Support for multiple table formats
- Automatic table detection and insertion

### 🎨 Rich Formatting Options
- **Background Colors**: Custom cell backgrounds using hex codes
- **Text Colors**: White text on dark backgrounds, colored text
- **Text Styles**: Bold and italic formatting
- **Professional Layouts**: Alternating row colors, styled headers

### 📝 Multiple Data Formats
1. **Styled Tables**: Full control over cell appearance
2. **Simple Lists**: Quick tables from nested arrays
3. **Dictionary Tables**: Auto-generate headers from object keys
4. **HTML Parsing**: Convert HTML tables to Word tables

## 📋 What's New

### Added
- `TableHandler` class for table processing
- Integrated table support in `DocxReplacer`
- Comprehensive test suite for table functionality
- Color styling system
- HTML table parsing
- Auto-header generation

### Improved
- Enhanced placeholder detection
- Better JSON structure handling
- Optimized document processing
- Comprehensive documentation

### Fixed
- Table data rendering as plain text
- Placeholder replacement issues
- Nested JSON structure handling

## 📦 Installation

```bash
pip install --upgrade docx-json-replacer
```

## 🚀 Quick Example

```python
from docx_json_replacer import DocxReplacer

data = {
    "company": "TechCorp",
    "sales": [
        {"cells": ["Month", "Revenue"], "style": {"bg": "4472C4", "color": "FFFFFF", "bold": True}},
        {"cells": ["January", "$100K"], "style": {"bg": "F2F2F2"}},
        {"cells": ["February", "$120K"], "style": {"bg": "FFFFFF"}}
    ]
}

replacer = DocxReplacer("template.docx")
replacer.replace_from_json(data)
replacer.save("report.docx")
```

## 📚 Documentation

Full documentation and examples available in the updated README.md

## 🔄 Migration from v0.3.0

No breaking changes! Your existing code will continue to work. Table support is automatically detected when your JSON contains:
- Lists of dictionaries with 'cells' key
- Lists of lists
- HTML table strings

## 🧪 Testing

All tests passing:
- 15 unit tests for table handler
- 5 CLI tests
- Integration tests

## 📊 Package Files

- **Source**: `docx_json_replacer-0.5.0.tar.gz`
- **Wheel**: `docx_json_replacer-0.5.0-py3-none-any.whl`
- **Size**: ~15KB

## 🙏 Acknowledgments

Thanks to all contributors and users who provided feedback for this release.

## 📝 License

MIT License

---

For issues or questions, please visit: https://github.com/liuspatt/docx-json-replacer