"""
ImageHandler for docx-json-replacer
Handles parsing and inserting images from base64 data into DOCX documents.
"""
import base64
import io
import re
from typing import Any, Dict, List, Optional, Union


class ImageHandler:
    """Handles image detection, parsing, and insertion from base64 data"""

    # Supported image formats
    SUPPORTED_FORMATS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

    # Inline image pattern: [dx-img:image_key]
    INLINE_IMAGE_PATTERN = re.compile(r'\[dx-img:([^\]]+)\]')

    @staticmethod
    def has_inline_images(text: str) -> bool:
        """
        Check if text contains inline image tags.

        Args:
            text: Text to check

        Returns:
            True if text contains [dx-img:key] tags
        """
        if not isinstance(text, str):
            return False
        return bool(ImageHandler.INLINE_IMAGE_PATTERN.search(text))

    @staticmethod
    def find_inline_images(text: str) -> List[str]:
        """
        Find all inline image references in text.

        Args:
            text: Text to search

        Returns:
            List of image keys referenced in the text
        """
        if not isinstance(text, str):
            return []
        return ImageHandler.INLINE_IMAGE_PATTERN.findall(text)

    @staticmethod
    def is_image_data(value: Any) -> bool:
        """
        Check if the value represents image data (single image).

        Args:
            value: Value to check

        Returns:
            True if value is a single image specification
        """
        if not isinstance(value, dict):
            return False

        # Must have type == 'image'
        if value.get('type') != 'image':
            return False

        # Must have 'data' (base64) and not be a list
        if 'list' in value:
            return False

        return 'data' in value

    @staticmethod
    def is_image_list_data(value: Any) -> bool:
        """
        Check if the value represents a list of images.

        Args:
            value: Value to check

        Returns:
            True if value is a list of images specification
        """
        if not isinstance(value, dict):
            return False

        # Must have type == 'image' or 'images'
        if value.get('type') not in ('image', 'images'):
            return False

        # Must have 'list' array
        if 'list' not in value:
            return False

        return isinstance(value.get('list'), list)

    @staticmethod
    def decode_base64_image(data: str) -> bytes:
        """
        Decode base64 image data to bytes.

        Args:
            data: Base64 encoded string (with or without data URI prefix)

        Returns:
            Decoded image bytes
        """
        # Remove data URI prefix if present (e.g., "data:image/png;base64,")
        if data.startswith('data:'):
            # Find the comma that separates metadata from data
            comma_idx = data.find(',')
            if comma_idx != -1:
                data = data[comma_idx + 1:]

        # Remove any whitespace
        data = re.sub(r'\s', '', data)

        return base64.b64decode(data)

    @staticmethod
    def get_image_stream(data: str) -> io.BytesIO:
        """
        Convert base64 data to a BytesIO stream for python-docx.

        Args:
            data: Base64 encoded image string

        Returns:
            BytesIO stream containing the image
        """
        image_bytes = ImageHandler.decode_base64_image(data)
        return io.BytesIO(image_bytes)

    @staticmethod
    def parse_dimension(dim: Union[str, int, float, None]) -> Optional[int]:
        """
        Parse dimension string to EMUs (English Metric Units) for python-docx.

        Args:
            dim: Dimension value like "5cm", "2in", "100pt", "200px", or numeric (assumes cm)

        Returns:
            Dimension in EMUs, or None if not specified/invalid
        """
        if dim is None:
            return None

        if isinstance(dim, (int, float)):
            # Assume centimeters if numeric
            from docx.shared import Cm
            return Cm(float(dim))

        if not isinstance(dim, str):
            return None

        dim = dim.strip().lower()

        if dim == 'auto':
            return None

        try:
            from docx.shared import Cm, Inches, Pt, Emu

            if dim.endswith('cm'):
                return Cm(float(dim[:-2]))
            elif dim.endswith('in'):
                return Inches(float(dim[:-2]))
            elif dim.endswith('pt'):
                return Pt(float(dim[:-2]))
            elif dim.endswith('px'):
                # Approximate: 1px ≈ 0.75pt
                return Pt(float(dim[:-2]) * 0.75)
            elif dim.endswith('emu'):
                return int(float(dim[:-3]))
            else:
                # Try to parse as cm if no unit
                return Cm(float(dim))
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def process_single_image(image_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single image specification.

        Args:
            image_spec: Dictionary with image data and options

        Returns:
            Processed image info ready for insertion
        """
        data = image_spec.get('data', '')
        format_hint = image_spec.get('format', 'png').lower()

        # Parse dimensions
        width = ImageHandler.parse_dimension(image_spec.get('width'))
        height = ImageHandler.parse_dimension(image_spec.get('height'))

        # Get alignment (default: left)
        alignment = image_spec.get('alignment', 'left').lower()
        if alignment not in ('left', 'center', 'right'):
            alignment = 'left'

        return {
            'data': data,
            'format': format_hint,
            'width': width,
            'height': height,
            'alignment': alignment,
            'stream': ImageHandler.get_image_stream(data) if data else None
        }

    @staticmethod
    def process_image_list(image_list_spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process a list of images specification.

        Args:
            image_list_spec: Dictionary with 'list' array of image specs

        Returns:
            List of processed image infos ready for insertion
        """
        images = []
        image_list = image_list_spec.get('list', [])

        # Get default values from parent spec
        default_width = image_list_spec.get('width')
        default_height = image_list_spec.get('height')
        default_alignment = image_list_spec.get('alignment', 'left')
        default_format = image_list_spec.get('format', 'png')

        # Get layout option (vertical, horizontal, grid)
        layout = image_list_spec.get('layout', 'vertical').lower()
        if layout not in ('vertical', 'horizontal', 'grid'):
            layout = 'vertical'

        # Get spacing between images
        spacing = image_list_spec.get('spacing', '0.5cm')

        for img_spec in image_list:
            if not isinstance(img_spec, dict):
                continue

            # Merge with defaults
            processed = ImageHandler.process_single_image({
                'data': img_spec.get('data', ''),
                'format': img_spec.get('format', default_format),
                'width': img_spec.get('width', default_width),
                'height': img_spec.get('height', default_height),
                'alignment': img_spec.get('alignment', default_alignment),
            })

            if processed['stream']:
                images.append(processed)

        return images, layout, spacing

    @staticmethod
    def validate_image_spec(spec: Dict[str, Any]) -> tuple:
        """
        Validate an image specification.

        Args:
            spec: Image specification dictionary

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(spec, dict):
            return False, "Image spec must be a dictionary"

        if spec.get('type') not in ('image', 'images'):
            return False, "Missing or invalid 'type' field"

        # For single image
        if 'data' in spec and 'list' not in spec:
            data = spec.get('data', '')
            if not data:
                return False, "Empty 'data' field"
            try:
                ImageHandler.decode_base64_image(data)
            except Exception as e:
                return False, f"Invalid base64 data: {e}"
            return True, None

        # For image list
        if 'list' in spec:
            img_list = spec.get('list', [])
            if not isinstance(img_list, list):
                return False, "'list' must be an array"
            if len(img_list) == 0:
                return False, "'list' is empty"

            for i, img in enumerate(img_list):
                if not isinstance(img, dict):
                    return False, f"Item {i} in list must be a dictionary"
                if 'data' not in img:
                    return False, f"Item {i} missing 'data' field"
                try:
                    ImageHandler.decode_base64_image(img.get('data', ''))
                except Exception as e:
                    return False, f"Item {i} has invalid base64 data: {e}"

            return True, None

        return False, "Missing 'data' or 'list' field"
