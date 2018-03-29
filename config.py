class config(object):
    DEBUG = True # Turns on debugging features in Flask
    BCRYPT_LEVEL = 12 # Configuration for the Flask-Bcrypt extension
    MAIL_FROM_EMAIL = "rickynyairo@gmail.com" # For use in application emails
    SQLALCHEMY_DATABASE_URI = 'postgres://pyvwooawnqetnx:e679603cb7cec6ad44f22476c3e19a3d0fb3098a57d48b5fa261e689122bf16d@ec2-23-21-85-76.compute-1.amazonaws.com:5432/dcr2iq15m06u5r'
    SQLALCHEMY_TRACK_MODIFICATIONS = False