import tkinter as tk
from bs4 import BeautifulSoup
import requests
#==============Global Vars================#
main = tk.Tk(screenName = None, baseName = None, className = 'WikiNews', useTk = 1)
page = requests.get("https://en.wikipedia.org/wiki/Special:Random")
soup = BeautifulSoup(page.content,'html.parser')
textTopic = "Topic:"
textBody = ""
Topic = tk.Message(main,aspect = 900,text = textTopic, justify = tk.CENTER)
Body = tk.Label(main,anchor = tk.NW, height = 50, width = 200,bg = '#00ffff',text = textBody, wraplength = 1600,justify = tk.LEFT)
#=========================================#

def getNewSource():
    global page
    global soup
    global textTopic
    page = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(page.content,'html.parser')
    textTopic = "TOPIC: " + soup.title.string
    textTopic = textTopic[0:textTopic.find("- Wikipedia")]
    Topic.config(text = textTopic)
    print(textTopic)
    textBody = ""
    for data in soup.find_all('p'):
        #print(data.getText())
        textBody+= data.getText() + "\n"
    Body.config(text = textBody)

def getBody():
    global page
    soupy = BeautifulSoup(page.content,'html.parser')
    print(soup.p)

#Main window
#main = tk.Tk(screenName = None, baseName = None, className = 'WikiNews', useTk = 1) 

#Button
refreshRand = tk.Button(main,text = 'Refresh', width = 50, height = 5,command = lambda: getNewSource())

#Displays Topic
#Topic = tk.Message(main,aspect = 400, text = textTopic, justify = tk.CENTER)

#Body = tk.Message(main,aspect = 25, text = soup.p, justify =tk.CENTER) 

Topic.pack()
Body.pack()
refreshRand.pack()
main.mainloop()
