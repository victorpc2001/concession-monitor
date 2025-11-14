import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Código de concesión
CODIGO_CONCESION = "010220524"

# URL objetivo de INGEMMET
URL = f"https://www.ingemmet.gob.pe/consultas/concesiones/{CODIGO_CONCESION}"

# Correo destinatario (TU correo)
TO_EMAIL = "andree.29.julio@gmail.com"

# Correo emisor genérico del sistema
FROM_EMAIL = "alertas.concesiones.system@gmail.com"
SMTP_USER = "alertas.concesiones.system@gmail.com"
SMTP_PASS = "ALERTA12345678"   # funciona sólo para envío básico

def enviar_alerta(mensaje):
    msg = MIMEMultipart()
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = "⚠️ ALERTA: Cambio en concesión minera INGEMMET"

    msg.attach(MIMEText(mensaje, "plain"))

    try:
        server = smtplib.SMTP("smtp-relay.brevo.com", 587)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        print("Correo enviado exitosamente.")
    except Exception as e:
        print("ERROR enviando correo:", e)

def obtener_estado():
    try:
        r = requests.get(URL, timeout=15)
        contenido = r.text.lower()

        if "vigente" in contenido:
            return "VIGENTE"
        if "cancelado" in contenido or "caducado" in contenido:
            return "CADUCADO"

        return "DESCONOCIDO"

    except:
        return "ERROR"

def main():
    estado = obtener_estado()

    if estado in ["VIGENTE", "CADUCADO"]:
        mensaje = (
            f"El estado de la concesión {CODIGO_CONCESION} es: {estado}\n"
            f"URL: {URL}"
        )
        enviar_alerta(mensaje)
    else:
        print("No se envió correo porque no se detectó estado claro.")

if __name__ == "__main__":
    main()
