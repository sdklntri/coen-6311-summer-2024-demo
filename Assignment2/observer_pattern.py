from abc import ABC, abstractmethod
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb+srv://sdhkalantari:29Day1358@cluster0.cjauxdk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
events_write_db = client.event_write_db
events_collection = events_write_db.events_write

class Observer(ABC):
    @abstractmethod
    def update(self, event):
        pass

class Subject(ABC):
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self, event):
        for observer in self._observers:
            observer.update(event)

class EventNotifier(Subject):
    def add_event(self, event):
        events_collection.insert_one(event)
        self.notify(event)

class Subscriber(Observer):
    def __init__(self, email):
        self.email = email
    
    def update(self, event):
        print(f"Notification sent to {self.email}: New event {event['name']} has been published.")

event_notifier = EventNotifier()
