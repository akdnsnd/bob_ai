import os
import requests 
import speech_recognition as sr
import pygame
import numpy as np
from gtts import gTTS
from datetime import datetime
import threading
import time
import math

# --- 1. CONFIGURAÇÕES TÉCNICAS E VISUAIS ---
CHAVE_API = os.getenv("GEMINI_KEY") or "AIzaSyBUcMvSS_gXXe64z1IQ2BFQczdc8jL3JWc"
LARGURA, ALTURA = 400, 400
FPS = 60

# Cores do Humor
PRETO      = (10, 10, 10)
BRANCO     = (255, 255, 255)
AZUL_SUAVE = (100, 150, 255)
CINZA_IDLE = (180, 180, 180)
BRILHO     = (40, 40, 40)
VERDE_DICA = (50, 255, 50)
VERMELHO_BRAVO = (255, 50, 50)
AMARELO_HUMOR = (255, 255, 50)

estado_bob = "IDLE"
cor_atual = CINZA_IDLE

# --- 2. SISTEMA DE SOM (BIPE) ---
def tocar_bipe():
    """Gera um bipe curto de ativação sem precisar de arquivo externo"""
    frequencia = 880  # Nota Lá (A5)
    duracao = 0.1     # Segundos
    amostragem = 44100
    n_amostras = int(duracao * amostragem)
    
    # Gera a onda senoidal
    buf = np.sin(2 * np.pi * np.arange(n_amostras) * frequencia / amostragem).astype(np.float32)
    sound = pygame.sndarray.make_sound((buf * 0.3 * 32767).astype(np.int16))
    sound.play()

# --- 3. CÉREBRO: CONEXÃO COM GEMINI ---
def consultar_gemini(texto):
    global cor_atual
    # Usando o modelo estável para evitar erros de preview
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={CHAVE_API}"
    cabecalho = {'Content-Type': 'application/json'}
    
    prompt_sistema = (
        "Você é o Bob, assistente de São Paulo. Use gírias: mano, parça, chefe, cara. "
        "Sua personalidade é instável: seja sarcástico, humorista ou bravo. "
        "Sempre dê uma dica ou sugestão extra sobre o assunto. "
        "Responda curto e termine com: [FELIZ], [BRAVO], [HUMOR] ou [DICA]."
    )

    dados = {"contents": [{"parts": [{"text": f"{prompt_sistema}\nUsuário: {texto}"}]}]}
    
    try:
        resposta = requests.post(url, headers=cabecalho, json=dados, timeout=10)
        if resposta.status_code == 200:
            res_json = resposta.json()
            texto_final = res_json['candidates'][0]['content']['parts'][0]['text']
            
            # Troca de cor por humor
            if "[BRAVO]" in texto_final: cor_atual = VERMELHO_BRAVO
            elif "[DICA]" in texto_final: cor_atual = VERDE_DICA
            elif "[HUMOR]" in texto_final: cor_atual = AMARELO_HUMOR
            else: cor_atual = BRANCO
            
            return texto_final.replace("[BRAVO]","").replace("[DICA]","").replace("[HUMOR]","").replace("[FELIZ]","")
        return "Mano, o sistema deu teto preto aqui. Tenta de novo, parça."
    except:
        return "Tô sem sinal, chefe. A fita tá louca."

# --- 4. VOZ ---
def falar(texto):
    global estado_bob
    arquivo_nome = "temp_voz.mp3"
    try:
        tts = gTTS(text=texto, lang='pt', slow=False)
        tts.save(arquivo_nome)
        pygame.mixer.music.load(arquivo_nome)
        estado_bob = "FALANDO"
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy(): time.sleep(0.1)
        pygame.mixer.music.unload() 
        estado_bob = "IDLE"
        if os.path.exists(arquivo_nome): os.remove(arquivo_nome)
    except:
        estado_bob = "IDLE"

# --- 5. AUDIÇÃO: MOTOR DA MENTE ---
def motor_da_mente():
    global estado_bob, cor_atual
    reconhecedor = sr.Recognizer()
    
    # Configuração de alta sensibilidade e resposta rápida
    reconhecedor.energy_threshold = 100 
    reconhecedor.dynamic_energy_threshold = False
    reconhecedor.pause_threshold = 0.5
    
    with sr.Microphone() as source:
        print("Bob v8.2 na escuta, parça!")
        
        while True:
            try:
                audio = reconhecedor.listen(source, phrase_time_limit=8)
                fala = reconhecedor.recognize_google(audio, language='pt-BR').lower()
                
                if "bob" in fala:
                    tocar_bipe() # Som de ativação
                    
                    comando = fala.replace("bob", "", 1).strip()
                    if len(comando) > 2:
                        estado_bob = "PROCESSANDO"
                        falar(consultar_gemini(comando))
                    else:
                        estado_bob = "OUVINDO"
                        cor_atual = AZUL_SUAVE
                        audio_comando = reconhecedor.listen(source, timeout=5, phrase_time_limit=8)
                        texto_c = reconhecedor.recognize_google(audio_comando, language='pt-BR')
                        estado_bob = "PROCESSANDO"
                        falar(consultar_gemini(texto_c))
            except (sr.UnknownValueError, sr.WaitTimeoutError):
                estado_bob = "IDLE"
                cor_atual = CINZA_IDLE
                continue
            except Exception as e:
                print(f"Erro: {e}")
                time.sleep(1)

# --- 6. INTERFACE ---
def desenhar_bob(screen):
    screen.fill(PRETO)
    centro = (LARGURA // 2, ALTURA // 2)
    t = time.time()
    raio_base = 80
    
    if estado_bob == "FALANDO":
        raio = raio_base + 20 + (math.sin(t * 20) * 25)
        cor = cor_atual
    elif estado_bob == "OUVINDO":
        raio = raio_base + (math.sin(t * 15) * 10)
        cor = AZUL_SUAVE
    elif estado_bob == "PROCESSANDO":
        raio = raio_base + (math.sin(t * 10) * 15)
        cor = BRANCO
    else: 
        raio = raio_base + (math.sin(t * 3) * 5)
        cor = CINZA_IDLE

    for i in range(1, 4):
        pygame.draw.circle(screen, BRILHO, centro, int(raio + (i * 8)), 1)
    pygame.draw.circle(screen, cor, centro, int(raio))

# --- 7. EXECUÇÃO ---
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    # Necessário para gerar sons via numpy
    pygame.mixer.set_num_channels(8)
    
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("BOB v8.2 - Beep Edition")

    threading.Thread(target=motor_da_mente, daemon=True).start()

    relogio = pygame.time.Clock()
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: rodando = False
        desenhar_bob(tela)
        pygame.display.flip()
        relogio.tick(FPS)
    pygame.quit()