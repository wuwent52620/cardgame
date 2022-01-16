# encoding: utf-8
import json

from app.views.base_view import BaseHandler
from app.models.host import Host, model_to_dict
from app.models.role import Role


class IndexHandler(BaseHandler):
    def get(self):
        data_list = list()
        hosts = self.session.query(Role).all()
        for host in hosts:
            data = model_to_dict(host)
            data['create_time'] = str(data['create_time'])
            data['update_time'] = str(data['update_time'])
            data_list.append(data)
        self.write(json.dumps({'status': True, 'msg': '吴文童', 'data': data_list}, ensure_ascii=False))
