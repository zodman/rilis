import click
from frozen import _upload_frozen
from nyaa import upload_torrent
from anidex import upload_file as anidex_upload_file
import formic
from utils import get_conf
import os

@click.group()
def cli():
    """       
    <:3 )~~~ Fansub rilis tool by zodman
    """

@cli.command()
@click.argument("torrent")
@click.argument("episode")
@click.argument("anime_slug")
@click.option("--images", '-i', multiple=True)
def frozen(torrent, episode, anime_slug, images):
    """ 
        Subir a frozen, recuerda usar comillas en windows para parametros

        Recuerda que seria frozen "file.torrent" 560 "anime_slug"

        Donde anime_slug es "cardcaptor-sakura-clean-card-hen" de la url
         https://www.frozen-layer.com/animes/cardcaptor-sakura-clean-card-hen

     """
    _upload_frozen(torrent, anime_slug, episode, images)


@cli.command()
@click.option("--subcat_id", default=1)
@click.option("--lang_id", default=29)
@click.option("--torrent_name", default="")
@click.argument("file")
def anidex(subcat_id, lang_id, torrent_name, file):
    """
        Subir a anidex, por default subcat_id=1 lang_id=29

    """
    params = get_conf("anidex")
    if not torrent_name:
        name = os.path.basename(file).replace(".torrent","")
        params.update({'torrent_name': name})
    success, resp = anidex_upload_file(file, subcat_id=subcat_id, 
                                       lang_id=lang_id, **params)
    if success:
        click.echo(resp)
    else:
        click.echo("FAILED")
        click.echo(resp)

@cli.command()
@click.argument("files", default="output_cr/*.torrent")
def nyaa(files):
    """ upload torrent files to NYAA """
    for file in formic.FileSet(include=files):
        print(upload_torrent(file))


if __name__ == '__main__':
    cli()