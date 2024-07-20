from pymongo import MongoClient
import json

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.bookstore

# Read JSON data from file
with open('books.json', 'r') as file:
    books = json.load(file)

# Insert data into MongoDB
db.books.insert_many(books)

print("Data inserted successfully!")
