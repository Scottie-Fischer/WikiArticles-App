#import tkinters as tk
from tkinter import *
from bs4 import BeautifulSoup
import requests

#==============Global Vars================#
page = requests.get("https://en.wikipedia.org/wiki/Special:Random")
soup = BeautifulSoup(page.content,'html.parser')
topic_text = "Topic:"
body_text = ""
rand_url = "https://en.wikipedia.org/wiki/Special:Random"
search_url = rand_url
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

search_button = Button(search_frame, text = "Search", command = lambda: print(search_str.get()))
search_button.grid(row = 0, column = 2, sticky = 'nsew')

body_label = Text(body_frame,padx = 25, wrap = WORD)
body_label.grid(row = 0, column = 0, sticky = 'nsew')

refresh_button = Button(refresh_frame, text = 'refresh')
refresh_button.grid(row = 0, column = 0, sticky = 'nsew')
#=========================================================================#

#=============Helper Funcs================#
def getRandSource():
    global search_url
    global rand_url

    search_url = rand_url
    getNewSource()

def getNewSource():
    global page
    global soup
    global topic_text
    global search_url
    global rand_url

    error_str = "Other reasons this message may be displayed"

    #Check if the url is empty
    if(search_url == ""):
        search_url = rand_url
    
    #Use bs4 to scrape wikipedia
    page = requests.get(search_url) 
    soup = BeautifulSoup(page.content,'html.parser')
    topic_text = "TOPIC: " + soup.title.string
    topic_text = topic_text[0:topic_text.find("- Wikipedia")]
    topic_message.config(text = topic_text)
    body_text = ""

    #Increment over paragraphs to grab text data
    
    for data in soup.find_all(['h2','p']):
        if data.getText() != "Contents":

            if data.contents[0].name == 'span':
                body_text += "----" + data.getText().upper() + "----\n\n"
            else:
                body_text += data.getText() + "\n"
    
    body_label.delete('@0,0',END)

    #Check if the article actually exists
    if error_str in body_text:
        body_label.insert('@0,0',"Error: No Article for Search\nPlease Try Something Else")
    else:
        body_label.insert('@0,0',body_text)    #print new entry

def newSearch():
    global page
    global soup
    global topic_text
    global search_url
    
    #Get Search String from Entry
    search_text = search_entry.get()
    #Change it to fit format wikipedia wants
    search_text = search_text.replace(" ","_")
    #Iterate Over URL to change lower case to uppercase
    counter = 0
    search_url = ""
    while counter <  len(search_text):
        if(search_text[counter] == "_"):
            search_url += "_" + search_text[counter+1].upper()
            counter +=2
        else:
            search_url += search_text[counter]
            counter+=1
    
    search_url = "https://en.wikipedia.org/wiki/" + search_url
    #Call Func to scrape wikipedia
    getNewSource()


#Update Refresh Button to have getNewSource() func as command
refresh_button.configure(command = getRandSource)
#Update Search Button to have newSearch() func as command
search_button.configure(command = newSearch)

root.mainloop()
