#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import sys

import click

from newschimp import renderer, sender
from newschimp.social import fb, gg, lanyrd
from newschimp.cli import cli_group
from newschimp.utils import ComplexCLI, load_settings

LOGGER = logging.getLogger(__name__)


def create_newsletter(settings):
    """Newsletter creation based on config and env variables"""
    context = {}
    try:
        fb_posts = fb.get_posts(settings, os.environ['FACEBOOK_TOKEN'], None)
    except KeyError:
        LOGGER.error('Facebook Token not defined')
        sys.exit()
    click.echo('[1/4] Getting Facebook Group posts')
    context['fb'] = fb.curate(fb_posts)
    ggroup_posts = gg.get_posts(settings, None)
    click.echo('[2/4] Getting Google Group posts')
    context['gg'] = gg.curate(ggroup_posts)
    click.echo('[3/4] Getting upcoming Lanyrd meetups')
    context['meetups'] = lanyrd.meetup_loop(settings)
    click.echo('[4/4] Rendering mail')
    renderer.render_files(settings, None, context)
    click.confirm(
        'Content is rendered, would you like to send it now?', abort=True)
    click.echo('Creating MailChimp campaign')
    sender.new_campaign(settings, os.environ.get('MAILCHIMP_KEY'))


cli_group.add_command(fb.cli)
cli_group.add_command(gg.cli)
cli_group.add_command(lanyrd.cli)

@cli_group.command(cls=ComplexCLI, invoke_without_command=True)
@click.option('--config', help='Custom config file', type=click.Path(
    exists=True, file_okay=True, resolve_path=True), default='config.yaml')
@click.pass_context
def main(ctx, config):
    ctx.obj['SETTINGS'] = load_settings(config)
    if ctx.invoked_subcommand is None:
        create_newsletter(ctx.obj['SETTINGS'])


if __name__ == '__main__':
    main(obj={})
