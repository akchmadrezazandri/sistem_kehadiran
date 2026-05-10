from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os


app = Flask(__name__)
load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

@app.route('/')
def home():
    return jsonify({
        "message": "Sistem Kehadiran Aktif"
    })

@app.route('/absen', methods=['POST'])
def absen():
    data = request.json

    nama = data['nama']
    status = data['status']

    cursor = db.cursor()

    query = "INSERT INTO absensi (nama, status) VALUES (%s, %s)"
    values = (nama, status)

    cursor.execute(query, values)
    db.commit()

    return jsonify({
        "message": "Absensi berhasil ditambahkan"
    })

@app.route('/data')
def data():
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM absensi")

    hasil = cursor.fetchall()

    return jsonify(hasil)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy"
    })

if __name__ == '__main__':
    app.run(debug=True)