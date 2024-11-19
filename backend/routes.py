from flask import current_app as app, request, jsonify, render_template, send_file
from flask_security import auth_required, verify_password, hash_password
from backend.models import db
from datetime import datetime
from backend.celery.tasks import add, create_csv
from celery.result import AsyncResult

datastore = app.security.datastore
cache = app.cache

@app.get('/')
def home():
    return render_template('index.html')

@app.get('/celery')
def celery():
    task = add.delay(10, 20)
    return {'task_id' : task.id}

@app.get('/get-celery-data/<id>')
def getData(id):
    result = AsyncResult(id)

    if result.ready():
        return {'result' : result.result}, 200
    else:
        return {'message' : 'task not ready'}, 405


@app.get('/create-csv')
def createCSV():
    task = create_csv.delay()
    return {'task_id' : task.id}, 200

@app.get('/get-csv/<id>')
def getCSV(id):
    result = AsyncResult(id)

    if result.ready():
        return send_file(f'./backend/celery/user-downloads/{result.result}'), 200
    else:
        return {'message' : 'task not ready'}, 405


@app.get('/cache')
@cache.cached(timeout = 5)
def cache():
    return {'time' : str(datetime.now())}

@app.get('/protected')
@auth_required('token')
def protected():
    return '<h1> only accsessible by auth user </h1>'


@app.route('/login', methods = ['POST'])
def login():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message' : 'invalid username'}), 404
    
    user = datastore.find_user(username = username)

    if not user:
        return jsonify({'message': 'invalid user'}), 404
    if verify_password(password, user.password):
        return jsonify({'token': user.get_auth_token(),
                        'email': user.email,
                        'role': user.roles[0].name,
                        'username': user.username,
                        'id': user.id})

    return jsonify({'message': 'wrong password'}), 400

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    role = data.get('role')

    if not email or not password or not username or role not in ['sponsor', 'influencer']:
        return jsonify({'message': 'invalid input'}), 404
    
    user = datastore.find_user(email = email)

    if user:
        return jsonify({'message' : 'user already exists'}), 404

    try:
        datastore.create_user(email = email, password = hash_password(password), username = username, roles = [role], active = True)
        db.session.commit()
        return jsonify({'message': 'user created'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'error creating user'}), 400
