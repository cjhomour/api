from common.base_request import Common
from common.log import logger


class Image(Common):
    def __init__(self):
        super(Image, self).__init__()

    def create_repo_url(self, reg_project_name=None):
        if reg_project_name:
            path = "/v1/registries/{}/{}/projects/{}/repositories".format(self.account, self.registry_name,
                                                                          reg_project_name)
        else:
            path = "/v1/registries/{}/{}/repositories".format(self.account, self.registry_name)

        return path

    def common_url(self, repo_name, reg_project_name=None):
        if reg_project_name:
            path = "/v1/registries/{}/{}/projects/{}/repositories/{}".format(self.account, self.registry_name,
                                                                             reg_project_name, repo_name)
        else:
            path = "/v1/registries/{}/{}/repositories/{}".format(self.account, self.registry_name, repo_name)
        return path

    def create_reg_project_url(self):
        return "/v1/registries/{}/{}/projects".format(self.account, self.registry_name)

    def delete_reg_project_url(self, reg_project_name):
        return "/v1/registries/{}/{}/projects/{}".format(self.account, self.registry_name, reg_project_name)

    def get_repo_tag_url(self, repo_name, reg_project_name=None):
        if reg_project_name:
            path = "/v1/registries/{}/{}/projects/{}/repositories/{}/tags".format(self.account, self.registry_name,
                                                                                  reg_project_name, repo_name)
        else:
            path = "/v1/registries/{}/{}/repositories/{}/tags?view_type=detail&page_size=20".format(
                self.account, self.registry_name, repo_name)
        return path

    def get_delete_repo_tag_url(self, repo_name, tag_name, reg_project_name=None):
        if reg_project_name:
            path = "/v1/registries/{}/{}/projects/{}/repositories/{}/tags/{}"\
                .format(self.account, self.registry_name, reg_project_name, repo_name, tag_name)
        else:
            path = "/v1/registries/{}/{}/repositories/{}/tags/{}"\
                .format(self.account, self.registry_name, repo_name, tag_name)
        return path

    def get_reg_project_list_url(self):
        return "/v1/registries/{}/{}/projects".format(self.account, self.registry_name)

    def get_repo_list_url(self, reg_project_name=None):
        if reg_project_name:
            path = "/v1/registries/{}/{}/projects/{}/repositories?page=1&page_size=20&".format(self.account,
                                                                                               self.registry_name,
                                                                                               reg_project_name)
        else:
            path = "/v1/registries/{}/{}/repositories?page=1&page_size=20&".format(self.account, self.registry_name)
        return path

    def get_image_url(self, repo_name, repo_tag, reg_project=None):
        if reg_project:
            path = "/v1/registries/{}/{}/projects/{}/repositories/{}/tags/{}" \
                .format(self.account, self.registry_name, reg_project, repo_name, repo_tag)
        else:
            path = "/v1/registries/{}/{}/repositories/{}/tags/{}" \
                .format(self.account, self.registry_name, repo_name, repo_tag)

        return path

    def create_reg_project(self, file, data):
        logger.info("************************** create registry project ********************************")
        path = self.create_reg_project_url()
        data = self.generate_data(file, data)
        return self.send(method='post', path=path, data=data, params={})

    def delete_reg_project(self, reg_project_name):
        logger.info("************************** delete registry project ********************************")
        path = self.delete_reg_project_url(reg_project_name)
        return self.send(method='delete', path=path, params={})

    def create_repo(self, file, data, reg_project_name=None):
        logger.info("************************** create repository ********************************")
        path = self.create_repo_url(reg_project_name=reg_project_name)
        data = self.generate_data(file, data)
        return self.send(method='post', path=path, data=data, params={})

    def update_repo(self, repo_name, file, data, reg_project_name=None):
        logger.info("************************** update repository ********************************")
        path = self.common_url(repo_name, reg_project_name=reg_project_name)
        data = self.generate_data(file, data)
        return self.send(method='put', path=path, data=data, params={})

    def delete_repo(self, repo_name, reg_project_name=None):
        logger.info("************************** delete repository ********************************")
        path = self.common_url(repo_name, reg_project_name=reg_project_name)
        return self.send(method='delete', path=path, params={})

    def get_repo_detail(self, repo_name, reg_project_name=None):
        path = self.common_url(repo_name, reg_project_name=reg_project_name)
        return self.send(method='get', path=path, params={})

    def get_repo_tag(self, repo_name, reg_project_name=None):
        path = self.get_repo_tag_url(repo_name, reg_project_name=reg_project_name)
        return self.send(method='get', path=path, params={})

    def delete_repo_tag(self, repo_name, tag_name, reg_project_name=None):
        path = self.get_delete_repo_tag_url(repo_name, tag_name, reg_project_name=reg_project_name)
        return self.send(method='delete', path=path, params={})

    def get_repo_list(self, reg_project_name=None, params=None):
        path = self.get_repo_list_url(reg_project_name=reg_project_name)
        return self.send(method='get', path=path, params=params)

    def get_reg_project(self, params=None):
        path = self.get_reg_project_list_url()
        return self.send(method='get', path=path, params=params)

    def get_image_detail(self, repo_name, repo_tag, reg_project=None):
        path = self.get_image_url(repo_name, repo_tag, reg_project=reg_project)
        return self.send(method='get', path=path, params={})
