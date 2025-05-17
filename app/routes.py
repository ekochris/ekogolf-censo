# app/routes.py
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, send_file, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from app.forms import RegistroForm
from app.models import db, Resident, Vehicle, User
from app.utils.pdf_generator import generar_pdf
from io import BytesIO
from datetime import datetime
from sqlalchemy import func
from openpyxl import Workbook
from openpyxl.styles import Font

bp = Blueprint('main', __name__)

def eliminar_archivo(ruta):
    if ruta and os.path.exists(ruta):
        os.remove(ruta)

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = RegistroForm()
    if form.validate_on_submit():
        id_front_path = save_file(form.id_front.data, 'ids')
        id_back_path = save_file(form.id_back.data, 'ids')

        resident = Resident(
            first_name=form.first_name.data,
            last_name_p=form.last_name_p.data,
            last_name_m=form.last_name_m.data,
            email=form.email.data,
            phone=form.phone.data,
            member_number=form.member_number.data,
            direccion_yvr=form.direccion_yvr.data,
            privada=form.privada.data,
            street_number=form.street_number.data,
            lote=form.lote.data,
            id_front=id_front_path,
            id_back=id_back_path,
            created_at=datetime.utcnow()
        )
        db.session.add(resident)
        db.session.commit()

        num_vehicles = int(form.num_vehicles.data)
        for i in range(num_vehicles):
            vehicle = Vehicle(
                resident_id=resident.id,
                make=getattr(form, f'make_{i+1}').data,
                model=getattr(form, f'model_{i+1}').data,
                year=getattr(form, f'year_{i+1}').data,
                color=getattr(form, f'color_{i+1}').data,
                plates=getattr(form, f'plates_{i+1}').data,
                vin=getattr(form, f'vin_{i+1}').data,
                photo_rear=save_file(getattr(form, f'photo_rear_{i+1}').data, 'vehicles'),
                photo_underside=save_file(getattr(form, f'photo_underside_{i+1}').data, 'vehicles'),
                circulation_card=save_file(getattr(form, f'circulation_card_{i+1}').data, 'vehicles')
            )
            db.session.add(vehicle)

        db.session.commit()

        # Generar PDF
        output_dir = os.path.join(current_app.static_folder, "pdfs")
        os.makedirs(output_dir, exist_ok=True)
        pdf_filename = f"registro_{resident.id}.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)
        logo_path = os.path.join(current_app.static_folder, "images", "logo.png")
        generar_pdf(resident, resident.vehicles, pdf_path, logo_path if os.path.exists(logo_path) else None)

        flash('Formulario enviado con éxito ✅', 'success')
        return redirect(url_for('main.gracias'))

    return render_template('form.html', form=form)

@bp.route('/eliminar_registro/<int:resident_id>', methods=['POST'])
def eliminar_registro(resident_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('No tienes permisos para realizar esta acción.', 'danger')
        return redirect(url_for('main.ver_registros'))

    residente = Resident.query.get_or_404(resident_id)
    archivos = [
        residente.id_front, residente.id_back,
        f"static/pdfs/registro_{residente.id}.pdf"
    ]
    for v in residente.vehicles:
        archivos += [v.photo_rear, v.photo_underside, v.circulation_card]

    for path in archivos:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                print(f"⚠️ Error al eliminar archivo: {path} — {e}")

    db.session.delete(residente)
    db.session.commit()
    flash('Registro eliminado correctamente ✅', 'success')
    return redirect(url_for('main.ver_registros'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if not request.remote_addr.startswith('127.') and not request.remote_addr.startswith('10.'):
        return "⛔ Acceso restringido solo desde la red local.", 403

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_role'] = user.role
            flash('Inicio de sesión exitoso ✅', 'success')
            return redirect(url_for('main.ver_registros'))
        else:
            flash('Usuario o contraseña incorrectos ❌', 'danger')
            return redirect(url_for('main.login'))

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_role', None)
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('main.login'))

@bp.route('/registros')
def ver_registros():
    if not request.remote_addr.startswith('127.') and not request.remote_addr.startswith('10.'):
        return "⛔ Acceso restringido solo desde la red local.", 403

    if 'user_id' not in session:
        flash('Debes iniciar sesión para ver esta página.', 'warning')
        return redirect(url_for('main.login'))

    fecha_str = request.args.get('fecha')
    if fecha_str:
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            residentes = Resident.query.filter(func.date(Resident.created_at) == fecha).all()
        except ValueError:
            flash('Formato de fecha inválido.', 'danger')
            residentes = Resident.query.all()
    else:
        residentes = Resident.query.all()

    return render_template('registros.html', residentes=residentes, fecha_filtro=fecha_str)

@bp.route('/exportar_excel')
def exportar_excel():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para exportar datos.', 'warning')
        return redirect(url_for('main.login'))

    residentes = Resident.query.all()
    wb = Workbook()
    ws = wb.active
    ws.title = 'Registros'

    headers = [
        'Nombre Completo', 'Correo', 'Socio', 'Teléfono', 'Dirección',
        'Privada', 'Placas', 'Marca', 'Modelo', 'Color',
        'INE Frente', 'INE Reverso', 'Trasera', 'Inferior', 'Circulación',
        'PDF', 'Fecha'
    ]
    ws.append(headers)

    def crear_link(ruta_relativa):
        if ruta_relativa:
            return f'=HYPERLINK("http://localhost:8080/{ruta_relativa}", "Ver")'
        return ''

    for r in residentes:
        direccion_completa = f"{r.direccion_yvr}-{r.street_number}-{r.lote}"
        if r.vehicles:
            for v in r.vehicles:
                row = [
                    f"{r.first_name} {r.last_name_p} {r.last_name_m}",
                    r.email,
                    r.member_number,
                    r.phone,
                    direccion_completa,
                    r.privada,
                    v.plates,
                    v.make,
                    v.model,
                    v.color,
                    crear_link(r.id_front),
                    crear_link(r.id_back),
                    crear_link(v.photo_rear),
                    crear_link(v.photo_underside),
                    crear_link(v.circulation_card),
                    crear_link(f"static/pdfs/registro_{r.id}.pdf"),
                    r.created_at.strftime('%d/%m/%Y %H:%M:%S') if r.created_at else ''
                ]
                ws.append(row)
        else:
            row = [
                f"{r.first_name} {r.last_name_p} {r.last_name_m}",
                r.email,
                r.member_number,
                r.phone,
                direccion_completa,
                r.privada,
                '', '', '', '',
                crear_link(r.id_front),
                crear_link(r.id_back),
                '', '', '',
                crear_link(f"static/pdfs/registro_{r.id}.pdf"),
                r.created_at.strftime('%d/%m/%Y %H:%M:%S') if r.created_at else ''
            ]
            ws.append(row)

    for col in ws.columns:
        max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_length + 2

    output_path = os.path.join(current_app.static_folder, "registros_exportados.xlsx")
    wb.save(output_path)
    return send_from_directory(current_app.static_folder, "registros_exportados.xlsx", as_attachment=True)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'heic', 'heif', 'webp'}

def save_file(file, folder):
    if file:
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            flash(f"❌ Formato de archivo no permitido: {filename}", 'danger')
            return None
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > 10 * 1024 * 1024:
            flash(f"❌ El archivo '{filename}' excede los 10 MB.", 'danger')
            return None
        uploads_dir = os.path.join('static', 'uploads', folder)
        os.makedirs(uploads_dir, exist_ok=True)
        filepath = os.path.join(uploads_dir, filename)
        file.save(filepath)
        return filepath
    return None

@bp.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    if not request.remote_addr.startswith('127.') and not request.remote_addr.startswith('10.'):
        return "⛔ Acceso restringido solo desde la red local.", 403

    if 'user_id' not in session:
        flash('Debes iniciar sesión como administrador.', 'warning')
        return redirect(url_for('main.login'))

    user = User.query.get(session['user_id'])
    if not user or user.role != 'admin':
        flash('No tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('main.ver_registros'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.', 'warning')
        else:
            nuevo_usuario = User(
                username=username,
                password=generate_password_hash(password),
                role=role
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash(f'Usuario "{username}" creado exitosamente ✅', 'success')
            return redirect(url_for('main.ver_registros'))

    return render_template('agregar_usuario.html')

@bp.app_errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

@bp.route('/gracias')
def gracias():
    return render_template('gracias.html')
