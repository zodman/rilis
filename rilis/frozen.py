#!/usr/bin/env python
# encoding=utf8
# made by zodman

import grab

import urllib.parse
import logging
import slugify 

logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def get_frozen_id(alias):
    a = get_conf("anime_series")
    for day in a:
        animes = a[day].get("animes")
        if not animes:
            continue
        for anime in animes:
            alias_cfg =anime.get("alias",None)
            assert alias, "le falta alias al anime {}".format(anime)
            if alias == alias_cfg:
                return anime.get("frozen")

def _upload_frozen(file, anime_alias,episode, images):
    cfg = get_conf("frozen_layer")
    user, passwd = cfg.get("username"), cfg.get("password")
    anime_id = get_frozen_id(anime_alias)

    if not anime_id:
        click.secho("No se subio a Frozen-Layer no se encontro fronzen id", bg="red", fg="white")
        return

    #robot = grab.Grab(verbose_logging=True, debug=True)
    robot = grab.Grab(timeout=1080, connect_timeout=1080)
    robot.setup(follow_location=True)
    robot.setup(debug_post=True)
    robot.go("https://www.frozen-layer.com/users/sign_in")
    robot.doc.set_input('user[login]', user)
    robot.doc.set_input('user[password]',passwd)
    resp = robot.doc.submit()
    if "Has conectado correctamente." in resp.body:
        click.echo("login success")
    else:
        click.secho("No se subio a Frozen-Layer login failed", bg="red", fg="white")
        return
    # fansub_id = 827 # Puya+
    fansub_id = cfg.get("fansub_id") # PuyaSUbs
    language = 'Japones'
    subs = u"Español"
    torrent_file = grab.UploadContent(open(file).read(),
            filename="{}.torrent".format(slugify.slugify(file))
            )
    desc = cfg.get("description")
    #  magic!
    print (torrent_file.filename, desc)
    robot.go("https://www.frozen-layer.com/descargas/nuevo/anime?id={}".format(anime_id))
    robot.doc.set_input("descarga[episodio]", u"{}".format(episode))
    robot.doc.set_input("descarga[fansub_id]", fansub_id)
    robot.doc.set_input("idioma", language)
    robot.doc.set_input("subtitulos", subs)
    robot.doc.set_input("descarga[descripcion]",desc)
    robot.doc.set_input("torrent", torrent_file)
    resp = robot.doc.submit(submit_name="login", remove_from_post=['torrent2',])

    if "Ha habido un problema" in resp.body:
        click.secho("No se subio a Frozen-Layer", bg="red", fg="white")
        click.echo("upload failed")
    url_for_images = robot.doc.select("//div[@id='editar_imagenes']/b/a/@href").text()
    url = "https://www.frozen-layer.com{}".format(url_for_images)
    for i in images:
        ff = grab.UploadContent(open(i).read())
        file = os.path.basename("{}.jpg".format(slugify.slugify(u"{}".format(i))))
        files_to_post = {'Filename':file, 'tipo':'descarga','Filedata':ff,'Upload':'Submit Query'}
        robot.go(url,multipart_post=files_to_post)
    click.echo("frozen url {}".format(url))
    url = urllib.parse.urlparse(url)
    id = urllib.parse_qs(url.query).get("descarga_id").pop()
    return "https://www.frozen-layer.com/descargas/{}".format(id)

