#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from datetime import datetime
from pprint import pprint

import click
import requests as req
from lxml.html import fromstring

LANYRD_BASE = 'http://lanyrd.com/'
LANYRD_URL = LANYRD_BASE + 'search/?q={}'


@asyncio.coroutine
def get_search(event):
    search_url = LANYRD_URL.format(event)
    search_results = req.get(search_url)
    frontpage = fromstring(search_results.text)
    frontpage.make_links_absolute(LANYRD_BASE)
    results = frontpage.xpath('//li[@class="s-conference s-result"]')
    return results


@asyncio.coroutine
def get_next_meetup(event, month):
    search = yield from get_search(event)
    for event in search:
        meetup_date = event.xpath('.//p[@class="date"]/abbr'
            )[0].attrib['title']
        parsed_date = datetime.strptime(meetup_date, '%Y-%m-%d')
        if parsed_date.month < month:
            continue
        event_node = event.xpath('.//h3/a')[0]
        return {
            'name': event_node.text,
            'url': event_node.attrib['href']
        }


@asyncio.coroutine
def scrape_meetups(settings):
    results = []
    for event in settings['events']:
        meetup = yield from get_next_meetup(event, settings['month'])
        results.append(meetup)
    return results


def meetup_loop(settings):
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(scrape_meetups(settings))
    loop.close()
    return results


@click.command(short_help='Meetup listing')
@click.pass_context
def cli(ctx):
    meetups = meetup_loop(ctx.obj['SETTINGS'])
    for meetup in meetups:
        pprint(meetup)
