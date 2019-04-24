import sys

from common.base_request import Common
from common.log import logger


class Subnet(Common):
    def get_subnet_crd_url(self):
        return "v2/kubernetes/clusters/{}/customresourcedefinitions?name=subnet".format(self.region_name)

    def get_subnet_url(self):
        return 'v2/subnet/clusters/{}'.format(self.region_id)

    def get_common_subnet_url(self, name):
        return 'v2/subnet/clusters/{}/{}'.format(self.region_id, name)

    def get_private_ip_url(self, name):
        return 'v2/subnet/clusters/{}/{}/private_ips'.format(self.region_id, name)

    def get_private_ip_common_url(self, name, ip):
        return 'v2/subnet/clusters/{}/{}/private_ips/{}'.format(self.region_id, name, ip)

    def get_calico_subnet_url(self):
        return 'v2/kubernetes/clusters/{}/resources'.format(self.region_name)

    def get_subnet_crd(self):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_subnet_crd_url()
        return self.send(method='get', path=url, params={})

    def list_subnet(self):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_subnet_url()
        return self.send(method='get', path=url, params={})

    def create_subnet(self, file, data):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_subnet_url()
        data = self.generate_data(file, data)
        return self.send(method='post', path=url, data=data, params={})

    def create_subnet_calico(self, file, data):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_calico_subnet_url()
        data = self.generate_data(file, data)
        return self.send(method='post', path=url, data=data, params={})

    def update_subnet(self, subnet_name, file, data):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_common_subnet_url(subnet_name)
        data = self.generate_data(file, data)
        return self.send(method='put', path=url, data=data, params={})

    def delete_subnet(self, subnet_name):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_common_subnet_url(subnet_name)
        return self.send(method='delete', path=url, params={})

    def get_subnet_detail(self, subnet_name):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_common_subnet_url(subnet_name)
        return self.send(method='get', path=url, params={})

    def list_ips(self, subnet_name):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_private_ip_url(subnet_name)
        return self.send(method='get', path=url, params={})

    def create_ips(self, subnet_name, file, data):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_private_ip_url(subnet_name)
        data = self.generate_data(file, data)
        return self.send(method='post', path=url, data=data, params={})

    def delete_ips(self, subnet_name, ip):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_private_ip_common_url(subnet_name, ip)
        return self.send(method='delete', path=url, params={})
