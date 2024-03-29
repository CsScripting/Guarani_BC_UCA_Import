import os.path
from numpy import True_

from pandas.core.frame import DataFrame
from general_mod import *
from variables_mod import *
import xlsxwriter
class HaltException(Exception): pass

# import qgrid as gd

def cleaning_data (df):
	
	df = df.apply(lambda x: x.str.strip())
	df.columns = df.columns.str.strip()
	df = df.replace(r'^\s*$', np.nan, regex=True)
	#valid_data =  df[df.notnull().all(axis =1)]
	#invalid_data = df[df.isnull().any(axis =1)]
	
	return (df)


def group_entities(df, list_series, sep = ',', sort_flag = True):
	
	df = df.applymap(str)
	df.set_index (list_series, inplace=True)
	df = df.groupby (level = list_series, sort = sort_flag).agg(sep.join)
	df.reset_index(inplace=True)
	
	return df


def read_data(events_file, events_spreed_sheet, \
			  groups_file, groups_spreed_sheet,courses_spreed_sheet = 'Carreras',\
			  validacion = False):
	try:
			
		flag_validacion_columns = False



		# Manage values 'NA'
		val_null = ['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A N/A', 
				   '#N/A', 'N/A', 'n/a', '', '#NA', 'NULL', 'null', 'NaN', '-NaN', 'nan', '-nan', '']


		df_events = pd.read_excel ('./Files/' + events_file, events_spreed_sheet, dtype = 'str', keep_default_na=False, na_values=val_null)
		df_courses = pd.read_excel ('./Files/' + events_file, courses_spreed_sheet, dtype = 'str', keep_default_na=False, na_values=val_null)

		df_grupos = pd.read_excel ('./Files/' + groups_file, groups_spreed_sheet, dtype = 'str', keep_default_na=False, na_values=val_null)
		df_salas = pd.read_excel ('./Files/' + events_file , 'Salas', dtype = 'str', keep_default_na=False, na_values=val_null)
		


		if (validacion == True):


			# FORMAT_DATA_VALIDACION
			col_names_events = df_events.columns.values.tolist()
			col_names_grupos = df_grupos.columns.values.tolist()
			col_names_salas = df_salas.columns.values.tolist()
			col_names_courses = df_courses.columns.values.tolist()
			
			
			flag_validacion, errorHeader, errorBody = format_validacion (col_names_events, col_names_grupos, col_names_salas, col_names_courses)
	

			if (flag_validacion == 'Wrong_Columns'):


				return (flag_validacion_columns, errorHeader, errorBody)

			
			else:

				flag_validacion_columns = True

				return (flag_validacion_columns, '', '')
			
		else:

			df_events = df_events [[v_comision, v_subcomision, v_day, v_hour_begin,
									v_hour_end, v_typology, v_mod_cod, v_section,
									v_students, v_group, v_weeks,
									v_course_code, v_year,
									g_plan_cod, v_mod_name,v_classrooms_code_guarani, v_id_event_guarani]]

								 
			df_events.drop_duplicates(inplace = True)

			return (df_events, df_grupos, df_courses, df_salas)


		
	except ValueError as e:

	
		if (str(e) == "Worksheet named 'Salas' not found"):


			flag_validacion_columns = False
			return (flag_validacion_columns, 'Error Sheet File', 'File Horarios must have sheets named Salas, and Carrerras.')


		elif (str(e) == "Worksheet named 'Carreras' not found"):


			flag_validacion_columns = False
			return (flag_validacion_columns, 'Error Sheet File', 'File Horarios must have sheets named Salas, and Carreras.')
				

		else: 

			error =  str(e)

			flag_validacion_columns = False

			return(flag_validacion_columns,'Error Sheet File', error)
			
				


	# Verify if file exist or Folder to store File
	except FileNotFoundError as e:


		error =  str(e)


		flag_validacion_columns = False

		return(flag_validacion_columns, 'File Not Found', error)






def format_validacion (col_events,  col_grupos, col_salas, col_course ):


	columns_files = []
	columns_files.insert(0, col_events)
	columns_files.append (col_grupos)
	columns_files.append (col_salas)
	columns_files.append (col_course)
	
	
	columns_values_original = []

	columns_events = [v_comision, v_subcomision, v_day, v_hour_begin,
					  v_hour_end, v_typology, v_mod_cod, v_section,
					  v_students, v_group, v_teacher, v_weeks,
					  v_course_code, v_year,
					  g_plan_cod, v_mod_name, v_classrooms_code_guarani, v_id_event_guarani]

	columns_values_original.insert(0, columns_events)
	
	
	
	columns_grupos = [g_name, g_plan_cod, g_students, g_max_limit, g_cons_limit,
					 v_comision, v_subcomision, g_nombre_comision,
					 v_section, g_agreggated_groups]
										
	
	columns_values_original.append(columns_grupos)
	
	columns_salas = [s_sala_name, s_sala_code, s_sala_edificio]
	
	columns_values_original.append(columns_salas)

	columns_courses = [c_courses_name,c_courses_sigla, c_courses_code]
	
	columns_values_original.append (columns_courses)



	for i in range (4):
	
		check_column_names = all(elem in columns_files[i] for elem in columns_values_original[i])

		if not check_column_names and i == 0:
				
			
			return ('Wrong_Columns', 'Wrong_Columns (Schedules)', columns_events )
			
				
		elif not check_column_names and i == 1:
		
			
			return ('Wrong_Columns', 'Wrong_Columns (Groups)', columns_grupos)

		elif not check_column_names and i == 2:
			
			return ('Wrong_Columns', 'Wrong_Columns (Salas)', columns_salas)
			
				
		elif not check_column_names and i == 3:

			return ('Wrong_Columns','Wrong_Columns (Carreras)', columns_courses)

	return('Columns_OK', '', '')

def check_nulls(df):


	df = df [[v_comision, v_subcomision, v_day, v_hour_begin, v_hour_end, 
			  v_typology,v_mod_cod, v_mod_name, v_section, 
			  v_students, v_group, v_weeks, 
			  v_year,v_course_code, v_codigo_plan, v_classrooms_code_guarani, v_id_event_guarani]]

	
	#remove duplicated because teacher lines
	df.drop_duplicates(inplace = True)  
	  
	df[v_students] = df[v_students].fillna('0')

	df_null = df[df.isnull().any (axis=1)].copy()
	df_null.fillna('NULL', inplace = True)

	
	if not df_null.empty:


		dir_file = './New_Files'
		timestr = t.strftime("_%Y%m%d_%H%M%S")

		if os.path.isdir(dir_file):

			df_null.to_excel('./New_Files/NullValues' + timestr + '.xlsx', 'NullValues', index = False )

		else:
			os.mkdir(dir_file)
			df_null.to_excel('./New_Files/NullValues' + timestr + '.xlsx', 'NullValues', index = False )
	
	#Extract all null values
	df = df.dropna(axis=0, how ='any').copy()
	  

	return (df)

	

def verify_students_null (df):

	df[v_students] = df[v_students].astype(int)
	df_events_wrong_number_students = df[df[v_students] <= 0].copy()
	
	df = df[df[v_students] >= 0]
		
	
	if not df_events_wrong_number_students.empty:

		dir_file = './New_Files'
		timestr = t.strftime("_%Y%m%d_%H%M%S")

		if os.path.isdir(dir_file):

			df_events_wrong_number_students.to_excel('./New_Files/StudentsNull' + timestr + '.xlsx', 'StudentsNull', index = False )

		else:
			os.mkdir(dir_file)
			df_events_wrong_number_students.to_excel('./New_Files/StudentsNull' + timestr + '.xlsx', 'StudentsNull', index = False )


	return (df)

def get_name_salas_btt(df_events, df_salas):

	flag_salas = False

	df = df_events.copy()


	df_salas[v_classrooms_code_guarani] = df_salas[s_sala_code].str.split('_').str[-1:].str.join(',')


	df = pd.merge(left= df, right = df_salas, how = 'left', on = v_classrooms_code_guarani, indicator = True)

	df_not_match_sala = df[df['_merge'] == 'left_only'].copy()



	df_map_classrooms = df[df['_merge'] == 'both'].copy()


	df_map_classrooms.drop(columns = ['_merge'], inplace = True)



	if not df_not_match_sala.empty:


		# Verificar a possibilidade de mapear as salas

		dir_file = './New_Files'
		timestr = t.strftime("_%Y%m%d_%H%M%S")

		if os.path.isdir(dir_file):

			path_file = './New_Files/Asign_Salas'+ timestr + '.xlsx'
			df_not_match_sala.to_excel(path_file, 'NotMatchSalas', index = False )

		else:

			path_file = './New_Files/Asign_Salas'+ timestr + '.xlsx'
			df_not_match_sala.to_excel(path_file, 'NotMatchSalas', index = False )
		



	return (df_map_classrooms)


def replace_minutes_hours(df):

	## Round values minutes to 15min

	df[v_hour_begin] = pd.to_datetime(df[v_hour_begin]).dt.round('15min').dt.strftime('%H:%M:%S')
	df[v_hour_end] = pd.to_datetime(df[v_hour_end]).dt.round('15min').dt.strftime('%H:%M:%S')
		
	return (df)


def verify_hour_begin_end(df):

	path_file = './New_Files/Incomplete_Data.xlsx'
	

	if os.path.exists(path_file):
		
		os.remove(path_file)

	df_wrong_hours = df[df[v_hour_begin] >= df[v_hour_end]]
	df_correct_hours = df[df[v_hour_begin] < df[v_hour_end]]


	if not df_wrong_hours.empty:
	

		if os.path.isfile(path_file):
				
				write_exist_file(df_wrong_hours, './New_Files/Incomplete_Data.xlsx', 'HourBegin>HourEnd')
				
		else:
		
				df_wrong_hours.to_excel('./New_Files/Incomplete_Data.xlsx', 'HourBegin>HourEnd', index = False )


	return (df_correct_hours, df_wrong_hours)


def sigla(name):
	new_sigla = name[0]
	for i in range(len(name)):
			if (name[i-1] == " " and name[i].isupper()):
					new_sigla += name[i]
	return new_sigla

def join_curriculum (df_events, df_courses, df_groups):
	
	df_events = pd.merge(left = df_events, right = df_courses, how = 'left', left_on = v_course_code , right_on = c_courses_code, indicator = True)

	df_events_map = df_events[df_events['_merge'] == 'both'].copy()
	df_course_not_map = df_events[df_events['_merge'] == 'left_only'].copy()


	if not df_course_not_map.empty:
			

		path_file = './New_Files/Incomplete_Data.xlsx'

		if os.path.isfile(path_file):
				
				write_exist_file(df_course_not_map, './New_Files/Incomplete_Data.xlsx', 'NotMapCarrera')
				
		else:
		
				df_course_not_map.to_excel('./New_Files/Incomplete_Data.xlsx', 'NotMapCarrera', index = False )

	df_events_map.drop(columns = ['_merge', c_courses_code], inplace = True)

	#Insert Sigla de Asignatura

	df_events_map.insert(8, v_mod_acron, df_events_map[v_mod_name].map(sigla))


	# Insert PlanInfo

	df_events_map[v_plan_name] = df_events_map[v_year] + df_events_map[c_courses_name]


	# Insert GroupInfo

	df_groups = df_groups[[v_codigo_plan, v_comision, v_subcomision, v_section, g_nombre_comision]].copy()
	df_groups.drop_duplicates( keep = 'first', inplace = True)


	df_events_map = pd.merge(df_events_map, df_groups , how = 'left', on = [v_codigo_plan, v_comision, v_subcomision, v_section],
					indicator = True )

	df_events_map_g = df_events_map[df_events_map['_merge'] == 'both'].copy()
	df_groups_not_map = df_events_map[df_events_map['_merge'] == 'left_only'].copy()


	if not df_groups_not_map.empty:
			

		path_file = './New_Files/Incomplete_Data.xlsx'

		if os.path.isfile(path_file):
				
				write_exist_file(df_groups_not_map, './New_Files/Incomplete_Data.xlsx', 'NotMapGroups')
				
		else:
		
				df_groups_not_map.to_excel('./New_Files/Incomplete_Data.xlsx', 'NotMapGroups', index = False)


	


	df_events_map_g[v_bullet_group] = df_events_map_g[v_plan_name] + '_' + df_events_map_g[g_nombre_comision]

	df_events_map_g [v_comision]= np.where(df_events_map_g[v_subcomision] != '0', df_events_map_g[v_comision] + '-' + df_events_map_g[v_subcomision],
							      		   df_events_map_g[v_comision])
 
	df_events_map_g = df_events_map_g [[v_comision, v_students, v_hour_begin, v_hour_end, v_day,
										v_mod_name, v_mod_acron, v_mod_cod,
										s_sala_name, s_sala_edificio, v_weeks, 
										v_typology,
										v_bullet_group,v_plan_name, g_plan_cod, v_year,
										c_courses_name, c_courses_sigla, v_course_code, v_id_event_guarani]]

	df_events_map_g.insert(8, v_mod_area, 'SD')

	return(df_events_map_g)



def grouped_data (df : DataFrame):


	df.drop_duplicates(keep= 'first', inplace = True)
	#No caso de existir mais de um numero de alunos por diferentes turmas de comissão ... ordenado por maior valor de numero de alunos
	df.sort_values(by = [v_students], ascending = False, inplace = True )


	#Tres agregações:
	#1ª agregar as turmas por comissão:

	list_series = [v_comision,v_hour_begin, v_hour_end, v_day,v_weeks, 
				   v_mod_name, v_mod_cod, v_mod_acron, v_mod_area,
				   s_sala_name, s_sala_edificio,
				   v_typology,v_id_event_guarani]

	df  = group_entities(df, list_series, sep = '##')

	df[v_students] = df[v_students].str.split('##').str[0]

	# 2º Agregar comissões que por vezes têm as mesma turmas associadas a diferentes disciplinas...para o mesmo id de Guarani
	# Neste caso são somados os numeros de alunos:

	list_series = [v_hour_begin, v_hour_end, v_day,
				   v_weeks, v_id_event_guarani]
	
	df  = group_entities(df, list_series, sep = ';;')


	#After agregatte comissiones compartidas somar o numero de alunos das diferentes comissoes.
	df[v_students] = df[v_students].apply(lambda x: sum(map(int, x.split(';;'))))
	df[v_students] = df [v_students].astype(str)

	df [v_type_comission] =  np.where((df[v_comision].str.count(';;') + 1 > 1), #mais de uma comissão
									  1, 0)
	
	#Para mais tarde gerir dominantes e dominadas
	df [v_mod_comun] = np.where((df[v_comision].str.count(';;') + 1 > 1) & #se tiver mais de uma comissão
	                                 (df[v_mod_cod].apply(lambda x: ';;'.join(set(x.split(';;')))).str.count(';;') +1 >1), # se tiver mais de uma disciplina
									  1, 0)
	
	
	#Podera ainda ser compartida...para mesmos grupos... mesma disciplina !!!!! enquadra-se na primeira opção
	#Podera ainda ser compartida .... para mesmos grupos .... diferentes disciplinas !!!! escolher disciplina a apresentar(Disciplina a apresentar a que tem mais alunos)

	
	return df

def insert_name_section (df: DataFrame):

	# A verificar como serão as designações de Turno:

	# No caso de comissão compartida fica inserir a string C_Compartida...
	# No caso de comissãp não compartida segue o padrão de Comissão_SubComissãp_IdGuaraní
 
	df [v_section]= np.where((df[v_type_comission] == 1) , 'Com.Comp_' + df[v_id_event_guarani],
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
	
	return (df)



def selec_data_comissiones_compartidas_to_import(df: DataFrame):

	df_to_import = df[[v_academic_term, v_section, v_students, v_hour_begin, v_hour_end,
             v_day, v_mod_name, v_mod_acron, v_mod_cod, v_mod_area, s_sala_name, s_sala_edificio, v_weeks,
             v_typology, v_bullet_group, v_plan_name, g_plan_cod, v_year, c_courses_name, c_courses_sigla, v_course_code, v_type_comission]].copy()

	df_to_import [v_bullet_group] = df_to_import [v_bullet_group].str.replace('##',';;')
	df_to_import [v_plan_name] = df_to_import [v_plan_name].str.replace('##',';;')
	df_to_import [g_plan_cod] = df_to_import [g_plan_cod].str.replace('##',';;')
	df_to_import [v_year] = df_to_import [v_year].str.replace('##',';;')
	df_to_import [c_courses_name] = df_to_import [c_courses_name].str.replace('##',';;')
	df_to_import [c_courses_sigla] = df_to_import [c_courses_sigla].str.replace('##',';;')
	df_to_import [v_course_code] = df_to_import [v_course_code].str.replace('##',';;')



	df_to_import[v_type_comission] = df_to_import[v_type_comission].astype(str)



	df_to_import[v_mod_name] = np.where(df_to_import[v_type_comission] == '1', df_to_import[v_mod_name].str.split(';;').str[0], df_to_import[v_mod_name]) 
	df_to_import[v_mod_cod] = np.where(df_to_import[v_type_comission] == '1', df_to_import[v_mod_cod].str.split(';;').str[0], df_to_import[v_mod_cod]) 
	df_to_import[v_mod_acron] = np.where(df_to_import[v_type_comission] == '1', df_to_import[v_mod_acron].str.split(';;').str[0], df_to_import[v_mod_acron]) 
	df_to_import[v_mod_area] = np.where(df_to_import[v_type_comission] == '1', df_to_import[v_mod_area].str.split(';;').str[0], df_to_import[v_mod_area])

	df_to_import[s_sala_name] = np.where(df_to_import[v_type_comission] == '1', df_to_import[s_sala_name].str.split(';;').str[0], df_to_import[s_sala_name])
	df_to_import[s_sala_edificio] = np.where(df_to_import[v_type_comission] == '1', df_to_import[s_sala_edificio].str.split(';;').str[0], df_to_import[s_sala_edificio])

	df_to_import[v_typology] = np.where(df_to_import[v_type_comission] == '1', df_to_import[v_typology].str.split(';;').str[0], df_to_import[v_typology])

	df_to_import.insert(0, v_event_name, df_to_import[v_section] + '_' + df_to_import[v_mod_name])





	return df_to_import


# def prepare_data_xml_compartidas (df : DataFrame):

# 	df = df [[v_mod_cod, v_plan_name, g_plan_cod]].copy()



# 	df_view = df.copy()

# 	return df