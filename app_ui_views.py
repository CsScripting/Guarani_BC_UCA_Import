from main_mod import begin_process
import settings_validation_ini as settIni
from library import (
    tk,
    messagebox,
    sys,
    os,
    Thread)

global main_window
main_window = tk.Tk()

from variables_mod import version

# Function Manage path log to generate .exe
def resource_path(relative_path):
    
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path)


#Save on list distinct String opciones (NameFile, NameEvent, Separator)
global names_inserted_vars
names_inserted_vars = []
for i in range(3):

    check_names = tk.StringVar
    names_inserted_vars.append(check_names)


#Save on list distinct INT opciones (RadioButtones, CheckBoxes)
global radio_button_vars 
radio_button_vars= []
for j in range(2):

    check_radio_button = tk.IntVar()
    radio_button_vars.append(check_radio_button)



def start_main_window():

    #path used on log secundary window
    global path
    global link
    global button_start
    global label1_begin
    global label2_begin
    
    #Proprieties Window
    main_window.geometry ("230x150")
    main_window.resizable(0, 0)
    main_window.title('Events XML')
    main_window.eval('tk::PlaceWindow %s center' % main_window.winfo_toplevel())
    main_window.wm_attributes("-topmost", 1)

    #Manage path log to generate .exe
    path = resource_path("./log.ico")
    main_window.iconbitmap(path + '/log.ico')

    #Objects inside Window:
     
    button_start = tk.Button(main_window, text = 'START', background="#d1e0e0", borderwidth=0)
    button_start['state'] = 'disabled'
    label1_begin= tk.Label(main_window, text = 'BTT XML BC\n\n-- Guarani to Bullet Calendar --\n'+ version,)
    label2_begin = tk.Label(main_window, text = '')
    link = tk.Label(main_window, text="Process Settings",font=('Helvetica', 8, 'underline'), fg="#663300", cursor="hand2")
    link.bind("<Button-1>", lambda e: start_settings_window())

    #Position objects inside window
    label1_begin.grid(column= 0, row = 0, pady=10)
    button_start.grid(column = 0, row = 1)
    link.grid(column=0, row=3, ipady=4)
    label2_begin.grid(column=0, row=4)

    #Center Window - position on grid
    main_window.columnconfigure(0, weight=1)
    main_window.rowconfigure(0, weight=1)
            

    main_window.mainloop()


def start_settings_window():

    global button_validation
    global group_choice1
    global group_choice2
    global classroom_choice1
    global classroom_choice2
    global link_edit

    disable_link_settings()

    # Proprieties Window
    global settings_window
    settings_window = tk.Toplevel()
    settings_window.title('Settings')
    settings_window.geometry ("230x150")
    settings_window.resizable(0, 0)
    settings_window.iconbitmap(path + '/log.ico')

    #Center Window(eval not available to object TopLevel):
    windowWidth = settings_window.winfo_reqwidth()
    windowHeight = settings_window.winfo_reqheight()
    positionRight = int(settings_window.winfo_screenwidth()/3 - windowWidth/3)
    positionDown = int(settings_window.winfo_screenheight()/2 - windowHeight/2)

    settings_window.geometry("+{}+{}".format(positionRight, positionDown))

    #Containers to distinct grid
    top_WindowGrid = tk.Frame(settings_window)
    bottom_WindowGrid = tk.Frame(settings_window)
    check_Section_WindowGrid = tk.Frame(settings_window)

    #Pack Containers Grid
    top_WindowGrid.pack(side="top", fill="x", expand=False)
    bottom_WindowGrid.pack(side="bottom", fill="both", expand=True)
    check_Section_WindowGrid.pack(side="bottom", fill="x", expand=False)
    
    #Proportions Window
    top_WindowGrid.grid_columnconfigure(0, weight=1)
    top_WindowGrid.grid_columnconfigure(1, weight=3)

    #Objects inside topGrid Window:

    #Config label File Schedules
    fileLabel_schedules = tk.Label(top_WindowGrid, text='File Schedules:', font="Segoe 8 italic", foreground="#009999")
    #Config textInsertion Schedules
    names_inserted_vars[0] = tk.Entry(top_WindowGrid,borderwidth=0,highlightthickness=1,highlightcolor='#ffb84d', width=20,justify='left',font=("Segoe 8"),background="#ffe6cc", disabledbackground="#ffe6cc")

    #Config label File Groups
    fileLabel_groups = tk.Label(top_WindowGrid, text='File Groups:', font="Segoe 8 italic", foreground="#009999")
    #Config textInsertion Groups
    names_inserted_vars[1] = tk.Entry(top_WindowGrid,borderwidth=0,highlightthickness=1,highlightcolor='#ffb84d', width=20,justify='left',font=("Segoe 8"),background="#ffe6cc", disabledbackground="#ffe6cc")

    #Config label File Schedules
    fileLabel_period_btt = tk.Label(top_WindowGrid, text='Acad. Term BTT:', font="Segoe 8 italic", foreground="#009999")
    #Config textInsertion Schedules
    names_inserted_vars[2] = tk.Entry(top_WindowGrid,borderwidth=0,highlightthickness=1,highlightcolor='#ffb84d', width=5,justify='left',font=("Segoe 8"),background="#ffe6cc", disabledbackground="#ffe6cc")
    
    #Position Objects inside TopGrid 
    fileLabel_schedules.grid(row=0, column=0, sticky=tk.W, pady=2,padx=3 )
    names_inserted_vars[0].grid(row=0, column=1, sticky='w')
    fileLabel_groups.grid(row=1, column=0, sticky=tk.W, pady=2,padx=3 )
    names_inserted_vars[1].grid(row=1, column=1, sticky='w')
    fileLabel_period_btt.grid(row=2, column=0, sticky=tk.W, pady=2,padx=3 )
    names_inserted_vars[2].grid(row=2, column=1, sticky='w')

    #Objects inside Bottom Grid Window:
            
    #(First Opcion: All Rows):
    opcion_group_historic = tk.Label(bottom_WindowGrid, text='Historic Groups:', font="Segoe 8 italic", foreground="#009999")        
    group_choice1= tk.Radiobutton(bottom_WindowGrid, text = 'True',font="Segoe 8 italic", variable=radio_button_vars[0], value=1)
    group_choice2= tk.Radiobutton(bottom_WindowGrid, text = 'False', font="Segoe 8 italic", variable=radio_button_vars[0], value=0)
    group_choice1.select() #Default opcion
    #Label to manage grid layout only
    label_empty = tk.Label(bottom_WindowGrid, text = '')

    #(Second Opcion: With ID):
    opcion_classrooms = tk.Label(bottom_WindowGrid, text='With Classroom:', font="Segoe 8 italic", foreground="#009999")        
    classroom_choice1= tk.Radiobutton(bottom_WindowGrid, text = 'True',font="Segoe 8 italic", variable=radio_button_vars[1], value=1)
    classroom_choice2= tk.Radiobutton(bottom_WindowGrid, text = 'False', font="Segoe 8 italic", variable=radio_button_vars[1], value=0)
    classroom_choice1.select() #Default opcion

    
    #(Last Opcion Grid: Button VAlidacion and Edit)
    button_validation = tk.Button(bottom_WindowGrid, text = 'Submit', background="#ffe6cc", borderwidth=0, cursor="hand2", command = data_validation)

    link_edit = tk.Label(bottom_WindowGrid, text="Edit",font=('Helvetica', 8, 'underline'), fg="#663300")
    disable_link_edit()
    

    #Position on Grid
    opcion_group_historic.grid(row=0, column=0, sticky=tk.W, padx=3)
    group_choice1.grid (row=0, column=1, sticky=tk.W, ipadx = 5)
    group_choice2.grid (row=0, column=2, sticky=tk.W,  ipadx = 5)
    label_empty.grid(row=0, column=3)

    opcion_classrooms.grid(row=1, column=0, sticky=tk.W, padx=3)
    classroom_choice1.grid (row=1, column=1, sticky=tk.W, ipadx = 5)
    classroom_choice2.grid (row=1, column=2, sticky=tk.W,  ipadx = 5)


    button_validation.grid(row=3, column=2, sticky=tk.E + tk.S, pady=7)
    link_edit.grid(row=3, column=1, sticky=tk.W, padx = 10)


    main_window.wm_state('iconic')
    settings_window.protocol("WM_DELETE_WINDOW", closing_behavior)


def disable_link_settings():

    link['state'] = 'disabled'
    link.config(cursor= "")
    link.unbind('<Button-1>')


def disable_link_edit():

    link_edit["state"] = 'disable'
    link_edit.config(cursor = "")
    link_edit.unbind('<Button-1>')
    

def enable_link_settings():

    link["state"] = "normal"
    link.config(cursor= "hand2")
    link.bind("<Button-1>", lambda e: start_settings_window())
    

def enable_link_edit():

    link_edit["state"] = "normal"
    link.config(cursor= "hand2")
    link_edit.bind("<Button-1>", lambda e: enable_settings()) 


def get_settings():

    file_shedules : str= names_inserted_vars[0].get()
    file_groups : str= names_inserted_vars[1].get()
    value_btt : str= names_inserted_vars[2].get()
    value_map_groups = radio_button_vars[0].get()
    value_insert_classrooms = radio_button_vars[1].get()
    
    
    file_shedules = file_shedules.strip()
    file_groups = file_groups.strip()

    return(file_shedules,file_groups,value_btt, value_map_groups, value_insert_classrooms)

def data_validation ():


    file_schedules,file_groups, value_btt, value_map_groups, value_insert_classrooms = get_settings()

    error = settIni.settings_validation_fields(file_schedules, file_groups, value_btt, value_map_groups, value_insert_classrooms)
    
    if error == False:

        global gl_file_schedules
        global gl_file_groups
        global gl_map_groups
        global gl_classrooms
        global gl_academic_term

        disable_settings()
        enable_link_edit()

        button_validation["text"] = 'Ready'
        button_validation['background'] = '#d1e0e0'
        button_validation.config(cursor= "")
        main_window.wm_state('normal')

        gl_file_schedules = file_schedules
        gl_file_groups = file_groups
        gl_map_groups = value_map_groups
        gl_classrooms = value_insert_classrooms
        gl_academic_term = value_btt

        enable_button_start()
        

def enable_button_start():

    button_start['state'] = 'normal'
    button_start['background'] = '#ffe6cc'
    button_start ['cursor']="hand2"
    button_start.config(command = on_click_two_threads) 
    


def disable_button_start():

    button_start['state'] = 'disable'
    button_start['background'] = '#d1e0e0'
    button_start ['cursor']=""

def disable_button_ready_settings():

    button_validation['state'] = 'disable'
    button_validation['background'] = '#d1e0e0'
    button_validation ['cursor']=""


def closing_behavior():

    value_inserted_file_schedules = names_inserted_vars[0].get()
    value_inserted_file_group = names_inserted_vars[1].get()
    value_inserted_btt = names_inserted_vars[2].get()

    if (value_inserted_file_group == '') & (value_inserted_file_schedules == '') & (value_inserted_btt == '') :

        enable_link_settings()
        settings_window.destroy()
        main_window.state('normal')

    else:
        
        if messagebox.askokcancel("Close Settings", "Do you want to quit? \n\n All SETTINGS Values Will Be LOST !!"):

            enable_link_settings()
            disable_button_start()
            settings_window.destroy()
            main_window.state('normal')

def disable_settings():

    names_inserted_vars[0].config(state='disable')
    names_inserted_vars[1].config(state='disable')
    names_inserted_vars[2].config(state='disable')
    group_choice1.config(state='disable')
    group_choice2.config(state='disable')
    classroom_choice1.config(state='disable')
    classroom_choice2.config(state='disable')
    
    

def enable_settings():

    names_inserted_vars[0].config(state='normal')
    names_inserted_vars[1].config(state='normal')
    names_inserted_vars[2].config(state='normal')
    group_choice1.config(state='normal')
    group_choice2.config(state='normal')
    classroom_choice1.config(state='normal')
    classroom_choice2.config(state='normal')


    button_validation['background'] = '#ffe6cc'
    button_validation["text"] = 'Submit'

    button_start['state'] = 'disable'
    button_start['background'] = '#d1e0e0'
    button_start.config(cursor= "")


#Functions UI-RUNNING
def update_start_window():

    label1_begin.config (text = 'BTT XML BC\n\n-- Guarani to Bullet Calendar --\n'+ version,)
    label2_begin.config(text = '')
    label3.config(text='')

    disable_button_start()
    label3.grid_remove()

    #Position objects inside window
    label1_begin.grid(column= 0, row = 0, pady=10)
    button_start.grid(column = 0, row = 1)
    link.grid(column=0, row=3, ipady=4)
    label2_begin.grid(column=0, row=4)
    enable_link_settings()

    #Center Window - position on grid
    main_window.columnconfigure(0, weight=1)
    main_window.rowconfigure(0, weight=1)

    return()

def status_running (name, func):
    global label3
    def on_start():
        global running
        running = True


    def on_stop():
        global running
        running = False
    
    on_start()

    if running:

        label1_begin.config (text = 'BTT XML BC\n\n-- Guarani to Bullet Calendar --\n'+ version,)
        label2_begin.config(text = 'Running')
        label3 = tk.Label(main_window, text = '....', font =(5)) 

        label1_begin.grid(column= 0, row = 0)
        label2_begin.grid (column = 0, row = 1)
        label3.grid(column = 0, row = 2)
        link.grid_remove()

        main_window.columnconfigure(0, weight=1)
        main_window.rowconfigure(0, weight=1)
        main_window.update()


    def update_status_running ():

        if running:

            # Get the current message
            current_status = label3["text"]

            if current_status.endswith("...."): current_status = ""

            # If not, then just add a "." on the end
            else: current_status += "."

            # Update the message
            label3["text"] = current_status

            # After 1 second, update the status
            main_window.after(1000, update_status_running)
        

    main_window.after(0, update_status_running) 

    valid_process = func(gl_file_schedules, gl_file_groups, gl_map_groups, gl_classrooms, gl_academic_term)

    on_stop()
    update_start_window()
    settings_window.destroy()

    if valid_process:
        tk.messagebox.showinfo('EventsXML', 'XML File Generated:\n\nCheck EventsFolder.')



def run_thread(name, func):

    Thread(target=status_running, args=(name, func)).start()    
     
def on_click_two_threads():

    disable_link_edit()
    disable_button_ready_settings()
    run_thread('process', begin_process)