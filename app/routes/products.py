from flask import Blueprint, jsonify, request
from jsonschema import validate, ValidationError
from bson import ObjectId
from pymongo.errors import PyMongoError
import io

from app.models.schemas import productSchema

import sys

sys.path.append('../../')
from config import mongo

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET', 'POST'])
def products():
    
    # GET Method
    if request.method == 'GET':
        products = mongo.db.products.find()
        product_list = []
        for pdt in products:
            product_data = {
                '_id': str(pdt['_id']),
                'pdtName': pdt['pdtName'],
                'pdtPrice': pdt['pdtPrice'],
                'pdtDesc': pdt['pdtDesc'],
                'pdtCategory': pdt['pdtCategory'],
                'pdtImage': pdt['pdtImage']
            }
            product_list.append(product_data)
            
        return jsonify({
            "status": "success",
            "data_count": len(product_list),
            "products": product_list
            }), 200
    
    # POST Method
    elif request.method == 'POST':
        data = request.get_json()
        
        # Input Validation
        try:
            validate(data, productSchema)
        except ValidationError as error:
            return ({"invalid input": error.message}), 400

    
        product_id = mongo.db.products.insert_one({
                'pdtName': data['pdtName'],
                'pdtPrice': data['pdtPrice'],
                'pdtDesc': data['pdtDesc'],
                'pdtCategory': data['pdtCategory'],
                'pdtImage': data['pdtImage'],
            }).inserted_id
            
        data['_id'] = str(product_id)
            
        return jsonify({
            "status": "success",
            "product": data
        }), 200
    
    else:
        return 405
    

@products_bp.route('/products/<id>', methods=['PUT', 'DELETE'])
def product(id):
    
    # PUT Method
    if request.method == 'PUT':
        data = request.get_json()
        
        # Input Validation
        try:
            validate(data, productSchema)
        except ValidationError as error:
            return ({"invalid input": error.message}), 400

        # Update Product
        result = mongo.db.products.update_one(
            { '_id': ObjectId(id)},
            { '$set': {
                'pdtName': data['pdtName'],
                'pdtPrice': data['pdtPrice'],
                'pdtDesc': data['pdtDesc'],
                'pdtCategory': data['pdtCategory'],
                'pdtImage': data['pdtImage']
            }}, upsert=False)
        
        # Error handling
        if result.matched_count == 0:
            return jsonify({'status': "error",
                            'message': "Product not found"}), 404
        else:
            if result.modified_count == 1:
                document = mongo.db.products.find_one({'_id': ObjectId(id)})
                document['_id'] = str(document['_id'])
                return jsonify({
                    'status': "success",
                    'message': "Product Updated successfully",
                    'data': document}), 200
            else:
                return jsonify({
                    'status': "success",
                    'message': "The product remains unchanged without any updates"}), 200
        
            
    # DELETE Method
    elif request.method == 'DELETE':
        
        try:
            result = mongo.db.products.delete_one({'_id': ObjectId(id)})

            if result.deleted_count == 1:
                return jsonify({"message": "Product deleted successfully"}), 200
            else:
                return jsonify({"message": "Product not found"}), 404
        
        except PyMongoError as error:
            return jsonify({"error": error.message}), 500
        
    else:
        return 405
    
# GET Products based on Category
@products_bp.route('/products/category/<category>', methods=['GET'])
def getProductsCategory(category):
    
    try:
        products = mongo.db.products.find({'pdtCategory': category})
    except PyMongoError as error:
        return jsonify({'status': 'error', 'message': 'Products not found for this category', 'error': error})
    
    # products['_id'] = str(products['_id'])
    print(products)
    
    product_list = []
    for pdt in products:
        product_data = {
            '_id': str(pdt['_id']),
            'pdtName': pdt['pdtName'],
            'pdtPrice': pdt['pdtPrice'],
            'pdtDesc': pdt['pdtDesc'],
            'pdtCategory': pdt['pdtCategory'],
            'pdtImage': pdt['pdtImage']
        }
        product_list.append(product_data)
        
    return jsonify({'status': 'success', 'message': f'Products in {category} category fetched successfully',
                    'data_count': len(product_list),
                    'products': product_list})