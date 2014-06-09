#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import click
from jinja2 import Environment, FileSystemLoader
from typogrify.filters import typogrify

from utils import load_settings


def render(settings):
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    context = {k.upper(): v for k, v in settings['context'].items()}
    output = env.get_template(settings['template']).render(**context)
    typo_output = typogrify(output)
    if settings.get('mail_render'):
        with open(settings['mail_render'], 'w') as html:
            html.write(typo_output)
    print(typo_output)


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
