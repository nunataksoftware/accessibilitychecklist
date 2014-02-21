#!env/bin/python
# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required, EqualTo, Email


class LoginForm(Form):
    username = TextField(u"User", [Required()])
    password = PasswordField(u"Password", [Required()])


class RegisterForm(Form):
    username = TextField(u"User", [Required()])
    password = PasswordField(u"Password", [Required()])
    repassword = PasswordField(u"Repeat password", [EqualTo("password")])


class ChangePassForm(Form):
    passw = PasswordField("Password",
                          [Required("Complete the field."), EqualTo("repeat", message="Passwords should be the same")])
    repeat = PasswordField(
        "Repeat Password", [Required("Complete the field.")])


class EditUserForm(Form):
    username_field = TextField("User", [Required("Required Field")])
    # email_field = TextField("Email", [Email("Email no valido")])
