from invoke import task

@task
def compile_mktorrent(ctx):
	with ctx.cd("mktorrent"):
		ctx.run("pyinstaller -F createtorrent.py")
	ctx.run("copy mktorrent\\dist\\createtorrent.exe dist\\ ")


@task
def deploy(ctx, up=False):
	"""
		script para generar el exe y subir a transfer para compartir
	"""
	cmd =[
	"pyinstaller",
	'--hidden-import','grab.transport',
	'-F'
	'rilis.py'
	]
	ctx.run(" ".join(cmd))
	ctx.run("copy conf.yaml.ini dist\conf.yaml")
	ctx.run("copy README.md dist\\ ")

	if up:
		ctx.run("7z a rilis.zip dist\\")
		ctx.run("curl --progress-bar -T rilis.zip transfer.sh -k -L")
