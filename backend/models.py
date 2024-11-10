from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

# User, Role, and UserRoles for RBAC
class User(db.Model, UserMixin):
   

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)
    
    # Many-to-many relationship with roles
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('bearers', lazy='dynamic'))
    # One-to-many relationships with campaigns and ad requests
    campaigns = db.relationship('Campaign', backref='sponsor', lazy=True)
    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True)


class Role(db.Model, RoleMixin):
   

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=True)


class UserRoles(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)


# Campaign Model
class Campaign(db.Model):
   

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    start_date = db.Column(db.DateTime, nullable = False)
    end_date = db.Column(db.DateTime, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.String, nullable=False)  # Either 'public' or 'private'
    goals = db.Column(db.String, nullable=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User (Sponsor)

    # One-to-many relationship with AdRequest
    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True)


# AdRequest Model
class AdRequest(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User (Influencer)
    requirements = db.Column(db.String, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)  # E.g., 'Pending', 'Accepted', 'Rejected'
    messages = db.Column(db.Text, nullable=True)


# Influencer Profile Information
class InfluencerProfile(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String, nullable=False)
    niche = db.Column(db.String, nullable=False)
    followers = db.Column(db.Integer, nullable=False)  # E.g., number of followers

    user = db.relationship('User', backref=db.backref('profile', uselist=False))


# For demonstration purposes; Redis caching or Celery jobs would be handled separately.
