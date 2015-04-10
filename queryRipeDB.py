#
# Find the subnet of ipaddresses in the Ripe Database
#
# Usage:
# Feed this script with ip addresses via stdin, one ip address per line.
# This script queries the Ripe Database for routing objects containing these ip addresses.
# The script returns the subnet of the ip address, one subnet per line.
#
# Copyright Martin Schimandl 2015
#
# References:
# https://github.com/RIPE-NCC/whois/wiki/WHOIS%20REST%20API%20WhoisResources
# http://docs.python-requests.org/en/latest/user/quickstart/
#

import requests # pip install requests
import json
import sys

# enable debug output on stderr
debug = 0


def writeDebug(message):
  if debug:
    sys.stderr.write(message)


def queryRipeDB( querystring ):
  headers = {
    'Accept': 'application/json'
  }

  payload= {
    'source': [
      'ripe',
      'radb-grs',
      'apnic-grs',
      'lacnic-grs',
      'arin-grs',
      'afrinic-grs',
      'ripe-grs',
    ],
    'query-string': querystring,
    'type': 'route'
  }

  return requests.get('http://rest.db.ripe.net/search',
    params=payload, headers=headers)


def fetchFirstRoute( response ):
  objects = response.json()['objects']['object']
  for obj in objects:
    if obj['type'] != 'route':
      writeDebug('Ignoring non route object of type %s' % obj['type']);
      continue
    else:
      writeDebug(json.dumps(obj, indent=2, separators=(',',': ')))
      return obj
  writeDebug('error no route objects found')
  return None


def fetchRouteAttribute( route ):
  if not 'primary-key' in route:
    return None

  if not 'attribute' in route['primary-key']:
    return None

  for attrib in route['primary-key']['attribute']:
    if attrib['name'] != 'route':
      writeDebug('Ignoring attribute of name %s' % attrib['name']);
      continue
    return attrib['value']


def subnetFromIpAddress(address):
  writeDebug('checking address %s' % address)
  response = queryRipeDB( address )
  writeDebug(response.url)

  if(response.status_code == 200):
    writeDebug("status code: %s" % response.status_code)

    route_obj = fetchFirstRoute(response)
    if isinstance(route_obj, dict):
      route = fetchRouteAttribute(route_obj)
      return route
    else:
      # no route found -> return ip address
      pass

  # nothing found -> return ip address
  return address+'/32'


for line in sys.stdin:
  print(subnetFromIpAddress(line.strip()))
