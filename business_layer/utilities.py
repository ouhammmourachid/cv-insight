from business_layer.tools.functions import *
from business_layer.tools.data_to_xlsx import data_to_xlsx
import smtplib
from tqdm import tqdm
import os
from PIL import Image
import cv2


def store_data_xl_dir(directory,competence):
    data=[['nom_complet','Email','tel','Adresse','Specialite','Experience professionelle','Formation','Competence','score']]
    d=[]
    for filename in tqdm(os.listdir(directory)):
        row=file_to_data(os.path.join(directory,filename))
        if row==0:
            continue
        s=scoring(row,competence)
        row.append(s)
        d.append(list(row))
        del row[-2]
        data.append(row)
    data_to_xlsx(data)
    return d

def store_data_xl_file(filename,competence):
    data=[['nom_complet','Email','tel','Adresse','Specialite','Experience professionelle','Formation','Competence','score']]
    d=[]
    row=file_to_data(filename)
    s=scoring(row,competence)
    row.append(s)
    d.append(list(row))
    del row[-2]
    data.append(row)
    data_to_xlsx(data)
    return d

def mail(recipient,full_name):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "Oussamahrita11@gmail.com"
    smtp_password = "jkhnlndmhgbgrded"

    sender = "Oussamahrita11@gmail.com"
    subject = "Acceptation de votre candidature"
    message="Cher "+full_name+" je suis ravi de vous informer que votre candidature pour le poste de a été retenue et que nous sommes heureux de vous accueillir dans notre entreprise.Nous avons été impressionnés par votre expérience professionnelle, vos compétences et vos qualités personnelles qui correspondent parfaitement à ce que nous recherchions pour ce poste.Votre contrat de travail sera envoyé par courrier électronique dans les prochains jours. Il contiendra toutes les informations nécessaires sur votre salaire, vos avantages sociaux et votre date d'entrée en fonction.Nous attendons avec impatience de travailler avec vous et de vous voir contribuer à notre succès. Si vous avez des questions ou des préoccupations, n'hésitez pas à me contacter par courrier électronique ou par téléphone."
    message = message.encode('utf-8')

    message = f"From: {sender}\nTo: {recipient}\nSubject: {subject}\n\n{message}"

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, recipient, message)

def array_to_img(arr,output_path):

    arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(arr)
    img.save(output_path)



