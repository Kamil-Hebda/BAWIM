import os
from urllib.parse import quote_plus

password = quote_plus(os.getenv('DB_PASSWORD', 'AGpiPAbmsPgaHZpsluaMjHvvXRigJVjr'))
db_host = os.getenv('DB_HOST', 'autorack.proxy.rlwy.net')
db_port = os.getenv('DB_PORT', '13722')
db_name = os.getenv('DB_NAME', 'railway')
db_user = os.getenv('DB_USER', 'postgres')

DATABASE_URL = f"postgresql://{db_user}:{password}@{db_host}:{db_port}/{db_name}"

class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False