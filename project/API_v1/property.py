from flask_restx import Resource, Namespace, reqparse, fields
from flask import jsonify, make_response
from flask import request
import sys
import json
from copy import deepcopy
import os
from web_email import property_delete_notification
from flask_jwt_extended import jwt_required
sys.path.append("..")
from init import db

ns = Namespace("property", description='Property manager')

# Property model
property_model = ns.model('Property', {
    "manager_id": fields.Integer(min=1),
    "tenant_information": fields.String,
    "address": fields.String,
    "postcode": fields.String,
    "latitude": fields.String,
    "longitude": fields.String,
    "last_visit": fields.Date,
    "rent_start": fields.Date,
    "rent_end": fields.Date
})

propertyAddModel = ns.model('propertyAdd', {
    "message": fields.String(example='successfully'),
    "p_id": fields.Integer(example=12312312321),
})

propertyInfoModel = ns.model('PropertyInfo', {
    "property_id": fields.Integer(min=1),
    "tenant_information": fields.String,
    "address": fields.String,
    "postcode": fields.String,
    "latitude": fields.String,
    "longitude": fields.String,
    "last_visit": fields.Date,
    "rent_start": fields.Date,
    "rent_end": fields.Date
})

info = ns.model('p_id', propertyInfoModel)
propertyGetModel = ns.model('propertyGet', {
    "message": fields.String(example='successfully'),
    "p_info": fields.Nested(info)
})


@ns.route('/Property_manage/', methods=["POST", "DELETE"])
class prop(Resource):
    @ns.param('id', description='Id of property need be delete', required=True)
    @ns.response(200, 'OK')
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'property Not Found')
    @ns.doc(description=" Deleting a property ")
    @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', type=int)
        args = parser.parse_args()
        id = args.get('id')
        table = "db_property"
        col = "p_id"
        if not db.data_in_db(table, col, id):
            ns.abort(404, "Property with Identifier {} doesn't exist".format(id))
        if os.path.exists(f'./files/properties/p{id}'):
            os.remove(f'./files/properties/p{id}')
        m_id, t_info = db.delete_property(id)
        if t_info:
            m_info = db.get_user_info("manager", m_id)
            m_name = m_info["name"]
            for i in t_info:
                property_delete_notification(i[1], i[0], m_name)
        msg = {"message": "The Property with Identifier {} was removed from the database!".format(id)}
        return make_response(jsonify(msg), 200)

    @ns.doc(description=" Add a property ")
    @ns.expect(property_model, validate=True)
    @ns.response(200, 'OK', model=propertyAddModel)
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'Not Found')
    @jwt_required()
    def post(self):
        property_info = deepcopy(request.json)
        mid = property_info['manager_id']
        col = ['m_id', 't_info', 'address', 'postcode', 'latitude', 'longitude', 'last_visit', 'rent_start', 'rent_end']
        property_info = dict(zip(col, property_info.values()))
        result = db.add_property(property_info, mid)
        if result == 2:
            msg = "The manager with Identifier {} doesn't exist".format(mid)
            return make_response(jsonify(msg), 404)
        elif result == 3:
            msg = "The property with address {} has already existed in the database".format(property_info['address'])
            return make_response(jsonify(msg), 400)
        elif result == 4:
            pid = db.property_id_select('db_property', property_info['address'])
            img = json.dumps(request.json['property_Image'])
            if img:
                f = open(f'./files/properties/p{pid}', 'w')
                f.write(img)
                f.close()
            msg = {"message": "The Property managed by manager with  Identifier {} was added into the database!".format(
                mid),
                "property_id": pid
            }
            return make_response(jsonify(msg), 200)


@ns.route('/Property_view/', methods=["GET"])
class getAllPro(Resource):
    @ns.param('m_id', description='Id of manager these properties belong to', required=True)
    @ns.response(200, 'OK', model=propertyGetModel)
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'property Not Found')
    @ns.doc(description=" Getting info of properties ")
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('m_id', location='args', type=int)
        args = parser.parse_args()
        mid = args.get('m_id')
        property_info = db.get_property_info(mid)
        if not property_info:
            msg = {"msg": "The manager with Identifier {} doesn't exist".format(mid)}
            return make_response(jsonify(msg), 404)
        msg = {'msg': 'successfully',
               'p_info': property_info}
        return make_response(jsonify(msg), 200)


@ns.route('/Property_modify/', methods=["PATCH"])
class modifyPro(Resource):
    @ns.response(200, 'OK', model=propertyGetModel)
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'property Not Found')
    @ns.doc(description=" Getting info of properties ")
    @ns.expect(propertyInfoModel, validate=True)
    @jwt_required()
    def patch(self):
        property_info = request.json
        property_id = property_info['property_id']
        col = ['t_info', 'address', 'postcode', 'latitude', 'longitude', 'last_visit', 'rent_start', 'rent_end']
        value = [property_info["tenant_information"], property_info['address'], property_info['postcode'],
                 property_info['latitude'], property_info['longitude'], property_info['last_visit'],
                 property_info['rent_start'], property_info['rent_end']]
        property_info_1 = dict(zip(col, value))
        result = db.property_db_update(property_info_1, property_id)
        if result == 4:
            img = json.dumps(request.json['property_Image'])
            if img:
                f = open(f'./files/properties/p{property_id}', 'w')
                f.write(img)
                f.close()
            msg = {'msg': "Property update successful",
                   'p_info': property_info
                   }
            return make_response(jsonify(msg), 200)
        elif result == 2:
            msg = {'msg': "The property with Identifier {} doesn't exist".format(property_id)}
            return make_response(jsonify(msg), 404)
        elif result == 3:
            msg = {'msg': "The property with address {} has already existed in the database".format(
                property_info['address'])}
            return make_response(jsonify(msg), 400)


@ns.route('/getaddr/<mid>', methods=["GET"])
class GetAddress(Resource):
    @staticmethod
    @jwt_required()
    def get(mid):
        property_info = db.get_property_info(mid)
        if not property_info:
            msg = {"msg": "The manager with Identifier {} doesn't exist".format(mid)}
            return make_response(jsonify(msg), 404)
        property_info = {i: {"loc": {'lat': property_info[i]['latitude'], 'lng': property_info[i]['longitude']},
                             'formatted_address': property_info[i]['address'], 'pid': property_info[i]['p_id']}
                         for i in property_info}
        msg = {'msg': 'successfully',
               'p_info': property_info}
        print(msg)
        return make_response(jsonify(msg), 200)


@ns.route('/getprop/<pid>', methods=["GET"])
class GetProperty(Resource):
    @staticmethod
    @ns.response(200, 'OK', model=propertyGetModel)
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'property Not Found')
    @jwt_required()
    def get(pid):
        propertyInfo = db.opera.select_data('db_property', '*', f'p_id = {pid}')[0]
        propertyInfo.pop(1)
        propertyKey = ['p_id', 't_info', 'address', 'postcode', 'latitude', 'longitude', 'last_visit', 'rent_start',
                       'rent_end']
        propertyInfo = dict(zip(propertyKey, propertyInfo))
        try:
            f = open(f"./files/properties/p{pid}", 'r')
            images = f.read()
            f.close()
        except FileNotFoundError:
            images = ''
        propertyInfo['property_Image'] = images
        msg = {'msg': 'successfully',
               'p_info': propertyInfo}
        return make_response(jsonify(msg), 200)
