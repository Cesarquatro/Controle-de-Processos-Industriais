'''
 * Docente:          Dhiego Fernandes Carvalho
 * Discente:         Cesar Augusto Mendes Cordeiro da Silva
 * GitHub:           https://github.com/Cesarquatro
 * Atividade Extra
 * 22/10/2024
'''

import serial  # Importa o módulo para comunicação serial
import pyqtgraph as pg  # Importa a biblioteca de plotagem em tempo real PyQtGraph
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets    # Importa classes essenciais do PyQtGraph para interfaces gráficas
import time  # Importa a biblioteca de gerenciamento de tempo

# Configuração da porta serial (modifique conforme necessário)
ser = serial.Serial('COM17', 115200, timeout=0.1)  # Define a comunicação serial na porta 'COM7' com taxa de 115200 bps

# Configuração da janela de plotagem usando PyQtGraphQQ
app = QtWidgets.QApplication([]) # Inicializa a aplicação PyQt
win = pg.GraphicsLayoutWidget(show=True, title="Leitura Serial em Tempo Real")  # Cria uma janela de gráficos
win.resize(800, 600)  # Ajusta o tamanho da janela de gráficos
win.setWindowTitle('PID Controller - Arduino UNO')  # Define o título da janela

# Criação dos gráficos
plot = win.addPlot(title="System Output (Actual) and Setpoint vs Time")  # Adiciona um gráfico à janela com o título
curve_actual = plot.plot(pen='b', name='Actual')  # Cria uma curva para representar o valor atual em azul ('b')
curve_setpoint = plot.plot(pen='w', name='Setpoint', linestyle='--')  # Cria uma curva para o setpoint, representada em branco ('w')

# Listas para armazenar os dados lidos
tempo_dados = []  # Armazena os valores de tempo
saida_real_dados = []  # Armazena os valores de saída atual do sistema
setpoint_dados = []  # Armazena os valores do setpoint

# Duração total da coleta de dados (em segundos)
total_duration = 40  # Define o tempo total de execução da coleta de dados
start_time = time.time()  # Armazena o tempo de início da coleta

print(f"Coletando dados por {total_duration} segundos...")  # Exibe uma mensagem informando o início da coleta

def update():
    """ Função de atualização que é chamada em cada iteração para atualizar os gráficos. """
    global tempo_dados, saida_real_dados, setpoint_dados  # Define as variáveis como globais para serem acessadas pela função
    
    # Lê uma linha de dados da porta serial
    line = ser.readline().decode('utf-8').strip()  # Lê a linha e converte de bytes para string
    if line:  # Verifica se a linha não está vazia
        data = line.split(',')  # Divide a string usando a vírgula como separador
        if len(data) == 5:  # Certifica-se de que há 5 valores na linha (tempo, setpoint, atual, erro e saída)
            try:
                # Captura o tempo, setpoint e valor atual a partir dos dados lidos
                current_time = float(data[0])  # Primeiro valor é o tempo
                setpoint = float(data[1])  # Segundo valor é o setpoint
                atual = float(data[2])  # Terceiro valor é o valor atual do sistema
                
                # Calcula o tempo decorrido em relação ao início da coleta de dados
                tempo_decorrido = current_time - start_time
                
                # Adiciona os valores capturados nas listas correspondentes
                tempo_dados.append(tempo_decorrido)
                setpoint_dados.append(setpoint)
                saida_real_dados.append(atual)
                
                # Atualiza as curvas do gráfico com os novos dados
                curve_actual.setData(tempo_dados, saida_real_dados)
                curve_setpoint.setData(tempo_dados, setpoint_dados)
                
            except ValueError:
                pass  # Ignora erros caso algum valor não possa ser convertido corretamente

# Configuração de um temporizador para atualizar os gráficos em intervalos regulares
timer = QtCore.QTimer()  # Cria um objeto temporizador do Qt
timer.timeout.connect(update)  # Conecta o evento de timeout à função update
timer.start(50)  # Define o intervalo de atualização para 50 ms (20 atualizações por segundo)

# Executa a aplicação PyQtGraph
if __name__ == '__main__':  # Verifica se o script está sendo executado diretamente
    try:
        QtGui.QApplication.instance().exec_()  # Inicia o loop principal da aplicação gráfica
    except KeyboardInterrupt:  # Permite interromper a execução com o teclado (CTRL+C)
        print("Coleta de dados interrompida pelo usuário.")  # Mensagem ao interromper a coleta
    finally:
        ser.close()  # Fecha a porta serial corretamente ao encerrar o programa
