from flask import render_template, url_for, redirect, request, flash, current_app
from flask_json import json_response
from sqlalchemy.exc import SQLAlchemyError

from app.admin import admin
from app.admin.forms.users import UsersForm
from app.models import User
from app import db
from app.utils.functions import row2dict
import requests
# from app.admin.forms.users import *


@admin.route('/user', methods=['GET'])
def listUsers():
    users = User.query.all()

    return json_response(data=(row2dict(x) for x in users))


@admin.route('/user', methods=['POST'])
def createUser():
    request_data = request.get_json()

    print(request_data)

    user = User(
        school_id=request_data['school_id'],
        username=request_data['username'],
        password=request_data['password'],
    )

    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        error = str(e.__dict__['orig'])
    except:
        db.session.rollback()
        error = 'An error occurred - no record created'

    return json_response(data=row2dict(user))




@admin.route('/user/add', methods=['GET','POST'])
def testCreateUser():
    form = UsersForm()
    if form.validate_on_submit():
        r = requests.post('http://127.0.0.1:5000/user', json=dict(
            school_id=form.school.data.id,
            username=form.username.data,
            password=form.password.data,
        ))

        return r

    return render_template('form_page.html',
                           form=form,
                           title="Add User")




# -- Working Json Code to ADD a new user --

# @admin.route('/users/add', methods=['POST'])
# def add_users():
#     newSchool_id = request.form['school_id']
#     newUsername = request.form['username']
#     newPassword = request.form['password']
#     users = User(school_id = newSchool_id, username=newUsername, password=newPassword)
#     db.session.add(users)
#     db.session.commit()
#     return "<p> New User Created</p>"

# @admin.route('/users/add', methods=['GET', 'POST'])
# def add_users():
#     form = UsersForm()
#     if form.validate_on_submit():
#         users = Users(name=form.name.data)
#         try:
#             db.session.add(users)
#             db.session.commit()
#         except:
#             db.session.rollback()
#
#         return redirect(url_for('admin.list_users'))
#
#     return render_template('admin/users.html',
#                            form=form,
#                            title="Add users")


# return render_template('admin/users.html',
#                        form=form,
#                        users=users,
#                        title='Edit subject users')
