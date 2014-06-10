#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
from utils import load_settings


@click.group()
@click.pass_context
def cli(ctx):
    """Group collector"""
