import pkg_resources

installed_packages = pkg_resources.working_set

# 生成安装包的语句
install_commands = []
for package in installed_packages:
    package_name = package.key
    package_version = package.version
    install_command = f"pip install {package_name}=={package_version}"
    install_commands.append(install_command)

# 打印所有生成的安装包语句
for command in install_commands:
    print(command)
    
"""
pip install urllib3==1.26.16
pip install timedelta==2020.12.3
pip install pytz==2023.3
pip install python-etcd==0.4.5
pip install pip==21.3.1
pip install elasticsearch==7.17.0
pip install dnspython==2.2.1
pip install certifi==2023.5.7
pip install setuptools==39.2.0
"""