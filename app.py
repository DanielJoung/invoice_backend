from flask import Flask
from resources.company import company
from resources.product import products
from resources.store import stores
from resources.user import user
import models
from flask_cors import CORS
from flask_login import LoginManager
import os
from dotenv import load_dotenv
load_dotenv()

DEBUG=True
PORT=os.environ.get("PORT")

app =Flask(__name__)

app.secret_key=os.environ.get("APP_SECRET")
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
  try:
    return models.User.get(models.User.id==userid)
  except models.DoesNotExist:
    return None

@login_manager.user_loader
def load_company(companyid):
  try:
    return models.Company.get(models.Company.id==companyid)
  except models.DoesNotExist:
    return None

CORS(company, origin=['http://localhost:3000'], supports_credentials=True)
CORS(products, origin=['http://localhost:3000'], supports_credentials=True)
CORS(stores, origin=['http://localhost:3000'], supports_credentials=True)
CORS(user, origin=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(company, url_prefix='/company')
app.register_blueprint(user, url_prefix='/users')
app.register_blueprint(stores, url_prefix='/stores')
app.register_blueprint(products, url_prefix='/products')


if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)