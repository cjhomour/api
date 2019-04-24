import base64
import json

from common.base_request import Common


class Secret(Common):
    def create_secret_url(self):
        return "v2/devops/namespace/secrets"

    def get_secret_url(self, secret_name=''):
        return "v2/devops/namespace/secrets/{}".format(secret_name)

    def create_manager_secret(self, file, data):
        path = self.create_secret_url()
        data = self.generate_data(file, data)
        return self.send(method='post', path=path, data=data, params={})

    def get_manager_secret_list(self):
        path = self.create_secret_url()
        return self.send(method='get', path=path, params={})

    def get_manager_secret_detail(self, secret_name):
        path = self.get_secret_url(secret_name)
        return self.send(method='get', path=path, params={})

    def delete_manager_secret(self, secret_name):
        path = self.get_secret_url(secret_name)
        return self.send(method='delete', path=path, params={})

    def update_manager_secret(self, secret_name, file, data):
        path = self.get_secret_url(secret_name)
        data = self.generate_data(file, data)
        return self.send(method='put', path=path, data=data, params={})

    def create_user_secret(self, file, data):
        path = self.create_secret_url()
        data = self.generate_data(file, data)
        return self.send(method='post', path=path, data=data)

    def get_user_secret_list(self):
        path = self.create_secret_url()
        return self.send(method='get', path=path)

    def get_user_secret_detail(self, secret_name):
        path = self.get_secret_url(secret_name)
        return self.send(method='get', path=path)

    def delete_user_secret(self, secret_name):
        path = self.get_secret_url(secret_name)
        return self.send(method='delete', path=path)

    def update_user_secret(self, secret_name, file, data):
        path = self.get_secret_url(secret_name)
        data = self.generate_data(file, data)
        return self.send(method='put', path=path, data=data)

    def dockerjson(self, auths, username, password, email):
        auth = "{}:{}".format(username, password)
        auth_base64 = str(base64.b64encode(auth.encode('utf-8')), 'utf8')
        data = {
            "auths": {
                auths: {
                    "username": username,
                    "password": password,
                    "email": email,
                    "auth": auth_base64
                }
            }
        }
        return str(base64.b64encode(json.dumps(data).encode('utf-8')), 'utf8')
