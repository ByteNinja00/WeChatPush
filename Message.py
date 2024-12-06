import requests
import os, json
from datetime import datetime

class TextMessage:
    """
    This class implements pushing text messages to corporate WeChat
    """
    def __init__(self, corpid: str, secret: str, /) -> None:
        self.corpid = corpid
        self.secret = secret

    def __cache_accesstoken(self) -> None:
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corpid}&corpsecret={self.secret}"
        request = requests.get(url=url)
        response = request.text
        with open(file='access_token.txt', mode='w+', encoding='utf-8') as f:
            f.write(response)
    
    def __verify_accesstoken_interval_time(self) -> bool:
        now_time_stamp = datetime.now().timestamp()
        if not os.path.exists('access_token.txt'):
            self.__cache_accesstoken()
        last_mofify_time = os.stat('access_token.txt').st_mtime
        time_interval = now_time_stamp - last_mofify_time
        if time_interval >= 7200:
            return True
             
    def pushing(self, mapping: any, /) -> any:
        """
        Exmaple for mapping:
        
        mapping={
            "touser": "username" like Zhangsan
            "msgtype": "text": Fixed
            "agentid": wechat app id like: 1000003
            "text": {
                "content": "Messages to be pushed"
            },
            "safe": 0: default 0 is disabled, 1 to enabled
        }
        """
        if self.__verify_accesstoken_interval_time():
            self.__cache_accesstoken()
        with open(file='access_token.txt', mode='r', encoding='utf-8') as f:
            readfile= json.loads(f.read())
        try:
            access_token = readfile['access_token']
        except KeyError as e:
            raise
        
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        request = requests.post(url=url, data=mapping)
        response = request.json()
        return response