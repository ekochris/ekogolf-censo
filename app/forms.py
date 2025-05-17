# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, NumberRange, InputRequired
from wtforms.validators import Regexp

class RegistroForm(FlaskForm):
    # Datos del residente
    first_name = StringField('Nombre(s)', validators=[DataRequired()])
    last_name_p = StringField('Apellido Paterno', validators=[DataRequired()])
    last_name_m = StringField('Apellido Materno', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    phone = StringField('Teléfono', validators=[DataRequired()])
    member_number = IntegerField('Número de Socio (usa 0 si no aplica)', validators=[InputRequired(), NumberRange(min=0)])

    privada = SelectField('Privada', choices=[
        ('Paseo del jaguar', 'Paseo del jaguar'),
        ('Xpokin peninsula', 'Xpokin peninsula'),
        ('Xpokin', 'Xpokin'),
        ('Kilil', 'Kilil'),
        ('Xkatay', 'Xkatay'),
        ('Serena', 'Serena'),
        ('Cutzam', 'Cutzam'),
        ('Tumin', 'Tumin'),
        ('Toh', 'Toh'),
        ('Anthea', 'Anthea'),
        ('Kanha', 'Kanha'),
        ('Oasis', 'Oasis'),
        ('Kutz', 'Kutz'),
        ('Harmonia', 'Harmonia'),
        ('Cutzam ll', 'Cutzam ll')
    ], validators=[DataRequired()])

    direccion_yvr = StringField('Dirección YVR', validators=[DataRequired()])
    street_number = StringField('Número de Calle')
    lote = StringField('Lote/Villa/Depto', validators=[
    DataRequired(),
    Regexp(r'^\d{3}[A-Za-z]?$', message="Debe ser 3 dígitos (ej. 123) o 3 dígitos seguidos de una letra (ej. 123A)")
    ])


    id_front = FileField('Foto INE Frente', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'pdf'], 'Formatos permitidos: .jpg, .jpeg, .png, .pdf')
    ])
    id_back = FileField('Foto INE Reverso', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'pdf'], 'Formatos permitidos: .jpg, .jpeg, .png, .pdf')
    ])

    num_vehicles = SelectField('Número de Vehículos', choices=[
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')
    ], validators=[DataRequired()])

    # Datos del vehículo 1
    make_1 = StringField('Marca del Vehículo 1', validators=[DataRequired()])
    model_1 = StringField('Modelo del Vehículo 1', validators=[DataRequired()])
    year_1 = StringField('Año del Vehículo 1', validators=[DataRequired()])
    color_1 = StringField('Color del Vehículo 1', validators=[DataRequired()])
    plates_1 = StringField('Placas del Vehículo 1', validators=[DataRequired()])
    vin_1 = StringField('Número de Serie del Vehículo 1', validators=[DataRequired()])
    photo_rear_1 = FileField('Foto Trasera del Vehículo 1', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'pdf'])])
    photo_underside_1 = FileField('Foto Inferior del Vehículo 1', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'pdf'])])
    circulation_card_1 = FileField('Tarjeta de Circulación del Vehículo 1', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'pdf'])])

    # Vehículos 2 a 4 (sin validadores obligatorios)
    make_2 = StringField('Marca del Vehículo 2')
    model_2 = StringField('Modelo del Vehículo 2')
    year_2 = StringField('Año del Vehículo 2')
    color_2 = StringField('Color del Vehículo 2')
    plates_2 = StringField('Placas del Vehículo 2')
    vin_2 = StringField('Número de Serie del Vehículo 2')
    photo_rear_2 = FileField('Foto Trasera del Vehículo 2', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf'])])
    photo_underside_2 = FileField('Foto Inferior del Vehículo 2', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf'])])
    circulation_card_2 = FileField('Tarjeta de Circulación del Vehículo 2', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf'])])

    make_3 = StringField('Marca del Vehículo 3')
    model_3 = StringField('Modelo del Vehículo 3')
    year_3 = StringField('Año del Vehículo 3')
    color_3 = StringField('Color del Vehículo 3')
    plates_3 = StringField('Placas del Vehículo 3')
    vin_3 = StringField('Número de Serie del Vehículo 3')
    photo_rear_3 = FileField('Foto Trasera del Vehículo 3', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf'])])
    photo_underside_3 = FileField('Foto Inferior del Vehículo 3', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf'])])
    circulation_card_3 = FileField('Tarjeta de Circulación del Vehículo 3', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf'])])

    make_4 = StringField('Marca del Vehículo 4')
    model_4 = StringField('Modelo del Vehículo 4')
    year_4 = StringField('Año del Vehículo 4')
    color_4 = StringField('Color del Vehículo 4')
    plates_4 = StringField('Placas del Vehículo 4')
    vin_4 = StringField('Número de Serie del Vehículo 4')
    photo_rear_4 = FileField('Foto Trasera del Vehículo 4', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf'])])
    photo_underside_4 = FileField('Foto Inferior del Vehículo 4', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf'])])
    circulation_card_4 = FileField('Tarjeta de Circulación del Vehículo 4', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf'])])

    submit = SubmitField('Enviar')
