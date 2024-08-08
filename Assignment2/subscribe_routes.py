from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from observer_pattern import event_notifier, Subscriber

subscribe_blueprint = Blueprint('subscribe', __name__)

# MongoDB setup
client = MongoClient('mongodb+srv://sdhkalantari:29Day1358@cluster0.cjauxdk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
email_verification_db = client.emailVerificationDB
subscribers_collection = email_verification_db.subscribers

@subscribe_blueprint.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    email = data['email']
    name = data['name']

    subscriber = {
        "email": email,
        "name": name,
        "verified": False,
        }

    try:
        subscribers_collection.insert_one(subscriber)
        event_notifier.attach(Subscriber(email))
        return jsonify({"message": "Subscription email has been recorded. Verification email sent."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
