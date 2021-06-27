# app/admin/forms.py
from datetime import date
# wtforms.fields.html5
from flask_wtf import FlaskForm, html5
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextField, FloatField, core, widgets, \
    PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Department, Role, Employee


# 管理员管理部分表单构建
class DepartmentForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired()], render_kw={'class': 'form-control'})
    base = StringField('所在城市', validators=[DataRequired()], render_kw={'class': 'form-control'})
    description = StringField('描述', validators=[DataRequired()], render_kw={'class': 'form-control'})
    # 部门人数之后根据数据库查询加上
    hc = IntegerField('转正名额', render_kw={'class': 'form-control'})
    submit = SubmitField('提交', render_kw={'class': 'form-control btn btn-lg btn-accent text-center'})


class RoleForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired()])
    description = StringField('描述', validators=[DataRequired()])
    submit = SubmitField('提交', render_kw={'class': 'form-control btn btn-lg btn-accent text-center'})


class EmployeeAssignForm(FlaskForm):
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name", render_kw={'class': 'form-control'})
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name", render_kw={'class': 'form-control'})
    wage = FloatField('薪资', default=Employee.wage, render_kw={'class': 'form-control'})
    submit = SubmitField('提交', render_kw={'class': 'form-control btn btn-lg btn-accent text-center'})


class ProfileForm(FlaskForm):
    username = StringField(label='昵称', default=Employee.username,
                           validators=[DataRequired(message='昵称不能为空'), Length(min=2, message='昵称长度必须大于%(min)d')])
    email = html5.EmailField(label='邮箱', default=Employee.email,
                             validators=[DataRequired(message='邮箱不能为空'), Email(message='邮箱格式有错')])
    full_name = StringField(label='姓名', default=Employee.full_name,
                            widget=widgets.TextInput(), validators=[DataRequired(message='姓名不能为空')])
    gender = core.RadioField(label='性别',
                             validators=[DataRequired("请选择性别")], choices=[(1, '男'), (0, '女')],
                             default=Employee.gender, coerce=int, validate_choice=Employee.gender,
                             render_kw={'class': 'custom-control custom-radio mb-1 radio-inline'})
    birthday = html5.DateField(label='出生日期',
                               default=Employee.birthday)
    # age = IntegerField(label='年龄', validators=[NumberRange(min=18, max=65, message='年龄需为18~65岁')]),
    entry_date = html5.DateField(label='入职日期',
                                 default=Employee.entry_date)
    location = StringField(label='所在城市',
                           default=Employee.location)
    highest_education = SelectField(label='最高学历',
                                    choices=[(1, '本科'),
                                             (2, '硕士'),
                                             (3, '博士'),
                                             (4, '博士后'),
                                             (0, '大专职校')],
                                    default=Employee.highest_education,
                                    coerce=int,
                                    validate_choice=Employee.highest_education)
    university = StringField(label='学校',
                             default=Employee.university)
    password = PasswordField('密码', default=Employee.password,
                             validators=[DataRequired(message='密码不能为空'),
                                         # Length(min=5, message='密码长度必须大于%(min)d'),
                                         EqualTo('confirm_password', message='两次密码必须一致')])
    confirm_password = PasswordField('确认密码', default=Employee.password)
    cv = StringField(label='个人简介', default=Employee.cv)
    wage = Employee.wage
    role = Employee.role_id
    submit = SubmitField('OK', render_kw={'class': 'form-control btn btn-lg btn-accent text-center'})


class SearchForm(FlaskForm):
    search = StringField('搜索', validators=[DataRequired()])
