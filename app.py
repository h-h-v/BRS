from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from flask_session import Session

app = Flask(__name__)

# Configure session
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Define your database connection details
DATABASE_URL = 'postgres://ermmmhea:o3nwulL9fesvtV9VHHcPAiXIlC6irytd@snuffleupagus.db.elephantsql.com/ermmmhea'

# Function to fetch buses from the database
def get_buses(from_location=None, to_location=None, travel_date=None):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        select_query = "SELECT * FROM buses WHERE 1=1"
        params = []

        if from_location:
            select_query += " AND route LIKE %s"
            params.append(f"%{from_location}%")

        if to_location:
            select_query += " AND route LIKE %s"
            params.append(f"%{to_location}%")

        if travel_date:
            select_query += " AND date = %s"
            params.append(travel_date)

        cursor.execute(select_query, params)
        rows = cursor.fetchall()
        return rows

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        if conn is not None:
            conn.close()

# Route to search for buses
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    from_location = request.form.get('from')
    to_location = request.form.get('to')
    travel_date = request.form.get('date')

    buses = get_buses(from_location, to_location, travel_date)
    username = session.get('username')  # Get the username from the session

    return render_template('search_result.html', buses=buses, from_location=from_location, to_location=to_location, username=username)

# Route to view seats
@app.route('/view_seats')
def view_seats():
    bus_id = request.args.get('bus_id')
    bus_details = {'bus_name': 'Demo Bus', 'from_location': 'City A', 'to_location': 'City B'}
    return render_template('view_seats.html', bus_details=bus_details)

# Route to add passenger details
@app.route('/add-passenger', methods=['GET', 'POST'])
def add_passenger():
    if request.method == 'POST':
        # Assuming you process and validate the form data here
        # Redirect to confirm booking after adding passenger details
        return redirect(url_for('confirm_booking'))
    else:
        seats = request.args.get('seats')
        if seats:
            seat_ids = seats.split(',')
            return render_template('add_passenger.html', seat_ids=seat_ids)
        else:
            return "No seats selected", 400


# Route to confirm booking
@app.route('/confirm-booking', methods=['POST'])
def confirm_booking():
    bus_details = {
        'bus_name': 'Demo Bus', 
        'from_location': 'City A', 
        'to_location': 'City B',
        'date': '2024-05-20'
    }
    
    # Extract passenger details from the form
    passengers = {}
    for key in request.form.keys():
        if key.startswith('name_'):
            seat_id = key.split('_')[1]
            passengers[seat_id] = {
                'name': request.form.get(f'name_{seat_id}'),
                'email': request.form.get(f'email_{seat_id}'),
                'age': request.form.get(f'age_{seat_id}'),
                'gender': request.form.get(f'gender_{seat_id}')
            }
    
    # Calculate total price
    total_price = len(passengers) * 1800  # Assuming each ticket costs 1800

    return render_template('confirm_booking.html', bus_details=bus_details, passengers=passengers, total_price=total_price)


# Route for login
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'user' and password == 'pass':
        session['username'] = username
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

# Route for logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
