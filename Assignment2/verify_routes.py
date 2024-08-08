from flask import Blueprint, request, jsonify
from pymongo import MongoClient

verify_blueprint = Blueprint('verify', __name__)

# MongoDB setup
client = MongoClient('mongodb+srv://sdhkalantari:29Day1358@cluster0.cjauxdk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
email_verification_db = client.emailVerificationDB
subscribers_collection = email_verification_db.subscribers

@verify_blueprint.route('/verify', methods=['GET'])
def verify():
    email = request.args.get('email')
    result = subscribers_collection.update_one({"email": email}, {"$set": {"verified": True}})

    if result.modified_count == 1:
        return jsonify({"message": "Email verified successfully."}), 200
    else:
        return jsonify({"error": "Verification failed."}), 400
