from flask_restx import Resource, Namespace, reqparse, fields
from flask import jsonify, make_response
from flask import request
import json
import time
import sys
from flask_jwt_extended import jwt_required

sys.path.append("..")
from init import db

ns = Namespace("Report", description='Report manager')


# Report model-> used to insert report
Report_model = ns.model('Report', {
    "p_id": fields.Integer(min=1),
    "repo_content": fields.String,
    "repo_title": fields.String,
    "repo_date": fields.String,
    "last_visit_time": fields.String
})
parser = reqparse.RequestParser()
parser.add_argument('m_id', location='args', type=int)
parser.add_argument('repo_id', location='args', type=int)


@ns.route('/unreported_property/', methods=["GET"])
class repo(Resource):
    @ns.doc(description=" select inspected report")
    @ns.param('m_id', description='Manager id', required=True)
    @ns.response(200, 'OK')
    @ns.response(200, 'OK')
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'Manager Not Found')
    @jwt_required()
    def get(self):
        args = parser.parse_args()
        mid = args.get('m_id')
        property_info = db.get_property_info(mid)
        if not property_info:
            msg = {"msg": "The manager with Identifier {} doesn't exist or doesn't have any property".format(mid)}
            return make_response(jsonify(msg), 404)
        i_plan = db.opera.select_data(f'db_manager', 'inspection_plan', f'm_id = {mid}')[0]
        if not i_plan:
            msg = {"msg": "The manager with Identifier {} doesn't have unreported property".format(mid)}
            return make_response(jsonify(msg), 404)
        current_plan = json.loads(i_plan)
        c_time = time.time()
        time_stp = float(time.mktime(time.strptime(current_plan["day"], "%Y-%m-%d %H:%M:%S")))
        if c_time < time_stp:
            msg = {"msg": "The manager with Identifier {} doesn't have unreported property".format(mid)}
            return make_response(jsonify(msg), 404)
        else:
            p_repo = {}
            p_list = current_plan["p_list"].split("|||")
            for key in property_info.keys():
                if str(property_info[key]["p_id"]) in p_list:
                    p_repo[key] = property_info[key]
                    property_info[key]['last_visit'] = current_plan["day"]
                    property_id = property_info[key]['p_id']
                    last_visit = current_plan["day"]
                    db.opera.update_db(property_info[key]["p_id"], 'p_id', 'db_property',
                                     ["last_visit"], [last_visit])
                    result = db.property_db_update(property_info[key], property_id)
                    if result == 4:
                        continue
                    elif result == 2:
                        msg = {'msg': "The property with Identifier {} doesn't exist".format(property_id)}
                        return make_response(jsonify(msg), 404)
                    elif result == 3:
                        msg = {'msg': "The property with address {} has already existed in the database".format(
                            property_info['address'])}
                        return make_response(jsonify(msg), 400)
            msg = {'msg': 'successfully', 'p_info': p_repo}
            return make_response(jsonify(msg), 200)


@ns.route('/repo_manage/', methods=["POST", "DELETE"])
class repo(Resource):
    @ns.param('repo_id', description='Id of Report need be delete', required=True)
    @ns.response(200, 'OK')
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'Report Not Found')
    @ns.doc(description=" Deleting a Report ")
    @jwt_required()
    def delete(self):
        args = parser.parse_args()
        id = args.get('repo_id')
        table = "db_repo"
        col = "repo_id"
        if not db.data_in_db(table, col, id):
            ns.abort(404, "Report with Identifier {} doesn't exist".format(id))
        db.delete_report(id)
        msg = {"message": "The Report with Identifier {} was removed from the database!".format(id)}
        return make_response(jsonify(msg), 200)

    @ns.doc(description=" Adding a Report ")
    @ns.expect(Report_model, validate=True)
    @ns.response(200, 'OK')
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'Property Not Found')
    @jwt_required()
    def post(self):
        repo_info = request.json
        p_id = repo_info['p_id']
        repo_info["repo_content"] = repo_info["repo_content"].replace("'", "''")
        repo_info["repo_title"] = repo_info["repo_title"].replace("'", "''")
        result = db.add_repo(repo_info, p_id)
        if result == 1:
            msg = "The property with Identifier {} doesn't exist".format(p_id)
            return make_response(jsonify(msg), 404)
        elif result == 2:
            mid = db.opera.select_data(f'db_property', 'm_id', f'p_id = {p_id}')[0]
            i_plan = db.opera.select_data(f'db_manager', 'inspection_plan', f'm_id = {mid}')[0]
            current_plan = json.loads(i_plan)
            current_plan["p_list"] = current_plan["p_list"].split("|||")
            current_plan["p_list"].remove(str(p_id))
            if len(current_plan["p_list"]) >= 1:
                current_plan["p_list"] = "|||".join(current_plan["p_list"])
                # db.store_plan(mid, "null", current_plan["day"], current_plan["p_list"], current_plan["destinations"],
                #               current_plan["duration"], "")
                db.store_plan(mid, current_plan["plan"], current_plan["day"], current_plan["p_list"],
                              current_plan["destinations"],
                              current_plan["duration"], current_plan["inPlan"])
            else:
                db.opera.update_db(mid, "m_id", "db_manager", ["inspection_plan"], ["null"])
            msg = {"message": "The report with identifier {} was added into the database!".format(p_id)}
            return make_response(jsonify(msg), 200)


@ns.route('/repo_overview/', methods=["GET"])
class get_all_Repo(Resource):
    @ns.param('m_id', description='Manager id', required=True)
    @ns.response(200, 'OK')
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'property Not Found')
    @ns.doc(description=" Getting info of Reports ")
    @jwt_required()
    def get(self):
        args = parser.parse_args()
        mid = args.get('m_id')
        repo_info = db.get_report_info(mid)
        if repo_info == 1:
            msg = {"msg": "The manager with Identifier {} doesn't have any property".format(mid)}
            return make_response(jsonify(msg), 404)
        if not repo_info:
            msg = {"msg": "The manager with Identifier {} doesn't have any report record".format(mid)}
            return make_response(jsonify(msg), 404)
        # print(property_info)
        msg = {'msg': 'successfully', 'repo_info': repo_info}
        return make_response(jsonify(msg), 200)


@ns.route('/report_modify/', methods=["PATCH"])
class modifyRepo(Resource):
    @ns.response(200, 'OK')
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'property Not Found')
    @ns.doc(description=" Getting info of properties ")
    @ns.param('repo_id', description='Id of Report need be modified', required=True)
    @ns.expect(Report_model, validate=True)
    @jwt_required()
    def patch(self):
        repo_info = request.json
        args = parser.parse_args()
        repo_id = args.get('repo_id')
        if "repo_content" in repo_info.keys():
            repo_info["repo_content"] = repo_info["repo_content"].replace("'", "''")
        if "repo_title" in repo_info.keys():
            repo_info["repo_title"] = repo_info["repo_title"].replace("'", "''")
        # col = ["p_id", "repo_content", "repo_title", "repo_date", "last_visit_time"]
        result = db.report_update(repo_info, repo_id)
        if result == 3:
            msg = {'msg': "report update successful"}
            return make_response(jsonify(msg), 200)
        elif result == 1:
            msg = {'msg': "The property with identifier {} doesn't exist".format(repo_info["p_id"])}
            return make_response(jsonify(msg), 404)
        elif result == 2:
            msg = {'msg': "The report with identifier {} doesn't exist".format(repo_id)}
            return make_response(jsonify(msg), 404)
