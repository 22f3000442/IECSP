from flask import jsonify, request, current_app as app
from datetime import datetime
from flask_restful import Api, Resource, fields, marshal_with
from flask_security import auth_required, current_user
from backend.models import Campaign, db

api = Api(prefix = '/api')

campaign_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'description' : fields.String,
    'start_date' : fields.DateTime,
    'end_date' : fields.DateTime,
    'budget' : fields.Float,
    'visibility': fields.String,
    'goals' : fields.String,
    'sponsor_id' : fields.Integer,
}

class CampaignAPI(Resource):
    
    @marshal_with(campaign_fields)
    @auth_required('token')
    def get(self, campaign_id):
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return {"message" : 'not found'}, 404
        return campaign
    @auth_required('token')
    def delete(self, campaign_id):
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return {"message" : "not found"}, 404
        if campaign.sponsor_id == current_user.id:
            db.session.delete(campaign)
            db.session.commit()
        else:
            return {"message" : "not valid user"}, 403        


class CampaignListAPI(Resource):
    
    @marshal_with(campaign_fields)
    @auth_required('token')
    def get(self):
        campaigns = Campaign.query.all()
        return campaigns
    @auth_required('token')
    def post(self):
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        start_date = datetime.strptime(data.get("start_date"), '%Y-%m-%d')
        end_date =datetime.strptime(data.get("end_date"), '%Y-%m-%d')
        budget = data.get("budget")
        visibility = data.get("visibility", "public")
        goals = data.get("goals")

        campaign = Campaign(name =  name, description = description, start_date = start_date, end_date = end_date, budget = budget,visibility = visibility, goals = goals, sponsor_id = current_user.id)
        db.session.add(campaign)
        db.session.commit()
        return jsonify({"message" : "campaign created"})


    

api.add_resource(CampaignAPI,'/campaigns/<int:campaign_id>')
api.add_resource(CampaignListAPI, '/campaigns')