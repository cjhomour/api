import pytest

from test_case.newapp.newapp import Newapplication
from test_case.subnet.subnet import Subnet


@pytest.mark.subnet
@pytest.mark.ace
class TestSubnetSuite(object):
    def setup_class(self):
        self.subnet = Subnet()
        self.subnet_name = 'alauda-subnet-{}'.format(self.subnet.region_name).replace('_', '-')
        # macvlan cidr需要和主机同网段
        self.masterip = self.subnet.global_info['$MASTERIPS'].split(',')[0]
        gateway = self.masterip.split('.')
        gateway.pop()
        self.macvlan_gateway = '.'.join(gateway)
        self.macvlan_cidr = "{}.0/24".format(self.macvlan_gateway)
        self.cidr_update = "{}.0/20".format(self.macvlan_gateway)
        self.ip1 = "{}.110".format(self.macvlan_gateway)
        self.ip2 = "{}.111".format(self.macvlan_gateway)
        self.ip3 = "{}.112".format(self.macvlan_gateway)

        # calico cidr不能和主机重合
        self.calico_gateway = '19.19.0'
        self.calico_cidr = "{}.0/24".format(self.calico_gateway)
        self.calico_ip1 = "{}.110".format(self.calico_gateway)

        self.newapp = Newapplication()
        self.k8s_namespace = self.newapp.global_info["$K8S_NAMESPACE"]
        self.newapp_name = 'subnet-statefulset'
        self.newapp_name_ip = 'ip-statefulset'
        self.teardown_class(self)

    def teardown_class(self):
        self.newapp.delete_newapp(self.k8s_namespace, self.newapp_name)
        self.newapp.delete_newapp(self.k8s_namespace, self.newapp_name_ip)
        if self.subnet.global_info['$NETWORK_TYPE'] == 'macvlan':
            self.subnet.delete_ips(self.subnet_name, self.ip1)
            self.subnet.delete_ips(self.subnet_name, self.ip2)
            self.subnet.delete_ips(self.subnet_name, self.ip3)
        self.subnet.delete_subnet(self.subnet_name)

    @pytest.mark.BAT
    def test_macvlan_subnet(self):
        '''
        macvlan子网测试:创建子网-更新子网-子网列表-子网详情-导入IP list-删除IP-导入IP range-IP列表-创建应用指定子网/IP-删除IP-删除子网
        :return:
        '''
        if self.subnet.global_info['$NETWORK_TYPE'] != 'macvlan':
            return True, "集群网络模式不是macvlan,不需要测试"
        crd_result = self.subnet.get_subnet_crd()
        assert crd_result.status_code == 200, "获取subnet的crd 失败:{}".format(crd_result.text)
        if len(crd_result.json()) == 0:
            assert False, "集群不支持subnet,请先部署subnet crd"

        result = {"flag": True}
        # create subnet
        createsubnet_result = self.subnet.create_subnet("./test_data/subnet/macvlan-subnet.json",
                                                        {"$subnet_name": self.subnet_name, "$cidr": self.macvlan_cidr,
                                                         '$gateway': self.macvlan_gateway})
        assert createsubnet_result.status_code == 201, "创建子网失败:{}".format(createsubnet_result.text)

        # update subnet
        update_result = self.subnet.update_subnet(self.subnet_name, "./test_data/subnet/macvlan-subnet.json",
                                                  {"$subnet_name": self.subnet_name, "$cidr": self.cidr_update})
        assert update_result.status_code == 204, "更新子网出错:{}".format(update_result.text)

        # list subnet
        list_result = self.subnet.list_subnet()
        result = self.subnet.update_result(result, list_result.status_code == 200, list_result.text)
        result = self.subnet.update_result(result, self.subnet_name in list_result.text, "子网列表：新建子网不在列表中")

        # detail subnet
        detail_result = self.subnet.get_subnet_detail(self.subnet_name)
        result = self.subnet.update_result(result, detail_result.status_code == 200, detail_result.text)
        result = self.subnet.update_result(result, self.subnet.get_value(detail_result.json(),
                                                                         'kubernetes.spec.cidr_block') == self.cidr_update,
                                           detail_result.text)

        # import list ip
        import_ip_list_result = self.subnet.create_ips(self.subnet_name, "./test_data/subnet/ip-list.json",
                                                       {'$ip3': self.ip3})
        assert import_ip_list_result.status_code == 201, "导入IP list失败:{}".format(import_ip_list_result.text)

        delete_result = self.subnet.delete_subnet(self.subnet_name)
        assert delete_result.status_code == 400, "子网非空 不能删除：{}".format(delete_result.text)

        # delete ip
        delete_ip_result = self.subnet.delete_ips(self.subnet_name, self.ip3)
        assert delete_ip_result.status_code == 204, "删除IP失败：{}".format(delete_ip_result.text)

        # wait for subnet empty
        self.subnet.check_value_in_response(self.subnet.get_private_ip_url(self.subnet_name), '[]')
        list_ip_result = self.subnet.list_ips(self.subnet_name)
        result = self.subnet.update_result(result, self.ip3 not in list_ip_result.text,
                                           "删除IP后：IP还在列表中")

        # import range ip
        range_ip_result = self.subnet.create_ips(self.subnet_name, "./test_data/subnet/ip-range.json",
                                                 {'$ip1': self.ip1, '$ip2': self.ip2})
        assert range_ip_result.status_code == 201, "导入IP range失败:{}".format(range_ip_result.text)

        # list ip
        list_ip_result = self.subnet.list_ips(self.subnet_name)
        result = self.subnet.update_result(result, list_ip_result.status_code == 200, list_ip_result.text)
        result = self.subnet.update_result(result, len(list_ip_result.json()) == 2, "IP列表：新建IP不在列表中")

        # create app with ip
        create_result = self.newapp.create_newapp('./test_data/newapp/macvlan-ip-statefulset.json',
                                                  {'$newapp_name': self.newapp_name_ip,
                                                   '$subnet_ip': self.ip2})
        assert create_result.status_code == 201, "新版应用创建失败 {}".format(create_result.text)
        app_status = self.newapp.get_newapp_status(self.k8s_namespace, self.newapp_name_ip, 'Running')
        assert app_status, "创建应用后，验证应用状态出错：app: {} is not running".format(self.newapp_name)

        # create app with subnet
        create_result = self.newapp.create_newapp('./test_data/newapp/macvlan-subnet-statefulset.json',
                                                  {'$newapp_name': self.newapp_name, '$subnet_name': self.subnet_name})
        assert create_result.status_code == 201, "新版应用创建失败 {}".format(create_result.text)
        app_status = self.newapp.get_newapp_status(self.k8s_namespace, self.newapp_name, 'Running')
        assert app_status, "创建应用后，验证应用状态出错：app: {} is not running".format(self.newapp_name)

        list_ip_result = self.subnet.list_ips(self.subnet_name)
        result = self.subnet.update_result(result, list_ip_result.status_code == 200, list_ip_result.text)
        result = self.subnet.update_result(result, self.subnet.get_value(list_ip_result.json(),
                                                                         '0.kubernetes.spec.used') is True,
                                           "ip状态不是使用中")
        result = self.subnet.update_result(result, self.subnet.get_value(list_ip_result.json(),
                                                                         '1.kubernetes.spec.used') is True,
                                           "ip状态不是使用中")

        delete_result = self.subnet.delete_ips(self.subnet_name, self.ip1)
        assert delete_result.status_code == 400, "IP使用中 不能删除：{}".format(delete_result.text)

        # delete app
        delete_result = self.newapp.delete_newapp(self.k8s_namespace, self.newapp_name_ip)
        assert delete_result.status_code == 204, "删除应用失败 {}".format(delete_result.text)
        self.newapp.check_exists(self.newapp.get_newapp_common_url(self.k8s_namespace, self.newapp_name_ip), 404)

        # delete app
        delete_result = self.newapp.delete_newapp(self.k8s_namespace, self.newapp_name)
        assert delete_result.status_code == 204, "删除应用失败 {}".format(delete_result.text)
        self.newapp.check_exists(self.newapp.get_newapp_common_url(self.k8s_namespace, self.newapp_name), 404)

        # wait for ip not used
        self.subnet.get_status(self.subnet.get_private_ip_url(self.subnet_name), '0.kubernetes.spec.used', False)
        self.subnet.get_status(self.subnet.get_private_ip_url(self.subnet_name), '1.kubernetes.spec.used', False)

        self.subnet.delete_ips(self.subnet_name, self.ip1)
        self.subnet.delete_ips(self.subnet_name, self.ip2)

        # wait for subnet empty
        self.subnet.check_value_in_response(self.subnet.get_private_ip_url(self.subnet_name), '[]')

        # delete subnet
        delete_result = self.subnet.delete_subnet(self.subnet_name)
        assert delete_result.status_code == 204, "删除子网失败：{}".format(delete_result.text)
        assert self.subnet.check_exists(self.subnet.get_common_subnet_url(self.subnet_name), 404)
        assert result['flag'], result

    @pytest.mark.BAT
    def test_calico_subnet(self):
        '''
        calico子网测试:创建子网-子网列表-更新子网-子网详情-IP列表为空-创建应用指定子网-验证IP状态-创建应用指定IP-验证应用容器IP-IP列表-删除非空子网-更新非空子网-删除子网
        :return:
        '''

        if self.subnet.global_info['$NETWORK_TYPE'] != 'calico':
            return True, "集群网络模式不是calico,不需要测试"
        crd_result = self.subnet.get_subnet_crd()
        assert crd_result.status_code == 200, "获取subnet的crd 失败:{}".format(crd_result.text)
        if len(crd_result.json()) == 0:
            assert False, "集群不支持subnet,请先部署subnet crd"

        result = {"flag": True}
        # create subnet
        createsubnet_result = self.subnet.create_subnet_calico("./test_data/subnet/calico-subnet.json",
                                                               {"$subnet_name": self.subnet_name,
                                                                "$cidr": self.calico_cidr})
        assert createsubnet_result.status_code == 201, "创建子网失败:{}".format(createsubnet_result.text)

        # list subnet
        list_result = self.subnet.list_subnet()
        result = self.subnet.update_result(result, list_result.status_code == 200, list_result.text)
        result = self.subnet.update_result(result, self.subnet_name in list_result.text, "子网列表：新建子网不在列表中")

        # update subnet
        update_result = self.subnet.update_subnet(self.subnet_name, './test_data/subnet/update-calico-subnet.json',
                                                  {'$mode': 'Always', '"$nat"': 'false'})
        assert update_result.status_code == 204, "更新子网出错:{}".format(update_result.text)

        # detail subnet
        detail_result = self.subnet.get_subnet_detail(self.subnet_name)
        result = self.subnet.update_result(result, detail_result.status_code == 200, detail_result.text)
        result = self.subnet.update_result(result,
                                           self.subnet.get_status(self.subnet.get_common_subnet_url(self.subnet_name),
                                                                  'kubernetes.spec.ipip_mode', 'Always'),
                                           '更新子网后ipip_mode不是Always')

        # list IP
        list_ip_result = self.subnet.list_ips(self.subnet_name)
        result = self.subnet.update_result(result, len(list_ip_result.json()) == 0, "IP列表不为空")

        # create app with subnet
        create_result = self.newapp.create_newapp_by_yaml(self.k8s_namespace, self.newapp_name,
                                                          './test_data/newapp/calico-subnet-statefulset.yml',
                                                          {'$newapp_name': self.newapp_name,
                                                           '$subnet_cidr': self.calico_cidr})
        assert create_result.status_code == 201, "新版应用创建失败 {}".format(create_result.text)
        app_status = self.newapp.get_newapp_status(self.k8s_namespace, self.newapp_name, 'Running')
        assert app_status, "创建应用后，验证应用状态出错：app: {} is not running".format(self.newapp_name)

        list_ip_result = self.subnet.list_ips(self.subnet_name)
        result = self.subnet.update_result(result, list_ip_result.status_code == 200, list_ip_result.text)
        result = self.subnet.update_result(result, len(list_ip_result.json()) == 1, "IP列表：不是1个")
        result = self.subnet.update_result(result, self.subnet.get_value(list_ip_result.json(),
                                                                         '0.kubernetes.spec.used') is True,
                                           "ip状态不是使用中")

        # delete app
        delete_result = self.newapp.delete_newapp(self.k8s_namespace, self.newapp_name)
        assert delete_result.status_code == 204, "删除应用失败 {}".format(delete_result.text)
        self.newapp.check_exists(self.newapp.get_newapp_common_url(self.k8s_namespace, self.newapp_name), 404)

        # create app with IP
        create_result = self.newapp.create_newapp_by_yaml(self.k8s_namespace, self.newapp_name_ip,
                                                          './test_data/newapp/calico-ip-statefulset.yml',
                                                          {'$newapp_name': self.newapp_name_ip,
                                                           '$subnet_ip': self.calico_ip1})
        assert create_result.status_code == 201, "新版应用创建失败 {}".format(create_result.text)
        app_status = self.newapp.get_newapp_status(self.k8s_namespace, self.newapp_name_ip, 'Running')
        assert app_status, "创建应用后，验证应用状态出错：app: {} is not running".format(self.newapp_name_ip)
        podip = self.newapp.get_status(self.newapp.get_newapp_pod_url(self.k8s_namespace, self.newapp_name_ip),
                                       '0.kubernetes.status.podIP', self.calico_ip1)
        assert podip, "应用运行后，容器IP不是{}".format(self.calico_ip1)

        # list ip
        list_ip_result = self.subnet.list_ips(self.subnet_name)
        result = self.subnet.update_result(result, list_ip_result.status_code == 200, list_ip_result.text)
        result = self.subnet.update_result(result, self.calico_ip1 in list_ip_result.text,
                                           "{}不在列表中".format(self.calico_ip1))

        delete_result = self.subnet.delete_subnet(self.subnet_name)
        assert delete_result.status_code == 400, "子网非空 不能删除：{}".format(delete_result.text)

        # update subnet not empty
        update_result = self.subnet.update_subnet(self.subnet_name, './test_data/subnet/update-calico-subnet.json',
                                                  {'$mode': 'Never', '"$nat"': 'true'})
        assert update_result.status_code == 204, "子网非空时，更新子网出错:{}".format(update_result.text)
        result = self.subnet.update_result(result,
                                           self.subnet.get_status(self.subnet.get_common_subnet_url(self.subnet_name),
                                                                  'kubernetes.spec.ipip_mode', 'Never'),
                                           '子网非空时，更新子网后ipip_mode不是never')
        result = self.subnet.update_result(result,
                                           self.subnet.get_status(self.subnet.get_common_subnet_url(self.subnet_name),
                                                                  'kubernetes.spec.nat_outgoing', True),
                                           '子网非空时，更新子网后nat_outgoing不是True')

        # delete app
        delete_result = self.newapp.delete_newapp(self.k8s_namespace, self.newapp_name_ip)
        assert delete_result.status_code == 204, "删除应用失败 {}".format(delete_result.text)
        self.newapp.check_exists(self.newapp.get_newapp_common_url(self.k8s_namespace, self.newapp_name_ip), 404)

        # wait for subnet empty
        self.subnet.check_value_in_response(self.subnet.get_private_ip_url(self.subnet_name), '[]')

        # delete subnet
        delete_result = self.subnet.delete_subnet(self.subnet_name)
        assert delete_result.status_code == 204, "删除子网失败：{}".format(delete_result.text)
        assert self.subnet.check_exists(self.subnet.get_common_subnet_url(self.subnet_name), 404)
        assert result['flag'], result
