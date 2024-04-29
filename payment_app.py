# from flask import Flask, request, jsonify
# import pika  # RabbitMQ için kullanılan kütüphane
# import sqlite3

# app = Flask(__name__)

# # RabbitMQ bağlantı parametreleri
# QUEUE_HOST = 'localhost'
# QUEUE_PORT = 5672
# QUEUE_USERNAME = 'guest'
# QUEUE_PASSWORD = 'guest'

# # Ödeme işlemi kuyruğu için tanımlanan isim
# PAYMENT_QUEUE_NAME = 'payment_queue'

# # SQLite veritabanı dosyası
# DATABASE = 'homework_db.db'
# # Öğrenci ve ödeme tablolarını oluşturacak fonksiyon
# def create_tables():
#     conn = sqlite3.connect(DATABASE)
#     c = conn.cursor()
    
#     # Öğrenci tablosunu oluştur
#     c.execute('''CREATE TABLE IF NOT EXISTS students (
#                     student_id INTEGER PRIMARY KEY,
#                     student_no TEXT UNIQUE,
#                     tuition_total REAL,
#                     balance REAL
#                 )''')
    
#     # Ödeme tablosunu oluştur
#     c.execute('''CREATE TABLE IF NOT EXISTS payments (
#                     payment_id INTEGER PRIMARY KEY,
#                     student_no TEXT,
#                     term TEXT,
#                     amount REAL,
#                     payment_status TEXT,
#                     FOREIGN KEY (student_no) REFERENCES students (student_no)
#                 )''')
    
#     conn.commit()
#     conn.close()

# # Veritabanı tablolarını oluştur
# create_tables()
# # Diğer kodlar buraya gelecek

# def create_payment_channel():
#     # RabbitMQ bağlantısı oluştur
#     credentials = pika.PlainCredentials(QUEUE_USERNAME, QUEUE_PASSWORD)
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=QUEUE_HOST, port=QUEUE_PORT, credentials=credentials))
#     channel = connection.channel()

#     # Ödeme kuyruğunu tanımla
#     channel.queue_declare(queue=PAYMENT_QUEUE_NAME)

#     return channel

# @app.route('/v1/pay-tuition', methods=['POST'])
# def pay_tuition():
#     data = request.get_json()
#     student_no = data.get('student_no')
#     term = data.get('term')

#     # Ödeme işlemi veritabanına işle
#     # Bu kısımda ödemenin gerçekleştirilmesi ve ödeme durumunun güncellenmesi yapılacak

#     # Ödeme bilgilerini RabbitMQ kuyruğuna gönder
#     payment_channel = create_payment_channel()
#     payment_channel.basic_publish(exchange='', routing_key=PAYMENT_QUEUE_NAME, body=student_no)

#     return jsonify({"payment_status": "In Progress"}), 200

# if __name__ == '__main__':
#     app.run(debug=True, port=9090)
from flask import Flask, request, jsonify
import pika  # RabbitMQ için kullanılan kütüphane
import sqlite3

app = Flask(__name__)

# RabbitMQ bağlantı parametreleri
QUEUE_HOST = 'localhost'
QUEUE_PORT = 5672
QUEUE_USERNAME = 'guest'
QUEUE_PASSWORD = 'guest'

# Ödeme işlemi kuyruğu için tanımlanan isim
PAYMENT_QUEUE_NAME = 'payment_queue'

# SQLite veritabanı dosyası
DATABASE = 'homework_db.db'

# Öğrenci ve ödeme tablolarını oluşturacak fonksiyon
def create_tables():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Öğrenci tablosunu oluştur
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY,
                    student_no TEXT UNIQUE,
                    tuition_total REAL,
                    balance REAL
                )''')
    
    # Ödeme tablosunu oluştur
    c.execute('''CREATE TABLE IF NOT EXISTS payments (
                    payment_id INTEGER PRIMARY KEY,
                    student_no TEXT,
                    term TEXT,
                    amount REAL,
                    payment_status TEXT,
                    FOREIGN KEY (student_no) REFERENCES students (student_no)
                )''')
    
    conn.commit()
    conn.close()

# Veritabanı tablolarını oluştur
create_tables()
def insert_data(student_no, tuition_total, balance):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Öğrencinin veritabanında olup olmadığını kontrol et
    c.execute("SELECT student_id FROM students WHERE student_no=?", (student_no,))
    existing_record = c.fetchone()
    
    # Eğer öğrenci yoksa, yeni öğrenciyi ekle
    if existing_record is None:
        c.execute("INSERT INTO students (student_no, tuition_total, balance) VALUES (?, ?, ?)",
                  (student_no, tuition_total, balance))
        conn.commit()
        print("Yeni öğrenci eklendi.")
    else:
        print("Öğrenci zaten veritabanında var.")
    
    conn.close()
# Önce veritabanı oluşturulması gerekiyor

# #Örnek verileri eklemek için fonksiyonu kullanabiliriz
insert_data('S001', 1000.0, 500.0)
insert_data('S002', 1500.0, 1500.0)
# insert_data('S003', 2000.0, 60.0)

def insert_payment(student_no, term, amount, payment_status):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    try:
        c.execute("INSERT INTO payments (student_no, term, amount, payment_status) VALUES (?, ?, ?, ?)",
                  (student_no, term, amount, payment_status))
        conn.commit()
        print("Yeni ödeme eklendi.")
    except sqlite3.IntegrityError:
        print("Ödeme zaten var.")
    
    conn.close()


# # Örnek verileri eklemek için fonksiyonu kullanabiliriz
insert_payment('S001', 'Spring2024', 1000.0, 'Paid')
insert_payment('S002', 'Spring2024', 1500.0, 'Unpaid')
# insert_payment('S003', 'Spring2024', 2000.0, 'Paid')
def create_payment_channel():
    # RabbitMQ bağlantısı oluştur
    credentials = pika.PlainCredentials(QUEUE_USERNAME, QUEUE_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=QUEUE_HOST, port=QUEUE_PORT, credentials=credentials))
    channel = connection.channel()

    # Ödeme kuyruğunu tanımla
    channel.queue_declare(queue=PAYMENT_QUEUE_NAME)

    return channel

def process_payment(student_no, term):
    # Ödeme işlemini gerçekleştir
    # Ödeme işlemi başarılıysa, veritabanında ödeme durumunu güncelle

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Ödeme durumunu güncelle
    c.execute("UPDATE payments SET payment_status = ? WHERE student_no = ? AND term = ?",
              ("Paid", student_no, term))
    
    conn.commit()
    conn.close()

@app.route('/v1/pay-tuition', methods=['POST'])
def pay_tuition():
    data = request.get_json()
    student_no = data.get('student_no')
    term = data.get('term')

    # Ödeme işlemi veritabanına işle
    process_payment(student_no, term)

    # Ödeme bilgilerini RabbitMQ kuyruğuna gönder
    payment_channel = create_payment_channel()
    payment_channel.basic_publish(exchange='', routing_key=PAYMENT_QUEUE_NAME, body='S001')
    # Ödeme isteğini RabbitMQ'ya gönderelim

    return jsonify({"payment_status": "In Progress"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=9090)
