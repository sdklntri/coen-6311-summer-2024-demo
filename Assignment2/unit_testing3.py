import unittest
import json
import logging
from unittest.mock import patch
from app import app, email_verification_db, events_read_db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.subscribers_collection = email_verification_db.subscribers
        cls.events_collection = events_read_db.events_read

        # Add sample data for testing
        cls.sample_event = {
            "title": "Sample Event",
            "location": "Sample Location",
            "date": "2024-08-01",
            "description": "This is a sample event.",
            "Subscribers": [],
            "event_id": "999"
        }

        cls.sample_subscriber = {
            "email": "test@example.com",
            "name": "Test User"
        }

        # Insert sample event
        cls.events_collection.insert_one(cls.sample_event)
        # Insert sample subscriber
        cls.subscribers_collection.insert_one(cls.sample_subscriber)

    @classmethod
    def tearDownClass(cls):
        # Clean up test data
        cls.events_collection.delete_one({"event_id": "999"})
        cls.subscribers_collection.delete_one({"email": "test@example.com"})

    def test_publish_event(self):
        response = self.client.post('/publish_event', data=json.dumps({
            "title": "New Event",
            "location": "New Location",
            "date": "2024-08-02",
            "description": "This is a new event."
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200, msg='Equal')
        logger.info(f"Publish Event Test: Received status code {response.status_code}")
        self.assertIn("Event published successfully.", response.json['message'])
        logger.info("Publish Event Test: Correct success message received")

        event_id = response.json['event_id']
        event = self.events_collection.find_one({"event_id": event_id})
        self.assertIsNotNone(event)
        logger.info(f"Publish Event Test: Event with ID {event_id} found in database")

        # Clean up the inserted event
        self.events_collection.delete_one({"event_id": event_id})

    def test_subscribe_to_event(self):
        response = self.client.post('/subscribe_to_event', data=json.dumps({
            "email": "test@example.com",
            "event_id": "999"
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200, msg='Equal')
        logger.info(f"Subscribe to Event Test: Received status code {response.status_code}")
        self.assertIn("Subscribed to event successfully.", response.json['message'])
        logger.info("Subscribe to Event Test: Correct success message received")

        event = self.events_collection.find_one({"event_id": "999"})
        self.assertIn("test@example.com", event["Subscribers"])
        logger.info("Subscribe to Event Test: Subscriber email found in event subscribers list")

        # Clean up the inserted subscriber from the event
        self.events_collection.update_one(
            {"event_id": "999"},
            {"$pull": {"Subscribers": "test@example.com"}}
        )

    @patch('builtins.print')
    def test_publish_event_to_subscribers(self, mock_print):
        # Insert a mock event with subscribers
        event_id = '061'
        subscribers = ['subscriber1@example.com', 'subscriber2@example.com']
        self.events_collection.insert_one({
            'title': 'Event to Publish',
            'location': 'Publish Location',
            'date': '2024-08-01',
            'description': 'This event is for testing publish to subscribers.',
            'Subscribers': subscribers,
            'event_id': event_id
        })
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)

        # Function to publish the event to subscribers
        def publish_event_to_subscribers(event_id):
            event = self.events_collection.find_one({'event_id': event_id})
            if event:
                for subscriber in event['Subscribers']:
                    print(f"Summary for {subscriber}: Title: {event['title']}, "
                          f"Location: {event['location']}, Date: {event['date']}, "
                          f"Description: {event['description']}")

        # Publish the event to subscribers
        publish_event_to_subscribers(event_id)

        # Check that the print function was called for each subscriber
        expected_calls = [
            unittest.mock.call(f"Summary for subscriber1@example.com: Title: Event to Publish, Location: Publish Location, Date: 2024-08-01, Description: This event is for testing publish to subscribers."),
            unittest.mock.call(f"Summary for subscriber2@example.com: Title: Event to Publish, Location: Publish Location, Date: 2024-08-01, Description: This event is for testing publish to subscribers.")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=True)
        logger.debug("Publish Event to Subscribers Test: All subscribers received event summary")

        # Clean up the inserted event
        #self.events_collection.delete_one({"event_id": event_id})

if __name__ == '__main__':
    unittest.main()
