from flask_sqlalchemy import SQLAlchemy
#from flask import Flask
from elixir import app
#app = Flask(__name__, instance_relative_config=True)
#app.config.from_object('config')
#app.config.from_pyfile('config.py')
#app.config.from_pyfile('models.py')
db = SQLAlchemy(app)

class users(db.Model):
    #table to store users
    __tablename__ = 'users'
    MSISDN = db.Column(db.String(10), primary_key = True)
    first_name = db.Column(db.String(10), unique = False, nullable = False)
    last_name = db.Column(db.String(10), unique = False)
    national_id = db.Column(db.Integer, unique = False, nullable = False)

    def __init__(self, MSISDN, first_name, last_name, national_id):
        self.MSISDN = MSISDN
        slef.first_name = first_name
        self.last_name = last_name
        self.national_id = national_id

    def __repr__(self):
        return '<Number %r>' % MSISDN

class partners(db.Model):
    __tablename__ = 'partners'

    short_code = db.Column(db.Integer, primary_key = True)
    contact = db.Column(db.String(10), unique = False)
    bus_name = db.Column(db.String(50), unique = False, nullable = False)
    def __init__(self, contact, short_code, bus_name):
        self.contact = contact
        self.short_code = short_code
        self.bus_name = bus_name

    def __repr__(self):
        return '<bus_name %r>' % bus_name

class b2c_transactions(db.Model):
    __tablename__ = 'b2c_transactions'
    tx_id = db.Column(db.String(10), primary_key = True)
    MSISDN = db.Column(db.String(10), unique = False, nullable = False)
    amount = db.Column(db.Integer, unique = False, nullable = False)
    bill_ref = db.Column(db.String(20), unique = False)

    def __init__(self, tx_id, MSISDN, amount, bill_ref):
        self.tx_id = tx_id
        self.MSISDN = MSISDN
        self.amount =amount
        if len(bill_ref) is not 0:
            self.bill_ref = bill_ref
        else:
            self.bill_ref = 'Promotion Payment'

class b2b_transactions(db.Model):
    __tablename__ = 'b2b_transactions'
    tx_id = db.Column(db.String(10), primary_key = True)
    short_code = db.Column(db.String(10), unique = False, nullable = False)
    amount = db.Column(db.Integer, unique = False, nullable = False)
    bill_ref = db.Column(db.String(20), unique = False)

    def __init__(self, tx_id, MSISDN, amount, bill_ref):
        self.tx_id = tx_id
        self.MSISDN = MSISDN
        self.amount =amount
        if len(bill_ref) is not 0:
            self.bill_ref = bill_ref
        else:
            self.bill_ref = 'Business Payment'

class c2b_transactions(db.Model):
    #_ID = 1000#itertools.count()
    __tablename__ = 'c2b_transactions'
    tx_id = db.Column(db.String(10), primary_key=True) #Transaction ID
    MSISDN = db.Column(db.String(80), unique=False, nullable = False)
    amount = db.Column(db.Integer, unique=False, nullable = False)
    bill_ref = db.Column(db.String(10), unique=False)
    
    def __init__(self, tx_id, MSISDN, amount, bill_ref):
        self.tx_id = tx_id
        self.MSISDN = MSISDN
        self.amount =amount
        if len(bill_ref) is not 0:
            self.bill_ref = bill_ref
        else:
            self.bill_ref = 'user'
                
    def __repr__(self):
        return '<Number %r>' % self.MSISDN