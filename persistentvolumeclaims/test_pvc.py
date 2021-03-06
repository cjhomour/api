import pytest

from test_case.persistentvolumeclaims.pvc import Pvc
from test_case.storageclasses.scs import Scs


@pytest.mark.pvc
@pytest.mark.ace
@pytest.mark.flaky(reruns=2, reruns_delay=3)
class TestPvcSuite(object):
    def setup_class(self):

        self.pvc = Pvc()
        self.pvc_name = 'alauda-pvc-{}'.format(self.pvc.region_name).replace('_', '-')
        self.k8s_namespace = self.pvc.global_info["$K8S_NAMESPACE"]
        self.scs = Scs()
        self.scs_name = 'alauda-scsforpvc-{}'.format(self.pvc.region_name).replace('_', '-')
        self.pvcusescs_name = 'alauda-pvcusescs-{}'.format(self.pvc.region_name).replace('_', '-')
        self.masterips = self.scs.global_info["$MASTERIPS"].split(",")
        self.default_size = self.scs.get_default_size()

        self.defaultscs_name = 'alauda-defaultscsforpvc-{}'.format(self.pvc.region_name).replace('_', '-')
        self.pvcusedefaultscs_name = 'alauda-pvcusedefaultscs-{}'.format(self.pvc.region_name).replace('_', '-')

        self.teardown_class(self)

    def teardown_class(self):
        self.scs.delete_scs(self.defaultscs_name)
        self.pvc.delete_pvc(self.k8s_namespace, self.pvcusedefaultscs_name)
        self.scs.delete_scs(self.scs_name)
        self.pvc.delete_pvc(self.k8s_namespace, self.pvcusescs_name)

    @pytest.mark.scs
    def test_pvc_use_scs(self):
        result = {"flag": True}
        create_result = self.scs.create_scs("./test_data/scs/scs.yml",
                                            {"$scs_name": self.scs_name, "$is_default": "false",
                                             })
        assert create_result.status_code == 201, "创建sc失败{}".format(create_result.text)

        # create pvc
        createpvc_result = self.pvc.create_pvc("./test_data/pvc/pvc.json",
                                               {"$pvc_name": self.pvcusescs_name, "$pvc_mode": "ReadWriteOnce",
                                                "$scs_name": self.scs_name, "$size": "1"})
        assert createpvc_result.status_code == 201, "创建pvc失败{}".format(createpvc_result.text)
        self.pvc.get_status(self.pvc.get_common_pvc_url(self.k8s_namespace, self.pvcusescs_name),
                            "status.phase", "Bound")
        # list pvc
        list_result = self.pvc.list_pvc()
        result = self.pvc.update_result(result, list_result.status_code == 200, list_result.text)
        result = self.pvc.update_result(result, self.pvcusescs_name in list_result.text, "获取持久卷声明列表：新建pvc不在列表中")
        # get pvc detail
        detail_result = self.pvc.get_pvc_detail(self.k8s_namespace, self.pvcusescs_name)
        result = self.pvc.update_result(result, detail_result.status_code == 200, detail_result.text)
        result = self.pvc.update_result(result, self.pvc.get_value(detail_result.json(), "status.phase") == "Bound",
                                        "pvc详情状态不是绑定{}".format(detail_result.text))
        volumeName = self.pvc.get_value(detail_result.json(), "kubernetes.spec.volumeName")
        result = self.pvc.update_result(result, volumeName.startswith("pvc"),
                                        "pvc详情关联持久卷不是以pvc开头的{}".format(detail_result.text))
        # update pvc
        update_result = self.pvc.update_pvc(self.k8s_namespace, self.pvcusescs_name, "./test_data/pvc/pvc-update.json",
                                            {"$pvc_name": self.pvcusescs_name, "$pvc_mode": "ReadWriteOnce",
                                             "$scs_name": self.scs_name, "$size": "1", "$vol_name": volumeName})
        result = self.pvc.update_result(result, update_result.status_code == 204, update_result.text)
        # get pvc detail
        detail_result = self.pvc.get_pvc_detail(self.k8s_namespace, self.pvcusescs_name)
        result = self.pvc.update_result(result, detail_result.status_code == 200, detail_result.text)
        result = self.pvc.update_result(result,
                                        self.pvc.get_value(detail_result.json(), "kubernetes.metadata.labels") == {
                                            "e2e": "pvc"},
                                        "pvc详情的标签没有更新{}".format(detail_result.text))
        result = self.pvc.update_result(result,
                                        self.pvc.get_value(detail_result.json(), "kubernetes.metadata.annotations") == {
                                            "e2e": "pvc"},
                                        "pvc详情的描述没有更新{}".format(detail_result.text))

        # delete pvc
        delete_result = self.pvc.delete_pvc(self.k8s_namespace, self.pvcusescs_name)
        assert delete_result.status_code == 204, "删除pvc失败 {}".format(delete_result.text)
        assert self.pvc.check_exists(
            self.pvc.get_common_pvc_url(self.k8s_namespace, self.pvcusescs_name),
            404)
        self.scs.delete_scs(self.scs_name)
        assert result['flag'], result

    @pytest.mark.scs
    def test_pvc_use_defaultscs(self):
        if self.default_size > 1:
            assert False, "有两个以上的默认存储类，无法测试"
        elif self.default_size == 0:
            create_result = self.scs.create_scs("./test_data/scs/scs.yml",
                                                {"$scs_name": self.defaultscs_name, "$is_default": "true",
                                                 })
            assert create_result.status_code == 201, "创建sc失败{}".format(create_result.text)
        result = {"flag": True}
        # create pvc
        createpvc_result = self.pvc.create_pvc("./test_data/pvc/pvc_usedefault.json",
                                               {"$pvc_name": self.pvcusedefaultscs_name, "$pvc_mode": "ReadWriteOnce",
                                                "$size": "1"})
        assert createpvc_result.status_code == 201, "创建pvc失败{}".format(createpvc_result.text)
        self.pvc.get_status(
            self.pvc.get_common_pvc_url(self.k8s_namespace, self.pvcusedefaultscs_name),
            "status.phase", "Bound")
        # get pvc detail
        detail_result = self.pvc.get_pvc_detail(self.k8s_namespace, self.pvcusedefaultscs_name)
        result = self.pvc.update_result(result, detail_result.status_code == 200, detail_result.text)
        result = self.pvc.update_result(result, self.pvc.get_value(detail_result.json(), "status.phase") == "Bound",
                                        "pvc详情状态不是绑定{}".format(detail_result.text))
        result = self.pvc.update_result(result, self.pvc.get_value(detail_result.json(),
                                                                   "kubernetes.spec.volumeName").startswith("pvc"),
                                        "pvc详情关联持久卷不是以pvc开头的{}".format(detail_result.text))
        self.pvc.delete_pvc(self.k8s_namespace, self.pvcusedefaultscs_name)
        self.scs.delete_scs(self.defaultscs_name)
        assert result['flag'], result
