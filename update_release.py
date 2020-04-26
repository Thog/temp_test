#!/usr/bin/env python3

import json
import re
import os
import sys
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

def get_assets_by_pattern(pattern):
    result = []
    for asset in event_data['release']['assets']:
        regex_result = re.search(pattern, asset['name'])
        if regex_result:
            result.append(asset)

    return result

def convert_release_to_build_type(release_type):
    if release_type in ['release', 'debug']:
        return release_type
    
    # TODO: legacy, remove
    if release_type == 'profiled':
        release_type = 'profile release'
    
    if release_type in ['profile release', 'profile debug']:
        release_type_part = release_type.split(' ')[1].capitalize()

        return 'profile' + release_type_part
    
    return 'unknown'

def construct_artefact_info(asset):
    file_name = os.path.basename(asset['name'])

    file_name_without_ext = os.path.splitext(file_name)[0]


    sha256sum_file_asset = get_asset_by_name(file_name_without_ext + '.sha256')

    raw_part = file_name_without_ext.split('-')[1:]

    if len(raw_part) < 4:
        return None

    release_type = raw_part[0].lower()
    target_os = raw_part[2]
    target_arch = raw_part[3]

    if sha256sum_file_asset is not None:
        sha256sum_file_content = request.urlopen(sha256sum_file_asset['browser_download_url']).read().strip().decode('utf-8')
        sha256sum = sha256sum_file_content.split(' ')[1]
    else:
        sha256sum = None

    return {'arch': target_arch, 'buildType': convert_release_to_build_type(release_type), 'fileName': file_name, 'fileHash': sha256sum, 'os': target_os, 'url': asset['browser_download_url']}

artifacts = []

for asset in get_assets_by_pattern("(.*).zip"):
    res = construct_artefact_info(asset)

    if res is None:
        print("%s got rejected, aborting!" % asset['name'])
        sys.exit(1)
    artifacts.append(res)

if len(artifacts) == 0:
    print('No artifacts in release, aborting!')
    sys.exit(1)

release_info = { 'version': event_data['release']['name'], 'artifacts': artifacts }

with open("latest.json", "w") as f:
    f.write(json.dumps(release_info, sort_keys=True, indent=4))

with open(release_info['version'] + ".json", "w") as f:
    f.write(json.dumps(release_info, sort_keys=True, indent=4))
