#!/usr/bin/env python
# encoding=utf8
# made by zodman
import click
import requests
import json
from utils import get_conf
import os
import io

NYAA_DOMAIN = "https://nyaa.si/"

def _get_login():
    cfg = get_conf("nyaa")
    return cfg.get("username"),cfg.get("password")


def upload_torrent(file):
    click.echo("upload to nyaa")
    u,p = _get_login()
    nyaa_cfg = get_conf("nyaa")
    info = nyaa_cfg.get("info")
    hidden = nyaa_cfg.get("hidden", False)
    filename = os.path.basename(file).replace(".torrent","")
    desc = nyaa_cfg.get("description")
    category = nyaa_cfg.get("category","1_3")
    remake = nyaa_cfg.get("remake", False)
    anonymous = nyaa_cfg.get("anonymous", False)
    data = {
        'category':category,
        'information': info,
        'description':desc,
        'name':filename,
        'remake': remake,
        'anonymous':anonymous,
        'hidden':hidden,
    }
    encoded_data = {'torrent_data':json.dumps(data)}
    f = open(file,"rb")
    files = {'torrent': f }
    res = requests.post(NYAA_DOMAIN +'api/upload', 
        data=encoded_data, 
        files=files, 
        auth=(u,p))
    click.echo("upload nyaa status_code: {}".format(res.status_code))
    if "Upload failed" in str(res.content):
        click.secho("failed to nyaa upload", fg="red")
        click.echo(str(res.content))
        return

    if res.status_code != 200:
        click.secho("failed to upload nyaa status_code {}".format(res.status_code), fg="red")
        errors = res.json()
        click.secho("{}".format(errors), fg="red")
        return
    elif res.status_code == 461:
        click.secho("Torrent exists on nyaa",fg="red")
        return
    else:
        id =res.json().get("id")
        click.secho("nyaa upload success https://nyaa.si/view/{}".format(id), fg="blue")
        return id


def upload_nyaa(file):
    tid = upload_torrent(file)
    if  tid is not None:
        view_url = NYAA_DOMAIN + "view/{0}".format(tid)
        click.secho("{}".format(view_url), fg="green")
        return view_url

