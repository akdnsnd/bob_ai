# --- BOB AI ---
# Agora o Bob tem uma base, vida, memoria usando o Gemini 3
import google.generativeai as genai
import os
from datetime import datetime

#CONFIFURACAO DE SEGURANCA
# O bob agora buscar a chave no 'cofre' do sistema, nao mais no texto do codigo

# Configuracao do CEREBRO
# Chave: AIzaSyCZS5KECaJIYIZVlabEAxgHgxO7qh2fDgQ
CHAVE_API = os.getenv("GEMINI_KEY")


if not CHAVE_API:
    print("ERRO: Nao encontrei a chave no sistema")
else:
    genai.configure(api_key=CHAVE_API)

# Configuracao do modelo (gemini1.5 flash)
model = genai.GenerativeModel ('models/gemini-3-flash-preview')

# Esse trecho lista os modelos que sua chave permite usar
print ("Modelos Disponiveis:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"-  {m.name}")

def iniciar_bob():
    # Criamos uma sessao de chat vazia para manter o historico (memoria)
    # o 'histoy=[]' indica que a conversa esta comecando do zero
    chat = model.start_chat(history=[])

    # Esta menssagem aparece somente quando o Bob e chamado
    print ("Sistema Neurais v3.0 Online...")
    print ("Salve chefe, o que manda??")
    # A variavel 'comando'  guarda o comando que voce digita
    # O .lower() deixa as letras minusculas 
    while True:
        comando = input ("\n Comando: ").lower()

        # Comandos "locais" (que o bob faz sem precisar de internet)
        if "horas" in comando:
            agora = datetime.now()
            hora_formatada = agora.strftime("%H:%M")
            print (f"Bob: sao {hora_formatada}.")

        elif "desligar" in comando or "sair" in comando:
            print ("Bob: Valeu, fui!")
            break

        # Comando de AI (Para tudo que ele nao souber responder localmente)
        #Bob com Memoria
        else:
            try:
                # O Bob envia sua pergunta para o Gemini
                # Adicionamos uma instrucao para elesempre agir como o Bob
                prompt_personalidade = f"(Voce é o Bob. Um assistente SUPER parceiro no estilo Jarvis que Responde de forma curta, brincalhona com capacidade de reinterpretar situações da vida de forma lúdica. Criatividade e Adaptação: Capacidade de mudar de perspectiva rapidamente e buscar soluções incomuns para problemas, muitas vezes usando o humor para aliviar a tensão. Com uma Voz e Flow Distintos e uma Ambição de Foco): {comando}"
                # Usamos o chat.send_message em vez de model.generate_content
                # Isso faz o google guarda o historico da conversa nesta sessao
                resposta = chat.send_message(prompt_personalidade)

                print (f"Bob: {resposta.text}")
            except Exception as e:
                print ("Bob: Tive um pequeno problema de conexao")
                print (f"ERRO: {e}")

        # --- CEREBRO DO BOB --- 
        # Aqui ele verifica e responde
        # break acaba com o loop
        if "ola" in comando or "oi" in comando:
            print ("Bob: Eae tudo bem?")


        elif "seu nome" in comando:
            print ("Bob: Eu sou o Bob e estou em treinamento")


        elif "data" in comando:
            agora = datetime.now()
            data_formatada = agora.strftime("%d/%m/%Y")
            print (f"hoje e dia {data_formatada}.")


        else:
            # Se ele nao reconhecer o comando ele da uma resposta padrao
            print ("Bob: Pode repetir chefe?")

# Esse comando e oque faz para o Bob entender e processar
iniciar_bob()

