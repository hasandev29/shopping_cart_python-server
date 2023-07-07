from flask import Blueprint, jsonify, request
from jsonschema import validate, ValidationError
from pymongo.errors import PyMongoError

from app.models.schemas import categorySchema

import sys

sys.path.append('../../')
from config import mongo

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'GET':
        
        try:
            categories = mongo.db.categories.find()
        except PyMongoError as e:
            return jsonify({'error': e})
        
        categoriesList = []
        for cat in categories:
            categoryData = {
                '_id': str(cat['_id']),
                'catName': cat['catName'],
                'catImage': cat['catImage']    
            }
            categoriesList.append(categoryData)
        
        return jsonify({
            'status': 'success',
            'data_count': len(categoriesList),
            'data': categoriesList})
    
    elif request.method == 'POST':
        data = request.get_json()
        
        try:
            validate(data, categorySchema)
        except ValidationError as e:
            return jsonify({'error': e.message}), 400
            
        category_id = mongo.db.categories.insert_one({
            'catName': data['catName'],
            'catImage': data['catImage']
        }).inserted_id
        
        data['_id'] = str(category_id)
        
        return jsonify({
            "status": "success",
            "data": data
            }), 200
    
    else:
        return 405