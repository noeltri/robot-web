from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

energia = 100
emocion = "óptimo"
ultimo_tema = None
historial = []

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
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global historial

    comando = request.json["mensaje"].lower()
    respuesta = procesar_comando(comando)

    # Guardar en memoria
    historial.append({
        "usuario": comando,
        "robot": respuesta
    })

    return jsonify({
        "respuesta": respuesta,
        "energia": energia,
        "emocion": emocion,
        "historial": historial
    })

if __name__ == "__main__":
    app.run(debug=True)


