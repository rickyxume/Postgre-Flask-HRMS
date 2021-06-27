# app/auth/views.py

from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user

from app.auth import auth
from app import db
from app.models import Employee
from app.auth.forms import LoginForm, RegistrationForm


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        employee = Employee(
            email=form.email.data,
            username=form.username.data,
            full_name=form.full_name.data,
            gender=form.gender.data,
            birthday=form.birthday.data,
            entry_date=form.entry_date.data,
            location=form.location.data,
            highest_education=form.highest_education.data,
            university=form.university.data,
            password=form.password.data,
            cv=form.cv.data)

        db.session.add(employee)
        db.session.commit()
        flash('恭喜你注册成功！现在可以登录啦！', 'success')

        # redirect to the login page
        return redirect(url_for('auth.login'))
    # else:
    #     error = ""

    # load registration template

    form.process()
    return render_template('auth/register.html', form=form, title='注册')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        # 检查员工是否在数据库
        # 以及密码是否匹配
        employee = Employee.query.filter_by(email=loginform.email.data).first()
        if employee is not None and employee.verify_password(
                loginform.password.data):
            # 用户登录
            login_user(employee)
            # 重定向到对应的页面
            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
        else:
            flash('邮箱或密码不正确', 'warning')

    # 加载登录模板
    return render_template('auth/login.html', form=loginform, title='登录')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经成功登出！', 'success')

    # redirect to the login page
    return redirect(url_for('auth.login'))
