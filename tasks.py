from invoke import task

@task
def deploy(ctx, up=False):
	ctx.run("pyinstaller -F rilis.py")
	ctx.run("copy conf.yaml.ini dist\conf.yaml")
	ctx.run("copy README.md dist\\ ")
	if up:
		ctx.run("7z a rilis.zip dist\\")
		ctx.run("curl --progress-bar -T rilis.zip transfer.sh -k -L")