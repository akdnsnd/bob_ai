# --- BOB AI v3.1 ---
# Totalmente integrado à IA (Sem comandos locais)

import google.generativeai as genai
import os
import gradio as gr
from gtts import gTTS
from datetime import datetime

# CONFIGURAÇÃO DE SEGURANÇA
CHAVE_API = os.getenv("GEMINI_KEY")
if CHAVE_API:
    genai.configure(api_key=CHAVE_API)

# Inicializando o modelo
model = genai.GenerativeModel('gemini-3-flash-preview')
chat = model.start_chat(history=[])

def falar(texto):
    """Gera o arquivo de áudio da resposta"""
    tts = gTTS(text=texto, lang='pt', slow=False)
    arquivo_audio = "resposta_bob.mp3"
    tts.save(arquivo_audio)
    return arquivo_audio

def responder_bob(mensagem, historico):
    """Envia tudo para a IA e processa a resposta"""
    
    # Pegamos os dados do sistema para dar contexto à IA
    agora = datetime.now()
    data_hora_contexto = agora.strftime("%d/%m/%Y às %H:%M")
    
    try:
        # Criamos um "System Prompt" dinâmico que informa a hora sem comandos IF
        prompt = (
            f"Contexto atual: Hoje é dia {data_hora_contexto}. "
            f"Sua personalidade: Você é o Bob, um assistente virtual super parceiro sarcástico, inteligente, leal, estilo Jarvis. "
            f"Responda de forma que compreende, curta, brincalhona com capacidade de reinterpretar situações de forma lúdica. "
            f"Criatividade e Adaptação: Capacidade de mudar de perspectiva rapidamente e buscar soluções incomuns para problemas pensando fora da caixa {mensagem}"
        )
        
        # Envia para a IA
        response = chat.send_message(prompt)
        resposta_texto = response.text
        
    except Exception as e:
        resposta_texto = "Senhor, houve uma falha na conexão dos meus servidores neurais."

    # Gera a voz do Bob
    audio_path = falar(resposta_texto)
    
    return resposta_texto, audio_path

# --- INTERFACE GRADIO ---
with gr.Blocks(title="BOB AI") as demo:
    gr.Markdown("# 🤖 BOB AI - Protocolo Neural Ativo")
    
    with gr.Row():
        with gr.Column():
            chatbot = gr.Chatbot(label="Comunicação")
            msg = gr.Textbox(label="Comando:", placeholder="Fale comigo, senhor...")
            botao = gr.Button("Enviar")
        
        with gr.Column():
            audio_player = gr.Audio(label="Voz do Bob", autoplay=True)

    def processar_interacao(mensagem, historico):
        texto_resp, audio_resp = responder_bob(mensagem, historico)
        historico.append((mensagem, texto_resp))
        return historico, audio_resp, ""

    botao.click(processar_interacao, [msg, chatbot], [chatbot, audio_player, msg])
    msg.submit(processar_interacao, [msg, chatbot], [chatbot, audio_player, msg])

if __name__ == "__main__":
    demo.launch()
       