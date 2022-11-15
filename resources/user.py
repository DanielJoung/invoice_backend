import models
from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

user = Blueprint("user", "user")


@user.route("/search_user", methods=['GET'])
def get_user():
    result = models.User.select()
    user_dicts = [model_to_dict(user) for user in result]
    return jsonify({
        'data': user_dicts,
        'message': "Successfully found",
        'status': 200
    }), 200


@user.route("/register", methods=["POST"])
def register():
    payload = request.get_json()
    # print(payload)
    # get the company name in the payload
    # get the company id
    # comp = models.Company.select()
    find_company = models.Company.select().where(
        models.Company.companyname == payload['company'])
    # del find_company['password']
    payload['company'] = find_company

    payload['email'] = payload['email'].lower()
    # print(payload)
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={"code": 401, "message": "A user with that email already exists"}), 401
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)
        login_user(user)

        user_dict = model_to_dict(user)
        print(user_dict, "info")
        del user_dict['password']
        del user_dict['company']['password']

        # print(user_dict)

        return jsonify(
            data=user_dict,
            status={
                "code": 201,
                "message": "Success"
            }
        ), 201


@user.route("/login", methods=["POST"])
def login():
    payload = request.get_json()
    try:
        user = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user)
        if (check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            print(user_dict)
            return jsonify(
                data=user_dict,
                status={
                    "code": 200,
                    "message": "Success Login"
                }
            ), 200
        else:
            return jsonify(
                data={},
                status={
                    'code': 401,
                    'message': "Email or Password does not match"
                }
            ), 401
    except models.DoesNotExist:
        return jsonify(
            data={},
            status={
                'code': 401,
                'message': 'Email or Password does not match'
            }
        ), 401


@user.route('/logged_in_user', methods=['GET'])
def get_logged_in_user():
    user_dict = model_to_dict(current_user)
    user_dict.pop('password')

    return jsonify(
        data=user_dict,
        status={
            "code": 200
        }
    ), 200


@user.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(
        message="logout"
    )
