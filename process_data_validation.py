from library import (
    os,
    time, 
    DataFrame
)

from variables_mod import *
def create_validation_folder():

    if not os.path.isdir(v_events_dir):

        os.mkdir(v_events_dir)

    timestr = time.strftime("_%Y%m%d_%H%M%S")

    process_folder= './' + v_events_dir + '/' + 'BC_XML' + timestr

    if not os.path.isdir(process_folder):
        
        os.mkdir(process_folder) 

    process_code = timestr

    return(process_folder,process_code)


def create_xlsx_data_process(file_schedules : str, file_groups : str, folder : str, process_code :str, map_groups : int, check_classrooms : int, academic_term : str):

    df_process = DataFrame(columns = [v_variables_process, v_variables_values])

    #Insert Name file Events
    df_process = df_process.append({v_variables_process : v_file_events, 
                                    v_variables_values : file_schedules}, ignore_index = True)


    #Insert Name file Groups
    df_process = df_process.append({v_variables_process : v_file_groups, 
                                    v_variables_values : file_groups}, ignore_index = True)

    #Insert Name file Groups
    df_process = df_process.append({v_variables_process : v_file_groups, 
                                    v_variables_values : file_groups}, ignore_index = True)

    #Insert Academic Term BTT
    df_process = df_process.append({v_variables_process : v_acad_term_btt, 
                                    v_variables_values : academic_term}, ignore_index = True)

    #Insert Opcion Historic_Groups
    if map_groups == 1:

        value_map_groups = 'True'
    else: 
        value_map_groups = 'False' 

    df_process = df_process.append({v_variables_process : v_historic_groups, 
                                    v_variables_values : value_map_groups}, ignore_index = True)


    #Insert Opcion Classrooms
    if check_classrooms == 1:

        value_check_classrooms = 'True'
    else: 
        value_check_classrooms = 'False' 

    df_process = df_process.append({v_variables_process : v_with_classrooms, 
                                    v_variables_values : value_check_classrooms}, ignore_index = True)


    name_file_validation = folder + '/DataValidation' + process_code
    df_process.to_excel(name_file_validation + '.xlsx', 'Variables', index = False,freeze_panes=(1,0))
    
    return(name_file_validation)