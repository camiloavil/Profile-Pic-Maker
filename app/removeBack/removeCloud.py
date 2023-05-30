#This scrpit remove the background of a pic fomr API https://www.remove.bg
#the API key was set on file __init__.py as removebg_API = 'the APIkey create from the website'
#remove.bg alows used 50 pics every month
#the code was provided by remove.bg webpage

#for future develope implementar https://github.com/danielgatis/rembg wont nedd an external API
import requests, os
from app.removeBack import removebg_APIkey

urlRemoveBg = 'https://api.remove.bg/v1.0/removebg'

def removeBG_one_pic(url_jpg: str):
    print(f"let's remove background of {url_jpg}")
    if isinstance(url_jpg, str) and os.path.isfile(url_jpg) and url_jpg.lower().endswith(".jpg"):
        print(f'processing {url_jpg}')
        url_png=url_jpg.replace('.jpg','.png')
        response = requests.post(
            urlRemoveBg,
            files={'image_file': open(url_jpg, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': removebg_APIkey},
        )
        if response.status_code == requests.codes.ok:
            with open(url_png, 'wb') as out:
                out.write(response.content)
                print(f'Backgorund remove [SUCCESS] {url_png}') 
        else:
            print("[ERROR]:", response.status_code, response.text)
    else:
        print('Sorry parameter incorrect')

