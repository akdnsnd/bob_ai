# --- Base Bob v7.0 ---

import os
import requests 
import speech_recognition as sr
import pygame
from gtts import gTTS
from datetime import datetime
import threading
import time
import math # Importamos math para a pulsação suave

# --- 1. CONFIGURAÇÃO DA INTELIGÊNCIA ---
CHAVE_API = os.getenv("GEMINI_KEY")

def consultar_gemini(texto):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={CHAVE_API}"
    cabecalho = {'Content-Type': 'application/json'}
    dados = {
        "contents": [{
            "parts": [{"text": f"Contexto: {datetime.now()}. Você é o Bob. Responda curto: {texto}"}]
        }]
    }
    try:
        resposta = requests.post(url, headers=cabecalho, json=dados)
        if resposta.status_code == 200:
            resultado = resposta.json()
            return resultado['candidates'][0]['content']['parts'][0]['text']
        return "Erro na comunicação, senhor."
    except:
        return "Falha na conexão."

# --- 2. CONFIGURAÇÕES VISUAIS (ATUALIZADO) ---
LARGURA, ALTURA = 400, 400
PRETO = (10, 10, 10)
BRANCO = (255, 255, 255)
AZUL_SUAVE = (100, 150, 255)

estado_bob = "IDLE"
contador_respostas = 1

# --- 3. FUNÇÕES DE VOZ (MANTIDAS) ---
def falar(texto):
    global estado_bob
    global contador_respostas

    try:
        print(f"Bob: {texto}")

        tts = gTTS(text=texto, lang='pt', slow=False)

        arquivo = f"{contador_respostas}.mp3"
        contador_respostas += 1

        tts.save(arquivo)

        pygame.mixer.music.load(arquivo)
        estado_bob = "FALANDO"
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.05)
        
        estado_bob = "IDLE"
    
    except Exception as e:
        print(f"Erro: {e}")
        estado_bob = "IDLE"

def motor_da_mente():
    global estado_bob
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as source:
        reconhecedor.adjust_for_ambient_noise(source, duration=1)
        while True:
            try:
                audio = reconhecedor.listen(source, phrase_time_limit=3)
                fala = reconhecedor.recognize_google(audio, language='pt-BR').lower()
                if "bob" in fala:
                    estado_bob = "OUVINDO"
                    falar("Sim?")
                    audio_comando = reconhecedor.listen(source, timeout=5, phrase_time_limit=8)
                    texto_comando = reconhecedor.recognize_google(audio_comando, language='pt-BR')
                    estado_bob = "PROCESSANDO"
                    falar(consultar_gemini(texto_comando))
            except:
                pass

# --- 4. INTERFACE GRÁFICA: A BOLA PULSANTE ---
def desenhar_bob(screen):
    screen.fill(PRETO)
    centro = (LARGURA // 2, ALTURA // 2)
    tempo_atual = time.time()
    
    # Configuração da pulsação base (Respiração lenta)
    raio_base = 80
    pulsacao_suave = math.sin(tempo_atual * 3) * 5 
    
    if estado_bob == "FALANDO":
        # Pulsação forte e rápida enquanto fala
        variacao = math.sin(tempo_atual * 20) * 25
        cor = BRANCO
        raio_final = raio_base + 20 + variacao
    elif estado_bob == "OUVINDO":
        # Fica num tom azulado e vibra levemente
        cor = AZUL_SUAVE
        raio_final = raio_base + math.sin(tempo_atual * 15) * 8
    elif estado_bob == "PROCESSANDO":
        # Pulsa como um batimento cardíaco
        cor = BRANCO
        raio_final = raio_base + (math.sin(tempo_atual * 10) * 15)
    else:
        # Modo IDLE: Apenas "respirando"
        cor = (200, 200, 200) # Cinza claro
        raio_final = raio_base + pulsacao_suave

    # Desenha o brilho (opcional - várias camadas dão efeito de luz)
    for i in range(3):
        alpha_raio = int(raio_final + (i * 10))
        pygame.draw.circle(screen, (50, 50, 50), centro, alpha_raio, 1)

    # Desenha a bola principal
    pygame.draw.circle(screen, cor, centro, int(raio_final))

# --- 5. EXECUÇÃO ---
pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("BOB - Interface Esférica")

threading.Thread(target=motor_da_mente, daemon=True).start()

rodando = True
relogio = pygame.time.Clock()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    desenhar_bob(tela)
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()