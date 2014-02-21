#!env/bin/python
# -*- coding: utf-8 -*-

from app import db


class Principle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codename = db.Column(db.String(255), nullable=False)

    translations = db.relationship("PrinciplesTranslation", backref="principle")

    def __unicode__(self):
        return self.codename


class PrinciplesTranslation(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    principle_id = db.Column(db.Integer, db.ForeignKey("principle.id"))
    language = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __unicode__(self):
        return self.name
