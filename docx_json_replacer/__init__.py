from .docx_replacer import DocxReplacer, replace_docx_template
from .table_handler import TableHandler
from .formatting_handler import FormattingHandler
from .image_handler import ImageHandler

__version__ = "0.9.1"
__all__ = ["DocxReplacer", "replace_docx_template", "TableHandler", "FormattingHandler", "ImageHandler"]