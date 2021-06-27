# app/home/views.py

from flask import abort, render_template
from flask_login import current_user, login_required
from app.home import home
from app import db
from app.models import Employee

# 蓝图主页
@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


# 蓝图看板
@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")


# class wage_statistic:
# 	def GET(self):
# 		role_check(session.role,['TE'])
# 		command="SELECT * FROM STUMAN.SCORE_STATISTIC_OUTER_VIEW;"
# 		data=db.query(command).list()
# 		return render.te_score_statistic(session.username,session.no,data)


# 管理员看板,查数据
@home.route('/admin/dashboard', methods=['GET', ])
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")