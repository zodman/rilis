#!/usr/bin/env python
# encoding=utf8
# made by zodman
import click
import requests
import re
import json
from utils import get_conf
import os
import io

NYAA_DOMAIN = "https://nyaa.si/"

def _get_login():
    cfg = get_conf("nyaa")
    return cfg.get("username"),cfg.get("password")


def upload_torrent(file):
    u,p = _get_login()
    nyaa_cfg = get_conf("nyaa")
    info = nyaa_cfg.get("info")
    hidden = nyaa_cfg.get("hidden")
    filename = os.path.basename(file).replace(".torrent","")
    desc = nyaa_cfg.get("description")
    data = {
        'category':"1_3",
        'information': info,
        'description':desc,
        'name':filename,
        'remake':False,
        'anonymous':False,
        'hidden':hidden,
    }
    encoded_data = {'torrent_data':json.dumps(data)}
    f = open(file,"rb")
    files = {'torrent': f }
    res = requests.post(NYAA_DOMAIN +'api/upload', 
        data=encoded_data, 
        files=files, 
        auth=(u,p))
    click.echo("upload status_code: {}".format(res.status_code))
    if "Upload failed" in str(res.content):
        click.echo("failed to upload")
        click.echo(str(res.content))
        return

    if res.status_code != 200:
        click.echo("failed to upload status_code {}".format(res.status_code))
        click.echo(str(res.content))
        return
    elif res.status_code == 461:
        click.echo("El torrent ya existe")
        return
    else:
        return res.json().get("id")


def upload_nyaa(file):
    tid = upload_torrent(file)
    if  tid is not None:
        view_url = NYAA_DOMAIN + "view/{0}".format(tid)
        click.secho("{}".format(view_url), fg="green")
        return view_url

