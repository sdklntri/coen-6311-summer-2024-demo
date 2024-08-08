from flask import Flask, request, jsonify, send_from_directory, render_template
from pymongo import MongoClient
from subscribe_routes import subscribe_blueprint
from verify_routes import verify_blueprint
import os
import random

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb+srv://sdhkalantari:29Day1358@cluster0.cjauxdk.mongodb.net/?retryWrites=true&w=majority')
email_verification_db = client.emailVerificationDB
events_read_db = client.events_read_db
events_write_db = client.events_write_db

subscribers_collection = email_verification_db.subscribers
events_collection = events_read_db.events_read

# Ensure unique index on email
subscribers_collection.create_index("email", unique=True)

# Register blueprints
app.register_blueprint(subscribe_blueprint)
app.register_blueprint(verify_blueprint)

# Root route
@app.route('/')
def home():
    return render_template('index.html')
    #return jsonify({"message": "Welcome to the Email Verification App"}), 200


# Route for favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/subscribe_to_event', methods=['POST'])
def subscribe_to_event():
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400
    #email = data.get('email')
    #event_id = data.get('event_id')
    email = data['email']
    event_id = data['event_id']  # Ensure event_id is treated as a string

    print(f"Received request to subscribe email {email} to event_id {event_id}")

    event = events_collection.find_one({"event_id": event_id})
    print(f"Queried event: {event}")

    if not event:
        return jsonify({"error": "Event not found."}), 404

    if email not in event.get('Subscribers', []):
        events_collection.update_one(
            {"event_id": event_id},
            {"$addToSet": {"Subscribers": email}}
        )
        return jsonify({"message": "Subscribed to event successfully."}), 200
    else:
        return jsonify({"message": "Already subscribed to this event."}), 200

@app.route('/publish_event', methods=['POST'])
def publish_event():
    data = request.json
    event_id = str(random.randint(21 , 100)).zfill(3)  # Generate a random 3-digit event ID

    event = {
        "title": data['title'],
        "location": data['location'],
        "date": data['date'],
        "description": data['description'],
        "Subscribers": [],
        "event_id": event_id
    }

    events_collection.insert_one(event)
    print(f"Published event: {event}")

    return jsonify({"message": "Event published successfully.", "event_id": event_id}), 200

if __name__ == '__main__':
    app.run(port=3000)
