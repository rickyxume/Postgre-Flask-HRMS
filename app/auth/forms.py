# app/auth/forms.py
import datetime

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, RadioField, widgets, IntegerField, \
    SelectField
from wtforms.fields import html5, core
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from datetime import date

from ..models import Employee


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    username = StringField(label='昵称',
                           validators=[DataRequired(message='昵称不能为空'), Length(min=2, message='昵称长度必须大于%(min)d')])
    email = html5.EmailField(label='邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='邮箱格式有错')])
    full_name = StringField(label='姓名', widget=widgets.TextInput(), validators=[DataRequired(message='姓名不能为空')])
    gender = core.RadioField(label='性别', validators=[DataRequired("请选择性别")], choices=[(1, '男'), (0, '女')],
                             default=1, coerce=int, validate_choice=1,
                             render_kw={'class': 'custom-control custom-radio mb-1 radio-inline'})
    birthday = html5.DateField(label='出生日期', default=date.today)
    # age = IntegerField(label='年龄', validators=[NumberRange(min=18, max=65, message='年龄需为18~65岁')]),
    entry_date = html5.DateField(label='入职日期', default=date.today)
    location = StringField(label='所在城市')
    highest_education = SelectField(label='最高学历',
                                    choices=[(1, '本科'),
                                             (2, '硕士'),
                                             (3, '博士'),
                                             (4, '博士后'),
                                             (0, '大专职校')],
                                    default=1, coerce=int, validate_choice=1)
    university = StringField(label='学校')
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'),
                                               # Length(min=5, message='密码长度必须大于%(min)d'),
                                               EqualTo('confirm_password', message='两次密码必须一致')])
    confirm_password = PasswordField('确认密码')
    cv = StringField(label='个人简介', default='没有简介')
    submit = SubmitField('注册')

    # @property
    # def age(self):
    #     return ((datetime.datetime.now() - self.birthday).days) / 365

    # def validate_on_submit(self):
    #     result = super(RegistrationForm, self).validate()
    #     today = date.today
    #     if self.birthday.data > today:
    #         raise ValidationError('生日输入有误')
    #     else:
    #         return result

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被使用')

    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用')


"""
    示例代码
     validators=[
            validators.DataRequired(message='密码不能为空.'),
            validators.Length(min=8, message='用户名长度必须大于%(min)d'),
            validators.Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}",
                              message='密码至少8个字符，至少1个大写字母，1个小写字母，1个数字和1个特殊字符')
        ],
    """


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    # username = StringField('昵称', validators=[DataRequired(message='昵称不能为空'), Length(min=2, message='昵称长度必须大于%(min)d')])
    email = html5.EmailField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='邮箱格式有错')])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    submit = SubmitField('登录')
