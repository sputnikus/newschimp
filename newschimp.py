#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click

import renderer
import sender
from social import fb, gg, lanyrd
from cli import cli_group
from utils import ComplexCLI, load_settings


def create_newsletter(settings):
    pass


cli_group.add_command(fb.cli)
cli_group.add_command(gg.cli)
cli_group.add_command(lanyrd.cli)

@cli_group.command(cls=ComplexCLI, invoke_without_command=True)
@click.option('--config', help='Custom config file', type=click.Path(
    exists=True, file_okay=True, resolve_path=True), default='config.yaml')
@click.pass_context
def main(ctx, config):
    ctx.obj['SETTINGS'] = load_settings(config)
    create_newsletter(ctx.obj['SETTINGS'])


if __name__ == '__main__':
    main(obj={})
