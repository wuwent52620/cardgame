import traceback

import requests

from app.views.base_view import BaseHandler
from log.log_config import logger


class WeixinHandler(BaseHandler):
    appid = 'wxe6708db1c35a900b'  # 你本身的
    appsecret = '4d2a0329376de59f836a6fd571cded4c'  # 你本身的
    code = ''
    state = ''

    # 为了方便你们看,我都写在一个函数里
    def get(self):

        # 第一步获取code跟state
        try:
            self.code = self.get_body_argument('code', '')
            self.state = self.get_body_argument('state', '')
        except Exception as e:
            logger.error("获取code和stat参数错误：\n%s", str(traceback.format_exc()))


        # 2.经过code换取网页受权access_token
        try:
            url = u'https://api.weixin.qq.com/sns/oauth2/access_token'
            params = {
                'appid': self.appid,
                'secret': self.appsecret,
                'code': self.code,
                'grant_type': 'authorization_code'
            }
            res = requests.get(url, params=params).json()

            access_token = res["access_token"]  # 只是呈现给你们看,能够删除这行
            openid = res["openid"]  # 只是呈现给你们看,能够删除这行
        except Exception as e:
            logger.error("获取access_token参数错误：\n%s", str(traceback.format_exc()))
            raise Exception('404')

        # 3.若是access_token超时，那就刷新
        # 注意,这里我没有写这个刷新功能,不影响使用,若是想写的话,能够本身去看文档

        # 4.拉取用户信息
        try:
            user_info_url = u'https://api.weixin.qq.com/sns/userinfo'
            params = {
                'access_token': res["access_token"],
                'openid': res["openid"],
            }
            res = requests.get(user_info_url, params=params).json()
            """
            注意,这里有个坑,res['nickname']表面上是unicode编码,
            可是里面的串倒是str的编码,举个例子,res['nickname']的返回值多是这种形式
            u'\xe9\x97\xab\xe5\xb0\x8f\xe8\x83\x96',直接存到数据库会是乱码.必需要转成
            unicode的编码,须要使用
            res['nickname'] = res['nickname'].encode('iso8859-1').decode('utf-8')
            这种形式来转换.
            你也能够写个循环来转化.
            for value in res.values():
                value = value.encode('iso8859-1').decode('utf-8')
            """
        except Exception as e:
            logger.error("拉取用户信息错误：\n%s", str(traceback.format_exc()))
