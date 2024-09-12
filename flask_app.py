


from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

DATABASE = 'orders.db'
url = "https://Johnkardo1985.github.io"

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def create_tables():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            selected_items TEXT,
            address TEXT,
            phone_number TEXT,
            location TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/order', methods=['POST'])
def create_order():
    try:
        #response = requests.get(url)
        #data = response.json
        data = request.json
        selected_items = json.dumps(data.get('selectedItems', {}), ensure_ascii = False)  # Store selected items as a JSON string
        address = data.get('address', '')
        phone_number = data.get('phone_number', '')
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)
        location = "https://www.google.com/maps?q=" + str(latitude) + "," + str(longitude)


        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (selected_items, address, phone_number, location)
            VALUES (?, ?, ?, ?)
        ''', (selected_items, address, phone_number, location))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Order submitted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/')
def index () :
    return app.send_static_file('index.html')
if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
