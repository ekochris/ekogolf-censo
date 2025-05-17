from app import db
from datetime import datetime

class Resident(db.Model):
    __tablename__ = 'resident'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name_p = db.Column(db.String(100), nullable=False)
    last_name_m = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    member_number = db.Column(db.String(20), nullable=False)
    direccion_yvr = db.Column(db.String(100), nullable=False)
    street_number = db.Column(db.String(50), nullable=True)  # ✅ nuevo campo opcional
    privada = db.Column(db.String(100), nullable=False)
    lote = db.Column(db.String(100), nullable=False)
    id_front = db.Column(db.String(200))
    id_back = db.Column(db.String(200))
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    vehicles = db.relationship('Vehicle', backref='owner', cascade="all, delete-orphan")


class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    year = db.Column(db.Integer)
    color = db.Column(db.String(50))
    plates = db.Column(db.String(50))
    vin = db.Column(db.String(100))
    photo_rear = db.Column(db.String(200))
    photo_underside = db.Column(db.String(200))
    circulation_card = db.Column(db.String(200))
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'), nullable=False)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='viewer')
