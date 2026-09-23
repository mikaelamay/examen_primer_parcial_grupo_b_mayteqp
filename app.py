from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash

app = Flask(__name__)
app.secret_key = "clave_secreta_examen_biblioteca"

usuarios = {
    "carlos": "1111",
    "laura": "2222",
    "diego": "3333"
}

libros = [
    {"titulo": "Python desde cero", "autor": "Juan Pérez", "disponibles": 4},
    {"titulo": "Desarrollo Web", "autor": "María López", "disponibles": 2},
    {"titulo": "Inteligencia Artificial", "autor": "Pedro García", "disponibles": 0}
]


@app.route("/")
def index():
    ultimo_usuario = request.cookies.get("ultimo_usuario")
    return render_template("index.html", ultimo_usuario=ultimo_usuario)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")

        if usuario in usuarios and usuarios[usuario] == password:
            session["usuario"] = usuario
            flash(f"Bienvenido, {usuario}.")
            resp = make_response(redirect(url_for("libros_view")))
            resp.set_cookie("ultimo_usuario", usuario, max_age=60 * 60 * 24 * 30)
            return resp
        else:
            flash("Usuario o contraseña incorrectos.")
            return render_template("login.html")

    return render_template("login.html")


@app.route("/libros")
def libros_view():
    return render_template("libros.html", libros=libros)


@app.route("/perfil")
def perfil():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("perfil.html", usuario=session["usuario"])


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.")
    return redirect(url_for("index"))


@app.route("/eliminar_cookie")
def eliminar_cookie():
    resp = make_response(redirect(url_for("index")))
    resp.delete_cookie("ultimo_usuario")
    flash("Cookie 'ultimo_usuario' eliminada.")
    return resp


if __name__ == "__main__":
    app.run(debug=True)
