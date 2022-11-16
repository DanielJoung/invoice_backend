import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

stores = Blueprint("stores", "stores")


@stores.route("/all_store", methods={"GET"})
def products_index():
    current_user_store_dict = [model_to_dict(
        store) for store in current_user.stores]

    for store_dict in current_user_store_dict:
        del store_dict['company']['password']

    return jsonify({
        'data': current_user_store_dict,
        'message': f"Successfully found {len(current_user_store_dict)} products",
        'status': 200
    }), 200


@stores.route('/create', methods=['POST'])
def create_stores():
    payload = request.get_json()

    query = models.Company.get(
    models.Company.companyname == payload['company'])

    new_store = models.Store.create(
        storename=payload['storename'], company=query, address=payload['address'], storephone=payload['storephone'])

    store_dict = model_to_dict(new_store)
    del store_dict['company']['password']

    return jsonify(
        data=store_dict,
        message="Successfully created product",
        status=201
    ), 201


@stores.route('/<id>', methods=['PUT'])
def update_store(id):
    payload = request.get_json()
    query = models.Store.update(**payload).where(models.Store.id == id)
    query.execute()
    return jsonify(
        data=model_to_dict(models.Store.get_by_id(id)),
        status=200,
        message='Update successfully'
    ), 200


@stores.route('/<id>', methods=['DELETE'])
def delete_store(id):
    query = models.Store.delete().where(models.Store.id == id)
    query.execute()
    return jsonify(
        data=model_to_dict(models.Store.get_by_id(id)),
        message='Successfully deleted',
        status=200
    ), 200
