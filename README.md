# 🚨 Smart Emergency SOS

Smart Emergency SOS is a Flask-based emergency assistance web application designed to help users quickly access their location and manage emergency contacts.

## 🎯 Objective

The main objective of this project is to provide a simple emergency assistance system where users can:

- Activate an SOS request
- Get their current location
- Open the location in Google Maps
- Save emergency contacts
- Call saved emergency contacts
- Maintain emergency request history

## ✨ Features

### 🚨 SOS Activation
Users can press the SOS button to start an emergency request.

### 📍 Live Location
The application uses browser geolocation to obtain the user's current latitude and longitude.

### 🗺️ Google Maps
The captured coordinates can be opened directly in Google Maps.

### 👥 Emergency Contacts
Users can add trusted emergency contacts with their name and phone number.

### 📱 Call Contact
Saved contacts include a call option for supported devices.

### 📝 Emergency History
Every SOS activation is stored with:
- Event
- Location
- Date and time

## 🛠️ Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- SQLite
- Git & GitHub
- Browser Geolocation API

## 📂 Project Structure

```text
Smart_Emergency_SOS/
│
├── app.py
├── database.db
├── .gitignore
├── README.md
│
└── templates/
    └── index.html
    