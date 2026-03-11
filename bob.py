

import os
import requests # A nossa nova forma de falar com o Gemini
import speech_recognition as sr
import pygame
from gtts import gTTS
from datetime import datetime
import threading
import time

# --- 1. CONFIGURAÇÃO DA INTELIGÊNCIA (MODO DIRETO / REST API) ---
CHAVE_API = os.getenv("GEMINI_KEY")

def consultar_gemini(texto):
    """Faz o pedido diretamente à internet, ignorando bibliotecas velhas"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={CHAVE_API}"
    cabecalho = {'Content-Type': 'application/json'}
    dados = {
        "contents": [{
            "parts": [{"text": f"Contexto: {datetime.now()}. Você é o Bob/Jarvis. Responda curto: {texto}"}]
        }]
    }
    
    try:
        resposta = requests.post(url, headers=cabecalho, json=dados)
        if resposta.status_code == 200:
            resultado = resposta.json()
            return resultado['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"Erro da API: {resposta.text}")
            return "Senhor, houve um erro na minha comunicação central."
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return "Senhor, os meus cabos de internet falharam."

# --- 2. CONFIGURAÇÕES VISUAIS ---
LARGURA, ALTURA = 400, 400
PRETO = (15, 15, 15)
AZUL_JARVIS = (0, 200, 255)
VERMELHO_ALERTA = (255, 50, 50)

estado_bob = "IDLE"

# --- 3. FUNÇÕES DE VOZ E LÓGICA ---
def falar(texto):
    global estado_bob
    try:
        print(f"Bob responde: {texto}")
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
    global estado_bob
    reconhecedor = sr.Recognizer()
    
    with sr.Microphone() as source:
        reconhecedor.adjust_for_ambient_noise(source, duration=1)
        print("Bob Inicializado no Windows 7. Aguardando a Wake Word 'Bob'...")
        
        while True:
            try:
                audio = reconhecedor.listen(source, phrase_time_limit=3)
                fala = reconhecedor.recognize_google(audio, language='pt-BR').lower()
                
                if "bob" in fala:
                    estado_bob = "OUVINDO"
                    falar("Sim, senhor?")
                    
                    print("Ouvindo comando...")
                    audio_comando = reconhecedor.listen(source, timeout=5, phrase_time_limit=8)
                    texto_comando = reconhecedor.recognize_google(audio_comando, language='pt-BR')
                    print(f"Você disse: {texto_comando}")
                    
                    estado_bob = "PROCESSANDO"
                    
                    # Usa a nossa nova função direta
                    resposta_texto = consultar_gemini(texto_comando) 
                    
                    falar(resposta_texto)
                    
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception as e:
                estado_bob = "IDLE"
                time.sleep(1)

# --- 4. INTERFACE GRÁFICA (ROSTO) ---
def desenhar_bob(screen):
    screen.fill(PRETO)
    centro = (LARGURA // 2, ALTURA // 2)
    
    raio_base = 140
    if estado_bob == "PROCESSANDO":
        raio_base += int(5 * (time.time() % 1 * 2))
        cor = VERMELHO_ALERTA
    elif estado_bob == "OUVINDO":
        cor = (255, 255, 255)
    else:
        cor = AZUL_JARVIS

    pygame.draw.circle(screen, cor, centro, raio_base, 2)
    pygame.draw.circle(screen, cor, centro, raio_base - 10, 1)

    olho_y = centro[1] - 30
    if estado_bob == "OUVINDO":
        pygame.draw.circle(screen, cor, (centro[0]-50, olho_y), 12)
        pygame.draw.circle(screen, cor, (centro[0]+50, olho_y), 12)
    else:
        pygame.draw.rect(screen, cor, (centro[0]-60, olho_y, 20, 5))
        pygame.draw.rect(screen, cor, (centro[0]+40, olho_y, 20, 5))

    if estado_bob == "FALANDO":
        altura_boca = int(10 + abs(30 * (time.time() % 0.4 - 0.2) * 5))
        pygame.draw.ellipse(screen, cor, (centro[0]-30, centro[1]+40, 60, altura_boca), 2)
    else:
        pygame.draw.line(screen, cor, (centro[0]-20, centro[1]+60), (centro[0]+20, centro[1]+60), 2)

# --- 5. EXECUÇÃO ---
pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("BOB OS v5.1 - Win7 Edition")

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