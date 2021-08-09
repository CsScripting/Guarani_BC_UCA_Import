import pandas as pd
import numpy as np
import configparser as cp
from configparser import SafeConfigParser
import time as t


v_day = 'dia_semana'
v_event_id = 'ID'
v_event_name = 'EventName'
v_hour_begin = 'hora_inicio'
v_hour_end  = 'hora_finalizacion'
v_typology = 'tipologia'
v_mod_cod = 'codigo_asignatura'
v_mod_name = 'nombre_asignatura'
v_group = 'grupo'
v_bullet_group = 'grupo_bullet'
v_section = 'turno'
v_section_number = 'numero_turnos'
v_students = 'numero_alumnos'
v_teacher = 'codprof'
v_week_load = 'WeekLoadName'
v_weeks = 'semanas'
v_comision = 'comision'
v_subcomision = 'subcomision'
v_year = 'curso'
v_plan = 'Plan'
v_slot = 'slots'
v_repeticion = 'repetition'
v_group_new = 'Group'
v_codigo_plan = 'codigo_plan'
v_classrooms = 'aula'
v_classrooms_type = 'espacio_tipo_guarani'
v_classrooms_code_guarani = 'espacio'

v_mod_area = 'area_academica'

v_mod_acron = 'acronym_module'

v_hour_begin_min = 'hora_inicio_m'
v_hour_end_min = 'hora_fin_m'
v_course_code = 'carrera'


v_event_name = 'nombre_evento'
v_academic_term = 'periodo_BTT'


#Variables File Groups
g_name = 'nombre'
g_plan_cod = 'codigo_plan'
g_students = 'cupo'
g_max_limit = 'limitemaximo'
g_cons_limit = 'limiteconsecutivo'
g_nombre_comision = 'nombre_split'
g_agreggated_groups = 'teoria_unif'

#Variables Planes

v_plan_name = 'PlanName'

#Variables Courses

c_courses_name = 'NombreCarrera'
c_courses_code = 'CodigoCarrera'
c_courses_sigla = 'SiglaCarrera'



#Variables_salas

s_sala_name = 'NombreSala'
s_sala_code = 'CodigoSala'
s_sala_edificio = 'Edificio'

s_caraceristic = 'Caracteristicas'
s_name_classrooms = 'Nombres'
s_name_classroom = 'Nombre_Sala'
s_name_update_classroom = 'Nombre_Update'
s_name_btt = 'aula_btt'

#Variables_Validation_Salas
s_pract_typology = 'pract_sigla'
s_id_guarani = 'id_salas'

#variable_Validtion_Students
st_id_student_number = 'id_students'
st_number_students = 'alumnos_historico'


# -- variables -END- #



class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


#Variables_XML

xml_header = '<?xml version="1.0"?>\n\
<Schedule xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n <Events>\n'
xml_footer = '\n</Events>\n</Schedule>'