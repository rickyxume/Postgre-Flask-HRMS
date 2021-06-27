# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import case, func
from sqlalchemy.orm import session

from app.admin import admin
from app import db
from app.admin.forms import DepartmentForm, EmployeeAssignForm, RoleForm, SearchForm, ProfileForm
from app.models import Department, Employee, Role


def check_admin():
    """
    防止非管理员访问页面
    """
    if not current_user.is_admin:
        abort(403)


# Department Views


@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    列出所有部门
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="管理部门")


@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data,
                                base_city=form.base.data,
                                head_count=form.hc.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash(message='你成功添加了一个新部门', category='success')
        except:
            # in case department name already exists
            # db.session.rollback()
            flash(message='该部门已存在！', category='warning')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="增设部门")


@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        department.base_city = form.base.data
        department.head_count = form.hc.data
        db.session.commit()
        flash(message='你成功编辑了一个部门！', category='success')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="编辑部门")


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash(message='你成功删除了一个部门！', category='warning')

    return redirect(url_for('admin.list_departments'))

    # return render_template(url_for('admin.list_departments'), title="删除部门")


# Role Views


@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    roles = Role.query.all()
    # role = Role.query.get_or_404(id)
    # average_wage = role.query(func.avg(Employee.wage)).join(Role).filter(role.id == Employee.role_id).group_by(Employee.role_id).all()
    # db.session.add(average_wage)
    # db.session.commit()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='管理职位')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data
                    )

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash(message='你成功添加了一个职位！', category='success')
        except:
            # in case role name already exists
            flash(message='该职位已存在！', category='warning')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='新增职位')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data

        db.session.add(role)
        db.session.commit()
        flash(message='你成功编辑了一个职位！', category='success')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="编辑职位")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash(message='你成功删除了一个职位！', category='warning')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    # return render_template(title="Delete Role")


# Employee Views

@admin.route('/employees')
@login_required
def list_employees():
    """
    正序列出所有员工
    """
    check_admin()
    # (Employee.id,Employee.full_name,Employee.username,Employee.email,Employee.role,Employee.department,Employee.wage,Employee.entry_date,Employee.highest_education,Employee.university)
    employees = Employee.query.all()

    return render_template('admin/employees/employees.html',
                           employees=employees, title='管理员工')

@admin.route('/employees')
@login_required
def list_employees_by_wage():
    check_admin()
    # (Employee.id,Employee.full_name,Employee.username,Employee.email,Employee.role,Employee.department,Employee.wage,Employee.entry_date,Employee.highest_education,Employee.university)
    employees = Employee.query.all()

    return render_template('admin/employees/employees.html',
                           employees=employees, title='管理员工')


@admin.route('/employees/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def employee_profile(id):
    """用户信息编辑
    """
    add_profile = False
    # role = Role.query.get_or_404(id)
    employee = Employee.query.get_or_404(id)
    form = ProfileForm(obj=employee)
    if form.validate_on_submit():
        employee.name = form.name.data
        employee.description = form.description.data

        db.session.add(employee)
        db.session.commit()
        flash(message='成功更新个人信息！', category='success')

        # redirect to the roles page
        return redirect(url_for('admin.employee_profile'))

    # form.description.data = role.description
    # form.name.data = role.name
    return render_template('admin/employees/employee-profile.html', profile=employee_profile,
                           form=form, title="员工简历")


@admin.route('/employees/')
@login_required
def list_sort_by_employee_id():
    check_admin()
    # 根据id倒序序排
    employees_id = Employee.query.order_by(Employee.id.desc()).all()
    return render_template('admin/employees/employees.html',
                           employees=employees_id, title='员工按编号排序')

@admin.route('/employees/')
@login_required
def list_sort_by_employee_wage():
    check_admin()
    employees_wage = Employee.query.order_by(Employee.wage.desc()).all()
    return render_template('admin/employees/employees.html',
                           employees=employees_wage, title='员工按薪资排序')


@admin.route('/employees/')
@login_required
def list_sort_by_employee_entry_date():
    check_admin()
    employees_entry_date = Employee.query.order_by(Employee.entry_date.desc()).all()
    return render_template('admin/employees/employees.html',
                           employees=employees_entry_date, title='员工按入职日期排序')


@admin.route('/employees/', methods=['POST', 'GET'])
@login_required
def search_employees():
    check_admin()
    # try:

    name = request.form.get('full_name')  # 要查询的内容，这里是姓名
    employees_name = Employee.query.filter(Employee.full_name == name).all()  # 查询跟name有关的数据，返回结果为列表

    # employees = db.session.query(Employee).fitter(Employee.full_name.CONTAINS(content)).all()
    print("*************测试打印搜索返回的\n***************", name, employees_name)
    return render_template('admin/employees/employees.html',
                           employees=employees_name,
                           name=name,
                           title='搜索员工')

# emps = session.query(EmpMaster).filter(
#     EmpMaster.EMAIL.contains('west')
# ).all()
# print_emps(emps)



@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    check_admin()

    employee = Employee.query.get_or_404(id)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        employee.wage = form.wage.data
        db.session.add(employee)
        db.session.commit()
        flash(message='你成功分配了一个员工！', category='success')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='分配员工')


@admin.route('/employees/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    check_admin()

    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash(message='你成功删除了一名员工！', category='warning')

    return redirect(url_for('admin.list_employees'))

    # return render_template(title="Delete Employee")

