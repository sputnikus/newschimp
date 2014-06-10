#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import click
from lxml.html import fromstring
from jinja2 import Environment, FileSystemLoader
from typogrify.filters import typogrify

from cli import cli_group 


def render_files(settings, template, context={}):
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    if 'context' in settings:
        settings['context'].update(context)
    else:
        settings['context'] = context 
    full_context = {k.upper(): v for k, v in settings['context'].items()}
    try:
        used_template = template if template else settings['template']
    except KeyError:
        print('Some error shit') # TODO: Logging
        sys.exit()
    html_output = env.get_template(settings['template']).render(**full_context)
    text_output = fromstring(html_output).text_content()
    typo_output = typogrify(html_output)
    if settings.get('html_output'):
        with open(settings['html_output'], 'w') as html:
            html.write(typo_output)
        if settings.get('text_output'):
            with open(settings['text_output'], 'w') as text:
                text.write(text_output)
    else:
        print(text_output)


@cli_group.command(short_help='HTML and text email rendering')
@click.option('--template', help='Template file', type=click.Path(
    exists=True, file_okay=True, resolve_path=True))
@click.pass_context
def cli(ctx, template):
    render_files(ctx.obj['SETTINGS'], template)
