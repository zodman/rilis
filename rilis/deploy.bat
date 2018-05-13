pyinstaller -F rilis.py
copy conf.yaml.ini dist\conf.yaml
copy README.md dist\

#7z a rilis.zip dist\
#curl -T rilis.zip transfer.sh -k -L