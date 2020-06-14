#!/usr/bin/env python

import requests
import re
import docker

ORIGINAL_IMAGE="homeassistant/home-assistant"
CUSTOM_IMAGE="skaronator/home-assistant-stable"
CUSTOM_IMAGE_TAG="{}:latest".format(CUSTOM_IMAGE)
TAG_URL="https://hub.docker.com/v2/repositories/{}/tags".format(ORIGINAL_IMAGE)


# This function return false for all invalid tags
# Invalid tags are usually static tags likt latest and beta but also
# dev branch builds as well as beta builds
def validate_tag(tag: str):
  if (tag in ['latest', 'rc', 'beta', 'dev', 'stable']):
    return False

  # Remove tags ending with dev and 8 digit number
  if (re.compile(r".*\.dev\d{8}$").match(tag)):
    return False

  # Remove tags ending with .0b and 1-2 digit number
  if (re.compile(r".*.0b\d{1,2}$").match(tag)):
    return False

  return True


# Return a list of all tags for a given page number
def get_tags(page: int):
  url = '{}?page={}'.format(TAG_URL, page)
  print('get_tags(): GET {}'.format(url))
  resp = requests.get(url)
  if resp.status_code != 200:
    raise Exception('GET {} {}'.format(url, resp.status_code))
  
  results = resp.json()['results']
  tags = list(map((lambda x: x['name']), results))
  valid_tags = list(filter(validate_tag, tags))

  print('get_tags(): allTags: {}'.format(tags))
  print('get_tags(): valid_tags: {}'.format(valid_tags))
  return valid_tags


def get_last_stable(tags: list):
  print('get_last_stable(): tags {}'.format(tags))
  # Returns the highest number for a defined position in a semver version 
  # position 0 = major
  # position 1 = minor
  def get_highest_version(position: int) -> int:
    versions = map((lambda x: int(x.split(".")[position:(position+1)][0])), tags)
    return max(list(versions))

  max_minor = get_highest_version(1)
  stable_version = [0, 0, 0]

  for tag in tags:
    major, minor, patch = (int(x) for x in tag.split("."))

    # select the penultimate minor version
    if (max_minor-1 != minor):
      continue

    # Make sure that we get the highest patch version
    if (stable_version[2] < patch):
      stable_version = [major, minor, patch]

  stable_tag = ".".join(str(x) for x in stable_version)
  print('get_last_stable(): stable_tag {}'.format(stable_tag))
  return stable_tag


def pull_push_image(tag: str):
  client = docker.from_env()

  hass_tag = '{}:{}'.format(ORIGINAL_IMAGE, tag)
  print('get_last_stable(): docker pull {}'.format(hass_tag))
  image = client.images.pull(hass_tag)

  print('get_last_stable(): docker tag {}'.format(CUSTOM_IMAGE_TAG))
  image.tag(CUSTOM_IMAGE_TAG)

  print('get_last_stable(): docker push {}'.format(CUSTOM_IMAGE_TAG))
  for line in client.images.push(CUSTOM_IMAGE_TAG, stream=True, decode=True):
    print(line)

  return True


if __name__ == '__main__':
  # We just get the last 5 pages. Usually 2 is enough and/or the logic could be improve
  # to load only as many pages as we need but honestly this is fine
  tags = []
  for x in range(1, 6):
    tags += get_tags(x)
  
  tag = get_last_stable(tags)
  pull_push_image(tag)