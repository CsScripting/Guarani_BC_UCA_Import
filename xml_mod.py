from variables_mod import *
from library import(
	codecs
)


def xml_btt (df, check_classrooms):

	xml_write = []

	for row in df.index:

		name_event = df[v_event_name]
		academic_term = df[v_academic_term]

		section_name = df[v_section]
		students = df[v_students]
		hour_begin = df[v_hour_begin]
		hour_end = df[v_hour_end]
		day = df[v_day]
		mod_name = df[v_mod_name]
		mod_acron = df[v_mod_acron]
		mod_code = df[v_mod_cod]
		mod_area = df[v_mod_area]
		if check_classrooms == 1:
			sala_name = df[s_sala_name]
			sala_edif = df[s_sala_edificio]
		weeks = df[v_weeks]
		typologie = df[v_typology]

		count_groups = df[v_bullet_group].count(';;') + 1

		st_group = df[v_bullet_group].split(';;')
		plan_name = df[v_plan_name].split(';;')
		plan_cod = df[g_plan_cod].split(';;')
		year = df[v_year].split(';;')
		carrera_name = df[c_courses_name].split(';;')
		carrera_acron = df[c_courses_sigla].split(';;')
		carrera_code = df[v_course_code].split(';;')

		count_carreras = df[c_courses_name].count(';;') + 1



		if (row == v_course_code):

			validate_group = list()

			xml_write.append(' <EventXmlRepresentation>') 
			xml_write.append('   <Name>{0}</Name>'.format(name_event.strip()))
			xml_write.append('   <AcademicTermId>{0}</AcademicTermId>'.format(academic_term.strip()))
			xml_write.append('   <WLSSectionName>{0}</WLSSectionName>'.format(section_name.strip()))
			xml_write.append('   <WLSSectionConnector />')
			xml_write.append('   <NumberStudents>{0}</NumberStudents>'.format(students.strip()))
			xml_write.append('   <StartTime>{0}</StartTime>'.format(hour_begin.strip()))
			xml_write.append('   <EndTime>{0}</EndTime>'.format(hour_end.strip()))
			xml_write.append('   <Day>{0}</Day>'.format(day.strip()))
			xml_write.append('   <Module>')
			xml_write.append('     <Name>{0}</Name>'.format(mod_name.strip()))
			xml_write.append('     <Acronym>{0}</Acronym>'.format(mod_acron.strip()))
			xml_write.append('     <Code>{0}</Code>'.format(mod_code.strip()))
			xml_write.append('     <ScientificArea> <Name>{0}</Name> </ScientificArea>'.format(mod_area.strip()))
			xml_write.append('   </Module>')
			
			if check_classrooms == 1:
				xml_write.append('   <Classrooms>')
				xml_write.append('     <Classroom>')
				xml_write.append('       <Name>{0}</Name>'.format(sala_name.strip()))
				xml_write.append('     	 <Building>')
				xml_write.append('         <Name>{0}</Name>'.format(sala_edif.strip()))
				xml_write.append('     	 </Building>')
				xml_write.append('     </Classroom>')
				xml_write.append('   </Classrooms>')
			else:
				xml_write.append('   <Classrooms />')

			xml_write.append('   <Teachers />')
			xml_write.append('   <Weeks>')
			week_insert = weeks.split(',')
			for value in week_insert:
				xml_write.append('     <Week>')
				xml_write.append('      <StartDate>{0}</StartDate>'.format(value.strip()))
				xml_write.append('     </Week>')
			xml_write.append('   </Weeks>')
			xml_write.append('   <Typologies>')
			xml_write.append('     <Typology>')
			xml_write.append('      <Name>{0}</Name>'.format(typologie.strip()))
			xml_write.append('     </Typology>')
			xml_write.append('   </Typologies>')
			xml_write.append('   <StudentGroups>')
			for i in range (count_groups):
				
				if ((i == 0) | (st_group[i] not in validate_group)):

					xml_write.append('     <StudentGroup>')
					xml_write.append('      <Name>{0}</Name>'.format(st_group[i].strip()))
					xml_write.append('      <CurricularPlan>')
					xml_write.append('       <Name>{0}</Name>'.format(plan_name[i].strip()))
					xml_write.append('       <Code>{0}</Code>'.format(plan_cod[i].strip()))
					xml_write.append('       <Year>{0}</Year>'.format(year[i].strip()))
					xml_write.append('       <Course>')
					xml_write.append('        <Name>{0}</Name>'.format(carrera_name[i].strip()))
					xml_write.append('        <Acronym>{0}</Acronym>'.format(carrera_acron[i].strip()))
					xml_write.append('        <Code>{0}</Code>'.format(carrera_code[i].strip()))
					xml_write.append('       </Course>')
					xml_write.append('      </CurricularPlan>')
					xml_write.append('     </StudentGroup>')

				validate_group.append(st_group[i])

			xml_write.append('   </StudentGroups>')
			xml_write.append(' </EventXmlRepresentation>') 

	return '\n'.join(xml_write)

