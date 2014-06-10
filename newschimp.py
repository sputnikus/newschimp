#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click

import renderer
import sender
from social import fb, gg, lanyrd
from cli import cli
from utils import ComplexCLI, load_settings


cli.add_command(fb.cli)
cli.add_command(gg.cli)
cli.add_command(lanyrd.cli)

@cli.command(cls=ComplexCLI)
@click.option('--config', help='Custom config file', type=click.Path(
    exists=True, file_okay=True, resolve_path=True), default='config.yaml')
@click.pass_context
def main(ctx, config):
    ctx.obj['SETTINGS'] = load_settings(config)


if __name__ == '__main__':
    main(obj={})
