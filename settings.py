import os


def get_list_from_str(string, separator=','):
    if string is not None and string != '':
        return string.split(separator)


# necessary
API_URL = os.getenv("API_URL", "https://cloud-staging-api.alauda.cn")
ACCOUNT = os.getenv("ACCOUNT", "alauda")
SUB_ACCOUNT = os.getenv("SUB_ACCOUNT", "")
PASSWORD = os.getenv("PASSWORD", "Alauda2018!@#")
REGION_NAME = os.getenv("REGION_NAME", "high-region-available")
REGISTRY_NAME = os.getenv("REGISTRY_NAME", "high-registry")
IMAGE = os.getenv("IMAGE", "index.alauda.cn/alaudaorg/qaimages:helloworld")
# not necessary
REGISTRY_CREDENTIAL = os.getenv("REGISTRY_CREDENTIAL", "alauda-registry-credential")

JENKINS_ENDPOINT = os.getenv("JENKINS_ENDPOINT",
                             "http://192.144.148.212:8899")
JENKINS_USER = os.getenv("JENKINS_USER", "admin")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN", "ebc372b57c4ac531f74949a4d71f5325")

SONAR_ENDPOINT = os.getenv("SONAR_ENDPOINT",
                           "http://192.144.148.212:10007")
SONAR_TOKEN = os.getenv("SONAR_TOKEN", "94df71bcca7d1e03cecee2222e4afa6047618533")

SVN_REPO = os.getenv("SVN_REPO", "http://192.144.148.212:10009/alauda_test/")
SVN_CREDENTIAL = os.getenv("SVN_CREDENTIAL", "alauda-svn-credential")
SVN_USERNAME = os.getenv("SVN_USERNAME", "User_Name-01")
SVN_PASSWORD = os.getenv("SVN_PASSWORD", "alauda_Test-!@#")

GIT_REPO = os.getenv("GIT_REPO",
                     "http://192.144.148.212:10008/root/test123")
GIT_CREDENTIAL = os.getenv("GIT_CREDENTIAL", "alauda-git-credential")
GIT_USERNAME = os.getenv("GIT_USERNAME", "root")
GIT_PASSWORD = os.getenv("GIT_PASSWORD", "07Apples")

# 应用目录添加git类型用的git参数
GIT_URL = os.getenv("GIT_URL", "https://bitbucket.org/mathildetech/devops-charts.git")
GIT_PATH = os.getenv("GIT_PATH", "/")
GIT_BRANCH = os.getenv("GIT_BRANCH", "master")
GIT_USER = os.getenv("GIT_USER", "rzli@alauda.io")
GIT_PWD = os.getenv("GIT_PWD", "Luhan0420.")

TESTCASES = os.getenv("TESTCASES", "")
CASE_TYPE = os.getenv("CASE_TYPE", "BAT")
PROJECT_NAME = os.getenv("PROJECT_NAME", "e2etest3")
ENV = os.getenv("ENV", "Staging")

RECIPIENTS = get_list_from_str(os.getenv("RECIPIENTS", "testing@alauda.io"))
K8S_NAMESPACE = os.getenv("K8S_NAMESPACE", "{}-{}".format(PROJECT_NAME, REGION_NAME).replace("_", "-"))
SPACE_NAME = os.getenv("SPACE_NAME", "alauda-default-{}".format(REGION_NAME).replace("_", "-"))

SECRET_ID = os.getenv("SECRET_ID", "AKID84kBMHwKUP4VggjwBAKFvxlJcgU3frtg")
SECRET_KEY = os.getenv("SECRET_EKY", "aDlNSjBSZGRPdkxXUjZWZ2JHZnFPaGpXMklJa3d0WjA=")

OAUTH2_CLIENTID = os.getenv("OAUTH2_CLIENTID", "test")
OAUTH2_CLIENTSECRET = os.getenv("OAUTH2_CLIENTSECRET", "test")
DOCKER_AUTH = os.getenv("DOCKER_AUTH", "harbor.com")
DOCKER_USERNAME = os.getenv("DOCKER_USERNAME", "admin")
DOCKER_PASSWORD = os.getenv("DOCKER_PASSWORD", "passsword")
DOCKER_EMAIL = os.getenv("DOCKER_EMAIL", "a@b.com")

VM_IPS = os.getenv("VM_IPS", "").split(";")
VM_USERNAME = os.getenv("VM_USERNAME", "root")
VM_PASSWORD = os.getenv("VM_PASSWORD", "07Apples")
VM_PEM = "./key.pem"

# 中间件的镜像仓库地址
MIDDLEWARE_REGISTRY = os.getenv("MIDDLEWARE_REGISTRY", "10.0.128.201:60080")

SMTP = {
    'host': os.getenv('SMTP_HOST', 'smtpdm.aliyun.com'),
    'port': os.getenv('SMTP_PORT', 465),
    'username': os.getenv('SMTP_USERNAME', 'staging@alauda.cn'),
    'password': os.getenv('SMTP_PASSWORD', 'Ahvooy5ie22H0tel'),
    'sender': os.getenv('EMAIL_FROM', 'staging@alauda.cn'),
    'debug_level': 0,
    'smtp_ssl': True
}

LOG_LEVEL = "INFO"
LOG_PATH = "./report"
REPO_NAME = "hello-world"
REPO_PROJECT = "e2etest"
TARGET_REPO_NAME = "sys-repo"
GLOBAL_INFO_FILE = "./temp_data/global_info.json"
