from flask import Blueprint, jsonify, request
from jsonschema import validate, ValidationError
from bson import ObjectId
from pymongo.errors import PyMongoError

from app.models.schemas import cartSchema

import sys

sys.path.append('../../')
from config import mongo

cart_Bp = Blueprint('cart', __name__)

@cart_Bp.route('/cart', methods=['GET', 'POST'])
def cart():
    # GET Method
    if request.method == 'GET':
        
        try:
            cart_items = mongo.db.carts.find()
        except PyMongoError as e:
            return jsonify({'error': e})
        
        cartList = []
        for cart in cart_items:
            cartData = {
                '_id': str(cart['_id']),
                "userId": cart["userId"],
                "pdtId": str(cart["pdtId"]),
                "quantity": cart["quantity"],
                "price": cart["price"],
                "total": cart["total"]  
            }
            cartList.append(cartData)
        
        return jsonify({
            'status': 'success',
            'data_count': len(cartList),
            'items': cartList})
    
    # POST Method
    elif request.method == 'POST':
        data = request.get_json()
        
        try:
            validate(data, cartSchema)
        except ValidationError as e:
            return jsonify({'error': e.message}), 400
        
        cart_id = mongo.db.carts.insert_one({
          "userId": data["userId"],
          "pdtId": ObjectId(data["pdtId"]),
          "quantity": data["quantity"],
          "price": data["price"],
          "total": data["total"]
        }).inserted_id
        
        data['_id'] = str(cart_id)
        
        return jsonify({
            "status": "success",
            "data": data}), 200
    
    else:
        return 405
    
@cart_Bp.route('/cart/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def cart_id(id):
    
    # GET Method
    if request.method == 'GET':
        user_id = id
        
        try:
            cart_items = mongo.db.carts.find({'userId': user_id})
        except PyMongoError as e:
            return jsonify({'message': e.message}), 400
        
        cart_items = [
            {
                '_id': str(item['_id']),
                'userId': item['userId'],
                'pdtId': str(item['pdtId']),
                'quantity': item['quantity'],
                'price': item['price'],
                'total': item['total']
            } for item in cart_items
        ]
        
        if cart_items:
            return jsonify({
            'status':'success',
            'message':'Cart items fetched successfully',
            'data_count': len(cart_items),
            'items': cart_items
        }), 200
        else:
            return jsonify({
            'status':'failed',
            'message':f'No cart found for this User ({user_id})'
        }), 400
        
    # UPDATE Cart Method
    elif request.method == 'PUT':
        cart_id = ObjectId(id)
        data = request.get_json()
        
        try:
            validate(data, cartSchema)
        except ValidationError as e:
            return jsonify({"Invalid Input":e.message})
        
        result = mongo.db.carts.update_one(
            {'_id': ObjectId(id)},
            { '$set': {
                "userId": data["userId"],
                "pdtId": ObjectId(data["pdtId"]),
                "quantity": data["quantity"],
                "price": data["price"],
                "total": data["total"]
            }
        }, upsert=False)
        
        if result.matched_count == 0:
            return jsonify({'status': "error",
                            'message': "Cart not found"}), 404
        else: 
            if result.modified_count == 1:
                document = mongo.db.carts.find_one({'_id': ObjectId(id)})
                
                document['_id'] = str(document['_id'])
                document['pdtId'] = str(document['pdtId'])
                
                return jsonify({'status': "success",
                                'message': "Cart updated successfully",
                                'data': document}), 200
            else:
                return jsonify({
                    'status': "success",
                    'message': "The cart remains unchanged without any updates"}), 200
                
    
    # DELETE Cart Method
    elif request.method == 'DELETE':
        cart_id = ObjectId(id)
        
        try:
            result = mongo.db.carts.delete_one({'_id': cart_id})
        except PyMongoError as e:
            return jsonify({'error': e.message})
            
        if result.deleted_count:
            return jsonify({"message": "Cart deleted successfully"}), 200
        else:
            return jsonify({"message": "Cart not found"}), 404
        
    
    else:
        return 405