#!env/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, flash, redirect, url_for
from models import User
from forms import LoginForm, RegisterForm, ChangePassForm, EditUserForm
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.admin import expose
from flask.ext.admin.contrib.sqla import ModelView
from sqlalchemy.exc import IntegrityError

users = Blueprint("users", __name__, url_prefix="/users", template_folder="templates")

# callback
@login_manager.user_loader
def user_load(userid):
    return User.query.get(userid)

@users.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if (user != None) and (check_password_hash(user.password, form.password.data)):
            login_user(user)
            next = request.args.get("next", url_for("index"))
            return redirect(next)
        else:
            flash(u"The user name or the password are incorrect")
    return render_template("login.html", form=form)

@users.route("/register", methods=["POST", "GET"])
#@login_required
def register():
    form = RegisterForm(csrf_enabled=False)
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count() > 0:
            flash(u"This user name is already taken")
        else:
            user = User(
                username=form.username.data,
                password=generate_password_hash(form.password.data)
                )

            db.session.add(user)
            db.session.commit()

            flash(u"Registration successful")

    return render_template("register.html", form=form)

@users.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))



class UserView(ModelView):

    # View to change the password
    @expose("/pass/<int:user_id>", methods=["POST", "GET"])
    def change_pass(self, user_id):
        form = ChangePassForm(csrf_enabled=False)
        if form.validate_on_submit():
            user = User.query.get(user_id)
            user.password = generate_password_hash(form.passw.data)
            db.session.add(user)
            try:
                db.session.commit()
                flash(u"The password has been changed successfully")
            except Exception:
                flash("Unexpected error")
        return self.render("admin_local/model/change_pass.html", form=form)

    column_list = ("username",)

    edit_template = "admin_local/model/edit_user.html"

    def __init__(self, session, name):
        super(UserView, self).__init__(User, session, name)

    # Get the user id
    def get_primary_key(self, model):
        return model.id

    # Actions to register the user
    def create_model(self, form):
        if form.validate_on_submit:

            user = User(
                username=form.username.data,
                password=generate_password_hash(form.password.data),
                #email=form.email_field.data,
                )

            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash("El nombre del user ya existe")

    def update_model(self, form, model):
        model.username = form.username_field.data
        model.email = form.email_field.data
        db.session.add(model)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("This user name is already taken")
        else:
            flash("The changes has been saved successfully")

    # Create form
    def create_form(self, obj=None):
        form = RegisterForm()
        return form

    # Edit Form
    def edit_form(self, obj):
        form = EditUserForm(username_field=obj.username,
                                 #email_field=obj.email,
                                 )
        return form

