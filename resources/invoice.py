import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

invoices = Blueprint("invoices", "invoices")

@invoices.route("/all_invoice", methods=["GET"])
def invoice_index():
  current_user_invoice_dicts = [model_to_dict(invoice) for invoice in current_user.invoices]
  print(current_user_invoice_dicts)

  return jsonify({
    "data" : current_user_invoice_dicts,
    "message" : "Success to get",
    "status" :200
  }),200


@invoices.route("/create", methods=["POST"])
# @login_required
def create_invoice():
  payload = request.get_json()

  query = models.User.get(
    models.User.username == payload['user'])

  new_invoice = models.Invoice.create(
      balance=payload['balance'], case=payload['case'], user=query)

  invoice_dict = model_to_dict(new_invoice)
  print(invoice_dict)

  return jsonify(
    data= invoice_dict,
    message = "Success create",
    status = 201
  ),201


@invoices.route("/<id>", methods=["GET"])
def get_one_invoice(id):
  invoice = models.Invoice.get_by_id(id)
  return jsonify(
    data = model_to_dict(invoice),
    message = "Success",
    status = 200
  ),200


@invoices.route("/<id>", methods=["PUT"])
def update_invoice(id):
  payload = request.get_json()
  query = models.Invoice.updata(**payload).where(models.Invoice.id == id)
  query.execute()
  return jsonify(
    data = model_to_dict(models.Invoice.get_by_id(id)),
    message = "Updated Success",
    status = 200
  ),200

@invoices.route("/<id>", methods=["DELETE"])
def delete_invoice(id):
  query = models.Invoice.delete().where(models.Invoice.id == id)
  query.execute()
  return jsonify(
    data = model_to_dict(models.Invoice.get_by_id(id)),
    message = "Success delete",
    status =200
  ),200
