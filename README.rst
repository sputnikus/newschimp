NewsChimp
=========

Generator of monthly newsletter campaigns on MailChimp. Based od laziness and boredom.


Status
------

In heavy development. Please touch anything important for fun.


Usage
-----

.. code-block:: bash

    $ python3 newschimp.py --help
    Usage: newschimp.py [OPTIONS] COMMAND [ARGS]...

    Options:
    --config PATH  Custom config file
    --help         Show this message and exit.

    Commands:
    fb        Facebook curator
    gg        Google Groups curator
    lanyrd    Meetup listing
    renderer  HTML and text email rendering
    sender    Campaign creation

If you want to use subcommand with config, do it in format

.. code-block:: bash

    $ python3 newschimp.py --config PATH command


Config
------

Default config file is ``./config.yaml``. Here's minimalistic setting:

.. code-block:: yaml
    month:
    facebook_group_id:
    # Oldest facebook post epoch time
    since:
    google_group_name:
    # Events for lanyrd to search
    events:
        -
    # Input template
    template:
    context:
        # Additional template context
        header:
    # Template outputs
    html_output:
    text_output:
    # MailChimp settings
    mail_list:
    subject:
    reciever:
    sender:
        email:
        name:

You also need to setup environment variables (for automatic campaign creation):

- ``FACEBOOK_TOKEN``
- ``MAILCHIMP_KEY``


Requirements
------------

Python 3 and stuff in ``requirements.txt``


License
-------

See LICENSE file


TODO
----

- Newsletter creation wizard
- Support of more social sources
- Better config structure

