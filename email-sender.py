import smtplib, ssl , mimetypes
from email.message import EmailMessage
from pathlib import Path
import time
import random
import socket
_orig_getaddrinfo = socket.getaddrinfo
def _ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _ipv4_getaddrinfo
list = []
file = Path("file.pdf")
cv = Path("cv.pdf")
my_mail = input("[$] Enter your email :")
MDP = input("[$] Enter your password :")
subject = input("[$] Enter the subject of your mail :")
body = ""

def mail_sender():
    context = ssl.create_default_context()
    for mail in list:
        msg = EmailMessage()
        msg["From"] = my_mail
        msg["To"] = mail
        msg["Subject"] = subject
        msg.set_content(body)
        if cv.is_file():
            ctype, encoding = mimetypes.guess_type(cv)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"
            maintype, subtype = ctype.split("/", 1)
            with open(cv, "rb") as f :
                msg.add_attachment(
                    f.read(),
                    maintype=maintype,
                    subtype=subtype,
                    filename=cv.name
                )
        else:
            print("Problème avec le fichier")
        if file.is_file():
            ctype, encoding = mimetypes.guess_type(file.name)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"
            maintype, subtype = ctype.split("/", 1)
            with open(file, "rb") as f :
                msg.add_attachment(
                    f.read(),
                    maintype=maintype,
                    subtype=subtype,
                    filename=file.name
                )
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(my_mail, MDP)
                server.send_message(msg)
                print(f"✅ Email envoyé à {mail} avec succès !")
                delai = random.randint(10,40)
                print(f"⌛ Attente de {delai} secondes...")
                time.sleep(delai)
        except Exception as e:
            print(f"❌ Erreur pour {mail}: {e}")
if __name__ == "__main__":
    mail_sender()