#This scrpit remove the background of a pic fomr API https://www.remove.bg
#the API key was set on file __init__.py as removebg_API = 'the APIkey create from the website'
#remove.bg alows used 50 pics every month
#the code was provided by remove.bg webpage

# Requires "requests" to be installed (see python-requests.org)
import requests, os
from app.removeBack import removebg_APIkey

urlRemoveBg = 'https://api.remove.bg/v1.0/removebg'

def removeBG_one_pic(url_jpg: str):
    print(f"let's remove background of {url_jpg}")
    if isinstance(url_jpg, str) and os.path.isfile(url_jpg) and url_jpg.lower().endswith(".jpg"):
        print('The file is correct')
        print(f'My APIkey {removebg_APIkey}')
    else:
        print('Sorry parameter incorrect')
        # response = requests.post(
        #     urlRemoveBg,
        #     files={'image_file': open('/path/to/file.jpg', 'rb')},
        #     data={'size': 'auto'},
        #     headers={'X-Api-Key': 'INSERT_YOUR_API_KEY_HERE'},
        # )
        # if response.status_code == requests.codes.ok:
        #     with open('no-bg.png', 'wb') as out:
        #         out.write(response.content)
        # else:
        #     print("Error:", response.status_code, response.text)
