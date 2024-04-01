import os

class Config:
  PROPAGATE_EXCEPTIONS = True
  API_TITLE = '141-week-5-proj'
  API_VERSION = 'v1'
  OPENAPI_VERSION = '3.0.1'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DB_PROJ_URL')
  JWT_SECRET_KEY = "This is a scret key. Don't give this to anyone!"