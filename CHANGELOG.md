# Changelog

All notable changes to docx-json-replacer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-01-15

### Added
- 🎨 **Table Support**: Create formatted Word tables from JSON data
- 🎨 **Color Styling**: Support for background colors, text colors, bold, and italic formatting
- 📊 **Multiple Table Formats**: 
  - Styled tables with custom colors and formatting
  - Simple list tables from nested arrays
  - Auto-header generation from dictionary data
  - HTML table parsing and conversion
- 📝 **Enhanced Documentation**: Comprehensive README with examples and color reference
- 🧪 **Table Handler Module**: Dedicated module for table processing logic
- ✅ **Comprehensive Tests**: Added tests for all table functionality

### Changed
- 🔧 **Improved DocxReplacer**: Integrated table detection and creation directly into main class
- 📚 **Updated Dependencies**: Added python-docx >= 0.8.11 requirement
- 🚀 **Better Performance**: Optimized placeholder detection and replacement

### Fixed
- 🐛 Fixed issue where table data was rendered as plain text instead of actual tables
- 🐛 Fixed placeholder replacement for nested JSON structures
- 🐛 Improved HTML content cleaning

## [0.3.0] - 2024-12-XX

### Added
- Initial release with basic text replacement functionality
- CLI tool for command-line usage
- Python API for programmatic usage
- Support for nested JSON keys with dot notation
- HTML content cleaning

## [0.1.0] - 2024-XX-XX

### Added
- Project initialization
- Basic DOCX template replacement
- Simple JSON data support