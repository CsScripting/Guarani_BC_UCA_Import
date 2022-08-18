import process_data_validation as procVal
from variables_mod import *
import validation_mod as val
import xml_mod as xml_m

from library import(
	codecs, 
    messagebox
)

# only dev mod - check errores
import traceback

def begin_process(file_schedules : str,  file_groups : str, map_groups : int, check_classrooms : int, academic_term : str):


    try:

        valid_process = False

        process_folder, process_code = procVal.create_validation_folder()
        
        name_file_validation = procVal.create_xlsx_data_process (file_schedules, file_groups, process_folder, process_code, map_groups, 
                                                                 check_classrooms, academic_term)

        df_events, df_grupos, df_courses, df_salas, df_historic_students= val.read_data(file_schedules, file_groups, check_classrooms, map_groups)
        df_events = val.cleaning_data (df_events)
        df_courses = val.cleaning_data (df_courses)
        df_grupos = val.cleaning_data (df_grupos)
        df_salas =  val.cleaning_data (df_salas)

        if map_groups == 1:
            df_historic_students = val.cleaning_data(df_historic_students)



        #Passar Variavel a dizer que ficou com dados incompletos(Para Apresentar no fim)
        df_events = val.check_nulls(df_events, check_classrooms, name_file_validation)

        # Extract Null Values after verify values students

        # Number students < 0 Retirados de eventos a importar...Esta a escrever em ficheiro tambem...
        df_events = val.verify_students_null(df_events, name_file_validation)



        classrooms_guarani = val.check_classrooms_without_ID(df_salas, name_file_validation)
        classrooms_guarani = df_salas.copy()

        if check_classrooms == 1:

            # ID to Asig Salas
            df_events_salas = df_events.copy()

            # Verificar a validação de Salas que não foram respectivamente mapeadas...    
            # Insert classrooms BC
            df_join_events_salas = val.get_name_salas_btt(df_events_salas, classrooms_guarani, name_file_validation)

            df_events = df_join_events_salas.copy()

        else:

            val.create_BEST_Classrooms(classrooms_guarani, process_folder, process_code)

            
        # Neste momento é efectuado no processo de BC_To_BTT
        # df_events = val.replace_minutes_hours(df_events)


        #Verificar se eventos tem hora de inicio superior a hora de fim(verificar como mostrar a validação)

        df_events = val.verify_hour_begin_end(df_events, name_file_validation)

        #Os duplicados de professores ja foram retirados em metodo anterior...

        df_events = val.join_curriculum(df_events, df_courses, df_grupos, check_classrooms, name_file_validation)

        if map_groups == 1:

            df_events = val.map_students_number_historic (df_events, df_historic_students)

        else:

            # No caso de verificar o historico faz drop de estas colunas em metodo map_students_number_historic
            df_events.drop(columns=[v_section, g_nombre_comision])

        #Agrupar Eventos para inserir em XML:

        df_events = val.grouped_data(df_events, check_classrooms, map_groups)

        df_events = val.insert_name_section(df_events)

        df_events = val.insert_name_acad_term(df_events, academic_term)

        df_events = val.final_weeks(df_events)

        # df_compartidas = val.prepare_data_xml_compartidas(df_compartidas)

        #Ajustar de onde se pretende sacar o Excel para apresentar a user (Aqui terá os separadores que permite leitura a user)

        df_events = val.selec_data_comissiones_compartidas_to_import(df_events, check_classrooms)

        #Não usar a partir de v3.0.1 (filtrar por zero...neste metodo nunca irá guradar eventos = 0)
        df_events = val.filter_events_grouped_students_null (df_events, name_file_validation)

        if check_classrooms == 0:
            
            val.create_add_classrooms(df_events, process_folder, process_code)

        file_name = '/Horarios_UCA_'

        path_file_xml = process_folder + file_name + process_code + '.xml'
        XML_AGREGADO = (xml_header + '\n'.join(df_events.apply(xml_m.xml_btt,args = (check_classrooms,), axis=1)) + '\n' + xml_footer)
        
        with codecs.open(path_file_xml ,'w', 'utf-8') as f:
            f.write(XML_AGREGADO)

        # time.sleep(4)

        valid_process = True

        return (valid_process)
        
    except Exception as E:  
       
        messagebox.showerror('Error', 'Contact:\n\n' + 'info@bulletsolutions.com')

        # Only to Debug
        print (traceback.format_exc())

       
