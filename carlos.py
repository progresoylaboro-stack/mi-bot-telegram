from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel
import random
import time
import json
import os

# Credenciales de la API de Telegram
api_id = 25408691
api_hash = '75a710d6238ab8820595048fd994cec4'

# Configuración del bot
MODO_PRUEBA = False  # Cambia a True para pruebas rápidas
CLAVE = "foto extraída de cartilla"
ARCHIVO_RESPUESTAS = "respuestas.txt"
ARCHIVO_USADAS = "usadas.json"
ID_GRUPO = -1001370401693  # Puede ser el nombre del grupo o su ID numérico

# Inicializar cliente de Telethon
client = TelegramClient('session_name', api_id, api_hash)

# Cargar respuestas desde el archivo
def cargar_respuestas():
    with open(ARCHIVO_RESPUESTAS, 'r', encoding='utf-8') as f:
        return [linea.strip() for linea in f if linea.strip()]

# Cargar respuestas ya utilizadas
def cargar_usadas():
    if not os.path.exists(ARCHIVO_USADAS):
        return []
    with open(ARCHIVO_USADAS, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get('respuestas_usadas', [])

# Guardar respuesta como utilizada
def guardar_usada(respuesta):
    usadas = cargar_usadas()
    usadas.append(respuesta)
    with open(ARCHIVO_USADAS, 'w', encoding='utf-8') as f:
        json.dump({'respuestas_usadas': usadas}, f, indent=4, ensure_ascii=False)

# Elegir una respuesta no utilizada
def elegir_respuesta():
    todas = cargar_respuestas()
    usadas = cargar_usadas()
    disponibles = [r for r in todas if r not in usadas]
    if not disponibles:
        reset_usadas()
        disponibles = todas
    respuesta = random.choice(disponibles)
    guardar_usada(respuesta)
    return respuesta

# Reiniciar el archivo de respuestas usadas
def reset_usadas():
    if os.path.exists(ARCHIVO_USADAS):
        os.remove(ARCHIVO_USADAS)

# Función para responder con retraso
def responder_con_delay(mensaje):
    tiempo_espera = random.randint(600, 900) if not MODO_PRUEBA else random.randint(10, 15)
    time.sleep(tiempo_espera)
    respuesta = elegir_respuesta()
    client.send_message(mensaje.chat.id, respuesta)

# Función principal para procesar mensajes antiguos
def procesar_mensajes():
    grupo = client.get_entity(ID_GRUPO)
    mensajes = client.get_messages(grupo, limit=100)  # Limita a los últimos 100 mensajes
    for mensaje in mensajes:
        if CLAVE in mensaje.text.lower():
            print(f"Respondiendo al mensaje de {mensaje.sender_id}")
            responder_con_delay(mensaje)

# Iniciar cliente y procesar mensajes
with client:
    print("🤖 Bot Carlos corriendo en Termux...")
    procesar_mensajes()
    client.run_until_disconnected()
