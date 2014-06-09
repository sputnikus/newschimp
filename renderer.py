#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import click
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from typogrify.filters import typogrify

from utils import load_settings


def render(settings):
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    context = {k.upper(): v for k, v in settings['context'].items()}
    html_output = env.get_template(settings['template']).render(**context)
    text_output = BeautifulSoup(html_output).get_text()
    typo_output = typogrify(html_output)
    if settings.get('mail_render'):
        with open(settings['html_output'], 'w') as html:
            html.write(typo_output)
        with open(settings['text_output'], 'w') as text:
            text.write(typo_output)
    else:
        print(text_output)


@click.command()
@click.option('--config', help='Custom config file')
@click.option('--template', help='Template file')
@click.option('--output', help='Output file')
def main(config, template, output):
    settings = load_settings(config)
    if template:
        settings['template'] = template
    if output:
        settings['mail_render'] = output
    render(settings)


if __name__ == '__main__':
    main()
