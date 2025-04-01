from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

def generar_contrasena(longitud, incluir_mayusculas, incluir_minusculas, incluir_numeros, incluir_simbolos):
    if longitud < 8 or longitud > 20:
        return "La longitud debe estar entre 8 y 20 caracteres."

    # Construir el conjunto de caracteres basado en las opciones seleccionadas
    caracteres = ""
    if incluir_mayusculas:
        caracteres += string.ascii_uppercase
    if incluir_minusculas:
        caracteres += string.ascii_lowercase
    if incluir_numeros:
        caracteres += string.digits
    if incluir_simbolos:
        caracteres += string.punctuation

    # Validar que al menos una opción esté seleccionada
    if not caracteres:
        return "Debes seleccionar al menos una opción para generar la contraseña."

    # Generar la contraseña
    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contrasena

@app.route("/", methods=["GET", "POST"])
def index():
    contrasena = None
    error = None

    if request.method == "POST":
        try:
            longitud = int(request.form["longitud"])
            if longitud < 8 or longitud > 20:
                error = "La longitud debe estar entre 8 y 20 caracteres."
            else:
                incluir_mayusculas = "mayusculas" in request.form
                incluir_minusculas = "minusculas" in request.form
                incluir_numeros = "numeros" in request.form
                incluir_simbolos = "simbolos" in request.form

                if not (incluir_mayusculas or incluir_minusculas or incluir_numeros or incluir_simbolos):
                    error = "Debes seleccionar al menos una opción para generar la contraseña."
                else:
                    contrasena = generar_contrasena(longitud, incluir_mayusculas, incluir_minusculas, incluir_numeros, incluir_simbolos)
        except ValueError:
            error = "Por favor, introduce un número válido."

    return render_template("index.html", contrasena=contrasena, error=error)

if __name__ == "__main__":
    app.run(debug=True)