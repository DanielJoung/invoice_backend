import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

products = Blueprint("products", "products")


@products.route("/", methods={"GET"})
def products_index():
    result = models.Product.select()
    product_dict = [model_to_dict(product) for product in result]
    print(product_dict, "get product")
    # del product_dict["company"]["password"]
    return jsonify({
        'data': product_dict,
        'message': "Successfully found",
        'status': 200
    }), 200


@products.route('/', methods=['POST'])
@login_required
def create_products():
    payload = request.get_json()

    query = models.Company.get(
        models.Company.companyname == payload['company'])

    new_product = models.Product.create(
        productname=payload['productname'], company=query, price=payload['price'], quantity=payload['quantity'], discount=payload['discount'])

    product_dict = model_to_dict(new_product)
    # product_dict['company'].pop['password']
    del product_dict['company']['password']
    return jsonify(
        data=product_dict,
        message="Successfully created product",
        status=201
    ), 201


@products.route('/<id>', methods=['PUT'])
def update_product(id):
    payload = request.get_json()
    query = models.Product.update(**payload).where(models.Product.id == id)
    query.execute()
    return jsonify(
        data=model_to_dict(models.Product.get_by_id(id)),
        status=200,
        message='Update successfully'
    ), 200


@products.route('/<id>', methods=['DELETE'])
def delete_product(id):
    query = models.Product.delete().where(models.Product.id == id)
    query.execute()
    return jsonify(
        data=model_to_dict(models.Product.get_by_id(id)),
        message='Successfully deleted',
        status=200
    ), 200
