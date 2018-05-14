import requests
import os 
from utils import get_conf

ANIDEX_API_KEY = get_conf("anidex_api_key")
END_POINT = "https://anidex.info/api/"

ANIME_SUB=1
ANIME_RAW=2
ANIME_DUB=3
LA_SUB=4
LA_RAW=5
SPANISH=29

###
# curl -F "subcat_id=1" -F "file=@/path/filename.torrent" -F "group_id=1" -F "lang_id=1" -F "api_key=x-xxxxxxxxxxxxxxxxx" https://anidex.info/api/
def upload_file(torrent_file, subcat_id=ANIME_SUB, lang_id=SPANISH,**kwargs):
    torrent_filename = os.path.basename(torrent_file)
    files = {'file':(torrent_filename, open(torrent_file, "rb"))}
    data = {'subcat_id': subcat_id, 'group_id': 0, 
           # 'debug':1,
            'lang_id': lang_id,
            'api_key':ANIDEX_API_KEY}
    data.update(kwargs)
    resp = requests.post(END_POINT, data=data, files=files)
    resp_content = resp.content
    if 'error' in str(resp_content.lower()):
        return False, resp_content
    else:
        return True, resp_content 