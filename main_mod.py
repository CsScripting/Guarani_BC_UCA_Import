from pandas.core.frame import DataFrame
from general_mod import group_unique_entities
import os
import variables_mod as v
import validation_mod as val
import xml_mod as xml_m

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from threading import Thread

from library import(
	codecs
)

def begin_process(file_schedules : str,  file_groups : str, map_groups : int, check_classrooms : int, academic_term : str):

    

    try:

        if check_classrooms == 1:

            df_events, df_grupos, df_courses, df_salas, df_historic_students= val.read_data(file_schedules, file_groups, check_classrooms, map_groups)
            df_events = val.cleaning_data (df_events)
            df_courses = val.cleaning_data (df_courses)
            df_grupos = val.cleaning_data (df_grupos)
            df_salas =  val.cleaning_data (df_salas)

        else:

            df_events, df_grupos, df_courses, df_historic_students = val.read_data(file_schedules, file_groups,check_classrooms, map_groups)

            df_events = val.cleaning_data (df_events)
            df_courses = val.cleaning_data (df_courses)
            df_grupos = val.cleaning_data (df_grupos)
              

        # Verify null Values (extract all nulls except values number_students (null student convert to value 0))

        #Passar Variavel a dizer que ficou con dados incompletos(Para Apresentar no fim)
        df_events = val.check_nulls(df_events, check_classrooms)

        # Extract Null Values after verify values students

        # Number students < 0 Retirados de eventos a importar...Esta a escrever em ficheiro tambem...
        df_events = val.verify_students_null(df_events)

        if check_classrooms == 1:

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

        df_events = val.join_curriculum(df_events, df_courses, df_grupos, check_classrooms)

        if map_groups == 1:

            df_events = val.map_students_number_historic (df_events, df_historic_students)

        else:

            df_events.drop(columns=[v.v_section, v.g_nombre_comision])

        #Agrupar Eventos para inserir em XML:

        df_events = val.grouped_data(df_events, check_classrooms, map_groups)

        df_events = val.insert_name_section(df_events)

        df_events = val.insert_name_acad_term(df_events, academic_term)

        df_events = val.final_weeks(df_events)

        # df_compartidas = val.prepare_data_xml_compartidas(df_compartidas)

        df_events = val.selec_data_comissiones_compartidas_to_import(df_events, check_classrooms)

        df_events.to_excel('./New_Files/EventsGrouped.xlsx', 'Hoja1', index = False)

        file_name = 'Horarios_UCA_'
        XML_AGREGADO = (v.xml_header + '\n'.join(df_events.apply(xml_m.xml_btt,args = (check_classrooms,), axis=1)) + '\n' + v.xml_footer)
        

       #Write File
        path_file = './Xml_Files'

        if os.path.isdir(path_file):

            timestr = v.t.strftime("%Y%m%d_%H%M%S")
            with codecs.open('./Xml_Files/' + file_name + timestr + '.xml' ,'w', 'utf-8') as f:
                f.write(XML_AGREGADO)

        else:

            os.mkdir(path_file)
            timestr = v.t.strftime("%Y%m%d_%H%M%S")
            with codecs.open('./Xml_Files/' + file_name + timestr + '.xml' ,'w', 'utf-8') as f:
                f.write(XML_AGREGADO)

        # root.withdraw()
        tk.messagebox.showinfo('EventsXML', 'XML File Generated:\n\nCheck Folder XML_Files.')


    except NameError as E:  
         
         print (E)
    #    tk.messagebox.showerror('Error', 'Contact:\n\n' + 'info@bulletsolutions.com')
       
