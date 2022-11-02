import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

products = Blueprint("products","products")

@products.route("/products", methods={"GET"})
def products_index():

  current_user_product_dict = [model_to_dict(product) for product in current_user.products]

  for product_dict in current_user_product_dict:
    product_dict['company'].pop('password')

  return jsonify ({
    'data': current_user_product_dict,
    'message': f"Successfully found {len(current_user_product_dict)} products",
    'status': 200
  }),200

@products.route('/product', methods=['POST'])
def create_products():
  payload = request.get_json()
  new_product = models.Product.create(productName=payload['productName'],company=current_user.id, price=payload['price'], quantity=payload['quantity'],discount=payload['discount'])
  
  product_dict = model_to_dict(new_product)
  product_dict['company'].pop['password']
  return jsonify(
    data=product_dict,
    message = "Successfully created product",
    status=201
  ),201

@products.route('/products/<id>', methods=['PUT'])
def update_product(id):
  payload = request.get_json()
  query = models.Product.update(**payload).where(models.Product.id == id)
  query.execute()
  return jsonify(
    data = model_to_dict(models.Product.get_by_id(id)),
    status=200,
    message = 'Update successfully'
  ),200

@products.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  query = models.Product.delete().where(models.Product.id == id)
  query.execute()
  return jsonify(
    data = model_to_dict(models.Product.get_by_id(id)),
    message = 'Successfully deleted',
    status=200
  ),200