from main_mod import *
import app_ui_views as view

def UI():

    try:

        view.start_main_window()

    except Exception as E:  

       
       view.messagebox.showerror('Error', 'Contact:\n\n' + 'info@bulletsolutions.com')