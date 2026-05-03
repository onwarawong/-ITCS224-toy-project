# Hotel Reservation App

A simple Flask web app for hotel room reservations.

## Features
- Search for available rooms by check-in and check-out dates
- Book a room with guest details
- Receive a booking confirmation with reference number
- Cancel a booking using the reference number
- Mobile-friendly design

## Installation
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`
3. Open http://127.0.0.1:5000 in your browser

## Usage
- Enter check-in and check-out dates on the home page
- Select an available room type
- Fill in guest name and email
- Confirm the booking
- To cancel, use the reference number from the confirmation

## Data Storage
Bookings are stored in `bookings.json` locally.