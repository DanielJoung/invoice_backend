import models
from flask import request, jsonify, Blueprint,session
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

user = Blueprint("user", "user")

@user.route("/register", methods=["POST"])
def register():
    payload = request.get_json()
    # print(payload)
    # get the company name in the payload
    # get the company id
    # comp = models.Company.select()
    find_company = models.Company.select().where(
        models.Company.companyname == payload['company'])

    payload['company'] = find_company

    payload['email'] = payload['email'].lower()

    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={"code": 401, "message": "A user with that email already exists"}), 401
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        
        user = models.User.create(**payload)
        login_user(user)
        user_dict = model_to_dict(user)
        del user_dict['password']
        del user_dict['company']['password']



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
    # print(payload)
    try:
        user = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user)
        if (check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            del user_dict["company"]['password']
            login_user(user)
            # print(current_user.id)
            session["login_type"] ="User"
            # print(session.get("login_type"))
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

@user.route("/search_user", methods=['GET'])
def get_user():
    find_company = models.User.get(models.User.id == current_user)
    user_dicts = model_to_dict(find_company)
    print(current_user,"user")
    del user_dicts["password"]
    del user_dicts["company"]["password"]

    # product
    product_dicts = []
    find_company_product = models.Product.select()
    all_product_dicts = [model_to_dict(product) for product in find_company_product]
    # print(product_dicts,"product")
    for product in all_product_dicts: 
        if(product["company"]["companyname"] == user_dicts["company"]["companyname"]):
            product_dicts.append(product)

    # store
    find_company_store = models.Store.select()
    store_dicts = []
    all_store_dicts = [model_to_dict(store) for store in find_company_store]
    for store in all_store_dicts:
        if (store["company"]["companyname"] == user_dicts["company"]["companyname"]):
            store_dicts.append(store)
    # print(store_dicts,"store")

    for password in store_dicts:
        del password["company"]["password"]
    for password in product_dicts:
        del password["company"]["password"]

    return jsonify(
        user= user_dicts,
        product= product_dicts,
        store= store_dicts,
        message = "Successfully found",
        status= 200
    ), 200


@user.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(
        message="logout"
    )


