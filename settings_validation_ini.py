import settings_validation_functions as settValidation
from library import messagebox
import variables_mod as v


def settings_validation_fields(file_schedules:str, file_groups:str, value_btt:str, value_map_groups:int, value_insert_classrooms:int):

    error_exception = False

    try: 
        
        #Check folder
        settValidation.validation_folder()
        
        #Check if File existe on folder
        settValidation.verify_file_settings(file_schedules, file_groups, value_btt, value_map_groups)

        #ValidacionesFile
        settValidation.verify_columns_files(file_schedules, file_groups, value_map_groups, value_insert_classrooms)

        return(error_exception)
 

    except settValidation.ValidationFolder:

        messagebox.showerror('Validation Folder', 'Files ' + file_schedules + ' must be inserted on folder ' + v.xlsx_dir + ' !!')
    
    except settValidation.FileNameInserted as e:

        messagebox.showerror('Validation File', 'File ' + e.error_value + '  does not existe on folder ' + v.xlsx_dir + ' !!')

    except settValidation.FileHistoricNotInserted as e:

        messagebox.showerror('Validation File', 'To generate with STUDENT HISTORIC:\n\n Insert ' + e.error_value + '  on folder ' + v.xlsx_dir + ' !!')
        
    except settValidation.FileNameNotInserted as e:

        messagebox.showerror('Validation Files', 'Fill all boxs to submit !!')
        
    except settValidation.FileNameErrorExtension:

        messagebox.showerror('Validation File', 'Files must have a .xlsx extension !!')

    except settValidation.BttValueValidation:

        messagebox.showerror('Data Validation', 'Value BTT must be a int value !!')

    except settValidation.ErrorSheetFileSchedules as e:

        messagebox.showerror('File Schedules', e.error_value +  ' must have sheets named:\n\nHorarios;\nSalas;\nCarreras.')


    except settValidation.ErrorSheetFileGroups as e:

        messagebox.showerror('File Groups', e.error_value +  ' must have a sheet named:\n\nGrupos.')

    except settValidation.WrongColumnsFile as e:

        if e.error_value == v.sheet_horarios:

            columns_original = v.v_comision+ ' - ' + v.v_subcomision+ ' - ' + v.v_day+ ' - ' + v.v_hour_begin+ ' - ' + \
					           v.v_hour_end+ ' - ' + v.v_typology+ ' - ' + v.v_mod_cod+ ' - ' + v.v_section+ ' - ' + \
					           v.v_students+ ' - ' + v.v_group+ ' - ' + v.v_teacher+ ' - ' + v.v_weeks+ ' - ' + \
					           v.v_course_code+ ' - ' + v.v_year+ ' - ' + \
					           v.g_plan_cod + ' - ' + v.v_mod_name+ ' - ' + v.v_classrooms_code_guarani+ ' - ' + v.v_id_event_guarani

        if e.error_value == v.sheet_classrooms:

            columns_original = v.s_sala_name + ' - ' + v.s_sala_code + ' - ' + v.s_sala_edificio


        if e.error_value == v.sheet_course:

            columns_original = v.c_courses_name + ' - ' + v.c_courses_sigla + ' - ' + v.c_courses_code

        if e.error_value == v.sheet_grupos:

            columns_original = v.g_name+ ' - ' + v.g_plan_cod+ ' - ' + v.g_students+ ' - ' + v.g_max_limit+ ' - ' + \
                               v.g_cons_limit+ ' - ' + v.v_comision+ ' - ' + v.v_subcomision+ ' - ' + v.g_nombre_comision+ ' - ' + \
 					           v.v_section+ ' - ' + v.g_agreggated_groups

        if e.error_value == v.sheet_historic:

            columns_original = v.v_mod_cod + ' - ' + v.v_typology+ ' - ' + v.v_section+ ' - ' + v.v_mod_name+ ' - ' + \
                               v.g_nombre_comision+ ' - ' + v.v_students + ' - ' + v.g_plan_cod

        messagebox.showerror('Check Sheet ' + e.error_value, 'Possible Columns Names:\n\n' + columns_original)

    except settValidation.ErrorSheetFileHistoric as e:

        messagebox.showerror('Check Sheet'  , 'File '+ e.error_value + ' must have sheet:\n\n' + 'Datos')
  