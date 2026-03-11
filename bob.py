# --- Bob AI v5.0 ---
# Agora com cara nova e ativaçao por voz

import google.generativeai as genai
import os
import speech_recognition as sr
import pygame
from gtts import gTTS
from datetime import datetime
import threading
import time

# --- 1. CONFIGURAÇÃO DA INTELIGÊNCIA ---
CHAVE_API = os.getenv("GEMINI_KEY")
genai.configure(api_key=CHAVE_API)
model = genai.GenerativeModel('gemini-3-flash-preview')
chat = model.start_chat(history=[])

# --- 2. CONFIGURAÇÕES VISUAIS ---
LARGURA, ALTURA = 400, 400
PRETO = (15, 15, 15)
AZUL_JARVIS = (0, 200, 255)
VERMELHO_ALERTA = (255, 50, 50)

estado_bob = "IDLE" # IDLE, OUVINDO, PROCESSANDO, FALANDO

# --- 3. FUNÇÕES DE VOZ E LÓGICA ---

def falar(texto):
    """Gera o áudio e anima a boca"""
    global estado_bob
    try:
        tts = gTTS(text=texto, lang='pt', slow=False)
        arquivo = "vozinha.mp3"
        tts.save(arquivo)
        
        pygame.mixer.music.load(arquivo)
        estado_bob = "FALANDO"
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        estado_bob = "IDLE"
    except Exception as e:
        print(f"Erro no áudio: {e}")
        estado_bob = "IDLE"

def motor_da_mente():
    """O cérebro que ouve e pensa"""
    global estado_bob
    reconhecedor = sr.Recognizer()
    
    with sr.Microphone() as source:
        reconhecedor.adjust_for_ambient_noise(source, duration=1)
        print("Bob Inicializado. Aguardando comando...")
        
        while True:
            try:
                # 1. Escuta a Wake Word
                audio = reconhecedor.listen(source, phrase_time_limit=3)
                fala = reconhecedor.recognize_google(audio, language='pt-BR').lower()
                
                if "bob" in fala:
                    estado_bob = "OUVINDO"
                    falar("Sim, senhor?")
                    
                    # 2. Escuta o comando real
                    print("Ouvindo comando...")
                    audio_comando = reconhecedor.listen(source, timeout=5, phrase_time_limit=8)
                    texto_comando = reconhecedor.recognize_google(audio_comando, language='pt-BR')
                    
                    # 3. Processa no Gemini
                    estado_bob = "PROCESSANDO"
                    prompt = f"Contexto: {datetime.now()}. Você é o Bob/Jarvis. Responda curto: {texto_comando}"
                    response = chat.send_message(prompt)
                    
                    # 4. Responde
                    falar(response.text)
                    
            except Exception:
                estado_bob = "IDLE"
                continue

# --- 4. INTERFACE GRÁFICA (ROSTO) ---

def desenhar_bob(screen):
    screen.fill(PRETO)
    centro = (LARGURA // 2, ALTURA // 2)
    
    # Pulsação suave do círculo externo
    raio_base = 140
    if estado_bob == "PROCESSANDO":
        raio_base += int(5 * (time.time() % 1 * 2)) # Pulsa rápido
        cor = VERMELHO_ALERTA
    elif estado_bob == "OUVINDO":
        cor = (255, 255, 255) # Branco quando ouve
    else:
        cor = AZUL_JARVIS

    # Desenho da "Cabeça"
    pygame.draw.circle(screen, cor, centro, raio_base, 2)
    pygame.draw.circle(screen, cor, centro, raio_base - 10, 1)

    # Olhos
    olho_y = centro[1] - 30
    if estado_bob == "OUVINDO":
        # Olhos arregalados
        pygame.draw.circle(screen, cor, (centro[0]-50, olho_y), 12)
        pygame.draw.circle(screen, cor, (centro[0]+50, olho_y), 12)
    else:
        # Olhos normais (traços tecnológicos)
        pygame.draw.rect(screen, cor, (centro[0]-60, olho_y, 20, 5))
        pygame.draw.rect(screen, cor, (centro[0]+40, olho_y, 20, 5))

    # Boca Animada
    if estado_bob == "FALANDO":
        # Altura da boca varia com o tempo para simular fala
        altura_boca = int(10 + abs(30 * (time.time() % 0.4 - 0.2) * 5))
        pygame.draw.ellipse(screen, cor, (centro[0]-30, centro[1]+40, 60, altura_boca), 2)
    else:
        # Linha reta (silêncio)
        pygame.draw.line(screen, cor, (centro[0]-20, centro[1]+60), (centro[0]+20, centro[1]+60), 2)

# --- 5. EXECUÇÃO ---

pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("BOB OS v5.0")

# Lançar a mente do Bob em paralelo
threading.Thread(target=motor_da_mente, daemon=True).start()

rodando = True
relogio = pygame.time.Clock()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    desenhar_bob(tela)
    pygame.display.flip()
    relogio.tick(60) # 60 FPS para animação lisa

pygame.quit()