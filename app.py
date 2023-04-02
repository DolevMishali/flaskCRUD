from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

db_path = os.path.join(app.root_path, 'data.csv')

# Read all resources
@app.route('/my_resource', methods=['GET'])
def get_all_my_resources():
    with open(db_path, mode='r') as file:
        reader = csv.DictReader(file)
        my_resources = [row for row in reader]

    return jsonify(my_resources)



# Create a new resource
@app.route('/my_resource', methods=['POST'])
def add_my_resource():
    with open(db_path, mode='a', newline='') as file:
        fieldnames = ['id', 'name', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        name = request.json['name']
        description = request.json['description']

        writer.writerow({'id': get_next_id(), 'name': name, 'description': description})

    return jsonify({'message': 'Resource created successfully'})

# Update a resource by ID
@app.route('/my_resource/<int:id>', methods=['PUT'])
def update_my_resource_by_id(id):
    with open(db_path, mode='r') as file:
        reader = csv.DictReader(file)
        my_resources = [row for row in reader]

    my_resource = next((row for row in my_resources if int(row['id']) == id), None)

    if my_resource:
        my_resource['name'] = request.json.get('name', my_resource['name'])
        my_resource['description'] = request.json.get('description', my_resource['description'])

        with open(db_path, mode='w', newline='') as file:
            fieldnames = ['id', 'name', 'description']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(my_resources)

        return jsonify({'message': 'Resource updated successfully'})
    else:
        return jsonify({'message': 'Resource not found'})

# Delete a resource by ID
@app.route('/my_resource/<int:id>', methods=['DELETE'])
def delete_my_resource_by_id(id):
    with open(db_path, mode='r') as file:
        reader = csv.DictReader(file)
        my_resources = [row for row in reader]

    my_resource = next((row for row in my_resources if int(row['id']) == id), None)
    if my_resource:
        my_resources.remove(my_resource)

        with open(db_path, mode='w', newline='') as file:
            fieldnames = ['id', 'name', 'description']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            for i, row in enumerate(my_resources): #Added to update the IDs after deleting
                row['id'] = str(i + 1)

            writer.writeheader()
            writer.writerows(my_resources)

        return jsonify({'message': 'Resource deleted successfully'})
    else:
        return jsonify({'message': 'Resource not found'})


# Read a single resource by ID
@app.route('/my_resource/<int:id>', methods=['GET'])
def get_my_resource_by_id(id):
    with open(db_path, mode='r') as file:
        reader = csv.DictReader(file)
        my_resource = next((row for row in reader if int(row['id']) == id), None)

    if my_resource:
        return jsonify(my_resource)
    else:
        return jsonify({'message': 'Resource not found'})

# Read a single resource by Name
@app.route('/my_resource/<string:name>', methods=['GET'])
def get_my_resource_by_name(name):
    with open(db_path, mode='r') as file:
        reader = csv.DictReader(file)
        my_resource = next((row for row in reader if row['name'] == name), None)

    if my_resource:
        return jsonify(my_resource)
    else:
        return jsonify({'message': 'Resource not found'})

# Helper function to get the next available ID
def get_next_id():
    with open(db_path, mode='r') as file:
        reader = csv.DictReader(file)
        ids = [int(row['id']) for row in reader]

    if ids:
        return max(ids) + 1
    else:
        return 1