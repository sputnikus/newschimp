#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import sys
import time
from datetime import datetime
from pprint import pprint

import click
import requests as req

FACEBOOK_GROUP_URL = 'https://graph.facebook.com/v2.0/{}/feed'
LOGGER = logging.getLogger(__name__)


def get_posts(settings, token, group):
    try:
        group_id = group if group else settings['facebook']['group_id']
    except KeyError:
        LOGGER.error('Facebook Group id not defined')
        sys.exit()
    group_uri = FACEBOOK_GROUP_URL.format(group_id)
    epoch_since = time.mktime(datetime(
        datetime.now().year,
        settings['month'],
        1).timetuple())
    payload = {
        'limit': 10000,
        'access_token': token,
        'since': epoch_since,
    }
    posts = req.get(group_uri, params=payload)
    try:
        return posts.json()['data']
    except KeyError:
        LOGGER.error('Facebook API error:')
        LOGGER.error(posts.json()['error'])
        sys.exit()


def score(post):
    try:
        temp_score = len(post['likes']['data'])
    except KeyError:
        temp_score = 0
    try:
        for comment in post['comments']['data']:
            temp_score += comment['like_count']
    finally:
        return temp_score


def curate(posts, count=5):
    active = [post for post in posts if score(post) > 1]
    best = sorted(active, key=lambda post: score(post))[-count:]
    for post in best:
        summary = {
            'fb_url': post['actions'][0]['link'],
            'from': post['from']['name'],
        }
        if 'message' in post:
            summary['message'] = post['message']
        if 'link' in post:
            try:
                summary['link_name'] = post['name']
                summary['link_url'] = post['link']
            except KeyError:
                summary['message'] = post['message']
        yield summary


@click.command(short_help='Facebook curator')
@click.option('--group', help='Group ID')
@click.option('--token', help='Facebook token', envvar='FACEBOOK_TOKEN')
@click.pass_context
def cli(ctx, token, group):
    monthly_posts = get_posts(ctx.obj['SETTINGS'], token, group)
    best_posts = curate(monthly_posts)
    for post in best_posts:
        pprint(post)
