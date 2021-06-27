# run.py

import os

from app import create_app

# 设置环境变量
config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


if __name__ == '__main__':
    app.run()