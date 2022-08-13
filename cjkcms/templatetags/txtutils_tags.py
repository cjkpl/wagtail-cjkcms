from django import template
from typing import TypeVar

register = template.Library()
T = TypeVar("T")


@register.tag(name="captureas")
def do_captureas(parser, token):
    """
    Capture content for re-use throughout a template.
    particularly handy for use within social meta fields
    that are virtually identical.
    """
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError as e:
        raise template.TemplateSyntaxError(
            "'captureas' node requires a variable name."
        ) from e

    nodelist = parser.parse(("endcaptureas",))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)


class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ""


@register.simple_tag
def assign(variable: T) -> T:
    return variable


@register.filter
def in_list(value, the_list):
    """
    Returns true if value is in comma-separated list built from the_list string
    """
    value = str(value)
    return value in the_list.split(",")
