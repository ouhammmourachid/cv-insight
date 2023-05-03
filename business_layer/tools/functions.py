import openai
import json
from business_layer.tools.pdf_to_text import pdf_to_text
import cv2
from business_layer.tools.pdf_to_img import pdf_to_img
import os

def ChatGPT_conversation(conversation):
    with open('business_layer/tools/key_openai.txt','r') as file:
        API_KEY=file.read()
    openai.api_key=API_KEY
    model_id='gpt-3.5-turbo'
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    
    return conversation

def get_data(text):
    conversation = []
    with open('business_layer/tools/q.txt','r') as file:
        q=file.read()
    conversation.append({'role': 'system', 'content': q+'\n'+text})
    conversation = ChatGPT_conversation(conversation)
    text=conversation[-1]['content']
    text=text.replace('\n',"")
    list=json.loads(text)
    return list


def file_to_data(pdf_file):
    n=0
    data=[]
    text=pdf_to_text(pdf_file)
    while(n<=1):
        try:
            list=get_data(text)
            n=5
        except Exception as e:
            if(n==2):
                print("we can't treat this cv")
                return 0
            n+=1

    try:
                a=""
                b=""
                c=""
                d=cutImage(pdf_file)
                for i in list[5]:
                    if i==None:
                          continue
                    a+=i+","
                for j in list[6]:
                    if j==None:
                          continue
                    b+=j+","
                for k in list[7]:
                    if k==None:
                          continue
                    c+=k+","
                
                data.append(list[0])
                data.append(list[1])
                data.append(list[2])
                data.append(list[3])
                data.append(list[4])
                data.append(a)
                data.append(b)
                data.append(c)
                data.append(d)
    except Exception as e:
                return 0
    return data

def scoring(x,competence):
    competence=competence.lower()
    ma_chaine = x[7].lower()
    mon_tableau = ma_chaine.split(",")
    competences = competence.split(",")
    compteur = 0
    for element in mon_tableau:
        if element in competences:
            compteur += 1
    score = compteur * 100 / len(competences)
    return score

def cutImage(pdf_path):
    output_path='business_layer/cvs/Images/img0.jpg'
    pdf_to_img(pdf_path,output_path)
    img = cv2.imread(output_path)
    face_cascade = cv2.CascadeClassifier('business_layer/tools/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 1:
        x, y, w, h = faces[0]
        face = img[y-20:y+h+10, x:x+w+2]
    if(os.path.exists(output_path)):
        os.remove(output_path)
    return face
