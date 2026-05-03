from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime, date
import random
import string

app = Flask(__name__)

# Room data
ROOMS = {
    'Standard': {'price': 100, 'capacity': 5},
    'Deluxe': {'price': 150, 'capacity': 3},
    'Suite': {'price': 250, 'capacity': 1}
}

BOOKINGS_FILE = 'bookings.json'

def load_bookings():
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_bookings(bookings):
    with open(BOOKINGS_FILE, 'w') as f:
        json.dump(bookings, f, indent=4)

def generate_ref():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(8))

def dates_overlap(start1, end1, start2, end2):
    return max(start1, start2) < min(end1, end2)

def get_available_rooms(checkin, checkout):
    bookings = load_bookings()
    available = {}
    for room_type, data in ROOMS.items():
        booked_count = 0
        for booking in bookings:
            if booking['room_type'] == room_type:
                b_checkin = date.fromisoformat(booking['checkin'])
                b_checkout = date.fromisoformat(booking['checkout'])
                if dates_overlap(checkin, checkout, b_checkin, b_checkout):
                    booked_count += 1
        if booked_count < data['capacity']:
            available[room_type] = data
    return available

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    checkin_str = request.form['checkin']
    checkout_str = request.form['checkout']
    try:
        checkin = date.fromisoformat(checkin_str)
        checkout = date.fromisoformat(checkout_str)
        if checkin >= checkout or checkin < date.today():
            return render_template('home.html', error="Invalid dates")
        available = get_available_rooms(checkin, checkout)
        return render_template('search.html', available=available, checkin=checkin_str, checkout=checkout_str)
    except ValueError:
        return render_template('home.html', error="Invalid date format")

@app.route('/book/<room_type>', methods=['GET', 'POST'])
def book(room_type):
    if room_type not in ROOMS:
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        # Validate
        try:
            checkin_date = date.fromisoformat(checkin)
            checkout_date = date.fromisoformat(checkout)
            nights = (checkout_date - checkin_date).days
            total_price = ROOMS[room_type]['price'] * nights
            ref = generate_ref()
            booking = {
                'ref': ref,
                'name': name,
                'email': email,
                'checkin': checkin,
                'checkout': checkout,
                'room_type': room_type,
                'total_price': total_price
            }
            bookings = load_bookings()
            bookings.append(booking)
            save_bookings(bookings)
            return render_template('confirm.html', booking=booking)
        except ValueError:
            return render_template('book.html', room_type=room_type, checkin=checkin, checkout=checkout, error="Invalid data")
    else:
        checkin = request.args.get('checkin')
        checkout = request.args.get('checkout')
        return render_template('book.html', room_type=room_type, checkin=checkin, checkout=checkout)

@app.route('/cancel', methods=['GET', 'POST'])
def cancel():
    if request.method == 'POST':
        ref = request.form['ref']
        bookings = load_bookings()
        for i, booking in enumerate(bookings):
            if booking['ref'] == ref:
                removed = bookings.pop(i)
                save_bookings(bookings)
                return render_template('cancel_confirm.html', booking=removed)
        return render_template('cancel.html', error="Booking not found")
    return render_template('cancel.html')

if __name__ == '__main__':
    app.run(debug=True)