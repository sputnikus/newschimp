#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import click
from lxml.html import fromstring
from jinja2 import Environment, FileSystemLoader
from typogrify.filters import typogrify

from utils import load_settings


def render(settings):
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    context = {k.upper(): v for k, v in settings['context'].items()}
    html_output = env.get_template(settings['template']).render(**context)
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


@click.command()
@click.option('--config', help='Custom config file')
@click.option('--template', help='Template file')
def main(config, template):
    settings = load_settings(config)
    if template:
        settings['template'] = template
    render(settings)


if __name__ == '__main__':
    main()
