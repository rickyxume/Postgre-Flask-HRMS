# app/models.py
import datetime
import enum

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


"""
autoincrement ： True . 表示这个字段是自增的。
index : True. 设置这个字段为索引。
nullable ： True. 允许次字段为空。
primary_key ： True. 设置此字段为主键。非常值得注意的是！！！！ SQLAlchemy中， 每个类中至少有一个主键！！！
unique : True. 设置此字段唯一。此字段相同的数据，第一条数据插入后， 之后的就不允许再插入了， 直接 pass 掉。
"""


# def get_age_from(birthday):
#     today = datetime.date.today()
#     return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


class Employee(UserMixin, db.Model):
    """
    建表Employee
    """

    # 确保表将以复数而不是单数命名
    # 和模型名一样
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, doc='id主键自增')
    email = db.Column(db.String(20), index=True, unique=True, doc='唯一邮箱')
    username = db.Column(db.String(20), index=True, unique=True, doc='唯一用户名昵称')
    full_name = db.Column(db.String(20), index=True, doc='姓名')
    gender = db.Column(db.Integer, doc='性别1男0女')
    birthday = db.Column(db.Date(), index=True, doc='生日')
    # age = db.Column(db.Integer, default=get_age_from(birthday), doc='年龄')
    #  SELECT  TIMESTAMPDIFF(YEAR, @birthday, CURDATE()) --计算age(timestamp)
    age = db.Column(db.Integer, index=True, doc='年龄')
    entry_date = db.Column(db.Date(), index=True, doc='入职日期')
    location = db.Column(db.String(10), index=True, doc='所处城市')
    highest_education = db.Column(db.Integer, index=True, doc='最高学历')
    university = db.Column(db.String(20), index=True, doc='读过的大学')
    cv = db.Column(db.String(300), doc='个人介绍')
    password_hash = db.Column(db.String(128), doc='密码哈希值')
    wage = db.Column(db.Float, default=0, doc='薪资')
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), doc='部门id外键')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), doc='职位id外键')
    is_admin = db.Column(db.Boolean, default=False, doc='是否是管理员，默认不是')

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Department(db.Model):
    """
    建表Department
    """
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, doc='id主键')
    name = db.Column(db.String(60), unique=True, doc='部门名称')
    description = db.Column(db.String(200), doc='部门描述')
    base_city = db.Column(db.String(10), doc='部门所在城市')
    head_count = db.Column(db.Integer, doc='部门转正名额')
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic', doc='部门员工')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Role(db.Model):
    """
    建表Role
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, doc='id主键')
    name = db.Column(db.String(60), unique=True, doc='职位名称')
    description = db.Column(db.String(200), doc='职位描述')
    average_wage = db.Column(db.Integer,doc='平均薪资')
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic', doc='员工')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
