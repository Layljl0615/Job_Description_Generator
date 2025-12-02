import re
from django.utils.html import escape
from django.utils.safestring import mark_safe


def render_job_description(text: str) -> str:
    """
    Convert stored JD markdown-like text into safe HTML with uppercase bold labels.
    """
    if not text:
        return ""

    escaped = escape(text)

    formatted = re.sub(
        r"\*\*(.+?)\*\*",
        lambda match: f"<strong>{match.group(1).upper()}</strong>",
        escaped,
    )
    formatted = re.sub(r"(^|\n)-\s*", r"\1• ", formatted)
    formatted = formatted.replace("\n", "<br>")

    return mark_safe(formatted)
