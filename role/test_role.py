from test_case.role.role import Role
from test_case.account.account import Account
from common.base_request import Common
from common.log import logger
import pytest


def get_file_path(file_type, file_name):
    return "./test_data/{0}/{1}.json".format(file_type, file_name)


def get_response_detail(response):
    return "响应状态码: {}, 返回结果：{}".format(
        response.status_code,
        response.content
    )


@pytest.mark.role
@pytest.mark.ace
@pytest.mark.BAT
@pytest.mark.flaky(reruns=2, reruns_delay=3)
class TestRoleSuite(object):
    def get_role_uuid(self, role_name):
        role_detail = self.role.get_role_detail(role_name)
        try:
            uuid = self.common.get_uuid_accord_name(role_detail.json(), {"name": role_name}, 'uuid')
            return uuid
        except Exception as e:
            logger.error(e)

    def verify_value_in_role_detail(self, role_name, result=None, field=None, except_value=None):
        response = self.role.get_role_detail(role_name)
        try:
            if result:
                return except_value in self.common.get_value_list(response.json(), "{}.{}".format(result, field))
            else:
                return except_value in self.common.get_value_list(response.json(), field)
        except Exception as e:
            logger.error(e)
            return False

    def setup_class(self):
        self.role = Role()
        self.account = Account()
        self.common = Common()
        self.role_name = "e2erole"
        self.add_permission = "project"
        self.parent_role_name = "administrator"
        self.sub_account_data = {
            "$sub_account_user_name": "e2erolesubaccount",
            "$sub_account_password": "123456"
        }
        self.account.create_sub_account(get_file_path('account', 'create_sub_account'), self.sub_account_data)
        self.role_template_name = "e2eroletemplate"
        self.permission_scopes = "test"

    def teardown_class(self):
        self.role.delete_role(self.role_name)
        self.account.delete_sub_account(self.sub_account_data['$sub_account_user_name'])
        self.role.delete_role_template(self.role_template_name)

    def test_role_template(self):
        """
        流程： 获取角色模版约束-创建模版-获取角色模版列表(验证公有模版及新创建模版)-更新模版-获取模版详情验证更新结果-使用模版生成权限
              -验证生成权限内容-删除角色模版-验证角色模版列表
        """
        # 获取存在的约束列表
        get_role_templates_scopes_result = self.role.get_role_templates_scopes()
        assert get_role_templates_scopes_result.status_code == 200, "获取scopes 失败，{}".format(get_response_detail(
            get_role_templates_scopes_result
        ))
        scopes_list = self.common.get_value_list(get_role_templates_scopes_result.json(), 'resource_type')
        except_scopes_list = ["cluster", "namespace", "project", "registry", "registry_project", "space"]

        assert except_scopes_list == scopes_list, "约束获取失败，约束内容与预期不相同，预期结果: {}, 实际结果: {}".format(
            except_scopes_list, scopes_list
        )

        # 创建角色模版
        create_role_template_data = {
            "$role_template_name": self.role_template_name,
        }
        create_role_template = self.role.create_role_template(
            get_file_path('role', 'create_role_template'),
            create_role_template_data
        )
        assert create_role_template.status_code == 201, "创建角色模版失败，{}".format(
            get_response_detail(create_role_template)
        )
        role_template_uuid = self.common.get_value(create_role_template.json(), 'uuid')

        # 验证角色模版列表包含公有模版和私有模版
        get_role_template_list_result = self.role.get_role_template_list()
        assert get_role_template_list_result.status_code == 200, "获取角色模版列表失败，{}".format(
            get_response_detail(get_role_template_list_result)
        )
        role_templates_list = self.common.get_value_list(get_role_template_list_result.json(), 'name')
        except_role_template_list = {'super_admin', 'platform_trusted_admin', 'platform_untrusted_admin',
                                     'platform_auditor', 'project_admin', 'project_auditor', 'namespace_admin',
                                     'namespace_auditor', 'namespace_developer', self.role_template_name}

        assert except_role_template_list.issubset(role_templates_list), "角色模版列表中没有包含全部系统预设角色模版"

        # 更新角色模版
        update_role_template_data = {
            "$role_template_name": self.role_template_name
        }
        update_role_template_result = self.role.update_role_template(
            get_file_path('role', 'update_role_template'),
            update_role_template_data,
            role_template_uuid
        )
        assert update_role_template_result.status_code == 200, "更新角色模版失败, {}".format(
            get_response_detail(update_role_template_result)
        )

        # 获取角色模版详情
        get_role_template_detail_result = self.role.get_role_template_detail(role_template_uuid)
        assert get_role_template_detail_result.status_code == 200, "获取角色模版详情失败，{}".format(get_response_detail(
            get_role_template_detail_result
        ))
        assert self.common.get_value(get_role_template_detail_result.json(), 'description') != self.common.get_value(
            create_role_template.json(), 'description'), "角色模版更新失败，数据没有更新"

        # 通过角色模版生成权限列表
        generate_permission_by_role_template_data = {
            "$scopes": self.permission_scopes
        }
        generate_permission_by_role_template_result = self.role.generate_permission_by_role_template(
            file=get_file_path('role', 'generate_permission_by_role_template'),
            data=generate_permission_by_role_template_data,
            role_template_uuid=role_template_uuid
        )

        assert generate_permission_by_role_template_result.status_code == 200, "使用角色模版失败，{}".format(
            get_response_detail(generate_permission_by_role_template_result)
        )
        generate_result = generate_permission_by_role_template_result.json()
        assert self.common.get_value(generate_result, '0.resource_type') == 'application', '生成角色失败'
        assert self.common.get_value(
            generate_result, '0.constraints.0.res:cluster') == self.permission_scopes, "生成角色失败"

        # 删除角色模版
        delete_role_template_result = self.role.delete_role_template(role_template_uuid)
        assert delete_role_template_result.status_code == 204, "删除角色模版失败，{}".format(get_response_detail(
            delete_role_template_result
        ))

        # 获取角色模版列表验证删除的角色模版不在列表中
        get_role_template_list_result = self.role.get_role_template_list()
        assert get_role_template_list_result.status_code == 200, "获取角色模版列表失败，{}".format(
            get_response_detail(get_role_template_list_result)
        )
        role_templates_list = self.common.get_value_list(get_role_template_list_result.json(), 'name')
        assert self.role_template_name not in role_templates_list, "删除角色模版失败，角色模版依然存在角色模版列表中"

    def test_role(self):
        """
        流程： 获取权限列表-创建角色-验证角色列表-更新角色详情-获取角色详情-验证更新角色成功-添加父角色-验证角色详情中父角色-删除父角色
              -验证角色详情页父角色删除成功-角色添加权限-验证角色详情页权限-删除角色权限-验证角色详情页权限-添加角色成员-验证角色成员列
              表添加成员成功-删除角色成员-验证角色成员列表删除成员成功-删除角色-验证角色列表删除角色成功
        """
        # 获取权限列表
        get_permission_schema = self.role.get_permission_schema()
        assert get_permission_schema.status_code == 200, "获取 permission 列表失败，{}".format(
            get_response_detail(get_permission_schema)
        )

        # 简单验证权限列表数据大于0
        assert len(get_permission_schema.json()) > 0, "获取permission 列表失败，列表为空"

        # 创建角色
        create_role_data = {
            "$role_name": self.role_name
        }
        create_role_result = self.role.create_role(get_file_path('role', 'create_role'), create_role_data)
        assert create_role_result.status_code == 200, "创建角色失败，{}".format(get_response_detail(create_role_result))

        # 获取角色列表包含创建的角色
        get_role_list_result = self.role.get_role_list()
        assert get_role_list_result.status_code == 200, "获取角色列表失败, {}".format(
            get_response_detail(get_role_list_result)
        )
        assert self.role_name in self.common.get_value_list(
            self.common.get_value(get_role_list_result.json(), 'results'), 'name'), "创建角色失败，创建的角色不在角色列表中"

        # 更新角色
        update_role_data = {
            "$role_name": self.role_name,
            "$add_permission": self.add_permission
        }
        update_role_result = self.role.update_role_detail(get_file_path('role', 'update_role_detail'),
                                                          update_role_data,
                                                          role_name=self.role_name)
        assert update_role_result.status_code == 204, "更新角色失败，{}".format(get_response_detail(update_role_result))

        # 获取角色中的权限
        get_role_detail_result = self.role.get_role_detail(self.role_name)
        assert get_role_detail_result.status_code == 200, "获取角色详情失败，{}".format(
            get_response_detail(get_role_list_result)
        )
        operate_permission_uuid = self.common.get_uuid_accord_name(self.common.get_value(
            get_role_detail_result.json(), 'permissions'), {"resource_type": self.add_permission}, "uuid")

        # 验证更新角色总的权限
        assert self.add_permission in self.common.get_value_list(self.common.get_value(
            get_role_detail_result.json(), 'permissions'), 'resource_type'), "更新角色失败，更新的权限不在角色的详情中"

        # 验证添加父角色
        add_parent_data = {
            "$parent_role_name": self.parent_role_name,
            "$parent_role_uuid": self.get_role_uuid(self.parent_role_name)
        }
        add_parent_result = self.role.add_parent_to_role(get_file_path('role', 'add_parent'),
                                                         add_parent_data,
                                                         self.role_name)
        assert add_parent_result.status_code == 204, "添加父角色失败，{}".format(get_response_detail(add_parent_result))

        # 验证添加额父角色在角色详情中
        get_role_detail_result = self.role.get_role_detail(self.role_name)
        assert self.parent_role_name in self.common.get_value_list(self.common.get_value(
            get_role_detail_result.json(), 'parents'), 'name'), "添加父角色失败，添加的父角色不在角色的详情中"

        # 验证删除父角色
        remove_parent_role_result = self.role.remove_parent_from_role(self.role_name,
                                                                      self.get_role_uuid(self.parent_role_name)
                                                                      )
        assert remove_parent_role_result.status_code == 204, "删除父角色失败，{}".format(
            get_response_detail(remove_parent_role_result)
        )

        # 验证删除的父角色不在角色详情中
        assert self.verify_value_in_role_detail(self.role_name,
                                                'parents',
                                                'name',
                                                self.parent_role_name
                                                ) is False, "删除父角色失败，删除的父角色依然角色的详情中"

        # 验证删除角色中的权限
        remove_permission_result = self.role.remove_permission_from_role(self.role_name, operate_permission_uuid)

        assert remove_permission_result.status_code == 204, "删除权限失败，{}".format(
            get_response_detail(remove_permission_result)
        )

        # 验证删除后的权限不在角色详情中
        assert self.verify_value_in_role_detail(self.role_name,
                                                'permissions',
                                                'uuid',
                                                operate_permission_uuid
                                                ) is False, "删除权限失败，删除的权限依然角色的详情中"

        # 验证添加权限到角色
        add_permission_data = {
            "$permission": self.add_permission
        }
        add_permission_result = self.role.add_permission_to_role(get_file_path('role', 'add_permission'),
                                                                 add_permission_data, self.role_name)
        assert add_permission_result.status_code == 201, "删除权限失败，{}".format(
            get_response_detail(add_permission_result)
        )

        # 验证添加的权限在角色详情中
        get_role_detail_result = self.role.get_role_detail(self.role_name)
        assert self.add_permission in self.common.get_value_list(
            self.common.get_value(get_role_detail_result.json(), 'permissions'),
            'resource_type'), "添加权限失败，添加的权限不在角色的详情中"

        # 给角色绑定子账号
        assign_role_to_sub_account = {
            "$sub_account": self.sub_account_data['$sub_account_user_name']
        }
        assign_role_to_sub_account_result = self.role.assign_role_to_user(
            get_file_path('role', 'operate_role_for_sub_account'),
            assign_role_to_sub_account,
            self.role_name)
        assert assign_role_to_sub_account_result.status_code == 200, "角色添加子账号失败，{}".format(
            get_response_detail(assign_role_to_sub_account_result)
        )

        assert self.common.get_value(
            assign_role_to_sub_account_result.json(), '0.user') == self.sub_account_data['$sub_account_user_name']
        assert self.common.get_value(assign_role_to_sub_account_result.json(), '0.role_name') == self.role_name

        # 获取绑定该角色的子账号列表
        list_sub_account_from_role = self.role.get_role_user_list(self.role_name)
        assert list_sub_account_from_role.status_code == 200, "获取角色用户列表失败，{}".format(
            get_response_detail(list_sub_account_from_role)
        )

        assert self.sub_account_data['$sub_account_user_name'] in self.common.get_value_list(
            self.common.get_value(list_sub_account_from_role.json(), 'results'),
            'user'), "角色添加子账号失败，角色的子账号列表中没有已经添加的子账号"

        # 接触子账号与角色的绑定
        revoke_role_to_sub_account_result = self.role.revoke_role_to_user(
            get_file_path('role', 'operate_role_for_sub_account'),
            assign_role_to_sub_account,
            self.role_name)
        assert revoke_role_to_sub_account_result.status_code == 204, "删除角色子账号失败，{}".format(
            get_response_detail(revoke_role_to_sub_account_result)
        )

        # 获取角色绑定的子账号列表验证子账号删除成功
        list_sub_account_from_role = self.role.get_role_user_list(self.role_name)
        assert list_sub_account_from_role.status_code == 200, "获取角色用户列表失败，{}".format(
            get_response_detail(list_sub_account_from_role)
        )
        assert self.common.get_value(list_sub_account_from_role.json(),
                                     'results') is None, "角色删除子账号失败，角色的子账号列表中依然存在已经删除的子账号"

        # 验证删除角色
        delete_role_result = self.role.delete_role(self.role_name)
        assert delete_role_result.status_code == 204, "删除角色失败，{}".format(get_response_detail(
            delete_role_result
        ))

        # 验证删除的角色不在角色列表
        get_role_list_result = self.role.get_role_list()
        assert get_role_list_result.status_code == 200, "获取角色列表失败, {}".format(
            get_response_detail(get_role_list_result)
        )

        assert self.role_name not in self.common.get_value_list(
            self.common.get_value(get_role_list_result.json(), 'results'), 'name'), "删除角色失败，删除的角色依然存在角色列表中"
