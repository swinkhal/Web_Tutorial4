from flask import Flask, request, jsonify

app = Flask(__name__)

# initialize list of users
users = [
    {'id': '1', 'email': 'abc@abc.ca', 'firstName': 'ABC'},
    {'id': '2', 'email': 'xyz@xyz.ca', 'firstName': 'XYZ'}
]

# helper function to generate a unique ID for each user
def generate_id():
    if len(users) == 0:
        return '1'
    else:
        last_user = users[-1]
        return str(int(last_user['id']) + 1)

# helper function to find a user by ID
def find_user(id):
    for user in users:
        if user['id'] == id:
            return user
    return None

@app.route('/users', methods=['GET'])
def get_users():
    # return list of users
    return jsonify({'message': 'Users retrieved', 'success': True, 'users': users}), 200

@app.route('/add', methods=['POST'])
def add_user():
    # get user details from the request body
    user = request.json
    email = user.get('email')
    first_name = user.get('firstName')
    if not email or not first_name:
        return jsonify({'message': 'Missing email or first name', 'success': False}), 400

    # generate a unique ID for the new user
    user_id = generate_id()

    # create new user object
    new_user = {'id': user_id, 'email': email, 'firstName': first_name}

    # add user to list
    users.append(new_user)

    # return success response
    return jsonify({'message': 'User added', 'success': True}), 200

@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    # find user by ID
    user = find_user(id)
    if not user:
        return jsonify({'message': 'User not found', 'success': False}), 404

    # update user details from the request body
    user_data = request.json
    email = user_data.get('email')
    first_name = user_data.get('firstName')
    if email:
        user['email'] = email
    if first_name:
        user['firstName'] = first_name

    # return success response
    return jsonify({'message': 'User updated', 'success': True}), 200


@app.route('/user/<string:id>', methods=['GET'])
def get_user(id):
    for user in users:
        if user['id'] == id:
            return jsonify({
                'success': True,
                'user': user
            })
    return jsonify({
        'message': 'User not found',
        'success': False
    })
