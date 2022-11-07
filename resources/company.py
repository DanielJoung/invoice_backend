import models
from flask import request, jsonify,Blueprint
from flask_bcrypt import generate_password_hash,check_password_hash
from flask_login import login_user,current_user,logout_user
from playhouse.shortcuts import model_to_dict

company = Blueprint("company","company")

@company.route("/search", methods=['GET'])
def get_company():
  result = models.Company.select()

  company_dicts = [model_to_dict(company) for company in result]

  return jsonify({
    'data': company_dicts,
    'message': "Successfully found",
    'status': 200
  }),200

@company.route("/register", methods=["POST"])
def register():
  payload=request.get_json()
  payload['email'] = payload['email'].lower()

  try:
    models.Company.get(models.Company.email == payload['email'])
    return jsonify(data={},status={"code":401,"message":"A company with that email already exists"}),401

  except models.DoesNotExist:
    payload['password'] = generate_password_hash(payload['password'])
    company=models.Company.create(**payload)
    login_user(company)

    company_dict = model_to_dict(company)
    del company_dict['password']

    return jsonify(
      data=company_dict,
      status={
        "code": 201,
        "message": "Success"
      }
    ),201

@company.route("/login", methods=["POST"])
def login():
  payload=request.get_json()
  try:
    company=models.Company.get(models.Company.email == payload['email'])
    company_dict = model_to_dict(company)

    if(check_password_hash(company_dict['password'],payload['password'])):
      del company_dict['password']
      login_user(company)
      return jsonify(
        data=company_dict,
        status={
          "code": 200,
          "message": "Success Login"
        }
      ),200
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

@company.route("/logged_in_company", methods=["GET"])
def get_logged_in_company():
  company_dict = model_to_dict(current_user)
  company_dict.pop("password")
  return jsonify(data=company_dict),200


@company.route('/logout', methods=['GET'])
def logout():
  logout_user()
  return jsonify(
    message= "logout"
  )