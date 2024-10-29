import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = 'COM17'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 115200

dataList = {"Tempo(s)"    :[], 
            "Setpoint"    :[], 
            "Erro"        :[],
            "Valor Atual" :[],
            "Saída PWM"   :[]}
Keys = list(dataList.keys())

# Função de animação para atualizar o gráfico em tempo real
def animate(i, dataList, ser):
    reading = ser.readline().decode('utf-8')  # Lê dados da porta serial e decodifica para string
    
    try:
        reading = [float(value) for value in reading.strip().split(',')]  # Converte dados para float
        if len(reading) == len(Keys):  # Verifica se o número de valores recebidos corresponde às chaves
            for i in range(len(reading)):
                dataList[Keys[i]].append(reading[i])  # Adiciona os valores ao dataList

    except ValueError:  # Ignora se algum valor não for convertível
        pass

    # Limita o tamanho dos dados para 50 elementos para cada chave
    for key in Keys:
        dataList[key] = dataList[key][-50:]
    
    ax.clear()  # Limpa o gráfico para nova atualização

    # Plota cada variável na mesma tela com diferentes cores e legendas
    ax.plot(dataList["Tempo(s)"], dataList["Setpoint"], 
            label=f"Setpoint = {dataList['Setpoint'][-1]}",
            color='b', linestyle='--', linewidth=5)
    ax.plot(dataList["Tempo(s)"], dataList["Valor Atual"],
            label=f"Valor Atual = {dataList['Valor Atual'][-1]}",
            color='g')
    ax.plot(dataList["Tempo(s)"], dataList["Erro"],
            label=f"Erro = {dataList['Erro'][-1]}",
            color='r')
    # ax.plot(dataList["Tempo(s)"], dataList["Saída PWM"], label="Saída PWM", color='m')

    # Configurações do gráfico
    ax.set_xlabel("Tempo(s)")
    ax.set_ylabel("Valores")
    ax.set_title("Leituras do Arduino")
    ax.grid(axis="y")
    ax.legend(loc="best")

# Configuração da figura e eixo
fig, ax = plt.subplots(figsize=(10, 6))

# Inicializa a comunicação serial
ser = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=0.1)
time.sleep(2)

# Configuração da animação
ani = animation.FuncAnimation(fig, animate, fargs=(dataList, ser), interval=0.1, frames=144)

plt.tight_layout()
plt.show()

ser.close()