# encoding: utf-8

from app.views.base_view import BaseHandler
from app.models.host import Host, model_to_dict
from app.models.role import Role
from app.models.card import BasicCard


class IndexHandler(BaseHandler):

    def get(self):
        data_list = list()
        hosts = self.session.query(BasicCard).all()
        for host in hosts:
            data = model_to_dict(host, exclude='create_time,update_time')
            data_list.append(data)
        self.response.update_data(**{str(data['id']): data for data in data_list})

        self.write(self.response.data)

    def post(self):
        self.response.update(message='qwer', data='123456')
        self.write(self.response.data)
