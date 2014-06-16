#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import time
import sys
from datetime import date
from pprint import pprint

import click
from lxml.html import fromstring
from selenium import webdriver

CZ_MONTHS = {
    'března': 3,
    'dubna': 4,
    'května': 5,
    'června': 6,
}
GOOGLE_GROUP_BASE = 'https://groups.google.com/forum/'
GOOGLE_GROUP_URL = GOOGLE_GROUP_BASE + '#!forum/{}'
LOGGER = logging.getLogger(__name__)


def date_parse(raw_date):
    tokens = raw_date.split()
    day = int(tokens[1].strip('.'))
    month = CZ_MONTHS[tokens[2]]
    year = int(tokens[3])
    return date(year, month, day)


def thread_to_dict(thread):
    parsed = {'name': thread.xpath('.//a[@class="GIEUOX-DPL"]')[0].text}
    parsed['url'] = thread.xpath('.//a[@class="GIEUOX-DPL"]')[0].attrib['href']
    raw_last_change = thread.xpath('.//span[@class="GIEUOX-DOQ"]/span'
        )[0].attrib['title']
    last_change = date_parse(raw_last_change)
    parsed['month'] = last_change.month
    info = thread.xpath('.//span[@class="GIEUOX-DOQ"]')
    parsed['seen'] = int(info[1].text.split()[0])
    parsed['posts'] = int(info[0].text.split()[0])
    return parsed


def get_posts(settings, group):
    try:
        group_id = group if group else settings['google_group_name']
    except KeyError:
        LOGGER.error('Google Group name not defined')
        sys.exit()
    group_url = GOOGLE_GROUP_URL.format(group_id)
    browser = webdriver.PhantomJS()
    browser.set_window_size(1024, 768)
    browser.get(group_url)
    time.sleep(5)
    frontpage = fromstring(browser.page_source)
    browser.quit()
    frontpage.make_links_absolute(GOOGLE_GROUP_BASE)
    html_threads = frontpage.xpath('//div[@class="GIEUOX-DEQ"]')
    threads = (thread_to_dict(thread) for thread in html_threads)
    return [
        thread for thread in threads if thread['month'] >= settings['month']]


def score(post):
    return post['seen'] + post['posts']


def curate(posts, count=3):
    active = [post for post in posts if score(post) > 1]
    best = sorted(active, key=lambda post: score(post))[-count:]
    for post in best:
        summary = {
            'name': post['name'],
            'url': post['url'],
        }
        yield summary


@click.command()
@click.option('--group', help='Group ID')
@click.pass_context
def cli(ctx, group):
    """Google Groups curator"""
    monthly_posts = get_posts(ctx.obj['SETTINGS'], group)
    best_posts = curate(monthly_posts)
    for post in best_posts:
        pprint(post)
