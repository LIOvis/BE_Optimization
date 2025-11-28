from flask import request, jsonify

from models.warranty import Warranties, warranties_schema, warranty_schema
from util.reflection import populate_object
from models.product import Products
from db import db

def add_warranty():
    post_data = request.form if request.form else request.json

    new_warranty = Warranties.new_warranty_obj()

    populate_object(new_warranty, post_data)

    try:
        db.session.add(new_warranty)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to add warranty"}), 400

    return jsonify({"message": "warranty added", "result": warranty_schema.dump(new_warranty)}), 201


def get_all_warranties():
    query = db.session.query(Warranties).all()


    return jsonify({"message": "warranties found", "results": warranties_schema.dump(query)}), 200


def get_warranty_by_id(warranty_id):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not query:
        return jsonify({"message": "warranty not found"}), 404
    

    return jsonify({"message": "warranty found", "result": warranty_schema.dump(query)}), 200


def update_warranty_by_id(warranty_id):
    post_data = request.form if request.form else request.json
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not query:
        return jsonify({"message": "warranty not found"}), 404 

    try:
        populate_object(query, post_data)
        db.session.commit()
    
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update warranty"}), 400

    return jsonify({"message": "warranty updated", "result": warranty_schema.dump(query)}), 200


def delete_warranty_by_id(warranty_id):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not query:
        return jsonify({"message": "warranty not found"}), 404
    
    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete warranty"}), 400
    
    return jsonify({"message": "warranty deleted"}), 200