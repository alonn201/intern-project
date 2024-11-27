from flask import Blueprint, request, jsonify
from claims.claims import Claim
from flask_jwt_extended import jwt_required

claim_blueprint = Blueprint('claim', __name__)

@claim_blueprint.route('/claim', methods=['POST'])
@jwt_required()
def add_Claim():
    
    # Add a new Claim record
    data = request.get_json()
    claim = Claim(**data)
    valid, msg = claim.validate()
    if not valid:
        return jsonify({"error": msg}), 400
    
    success, result = claim.save()
    if success:
        return jsonify({"message": "Claim record added successfully", "id": result}), 201
    
    return jsonify({"error": result}), 500

@claim_blueprint.route('/claim/<id>', methods=['DELETE'])
@jwt_required()
def delete_claim(id):
    
    if not id:
        return jsonify({"error": "ID is required"}), 400
    
    success, msg = Claim.delete(id)
    if success:
        return jsonify({"message": "Claim record deleted successfully"}), 200
    
    return jsonify({"error": msg}), 500

@claim_blueprint.route('/claim/<id>', methods=['PUT'])
@jwt_required()
def update_claim(id):
    
    data = request.get_json()
    
    if not id:
        return jsonify({"error": "ID is required to update a record"}), 400
    
    claim = Claim(**data)
    valid, msg = claim.validate()
    if not valid:
        return jsonify({"error": msg}), 400
    
    success, msg = Claim.update(id, **data)
    if success:
        return jsonify({"message": "Claim record updated successfully"}), 200
    
    return jsonify({"error": msg}), 500

@claim_blueprint.route('/claim', methods=['GET'])
@jwt_required()
def search_claim():
    
    # Collect filters from query parameters
    filters = {key: request.args.get(key) for key in request.args if request.args.get(key) is not None}
        
    result, msg = Claim.search(filters)
    
    # Check if any records were found
    if result is not None and len(result) > 0:
        return jsonify(result), 200
    elif result is not None and len(result) == 0:
        return jsonify({"error": "No records found matching the search criteria"}), 404
    else:
        return jsonify({"error": msg}), 500