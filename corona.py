import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import psutil
import pyjokes
import os
import pyautogui
import json
import requests
import wolframalpha
import time

corona = pyttsx3.init()
Voices = corona.getProperty('voices')
voice_id = Voices[1].id
corona.setProperty('voice',voice_id)
corona.setProperty('rate',190)
wolframalpha_app_id = 'AKXGHE-TH8HRQ233A'

def speech(content): # function for the assistant speak
    corona.say(content)
    corona.runAndWait()

def say_time(): # function for saying time
    time = datetime.datetime.now().strftime("%H:%M")
    speech("it is")
    speech(time)

def say_date():
    
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year 
    date = datetime.datetime.now().day
    speech("Today's date is")
    speech(date)
    speech(month)
    speech(year)

def intro():
    speech('Okaa eri  maiarasan!')
    say_date()
    say_time()

    hour = datetime.datetime.now().hour

    if hour > 6 and hour < 12:
        speech("O hai yo ")
    elif hour >=12 and hour <16:
        speech("kon nichiva")
    elif hour >=16 and hour <22:
        speech("kon bunva")
    else:
        speech ('Oya sumi')

def getCommand():
    rec = sr.Recognizer()
    with sr.Microphone() as mic:
        speech('listening')
        print("Listening......")
        rec.pause_threshold = 1
        content = rec.listen(mic)
    
    try:
        print("Recognizing.....")
        command = rec.recognize_google(content,language="en-US")
        print(command)
    
    except Exception as ex:
        print(ex)
        speech("Can't get u please repeat")
        print("Can't get u please repeat.........")
        return "None"
    return command

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()

    server.login('projects.mei.407@gmail.com','Amater$u')
    server.sendmail('projects.mei.407@gmail.com',to,content)
    server.close()

def cpu():
    usage = str(psutil.cpu_percent())
    speech('CPU is at'+usage) 

    battery = psutil.sensors_battery()
    speech('Available battery percentage ')
    speech(battery.percent)

def joke():
    speech(pyjokes.get_joke())

def scrsht():
    img = pyautogui.screenshot()
    img.save('C:/Users/scrsht.png')


if __name__ == "__main__":
    intro()

    while True:
        command = getCommand().lower() # lower is used for uniformity

        if 'wikipedia' in command:
            speech('searching.....')
            command = command.replace('wikipedia','')
            result = wikipedia.summary( command , sentences = 3 )
            speech("As in wikipedia")
            print(result)
            speech(result)

        elif 'time' in command:
            say_time()

        elif 'date' in command:
            say_date()

        elif 'send a mail' in command:
            try:
                speech('What is the context of the mail?')
                content = getCommand()
                to = input("Enter the receiver mail")
                sendEmail(to,content)
                speech(content)
                speech('The has been posted successfully')

            except Exception as e:
                print(e)
                speech('Sorry for the trouble. I am facing an error')

        elif 'chrome' in command:
            speech('What should I search?')
            chromepath = 'C: /Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            search = getCommand().lower()
            wb.get(chromepath).open_new_tab(search+'.com')

        elif 'youtube' in command:
            speech('What is your interest today?')
            search = getCommand().lower()
            speech('All the way to youtube!')
            wb.open("https://www.youtube.com/results?search_query="+search)

        elif 'google' in command:
            speech('What should i search for?')
            search = getCommand().lower()
            speech("Here is what i got")
            wb.open("https://www.google.com/results?search_q="+search)

        elif 'cpu' in command:
            cpu()

        elif 'joke' in command:
            joke()

        elif 'word document' in  command:
            speech('Opening MS word......')
            ms_word = r'C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE'
            os.startfile(ms_word)
        
        elif 'write a note' in command:
            speech('I am on it. Started recording.....')
            notes = getCommand()
            file = open('notes.txt','w')
            file.write(datetime.date.today())
            file.write(':- \n')
            file.write(notes)
            speech('The notes have been recorded')

        elif 'show notes' in command:
            speech('showing notes...')
            file = open('notes.txt','r')
            print(file.read())
            speech(file.read())

        elif 'screenshot' in command:
            scrsht()
            speech('Screenshot taken')

        elif 'remember that' in command:
            speech('What should I record')
            mem = getCommand()
            speech('This is what i got'+mem)
            remember = open('memory.txt','w')
            remember.write(mem)
            remember.close()
            
        elif 'do you remember anything' in command:
            remember = open('memory.txt','r')
            speech("Here's what i recorded "+remember.read())

        elif 'go offline' in command:
            speech('I am taking a leave, take care')
            quit()
        
        elif 'where is' in command:
            command = command.replace('where is','')
            speech('Location found at ')
            wb.open_new_tab('https://www/google.com/maps/place/'+command)

        elif 'calculate' in command:
            client = wolframalpha.Client(wolframalpha_app_id)
            ind = command.lower().split().index('calculate')
            command = command.split()[ind + 1:]
            res = client.query(''.join(command))
            answer = next(res.results)
            print(answer)
            speech('The answer is '+answer)
            
        elif 'stop listeneing' in command:
            speech('For how long should i hold?')
            tim = int(getCommand())
            time.sleep(tim)
            print(tim)

        elif 'logout' in command:
            os.system('shutdown -l')
        
        elif 'restart' in command:
            os.system('shutdown /r /t 1')

        elif 'shutdown' in command:
            os.system('shutdown /l /t 1')
