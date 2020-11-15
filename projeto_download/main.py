# Importando arquivos de PyQt5
from PyQt5 import uic, QtWidgets, QtGui
import mysql.connector
import sys
from datetime import date, time

banco_dados = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="agendamento"
)

def excluir_dado():
    linha_remover = agendamentos_dados.tableWidget.currentRow()
    agendamentos_dados.tableWidget.removeRow(linha_remover)

    cursor = banco_dados.cursor()
    cursor.execute("SELECT id FROM solicitacao")
    id_lidos = cursor.fetchall()
    valor_id = id_lidos[linha_remover][0]
    cursor.execute("DELETE FROM solicitacao WHERE id="+ str(valor_id))



def lista_agendamentos():

    agendamentos_dados.show()

    cursor = banco_dados.cursor()
    cursor.execute("SELECT * FROM solicitacao")
    dados_lidos = cursor.fetchall()

    agendamentos_dados.tableWidget.setRowCount(len(dados_lidos))
    agendamentos_dados.tableWidget.setColumnCount(7)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 7):
            agendamentos_dados.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def continuacao_sim():
    formulario_dados.remetente.setText("")
    formulario_dados.destino.setText("")
    formulario_dados.comunicacao.setCurrentIndex(0)
    formulario_dados.mensagem.setText("")
    segunda_tela.hide()

def continuacao_nao():
    segunda_tela.hide()
    formulario_dados.hide()
    sys.exit()

# Funcao acessa os valores dos campos do formulario
def formulario_leitura():

    # Leitura dos dados
    dado_comunicacao = formulario_dados.comunicacao.currentText()
    dado_remetente = formulario_dados.remetente.text()
    dado_destino = formulario_dados.destino.text()
    dado_data = formulario_dados.data.date().toPyDate()
    dado_mensagem = formulario_dados.mensagem.toPlainText()
    dado_hora = formulario_dados.tempo.time().toPyTime()


    # Envio dos dados
    comando_mysql = "INSERT INTO solicitacao (comunicacao, remetente, destino, data, hora, mensagem, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    dados = (str(dado_comunicacao), str(dado_remetente), str(dado_destino), str(dado_data), str(dado_hora), str(dado_mensagem), str("Em análise"))
    banco_dados.cursor().execute(comando_mysql, dados)
    banco_dados.commit()

    segunda_tela.show()
    segunda_tela.sim.clicked.connect(continuacao_sim)
    segunda_tela.nao.clicked.connect(continuacao_nao)

# Cria a Aplicacao
app = QtWidgets.QApplication([])

# Importando o formulario
formulario_dados = uic.loadUi("formulario.ui")
segunda_tela = uic.loadUi("continuacao.ui")
agendamentos_dados = uic.loadUi("agendamentos.ui")

formulario_dados.show()

# Aciona botao e acessa a funcao de leitura de dados (formulario_leitura)
formulario_dados.botao_enviar.clicked.connect(formulario_leitura)
formulario_dados.botao_agendamentos.clicked.connect(lista_agendamentos)
agendamentos_dados.botao_excluir.clicked.connect(excluir_dado)


app.exec()