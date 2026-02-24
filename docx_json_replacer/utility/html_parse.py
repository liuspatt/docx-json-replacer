import re
from typing import Union, List, Any, Dict


def clean_html_content(value: str) -> str:
    """Convert HTML content to plain text, preserving structure."""
    if not isinstance(value, str):
        return value

    # Return plain text with formatting markers
    return _clean_plain_text_with_formatting_markers(value)


def has_html_formatting(value: str) -> bool:
    """Check if value contains HTML formatting tags that need special handling."""
    if not isinstance(value, str):
        return False
    # Check for bold, italic, underline tags
    return bool(re.search(r'<(b|strong|i|em|u)(\s[^>]*)?>.*?</\1>', value, re.IGNORECASE | re.DOTALL))


def parse_html_to_runs(html_text: str) -> List[Dict[str, Any]]:
    """
    Parse HTML text and return list of formatted text parts for Word runs.

    Each part is a dict with:
    - 'text': The text content
    - 'bold': True if text should be bold
    - 'italic': True if text should be italic
    - 'underline': True if text should be underlined

    Args:
        html_text: HTML string to parse

    Returns:
        List of dicts representing formatted text runs
    """
    if not isinstance(html_text, str):
        return [{'text': str(html_text)}]

    # Handle line breaks first
    html_text = html_text.replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')

    # Handle paragraphs
    html_text = re.sub(r'<p[^>]*>', '', html_text)
    html_text = html_text.replace('</p>', '\n')

    # Convert HTML entities
    html_text = _convert_html_entities(html_text)

    parts = []
    current_text = []
    format_stack = {'bold': 0, 'italic': 0, 'underline': 0}
    i = 0

    while i < len(html_text):
        if html_text[i] == '<':
            # Find the end of the tag
            tag_end = html_text.find('>', i)
            if tag_end == -1:
                # Malformed tag, treat as text
                current_text.append(html_text[i])
                i += 1
                continue

            tag = html_text[i:tag_end+1]
            tag_lower = tag.lower()

            # Check if we have accumulated text to save
            if current_text:
                text = ''.join(current_text)
                if text:  # Include whitespace-only text too
                    part = {'text': text}
                    if format_stack['bold'] > 0:
                        part['bold'] = True
                    if format_stack['italic'] > 0:
                        part['italic'] = True
                    if format_stack['underline'] > 0:
                        part['underline'] = True
                    parts.append(part)
                current_text = []

            # Handle opening/closing tags
            if re.match(r'<(b|strong)(\s[^>]*)?>$', tag_lower):
                format_stack['bold'] += 1
            elif re.match(r'</(b|strong)>$', tag_lower):
                format_stack['bold'] = max(0, format_stack['bold'] - 1)
            elif re.match(r'<(i|em)(\s[^>]*)?>$', tag_lower):
                format_stack['italic'] += 1
            elif re.match(r'</(i|em)>$', tag_lower):
                format_stack['italic'] = max(0, format_stack['italic'] - 1)
            elif re.match(r'<u(\s[^>]*)?>$', tag_lower):
                format_stack['underline'] += 1
            elif re.match(r'</u>$', tag_lower):
                format_stack['underline'] = max(0, format_stack['underline'] - 1)
            # Skip other tags (remove them)

            i = tag_end + 1
        else:
            current_text.append(html_text[i])
            i += 1

    # Don't forget any remaining text
    if current_text:
        text = ''.join(current_text)
        if text:
            part = {'text': text}
            if format_stack['bold'] > 0:
                part['bold'] = True
            if format_stack['italic'] > 0:
                part['italic'] = True
            if format_stack['underline'] > 0:
                part['underline'] = True
            parts.append(part)

    # If no parts were created, return empty text
    if not parts:
        return [{'text': ''}]

    return parts


def _clean_plain_text(value: str) -> str:
    """Clean HTML without formatting - just extract text."""
    # Convert HTML tables to plain text format
    if '<table>' in value:
        value = _convert_html_table_plain(value)
    
    # Convert HTML lists to plain text format
    if '<ul>' in value or '<ol>' in value:
        value = _convert_html_lists_plain(value)
    
    # Convert paragraphs and line breaks
    value = re.sub(r'<p[^>]*>', '\n\n', value)
    value = re.sub(r'</p>', '', value)
    value = re.sub(r'<br[^>]*/?>', '\n', value)
    
    # Remove all HTML tags
    value = re.sub(r'<[^>]+>', '', value)
    
    # Convert HTML entities
    value = _convert_html_entities(value)
    
    # Clean up extra whitespace
    value = re.sub(r'\n\s*\n\s*\n', '\n\n', value)
    value = re.sub(r'[ \t]+', ' ', value)
    
    return value.strip()


def _clean_plain_text_with_formatting_markers(value: str) -> str:
    """Clean HTML and add formatting markers for display."""
    # Convert HTML tables to plain text format
    if '<table>' in value:
        value = _convert_html_table_plain(value)
    
    # Convert HTML lists to plain text format
    if '<ul>' in value or '<ol>' in value:
        value = _convert_html_lists_plain(value)
    
    # Mark bold text with asterisks (common convention)
    value = re.sub(r'<(b|strong)>(.*?)</\1>', r'**\2**', value, flags=re.IGNORECASE)
    
    # Mark headings as bold with clear separation
    for i in range(1, 7):
        value = re.sub(rf'<h{i}[^>]*>(.*?)</h{i}>', rf'\n\n**\1**\n', value, flags=re.IGNORECASE)
    
    # Mark italic text
    value = re.sub(r'<(i|em)>(.*?)</\1>', r'*\2*', value, flags=re.IGNORECASE)
    
    # Mark underlined text
    value = re.sub(r'<u>(.*?)</u>', r'_\1_', value, flags=re.IGNORECASE)
    
    # Convert paragraphs and line breaks
    value = re.sub(r'<p[^>]*>', '\n\n', value)
    value = re.sub(r'</p>', '', value)
    value = re.sub(r'<br[^>]*/?>', '\n', value)
    
    # Remove remaining HTML tags
    value = re.sub(r'<[^>]+>', '', value)
    
    # Convert HTML entities
    value = _convert_html_entities(value)
    
    # Clean up extra whitespace
    value = re.sub(r'\n\s*\n\s*\n', '\n\n', value)
    value = re.sub(r'[ \t]+', ' ', value)
    
    return value.strip()


def _convert_html_table_plain(value: str) -> str:
    """Convert HTML table to plain text."""
    # Extract table headers
    headers = re.findall(r'<th[^>]*>(.*?)</th>', value, flags=re.IGNORECASE)
    
    # Extract table rows
    rows = []
    row_matches = re.findall(r'<tr[^>]*>(.*?)</tr>', value, flags=re.IGNORECASE)
    
    for row_html in row_matches:
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row_html, flags=re.IGNORECASE)
        if cells:
            # Clean any nested HTML in cells
            cells = [re.sub(r'<[^>]+>', '', cell) for cell in cells]
            rows.append(cells)
    
    # Format as plain text table
    if not rows:
        return ''
    
    # Calculate column widths
    all_rows = rows
    if headers:
        all_rows = [headers] + rows
    
    max_widths = []
    for i in range(max(len(row) for row in all_rows) if all_rows else 0):
        max_width = max(len(str(row[i])) if i < len(row) else 0 for row in all_rows)
        max_widths.append(max(max_width, 8))  # Minimum width of 8
    
    # Build table
    result = []
    
    # Add headers if present
    if headers:
        header_line = ' | '.join(headers[i].ljust(max_widths[i]) if i < len(headers) else ''.ljust(max_widths[i]) for i in range(len(max_widths)))
        separator = ' | '.join('-' * max_widths[i] for i in range(len(max_widths)))
        result.append(header_line)
        result.append(separator)
        rows = rows[1:] if len(rows) > 1 and headers == rows[0] else rows
    
    # Add data rows
    for row in rows:
        row_line = ' | '.join(str(row[i]).ljust(max_widths[i]) if i < len(row) else ''.ljust(max_widths[i]) for i in range(len(max_widths)))
        result.append(row_line)
    
    return '\n'.join(result)


def _convert_html_lists_plain(value: str) -> str:
    """Convert HTML lists to plain text."""
    # Convert ordered lists
    ol_pattern = r'<ol[^>]*>(.*?)</ol>'
    ol_matches = re.findall(ol_pattern, value, flags=re.IGNORECASE | re.DOTALL)
    
    for ol_content in ol_matches:
        items = re.findall(r'<li[^>]*>(.*?)</li>', ol_content, flags=re.IGNORECASE | re.DOTALL)
        formatted_items = []
        for i, item in enumerate(items, 1):
            clean_item = re.sub(r'<[^>]+>', '', item).strip()
            formatted_items.append(f'{i}. {clean_item}')
        
        list_text = '\n'.join(formatted_items)
        value = re.sub(ol_pattern, list_text, value, count=1, flags=re.IGNORECASE | re.DOTALL)
    
    # Convert unordered lists
    ul_pattern = r'<ul[^>]*>(.*?)</ul>'
    ul_matches = re.findall(ul_pattern, value, flags=re.IGNORECASE | re.DOTALL)
    
    for ul_content in ul_matches:
        items = re.findall(r'<li[^>]*>(.*?)</li>', ul_content, flags=re.IGNORECASE | re.DOTALL)
        formatted_items = []
        for item in items:
            clean_item = re.sub(r'<[^>]+>', '', item).strip()
            formatted_items.append(f'• {clean_item}')
        
        list_text = '\n'.join(formatted_items)
        value = re.sub(ul_pattern, list_text, value, count=1, flags=re.IGNORECASE | re.DOTALL)
    
    return value


def _convert_html_entities(value: str) -> str:
    """Convert HTML entities to their character equivalents."""
    # Common HTML entities
    entities = {
        '&nbsp;': ' ',
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&#39;': "'",
        '&apos;': "'",
        '&copy;': '©',
        '&reg;': '®',
        '&trade;': '™',
        '&mdash;': '—',
        '&ndash;': '–',
        '&hellip;': '...',
        '&laquo;': '«',
        '&raquo;': '»',
        '&ldquo;': '"',
        '&rdquo;': '"',
        '&lsquo;': ''',
        '&rsquo;': ''',
    }
    
    for entity, replacement in entities.items():
        value = value.replace(entity, replacement)
    
    # Handle numeric entities
    value = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), value)
    value = re.sub(r'&#x([0-9a-fA-F]+);', lambda m: chr(int(m.group(1), 16)), value)
    
    return value