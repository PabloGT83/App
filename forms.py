#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 18:49:47 2021

@author: pablogtorres
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
  user =  StringField(label="", validators=[DataRequired()], description="")
  submit = SubmitField("Try a Twitter user!!")