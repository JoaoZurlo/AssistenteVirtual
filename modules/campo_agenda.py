import datetime

import pandas as pd

hora_atual = datetime.datetime.now()
# print(hora_atual)
hora_atual, minuto_atual = datetime.datetime.time(hora_atual).hour, datetime.datetime.time(hora_atual).minute
# print('Hora atual:', hora_atual)
# print('Minuto atual', minuto_atual)
data_atual = datetime.datetime.date(datetime.datetime.today())

# print('Data_atual:', data_atual)

planilha_agenda = 'C:/Users/jzurlo\Downloads/Curso IA\Pycharm/Assistente_Virtual/agenda.xlsx'
agenda = pd.read_excel(planilha_agenda)
# print(agenda)

descricao, responsavel, hora_agenda = [], [], []

for index, row in agenda.iterrows():
    # print(index)
    # print(row)
    data = datetime.datetime.date(row['data'])
    # print(data)
    hora_completa = datetime.datetime.strptime(str(row['hora']), '%H:%M:%S')
    # print(hora_completa)
    hora = datetime.datetime.time(hora_completa).hour
    # print(hora)

    if data_atual == data:
        if hora >= hora_atual:
            descricao.append(row['descricao'])
            responsavel.append(row['responsavel'])
            hora_agenda.append(row['hora'])

print(descricao)
print(responsavel)
print(hora_agenda)


def carrega_agenda(descricao):
    if descricao:
        return descricao, responsavel, hora_agenda
    else:
        return False
