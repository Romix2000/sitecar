from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__, static_url_path='/static')



def initialize_database():
    conn = sqlite3.connect('car_rental.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cars'")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute('''
            CREATE TABLE cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')

        cars_data = [
            ("ford fiesta", "вільно"),
            ("renault logan", "вільно"),
            ("citroen с-elysee", "вільно"),
            ("honda accord x", "вільно"),
            ("toyota camry 70", "вільно"),
            ("mercedes C300", "вільно"),
            ("lexus ES", "вільно"),
            ("VW touareg", "вільно"),
            ("BMW X5", "вільно"),
            ("mercedes sprinter", "вільно"),
            ("mercedes atego (1222)", "вільно"),
            ("mercedes atego (2545)", "вільно")
        ]

        for car_data in cars_data:
            cursor.execute('INSERT INTO cars (model, status) VALUES (?, ?)', car_data)

        conn.commit()

    conn.close()

initialize_database()

@app.route('/')
def index():
    conn = sqlite3.connect('car_rental.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cars')
    cars = cursor.fetchall()
    conn.close()

    return render_template('index.html', cars=cars)

@app.route('/update_status/<int:car_id>', methods=['POST'])
def update_status(car_id):
    conn = sqlite3.connect('car_rental.db')
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM cars WHERE id=?', (car_id,))
    current_status = cursor.fetchone()[0]
    new_status = 'занято' if current_status == 'вільно' else 'вільно'
    cursor.execute('UPDATE cars SET status=? WHERE id=?', (new_status, car_id))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
