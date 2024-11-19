import os
from urllib.parse import quote_plus

password = quote_plus(os.getenv('DB_PASSWORD', 'AGpiPAbmsPgaHZpsluaMjHvvXRigJVjr'))
db_host = os.getenv('DB_HOST', 'autorack.proxy.rlwy.net')
db_port = os.getenv('DB_PORT', '13722')
db_name = os.getenv('DB_NAME', 'railway')
db_user = os.getenv('DB_USER', 'postgres')

password_2 = quote_plus(os.getenv('LOCAL_DB_PASSWORD', 'postgres'))
db_host_2 = os.getenv('LOCAL_DB_HOST', 'localhost')
db_port_2 = os.getenv('LOCAL_DB_PORT', '5432')
db_name_2 = os.getenv('LOCAL_DB_NAME', 'users')
db_user_2 = os.getenv('LOCAL_DB_USER', 'postgres')

DATABASE_URL = f"postgresql://{db_user}:{password}@{db_host}:{db_port}/{db_name}"
DATABASE_URL_2 = f"postgresql://{db_user_2}:{password_2}@{db_host_2}:{db_port_2}/{db_name_2}"

class Config:
    SQLALCHEMY_BINDS = {
        'db1': DATABASE_URL,
        'db2': DATABASE_URL_2
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

