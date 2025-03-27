import json
import requests
import loguru

from io import BytesIO
from PIL import Image

class JsonUtils:
    def __init__(self):
        pass

    @staticmethod
    def write(obj: object, filename: str, append:bool=False):
        if append:
            filemode = 'a'
        else:
            filemode = 'w'

        with open(filename, filemode, encoding= 'utf-8') as f:
            json.dump(obj, f)


    @staticmethod
    def getValueByPath(json_str_or_obj, valuePath: str):
        '''

        :param json_str_or_obj: an Object or json String
        :param valuePath: like "/[0]/data/url"
        :return: a Value
        '''

        if isinstance(json_str_or_obj, str):
            _obj = json.loads(json_str_or_obj)
        else:
            _obj = json_str_or_obj

        # Parse the valuePath String
        valuepaths = valuePath.split('/')
        for _path in valuepaths:
            if _path.strip() == '':
                continue
            else:
                if _path[0] == '[' and _path[-1] == ']':
                    index = int(_path[1:-1])
                    _obj = _obj[index]
                else:
                    _obj = _obj[_path]

        return _obj


class httpClient:
    def __init__(self):
        pass

    @staticmethod
    def getPicture(apiUrl: str, savePath: str, json_path: str = None, show: bool = False, requests_headers: dict = None):
        '''

        :param apiUrl:  the API to get the picture (or json)
        :param savePath:  where to save the picture
        :param show: whether show the picture
        :param json_path: if apiUrl return a json str, tell us the picture's url path in json. If None, Download piture Directly.
        :param requests_headers: headers to send requests
        :return: PIL Image Object or None if failed
        '''

        try:
            httpResp = requests.get(apiUrl, headers=requests_headers)
        except:
            loguru.logger.error(f"Failed to send requests to {apiUrl}, check the Url or your connection.")

        # decide whether the json or binary picture
        if json_path == None:
            try:
                imgBinary = httpResp.content
                img = Image.open(BytesIO(imgBinary))
            except:
                loguru.logger.error("Failed to load the picture. Check if the API is availabel.")
                return None

            try:
                img.save(savePath)
                if show:
                    img.show(savePath)
                return img
            except:
                loguru.logger.error("Failed to save the picture. Check the permissions.")
                return None


        else:
            try:
                jsonstr = httpResp.content
                imgUrl  = JsonUtils.getValueByPath(jsonstr, json_path)
            except:
                loguru.logger.error(f"Failed to parse the jsons. The API returns:\n  {jsonstr}\n")
                return None

            return httpClient.getPicture(imgUrl, savePath, show=show, requests_headers=requests_headers)

