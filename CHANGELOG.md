# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0] - 2024-09-30

### Added
- **HTML Formatting Support in Table Cells**
  - Support for `<b>`, `<strong>`, `<i>`, `<em>`, `<u>` tags for text formatting
  - Support for `<br>` line breaks and `<p>` paragraph tags
  - Smart handling of malformed HTML (unclosed tags, duplicate opening tags)

- **Cell-Level Styling**
  - Individual styling for each cell in a table row
  - New `cell_styles` array property for per-cell customization
  - Mixed styling support (row defaults with cell overrides)
  - Inline cell objects with `content` and `style` properties

- **Improved HTML Parser**
  - Sequential character-by-character parsing for better accuracy
  - Handles duplicate opening tags as closing tags
  - Properly processes nested and malformed HTML structures

### Changed
- Updated dependencies: `docxcompose>=1.3.0` (was `docxtpl>=0.20.0`)
- Improved table generation performance
- Better error handling for invalid table data

### Fixed
- Fixed issue where multiple `<b>` tags would make all text between them bold
- Fixed HTML tag processing in table cells preserving proper formatting
- Fixed style application priority (cell > row > default)

## [0.5.1] - 2024-01-15

### Fixed
- Bug fixes in table cell replacement

## [0.5.0] - 2024-01-10

### Added
- Table support with dynamic generation from JSON arrays
- Row-level styling for tables
- Background colors, text colors, bold, and italic support

## [0.4.0] - 2023-12-20

### Added
- Support for placeholders in table cells
- Batch processing capabilities

### Changed
- Improved placeholder detection algorithm

## [0.3.0] - 2023-11-15

### Added
- Support for nested JSON keys with dots (e.g., `client.name`)
- Command-line interface

## [0.2.0] - 2023-10-10

### Added
- HTML tag cleaning
- Support for headers and footers

## [0.1.0] - 2023-09-01

### Added
- Initial release
- Basic placeholder replacement in paragraphs
- JSON file support
- Python API