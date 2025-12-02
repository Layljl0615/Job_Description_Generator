from django import template
from chatbot.utils import render_job_description

register = template.Library()


@register.filter
def jd_to_html(text: str) -> str:
    """
    Render the stored job description markdown into safe HTML.
    """
    return render_job_description(text or "")
