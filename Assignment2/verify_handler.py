def verify(db, email):
    try:
        result = db.subscribers.update_one({"email": email}, {"$set": {"verified": True}})
        if result.matched_count == 0:
            raise Exception('Email not found')
        return {"message": "Email verified"}
    except Exception as e:
        print('Error during verification:', e)
        raise Exception('Error during verification')
