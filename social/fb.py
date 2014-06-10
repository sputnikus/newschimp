#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from pprint import pprint

import click
import requests as req

FACEBOOK_GROUP_URL = 'https://graph.facebook.com/v2.0/{}/feed'


def get_posts(settings, token, group):
    if not token:
        token = FACEBOOK_TOKEN
    try:
        group_id = group if group else settings['group_id']
    except KeyError:
        print('Some error shit') # TODO: Logging
        sys.exit()
    group_uri = FACEBOOK_GROUP_URL.format(group_id)
    payload = {
        'limit': 10000,
        'access_token': token,
        'since': settings['since']
    }
    posts = req.get(group_uri, params=payload)
    try:
        return posts.json()['data']
    except KeyError:
        print(posts.json()['error'])
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


@click.command(short_help='Facebook curator')
@click.option('--group', help='Group ID')
@click.option('--token', help='Facebook token', envvar='FACEBOOK_TOKEN')
@click.pass_context
def cli(ctx, token, group):
    monthly_posts = get_posts(ctx.obj['SETTINGS'], token, group)
    best_posts = curate(monthly_posts)
    for post in best_posts:
        pprint(post)
