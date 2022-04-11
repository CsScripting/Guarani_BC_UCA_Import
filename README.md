### - Processo de Gerar XML de Importação no BC - ###

- Gera Ficheiro de XML BTT_BC_XML


Caminho de Deploy:

C:\Users\Paulo Fernandes\Desktop\LocalRepositories\Release_Environment\Deploy_GUARANI_BC_UCA

Create File:

pyinstaller --noconsole --onefile --icon="log.ico" --add-data="log.ico;." ProcesoGuaraniBC.py

#Variaveis associadas a Processos:

Validação:
--> Serão sempre necessarios dados relativos a Horarios, Grupos e Carreras (Folha dentro de Horarios)

Parametro 1:
# With Classrooms

Parametro 2:
# Historic Groups

* Se consultar o historico de alunos vai a folder de DataProcess verificar o Ficheiro de HistoricoInscriptos.xlsx


#Verificar com Juan se Guarani so admite associada a uma asignacion...Não estou a gerir para os casos de ter mais de uma salas...
Importante ver o ponto acima...

# Comentario associado:
'''
	2º Agregar comissões diferentes disciplinas...para o mesmo id de Guarani;
	 - Neste caso são somados os numeros de alunos !!!
	 - No caso de Guarani so admitir um espaço agregar tambem por sala e edificio !!!
'''


# Número de alunos de comissões e comissões compartidas:
- Não somar dentro de mesma comissão;
- Somar diferentes comissões dentro de mesmo id de asignación;

# Strip values variable variable btt - Getting settings

# Eventos considerados:

- Depois de agrupados eventos apenas considerados os que apresentam número de alunos diferentes de 0.

# Caso de numero de alunos diferente de Int !!!
# Caso de formato de data errado !!!