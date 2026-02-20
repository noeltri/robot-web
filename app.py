from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("memory.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            response TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


energia = 100
emocion = "óptimo"
ultimo_tema = None
historial = []


def save_to_memory(user_message, bot_response):
    conn = sqlite3.connect("memory.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations (message, response, timestamp) VALUES (?, ?, ?)",
        (user_message, bot_response, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def procesar_comando(comando):
    global energia, emocion, ultimo_tema

    respuesta = ""

    if comando == "saludar":
        respuesta = "Hola. Sistema activo."
        energia -= 5

    elif comando == "analizar":
        respuesta = "Especificá qué querés que analice."
        energia -= 15

    elif comando == "estado":
        respuesta = f"Energía: {energia} | Estado: {emocion}"

    elif comando == "recargar":
        energia += 40
        if energia > 100:
            energia = 100
        respuesta = "Recargando sistema..."

    else:
        respuesta = "Comando no reconocido."

    if energia <= 20:
        emocion = "agotado"
    elif energia <= 50:
        emocion = "estable"
    else:
        emocion = "óptimo"

    return respuesta

@app.route("/")
def index():
    conversaciones = load_memory()
    return render_template("index.html", conversaciones=conversaciones)

@app.route("/chat", methods=["POST"])
def chat():
    global historial

    comando = request.json["mensaje"].lower()
    respuesta = procesar_comando(comando)

    historial.append({
        "usuario": comando,
        "robot": respuesta
    })

    save_to_memory(comando, respuesta)
def load_memory():
    conn = sqlite3.connect("memory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT message, response FROM conversations ORDER BY id DESC LIMIT 20")
    rows = cursor.fetchall()
    conn.close()
    return rows[::-1]  
    return jsonify({
        "respuesta": respuesta,
        "energia": energia,
        "emocion": emocion,
        "historial": historial
    })


if __name__ == "__main__":
    app.run(debug=True)

    
