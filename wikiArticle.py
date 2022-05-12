#import tkinters as tk
from tkinter import *
from bs4 import BeautifulSoup
import requests

#==============Global Vars================#
page = requests.get("https://en.wikipedia.org/wiki/Special:Random")
soup = BeautifulSoup(page.content,'html.parser')
topic_text = "Topic:"
body_text = ""
#==============Frame Setup================#
root = Tk(className = 'wikiNews', useTk = 1)
root.geometry('1280x720')

#Tkinter's String Var for Entry Widget
search_str = StringVar()
search_str.set("Search Here") #default text

#Configuring Root Row/Col
root.grid_rowconfigure(0,weight=0)  #This is for Search
root.grid_rowconfigure(1,weight=0)  #This is for Topic
root.grid_rowconfigure(2,weight=1)  #This is for Body
root.grid_rowconfigure(3,weight=0)  #This is for button
root.grid_columnconfigure(0,weight=1)
root.grid_columnconfigure(1,weight=1)
root.grid_columnconfigure(2,weight=1)

#Frame for Search Widgets
search_frame = Frame(root,bg = 'black',width = 50, height = 75)
search_frame.grid(row = 0, column = 0, columnspan = 3, sticky = 'nsew')
#Config Search Frame's Grid
search_frame.grid_rowconfigure(0,weight=1)
search_frame.grid_columnconfigure(0,weight=1)
search_frame.grid_columnconfigure(1,weight=1)
search_frame.grid_columnconfigure(2,weight=1)

#Frame for Topic Widget
topic_frame = Frame(root,bg='',width = 100, height = 75)
topic_frame.grid(row = 1, column = 0, columnspan = 3, sticky = 'nsew')
topic_frame.grid_columnconfigure(0,weight=1) #Config this frame's grid

#Frame for the Body of Text
body_frame = Frame(root,bg='pink',width = 50, height = 100)
body_frame.grid(row = 2, column = 0, columnspan = 3, sticky = 'nsew')
#Config Body Frame's Grid
body_frame.grid_rowconfigure(0,weight = 1)
body_frame.grid_columnconfigure(0,weight = 1)

#Frame for the Refresh Button
refresh_frame = Frame(root,bg='white',width = 50, height = 75)
refresh_frame.grid(row = 3, column = 0, columnspan = 3, sticky = 'nsew')
#Config Refresh Frame's Grid
refresh_frame.grid_columnconfigure(0, weight = 1)

#=========================================================================#
#==============Widgets====================#

topic_message = Message(topic_frame, text = "Topic",width = 700, justify = CENTER)
topic_message.grid(row = 0, column = 0, sticky='nsew')

search_entry = Entry(search_frame,textvariable = search_str)
search_entry.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew')

search_but = Button(search_frame, text = "Search", command = lambda: print(search_str.get()))
search_but.grid(row = 0, column = 2, sticky = 'nsew')

body_label = Text(body_frame,padx = 25, wrap = WORD)
body_label.grid(row = 0, column = 0, sticky = 'nsew')

refresh_button = Button(refresh_frame, text = 'refresh')
refresh_button.grid(row = 0, column = 0, sticky = 'nsew')
#=========================================================================#

#==============Global Vars================#
#ScrollBar = tk.Scrollbar(main, orient = 'vertical', command = Body.yview)
#Body.config(yscrollcommand = ScrollBar.set)

#=========================================================================#

#=============Helper Funcs================#
def getNewSource():
    global page
    global soup
    global textTopic
    page = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(page.content,'html.parser')
    topic_text = "TOPIC: " + soup.title.string
    topic_text = topic_text[0:topic_text.find("- Wikipedia")]
    topic_message.config(text = topic_text)
    print(topic_text)
    body_text = ""
    for data in soup.find_all('p'):
        body_text += data.getText() + "\n"

    body_label.delete('@0,0',CURRENT)  #delete previous entry
    body_label.insert('@0,0',body_text)    #print new entry



#========================================================================#

#Update Refresh Button to have getNewSource() func as command
refresh_button.configure(command = getNewSource)

root.mainloop()
