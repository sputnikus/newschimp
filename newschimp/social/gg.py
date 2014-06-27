#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    newschimp.social.gg
    ~~~~~~~~~~~~~~~~~~~

    Google Group curator

    :author: Martin Putniorz
    :year: 2014
'''
import gettext
import logging
import time
import sys
from datetime import date
from pprint import pprint

import click
from lxml import etree
from lxml.html import fromstring
from selenium import webdriver

t = gettext.translation('gg', 'locale', fallback=True)
_ = t.gettext

MONTHS = {
    _('january'): 1,
    _('february'): 2,
    _('march'): 3,
    _('april'): 4,
    _('may'): 5,
    _('june'): 6,
    _('july'): 7,
    _('august'): 8,
    _('september'): 9,
    _('october'): 10,
    _('november'): 11,
    _('december'): 12,
}
GOOGLE_GROUP_BASE = 'https://groups.google.com/forum/'
GOOGLE_GROUP_URL = GOOGLE_GROUP_BASE + '#!forum/{}'
LOGGER = logging.getLogger(__name__)


def date_parse(raw_date):
    '''Make some sense for default Group datetime string'''
    tokens = raw_date.split()
    day = int(tokens[1].strip('.'))
    month = MONTHS[tokens[2]]
    year = int(tokens[3])
    return date(year, month, day)


def thread_to_dict(thread):
    '''Serialize Group thread into Python dictionary'''
    parsed = {'name': thread.xpath('.//a')[0].text}
    parsed['url'] = thread.xpath('.//a')[0].attrib['href']
    raw_last_change = thread.xpath('.//span[@title]'
        )[0].attrib['title']
    last_change = date_parse(raw_last_change)
    parsed['month'] = last_change.month
    info = thread.xpath('.//div[contains(@style,"right")]')[0]
    parsed['seen'] = int(info.xpath('.//span[@class]')[3].text.split()[0])
    parsed['posts'] = int(info.xpath('.//span[@class]')[4].text.split()[0])
    return parsed


def get_posts(settings, group):
    '''Gets Group posts using PhantomJS and lxml'''
    try:
        group_id = group if group else settings['google']['group_name']
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
    html_threads = frontpage.xpath('//div[@role="listitem"]')
    threads = (thread_to_dict(thread) for thread in html_threads)
    return [
        thrd for thrd in threads if thrd['month'] >= settings['month']]


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
    '''Google Groups curator'''
    monthly_posts = get_posts(ctx.obj['SETTINGS'], group)
    best_posts = curate(monthly_posts)
    for post in best_posts:
        pprint(post)
