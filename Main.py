# requests 
import requests

# tkinter 
from tkinter import *
import tkinter as tk
from tkinter import filedialog,messagebox

# selenium 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# pharse path 
from pathlib import Path

# waiting a link text appears 
def linkText(driver,value):
    element = driver.find_element_by_id("link0")
    if value in element.text:
        return False
    else:
        return element.text

# GUI START     
def widgets():

    labelLink = Label(root,text="SLIDE SHARE LINK    :",bg="brown4",fg="chocolate1",font=("arial",11,"bold"))
    labelLink.grid(row=1,column=0,pady=6,padx=5)

    # input link slide share which want download pdf
    root.linkText = Entry(root,bd=4,width=55,textvariable=slideShareLink,fg="chocolate2",font=("arial",11,"italic","bold"),bg="cornsilk3")
    root.linkText.grid(row=1,column=1,pady=6,padx=10,columnspan=2)

    destinationLable = Label(root,text="DESTINATION             :",bg="brown4",fg="chocolate1",font=("arial",11,"bold"),width = 18)
    destinationLable.grid(row=2,column=0,pady=6,padx=5)

    root.destinationPath = Entry(root,bd=4,width=38,textvariable=downloadPath,fg="chocolate2",font=("arial",11,"italic","bold"),bg="cornsilk3")
    root.destinationPath.grid(row=2,column=1,pady=6,padx=10)

    browseButton = Button(root,text="BROWSE",width=15,bg="cornsilk3",activebackground="cornsilk3",command=browse) 
    browseButton.grid(row=2,column=2,pady=6,padx=10,columnspan=2)

    downloadButton = Button(root,text="DOWNLOAD PDF",width=30,bg="cornsilk3",activebackground="cornsilk3",command=download) 
    downloadButton.grid(row=3,column=1,pady=6,padx=10)

def browse():
    # Auto capture home path
    home = str(Path.home())
    # set directory pop up spawn , initiraldir itu optional itu adalah spawn pop up
    dwnldDirectory = filedialog.askdirectory(initialdir=home+"\Downloads")
    downloadPath.set(dwnldDirectory)

def download():
    try:
        # driver = webdriver.PhantomJS(executable_path=(str(Path.cwd())+r"\phantomjs-2.1.1-windows\bin\phantomjs.exe"))
        caps = DesiredCapabilities.PHANTOMJS 
        caps["phantomjs.page.settings.userAgent"] = ""
        driver = webdriver.PhantomJS(desired_capabilities=caps)
        
    except Exception as e: 
        messagebox.showerror(e,"Please Dont Delete, File Name PhantomJS !")
    # https://www.slideshare.net/secret/rMQvaTumPTtSiM --> contoh link 
    driver.get(f'https://simply-debrid.com/generate?link="{slideShareLink.get()}#submit2"')
    
    # pakai lambda karna webdriver hanya bisa membaca sebuah objek tidak bisa membaca sebuah fungsi
        # alternatifnya pakai class, karna class itu object
            # class link_text(object):
            #     def __init__(self,value):        
            #         self.value = value
            #     def __call__(self,driver):        
            #         locator = driver.find_element_by_id("link0").text
            #         if self.value in locator:
            #             return False
            #         else:
            #             return locator
            # linkPdf = WebDriverWait(driver,1).until(link_text("Generation in progress..."))
    
    linkPdf = WebDriverWait(driver,1).until(lambda x: linkText(driver,"Generation in progress...")) 
    print(linkPdf)
    driver.close()
    # url link
    url = linkPdf
    
    # capture name file 
    if url.find("/"):
        nameFile = url.rsplit("/",1)[1]
    else:
        nameFile = input("name file >> ") + ".pdf"

    # download pdf 
    filePdf = requests.get(url,allow_redirects = True)

    # save the file pdf , make spesifik name and path file
    root.update()
    open(downloadPath.get() + "/" +  nameFile,"wb").write(filePdf.content)
    # display the pdf success download
    messagebox.showinfo("SUCCESS","DOWNLOAD PDF FROM SLIDE SHARE")
    # check if want to quit from program
    checkQuit = messagebox.askyesno("QUIT","QUIT FROM PROGRAM ?")
    if checkQuit:
        root.destroy()
    
    
if __name__ == "__main__":
    # create tk object
    root = tk.Tk()   
    # make size pop up  width x hight / lebar x panjang
    root.geometry("650x120")
    # make sure user can't maximaze 
    root.resizable(False,False)
    # title of pop up
    root.title("SlideHere-Pdf")
    # makin tinggi makin dark
    root.config(background="brown4") 

    # variable for each entry: sildeShareLink and downloadButton
    # berguna untuk get and set isinya di setiap fungsi yang berbeda
    slideShareLink = StringVar()
    downloadPath = StringVar()

    widgets()
    root.mainloop()