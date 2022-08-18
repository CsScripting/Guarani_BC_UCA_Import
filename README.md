### - Processo de Gerar XML de Importação no BC - ###

* Gera Ficheiro de XML BTT_BC_XML


### - Caminho de Deploy:

C:\Users\Paulo Fernandes\Desktop\LocalRepositories\Release_Environment\Deploy_GUARANI_BC_UCA

Create File:

pyinstaller --noconsole --onefile --icon="log.ico" --add-data="log.ico;." ProcesoGuaraniBC.py --version-file version_info_GUARANI_BC_UCA.txt

### - Variaveis associadas a Processos:

Validação:
--> Serão sempre necessarios dados relativos a Horarios, Grupos e Carreras (Folha dentro de Horarios)

Parametro 1:
With Classrooms
--> Se tiver de atribuir salas deve ser adicionado dentro de ficheiro de Horarios folha relativa a Salas.

Parametro 2:
Historic Groups
--> Se consultar o historico de alunos vai a folder de DataProcess verificar o Ficheiro de HistoricoInscriptos.xlsx

### Bugs a verificar:
- Verificar caso de quando se importa desde Guarani, se só tem sempre um espaço associado
#Verificar com Juan se Guarani so admite associada a uma asignacion...Não estou a gerir para os casos de ter mais de uma salas...
Importante ver o ponto acima...

Analisar metodo de grouped_data em main_mod para o caso descrito acima...

#Comentario associado:
'''
	2º Agregar comissões diferentes disciplinas...para o mesmo id de Guarani;
	 - Neste caso são somados os numeros de alunos !!!
	 - No caso de Guarani so admitir um espaço agregar tambem por sala e edificio !!!
'''

- (Done)Número de alunos de comissões e comissões compartidas:
   #Não somar dentro de mesma comissão;
   #Somar diferentes comissões dentro de mesmo id de asignación;

- Strip values variable variable btt - Getting settings

- Caso de numero de alunos diferente de Int !!!
- Caso de formato de data errado !!!

### Notas a Considerar:

- Não existe relação de processos a executar...Pode gerar com salas ou não !! Segundo historico ou não !!
- Depois de somados alunos das diferentes comissões compartidas apenas considerados as comissões com número de alunos != zero.
  Valores a nulo não são retirados à cabeça...podem juntar com comissão compartida...
  Verificar a diferença entre StudentsNull e EventStudentZero

**Versões:**

* 3.1.0

- [x] Numero de aluno NULL retirados;
  -> Já não escreve em ficheiro de DataValidation (StudentsNull)...que antes passava a zero...
  -> Fica Inserido en NullValues
  -> Comissões com zero alunos retiradas de horarios (Mesmo que tenham Id de Asignacion), Antes Agregava-se as comissões com zero alunos, podia ter outra comissão 
    associada, que já tinha alunos !!!!
  -> Neste caso já não sera necesario executar em main_mod função de filter_events_grouped_students_null

  - [ ] Validar Mapeamento de Curriculum;
  - [ ] Validar Possibilidade de poder associar mais de uma sala...associar a BcToBTT;
  - [ ] Validar Caracteres especiais nomeadamente & e virgulas;
  - [X] Salas Sempre Obrigatorias, inserir eventos com salas, ou preparar atribuição de salas por ficheiro;
  - [X] Validação ID Guarani;

  - [X] Criar BESTClassrooms...valores Default a usar em processo de Atribuição de Salas;  


  - [X] Criar AddClassrooms...valores Default a usar em processo de Atribuição de Salas;  
        - v_mod_code, v_section, v_typologie, v_student_group,
        - v_prioriyt_value, v_prioriyt_class, v_alternative_value, v_alternative_class

   - [X] para Criar o BESTClassrooms estava a filtrar por salas que efectivamente tinha o codigo corrreto de Guarani ....????
         Neste momento não está. Será para usar desta forma ?????

  * 3.1.1

  - [X] Validação de Colunas de Ficheiro de Salas; 
        Na Apresentação de Erro não apresentava a necessidade de ter as caracteristicas de salas !!!

  - [X] Validação se String permite passar para int(isdigit) para as analises de Inteiros nos numeros de alunos; 

  - [ ] Mais tarde decidir onde deverá ficar o arredondar as horas;