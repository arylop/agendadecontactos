
from flask import Flask, render_template, request, redirect, url_for, flash
from database import conectar, crear_tabla

app = Flask(__name__)
app.secret_key = "minions_agenda_123"

crear_tabla()


@app.route("/")
def inicio():
    conexion = conectar()

    contactos = conexion.execute(
        "SELECT * FROM contactos ORDER BY nombre"
    ).fetchall()

    conexion.close()

    return render_template("index.html", contactos=contactos)


@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"].strip()
    telefono = request.form["telefono"].strip()
    correo = request.form["correo"].strip()
    categoria = request.form["categoria"]

    if not nombre or not telefono:
        flash("¡Ups! Falta el nombre o el teléfono 🍌")
        return redirect(url_for("inicio"))

    conexion = conectar()

    conexion.execute("""
        INSERT INTO contactos (nombre, telefono, correo, categoria)
        VALUES (?, ?, ?, ?)
    """, (nombre, telefono, correo, categoria))

    conexion.commit()
    conexion.close()

    flash("¡Contacto agregado correctamente! 🍌")
    return redirect(url_for("inicio"))


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conexion = conectar()

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        telefono = request.form["telefono"].strip()
        correo = request.form["correo"].strip()
        categoria = request.form["categoria"]

        if not nombre or not telefono:
            conexion.close()
            flash("El nombre y el teléfono son obligatorios.")
            return redirect(url_for("editar", id=id))

        conexion.execute("""
            UPDATE contactos
            SET nombre = ?, telefono = ?, correo = ?, categoria = ?
            WHERE id = ?
        """, (nombre, telefono, correo, categoria, id))

        conexion.commit()
        conexion.close()

        flash("¡Contacto actualizado! 💛")
        return redirect(url_for("inicio"))

    contacto = conexion.execute(
        "SELECT * FROM contactos WHERE id = ?", (id,)
    ).fetchone()

    conexion.close()

    if contacto is None:
        flash("No encontramos ese contacto.")
        return redirect(url_for("inicio"))

    return render_template("editar.html", contacto=contacto)


@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conexion = conectar()

    conexion.execute(
        "DELETE FROM contactos WHERE id = ?", (id,)
    )

    conexion.commit()
    conexion.close()

    flash("Contacto eliminado. ¡Hasta la próxima! 🍌")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
