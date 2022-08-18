from pandas import date_range
from general_mod import write_file, weekly_date, asign_weeks, group_unique_entities
from variables_mod import *
class HaltException(Exception): pass

from library import (
	DataFrame,
	read_excel,
	merge,
	to_datetime,
	where,
	nan
	)

# import qgrid as gd

def cleaning_data (df : DataFrame):
	
	df = df.apply(lambda x: x.str.strip())
	df.columns = df.columns.str.strip()
	df = df.replace(r'^\s*$', nan, regex=True)
	
	return (df)


def group_entities(df, list_series, sep = ',', sort_flag = True):
	
	df = df.applymap(str)
	df.set_index (list_series, inplace=True)
	df = df.groupby (level = list_series, sort = sort_flag).agg(sep.join)
	df.reset_index(inplace=True)
	
	return df


def read_data(events_file, groups_file, check_classroom : int, map_groups : int):
	
	df_historic : DataFrame() = []
	df_salas : DataFrame() = []
	directory_files = './' + xlsx_dir	+ '/'
	

	# Manage values 'NA'
	val_null = ['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A N/A', 
				'#N/A', 'N/A', 'n/a', '', '#NA', 'NULL', 'null', 'NaN', '-NaN', 'nan', '-nan', '']

	
	df_events = read_excel (directory_files + events_file, sheet_horarios, dtype = 'str', keep_default_na=False, na_values=val_null)
	df_courses = read_excel (directory_files + events_file, sheet_course, dtype = 'str', keep_default_na=False, na_values=val_null)
	df_grupos = read_excel (directory_files + groups_file, sheet_grupos, dtype = 'str', keep_default_na=False, na_values=val_null)

	df_salas = read_excel (directory_files + events_file , sheet_classrooms, dtype = 'str', keep_default_na=False, na_values=val_null)

	if map_groups == 1:

		df_historic = read_excel (directory_files + 'HistoricoInscriptos.xlsx', 'Datos', dtype = 'str', keep_default_na=False, na_values=val_null)
	
	if (check_classroom == 1):

	
		df_events = df_events [[v_comision, v_subcomision, v_day, v_hour_begin,
								v_hour_end, v_typology, v_mod_cod, v_section,
								v_students, v_group, v_weeks,
								v_course_code, v_year,
								g_plan_cod, v_mod_name,v_classrooms_code_guarani, v_id_event_guarani]]

									
		df_events.drop_duplicates(inplace = True)

	else:

		df_events = df_events [[v_comision, v_subcomision, v_day, v_hour_begin,
								v_hour_end, v_typology, v_mod_cod, v_section,
								v_students, v_group, v_weeks,
								v_course_code, v_year,
								g_plan_cod, v_mod_name, v_id_event_guarani]]

									
		df_events.drop_duplicates(inplace = True)

	return (df_events, df_grupos, df_courses, df_salas, df_historic)



def check_nulls(df : DataFrame, check_classrooms : int, name_file_validation):

	if check_classrooms == 1:

		df = df [[v_comision, v_subcomision, v_day, v_hour_begin, v_hour_end, 
				v_typology,v_mod_cod, v_mod_name, v_section, 
				v_students, v_group, v_weeks, 
				v_year,v_course_code, v_codigo_plan, v_classrooms_code_guarani, v_id_event_guarani]]

	else:

		df = df [[v_comision, v_subcomision, v_day, v_hour_begin, v_hour_end, 
				  v_typology,v_mod_cod, v_mod_name, v_section, 
				  v_students, v_group, v_weeks, 
				  v_year,v_course_code, v_codigo_plan, v_id_event_guarani]]

	#remove duplicated because teacher lines
	df.drop_duplicates(inplace = True)  

	#Todos os nulos, inclusive numero de alunos retirados à cabeça ... alterado para 3.0.1  
	# df[v_students] = df[v_students].fillna('0')

	df_null = df[df.isnull().any (axis=1)].copy()
	df_null.fillna('NULL', inplace = True)

	
	if not df_null.empty:

		sheet_name = 'NullValues'
		write_file (df_null, name_file_validation + '.xlsx', sheet_name)
	
	#Extract all null values
	df = df.dropna(axis=0, how ='any').copy()

	return (df)


def verify_students_null (df : DataFrame, name_file_validation : str):

	df_check = df.copy()

	df = df_check[df_check[v_students].str.isdigit()].copy()

	df_not_valid = df_check[~df_check[v_students].str.isdigit()].copy()
	
	
	df[v_students] = df[v_students].astype(int)
	df_events_wrong_number_students = df[df[v_students] <= 0].copy()
	
	df = df[df[v_students] > 0]

	if not df_not_valid.empty:

		sheet_name = 'WrongStudentsNumber'
		write_file (df_not_valid, name_file_validation + '.xlsx', sheet_name)
		
	
	if not df_events_wrong_number_students.empty:

		sheet_name = 'ZeroStudents'
		write_file (df_events_wrong_number_students, name_file_validation + '.xlsx', sheet_name)


	return (df)

def get_name_salas_btt(df_events : DataFrame, df_salas : DataFrame, name_file_validation : str):


	df = df_events.copy()

	df_salas.drop(columns=s_sala_caracteristic, inplace=True)
	df_salas.drop_duplicates(inplace = True)

	df_salas[v_classrooms_code_guarani] = df_salas[s_sala_code].str.split('_').str[-1:].str.join(',')


	df = merge(left= df, right = df_salas, how = 'left', on = v_classrooms_code_guarani, indicator = True)

	df_not_match_sala = df[df['_merge'] == 'left_only'].copy()



	df_map_classrooms = df[df['_merge'] == 'both'].copy()


	df_map_classrooms.drop(columns = ['_merge'], inplace = True)



	if not df_not_match_sala.empty:

		sheet_name = 'NotMapClassroom'
		write_file (df_not_match_sala, name_file_validation + '.xlsx', sheet_name)
	
	return (df_map_classrooms)


def replace_minutes_hours(df):

	## Round values minutes to 15min

	df[v_hour_begin] = to_datetime(df[v_hour_begin]).dt.round('15min').dt.strftime('%H:%M:%S')
	df[v_hour_end] = to_datetime(df[v_hour_end]).dt.round('15min').dt.strftime('%H:%M:%S')
		
	return (df)


def verify_hour_begin_end(df: DataFrame, name_file_validation : str):


	df_wrong_hours = df[df[v_hour_begin] >= df[v_hour_end]]
	df_correct_hours = df[df[v_hour_begin] < df[v_hour_end]]


	if not df_wrong_hours.empty:

		sheet_name = 'HourBegin>HourEnd'
		write_file (df_wrong_hours, name_file_validation + '.xlsx', sheet_name)


	return (df_correct_hours)


def sigla(name):
	new_sigla = name[0]
	for i in range(len(name)):
			if (name[i-1] == " " and name[i].isupper()):
					new_sigla += name[i]
	return new_sigla

def join_curriculum (df_events, df_courses, df_groups, check_classrooms, name_file_validation):
	
	df_courses.drop_duplicates(inplace = True)
	df_events = merge(left = df_events, right = df_courses, how = 'left', left_on = v_course_code , right_on = c_courses_code, indicator = True)

	df_events_map = df_events[df_events['_merge'] == 'both'].copy()
	df_course_not_map = df_events[df_events['_merge'] == 'left_only'].copy()


	if not df_course_not_map.empty:

		sheet_name = 'NotMapCarrera'
		write_file (df_course_not_map, name_file_validation + '.xlsx', sheet_name)	


	df_events_map.drop(columns = ['_merge', c_courses_code], inplace = True)

	#Insert Sigla de Asignatura

	df_events_map.insert(8, v_mod_acron, df_events_map[v_mod_name].map(sigla))


	# Insert PlanInfo

	df_events_map[v_plan_name] = df_events_map[v_year] + df_events_map[c_courses_name]


	# Insert GroupInfo

	df_groups = df_groups[[v_codigo_plan, v_comision, v_subcomision, v_section, g_nombre_comision]].copy()
	df_groups.drop_duplicates( keep = 'first', inplace = True)


	df_events_map = merge(df_events_map, df_groups , how = 'left', on = [v_codigo_plan, v_comision, v_subcomision, v_section],
					indicator = True )

	df_events_map_g = df_events_map[df_events_map['_merge'] == 'both'].copy()
	df_groups_not_map = df_events_map[df_events_map['_merge'] == 'left_only'].copy()


	if not df_groups_not_map.empty:

		sheet_name = 'NotMapGroups'
		write_file (df_groups_not_map, name_file_validation + '.xlsx', sheet_name)	

	df_events_map_g[v_bullet_group] = df_events_map_g[v_plan_name] + '_' + df_events_map_g[g_nombre_comision]

	df_events_map_g [v_comision]= where(df_events_map_g[v_subcomision] != '0', df_events_map_g[v_comision] + '-' + df_events_map_g[v_subcomision],
								  		   df_events_map_g[v_comision])
	
	if check_classrooms == 1:
		df_events_map_g = df_events_map_g [[v_comision, v_students, v_hour_begin, v_hour_end, v_day,
											v_mod_name, v_mod_acron, v_mod_cod,
											s_sala_name, s_sala_edificio, v_weeks, 
											v_typology,
											v_bullet_group,v_plan_name, g_plan_cod, v_year,
											c_courses_name, c_courses_sigla, v_course_code,g_nombre_comision, v_section,v_id_event_guarani]]

		df_events_map_g.insert(8, v_mod_area, 'SD')

		return(df_events_map_g)

	else:

		df_events_map_g = df_events_map_g [[v_comision, v_students, v_hour_begin, v_hour_end, v_day,
											v_mod_name, v_mod_acron, v_mod_cod,
											v_weeks, 
											v_typology,
											v_bullet_group,v_plan_name, g_plan_cod, v_year,
											c_courses_name, c_courses_sigla, v_course_code,g_nombre_comision,v_section, v_id_event_guarani]]

		df_events_map_g.insert(8, v_mod_area, 'SD')

		return(df_events_map_g)



def grouped_data (df : DataFrame, check_classrooms, check_groups):


	df.drop_duplicates(keep= 'first', inplace = True)
	#No caso de existir mais de um numero de alunos por diferentes turmas de comissão ... ordenado por maior valor de numero de alunos
	df.sort_values(by = [v_students], ascending = False, inplace = True )


	#Tres agregações:
	#1ª agregar as turmas por comissão:

	if check_classrooms == 1:
		list_series = [v_comision,v_hour_begin, v_hour_end, v_day,v_weeks, 
					   v_mod_name, v_mod_cod, v_mod_acron, v_mod_area,
					   s_sala_name, s_sala_edificio,
					   v_typology,v_id_event_guarani]
	else:

		list_series = [v_comision,v_hour_begin, v_hour_end, v_day,v_weeks, 
					   v_mod_name, v_mod_cod, v_mod_acron, v_mod_area,
					   v_typology,v_id_event_guarani]

	df[v_students] = df[v_students].astype(int)
	df = df.sort_values(by = v_students, ascending =  False)
	
	df  = group_entities(df, list_series, sep = '##')
	df[v_students] = df[v_students].str.split('##').str[0]

	'''
	2º Agregar comissões diferentes disciplinas...para o mesmo id de Guarani;
	 - Neste caso são somados os numeros de alunos !!!
	 - No caso de Guarani so admitir um espaço agregar tambem por sala e edificio !!!
	'''

	if check_classrooms == 1:
		list_series = [v_hour_begin, v_hour_end, v_day,
					   v_weeks, s_sala_name, s_sala_edificio, v_id_event_guarani]
	
	else:

		list_series = [v_hour_begin, v_hour_end, v_day,
					   v_weeks, v_id_event_guarani] 
		
	df  = group_entities(df, list_series, sep = ';;')


	#After agregatte comissiones compartidas somar o numero de alunos das diferentes comissoes.
	df[v_students] = df[v_students].apply(lambda x: sum(map(int, x.split(';;'))))
	df[v_students] = df [v_students].astype(str)

	df [v_type_comission] =  where((df[v_comision].str.count(';;') + 1 > 1), #mais de uma comissão
									  1, 0)
	
	#Comissiones compartidas - manage classroom 305 Magno;;305Magno ... exemplo de asignacion 12313
	
	#Para mais tarde gerir dominantes e dominadas
	df [v_mod_comun] = where((df[v_comision].str.count(';;') + 1 > 1) & #se tiver mais de uma comissão
									 (df[v_mod_cod].apply(lambda x: ';;'.join(set(x.split(';;')))).str.count(';;') +1 >1), # se tiver mais de uma disciplina
									  1, 0)
	
	
	#Podera ainda ser compartida...para mesmos grupos... mesma disciplina !!!!! enquadra-se na primeira opção
	#Podera ainda ser compartida .... para mesmos grupos .... diferentes disciplinas !!!! escolher disciplina a apresentar(Disciplina a apresentar a que tem mais alunos)

	
	return df

def insert_name_section (df: DataFrame):

	# A verificar como serão as designações de Turno:
	# No caso de comissão compartida fica inserir a string C_Compartida...
	# No caso de comissãp não compartida segue o padrão de Comissão_SubComissãp_IdGuaraní
 
	df [v_section]= where((df[v_type_comission] == 1) , 'Com.Comp_' + df[v_id_event_guarani],
							 df[v_comision] + '_' + df[v_id_event_guarani])


	return df

def insert_name_acad_term (df, academicTerm):

	df.insert(0, v_academic_term, academicTerm)

	return (df)



def final_weeks(df):

	df['week_begin'] = df[v_weeks].str.split(',').str[0]
	df['week_end'] = df[v_weeks].str.split(',').str[1]
	df = weekly_date(df, ['week_begin', 'week_end'])
	df = asign_weeks (df, 'week_begin', 'week_end')
	df[v_weeks] = df['WEEKS_EVENT']
	df.drop(columns = 'WEEKS_EVENT', inplace = True)
	
	# raise ParserError("Unknown string format: %s", timestr)

	return (df)



def selec_data_comissiones_compartidas_to_import(df: DataFrame, check_classroom : int):

	if check_classroom == 1:

		df_to_import = df[[v_academic_term, v_section, v_students, v_hour_begin, v_hour_end,
						v_day, v_mod_name, v_mod_acron, v_mod_cod, v_mod_area, s_sala_name, s_sala_edificio, v_weeks,
						v_typology, v_bullet_group, v_plan_name, g_plan_cod, v_year, c_courses_name, c_courses_sigla, v_course_code, v_type_comission]].copy()

		df_to_import[s_sala_name] = where(df_to_import[v_type_comission] == '1', df_to_import[s_sala_name].str.split(';;').str[0], df_to_import[s_sala_name])
		df_to_import[s_sala_edificio] = where(df_to_import[v_type_comission] == '1', df_to_import[s_sala_edificio].str.split(';;').str[0], df_to_import[s_sala_edificio])

	else:

		df_to_import = df[[v_academic_term, v_section, v_students, v_hour_begin, v_hour_end,
						   v_day, v_mod_name, v_mod_acron, v_mod_cod, v_mod_area, v_weeks,
						   v_typology, v_bullet_group, v_plan_name, g_plan_cod, v_year, c_courses_name, c_courses_sigla, v_course_code, v_type_comission]].copy()


	#To remove separator compartidas
	df_to_import [v_bullet_group] = df_to_import [v_bullet_group].str.replace('##',';;')
	df_to_import [v_plan_name] = df_to_import [v_plan_name].str.replace('##',';;')
	df_to_import [g_plan_cod] = df_to_import [g_plan_cod].str.replace('##',';;')
	df_to_import [v_year] = df_to_import [v_year].str.replace('##',';;')
	df_to_import [c_courses_name] = df_to_import [c_courses_name].str.replace('##',';;')
	df_to_import [c_courses_sigla] = df_to_import [c_courses_sigla].str.replace('##',';;')
	df_to_import [v_course_code] = df_to_import [v_course_code].str.replace('##',';;')



	df_to_import[v_type_comission] = df_to_import[v_type_comission].astype(str)


	#Select only one module to generate insert event on BC.
	df_to_import[v_mod_name] = where(df_to_import[v_type_comission] == '1', df_to_import[v_mod_name].str.split(';;').str[0], df_to_import[v_mod_name]) 
	df_to_import[v_mod_cod] = where(df_to_import[v_type_comission] == '1', df_to_import[v_mod_cod].str.split(';;').str[0], df_to_import[v_mod_cod]) 
	df_to_import[v_mod_acron] = where(df_to_import[v_type_comission] == '1', df_to_import[v_mod_acron].str.split(';;').str[0], df_to_import[v_mod_acron]) 
	df_to_import[v_mod_area] = where(df_to_import[v_type_comission] == '1', df_to_import[v_mod_area].str.split(';;').str[0], df_to_import[v_mod_area])


	df_to_import[v_typology] = where(df_to_import[v_type_comission] == '1', df_to_import[v_typology].str.split(';;').str[0], df_to_import[v_typology])

	df_to_import.insert(0, v_event_name, df_to_import[v_section] + '_' + df_to_import[v_mod_name])

	return df_to_import


# def prepare_data_xml_compartidas (df : DataFrame):

# 	df = df [[v_mod_cod, v_plan_name, g_plan_cod]].copy()

# 	df_view = df.copy()

# 	return df


def map_students_number_historic (df_event : DataFrame, df_historic : DataFrame):

	df_historic.rename(columns = {v_students : 'students_historic'}, inplace=True)
	df_event [v_students] = df_event[v_students].astype(int)
	df_event = merge(left = df_event, right = df_historic, how = 'left', on = [v_mod_cod, v_typology, v_section, v_mod_name, g_nombre_comision, g_plan_cod], indicator=True )

	df_event['students_historic'].fillna('0', inplace = True)
	df_event['students_historic'] = df_event['students_historic'].astype(int) 
	df_event[v_students] = where((df_event[v_students] < 10) & (df_event['_merge'] == 'both') & (df_event['students_historic'] > df_event[v_students]), 
									df_event['students_historic'], df_event[v_students] )

	df_event.drop(columns=[g_nombre_comision, v_section, 'students_historic', '_merge'], inplace = True)


	return(df_event)


def filter_events_grouped_students_null (df : DataFrame, name_file_validation : str):

	# Numero de alunos so pode ser 0 ou maior que zero, já retirados em metodo anterior numero de alunos inferior a Zero ou Zero...
	
	df_events_to_import = df[df[v_students] != '0']

	df_events_not_import = df[df[v_students] == '0']

	if not df_events_to_import.empty:

		sheet_name = 'EventToImport'
		write_file (df_events_to_import, name_file_validation + '.xlsx', sheet_name)

	if not df_events_not_import.empty:

		sheet_name = 'EventStudentZero'
		write_file (df_events_not_import, name_file_validation + '.xlsx', sheet_name)
	


	return (df_events_to_import)


def create_BEST_Classrooms (df_classrooms : DataFrame, folder : str, process_code: str):
	# Manage Buildings

	df_classrooms = df_classrooms[[s_sala_name, s_sala_caracteristic, s_sala_edificio]].copy()
	

	df_classrooms.rename(columns = {s_sala_name : v_classroom_name,
							        s_sala_caracteristic : v_classroom_characteristic,
									s_sala_edificio : v_classroom_building}, inplace=True)

	

	df_classrooms[v_classroom_characteristic].fillna('', inplace=True)
	df_classrooms_buildings = df_classrooms[[v_classroom_name, v_classroom_building]].copy()

	df_classrooms_buildings.sort_values(by=[v_classroom_building, v_classroom_name], inplace=True, ascending= True)

	series_to_group = v_classroom_building
	#Ao agrupar por entidades unicas já estou a exluir salas repetidas, por causa das repetições de sala. derivado de ser inserida linha por caracteristica de sala...
	df_classrooms_buildings = group_unique_entities(df_classrooms_buildings,series_to_group, sep=',')

	
	file_name = 'BEST_Classrooms'
	sheet_name = 'BuildingsBEST'
	name_file_classrooms_best = folder + '/' + file_name + process_code

	df_classrooms_buildings.to_excel(name_file_classrooms_best + '.xlsx', sheet_name, index = False,freeze_panes=(1,0))
	
	# Manage Characteristic
	df_classrooms_caracteristic = df_classrooms[[v_classroom_name, v_classroom_characteristic]].copy()

	df_classrooms_caracteristic.sort_values(by=[v_classroom_characteristic, v_classroom_name], inplace=True, ascending= True)

	series_to_group = v_classroom_characteristic
	df_classrooms_caracteristic = group_unique_entities(df_classrooms_caracteristic,series_to_group, sep=',')

	sheet_name = 'CharacteristicBEST'
	write_file (df_classrooms_caracteristic, name_file_classrooms_best + '.xlsx', sheet_name)

	# Manage Classrooms
	df_classrooms_unique = df_classrooms[[v_classroom_name, v_classroom_characteristic, v_classroom_building]].copy()

	df_classrooms_unique.sort_values(by=[v_classroom_building, v_classroom_name], inplace=True, ascending= True)

	series_to_group = [v_classroom_building, v_classroom_name]
	df_classrooms_unique = group_unique_entities(df_classrooms_unique,series_to_group, sep=',')

	sheet_name = 'ClassroomsBEST'
	write_file (df_classrooms_unique, name_file_classrooms_best + '.xlsx', sheet_name)


	# Add Leyenda 
	df_leyenda = DataFrame(columns = [v_column_value_asignacion, v_column_entity_asignacion])

	#Insert Name file Events
	df_leyenda = df_leyenda.append({ v_column_value_asignacion : '0', 
									 v_column_entity_asignacion : v_bulding_best,
									 }, ignore_index = True)


	df_leyenda = df_leyenda.append({ v_column_value_asignacion : '1', 
									 v_column_entity_asignacion : v_characteristic_best,
									 }, ignore_index = True)

	df_leyenda = df_leyenda.append({ v_column_value_asignacion : '2', 
									 v_column_entity_asignacion : v_classroom_best,
									 }, ignore_index = True)

	sheet_name = 'LeyendaAddClassrooms'
	write_file (df_leyenda, name_file_classrooms_best + '.xlsx', sheet_name)

	return()


def check_classrooms_without_ID (df : DataFrame, name_file_validation):

	df_no_code = df[df[[s_sala_code]].isnull().any (axis=1)].copy()
	df_no_code = df_no_code.drop_duplicates()
	
	df_no_code = df_no_code.drop_duplicates().sort_values(by=[s_sala_name, s_sala_edificio])

	sheet_name = 'ClassWithoutCode'
	write_file (df_no_code, name_file_validation + '.xlsx', sheet_name)

	df_with_code = df[df[[s_sala_code]].notnull().all (axis=1)].copy()


	df_with_code_error = df_with_code[df_with_code[s_sala_code].str.count('_') != 1].copy()
	df_with_code_error = df_with_code_error.drop_duplicates()

	sheet_name = 'ClassWrongCode'
	write_file (df_with_code_error, name_file_validation + '.xlsx', sheet_name)

	df_classroom_code_guarani = df_with_code[df_with_code[s_sala_code].str.count('_') == 1].copy()

	df_classroom_with_id_guarani = df_classroom_code_guarani[[s_sala_name, s_sala_code, s_sala_edificio]].copy()
	df_classroom_with_id_guarani.drop_duplicates(inplace=True)

	sheet_name = 'ClassCodeOK'
	write_file (df_classroom_with_id_guarani, name_file_validation + '.xlsx', sheet_name)


	return(df_classroom_code_guarani)


def create_add_classrooms (df_events : DataFrame, folder : str, process_code: str):

	df = df_events.copy()


	df.rename (columns = {v_mod_name : v_module_name,
	                      v_mod_cod : v_module_code,
						  v_typology : v_module_typology, 
						  v_bullet_group : v_student_group_name,
						  v_section :v_sectionName }, inplace = True )

	df = df [[v_module_name, v_module_code, v_module_typology, v_student_group_name, v_sectionName,
	          v_plan_name, v_codigo_plan, v_year, c_courses_name, v_course_code, v_type_comission, v_students, v_hour_begin, v_hour_end,
			  v_day, v_weeks ]].copy()

	df [v_value_priority], df[v_classroom_priority] = ['', '']
	df [v_value_alternative], df[v_classroom_alternative] = ['', ''] 



	name_file = folder + '/AddClassrooms' + process_code
	df.to_excel(name_file + '.xlsx', 'AddClassrooms', index = False,freeze_panes=(1,0))





