import requests


# 配置文件：微信小程序
class WxappConfig(object):
    appid = ''
    secret = ''


class WxappUtils(object):

    def __init__(self, config: WxappConfig):
        self.config: WxappConfig = config

    def jscode2session(self, code):
        """
        登录
        :url https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html
        :param code: 小程序登录时获取的 code
        :return:
        """
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={JSCODE}&grant_type=authorization_code'
        url = url.format(**{
            'APPID': self.config.appid,
            'SECRET': self.config.secret,
            'JSCODE': code,
        })

        resp = requests.get(url)
        return resp.json()
