#!/usr/bin/env python
# coding: utf-8

import sys
import shlex
import pycdlib
from configparser import ConfigParser
import requests
import zipfile
from io import BytesIO
from functools import lru_cache
import xml.etree.ElementTree as ET
import re
import os


serial_re = re.compile(r'^cdrom0:\\([A-Z]{4})_(\d{3})\.(\d{2});\d$')
title_re = re.compile(r'^([^(]+)(:?\s\(.*)$')


def get_xml_database(url="http://redump.org/datfile/ps2/serial"):
    body = requests.get(url, stream=True).content
    with zipfile.ZipFile(BytesIO(body)) as ziphl:
        with ziphl.open(ziphl.filelist[0].filename) as xml:
            return xml.read()


def get_games(root):
    for game in root.findall('./game'):
        name = game.get('name')
        serials = game.find('serial')
        if serials is not None:
            for serial in serials.text.split(','):
                yield (serial.strip(), name)


@lru_cache()
def build_serial_db():
    xml = get_xml_database()
    root = ET.fromstring(xml)
    games = get_games(root)
    return dict(games)


def get_serial(filename):
    iso = pycdlib.PyCdlib()
    iso.open(filename)
    try:
        for entry in iso.list_dir('/'):
            if entry.is_file() and entry.file_identifier().split(b';')[0].lower() == b'system.cnf':
                with iso.open_file_from_iso(iso_path=f"/{entry.file_identifier().decode('utf-8')}") as system:
                    cfg = ConfigParser()
                    cfg.read_string("[main]\r\n" + system.readall().decode('utf-8'))
                    return serial_re.match(cfg['main']['BOOT2']).groups()
    except:
        return None


def get_serial_and_name(iso):
    if (serial := get_serial(iso)) is None:
        raise ValueError("Serial not found")
    elif (name := build_serial_db().get(f"{serial[0]}-{serial[1]}{serial[2]}", None)) is not None:
        return (serial, name)
    else:
        return (serial, os.path.splitext(os.path.basename(iso))[1])


def short_title(txt):
    try:
        return title_re.match(txt).group(1)
    except:
        return None


def build_hdl_command(device, title, iso, serial):
    return ["hdl_dump", "inject_dvd", device, title, iso, serial, "*u4"]


def command_from_iso(device, iso):
    serial, name = get_serial_and_name(iso)
    return build_hdl_command(device, short_title(name) or name, iso, f"{serial[0]}_{serial[1]}.{serial[2]}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} device game1.iso [game2.iso...]", file=sys.stderr)
        sys.exit(1)
    else:
        for filename in sys.argv[2:]:
            print(" ".join(map(shlex.quote, command_from_iso(sys.argv[1], filename))))
