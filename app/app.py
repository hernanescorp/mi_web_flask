from flask import Flask, render_template, request, redirect
import mysql.connector
from email.message import EmailMessage
import smtplib
import ssl

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': '172.17.0.1',
    'user': 'hernan',
    'password': 'Cristiano8_',
    'database': 'graxiano'
}

# Función para enviar el correo de notificación
def enviar_correo_contacto(nombre, email, telefono, empresa, mensaje):
    email_sender = 'hernan081097@gmail.com'
    email_password = 'rtoa yabv sqsd aqbr'
    email_receiver = 'hernanescorp@gmail.com'

    subject = f"📬 Nuevo contacto desde Graxiano: {nombre}"
    body = f"""
    Se ha recibido un nuevo mensaje desde el formulario de contacto:

    🧑 Nombre: {nombre}
    📧 Email: {email}
    📱 Teléfono: {telefono}
    🏢 Empresa: {empresa}
    💬 Mensaje:
    {mensaje}

    Saludos,
    Sitio Web Graxiano
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls(context=context)
            smtp.login(email_sender, email_password)
            smtp.send_message(em)
            print("✅ Correo enviado correctamente.")
    except Exception as e:
        print("❌ Error al enviar correo:", e)

# Rutas
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hernan')
def hernan():
    return render_template('hernan.html')

@app.route('/graxiano')
def graxiano():
    return render_template('graxiano.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        empresa = request.form['empresa']
        mensaje = request.form['mensaje']

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clientes_potenciales (nombre, email, telefono, empresa, mensaje)
                VALUES (%s, %s, %s, %s, %s)
            """, (nombre, email, telefono, empresa, mensaje))
            conn.commit()
            cursor.close()
            conn.close()

            # Enviar correo
            enviar_correo_contacto(nombre, email, telefono, empresa, mensaje)

            return redirect('/contacto?exito=1')
        except Exception as e:
            print("❌ Error al guardar:", e)
            return redirect('/contacto?error=1')

    return render_template('contacto.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
