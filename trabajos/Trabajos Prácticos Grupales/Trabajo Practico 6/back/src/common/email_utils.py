import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os import getenv
from src.common.persistance.models import Reserva


# --- Carga de Configuración de Entorno ---
SMTP_SERVER = getenv("SMTP_SERVER")
SMTP_PORT = int(getenv("SMTP_PORT", 587))
SMTP_USERNAME = getenv("SMTP_USERNAME")
SMTP_PASSWORD = getenv("SMTP_PASSWORD")
SENDER_EMAIL = getenv("SENDER_EMAIL")

def send_ticket_email(recipient_email: str, reserva: "Reserva"):
    """
    Simula la creación y envío de un email con las entradas (tickets) de la reserva.
    """
    if not all([SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL]):
        print("\n--- ERROR DE CONFIGURACIÓN DE EMAIL ---")
        print("Variables SMTP no definidas. Simulando envío de email.")
        print(f"SIMULACIÓN: Email de entradas enviado a {recipient_email} para Reserva ID {reserva.id}")
        return

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = f"¡Tus entradas de Eco Harmony Park para la Reserva ID {reserva.id}!"

    if reserva.tipo_pago == "efectivo":
        pago_info = "Forma de Pago: Efectivo"
        pago_monto = f"Total a Pagar: ${reserva.total_monto():.2f} (abonar al ingresar al parque)"
    else:
        pago_info = "Forma de Pago: Tarjeta"
        pago_monto = f"Total Pagado: ${reserva.total_monto():.2f}"

    # 1. Cuerpo del Correo
    body = f"""
    Estimado/a cliente,

    ¡Gracias por tu compra! Adjunto encontrarás tus entradas (tickets) para el parque.

    Detalles de la Reserva:
    - ID: {reserva.id}
    - Fecha: {reserva.fecha}
    - Cantidad de Entradas: {len(reserva.visitantes)}
    - {pago_info}
    - {pago_monto}

    ¡Disfruta tu visita!
    """
    msg.attach(MIMEText(body, 'plain'))

    # 2. Simulación de Entradas/Tickets Adjuntos
    # En un caso real, aquí generarías un PDF con los códigos QR o detalles.
    '''# FALTA IMPLEMENTAR ESTA PARTE
    

    
    '''

    visitantes_info = "\n".join(
        [f" - Visitante {i+1}: Edad {v.edad}, Tipo Entrada {v.tipo_entrada}, Monto {v.monto_final:.2f}" for i, v in enumerate(reserva.visitantes)]
    )

    ticket_content = f"Entrada para Reserva ID {reserva.id}\n\nDetalles de los Visitantes:\n{visitantes_info}"

    ticket_part = MIMEApplication(ticket_content.encode('utf-8'), _subtype="txt")
    ticket_part.add_header('Content-Disposition', 'attachment', filename=f"Entradas_Reserva_{reserva.id}.txt")
    msg.attach(ticket_part)
    
    # 3. Envío
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Habilitar seguridad TLS
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        print(f"REAL: Email de entradas enviado exitosamente a {recipient_email}.")
    except Exception as e:
        print(f"ERROR: No se pudo enviar el email a {recipient_email}. Error: {e}")
