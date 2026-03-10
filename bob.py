# --- BOB AI v1.0 ---
# Este é a base do Bob

def iniciar_bob():
    # Esta menssagem aparece somente quando o Bob e chamado
    print('Iniciando Sistemas...')
    print('Salve chefe, o que manda??')
    # A variavel 'comando'  guarda o comando que voce digita
    # O .lower() deixa as letras minusculas 
    while True:
        comando = input('\n Comando: ').lower()

        # --- CEREBRO DO BOB --- 
        # Aqui ele verifica e responde
        # break acaba com o loop
        if 'ola' in comando or 'oi' in comando:
            print('Bob: Eae tudo bem?')

        elif 'seu nome' in comando:
            print('Bob: Eu sou o Bob e estou em treinamento')

        elif 'desligar' in comando or 'sair' in comando:
            print('Bob: Valeu, fui!')
            break

        else:
            # Se ele nao reconhecer o comando ele da uma resposta padrao
            print('Bob: Pode repetir chefe?')

# Esse comando e oque faz para o Bob entender e processar
if __name__ == '__main__':
    iniciar_bob

