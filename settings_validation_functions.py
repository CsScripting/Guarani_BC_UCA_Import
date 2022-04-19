from library import (
    os,
    ExcelFile,
    openpyxl)

import validation_mod as v

#Excepciones Settings Process
class ValidationFolder(Exception):
    pass


class ValidationFolder(Exception):
    pass

class FileNameInserted(Exception):
    def __init__(self, error_value):
        self.error_value = error_value
    pass

class FileNameNotInserted(Exception):
    pass

class FileHistoricNotInserted(Exception):
    def __init__(self, error_value):
        self.error_value = error_value
    pass

class ErrorSheetFileHistoric(Exception):
    def __init__(self, error_value):
        self.error_value = error_value
    pass

class FileNameErrorExtension(Exception):
    pass

class WrongColumsNoEventName(Exception):
    pass

class BttValueValidation(Exception):
    pass

class ErrorSheetFileSchedules(Exception):
    def __init__(self, error_value):
        self.error_value = error_value
    pass

class ErrorSheetFileGroups(Exception):
    def __init__(self, error_value):
        self.error_value = error_value
    pass

class WrongColumnsFile(Exception):
    def __init__(self, error_value):
        self.error_value = error_value
    pass

def validation_folder():

    check_directory = './' + v.xlsx_dir

    if not os.path.isdir(check_directory):
        
        os.mkdir(check_directory)
        raise ValidationFolder


def verify_file_settings(file_schedules : str,  file_groups, btt_value : int,  value_map_groups : int):


    path_to_schedules = './' + v.xlsx_dir + '/' + file_schedules
    path_to_groups = './' + v.xlsx_dir + '/' + file_groups


    if value_map_groups == 1:
        path_to_historic = './' + v.xlsx_dir + '/' + v.file_historic
        if not os.path.exists(path_to_historic):
            raise FileHistoricNotInserted(v.file_historic)
    
    if (file_schedules == '') | (file_groups == '') | (btt_value == ''):
        raise FileNameNotInserted ()

    file_schedules_extension = file_schedules.split('.')[-1]
    file_groups_extension = file_groups.split('.')[-1]

    if (file_schedules_extension != 'xlsx') |  (file_groups_extension != 'xlsx'):
        raise FileNameErrorExtension

    # verify if int btt_value
    try:
        btt_value = int(btt_value)
    except ValueError:
        raise BttValueValidation

    check_directory = './' + v.xlsx_dir

    if not os.path.exists(path_to_schedules):
        raise FileNameInserted(file_schedules)

    if not os.path.exists(path_to_groups):
        raise FileNameInserted(file_groups)



def verify_columns_files(file_schedules : str, file_groups:str,  check_historic : int, insert_classrooms : int,):

    path_to_file_schedules = './' + v.xlsx_dir + '/' + file_schedules
    path_to_file_groups = './' + v.xlsx_dir + '/' + file_groups

    if check_historic == 1:

        path_to_historic = './' + v.xlsx_dir + '/' + v.file_historic
        file_historic_read = ExcelFile(path_to_historic)
        sheets_file_historic = file_historic_read.sheet_names

        sheets_original_historic = [v.sheet_historic]
        check_sheets_name_historic =  all(elem in sheets_file_historic for elem in sheets_original_historic)

        if not check_sheets_name_historic:
            file_historic_read.close()
            raise ErrorSheetFileHistoric(v.file_historic)

        file_historic_read.close()


    #Check Sheet Files (Schedules)
    file_schedules_read = ExcelFile(path_to_file_schedules)
    sheets_file_schedules = file_schedules_read.sheet_names

    if insert_classrooms == 1:
        sheets_original_schedules = ['Horarios', 'Carreras', 'Salas']
    else:
        sheets_original_schedules = ['Horarios', 'Carreras']

    check_sheets_name_schedule =  all(elem in sheets_file_schedules for elem in sheets_original_schedules)

    if not check_sheets_name_schedule:
        file_schedules_read.close()
        raise ErrorSheetFileSchedules(file_schedules)
    
    file_schedules_read.close()


    #Check Sheet Files (Groups)
    file_group_read = ExcelFile(path_to_file_groups)
    sheets_file_group = file_group_read.sheet_names
    sheets_original_group = ['Grupos']
    check_sheets_name_group =  all(elem in sheets_file_group for elem in sheets_original_group)

    if not check_sheets_name_group:
        file_group_read.close()
        raise ErrorSheetFileGroups(file_groups)

    file_group_read.close()

    # Check Columns Names file Schedules(don´t load all file)

    load_file_schedules = openpyxl.load_workbook(filename= path_to_file_schedules, read_only=True)
    
    #Check Columns Horarios
    load_schedule_sheet = load_file_schedules[v.sheet_horarios]
    columns_file_horarios=[]

    for cell in load_schedule_sheet[1]:
        columns_file_horarios.append(cell.value)
    
    columns_horarios_original = [v.v_comision, v.v_subcomision, v.v_day, v.v_hour_begin,
					             v.v_hour_end, v.v_typology, v.v_mod_cod, v.v_section,
					             v.v_students, v.v_group, v.v_teacher, v.v_weeks,
					             v.v_course_code, v.v_year,
					             v.g_plan_cod, v.v_mod_name, v.v_classrooms_code_guarani, v.v_id_event_guarani]

    check_columns_names_horarios =  all(elem in columns_file_horarios for elem in columns_horarios_original)

    if not check_columns_names_horarios:
        load_file_schedules.close()
        raise WrongColumnsFile(v.sheet_horarios)

    if insert_classrooms == 1:

        #Check Columns Salas
        load_classrooms_sheet = load_file_schedules[v.sheet_classrooms]
        columns_file_salas=[]

        for cell in load_classrooms_sheet[1]:
            columns_file_salas.append(cell.value)
        
        columns_salas_original = [v.s_sala_name, v.s_sala_code, v.s_sala_edificio]

        check_columns_names_salas =  all(elem in columns_file_salas for elem in columns_salas_original)

        if not check_columns_names_salas:
            load_file_schedules.close()
            raise WrongColumnsFile(v.sheet_classrooms)


    #Check Columns Carreras
    load_course_sheet = load_file_schedules[v.sheet_course]
    columns_file_course=[]

    for cell in load_course_sheet[1]:
        columns_file_course.append(cell.value)
    
    columns_course_original = [v.c_courses_name,v.c_courses_sigla, v.c_courses_code]

    check_columns_names_courses =  all(elem in columns_file_course for elem in columns_course_original)

    if not check_columns_names_courses:
        load_file_schedules.close()
        raise WrongColumnsFile(v.sheet_course)

    load_file_schedules.close()    

    # Check Columns Names file Groups(don´t load all file)

    load_file_groups = openpyxl.load_workbook(filename= path_to_file_groups, read_only=True)

    #Check Columns grupos
    load_group_sheet = load_file_groups[v.sheet_grupos]
    columns_file_grupos=[]

    for cell in load_group_sheet[1]:
        columns_file_grupos.append(cell.value)
    
    columns_grupos_original = [v.g_name, v.g_plan_cod, v.g_students, v.g_max_limit, v.g_cons_limit,
					           v.v_comision, v.v_subcomision, v.g_nombre_comision,
					           v.v_section, v.g_agreggated_groups]

    check_columns_names_grupos =  all(elem in columns_file_grupos for elem in columns_grupos_original)

    if not check_columns_names_grupos:
        load_file_groups.close()
        raise WrongColumnsFile(v.sheet_grupos)

    load_file_groups.close()

    # Check Columns Names file HistoricGroups(don´t load all file)
    if check_historic == 1:
        load_file_historic = openpyxl.load_workbook(filename= path_to_historic, read_only=True)

        #Check Columns grupos
        load_historic_sheet = load_file_historic[v.sheet_historic]
        columns_file_historic=[]

        for cell in load_historic_sheet[1]:
            columns_file_historic.append(cell.value)
        
        columns_historic_original = [v.v_mod_cod, v.v_typology, v.v_section, v.v_mod_name, 
                                     v.g_nombre_comision, v.v_students, v.g_plan_cod]

        check_columns_names_historic =  all(elem in columns_file_historic for elem in columns_historic_original)

        if not check_columns_names_historic:
            load_file_historic.close()
            raise WrongColumnsFile(v.sheet_historic)

        load_file_historic.close()


    return()

