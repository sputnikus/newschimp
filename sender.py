#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import click
import mailchimp

from utils import load_settings


def new_campaign(api, settings):
    text_file = open(settings['text_output'], 'r')
    html_file = open(settings['html_output'], 'r')
    resp = api.campaigns.create(
        'auto',
        {
            'list_id': settings['mail_list'],
            'subject': settings['subject'],
            'from_email': settings['sender']['email'],
            'from_name': settings['sender']['name'],
            'to_name': settings['reciever'],
        },
        {
            'html': html_file.read(),
            'text': text_file.read(),
        })
    if resp['status'] = 'error':
        print('Something is terribly wrong')
        print(resp['code'], ' ', resp['error'])
    text_file.close()
    html_file.close()


@click.command()
@click.option('--config', help='Custom config file')
@click.option('--key', help='Mailchimp API key')
@click.option('--html', help='HTML file for campaign')
def main(config, key):
    settings = load_settings(config)
    api = mailchimp.Mailchimp(
        key if key else os.environ.get('MAILCHIMP_KEY'))
    new_campaign(api, settings)
