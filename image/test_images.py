from test_case.image.image import Image
import pytest


@pytest.mark.BAT
@pytest.mark.ace
@pytest.mark.flaky(reruns=2, reruns_delay=3)
class TestImageSuite(object):
    def setup_class(self):
        self.image_tool = Image()
        self.index = 10
        self.update_repo = "update daemon"
        self.reg_project_name = self.image_tool.region_name
        self.repo_name = self.image_tool.region_name

    def teardown_class(self):
        self.image_tool.delete_reg_project(self.reg_project_name)

    def test_repo_project_params(self):
        """
        创建镜像项目-获取镜像项目-获取带项目空间镜像项目-删除镜像项目
        :return:
        """
        create_reg_ret = self.image_tool.create_reg_project('./test_data/image/create_reg_project.yaml',
                                                            {"$REG_PROJECT_NAME": self.reg_project_name})
        assert create_reg_ret.status_code == 201, "创建镜像项目操作失败{}".format(create_reg_ret.text)
        get_reg_project = self.image_tool.get_reg_project()
        assert get_reg_project.status_code == 200, "获取镜像项目失败{}".format(get_reg_project.text)
        get_reg_project = self.image_tool.get_reg_project(self.image_tool.params)
        assert get_reg_project, "获取项目空间下镜像项目失败{}".format(get_reg_project)
        delete_reg_ret = self.image_tool.delete_reg_project(self.reg_project_name)
        assert delete_reg_ret.status_code == 204, "删除镜像项目操作失败{}".format(delete_reg_ret.text)

    def test_multiple_project(self):
        """
        循环开始-创建镜像项目-获取镜像项目-删除镜像项目-循环结束
        :return:
        """
        # create registry project
        # 循环创建多个镜像项目 由index控制创建次数 然后删除
        for i in range(1, self.index):
            create_reg_project = self.image_tool.create_reg_project('./test_data/image/create_reg_project.yaml',
                                                                    {"$REG_PROJECT_NAME": self.reg_project_name + str(i)})
            assert create_reg_project.status_code == 201, "创建镜像项目操作失败{}".format(create_reg_project.text)
            # get registry project
            get_reg_project = self.image_tool.get_reg_project()
            assert get_reg_project.status_code == 200, "获取镜像项目失败{}".format(get_reg_project.text)
            # delete registry project
            delete_reg_project = self.image_tool.delete_reg_project(self.reg_project_name + str(i))
            assert delete_reg_project.status_code == 204, "删除镜像项目操作失败{}".format(delete_reg_project.text)

    def test_one_project_multiple_repo(self):
        # create registry project
        # 循环创建多个镜像项目 由index控制创建次数 然后删除
        """
        创建镜像项目-循环开始创建镜像仓库-删除镜像仓库-删除镜像项目
        :return:
        """
        create_reg_ret = self.image_tool.create_reg_project('./test_data/image/create_reg_project.yaml',
                                                            {"$REG_PROJECT_NAME": self.reg_project_name})
        assert create_reg_ret.status_code == 201, "创建镜像项目操作失败{}".format(create_reg_ret.text)
        for i in range(1, self.index):
            create_repo_ret = self.image_tool.create_repo('./test_data/image/create_repo.yaml',
                                                          {"$REPO_IMAGE": self.repo_name + str(i)},
                                                          reg_project_name=self.reg_project_name)
            assert create_repo_ret.status_code == 201, "创建镜像仓库操作失败{}".format(create_repo_ret.text)
            # delete repo
            delete_repo_ret = self.image_tool.delete_repo(self.repo_name + str(i),
                                                          reg_project_name=self.reg_project_name)
            assert delete_repo_ret.status_code == 204, "删除镜像仓库操作失败{}".format(delete_repo_ret.text)
        # delete registry project
        delete_reg_ret = self.image_tool.delete_reg_project(self.reg_project_name)
        assert delete_reg_ret.status_code == 204, "删除镜像项目操作失败{}".format(delete_reg_ret.text)

    def test_shared_multiple_repo(self):
        """
        共享空间-循环开始创建镜像仓库-删除镜像仓库
        :return:
        """
        # create registry project
        for i in range(1, self.index):
            create_repo_ret = self.image_tool.create_repo('./test_data/image/create_repo.yaml',
                                                          {"$REPO_IMAGE": self.repo_name + str(i)})
            assert create_repo_ret.status_code == 201, "创建镜像仓库操作失败{}".format(create_repo_ret.text)
            # delete repo
            delete_repo_ret = self.image_tool.delete_repo(self.repo_name + str(i))
            assert delete_repo_ret.status_code == 204, "删除镜像仓库操作失败{}".format(delete_repo_ret.text)

    def test_project_repo(self):
        """
        "创建镜像项目-获取镜像项目-创建镜像仓库-获取镜像仓库-更新镜像仓库-获取镜像仓库详情-验证更新结果-删除镜像仓库-删除镜像项目"
        :return:
        """
        # create registry project
        create_reg_ret = self.image_tool.create_reg_project('./test_data/image/create_reg_project.yaml',
                                                            {"$REG_PROJECT_NAME": self.reg_project_name})
        assert create_reg_ret.status_code == 201, "创建镜像项目操作失败{}".format(create_reg_ret.text)

        # get registry project
        get_reg_ret = self.image_tool.get_reg_project()
        assert get_reg_ret.status_code == 200, "获取镜像项目操作失败{}".format(get_reg_ret.text)

        # create repo
        create_repo_ret = self.image_tool.create_repo('./test_data/image/create_repo.yaml',
                                                      {"$REPO_IMAGE": self.repo_name},
                                                      reg_project_name=self.reg_project_name)
        assert create_repo_ret.status_code == 201, "创建镜像仓库操作失败{}".format(create_repo_ret.text)

        # get repo
        get_repo_ret = self.image_tool.get_repo_detail(self.repo_name, reg_project_name=self.reg_project_name)
        assert get_repo_ret.status_code == 200, "获取镜像仓库失败{}".format(get_repo_ret.text)

        # update repo
        update_repo_ret = self.image_tool.update_repo(self.repo_name, './test_data/image/update_repo.yaml',
                                                      {"$UPDATE_REPO": self.update_repo},
                                                      reg_project_name=self.reg_project_name)
        assert update_repo_ret.status_code == 200, "更新镜像仓库操作失败{}".format(update_repo_ret.text)
        # get repo detail after update
        get_repo_detail = self.image_tool.get_repo_detail(self.repo_name, reg_project_name=self.reg_project_name)
        assert get_repo_detail.status_code == 200, "获取镜像仓库详情失败{}".format(get_repo_detail.text)
        # verify the update value
        content = get_repo_detail.json()
        ret = self.image_tool.get_value(content, 'full_description')
        assert ret == self.update_repo, "更新镜像仓库失败"

        # delete repo
        delete_repo_ret = self.image_tool.delete_repo(self.repo_name, reg_project_name=self.reg_project_name)
        assert delete_repo_ret.status_code == 204, "删除镜像仓库操作失败{}".format(delete_repo_ret.text)

        # delete registry project
        delete_reg_ret = self.image_tool.delete_reg_project(self.reg_project_name)
        assert delete_reg_ret.status_code == 204, "删除镜像项目操作失败{}".format(delete_reg_ret.text)

    def test_shared_repo(self):
        """
        共享空间-创建镜像项目-获取镜像项目-创建镜像仓库-获取镜像仓库-更新镜像仓库-获取镜像仓库详情-验证更新结果-删除镜像仓库-删除镜像项目
        :return:
        """
        # create repo
        create_repo_ret = self.image_tool.create_repo('./test_data/image/create_repo.yaml',
                                                      {"$REPO_IMAGE": self.repo_name})
        assert create_repo_ret.status_code == 201, "创建镜像仓库操作失败{}".format(create_repo_ret.text)

        # get repo
        get_repo_ret = self.image_tool.get_repo_detail(self.repo_name)
        assert get_repo_ret.status_code == 200, "获取镜像仓库失败{}".format(get_repo_ret.text)

        # update repo
        update_repo_ret = self.image_tool.update_repo(self.repo_name, './test_data/image/update_repo.yaml',
                                                      {"$UPDATE_REPO": self.update_repo})
        assert update_repo_ret.status_code == 200, "更新镜像仓库操作失败{}".format(update_repo_ret.text)
        # get repo detail after update
        get_repo_detail = self.image_tool.get_repo_detail(self.repo_name,)
        assert get_repo_detail.status_code == 200, "获取镜像仓库详情失败"
        # verify the update value
        content = get_repo_detail.json()
        ret = self.image_tool.get_value(content, 'full_description')
        assert ret == self.update_repo, "更新镜像仓库失败"

        # delete repo
        delete_repo_ret = self.image_tool.delete_repo(self.repo_name)
        assert delete_repo_ret.status_code == 204, "删除镜像项目操作失败{}".format(delete_repo_ret.text)
