from flask_restx import (Namespace, Resource, reqparse, fields)
from flask import jsonify, make_response
from flask import request
import sys
sys.path.append("..")
from init import db
from flask_jwt_extended import create_access_token


ns = Namespace('auth', description='API for login, register, ...', path='/auth')


logInModel = ns.model('logIn', {
    'msg': fields.String(example='successfully'),
    'uid': fields.Integer(example=12312312321),
    # 'uname': fields.String(example='some user'),
    'token': fields.String(example='This is a token'),
    'avatar': fields.String(example='This is an avatar')
})

RegisterModel = ns.model('Register', {
    "role": fields.String,
    'email': fields.String,
    'password': fields.String,
    "username": fields.String,
    # "phone": fields.Integer(exmaple=400000000)
    "phone": fields.String
})

parser = reqparse.RequestParser()
parser.add_argument('role')
parser.add_argument('email')
parser.add_argument('password')
parser.add_argument('user_role', location='json', type=str)
parser.add_argument('new_password', location='json', type=str)
parser.add_argument('old_password', location='json', type=str)


@ns.route('/login', methods=['POST'])
class LogIn(Resource):
    @ns.param('role', description='The role of the user', required=True, example='manager')
    @ns.param('email',  required=True)
    @ns.param('password', required=True)
    @ns.response(200, 'OK', model=logInModel)
    @ns.response(400, 'Password does not match the account')
    @ns.response(404, 'Account does not exist')
    def post(self):
        args = parser.parse_args()
        user_role = args.get('role')
        password = args.get('password')
        email = args.get('email')
        if not db.user_email_exists(user_role, email):
            msg = {"msg": "Account does not exist"}
            return make_response(jsonify(msg), 404)
        user_id = db.valid_user(user_role, email, password)
        if user_id is None:
            msg = {"msg": "Password does not match the account"}
            return make_response(jsonify(msg), 400)
        else:
            try:
                f = open(f'./files/avatars/{user_role}{user_id}')
                avatar = f.read()
                f.close()
            except FileNotFoundError:
                avatar = ''
            token = create_access_token(identity=f"{user_role[0]}{user_id}")
            msg = {"msg": "Login successfully", "id": str(user_id), "avatar": avatar, "token": token}
            return make_response(jsonify(msg), 200)


@ns.route('/register', methods=['POST'])
class register(Resource):
    @ns.response(200, 'OK')
    @ns.response(400, 'Account already exists')
    @ns.expect(RegisterModel, validate=True)
    def post(self):
        users_info = request.json
        user_role = users_info["role"]
        email = users_info["email"]
        # if db.user_email_exists(user_role, email):
        #     return make_response(jsonify({"msg": "Account already exists"}), 400)
        # else:
        user_id = db.save_user_data(users_info, user_role)
        return make_response(jsonify({"msg": "Registered successful", "user_id": user_id}), 200)


@ns.route('/emailValid')
class EmailExist(Resource):
    @staticmethod
    def post():
        role = request.json['role']
        email = request.json['email']
        if db.user_email_exists(role, email):
            uid = db.user_id_select(f'db_{role}', f'{role[0]}_', email, f'{role[0]}_email')
            msg = f'{email} has been registered as a {role} account.'
            print(uid)
            return make_response(jsonify({'msg': msg, 'id': uid}), 400)
        else:
            return make_response(jsonify({'msg': 'ok'}), 200)


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
    def patch(self, uid):
        args = parser.parse_args()
        user_role = args.get('user_role')
        new_password = args.get('new_password')
        mode = args.get('mode')
        user_id = int(uid)
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


@ns.route('/logout')
class LogOut(Resource):
    @staticmethod
    def get():
        return make_response(jsonify({'msg': 'successfully'}), 200)
