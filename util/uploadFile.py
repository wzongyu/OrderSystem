import os
import os.path
import paramiko
import datetime
import re

def uploadAndGetUrl(imgName):
    
    # 配置属性
    config = {
        # 本地项目路径
        'local_path': '****'+imgName,
        # 服务器项目路径
        'ssh_path': '****'+imgName,
        # 项目名
        'project_name': '',
        # 忽视列表
        'ignore_list': [],
        # ssh地址、端口、用户名、密码
        'hostname': '139.196.191.74',
        'port': 22,
        'username': '****',
        'password': '****',
        # 是否强制更新
        'mandatory_update': False,
        # 更新完成后是否重启tomcat
        'restart_tomcat': False,
        # tomcat bin地址
        'tomcat_path': '',
        # 被忽略的文件类型
        'ignore_file_type_list': []
    }

    # ssh控制台
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=config['hostname'], port=config['port'],
                username=config['username'], password=config['password'])
    # ssh传输
    transport = paramiko.Transport((config['hostname'], config['port']))
    transport.connect(username=config['username'], password=config['password'])
    sftp = paramiko.SFTPClient.from_transport(transport)

    # sftp.putfo(fl, config['ssh_path'], len(fl), None, True)
    sftp.put(config['local_path'], config['ssh_path'])

    # 关闭连接
    sftp.close()
    ssh.close()

    return "http://139.196.191.74:8080/img/"+imgName
