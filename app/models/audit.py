from flask_login import UserMixin
from app import db


class Audit(db.Model, UserMixin):
    __tablename__ = 'audit'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    audit_date = db.Column(db.DateTime)
    table_name = db.Column(db.String(100))
    primary_key_value = db.Column(db.Integer)
    audit_detail = db.relationship('AuditDetail', backref='audit')

    def __repr__(self):
        return '{}'.format(self.name)
