import pytest

from test_case.namespace.namespace import Namespace
from test_case.persistentvolumeclaims.pvc import Pvc


@pytest.mark.BAT
@pytest.mark.ace
@pytest.mark.flaky(reruns=2, reruns_delay=3)
class TestNamespaceSuite(object):
    def setup_class(self):
        self.namespace = Namespace()
        self.general_namespace_name = "{}-general-{}".format(self.namespace.project_name,
                                                             self.namespace.region_name).replace('_', '-')
        self.pvc = Pvc()
        self.pvc_name = 'alauda-pvcforquota-{}'.format(self.namespace.region_name).replace('_', '-')

        self.teardown_class(self)

    def teardown_class(self):
        self.pvc.delete_pvc(self.general_namespace_name, self.pvc_name)
        self.namespace.delete_general_namespaces(self.general_namespace_name)

    @pytest.mark.ns
    def test_general_namespaces(self):
        '''
        创建命名空间-获取resourcequota-获取limitrange-获取命名空间列表-验证配额pvc-更新命名空间-获取resourcequota-获取limitrange-验证配额pvc-删除命名空间
        :return:
        '''
        result = {"flag": True}
        create_ns_result = self.namespace.create_general_namespaces('./test_data/namespace/update_namespace.json',
                                                                    {'$K8S_NAMESPACE': self.general_namespace_name,
                                                                     '"$pvcsize"': "0"})
        assert create_ns_result.status_code == 201, "创建新命名空间失败 {}".format(create_ns_result.text)
        resourcequota_flag = self.namespace.check_exists(
            self.namespace.get_resourcequota_url(self.general_namespace_name, 'default'), 200)
        result = self.namespace.update_result(result, resourcequota_flag, 'resourcequota创建失败')
        limitrange_flag = self.namespace.check_exists(
            self.namespace.get_limitrange_url(self.general_namespace_name, 'default'), 200)
        result = self.namespace.update_result(result, limitrange_flag, 'limitrange创建失败')
        list_ns_result = self.namespace.list_namespaces()
        result = self.namespace.update_result(result, list_ns_result.status_code == 200, '获取命名空间列表失败')
        result = self.namespace.update_result(result, self.general_namespace_name in list_ns_result.text,
                                              '获取命名空间列表失败:新建的不在列表中')
        create_pvc_result = self.pvc.create_pvc("./test_data/pvc/pvc.json",
                                                {"$pvc_name": self.pvc_name, "$pvc_mode": "ReadWriteOnce",
                                                 "$scs_name": "", "$size": "1",
                                                 "$K8S_NAMESPACE": self.general_namespace_name})
        assert create_pvc_result.status_code == 403, "超出配额后,创建pvc成功，应该不能创建"
        update_ns_result = self.namespace.update_general_namespaces(self.general_namespace_name,
                                                                    './test_data/namespace/update_namespace.json',
                                                                    {'$K8S_NAMESPACE': self.general_namespace_name,
                                                                     '"$pvcsize"': "1"})
        assert update_ns_result.status_code == 200, "更新新命名空间失败 {}".format(create_ns_result.text)
        detail_resourcequota = self.namespace.detail_resourcequota(self.general_namespace_name, 'default')
        result = self.namespace.update_result(result, detail_resourcequota.status_code == 200, '获取集群配额失败')
        result = self.namespace.update_result(result, self.namespace.get_value(detail_resourcequota.json(),
                                                                               'kubernetes.spec.hard.persistentvolumeclaims') == '1',
                                              '获取resourcequota错误，persistentvolumeclaims不是1')
        detail_limitrange = self.namespace.detail_limitrange(self.general_namespace_name, 'default')
        result = self.namespace.update_result(result, detail_limitrange.status_code == 200, '获取容器配额失败')
        result = self.namespace.update_result(result, self.namespace.get_value(detail_limitrange.json(),
                                                                               'kubernetes.spec.limits.0.max.memory') == '8G',
                                              '获取limitrange错误，max.memory不是8G')
        create_pvc_result = self.pvc.create_pvc("./test_data/pvc/pvc.json",
                                                {"$pvc_name": self.pvc_name, "$pvc_mode": "ReadWriteOnce",
                                                 "$scs_name": "", "$size": "1",
                                                 "$K8S_NAMESPACE": self.general_namespace_name})
        assert create_pvc_result.status_code == 201, "配额内,创建pvc失败"
        used = self.namespace.get_status(
            self.namespace.get_resourcequota_url(self.general_namespace_name, 'default'),
            'kubernetes.status.used.persistentvolumeclaims', '1')
        result = self.namespace.update_result(result, used, '获取resourcequota详情失败:已使用的pvc数不是1')
        self.pvc.delete_pvc(self.general_namespace_name, self.pvc_name)
        self.pvc.check_exists(self.pvc.get_common_pvc_url(self.general_namespace_name, self.pvc_name), 404)
        delete_ns_result = self.namespace.delete_general_namespaces(self.general_namespace_name)
        assert delete_ns_result.status_code == 204, "删除命名空间失败 {}".format(delete_ns_result.text)
        delete_flag = self.namespace.check_exists(self.namespace.get_namespace_url(self.general_namespace_name), 404)
        assert delete_flag, "删除命名空间失败"
        assert result['flag'], result
