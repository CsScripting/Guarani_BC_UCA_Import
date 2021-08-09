import os
# import codecs
import variables_mod as v
import validation_mod as val
import xml_mod as xml_m

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from threading import Thread

root = tk.Tk()

def begin_process():

    

    try:

        conf = v.cp.RawConfigParser()   

        #Path Jupyter
        # Path = 'C:/Users/Paulo Fernandes/Desktop/AmbienteProvas_PY/GUARANI_BC_UCA/ScriptFiles/config.txt'

        # Path cmd
        Path = './ScriptFiles/config.txt'


        conf.read(Path)

        file_groups = conf.get('datosEntrada', 'fileGrupos')
        hoja_groups = conf.get('datosEntrada', 'hojaGrupos')
        file_schedules = conf.get('datosEntrada', 'fileHorarios')
        hoja_schedules = conf.get('datosEntrada', 'hojaHorarios')


        academicTerm = conf.get('periodBtt', 'periodo')


        flag_wrong_info = False
        flag_wrong_classroom = False
        flag_validacion_columns = False


        flag_validacion_columns, errorHeader, errorBody = val.read_data(file_schedules,hoja_schedules, file_groups, hoja_groups, 
                                                          validacion = True) 

        if (flag_validacion_columns == False):

            if isinstance(errorBody, list):
  
                errorBody = ','.join(errorBody)           

            tk.messagebox.showerror(errorHeader, 'Check:\n\n' + errorBody)

            # print('errorHeader')
            # print('errorBodyStr')

        else:

            df_events, df_grupos, df_courses, df_salas= val.read_data(file_schedules, hoja_schedules, file_groups, hoja_groups)

            
            # DATA PREPARACION

            df_events = val.cleaning_data (df_events)
            df_courses = val.cleaning_data (df_courses)
            df_grupos = val.cleaning_data (df_grupos)
            df_salas =  val.cleaning_data (df_salas)                

            # Verify null Values (extract all nulls except values number_students (null student convert to value 0))

            #Passar Variavel a dizer que ficou con dados imcmpletpos(Para Apresentar no fim)
            df_events = val.check_nulls(df_events)

            # Extract Null Values after verify values students

            # Number students < 0 Retirados de eventos a importar...Esta a escrever em ficheiro tambem...
            df_events = val.verify_students_null(df_events)


            # ID to Asig Salas
            df_events_salas = df_events.copy()

            # Verificar a validação de Salas que não foram respectivamente mapeadas...    
            # Insert classrooms BC
            df_join_events_salas = val.get_name_salas_btt(df_events_salas, df_salas)


            df_events = df_join_events_salas.copy()

            df_events = val.replace_minutes_hours(df_events)


            #Verificar se eventos tem hora de inicio superior a hora de fim(verificar como mostrar a validação)

            df_events, df_wrong_hours = val.verify_hour_begin_end(df_events)

            #Os duplicados de professores ja foram retirados em metodo anterior...

            df_events = val.join_curriculum(df_events, df_courses, df_grupos)


            #Agrupar Eventos para inserir em XML:


            df_events = val.grouped_data(df_events)

            
            df_events = val.insert_name_acad_term(df_events, academicTerm)

            df_events = val.final_weeks(df_events)


            file_name = 'Horarios_UCA_'
            XML_AGREGADO = (v.xml_header + '\n'.join(df_events.apply(xml_m.xml_btt, axis=1)) + '\n' + v.xml_footer)
            

            #Write File
            path_file = './Xml_Files'

            if os.path.isdir(path_file):

                timestr = v.t.strftime("%Y%m%d_%H%M%S")
                with open('./Xml_Files/' + file_name + timestr + '.xml' ,'w') as f:
                    f.write(XML_AGREGADO)

            else:

                os.mkdir(path_file)
                timestr = v.t.strftime("%Y%m%d_%H%M%S")
                with open('./Xml_Files/' + file_name + timestr + '.xml' ,'w') as f:
                    f.write(XML_AGREGADO)

            root.withdraw()
            tk.messagebox.showinfo('EventsXML', 'XML File Generated:\n\nCheck Folder XML_Files.')
                
        
    except PermissionError as e:

        tk.messagebox.showerror('Close File', 'Check:\n\n' + 'Close Incomplete_Data on Folder New_Files')
       

#python ProcesoGuaraniBC.py
