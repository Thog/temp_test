#!/usr/bin/env python3

import json
import os
from urllib import request


event_path = os.environ['GITHUB_EVENT_PATH']

with open(event_path, "r") as f:
    event_data = json.load(f)

if event_data['action'] != 'published':
    print("Invalid state to trigger this action")
    exit(1)

def get_asset_by_name(name):
    for asset in event_data['release']['assets']:
        if asset['name'] == name:
            return asset
    return None

release_info_asset = get_asset_by_name('release_information.json')

if release_info_asset == None:
    print("release_information.json couldn't be found on the published release")
    exit(1)

 # TODO
exit(1)