from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user
from flask_restx import Resource, reqparse, fields, Namespace
from flask import jsonify, make_response
import sys

sys.path.append("..")
from init import db

ns = Namespace("user", description='Api for user profile update')

parser = reqparse.RequestParser()
parser.add_argument('user_role', location='json', type=str)
parser.add_argument('new_password', location='json', type=str)
parser.add_argument('old_password', location='json', type=str)
parser.add_argument('new_email', location='json', type=str)
parser.add_argument('user_name', location='json', type=str)
parser.add_argument('phone', location='json', type=str)
parser.add_argument('avatar', location='json', type=str)
parser.add_argument('mode', location='json', type=str)

addressModel = ns.model('location_info ', {
    '1': fields.String(),
    '2': fields.String(),
    '3': fields.String()
})


# updating info for both manager & tenant
@ns.route('/user_password/<uid>', methods=["PATCH"])
class user_password(Resource):
    @ns.param('user_role', description='User is "manager" or "tenant"', required=True, example='manager')
    @ns.param('new_password', required=True, example='0231awE.')
    @ns.param('old_password', required=True)
    @ns.response(200, 'OK')
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'User Not Found')
    @ns.doc(description=" Update User password based on user type")
    @jwt_required()
    def patch(self, uid):
        args = parser.parse_args()
        user_role = args.get('user_role')
        new_password = args.get('new_password')
        mode = args.get('mode')
        user_id = int(uid)
        jwt_user = get_jwt_identity()
        if user_role[0] != jwt_user[0] or uid != jwt_user[1:]:
            return make_response(jsonify({'msg': "Authorization failed."}), 401)
        old_password = ''
        if mode == 'change':
            old_password = args.get('old_password')
            if not db.user_password_check(user_role, old_password):
                msg = {"msg": "User old password incorrect"}
                return make_response(jsonify(msg), 400)
        update_info = {"new_password": new_password, "old_password": old_password}
        try:
            if db.user_db_update(update_info, user_role, user_id):
                msg = {"msg": "Password update successful"}
                return make_response(jsonify(msg), 200)
            else:
                ns.abort(404, "user {} do not exist".format(user_id))
        except ValueError:
            ns.abort(404, "user password update failed")


@ns.route('/user_email/<uid>', methods=["PATCH", "POST"])
class user_email(Resource):
    @ns.param('user_role', description='User is "manager" or "tenant"', required=True, example='manager')
    @ns.param('new_email', required=True, example='example@gmail.com')
    @ns.response(200, 'OK')
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'User Not Found')
    @ns.doc(description=" Update User email based on user type")
    @jwt_required()
    def patch(self, uid):
        args = parser.parse_args()
        user_role = args.get('user_role')
        new_email = args.get('new_email')
        update_info = {"new_email": new_email}
        user_id = int(uid)
        jwt_user = get_jwt_identity()
        if user_role[0] != jwt_user[0] or uid != jwt_user[1:]:
            return make_response(jsonify({'msg': "Authorization failed."}), 401)
        try:
            if db.user_db_update(update_info, user_role, user_id):
                msg = {"msg": "Email update successful"}
                return make_response(jsonify(msg), 200)
            else:
                ns.abort(404, "user {} do not exist".format(user_id))
        except ValueError:
            ns.abort(404, "user email update failed")


@ns.route('/user_default/<uid>', methods=["PATCH", "POST"])
class user_default(Resource):
    @ns.param('user_role', description='User is "manager" or "tenant"', required=True)
    @ns.param('user_name', required=True, example="Aesz_1")
    @ns.param('phone', required=True, example="0412345678")
    @ns.response(200, 'OK')
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'User Not Found')
    @ns.doc(description=" Update User name & phone based on user type")
    @jwt_required()
    def patch(self, uid):
        args = parser.parse_args()
        user_role = args.get('user_role')
        jwt_user = get_jwt_identity()
        if user_role[0] != jwt_user[0] or uid != jwt_user[1:]:
            return make_response(jsonify({'msg': "Authorization failed."}), 401)
        user_name = args.get('user_name')
        phone = args.get('phone')
        avatar = args.get('avatar')
        if avatar != '':
            f = open(f"./files/avatars/{user_role}{uid}", 'w')
            f.write(avatar)
            f.close()
        update_info = {"user_name": user_name, "phone": phone}
        user_id = int(uid)
        try:
            if db.user_db_update(update_info, user_role, user_id):
                msg = {"msg": "User name & phone update successful"}
                return make_response(jsonify(msg), 200)
            else:
                ns.abort(404, "user {} do not exist".format(user_id))
        except ValueError:
            ns.abort(404, "User name & phone update failed")


#
@ns.route('/user_address/<uid>', methods=["POST"])
class user_address(Resource):
    @ns.param('user_role', description='User is "manager" or "tenant"', required=True)
    @ns.expect(addressModel, validate=True)
    @ns.response(200, 'OK')
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'User Not Found')
    @ns.doc(description=" Update manager's prefer start location(key = 1,2,3) & tenant's living address(key = 1)")
    @jwt_required()
    def post(self, uid):
        args = parser.parse_args()
        user_role = args.get('user_role')
        address = request.json
        user_id = int(uid)
        jwt_user = get_jwt_identity()
        if user_role[0] != jwt_user[0] or uid != jwt_user[1:]:
            return make_response(jsonify({'msg': "Authorization failed."}), 401)
        try:
            if user_role == "manager":
                # maximum 3 location in address
                if db.user_db_update(address, user_role, user_id):
                    msg = {"msg": "manager's prefer start location update successful"}
                    return make_response(jsonify(msg), 200)
                else:
                    ns.abort(404, "user {} do not exist".format(user_id))
            elif user_role == "tenant":
                address = address["1"]
                response = db.tenant_address_update(address, user_role, user_id)
                if response == 1:
                    ns.abort(404, "address do not exist")
                elif response == 2:
                    ns.abort(404, "user {} do not exist".format(user_id))
                elif response == 3:
                    msg = {"msg": "tenant's address update successful"}
                    return make_response(jsonify(msg), 200)

        except ValueError:
            ns.abort(404, "User name & phone update failed")


# return basic user info
@ns.route('/getuser/<role>/<uid>')
class UserInfo(Resource):
    @staticmethod
    @jwt_required()
    def get(role, uid):
        msg = db.get_user_info(role, uid)
        if msg == 2:
            msg = {"msg": "The user with Identifier {} doesn't exist".format(uid)}
            return make_response(jsonify(msg), 404)
        if role == 'manager':
            property_info = None
            propertyAddress = db.get_property_info(uid)
            if propertyAddress:
                property_info = {propertyAddress[i]["p_id"]: {"loc": dict(lat=propertyAddress[i]['latitude'],
                                                                          lng=propertyAddress[i]['longitude']),
                                                              'formatted_address': propertyAddress[i]['address'],
                                                              'pid': propertyAddress[i]['p_id']}
                                 for i in propertyAddress}
            msg['properties'] = property_info
        user = get_jwt_identity()
        if role[0] != user[0] or uid != user[1:]:
            return make_response(jsonify({'msg': "Authorization failed."}), 401)
        return make_response(jsonify(msg), 200)
