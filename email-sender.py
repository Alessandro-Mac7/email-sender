import email, smtplib, ssl
import csv

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = "Test email"
body = "Ciao {name}"
sender = input("Inserisci la tua email:")
password = input("Inserisci la password:")

# Crea e setta il MIME
mimeMessage = MIMEMultipart()
mimeMessage["From"] = sender
mimeMessage["Subject"] = subject

# Aggiungo il testo
mimeMessage.attach(MIMEText(body, "plain"))

filename = "document.pdf"  # Nome file, va inserito nella stessa cartella dello script

with open(filename, "rb") as attachment:
    mimeObject = MIMEBase("application", "octet-stream")
    mimeObject.set_payload(attachment.read())

# Encode file in ASCII
encoders.encode_base64(mimeObject)
mimeObject.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Aggiungo l'allegato convertito in stringa
mimeMessage.attach(mimeObject)
text = mimeMessage.as_string()

# Login in gmail e send dell'email, se l'autenticazione è a due fattore generare un password momentanea da 
# https://myaccount.google.com/apppasswords
# Altrimenti consentire l'Accesso app meno sicure da google
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender, password)
    with open("contacts.csv") as file:
        reader = csv.reader(file) # formato nome, email
        next(reader)  # Salta header
        for name, email in reader:
            server.sendmail(
                sender,
                email,
                text.format(name=name),
            )
