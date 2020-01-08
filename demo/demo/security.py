"""
Dummy security module. Provides fake security functions
"""
import bleach

BLEACH_VALID_TAGS = ['p', 'b', 'strong', 'em', 'i', 'u', 'strike', 'ul', 'li',
                     'ol', 'br', 'span', 'blockquote', 'hr', 'a', 'img', 'h1',
                     'h2', 'h3', 'h4', 'h5', 'h6', 'table', 'caption', 'th',
                     'tr', 'td', 'tbody']
BLEACH_VALID_ATTRS = {
    'span': ['style', ],
    'p': ['align', 'style'],
    'a': ['href', 'rel', 'target', 'name'],
    'img': ['src', 'alt', 'style'],
    'div': ['style', ],
}
BLEACH_VALID_STYLES = ['color', 'cursor', 'float', 'margin', 'width',
                       'background-color']


def clean(obj):
    """
    Use tags from settings to bleach an object.
    """
    return bleach.clean(
        obj,
        BLEACH_VALID_TAGS,
        BLEACH_VALID_ATTRS,
        BLEACH_VALID_STYLES,
    )


def clean_alert(input_string):
    """
    Fake cleaner. Will remove "alert" in the input_string
    """
    return input_string.replace("alert", "")
