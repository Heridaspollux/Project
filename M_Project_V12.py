#!/usr/bin/env python
# coding: utf-8

# <h1 style="text-align: center">Competency Extraction from volunteer tasks and courses</h1>
# 
# <h2 style="text-align: center">Author: Hadi Sanaei</h2>
# 
# <h3 style="text-align: center">Supervisor: a.Univ.-Prof. Dr. Birgit Pröll</h3>
# 
# 

# In[1]:


import anvil.server

anvil.server.connect("server_3SUK256NKX6HGLZ2K7LDOLK6-ZS2CYIENMKWQIRXE")


# In[2]:


# #install library

# !pip3 install pdfplumber
# !pip3 install PyPDF2
# !pip3 install pandas  
# !pip3 install nltk
# !pip3 install regex
# !pip3 install matplotlib
# !pip3 install networkx
# !pip3 install tk
# !pip3 install pandastable
# !pip3 install numpy 
# !pip3 install pdfrw 
# !pip3 install requires.io
# !pip3 install pdfminer
# !pip3 install plotly
# !pip3 install geocoder
# !pip3 install pycopy-webbrowser
# !pip3 install urllib3
# !pip3 install pdf2image 
# !pip3 install Pillow


# In[3]:


# import packages

import pdfplumber
import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader
import pandas as pd  
import nltk, re
import matplotlib.pyplot as plt
import networkx as nx
from tkinter import *
from tkinter import ttk
from pandastable import Table, TableModel
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from pdfrw import PdfReader, PdfWriter
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import plotly.express as px
import geocoder
import webbrowser
from urllib.parse import quote
from pdf2image import convert_from_path
from PIL import ImageTk, Image
import os


# In[4]:


# open the pdf file
data = PyPDF2.PdfFileReader("BP_RK21.pdf")

# get number of pages
NumPages = data.getNumPages()
NumPages


# In[5]:


# Delete the pdf pages and save them in a new pdf file
def delPdf_page(pdfName, pdfNew_Name, pages):
    infile = PdfFileReader(pdfName, 'rb')
    outfile = PdfFileWriter()

    for i in range(infile.getNumPages()):
        if i not in pages:
            p = infile.getPage(i)
            outfile.addPage(p)

    with open(pdfNew_Name, 'wb') as f:
        outfile.write(f)
        
        
# Find string and return the pages that do not consist it
def find_string(pdfName, string):
    infile = PdfFileReader(pdfName, 'rb')
    delpages = []
    NumPages = infile.getNumPages()
    # extract text and do the search
    for i in range(0, NumPages):
        PdfPage = infile.getPage(i)
        Text = PdfPage.extractText() 
        if string not in Text:
            delpages.append(i)

    return delpages


# In[6]:


delPdf_page("BP_RK21.pdf", "pdfNew.pdf", find_string("BP_RK21.pdf", "Dauer"))

# open the pdf file
NewData = PyPDF2.PdfFileReader("pdfNew.pdf")

# get number of pages
NumPages = NewData.getNumPages()
NumPages


# In[7]:


def ge_to_en(text):                
    german_word=['ä','Ä','ü','Ü','ö','Ö','ß']
    for i in german_word:
        if i == 'ä':
            search_text = ("ä")
            replace_text = "ae"
            text = re.sub(search_text, replace_text, text)           

        elif i == 'Ä':
            search_text = ("Ä")
            replace_text = "AE"
            text = re.sub(search_text, replace_text, text)           

        elif i == 'ö':
            search_text = ("ö")
            replace_text = "oe"
            text = re.sub(search_text, replace_text, text)           

        elif i == 'Ö':
            search_text = ("Ö")
            replace_text = "OE"
            text = re.sub(search_text, replace_text, text)

        elif i == 'ü':
            search_text = ("ü")
            replace_text = "ue"
            text = re.sub(search_text, replace_text, text)

        elif i == 'Ü':
            search_text = ("Ü")
            replace_text = "UE"
            text = re.sub(search_text, replace_text, text)

        elif i == 'ß':
            search_text = ("ß")
            replace_text = "ss"
            text = re.sub(search_text, replace_text, text)

    return text


# In[8]:


#Convert pdf content to Text file
with pdfplumber.open("BP_RK21.pdf") as p:
    data = open("Pdf_Text.text", "w")
    for i in range(4,9):
        page = p.pages[i]
        text_data = (page.extract_text())
        text_data = ge_to_en(text_data)
        #print(text_data)
        data.write(text_data)
        

    data.close()


# In[9]:


def delete_lines(file_path, line_numbers):
    # Open the file and read all the lines into a list
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove the lines with the specified line numbers
    updated_lines = [line for i, line in enumerate(lines) if i+1 not in line_numbers]

    # Open the file in write mode and write the updated lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

file_path = "Pdf_Text.text"  
lines_to_delete = [2, 3,7,12,13,14,16]   # Specify the line numbers to delete

delete_lines(file_path, lines_to_delete)


# In[10]:


#Check the string is integer or not
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


# In[11]:


#Clean Text file
new_l = []
title = []
page_num = []
with open('Pdf_Text.text') as f:
    s = f.read()
lines = re.findall(r'[^\n]+\n+', s)
#print(lines)
for line in lines:
    new_l=line.replace('.', ' ')
    #print(new_l)
    len_line = len(new_l)
    page_Index=len_line-5
    #print(page_Index)
    if line == 'INHALTSVERZEICHNIS\n':
        continue
    else:
        rest_list = []

        if RepresentsInt(new_l[page_Index:-1]) == True and not rest_list:
            title.append(new_l[:page_Index+1])
            page_num.append(new_l[page_Index:-1])

            
        if RepresentsInt(new_l[page_Index:-1]) == True and rest_list:
            new_l+=rest_list
            title.append(new_l[:page_Index+1])
            page_num.append(new_l[page_Index:-1])

        
        if RepresentsInt(new_l[page_Index:-1]) == False:
            rest_list = new_l
    


# In[12]:


#Assign data of lists.  
data = {'Title': title, 'Page': page_num}  

#Create DataFrame  
dflist = pd.DataFrame(data)  

#Show output
dflist.style.set_properties(**{'text-align': 'left'}).set_caption("INHALTSVERZEICHNIS")


# ####Graph#####

# In[13]:


A = 'NOTFALLSANITÄTER\n ÜBUNGSTAG'
B = 'Praktische\n Übungen\n ohne\n Patientenkontakt'
C = 'Gerätelehre\n und\n Sanitätstechnik'
D = 'D'

global dfgraph
dfgraph = pd.DataFrame({ 'from':[B ,C, A], 'to':[A, A, D]})


G = nx.from_pandas_edgelist(dfgraph, 'from', 'to', create_using=nx.DiGraph())
    
initialpos = {B: (0, 0), C: (0, 2), A: (1, 1), D: (2, 1)}
fig = plt.Figure(figsize=(5, 5), dpi=150)
ax = fig.add_subplot(111)
    
nx.draw(G, pos=initialpos, with_labels=True, node_size=2000,
        font_size=5, font_color="black", font_weight="bold", arrows=True, ax=ax)


# In[ ]:


class App(Tk):
   
    
    
    def __init__(self):
        
        super(App, self).__init__()
        self.title("BILDUNGS PROGRAMM 2021")
        self.minsize(750,800)


        
        tabControl = ttk.Notebook(self)
        
        self.tab2 = ttk.Frame(tabControl)
        tabControl.add(self.tab2, text = "Courses List")

        self.tab3 = ttk.Frame(tabControl)
        tabControl.add(self.tab3, text = "Termine")
        
        self.tab4 = ttk.Frame(tabControl)
        tabControl.add(self.tab4, text = "Voraussetzung")
        self.tab5 = ttk.Frame(tabControl)
        tabControl.add(self.tab5, text = "Mehr Details")     
        tabControl.pack(expand = 1, fill = "both")
        self.widgets()
        
    
    
    def callback(self):
        global coursename
        global page_course
        global readfile
        global dfcal
        coursename = cmb.get()
        np.random.seed(0)

        page_course = int(dflist[dflist['Title'] == coursename]["Page"])
        
        p2 = page_course+1
        
        pages = PdfReader('BP_RK21.pdf').pages
        #parts = [20]
        parts = [(page_course,p2)]

        for part in parts:
            outdata = PdfWriter('0.pdf')
            for pagenum in range(*part):
                outdata.addpage(pages[pagenum-1])
            outdata.write()

            
        def extract_text_from_pdf(pdf_path):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
    
            with open(pdf_path, 'rb') as fh:
                for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
                    page_interpreter.process_page(page)
            
                text = fake_file_handle.getvalue()
    
            # close open handles
            converter.close()
            fake_file_handle.close()
            
            if text:
                return text
    
        if __name__ == '__main__':
            data = open('0.txt', "w")
            data.write(extract_text_from_pdf('0.pdf'))
            data.close()
        
        
        # opening a text file
        file1 = open('0.txt', "r")
       
        # read file content
        readfile = file1.read()
        
        
        
       # initializing substrings
        sub1 = "Termin"
        sub2 = "Kurskosten"

        # getting index of substrings
        idx1 = readfile.index(sub1)
        idx2 = readfile.index(sub2)

        # length of substring 1 is added to
        # get string from next character
        res = readfile[idx1 + len(sub1) + 1: idx2] 
        
        
        mystring = ''.join(map(str,res))

        sp1 = ['Mo.','Di.','Mi.','Do.','Fr.','Sa.','So.']
        sp2 = ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag']

        day = []
        res = mystring.split()
        for x in res:
            for y in sp1:
                if y in x:
                    day.append(y)
            for y in sp2:   
                if y in x:
                    day.append(y)
        
        


        # The regex pattern that we created
        pattern1 = "\d{2}[/.]\d{2}[/.]\d{4}"
        pattern2 = "\d{2}[/.]\d{2}"


        # Will return all the strings that are matched
        sd1 = re.findall(pattern1, mystring)
        sd2 = re.findall(pattern2, mystring)


        if len(day) != len(sd1):
            start_dates = sd2
    
        else:
            start_dates = sd1
    
    
        finish_dates = start_dates 
        
        #global dfcal
        dfcal = pd.DataFrame({'Task':day,'Start':start_dates, 'Finish':finish_dates})
        dfcal
             
       
                
        
        
        #termin#################################################
        pt = Table(self.tab3, dataframe=dfcal, showtoolbar=True, showstatusbar=True)
        pt.show()
        
        

        #graph##################################################
        
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self.tab4)
        canvas.draw()
    
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, self.tab4)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
    

    
        #details################################################
    
    
  
        
        # Store Pdf with convert_from_path function
        photo = convert_from_path('0.pdf')

        for i in range(len(photo)):

             # Save pages as images in the pdf
            photo[i].save('0.jpg')
    

        bg = ImageTk.PhotoImage(file="0.jpg")
        # create canvas
        canvas = Canvas(self.tab5, width=500, height=500)
        canvas.pack(fill=BOTH, expand=True)
        # place the image inside canvas
        canvas.create_image(0, 0, image=bg, anchor='nw')
        # resize function for resizing the image
        # with proper width and height of root window
        
        def resize_bg(event):
            global bgg, resized, bg2
            # open image to resize it
            bgg = Image.open("0.jpg")
            # resize the image with width and height of root
            resized = bgg.resize((event.width, event.height),
                                 Image.Resampling.LANCZOS)
    
            bg2 = ImageTk.PhotoImage(resized)
            canvas.create_image(0, 0, image=bg2, anchor='nw')
        
        if __name__ == '__main__':
            self.tab5.bind("<Configure>", resize_bg)

        
     

    
    def map_course(self):
        # initializing substrings
        sub1 = "Ort"
        sub2 = "Refere"
        sub3 = "Kursleit"

        # getting index of substrings
        idx1 = readfile.index(sub1)
        if "Refere" in readfile:
            idx2 = readfile.index(sub2)
        elif "Kursleit" in readfile:
            idx2 = readfile.index(sub3)


        
        # length of substring 1 is added to
        # get string from next character
        res = readfile[idx1 + len(sub1): idx2]
        
        BING_KEY = 'AtS61KK6V9sFBumUvWrjnzhHfPoRDidhExTbDGxzOepBX7V-tgMeSxoIIbw8Y718'
        searchTerm = res
        g = geocoder.bing(searchTerm, key=BING_KEY)
        
        lat = g.json['lat']
        long = g.json['lng']
        
        zoomLevel = 1 # Show entire world
        url = f"https://www.bing.com/maps?cp={lat}~{long}&lvl={zoomLevel}&sp=point.{lat}_{long}_{quote(searchTerm)}"
        webbrowser.open_new(url)
        
  
    #json##################################################################        
    
    
    
    def json(self):
        global coursename
        global page_course
        global readfile
        global dfcal
        coursename = cmb.get()
        np.random.seed(0)
        
        

        # Creating a function to
        # replace the text
        def ge_to_en(text):                
            german_word=['ä','Ä','ü','Ü','ö','Ö','ß']
            for i in german_word:
                if i == 'ä':
                    search_text = ("ä")
                    replace_text = "ae"
                    text = re.sub(search_text, replace_text, text)           

                elif i == 'Ä':
                    search_text = ("Ä")
                    replace_text = "AE"
                    text = re.sub(search_text, replace_text, text)           

                elif i == 'ö':
                    search_text = ("ö")
                    replace_text = "oe"
                    text = re.sub(search_text, replace_text, text)           

                elif i == 'Ö':
                    search_text = ("Ö")
                    replace_text = "OE"
                    text = re.sub(search_text, replace_text, text)

                elif i == 'ü':
                    search_text = ("ü")
                    replace_text = "ue"
                    text = re.sub(search_text, replace_text, text)

                elif i == 'Ü':
                    search_text = ("Ü")
                    replace_text = "UE"
                    text = re.sub(search_text, replace_text, text)

                elif i == 'ß':
                    search_text = ("ß")
                    replace_text = "ss"
                    text = re.sub(search_text, replace_text, text)

            return text


        
    
        page_course = (dflist["Page"])
        #print(dflist)
        
        
        #res is the page number of titles
        res = [eval(i) for i in page_course]
        #print(res)
        
        
        #Convert pdf content to Text file
        with pdfplumber.open("BP_RK21.pdf") as p:
            jfile = open('json.txt', "w")
            js_list = dflist.to_json()
            jfile.write( js_list)
            

            for i in range(10,172):
                data = open("temp.txt", "w")
                page = p.pages[i]
                #print(page)
                text_data = (page.extract_text())
                #print(text_data)
                text_data = ge_to_en(text_data)
                data.write('\n\n newpage \n ')
                data.write(text_data)
                data.close()
                
                # opening a text file
                file1 = open('temp.txt', "r")
       
                # read file content
                readfile = file1.read()
            
                if page=='139':
                    continue
               
                # initializing substrings
                sub_newpage = "newpage"
                sub_dauer = "Dauer"

                # getting index of substrings
                idx_newpage = readfile.index(sub_newpage)
                word = "Dauer"             # input word to be searched
                if(word in readfile):  # check if word is present or not
                    idx_dauer = readfile.index(sub_dauer)
                else:
                    continue          
                

                # length of substring 1 is added to
                # get string from next character
                res_title = [readfile[idx_newpage + len(sub_newpage) + 1: idx_dauer]]
                df_title = pd.DataFrame(res_title, columns=['Title'])
                df_title = (df_title.loc[0])
                df_title = df_title.replace('\n',' ', regex=True)

  
               # initializing substrings
                sub1 = "Termin"
                sub2 = "Kurskosten"

               
                ## when in backgraound we have different words and date that due to noise in our extract(eg.p-25)
                if("TermineTermine" in readfile):  # check if word is present or not
                    continue 

                
                # getting index of substrings
                idx1 = readfile.index(sub1)
                idx2 = readfile.index(sub2)

                # length of substring 1 is added to
                # get string from next character
                res = readfile[idx1 + len(sub1) + 1: idx2] 


                mystring = ''.join(map(str,res))
                

                sp1 = ['Mo','Di','Mi','Do','Fr','Sa','So']
                sp2 = ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag']

                day = []
                res = mystring.split()
                for x in res:
                    if x == "Die":
                        continue
                    elif x == "Mitarbeiter":
                        continue
                    
                    for y in sp1:
                        if y in x:
                            day.append(y)
                    for y in sp2:   
                        if y in x:
                            #x = x.replace(y,'')
                            day.append(y)




                # The regex pattern that we created
                pattern1 = "\d{2}[/.]\d{2}[/.]\d{4}"
                pattern2 = "\d{2}[/.]\d{2}"


                # Will return all the strings that are matched
                sd1 = re.findall(pattern1, mystring)
                sd2 = re.findall(pattern2, mystring)
              
                if len(day) == 0 :
                     continue
                    
                if len(sd1) != len(sd2):
                    continue
                    
                if len(day) != len(sd1):
                    start_dates = sd2

                else:
                    start_dates = sd1
               

                finish_dates = start_dates 
               
                
                dfcal = pd.DataFrame({'Task':day,'Start':start_dates, 'Finish':finish_dates})
                dfcal
                
                
                sub_ort = "Ort"

                for line in file1:
                    if "Ort " in line:
                        # go to the next line and initialize list elements
                        data_ort = [next(file1)]
                        # Create the pandas DataFrame with column name is provided explicitly
                        df_ort = pd.DataFrame(data_ort, columns=['Ort'])
                        df_ort = (df_ort.loc[0])
                        df_ort = df_ort.replace('\n',' ', regex=True)


                js_cal = dfcal.to_json()
                js_title = df_title.to_json()

                # Append text at the end of file
                jfile.write('\n\n')
                jfile.write(js_title)
                jfile.write("\n")
                jfile.write(js_cal)
                jfile.write("\n")

            

            os.remove("temp.txt")

                
            jfile.close()    

    
    def reload_window(self):
        # Destroy the existing Tkinter window
        app.destroy()
    
        # Create a new Tkinter window
        App()
    
     

    
    def widgets(self):
        
        l1=Label(self.tab2,text="Courses list")
        l1.grid(column=0, row=0)
        
        # Constructing the first frame, frame1
        frame1 = LabelFrame(self.tab2, text="List", fg="Black", padx=15, pady=15)
        # Displaying the frame1 in row 0 and column 0
        frame1.grid(row=0, column=0)
       
        frame2 = LabelFrame(self.tab2, text="Content", padx=15, pady=15)

        # Displaying the frame2 in row 0 and column 1
        frame2.grid(row=0, column=1)
    
        pt = Table(frame2, dataframe=dflist,showtoolbar=True, showstatusbar=True)
        pt.show()
        
        
        
        global cmb
        cmb=ttk.Combobox(frame1,values=title,width=30)
        cmb.grid(column=0, row=1)
        cmb.current(0)
        
        
        mapButton=Button(frame1,text="Show_Map",command= self.map_course)
        mapButton.grid(column=0, row=3)
        
        detailsButton=Button(frame1,text="  Show_Details  ",command=self.callback)
        detailsButton.grid(column=0, row=6)
        
        detailsButton=Button(frame1,text="  Create_JSON_File  ",command=self.json)
        detailsButton.grid(column=0, row=9)
        
        detailsButton = Button(frame1, text="Reload for Mehr Details", command=self.reload_window)
        detailsButton.grid(column=0, row=12)

        
               
    
    
        

app = App()
app.mainloop()


# In[ ]:





# In[ ]:




