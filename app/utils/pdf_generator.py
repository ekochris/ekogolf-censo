# app/utils/pdf_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os

def generar_pdf(resident, vehicles, output_path, logo_path=None):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # COLORES y fuente base
    verde_ekogolf = colors.HexColor("#6AA84F")
    c.setFont("Helvetica-Bold", 14)

    # Portada / Datos generales
    if logo_path and os.path.exists(logo_path):
        try:
            c.drawImage(logo_path, 50, height - 100, width=120, preserveAspectRatio=True, mask='auto')
        except:
            pass

    c.setFillColor(verde_ekogolf)
    c.drawString(200, height - 50, "FORMULARIO DE REGISTRO DE RESIDENTE")
    c.setFillColor(colors.black)

    c.setFont("Helvetica", 11)
    y = height - 120
    spacing = 16

    direccion_completa = f"{resident.direccion_yvr}-{resident.street_number}-{resident.lote}"

    datos = [
        ("Nombre", f"{resident.first_name} {resident.last_name_p} {resident.last_name_m}"),
        ("Correo", resident.email),
        ("Teléfono", resident.phone),
        ("Número de socio", resident.member_number),
        ("Dirección", direccion_completa),
        ("Privada", resident.privada),
    ]

    for etiqueta, valor in datos:
        c.drawString(50, y, f"{etiqueta}: {valor}")
        y -= spacing

    # Mostrar INE (frente y reverso)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y - 10, "Identificación Oficial:")
    y -= 130
    try:
        if resident.id_front and os.path.exists(resident.id_front):
            c.drawImage(resident.id_front, 50, y, width=200, height=120, preserveAspectRatio=True, mask='auto')
            c.drawString(50, y - 15, "Frontal")
    except: pass

    try:
        if resident.id_back and os.path.exists(resident.id_back):
            c.drawImage(resident.id_back, 300, y, width=200, height=120, preserveAspectRatio=True, mask='auto')
            c.drawString(300, y - 15, "Reverso")
    except: pass

    c.showPage()

    # Página por cada vehículo
    for idx, vehicle in enumerate(vehicles, start=1):
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(verde_ekogolf)
        c.drawString(200, height - 50, f"VEHÍCULO {idx}")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 11)

        y = height - 90
        veh_data = [
            ("Marca", vehicle.make),
            ("Modelo", vehicle.model),
            ("Año", vehicle.year),
            ("Color", vehicle.color),
            ("Placas", vehicle.plates),
            ("Número de serie", vehicle.vin)
        ]

        for label, value in veh_data:
            c.drawString(50, y, f"{label}: {value}")
            y -= spacing

        # Fotos del vehículo
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Fotografías del Vehículo:")

        y -= 130
        try:
            if vehicle.photo_rear and os.path.exists(vehicle.photo_rear):
                c.drawImage(vehicle.photo_rear, 50, y, width=150, height=100, preserveAspectRatio=True, mask='auto')
                c.drawString(50, y - 15, "Trasera")
        except: pass

        try:
            if vehicle.photo_underside and os.path.exists(vehicle.photo_underside):
                c.drawImage(vehicle.photo_underside, 220, y, width=150, height=100, preserveAspectRatio=True, mask='auto')
                c.drawString(220, y - 15, "Inferior")
        except: pass

        try:
            if vehicle.circulation_card and os.path.exists(vehicle.circulation_card):
                c.drawImage(vehicle.circulation_card, 390, y, width=150, height=100, preserveAspectRatio=True, mask='auto')
                c.drawString(390, y - 15, "Tarjeta de Circulación")
        except: pass

        c.showPage()

    c.save()
