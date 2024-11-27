from flask import Blueprint, request, jsonify
from insurance.insurance import Insurance
from flask_jwt_extended import jwt_required

insurance_blueprint = Blueprint('insurance', __name__)

@insurance_blueprint.route('/insurance', methods=['POST'])
@jwt_required()
def add_insurance():
    
    # Add a new insurance record
    data = request.get_json()
    insurance = Insurance(**data)
    valid, msg = insurance.validate()
    if not valid:
        return jsonify({"error": msg}), 400
    
    success, result = insurance.save()
    if success:
        return jsonify({"message": "Insurance record added successfully", "id": result}), 201
    
    return jsonify({"error": result}), 500

@insurance_blueprint.route('/insurance/<id>', methods=['DELETE'])
@jwt_required()
def delete_insurance(id):
    
    if not id:
        return jsonify({"error": "ID is required"}), 400
    
    success, msg = Insurance.delete(id)
    if success:
        return jsonify({"message": "Insurance record deleted successfully"}), 200
    
    return jsonify({"error": msg}), 500

@insurance_blueprint.route('/insurance/<id>', methods=['PUT'])
@jwt_required()
def update_insurance(id):
    
    # Update specific fields in an insurance record by ID
    data = request.get_json()
    if not id:
        return jsonify({"error": "ID is required to update a record"}), 400
    
    insurance = Insurance(**data)
    valid, msg = insurance.validate()
    if not valid:
        return jsonify({"error": msg}), 400
    
    success, msg = Insurance.update(id, **data)
    if success:
        return jsonify({"message": "Insurance record updated successfully"}), 200
    
    return jsonify({"error": msg}), 500

@insurance_blueprint.route('/insurance', methods=['GET'])
@jwt_required()
def search_insurance():
    
    # Collect filters from query parameters
    filters = {key: request.args.get(key) for key in request.args if request.args.get(key) is not None}
        
    result, msg = Insurance.search(filters)
    
    # Check if any records were found
    if result is not None and len(result) > 0:
        return jsonify(result), 200
    elif result is not None and len(result) == 0:
        return jsonify({"error": "No records found matching the search criteria"}), 404
    else:
        return jsonify({"error": msg}), 500