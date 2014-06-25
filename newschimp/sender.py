#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

import click
import mailchimp

from .cli import cli_group

LOGGER = logging.getLogger(__name__)


def new_campaign(settings, key):
    api = mailchimp.Mailchimp(key)
    text_file = open(settings['output']['text'], 'r')
    html_file = open(settings['output']['html'], 'r')
    chimp_settings = settings['mailchimp']
    resp = api.campaigns.create(
        'regular',
        {
            'list_id': chimp_settings['list'],
            'subject': chimp_settings['subject'],
            'from_email': chimp_settings['sender']['email'],
            'from_name': chimp_settings['sender']['name'],
            'to_name': chimp_settings['reciever'],
        },
        {
            'html': html_file.read(),
            'text': text_file.read(),
        })
    if resp['status'] == 'error':
        LOGGER.error('MailChimp API error: ')
        LOGGER.error(' '.join((resp['code'], resp['error'])))
    text_file.close()
    html_file.close()


@cli_group.command(short_help='Campaign creation')
@click.option('--key', help='Mailchimp API key', envvar='MAILCHIMP_KEY')
@click.pass_context
def cli(ctx, key):
    new_campaign(ctx.obj['SETTINGS'], key)
