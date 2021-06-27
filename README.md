# Postgre-Flask-HRMS
一个基于 PostgreSQL 和 Flask 框架的人力资源管理系统 Demo

## 数据库迁移

````shell
flask db init
flask db migrate
flask db upgrade
flask shell
from app.models import Employee
from app import db
admin = Employee(email="admin@admin.com",username="Admin",password="adminpassword",is_admin=True)
db.session.add(admin)
db.session.commit()
````

## 环境变量设置

在运行应用程序之前，请确保设置了FLASK_CONFIG和FLASK_APP环境变量:

```shell
set FLASK_CONFIG=development
set FLASK_APP=run.py
flask run
```

> * Serving Flask app "run"
> * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)