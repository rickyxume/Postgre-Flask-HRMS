# config.py
class Config(object):
    # 将所有环境中通用的任何配置放在此处
    DEBUG = True


# echo: True的时候，会打印所有的状态变化，包括转换的SQL语句。
# 一般在生产环境中，我们是把它设置为Flase的。
class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
