from datetime import timedelta
class Config:
    debug=True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:admin123*@localhost:5432/YESCABANK'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'YESC@BANK'  # Clave para firmar los tokens JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)  # Tiempo de expiración del token

    MAIL_SERVER = 'smtp.fastmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'yescabank@sent.com'
    MAIL_PASSWORD = '4p2t583b4k5s475y'
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True