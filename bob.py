# --- BOB AI v4.0 ---
# Agora com Audição (Microfone) e Inteligência Pura

import google.generativeai as genai
import os
import gradio as gr
from gtts import gTTS
from datetime import datetime

# CONFIGURAÇÃO DE SEGURANÇA
CHAVE_API = os.getenv("GEMINI_KEY")
if CHAVE_API:
    genai.configure(api_key=CHAVE_API)

model = genai.GenerativeModel('gemini-3-flash-preview')
chat = model.start_chat(history=[])

def falar(texto):
    """Gera o áudio da resposta"""
    tts = gTTS(text=texto, lang='pt', slow=False)
    arquivo_audio = "resposta_bob.mp3"
    tts.save(arquivo_audio)
    return arquivo_audio

def processar_tudo(audio_path, texto_input):
    """Lida com entrada de áudio OU texto e retorna resposta + voz"""
    
    # Se houver áudio, enviamos o arquivo para o Gemini transcrever e responder
    # Se não, usamos o texto digitado
    if audio_path:
        # O Gemini 3 consegue "ouvir" arquivos de áudio diretamente!
        audio_file = genai.upload_file(path=audio_path)
        prompt = [
            f"Contexto: Hoje é {datetime.now().strftime('%d/%m/%Y %H:%M')}. Você é o Bob, assistente estilo Jarvis.",
            "O áudio anexo é o meu comando. Responda de forma curta e direta.",
            audio_file
        ]
    else:
        prompt = f"Contexto: {datetime.now().strftime('%d/%m/%Y %H:%M')}. Você é o Bob. Responda: {texto_input}"

    try:
        response = chat.send_message(prompt)
        resposta_texto = response.text
    except Exception as e:
        resposta_texto = "Senhor, tive um erro nos meus sensores auditivos."

    audio_res = falar(resposta_texto)
    return resposta_texto, audio_res

# --- INTERFACE GRADIO ---
with gr.Blocks(title="BOB AI - Protocolo de Voz") as demo:
    gr.Markdown("# 🎙️ BOB AI - Interface de Voz Ativa")
    
    with gr.Row():
        with gr.Column():
            output_text = gr.Textbox(label="Bob diz:")
            audio_output = gr.Audio(label="Voz do Bob", autoplay=True)
        
        with gr.Column():
            input_audio = gr.Audio(label="Fale com o Bob (Clique no microfone)", sources=["microphone"], type="filepath")
            input_text = gr.Textbox(label="Ou digite aqui:")
            btn = gr.Button("Enviar ao Bob")

    # Ação do botão
    btn.click(
        fn=processar_tudo, 
        inputs=[input_audio, input_text], 
        outputs=[output_text, audio_output]
    )

if __name__ == "__main__":
    demo.launch(debug=True)