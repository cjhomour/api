from test_case.role.role import Role
from common.base_request import Common
import pytest
import json


def replace_data(string, data):
    """
    替换角色模版中的{{param}}参数
    :param string: 模版
    :param data: 需要替换的数据
    :return: 替换后的结果，string
    :example: template = "{{ param }}"
             data = {"{{ param }}": "project"}
             result = replace_data(template, data)
             result = "project"
    """
    for key, value in data.items():
        string = string.replace(key, value)
    return string


def del_private_role_template(data, del_value):
    """
    根绝value删除字典中的item
    :param data: 原角色模版列表
    :param del_value: 需要删除的模版类型
    :return: 返回所有删除指定value后的字典数据
    :example: a = {"a"："x"，"b"："x"，"c"："y"}
              result = del_private_role_template(a, "y")
              result = {"a"："x"，"b"："x"}
    """
    del_keys = []
    for key, value in data.items():
        if value == del_value:
            del_keys.append(key)
    for key in del_keys:
        data.pop(key)
    return data


def many_to_one_arry(data):
    """
    多维数组，转一维数组，为了校验内容相同但是顺序不同的数组，需要把多维数组转为一维数组进行进行校验
    :param data: 需要替换的数据，传入字典类型，key为文件中被替换的内容，value为替换的字符串
    :return: 转换成功的一维数组
    :example: a = [[1,2],[3,4]]
              result = many_to_one_arry(a)
              result = [1,2,3,4]
    """
    return eval('[' + str(data).replace(' ', '').replace('[', '').replace(']', '') + ']')


@pytest.mark.ace
@pytest.mark.BAT
@pytest.mark.flaky(reruns=2, reruns_delay=3)
class TestRoleTemplateSuite(object):
    def setup(self):
        self.role = Role()
        self.common = Common()
        self.system_role_template = {
            "super_admin", "platform_trusted_admin", "platform_untrusted_admin", "platform_auditor",
            "project_admin", "project_auditor", "namespace_admin", "namespace_auditor", "namespace_developer",
            "space_admin", "space_developer", "space_auditor"
        }

    def get_file_data(self, template_name):
        data = {}
        # 获取data中数据
        with open('./test_data/role/role-template/{}.json'.format(template_name), 'r') as f:
            file_data = f.read()
        data['actions'] = self.common.get_value_list(json.loads(file_data), 'actions')
        data['resource'] = self.common.get_value_list(json.loads(file_data), 'resource')
        data['resource_type'] = self.common.get_value_list(json.loads(file_data), 'resource_type')
        data['constraints'] = self.common.get_value_list(json.loads(file_data), 'constraints')
        return data

    def teardown(self):
        for key in self.system_role_template:
            self.role.delete_role("role-template-{}".format(key))

    def test_system_role_template(self):
        """
        流程：获取系统预置角色模版-验证系统预制角色模版权限与预置数据相同-使用预制角色模版创建角色-验证角色权限与模版相同-删除角色
        """
        # 获取公共模版列表
        result = False
        get_system_role_template_result = self.role.get_role_template_list()
        assert get_system_role_template_result.status_code == 200, "获取角色模版列表失败，{}".format(
            json.dumps(get_system_role_template_result.json(), indent=4)
        )
        name_result = self.common.get_value_list(get_system_role_template_result.json(), 'name')
        uuid_result = self.common.get_value_list(get_system_role_template_result.json(), 'uuid')
        personal_index = self.common.get_value_list(get_system_role_template_result.json(), 'official')
        puuid = dict(zip(uuid_result, personal_index))
        pname = dict(zip(name_result, personal_index))
        uuid = del_private_role_template(puuid, False)
        name = del_private_role_template(pname, False)
        assert self.system_role_template.issubset(name), "角色模版中不包含所有的系统预设角色模版"
        name_uuid = dict(zip(name, uuid))

        # 生成权限列表
        for key, value in name_uuid.items():
            # 生成权限模版
            generate_permission_by_role_template_result = self.role.generate_permission_by_role_template(
                role_template_uuid=value,
                params={
                    "dry-run": "true"
                }
            )
            assert generate_permission_by_role_template_result.status_code == 200, "请求角色模版失败，角色模版名称：{}, 响应结果：{}".format(
                key,
                json.dumps(generate_permission_by_role_template_result.json(), indent=4)
            )

            # 生成权限
            response_text = replace_data(generate_permission_by_role_template_result.text, {
                "{{project_name}}": "project",
                "{{space_name}}": "space",
                "{{namespace_name}}": "namespace"
            })

            # 创建角色
            body = {
                "name": "role-template-{}".format(key),
                "parents": [],
                "permissions": eval(response_text),
                "template_uuid": value
            }
            body = json.dumps(body)
            create_role_by_role_template_result = self.role.create_role(body=body)
            assert create_role_by_role_template_result.status_code == 200, "根据{}模版创建角色失败，返回结果：{}".format(
                key,
                json.dumps(create_role_by_role_template_result.json(), indent=4)
            )

            # # 生成权限验证文件 注释的代码是为了准备校验数据时使用，由于角色模版经常发生变化，每次有改变均需要执行此脚本，准备数据，
            # 实际测试时，需要把代码注释掉
            # write_permission_list = []
            # for uuid_value in create_role_by_role_template_result.json()[0]['permissions']:
            #     uuid_value.pop('uuid')
            #     write_permission_list.append(uuid_value)
            #     print(write_permission_list)
            # with open('./test_data/role/role-template/{}.json'.format(key), 'w') as f:
            #     json.dump(write_permission_list, f)

            # 判断权限正确性
            assert set(
                many_to_one_arry(
                    self.common.get_value_list(
                        self.common.get_value(
                            create_role_by_role_template_result.json(), '0.permissions'), 'actions'))).issubset(
                many_to_one_arry(self.get_file_data(key)['actions'])), "{}系统统预制角色模版有错误，actions资源与预存数据不符合".format(
                key
            )
            assert set(
                many_to_one_arry(
                    self.common.get_value_list(
                        self.common.get_value(
                            create_role_by_role_template_result.json(), '0.permissions'), 'resource_type'))).issubset(
                many_to_one_arry(self.get_file_data(key)['resource_type'])), "{}系统统预制角色模版有错误，resource_type资源与预存数据不符合".format(
                key
            )

            resource = dict(zip(
                self.common.get_value_list(
                    self.common.get_value(
                        create_role_by_role_template_result.json(), '0.permissions'), 'resource_type'),
                self.common.get_value_list(
                    self.common.get_value(create_role_by_role_template_result.json(), '0.permissions'),
                    'resource_type')
            ))

            except_resource = dict(zip(
                self.get_file_data(key)['resource_type'], self.get_file_data(key)['resource']
            ))

            constraints = dict(zip(
                self.common.get_value_list(
                    self.common.get_value(
                        create_role_by_role_template_result.json(), '0.permissions'), 'resource_type'),
                self.common.get_value_list(
                    self.common.get_value(create_role_by_role_template_result.json(), '0.permissions'),
                    'constraints')
            ))

            except_constraints = dict(zip(
                self.get_file_data(key)['resource_type'], self.get_file_data(key)['constraints']
            ))

            assert set(resource).issubset(set(except_resource)), "{}系统统预制角色模版有错误，resource资源与预存数据不符合".format(
                key
            )
            assert set(constraints).issubset(set(except_constraints)), "{}系统统预制角色模版有错误，constraints资源与预存数据不符合".format(
                key
            )

            delete_role = self.role.delete_role("role-template-{}".format(key))

            assert delete_role.status_code == 204, "删除角色模版，响应结果：{}".format(delete_role)

            # 判断是否遍历到最后一个值，保证for循环执行
            if key == list(name_uuid.keys())[-1]:
                result = True
        assert result is True, "系统角色模版测试失败"
