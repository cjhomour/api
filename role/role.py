from common.base_request import Common


class Role(Common):

    """
    api:
    1、list role
    2、create role
    """
    def create_role_url(self):
        return "v1/roles/{}".format(self.account)

    def list_role_url(self):
        return "v1/roles/{}?search=&page=1&page_size=1000&order_by=created_at&action=view&project_name=".format(
            self.account
        )

    """
    api:
    1、get the detail of role
    2、update the detail of role
    3、delete role
    """
    def role_detail_url(self, role_name):
        return "v1/roles/{0}/{1}".format(self.account, role_name)

    """
    api:
    1、add a new parent
    """
    def add_parent_to_role_url(self, role_name):
        return "v1/roles/{0}/{1}/parents".format(self.account, role_name)

    """
    api:
    1、remove one parent instance
    """
    def remove_parent_from_role_url(self, role_name, parent_uuid):
        return "v1/roles/{0}/{1}/parents/{2}".format(self.account, role_name, parent_uuid)

    """
    api:
    1、add a permission to a role
    """
    def add_permission_to_role_url(self, role_name):
        return "v1/roles/{0}/{1}/permissions".format(self.account, role_name)

    """
    api:
    1、update a permission in a role
    2、remove a permission from a role
    """
    def operate_permission_from_role_url(self, role_name, permission_uuid):
        return "v1/roles/{0}/{1}/permissions/{2}".format(self.account, role_name, permission_uuid)

    """
    api:
    1、list users that belong to a role
    2、assign role to one or more users
    3、revoke a role from one or more users
    """
    def operate_user_from_role_url(self, role_name):
        return "v1/roles/{0}/{1}/users?page=1&page_size=100&search=".format(self.account, role_name)
    """
    api:
    1、 get permission schema
    """
    def get_permission_schema_url(self):
        return "v1/role-schema"

    @Common.log_info
    def create_role(self, file=None, data=None, body=None):
        url = self.create_role_url()
        if body is not None:
            data = body
        else:
            data = self.generate_data(file, data)
        return self.send(method='POST', path=url, data=data, params='')

    @Common.log_info
    def get_role_list(self):
        url = self.list_role_url()
        return self.send(method='GET', path=url, params='')

    @Common.log_info
    def get_role_detail(self, role_name):
        url = self.role_detail_url(role_name)
        return self.send(method='GET', path=url)

    @Common.log_info
    def update_role_detail(self, file, data, role_name=None):
        url = self.role_detail_url(role_name)
        data = self.generate_data(file, data)
        return self.send(method='PUT', path=url, data=data, params='')

    @Common.log_info
    def delete_role(self, role_name):
        url = self.role_detail_url(role_name)
        return self.send(method='DELETE', path=url)

    @Common.log_info
    def add_parent_to_role(self, file, data, role_name=None):
        url = self.add_parent_to_role_url(role_name)
        data = self.generate_data(file, data)
        return self.send(method='POST', path=url, data=data, params='')

    @Common.log_info
    def remove_parent_from_role(self, role_name, parent_uuid):
        url = self.remove_parent_from_role_url(role_name, parent_uuid)
        return self.send(method='DELETE', path=url, params='')

    @Common.log_info
    def add_permission_to_role(self, file, data, role_name):
        url = self.add_permission_to_role_url(role_name)
        data = self.generate_data(file, data)
        return self.send(method='POST', path=url, data=data, params='')

    @Common.log_info
    def update_permission_from_role(self, file, data, role_name, permission_uuid):
        url = self.operate_permission_from_role_url(role_name, permission_uuid)
        data = self.generate_data(file, data)
        return self.send(method='PUT', path=url, data=data, params='')

    @Common.log_info
    def remove_permission_from_role(self, role_name, permission_uuid):
        url = self.operate_permission_from_role_url(role_name, permission_uuid)
        return self.send(method='DELETE', path=url, params='')

    @Common.log_info
    def get_role_user_list(self, role_name):
        url = self.operate_user_from_role_url(role_name)
        return self.send(method='GET', path=url, params='')

    @Common.log_info
    def assign_role_to_user(self, file, data, role_name):
        url = self.operate_user_from_role_url(role_name)
        data = self.generate_data(file, data)
        return self.send(method='POST', path=url, data=data, params='')

    @Common.log_info
    def revoke_role_to_user(self, file, data, role_name):
        url = self.operate_user_from_role_url(role_name)
        data = self.generate_data(file, data)
        return self.send(method='DELETE', path=url, data=data, params='')

    @Common.log_info
    def get_permission_schema(self):
        url = self.get_permission_schema_url()
        return self.send(method='GET', path=url)

    def get_role_templates_scopes_url(self):
        return "v1/role-templates-scopes"

    def get_role_template_list_url(self, role_template_name=None):
        if role_template_name:
            return "v1/role-templates/{}?search={}".format(self.account, role_template_name)
        else:
            return "v1/role-templates/{}".format(self.account)

    def create_role_template_url(self):
        return "v1/role-templates/{}".format(self.account)

    def operate_role_template_detail_url(self, role_template_uuid):
        return "v1/role-templates/{}/{}".format(self.account, role_template_uuid)

    def generate_permission_by_role_template_url(self, role_template_uuid):
        return "v1/role-templates/{}/{}/generate".format(self.account, role_template_uuid)

    @Common.log_info
    def get_role_templates_scopes(self):
        url = self.get_role_templates_scopes_url()
        return self.send(method='GET', path=url, params='')

    @Common.log_info
    def get_role_template_list(self, role_template_name=None):
        url = self.get_role_template_list_url(role_template_name)
        return self.send(method='GET', path=url, params='')

    @Common.log_info
    def create_role_template(self, file, data):
        data = self.generate_data(file, data)
        url = self.create_role_template_url()
        return self.send(method='POST', path=url, data=data, params='')

    @Common.log_info
    def get_role_template_detail(self, role_template_uuid):
        url = self.operate_role_template_detail_url(role_template_uuid)
        return self.send(method='GET', path=url, params='')

    @Common.log_info
    def update_role_template(self, file, data, role_template_uuid):
        data = self.generate_data(file, data)
        url = self.operate_role_template_detail_url(role_template_uuid)
        return self.send(method='PUT', path=url, data=data, params='')

    @Common.log_info
    def delete_role_template(self, role_template_uuid):
        url = self.operate_role_template_detail_url(role_template_uuid)
        return self.send(method='DELETE', path=url, params='')

    @Common.log_info
    def generate_permission_by_role_template(self, file=None, data=None, role_template_uuid=None, params=''):
        url = self.generate_permission_by_role_template_url(role_template_uuid)
        if file is None:
            data = {}
        else:
            data = self.generate_data(file, data)
        return self.send(method='POST', path=url, data=data, params=params)
