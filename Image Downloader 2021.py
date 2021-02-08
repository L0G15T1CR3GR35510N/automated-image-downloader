from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import os.path
import urllib.request
import tkinter as tk
from tkinter import *
from tkinter import ttk

downloads_folder = ('/Users/simonjakobsson//Desktop/') # this is where you specify where you want the folder of downloaded images

window = tk.Tk() # A window is an instance of Tkinter’s Tk class.
window.title("Simon's automated image downloader") # This is the title of the window

frame1 = tk.Frame(master=window, height=30, bg="white") #this just adds some fill
frame2 = tk.Frame(master=window, height=40, bg="white") #this just adds some fill
frame3 = tk.Frame(master=window, height=30, bg="white") #this just adds some fill

### top label ###
top_label = tk.Label(
    text="This program downloads images \n to a folder on the desktop",
    font=('helvetica', 16, 'bold'),
    foreground="white",  # Set the text color
    background="#bbdffa",  # Set the background color to hex value (can also be written as fg/bg)
    width=50, # measured in text units - based on the "0" character, not pixels, so the output won't be square
    height=3
)
### the search box ###

class PlaceholderEntry(ttk.Entry):
    def __init__(self, container, query_entry, *args, **kwargs):
        super().__init__(container, *args, style="Placeholder.TEntry", foreground='#424242', font=('Helvetica', 14, 'bold'), width=50)
        self.placeholder = query_entry
        self.insert("0", self.placeholder)
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

    def _clear_placeholder(self, e):
        if self["style"] == "Placeholder.TEntry":
            self.delete("0", "end")
            self["style"] = "TEntry"

    def _add_placeholder(self, e):
        if not self.get():
            self.insert("0", self.placeholder)
            self["style"] = "Placeholder.TEntry"

query_entry = PlaceholderEntry(window, "What do you want to search for?")

# search box end
def image_downloader (): # This function will go to google and download pictures of your choosing from google

    file_location = (downloads_folder + str(key_words) + ' ' + str(number_of_results) +' automated downloads/')
    print('the downloads folder is ' + downloads_folder)
    # the path to the chromedriver file that needs to be downloaded locally
    DRIVER_PATH = '/Users/simonjakobsson//Desktop/Coding/chromedriver/chromedriver' # this is where you add the chromedriver

    browser = webdriver.Chrome(executable_path=DRIVER_PATH)
    browser.get('https://google.com')
    search = browser.find_element_by_name('q') # this selects the search box and types in the search query

    search.send_keys(key_words, Keys.ENTER) # this types in what you are searching for
    elem = browser.find_element_by_link_text('Images')
    elem.get_attribute('href')
    elem.click()

    value = 0
    for i in range(number_of_results): # this scrolls down to make the images accessible for download
        browser.execute_script("scrollBy(" + str(value) + ",+1000);")
        value += 1000
        time.sleep(1)

    elem1 = browser.find_element_by_id('islmp') # Google images contain in a div tag with is ‘islmp’. That’s the reason to fetch it.

    sub = elem1.find_elements_by_tag_name("img")

    try:
        os.mkdir(file_location)
    except FileExistsError:
        pass

    count = 0
    for i in sub:
        if count <= (number_of_results - 1) : # this sets the number of image search results based on the tkinter input variable
            src = i.get_attribute('src')
            print(str(count) + ' images have been downloaded.')
            try:
                if src != None:
                    src = str(src)
                    # print(src) # uncomment for printed image source
                    count += 1
                    urllib.request.urlretrieve(src, os.path.join(file_location, str(key_words) + ' ' + str(count) + '.jpg'))


                else:
                    raise TypeError
            except TypeError:
                print('fail')

        else :
            browser.quit()

    browser.quit()

def store_text_entry (): #this is the search bar press that assigns all the variables and starts the img downloading function
    global key_words  # without this, the key_words variable is local inside the function only
    global number_of_results
    key_words = str(query_entry.get())
    number_of_results = int(interactive_slider.get())
    if str(key_words) == "What images do you want?":
        print('No new search query was entered')
    else:
        print('the information has been stored and the images will be downloaded')
        image_downloader() #this is the big function above


search_button_text = "Search and download"

search_button = tk.Button(
    text=search_button_text,
    font=('helvetica', 16, 'bold'),
    width=20,
    height=2,
    bg="red",
    fg="#d4d4d4",
    command=store_text_entry
)
### start of the slider part

interactive_slider = Scale(window, from_=0, to=50, length=400, foreground="#d4d4d4", tickinterval=10, orient=HORIZONTAL)
interactive_slider.set(10)

slider_label = tk.Label(
    text="How many results do you want?",
    font=('helvetica', 12),
    foreground="#d4d4d4",  # Set the text color
    background="white",  # Set the background color to hex value (can also be written as fg/bg)
    width=50, # measured in text units - based on the "0" character, not pixels, so the output won't be square
    height=2
)
### end of the slider part

quit_button = tk.Button(
    text="Close",
    font=('helvetica', 10, 'bold'),
    fg="black",
    command=quit
)

### update button start ####
'''
count = 0
v = 'old text'
simon_label = tk.Label(text=str(interactive_slider.get()))
simon_label.pack()

def text_updater ():
    global v
    global count
    count += 1
    if count == 1 :
        v = 'Option ' + str(count)
        print(v)
    elif count == 2 :
        v = 'Option ' + str(count)
        print(v)
    else :
        v = 'Option ' + str(count)
        print(v)
        count = 0

update_button = tk.Button(
    text=str(v),
    font=('helvetica', 10, 'bold'),
    fg="black",
    command=text_updater
)

update_button.pack()
'''
### update button end ###
'''
The window you created earlier doesn’t change. 
You just created a Label widget, but you haven’t added it to the window yet. 
There are several ways to add widgets to a window. 
Right now, you can use the Label widget’s .pack() method:
'''

top_label.pack()
frame1.pack(fill=tk.X)
query_entry.pack()
frame2.pack(fill=tk.X)
slider_label.pack()
interactive_slider.pack()
frame3.pack(fill=tk.X)
search_button.pack()
quit_button.pack(side=tk.LEFT)

'''
When you .pack() a widget into a window, 
Tkinter sizes the window as small as it can while still fully encompassing the widget. 
'''


### this is the resizing part
f = r'/Users/simonjakobsson//Desktop/photo practice 10 automated downloads'
for file in os.listdir(f):  # By using os.listdir() function you can read all the file names in a directory.
    f_img = f + "/" + file
    img = Image.open(f_img)
    img = img.resize((image_height, image_width))
    img.save(f_img)
print("ok I think that worked?")

window.mainloop()
