from invoke import task
import imp
import os
import datetime 

@task
def compile_mktorrent(ctx):
    with ctx.cd("mktorrent"):
        ctx.run("pyinstaller -F createtorrent.py")
    ctx.run("mkdir dist\\vendor\\")
    ctx.run("copy mktorrent\\dist\\createtorrent.exe dist\\vendor\\ ")

@task 
def download_vendor(ctx):
    VER="1.9.98-win32"
    cmd =[
    "curl",
    "--progress-bar",
    "https://megatools.megous.com/builds/megatools-{}.zip".format(VER),
     "> mega.zip",
    ]
    cxt.run(" ".join(cmd))
    ctx.run("7z x mega.zip -o vendor")


@task
def deploy(ctx, up=False):
    """
        script para generar el exe y subir a transfer para compartir
    """

    _, user_agent_path, _ =imp.find_module("user_agent")
    user_agent_data = os.path.join(user_agent_path,"data")
    cmd =[
    "pyinstaller",
    '--hidden-import','"grab.transport"',
    '--hidden-import','grab.transport.curl',
    '--hidden-import','pycurl',
    '--hidden-import','grab.response',
    '--add-data','{};{}'.format(user_agent_data,
                                 os.path.join("user_agent","data")),
    '-F',
    'rilis.py'
    ]
    ctx.run(" ".join(cmd))
    ctx.run("copy conf.yaml.ini dist\\conf.yaml")
    ctx.run("copy README.md dist\\ ")
    now = datetime.datetime.now().strftime("%d%H%M")
    if up:
        ctx.run("7z a rilis{}.zip dist\\".format(now))
        ctx.run("curl --progress-bar -T rilis{}.zip" \
                " transfer.sh -k -L".format(now))
        #ctx.run("del rilis{}.zip".format(now))
