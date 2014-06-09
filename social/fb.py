#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pprint import pprint

import click
import requests as req

from ..utils import load_settings

FACEBOOK_TOKEN = os.environ.get('FACEBOOK_TOKEN')
FACEBOOK_GROUP_URL = 'https://graph.facebook.com/v2.0/{}/feed'


def get_posts(settings, token):
    if not token:
        token = FACEBOOK_TOKEN
    group_uri = FACEBOOK_GROUP_URL.format(settings['group_id'])
    payload = {
        'limit': 10000,
        'access_token': token,
        'since': settings['since']
    }
    posts = req.get(group_uri, params=payload)
    return posts.json()['data']


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
        summary = [
            post['actions'][0]['link'],
            post['from']['name'],
        ]
        if 'message' in post:
            summary.append(post['message'])
        if 'link' in post:
            summary.append(post['name'])
            summary.append(post['link'])
        yield summary


@click.command()
@click.option('--token', help='Facebook token')
@click.option('--config', help='Custom config file')
def main(token, config):
    settings = load_settings(config)
    monthly_posts = get_posts(settings, token)
    best_posts = curate(monthly_posts)
    for post in best_posts:
        pprint(post)


if __name__ == '__main__':
    main()
