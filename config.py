import os

class Config(object):
    """
    Generic configuration file.
    @author Niranjan Balasubramani
    @email  nibalasu@akamai.com
    @date   2018-06-19
    """
    APP_NAME = 'BLOCKCHAIN-PYTHON'
    APP_VERSION = '0.1'
    APP_HOST = os.environ.get('CONFIG_SYNC_HOST','0.0.0.0')
    APP_PORT = int(os.environ.get('CONFIG_SYNC_PORT',5030))
    APP_DEBUG = True
