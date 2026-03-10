# --- BOB AI v1.0 ---
# Este é a base do Bob
from datetime import datetime

def iniciar_bob():
    # Esta menssagem aparece somente quando o Bob e chamado
    print ("Iniciando Sistemas...")
    print ("Salve chefe, o que manda??")
    # A variavel 'comando'  guarda o comando que voce digita
    # O .lower() deixa as letras minusculas 
    while True:
        comando = input ("\n Comando: ").lower()

        # --- CEREBRO DO BOB --- 
        # Aqui ele verifica e responde
        # break acaba com o loop
        if "ola" in comando or "oi" in comando:
            print ("Bob: Eae tudo bem?")

        elif "seu nome" in comando:
            print ("Bob: Eu sou o Bob e estou em treinamento")

        elif "desligar" in comando or "sair" in comando:
            print ("Bob: Valeu, fui!")
            break

        elif "horas" in comando:
            agora = datetime.now()
            hora_formatada = agora.strftime("%H:%M")
            print (f"Bob: sao {hora_formatada}.")

        elif "data" in comando:
            agora = datetime.now()
            data_formatada = agora.strftime("%d/%m/%Y")
            print (f"hoje e dia {data_formatada}.")
            

        else:
            # Se ele nao reconhecer o comando ele da uma resposta padrao
            print ("Bob: Pode repetir chefe?")

# Esse comando e oque faz para o Bob entender e processar
iniciar_bob()

