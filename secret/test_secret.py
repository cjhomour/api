import pytest
import base64
import time

from test_case.secret.secret import Secret


class Testsecret(object):
    def setup_class(self):
        self.secret_toll = Secret()

        self.secret_basic_auth_name = "alauda-secret-auth-e2e"
        self.secret_oauth2_name = "alauda-secret-oauth2-e2e"
        self.secret_docker_name = "alauda-secret-docker-e2e"
        self.secret_displayname = "alauda-secret-display"
        self.git_uesrname = str(base64.b64encode(self.secret_toll.global_info.get('$GIT_USERNAME').encode('utf-8')), 'utf8')
        self.git_password = str(base64.b64encode(self.secret_toll.global_info.get('$GIT_PASSWORD').encode('utf-8')), 'utf8')
        self.oauth2_clientid = str(base64.b64encode(self.secret_toll.global_info.get('$OAUTH2_CLIENTID').encode('utf-8')), 'utf8')
        self.oauth2_clientsecret = str(base64.b64encode(self.secret_toll.global_info.get('$OAUTH2_CLIENTSECRET').encode('utf-8')), 'utf8')
        self.docker_auth = self.secret_toll.global_info.get("$DOCKER_AUTH")
        self.docker_username = self.secret_toll.global_info.get("$DOCKER_USERNAME")
        self.docker_password = self.secret_toll.global_info.get("$DOCKER_PASSWORD")
        self.docker_email = self.secret_toll.global_info.get("$DOCKER_EMAIL")
        self.dockerconfigjson = self.secret_toll.dockerjson(self.docker_auth, self.docker_username,  self.docker_password, self.docker_email)

        self.teardown_class(self)

    def teardown_class(self):
        self.secret_toll.delete_manager_secret(self.secret_basic_auth_name)
        self.secret_toll.delete_manager_secret(self.secret_oauth2_name)
        self.secret_toll.delete_manager_secret(self.secret_docker_name)
        self.secret_toll.delete_user_secret(self.secret_basic_auth_name)
        self.secret_toll.delete_user_secret(self.secret_oauth2_name)
        self.secret_toll.delete_user_secret(self.secret_docker_name)

    @pytest.mark.secret
    def test_manager_secret_basic_auth(self):
        # create manager_secret_basic_auth
        ret = self.secret_toll.create_manager_secret('./test_data/secret/create_secret_basic_auth.yaml',
                                                     {"$secret_name": self.secret_basic_auth_name,
                                                      "$secret_displayname": self.secret_displayname,
                                                      "$GIT_USERNAME":  self.git_uesrname, "$GIT_PASSWORD": self.git_password})

        assert ret.status_code == 201, "创建平台用户名／密码凭据失败"

        # get maanger_secret list
        ret = self.secret_toll.get_manager_secret_list()
        assert self.secret_basic_auth_name in ret.text, "创建的凭据不在列表中"

        # update manager_secret_basic_auth
        ret = self.secret_toll.update_manager_secret(self.secret_basic_auth_name, './test_data/secret/update_secret_basic_auth.yaml',
                                                     {"$secret_name": self.secret_basic_auth_name,
                                                      "$secret_displayname": "update_secret",
                                                      "$GIT_USERNAME": self.git_uesrname, "$GIT_PASSWORD": self.git_password})
        assert ret.status_code == 200, "更新平台用户名／密码凭据失败"

        # get manager_secret_basic_auth detail
        ret = self.secret_toll.get_manager_secret_detail(self.secret_basic_auth_name)
        assert ret.status_code == 200, "获取详情失败"

        # check displayname is update
        displayname = self.secret_toll.get_value(ret.json(), 'metadata-annotations-alauda.io/displayName', delimiter='-')
        assert displayname == "update_secret", "凭据的描述没有更新"

        # delete manager_secret_basic_auth
        ret = self.secret_toll.delete_manager_secret(self.secret_basic_auth_name)
        assert ret.status_code == 204, "删除平台用户名／密码凭据失败"

        # 删除目前有延迟
        time.sleep(10)
        ret = self.secret_toll.get_manager_secret_detail(self.secret_basic_auth_name)
        assert ret.status_code == 404, "平台用户名／密码凭据没有成功被删除"

    @pytest.mark.secret
    def test_manager_secret_oauth2(self):
        # create manager_secret_oauth2
        ret = self.secret_toll.create_manager_secret('./test_data/secret/create_secret_oauth2.yaml',
                                                     {"$secret_name": self.secret_oauth2_name,
                                                      "$OAUTH2_CLIENTID": self.oauth2_clientid,
                                                      "$OAUTH2_CLIENTSECRET": self.oauth2_clientsecret})
        assert ret.status_code == 201, "创建平台OAuth2凭据失败"

        # get manager_secret_oauth2 detail
        ret = self.secret_toll.get_manager_secret_detail(self.secret_oauth2_name)
        assert ret.status_code == 200, "获取详情失败"

        # delete manager_secret_oauth2 detail
        ret = self.secret_toll.delete_manager_secret(self.secret_oauth2_name)
        assert ret.status_code == 204, "平台OAuth2凭据删除失败"

        time.sleep(10)
        ret = self.secret_toll.get_manager_secret_detail(self.secret_oauth2_name)
        assert ret.status_code == 404, "平台OAuth2凭据没有被成功删除"

    @pytest.mark.secret
    def test_manager_secret_dockerconfigjson(self):
        # create manager_secret_docker
        ret = self.secret_toll.create_manager_secret('./test_data/secret/create_secret_dockerconfigjson.yaml',
                                                     {"$secret_name": self.secret_docker_name,
                                                      "$dockerconfigjson": self.dockerconfigjson})
        assert ret.status_code == 201, "创建平台镜像服务凭据失败"

        # get manager_secret_docker detail
        ret = self.secret_toll.get_manager_secret_detail(self.secret_docker_name)
        assert ret.status_code == 200, "获取详情失败"

        # delete manager_secret_docker
        ret = self.secret_toll.delete_manager_secret(self.secret_docker_name)
        assert ret.status_code == 204, "删除平台镜像服务凭据失败"

        time.sleep(10)
        ret = self.secret_toll.get_manager_secret_detail(self.secret_docker_name)
        assert ret.status_code == 404, "平台镜像服务凭据没有被成功删除"

    @pytest.mark.secret
    def test_user_secret_basic_auth(self):
        # create user_secret_basic_auth
        ret = self.secret_toll.create_user_secret('./test_data/secret/create_secret_basic_auth.yaml',
                                                  {"$secret_name": self.secret_basic_auth_name,
                                                   "$secret_displayname": self.secret_displayname,
                                                   "$GIT_USERNAME": self.git_uesrname,
                                                   "$GIT_PASSWORD": self.git_password})

        assert ret.status_code == 201, "创建用户名／密码凭据失败"

        # get maanger_secret list
        ret = self.secret_toll.get_user_secret_list()
        assert self.secret_basic_auth_name in ret.text, "创建的凭据不在列表中"

        # update user_secret_basic_auth
        ret = self.secret_toll.update_user_secret(self.secret_basic_auth_name,
                                                  './test_data/secret/update_secret_basic_auth.yaml',
                                                  {"$secret_name": self.secret_basic_auth_name,
                                                   "$secret_displayname": "update_secret",
                                                   "$GIT_USERNAME": self.git_uesrname,
                                                   "$GIT_PASSWORD": self.git_password})
        assert ret.status_code == 200, "更新用户名／密码凭据失败"

        # get user_secret_basic_auth detail
        ret = self.secret_toll.get_user_secret_detail(self.secret_basic_auth_name)
        assert ret.status_code == 200, "获取详情失败"

        # check displayname is update
        displayname = self.secret_toll.get_value(ret.json(), 'metadata-annotations-alauda.io/displayName',
                                                 delimiter='-')
        assert displayname == "update_secret", "凭据的描述没有更新"

        # delete manager_secret_basic_auth
        ret = self.secret_toll.delete_user_secret(self.secret_basic_auth_name)
        assert ret.status_code == 204, "删除用户名／密码凭据失败"

        time.sleep(10)
        ret = self.secret_toll.get_user_secret_detail(self.secret_basic_auth_name)
        assert ret.status_code == 404, "用户名／密码凭据没有成功被删除"

    @pytest.mark.secret
    def test_user_secret_oauth2(self):
        # create user_secret_oauth2
        ret = self.secret_toll.create_user_secret('./test_data/secret/create_secret_oauth2.yaml',
                                                  {"$secret_name": self.secret_oauth2_name,
                                                   "$OAUTH2_CLIENTID": self.oauth2_clientid,
                                                   "$OAUTH2_CLIENTSECRET": self.oauth2_clientsecret})
        assert ret.status_code == 201, "创建用户OAuth2凭据失败"

        # get user_secret_oauth2 detail
        ret = self.secret_toll.get_user_secret_detail(self.secret_oauth2_name)
        assert ret.status_code == 200, "获取详情失败"

        # delete user_secret_oauth2 detail
        ret = self.secret_toll.delete_user_secret(self.secret_oauth2_name)
        assert ret.status_code == 204, "用户OAuth2凭据删除失败"

        time.sleep(10)
        ret = self.secret_toll.get_user_secret_detail(self.secret_oauth2_name)
        assert ret.status_code == 404, "用户OAuth2凭据没有被成功删除"

    @pytest.mark.secret
    def test_user_secret_dockerconfigjson(self):
        # create user_secret_docker
        ret = self.secret_toll.create_user_secret('./test_data/secret/create_secret_dockerconfigjson.yaml',
                                                  {"$secret_name": self.secret_docker_name,
                                                   "$dockerconfigjson": self.dockerconfigjson})
        assert ret.status_code == 201, "创建用户镜像服务凭据失败"

        # get user_secret_docker detail
        ret = self.secret_toll.get_user_secret_detail(self.secret_docker_name)
        assert ret.status_code == 200, "获取详情失败"

        # delete user_secret_docker
        ret = self.secret_toll.delete_user_secret(self.secret_docker_name)
        assert ret.status_code == 204, "删除用户镜像服务凭据失败"

        time.sleep(10)
        ret = self.secret_toll.get_user_secret_detail(self.secret_docker_name)
        assert ret.status_code == 404, "用户镜像服务凭据没有被成功删除"
