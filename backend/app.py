from flask import Flask, jsonify
from backend.models import DatabaseHandler

app = Flask(__name__)

@app.route('/api/scoreboard/<int:week>', methods=['GET'])
def get_data():
    conn = DatabaseHandler
    data = conn.execute('SELECT * FROM your_table').fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)