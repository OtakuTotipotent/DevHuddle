from django import template
import markdown

register = template.Library()


@register.filter(name="render_markdown")
def render_markdown(text):
    """Converts markdown text to safe HTML"""
    if not text:
        return ""
    return markdown.markdown(text, extensions=["extra", "nl2br", "sane_lists"])
