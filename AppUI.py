from main_mod import *

def UI():


    try:


        version = '2.0'
        #git commit from local

        def status_running (name, func):


            root.overrideredirect(True)

            label1 = Label(root, text = 'BTT XML BC\n\n-- Guarani to Bullet Calendar --\n'+ version)
            label2 = Label(root, text = 'Running')
            label3 = Label(root, text = '....', font =(5)) 

            label1.grid(column= 0, row = 0)
            label2.grid (column = 0, row = 1)
            label3.grid(column = 0, row = 2)

            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=1)
            root.update()

            
            

            def update_status_running ():


                # Get the current message
                current_status = label3["text"]

                # If the message is "Working...", start over with "Working"
                if current_status.endswith("...."): current_status = ""

                # If not, then just add a "." on the end
                else: current_status += "."

                # Update the message
                label3["text"] = current_status

                # After 1 second, update the status
                root.after(1000, update_status_running)
                

            root.after(0, update_status_running) 

            func()

            root.after(10, root.destroy)
       

        def run_thread(name, func):

            Thread(target=status_running, args=(name, func)).start()    
     
        def on_click_two_threads():

            run_thread('process', begin_process)

            


        root.geometry ("230x150")
        root.resizable(0, 0)
        root.title('EventsXml')
        

        root.iconbitmap('./ScriptFiles/Images/log.ico')
        root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
        root.wm_attributes("-topmost", 1)

        cmd = Button(root, text = 'START', background="#E0E0E0", borderwidth=0, command = on_click_two_threads )
        label1 = Label(root, text = 'BTT XML BC\n\n-- Guarani to Bullet Calendar --\n'+ version)
        label2 = Label(root, text = '')
        
        #PositionGrid
        label1.grid(column= 0, row = 0)
        cmd.grid(column = 0, row = 1)
        label2.grid(column= 0, row = 2)


        #center Label Inside the windowsWidow
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
            
        root.mainloop()


    finally:
        
       root.destroy