import json
import time

from flask import Flask, request, jsonify

app = Flask(__name__)

# Load seeded data from seed.json
try:
    with open('seed.json', 'r') as f:
        raw_users = json.load(f)
        # Convert keys to match internal structure
        users = [
            {
                "id": u["id"],
                "username": u["doggy"],
                "password": u["zebra42"],
                "email": u["kittycat"],
                "age": u["rocketShip"]
            } for u in raw_users
        ]
except FileNotFoundError:
    users = []


# GET: Return all users
# cRud snippet goes here
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# POST: Add a new user
# Crud snippet goes here
# although we are creating new users with this route
# when deleting, it can cause voerlap in id's
# also passwords aren't hashed
@app.route('/users', methods=['POST'])
def create_user():
   data = request.get_json()
   new_user = {
       'username': data.get('username'),
       'email': data.get('email'),
       'age': data.get('age'),
       'password': data.get('password'),
       'id': len(users) + 1
   }
   users.append(new_user)
   return jsonify(new_user), 201

# PUT: Update user by ID
# crUd snippet goes here
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
   data = request.get_json()
   for user in users:
       if user['id'] == user_id:
           user['username'] = data.get('username', user['username'])
           user['email'] = data.get('email', user['email'])
           user['age'] = data.get('age', user['age'])
           user['password'] = data.get('password', user['password'])
           return jsonify(user), 200
   return jsonify({"error": "User not found"}), 404

# DELETE: Remove user by ID
# cruD snippet goes here
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
  global users
  user = next((u for u in users if u['id'] == user_id), None)
  if not user:
    return jsonify({"error": "User not found"}), 404
  users = [u for u in users if u['id'] != user_id]
  return jsonify({"message": f"User {user_id} deleted"}), 200

# Starting the server (open docker first)
# docker build -t flask-puzzle-server .
# docker run -p 5001:5000 flask-puzzle-server

# curl commands

# Get all user data
# curl http://localhost:5001/users

# Create a user
# curl -X POST http://localhost:5001/users \
# -H "Content-Type: application/json" \
# -d '{"username":"ChrisRome", "email":"romero@gmail.com", "age":25, "password": "pass"}'

# This creates:
# {
#    "age": 25,
#    "email": "romero@gmail.com",
#    "id": 30,
#    "password": "pass",
#    "username": "ChrisRome"
#  }

# Update a user (PUT) by id
# curl -X PUT http://localhost:5001/users/30 \
# -H "Content-Type: application/json" \
# -d '{"username":"RomeroChristopher"}'

# Now the created user is this:
# {
#   "age": 25,
#   "email": "romero@gmail.com",
#   "id": 30,
#    "password": "pass",
#    "username": "RomeroChristopher"
#  }
# starts the application, and binds to 127.0.0.1 NOT localhost!!!

# Now Delete a user but id (my created one)
# curl -X DELETE http://localhost:5001/users/30

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
