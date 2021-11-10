import os
import smtplib
import imghdr
from email.message import EmailMessage
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
from threading import Thread

font = ImageFont.truetype('arial.ttf',30)

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

def reshape(something):
    reshaped_text = arabic_reshaper.reshape(something)
    bidi_text = get_display(reshaped_text)
    return bidi_text

def generateCertificate(studentData):
    
        Emails = []
        Names = []

        Position, Name, Email, Id = studentData.strip().split(',')
        img = Image.open('samples/Certificate Image 3.jpeg')
        bidi_Position = reshape(Position)
        bidi_Name = reshape(Name)
        draw = ImageDraw.Draw(img)
        Emails += [Email]
        Names += [Name]
        xPosition, yPosition = (730, 300)
        xName, yName = (700, 300)
        xId, yId = (205, 300)
        wPosition, hPosition = draw.textsize(bidi_Position, font=font)
        wName, hName = draw.textsize(bidi_Name, font=font)
        wId, hId = draw.textsize(Id, font=font)
        draw.text(xy=(xPosition-wPosition, yPosition), text=f'{bidi_Position}', fill=(0,0,0), font=font)
        draw.text(xy=(xName-wName, yName), text=f'{bidi_Name}', fill=(0,0,0), font=font)
        draw.text(xy=(xId-wId, yId), text=f'{Id}', fill=(0,0,0), font=font)
        img_fname = f'{Names[i-1]} \'s Certificate.png'
        img.save(f'pictures/{img_fname}')
        return Emails, Names

with open('Data3.csv', 'r', encoding='UTF-8') as f:

    threads = []

    for i, studentData in enumerate(f):
        if i == 0: continue
        
        thread = Thread(target=generateCertificate, args=(studentData,))
        threads.append(thread)
        thread.start()
        
    for thread in threads: 
        thread.join() # wait for completion


def sendEmail():
    Names = []
    Emails = []
    Emails, Names = generateCertificate()
    i = 0
    for Email in Emails:
        img_fname = f'{Names[i]} \'s Certificate.png'
        msg = EmailMessage()
        msg['Subject'] = F'شهادة {Names[i]}'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = Email
        msg.set_content('')

        with open(f'pictures/{img_fname}', 'rb') as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name
        msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            smtp.send_message(msg)
        i += 1