import models
from flask import request, jsonify,Blueprint
from flask_bcrypt import generate_password_hash,check_password_hash
from flask_login import login_user,current_user,logout_user
from playhouse.shortcuts import model_to_dict

user = Blueprint("users","user")

@user.route("/register", methods=["POST"])
def register():
  payload=request.get_json()
  payload['email'] = payload['email'].lower()
  try:
    models.User.get(models.User.email == payload['email'])
    return jsonify(data={},status={"code":401,"message":"A user with that email already exists"}),401
  except models.DoesNotExist:
    payload['password'] = generate_password_hash(payload['password'])
    user=models.User.create(**payload)
    login_user(user)
    user_dict = model_to_dict(user)

    del user_dict['password']

    return jsonify(
      data=user_dict,
      status={
        "code": 201,
        "message": "Success"
      }
    ),201

@user.route("/login", methods=["POST"])
def login():
  payload=request.get_json()
  try:
    user=models.User.get(models.User.email == payload['email'])
    user_dict = model_to_dict(user)
    if(check_password_hash(user_dict['password'],payload['password'])):
      del user_dict['password']
      login_user(user)
      return jsonify(
        data=user_dict,
        status={
          "code": 201,
          "message": "Success Login"
        }
      ),201
    else:
      return jsonify(
        data={},
        status={
          'code':401,
          'message': "Email or Password does not match"
        }
      ),401
  except models.DoesNotExist:
    return jsonify(
      data={},
      status= {
        'code':401,
        'message': 'Email or Password does not match'
      }
    ),401

@user.route('/logged_in_user', methods=['GET'])
def get_logged_in_user():
  current_user_user_dict = [model_to_dict(user) for user in current_user.users]

  for user_dict in current_user_user_dict:
    user_dict['company'].pop('password')

  return jsonify(
    data=current_user_user_dict,
    status={
      "code": 200
    }
  ),200

@user.route('/logout', methods=['GET'])
def logout():
  logout_user()
  return jsonify(
    message= "logout"
  )