from flask import Flask
import mysql.connector
import os

app = Flask(__name__)

def conectar_bd():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        user=os.getenv("MYSQL_USER", "admin"),
        password=os.getenv("MYSQL_PASSWORD", "admin123"),
        database=os.getenv("MYSQL_DATABASE", "holamundo")
    )

@app.route("/")
def inicio():
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                mensaje VARCHAR(255)
            )
        """)

        cursor.execute(
            "INSERT IGNORE INTO mensajes (id, mensaje) VALUES (1, 'Hola Mundo desde Docker y MySQL')"
        )

        cursor.execute("SELECT mensaje FROM mensajes WHERE id = 1")
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        return f"""
            <h1>{resultado[0]}</h1>
            <p>Aplicación conectada correctamente a MySQL.</p>
        """

    except Exception as error:
        return f"Error de conexión con MySQL: {error}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)