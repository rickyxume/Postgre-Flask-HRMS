from app import db
from app.models import Department, Employee, Role

# 添加数据
# employee = Employee(username,password,full_name,email,gender
#                     university,location,highest_education,
#                     birthday,wage,role_id,department_id)


db.session.add(employee)
db.session.commit()