#%%
"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""

from SFTPClient._secrets import Secrets

import os
import setuptools

setuptools.setup(setup_requires=['pbr'], pbr=True)

os.environ["SFTP_PORT"] = Secrets.PORT
os.environ["SFTP_SERVER"] = Secrets.IP_ADDRESS
os.environ["PROJECT_PATH"] = Secrets.PROJECT_PATH
os.environ["SFTP_USERNAME"] = Secrets.SFTP_USERNAME
os.environ["SFTP_PASSWORD"] = Secrets.SFTP_PASSWORD

