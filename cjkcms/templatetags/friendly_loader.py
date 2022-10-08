"""
https://github.com/ataylor32/django-friendly-tag-loader/blob/master/src/friendlytagloader/templatetags/friendly_loader.py
Sadly, this repo has not been updated for 3 years
"""
import contextlib

from django import template
from django.template.base import TokenType
from django.template.defaulttags import (
    CommentNode,
    IfNode,
    LoadNode,
    find_library,
    load_from_library,
)
from django.template.smartif import Literal

register = template.Library()


@register.tag
def friendly_load(parser, token):
    """
    Tries to load a custom template tag set. Non existing tag libraries
    are ignored.

    This means that, if used in conjunction with ``if_has_tag``, you can try to
    load the comments template tag library to enable comments even if the
    comments framework is not installed.

    For example::

        {% load friendly_loader %}
        {% friendly_load comments webdesign %}

        {% if_has_tag render_comment_list %}
            {% render_comment_list for obj %}
        {% else %}
            {% if_has_tag lorem %}
                {% lorem %}
            {% endif_has_tag %}
        {% endif_has_tag %}
    """
    bits = token.contents.split()
    if len(bits) >= 4 and bits[-2] == "from":
        # from syntax is used; load individual tags from the library
        name = bits[-1]
        with contextlib.suppress(template.TemplateSyntaxError):
            lib = find_library(parser, name)
            subset = load_from_library(lib, name, bits[1:-2])
            parser.add_library(subset)
    else:
        # one or more libraries are specified; load and add them to the parser
        for name in bits[1:]:
            with contextlib.suppress(template.TemplateSyntaxError):
                lib = find_library(parser, name)
                parser.add_library(lib)
    return LoadNode()


def do_if_has_tag(parser, token, negate=False):
    """
    The logic for both ``{% if_has_tag %}`` and ``{% if not_has_tag %}``.

    Checks if all the given tags exist (or not exist if ``negate`` is ``True``)
    and then only parses the branch that will not error due to non-existing
    tags.

    This means that the following is essentially the same as a
    ``{% comment %}`` tag::

      {% if_has_tag non_existing_tag %}
          {% non_existing_tag %}
      {% endif_has_tag %}

    Another example is checking a built-in tag. This will always render the
    current year and never FAIL::

      {% if_has_tag now %}
          {% now "Y" %}
      {% else %}
          FAIL
      {% endif_has_tag %}
    """
    bits = list(token.split_contents())
    if len(bits) < 2:
        raise template.TemplateSyntaxError("%r takes at least one arguments" % bits[0])
    end_tag = f"end{bits[0]}"
    has_tag = all(tag in parser.tags for tag in bits[1:])
    has_tag = (not negate and has_tag) or (negate and not has_tag)
    nodelist_true = nodelist_false = CommentNode()
    if has_tag:
        nodelist_true = parser.parse(("else", end_tag))
        token = parser.next_token()
        if token.contents == "else":
            parser.skip_past(end_tag)
    else:
        while parser.tokens:
            token = parser.next_token()
            if token.token_type == TokenType.BLOCK and token.contents == end_tag:
                return IfNode(
                    [(Literal(has_tag), nodelist_true), (None, nodelist_false)]
                )
            elif token.token_type == TokenType.BLOCK and token.contents == "else":
                break
        nodelist_false = parser.parse((end_tag,))
        parser.next_token()
    return IfNode([(Literal(has_tag), nodelist_true), (None, nodelist_false)])


@register.tag
def if_has_tag(parser, token):
    """
    Do something if all given tags are loaded::

       {% load friendly_loader %}
       {% friendly_load webdesign %}

       {% if_has_tag lorem %}
            {% lorem %}
       {% else %}
            Non dummy content goes here!
       {% endif_has_tag %}

    When given multiple arguments each and every tag in the list has to be
    available. This means that the following will render nothing::

       {% if_has_tag now nonexisting_tag %}
           {% now "Y" %}
       {% endif_has_tag %}
    """
    return do_if_has_tag(parser, token)


@register.tag
def ifnot_has_tag(parser, token):
    """
    Do something unless any given tag is loaded::

       {% load friendly_loader %}
       {% friendly_load comments %}

       {% ifnot_has_tag render_comment_list %}
            Comment support has been disabled.
       {% else %}
            {% render_comment_list for obj %}
       {% endifnot_has_tag %}

    In the case of multiple arguments, the condition will trigger if any tag in
    the list is unavailable. This means that the following will still render
    the current year::

       {% ifnot_has_tag now nonexisting_tag %}
           {% now "Y" %}
       {% endifnot_has_tag %}
    """
    return do_if_has_tag(parser, token, True)
