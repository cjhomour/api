# -*- coding: UTF-8 -*-
def casename():
    casename_dict = {
        "test_account": "创建子账号-获取子账号列表-获取子账号token(模拟登录)-更新token-更新子账号基本信息-获取子账号基本信息-更新"
                        "子账号密码-获取子账号token(模拟登录)-子账号加角色-获取子账号角色列表-删除子账号角色-验证已删除角色不在子账号"
                        "列表-删除子账号-获取子账号token(模拟登录)",
        "test_sub_account": "注册根账号-获取账号基本信息-更新账号密码-获取账号-token(模拟登录)-更新公司名称",
        "test_role": "获取权限列表-创建角色-验证角色列表-更新角色详情-获取角色详情-验证更新角色成功-添加父角色-"
                     "验证角色详情中父角色-删除父角色-验证角色详情页父角色删除成功-角色添加权限-验证角色详情页权限-"
                     "删除角色权限-验证角色详情页权限-添加角色成员-验证角色成员列表添加成员成功-删除角色成员-"
                     "验证角色成员列表删除成员成功-删除角色-验证角色列表删除角色成功",
        "test_role_template": "获取角色模版约束-创建模版-获取角色模版列表(验证公有模版及新创建模版)-更新模版-"
                              "获取模版详情验证更新结果-使用模版生成权限-验证生成权限内容-删除角色模版-验证角色模版列表",
        "test_system_role_template": "获取系统预置角色模版-验证系统预制角色模版权限与预置数据相同-使用系统预置角色模版创建角色-"
                                     "验证角色权限与模版相同-删除角色",
        "test_create_xvlan_region": "获取创建集群脚本-执行脚本-获取集群列表-添加主机节点-安装日志源-安装registry-获取主机列表-"
                                    "获取集群详情-更新主机标签-设置节点调度-设置节点不可调度-清理集群资源-删除集群",
        "test_newk8s_app": "应用测试:创建应用-验证应用状态-服务名称校验-获取应用详情-获取应用列表-获取应用yaml-操作事件-应用监控-日志-exec-"
                           "服务监控-访问组件地址-获取容器组列表-获取资源事件-获取组件实例数-重构实例-创建configmap-更新组件-验证组件更新-服务yaml-"
                           "获取文件日志源-停止组件-启动组件-获取版本-回滚到指定版本-回滚版本-停止应用-启动应用-删除服务-"
                           "更新应用-验证多容器-验证亲和反亲和-验证指定主机-删除应用",
        "test_dashboard": "创建监控面板-获取面板列表-更新面板-新建node-CPU监控图表-新建comp-ddagent图表-新建服务CPU图表-获取面板详情-删除图表-删除面板",
        "test_svn_build": "获取CI镜像-预览YAML-上传Dockerfile-预览Dockerfile-更新Dockerfile-删除Dockerfile-创建构建-"
                          "检查创建事件-获取构建配置列表-触发构建-构建日志-检查触发事件-检查版本-获取历史列表-删除构建历史-删除构建配置",
        "test_sync_public_registry": "创建同步配置-获取配置详情-更新配置-触发镜像同步-获取镜像同步状态-获取镜像同步日志-删除同步配置",

        "test_gfs_app": "应用使用gfs测试:创建gfs-创建应用-验证应用状态",
        "test_ebs_app": "应用使用ebs测试:创建ebs-创建应用-验证应用状态",
        "test_pvc_app": "应用使用pvc测试:创建存储卷-创建pv-创建pvc-创建应用-验证应用状态",
        "test_gfs_volume": "存储卷gfs测试:获取驱动类型-创建gfs-获取存储卷列表-获取gfs详情-删除gfs",
        "test_ebs_volume": "存储卷ebs测试:获取驱动类型-创建ebs-获取存储卷列表-获取ebs详情-删除ebs",
        "test_pv": "持久卷测试:创建pv-获取pv列表-更新pv-获取pv详情-删除pv",
        "test_ci_cd": "创建集成中心实例-获取实例状态-停用实例-获取实例状态-更新实例-获取实例状态-删除实例",
        "test_sonar_integration": "创建集成中心实例-获取实例状态-停用实例-获取实例状态-更新实例-获取实例状态-删除实例",
        # "test_clair_integration": "创建集成中心实例-获取实例状态-停用实例-获取实例状态-更新实例-获取实例状态-删除实例",
        "test_noti": "通知增删改查测试",
        "test_pvc": "持久卷声明测试:创建存储卷-创建pv-创建pvc-获取pvc列表-获取pvc详情-获取pv详情-删除pvc",
        "test_jenkins_buildimage_updateservice": "检查Jenkins是否能访问-判断集成中心实例是否创建成功-获取模板-创建svn凭证-创建镜像仓库凭证-获取镜像地址-"
                                                 "创建Jenkins流水线项目-获取流水线详情-更新流水线-执行流水线-获取流水线执行状态-检查应用的"
                                                 "镜像版本是否更新成功-删除Jenkins流水线",
        "test_jenkins_build_with_git": "检查Jenkins是否能访问-判断集成中心实例是否创建成功-获取模板-创建git凭证-创建流水线项目-"
                                       "执行流水线项目-取消执行流水线历史-再次执行流水线历史-删除流水线历史-删除流水线项目",
        "test_jenkins_build_with_svn_no_sonar": "检查Jenkins是否能访问-判断集成中心实例是否创建成功-获取模板-获取镜像版本-"
                                                "创建代码凭证-创建流水线项目-获取流水线项目列表-执行流水线项目-获取流水线运行历史列表-删除流水线项目",
        "test_jenkins_update_service": "检查Jenkins是否能访问-判断集成中心实例是否创建成功-获取模板-获取镜像仓库地址-获取镜像版本-"
                                       "创建流水线项目-执行流水线项目-获取流水线项目执行状态-获取应用详情-获取应用的镜像版本-"
                                       "获取应用的环境变量-删除流水线项目",
        "test_jenkins_build_with_svn_sonar": "检查Jenkins是否能访问-检查sonar是否能访问-判断集成中心实例是否创建成功-获取模板-"
                                             "创建svn代码仓库凭证-获取代码扫描阈值-获取开发语言-创建流水线项目-执行流水线项目-"
                                             "获取流水线项目的执行状态-删除流水线项目",
        "test_jenkins_sync_registry": "判断镜像仓库中是否有公有镜像仓库-检查Jenkins是否能访问-判断集成中心实例是否创建成功-"
                                      "创建镜像仓库凭证-获取模板-获取源仓库的信息-创建流水线项目-执行流水线项目-"
                                      "获取流水线项目的执行状态-验证镜像同步是否成功-删除流水线项目",
        "test_jenkins_template": "检查Jenkins是否能访问-获取模板列表-获取模板仓库列表-同步模板仓库-获取同步状态-获取模板仓库详情-验证同步结果",
        "test_pipeline": "创建流水线项目-获取流水线列表-获取流水线详情-更新流水线-获取流水线详情-获取应用详情-获取镜像版本-"
                         "启动流水线项目-获取流水线运行状态-获取流水线日志-验证应用是否更新成功-获取流水线历史列表-获取上传产出物-"
                         "获取下载产出物-删除流水线运行历史-删除流水线项目",
        "test_job": "任务测试:创建任务-获取创建任务事件-获取任务列表-获取任务配置详情-触发任务配置-查看任务历史-查看任务历史日志-定时任务"
                    "更新任务配置-更新任务事件-获取任务配置详情-触发任务-任务历史列表和日志-删除任务历史-删除任务配置-查看删除任务配置事件",
        "test_pvc_use_scs": "持久卷声明使用存储类测试:创建存储类-创建pvc-pvc列表-更新pvc-获取pvc详情-pvc删除",
        "test_pvc_use_defaultscs": "持久卷声明使用默认存储类测试:制造默认存储类-创建pvc-获取pvc详情-pvc删除",
        "test_scs": "存储类测试:创建sc-获取sc列表-设为默认-获取sc详情-删除sc",
        "test_configmap": "配置管理测试:创建cm-获取cm列表-更新cm-获取cm详情-删除cm",
        "test_metric_alarm": "指标警报测试:创建指标警报-获取警报详情-验证扩容-发送确认-更新指标警报-验证缩容-获取警报列表-删除警报",
        "test_log_alarm": "日志警报测试:创建日志警报-获取警报详情-更新日志警报-获取警报列表-删除警报",
        "test_log": "日志面板测试:获取日志源-获取查询类型-获取时间统计-日志查询-创建查询条件-获取条件详情-搜索查询条件-获取查询条件列表-删除查询条件",
        "test_namespace": "命名空间测试:创建命名空间-获取命名空间列表-获取命名空间详情-创建配额-获取配额列表-验证配额pvc-更新配额-验证配额pvc-获取配额详情-删除配额-删除命名空间",
        "test_resourcequota": "配额测试:创建命名空间-创建配额-验证配额pod-更新配额-验证配额pod-查看命名空间下的资源-删除有资源的命名空间-删除配额-删除应用-删除命名空间",
        "test_general_namespaces": "新命名空间测试:创建命名空间-获取resourcequota-获取limitrange-获取命名空间列表-验证配额pvc-更新命名空间-获取resourcequota-获取limitrange-验证配额pvc-删除命名空间",
        "test_newapp": "创建应用-获取拓扑图-获取容器组-获取yaml-获取日志-获取事件-获取k8s事件-exec-获取全部应用-获取命名空间下的应用-搜索应用-"
                       "更新应用-获取应用yaml-缩容-扩容-删除应用下的资源-获取应用详情-添加资源到应用-停止应用-启动应用-删除组件-删除应用",
        "test_app_with_cm": "应用使用configmap测试：创建configmap-创建应用-删除应用-删除configmap",
        "test_app_with_pvc": "应用使用pvc测试：创建sc-创建pvc-创建应用-获取pvc拓扑图-删除应用-删除pvc-删除sc",
        "test_tcp": "负载均衡测试：创建tcp端口-获取tcp端口详情-设置默认内部路由-获取应用访问地址-获取端口列表-删除tcp端口",
        "test_http": "负载均衡测试：创建http端口-创建规则-获取应用访问地址-获取规则详情-更新规则-获取规则列表-删除规则-删除http端口",
        "test_alb2": "负载均衡测试：创建负载均衡-负载均衡列表-更新域名后缀-获取负载均衡详情-删除负载均衡",
        "test_service": "内部路由测试:创建内部路由-内部路由列表-获取详情-更新内部路由-搜索内部路由-删除内部路由",
        "test_domain": "域名测试:创建域名-更新域名-域名列表-搜索域名-删除域名",
        "test_ingress": "外部路由测试:创建外部路由-外部路由列表-获取详情-更新外部路由-搜索外部路由-删除外部路由",
        "test_networkpolicy": "网络策略测试:创建网络策略-网络策略列表-更新网络策略-获取详情-删除网络策略",
        "test_macvlan_subnet": "macvlan子网测试:创建子网-更新子网-子网列表-子网详情-导入IPlist-删除IP-导入IPrange-IP列表-创建应用指定子网/IP-删除IP-删除子网",
        "test_calico_subnet": "calico子网测试:创建子网-子网列表-更新子网-子网详情-IP列表为空-创建应用指定子网-验证IP状态-创建应用指定IP-验证应用容器IP-IP列表-删除非空子网-更新非空子网-删除子网",
        "test_project": "创建项目-获取项目列表-更新项目-获取项目详情-删除项目",
        "test_space": "创建space-更新space-判断Jenkins是否能访问-创建集成中心实例-获取模板-创建代码仓库凭证-创建Jenkins流水线项目"
                      "-获取space资源详情-删除集成中心实例-删除Jenkins流水线-删除space",
        "test_sonarqube_plugin": "判断集群的网络模式-判断插件的类型-安装插件-获取已安装插件的状态-获取已安装插件的详情-删除应用-删除集成中心实例",
        "test_lb_dns": "创建(导入)lb-获取lb列表-删除新创建lb-添加自定义域名后缀-查看lb详情自定义域名-添加挂ha服务-获取服务域名(包括默认域名)-验证服务能够访问"
                       "-不使用默认域名-获取lb域名信息-验证ha地址不能访问-删除域名后缀-域名后缀地址不能访问"
                       "-不使用默认域名-获取lb域名信息-验证ha地址不能访问-删除域名后缀-域名后缀地址不能访问",
        "test_repository_git": "应用目录添加git模板仓库-获取模板仓库列表-获取git模板仓库详情信息-更新模板仓库-同步模板仓库",
        "test_repository_svn": "应用目录添加svn模板仓库-获取模板仓库列表-获取svn模板仓库详情信息-更新模板仓库-同步模板仓库-删除svn模板仓库",
        "test_catalog_mongodb": "应用目录获取git模板仓库id-获取模板仓库list-获取mongodb模板仓库id-获取模板仓库version id-创建mongodb应用-获取应用状态-删除应用",
        "test_mongodb": "中间件获取mongodb的模板id-获取mongodb可用的version id-创建mongodb应用-获取应用状态-删除应用",
        "test_mysql": "中间件获取mysql的模板id-获取mysql可用的version id-创建mongodb应用-获取应用状态-删除应用",
        "test_mysql_cluster": "中间件获取mysql-cluster的模板id-获取mysql-cluster可用的version id-创建mongodb应用-获取应用状态-删除应用",
        "test_rabbitmq_ha": "中间件获取rabbitmq的模板id-获取rabbitmq可用的version id-创建mongodb应用-获取应用状态-删除应用",
        "test_redis": "中间件获取redis的模板id-获取redis可用的version id-创建mongodb应用-获取应用状态-删除应用",
        "test_resource_list": "获取资源管理列表-校验列表资源类型",
        "test_manager_secret_basic_auth": "创建平台用户名／密码凭据-查看凭据列表-更新凭据-获取凭据详情-删除平台凭据",
        "test_manager_secret_oauth2": "创建平台OAuth2凭据-获取详情-删除平台凭据",
        "test_manager_secret_dockerconfigjson": "创建平台镜像服务凭据-获取详情-删除平台凭据",
        "test_user_secret_basic_auth": "创建用户用户名／密码凭据-查看凭据列表-更新凭据-获取凭据详情-删除平台凭据",
        "test_user_secret_oauth2": "创建用户OAuth2凭据-获取详情-删除平台凭据",
        "test_user_secret_dockerconfigjson": "创建用户镜像服务凭据-获取详情-删除平台凭据",
        "test_repo_project_params": "创建镜像项目-获取镜像项目-获取带项目空间镜像项目-删除镜像项目",
        "test_multiple_project": "循环开始-创建镜像项目-获取镜像项目-删除镜像项目-循环结束",
        "test_one_project_multiple_repo": "创建镜像项目-循环开始创建镜像仓库-删除镜像仓库-删除镜像项目",
        "test_shared_multiple_repo": "共享空间-循环开始创建镜像仓库-删除镜像仓库",
        "test_project_repo": "创建镜像项目-获取镜像项目-创建镜像仓库-获取镜像仓库-更新镜像仓库-获取镜像仓库详情-验证更新结果-"
                             "删除镜像仓库-删除镜像项目",
        "test_shared_repo": "共享空间-创建镜像项目-获取镜像项目-创建镜像仓库-获取镜像仓库-更新镜像仓库-获取镜像仓库详情-验证更新结果-"
                            "删除镜像仓库-删除镜像项目",
    }
    return casename_dict
