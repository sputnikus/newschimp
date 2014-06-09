#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from datetime import date
from pprint import pprint

import click
from lxml.html import fromstring
from selenium import webdriver

from ..utils import load_settings, CZ_MONTHS

GOOGLE_GROUP_BASE = 'https://groups.google.com/forum/'
GOOGLE_GROUP_URL = GOOGLE_GROUP_BASE + '#!forum/{}'


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


def get_posts(settings):
    group_url = GOOGLE_GROUP_URL.format(settings['group_name'])
    browser = webdriver.PhantomJS()
    browser.set_window_size(1024, 768)
    browser.get(group_url)
    time.sleep(5)
    browser.save_screenshot('screen.png')
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
        summary = [
            post['name'],
            post['url'],
        ]
        yield summary


@click.command()
@click.option('--config', help='Custom config file')
def main(config):
    settings = load_settings(config)
    monthly_posts = get_posts(settings)
    best_posts = curate(monthly_posts)
    for post in best_posts:
        pprint(post)

if __name__ == '__main__':
    main()
