#!/usr/bin/env python2.7

import click
import json
import requests
import time


def list_file_ids(channel, token, count, print_len=False):
    """
    Using a legacy token https://api.slack.com/custom-integrations/legacy-tokens
    and Slack's files.list API, we GET a JSON blob with files metadata, which
    we then form into a list of IDs.
    """
    uri = 'https://slack.com/api/files.list'
    params = {'token': token, 'channel': channel, 'count': count}

    response = requests.get(uri, params=params)
    files = json.loads(response.text)['files']

    file_ids = [ x['id'] for x in files ]
    if print_len:
        print 'This channel has {} file(s).'.format(len(file_ids))

    return file_ids


def delete_files(token, file_ids, rate_limit):
    """
    Pass in file IDs and use the files.delete API method to delete a file.
    
    Uses rate_limit to pause between each API call.
    """
    uri = 'https://slack.com/api/files.delete'
    for file_id in file_ids:
        params = {'token': token, 'file': file_id}
        print "Deleting file {}".format(file_id)
        response = requests.post(uri, params=params)
        print "Status code: {}".format(response.status_code)
        if rate_limit:
            time.sleep(rate_limit)


# By default '-h' doesn't give print help.
# http://click.pocoo.org/5/documentation/#help-parameter-customization
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)

@click.option('--token', '-t', required=True, help=("A user token, which you can get"
              "from https://api.slack.com/custom-integrations/legacy-tokens."
              "Be absolutely certain to not share this token with anyone.")
              )
@click.option('--channel', '-c', required=True, help='Encoded channel ID.')
@click.option('--count', default=1000, help='Number of files to delete at once.')
@click.option('--delete', default=False, is_flag=True, help='Set --delete if you want to actually delete files.')
@click.option('--print', 'print_len', is_flag=True, flag_value=True, default=True, help='Set --print to see number of files.')
@click.option('--rate-limit', '-r', default=1, help='Time to wait between each API call. Reference the rate limits here: https://api.slack.com/docs/rate-limits#tiers.')
def main(token, channel, count, print_len, delete, rate_limit):
    file_ids = list_file_ids(channel, token, count, print_len)
    if delete:
        delete_files(token, file_ids, rate_limit)


if __name__ == "__main__":
    main()
