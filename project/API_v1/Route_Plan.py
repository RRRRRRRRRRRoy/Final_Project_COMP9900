from flask_restx import Namespace, Resource, reqparse, fields
from flask import jsonify, make_response, request
import json
import time
import urllib.request as req
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz
import re
from time import strptime
from web_email import manager_request, te_reject, manager_notify
import sys
from flask_jwt_extended import jwt_required
sys.path.append("..")
from init import db

ns = Namespace('plan')

Plan_model = ns.model('plan', {
    "id": fields.Integer(min=1),
    "day": fields.String,
    "plan": fields.String,
    "p_list": fields.String,
    "duration": fields.String,
    "destinations": fields.String
})
parser = reqparse.RequestParser()
parser.add_argument("id")


def route_plan(addr_list, plan_time, destinations):
    """
    :param plan_time:
    :param destinations:
    :param addr_list:
    :return:
    """
    destinations = destinations.replace(" ", "%20")
    destinations = destinations.split("|||")
    head = 'https://maps.googleapis.com/maps/api/directions/json?'
    origin = 'origin=%s' % (destinations[0])
    destination = 'destination=%s' % (destinations[1])
    key = 'key=AIzaSyCyM4_46_2i9qeFS6XP9gzTg32RCLKkLZk'
    middle = ''
    for i in addr_list:
        temp_addr = i.replace(" ", "%20")
        middle += '|' + temp_addr

    waypoints = 'waypoints=optimize:true%s' % middle
    mode = 'mode=driving'
    time_stp = int(time.mktime(time.strptime(plan_time, "%Y-%m-%d %H:%M:%S")))
    departure_time = 'departure_time=%s' % (time_stp)

    new_url = head + '&' + origin + '&' + destination + '&' + waypoints + '&' + mode + '&' + departure_time + '&' + key

    # sample_address1 = Elizabeth%20St,%20Sydney%20NSW%202000
    # sample_address2 = Level%205/108%20Market%20St,%20Sydney%20NSW%202000
    ''' new_url = "https://maps.googleapis.com/maps/api/directions/json?origin=39%20Rhodes%20St,
     %20Hillsdale%20NSW%202036&destination=553%20Bunnerong%20Rd,%20Matraville%20NSW%202036&waypoints=optimize:true
     |Level%205/108%20Market%20St,%20Sydney%20NSW%202000|Bennelong%20Point,%20Sydney%20NSW%202000|College%20Rd,%20Kensington%20NSW
     |Elizabeth%20St,%20Sydney%20NSW%202000%202052&key=AIzaSyCyM4_46_2i9qeFS6XP9gzTg32RCLKkLZk" '''
    # sample_url = "https://maps.googleapis.com/maps/api/directions/json?origin=Brooklyn&destination=Queens&mode=transit&key=AIzaSyCyM4_46_2i9qeFS6XP9gzTg32RCLKkLZk"

    resource = req.Request(new_url)
    response = json.loads(req.urlopen(resource).read())
    response["request"] = {'travelMode': "DRIVING"}
    response['routes'][0]['bounds'] = {
        'north': response['routes'][0]['bounds']['northeast']['lat'],
        'east': response['routes'][0]['bounds']['northeast']['lng'],
        'south': response['routes'][0]['bounds']['southwest']['lat'],
        'west': response['routes'][0]['bounds']['southwest']['lng']
    }
    return response


def begin_time_update(b_time, duration, tz):
    time_stp = float(time.mktime(strptime(b_time, "%Y-%m-%d %H:%M:%S")))
    time_stp = time_stp + duration
    temp = pytz.datetime.datetime.fromtimestamp(time_stp, tz)
    b_time = temp.strftime("%Y-%m-%d %H:%M:%S")
    return b_time


def begin_time_reform(b_time, tz):
    b_time = b_time.split(" ")
    begin_day = b_time[0].split("-")
    begin_hour = b_time[1].split(":")
    return datetime(int(begin_day[0]), int(begin_day[1]), int(begin_day[2]), int(begin_hour[0]),
                               int(begin_hour[1]), int(begin_hour[2]), tzinfo=tz)


def get_calender_info(b_time, response, event_duration):
    tz = pytz.timezone("Australia/Sydney")
    activity = []
    plan = response["routes"][0]
    leg = plan["legs"]
    place_dict = {}
    for place in leg[:-1]:
        # driving event
        place_dict["even_1"] = "Driving to inspect location"
        place_dict["begin_1"] = begin_time_reform(b_time, tz)
        place_dict["start_location"] = place["start_address"]
        duration = place["duration"]["value"]
        place_dict["duration_1"] = timedelta(seconds=duration)
        b_time = begin_time_update(b_time, duration, tz)
        # inspection event
        place_dict["location"] = place["end_address"]
        place_dict["even_2"] = "Inspection"
        place_dict["duration_2"] = timedelta(seconds=event_duration)
        place_dict["begin_2"] = begin_time_reform(b_time, tz)
        b_time = begin_time_update(b_time, event_duration, tz)
        activity.append(place_dict)
        place_dict = {}
    place_dict["even_1"] = "Driving to end location"
    place_dict["begin_1"] = begin_time_reform(b_time, tz)
    place_dict["start_location"] = leg[-1]["start_address"]
    duration = leg[-1]["duration"]["value"]
    place_dict["duration_1"] = timedelta(seconds=duration)
    activity.append(place_dict)
    return activity


def event_detail(e, c, name, begin_t, duration, location):
    e.name = name
    e.begin = begin_t
    e.duration = duration
    e.location = location
    c.events.add(e)
    return c


def calendar_generator(b_time, response, event_duration):
    file = "./files/calendar/new.ics"
    event_duration = int(event_duration) * 60
    detail = get_calender_info(b_time, response, event_duration)
    c = Calendar()
    e = Event()
    with open(file, 'w') as calender_file:
        for info in detail[:-1]:
            # driving event
            name = info["even_1"]
            begin_t = info["begin_1"]
            location = info["start_location"]
            duration = info["duration_1"]
            event_detail(e, c, name, begin_t, duration, location)
            calender_file.writelines(c)
            # inspection event
            location = info["location"]
            name = info["even_2"]
            duration = info["duration_2"]
            begin_t = info["begin_2"]
            event_detail(e, c, name, begin_t, duration, location)
            calender_file.writelines(c)
        name = detail[-1]["even_1"]
        begin_t = detail[-1]["begin_1"]
        location = detail[-1]["start_location"]
        duration = detail[-1]["duration_1"]
        event_detail(e, c, name, begin_t, duration, location)
        calender_file.writelines(c)
    calender_file.close()
    return file


@ns.route('/store', methods=['POST'])
class save_plan(Resource):
    @ns.expect(Plan_model, validate=True)
    @ns.doc(description=" Saving inspection plan ")
    @ns.response(200, 'OK')
    @ns.response(400, 'Invalid input')
    @ns.response(404, 'Not exist')
    @jwt_required()
    def post(self):
        try:
            repo_info = request.json
            m_id = repo_info['id']
            plan = repo_info['plan']
            day = repo_info['day']
            p_list = repo_info['p_list']
            destinations = repo_info['destinations']
            event_duration = repo_info["duration"]
            in_plan = repo_info["inPlan"]
            response = db.store_plan(m_id, plan, day, p_list, destinations, event_duration, in_plan)
            if response == 1:
                ns.abort(404, "manager with identification {} do not exist".format(m_id))
            elif response == 2:
                rout = json.loads(plan)
                calendar_file = calendar_generator(day, rout, event_duration)
                manager_request(day, p_list)
                manager_notify(m_id, calendar_file)
                msg = {"msg": "Store successfully"}
                return make_response(jsonify(msg), 200)

        except ValueError:
            ns.abort(400, "The argument incorrect.")


@ns.route('/tenant_reject', methods=['POST'])
class tenant_reject(Resource):
    @ns.param('id', description='The user id of the tenant', required=True)
    @ns.response(200, 'OK')
    @ns.response(400, 'Invalid input')
    @ns.response(404, 'Not exist')
    @jwt_required()
    def post(self):
        args = parser.parse_args()
        t_id = args.get('id')
        response = db.tenant_inspection_check(t_id)
        if response == 1:
            ns.abort(404, "tenant with identification {} do not exist".format(t_id))
        if response == 2:
            ns.abort(404, "tenant with identification {} do not have linked manager".format(t_id))
        if response == 3:
            ns.abort(404, "tenant with identification {} do not have linked property".format(t_id))
        if response == 4:
            ns.abort(404, "tenant with identification {} do not have inspection plan".format(t_id))
        if len(response["p_list"]) >= 1:
            new_plan = route_plan(response["address"], response["day"], response["destinations"])
            calendar_file = calendar_generator(response["day"], new_plan, response["duration"])
            new_plan = json.dumps(new_plan)
            new_plan = new_plan.replace("'", "''")
            response["address"] = "|||".join(response["address"])
            response["p_list"] = "|||".join(response["p_list"])
            db.store_plan(response["m_id"], new_plan, response["day"], response["p_list"], response["destinations"],
                          response["duration"], response["in_plan"])
            db.opera.update_db(t_id, "t_id", "db_tenant", ["inspection_flag"], ["null"])
            te_reject(response["m_email"], response["t_name"], response["m_name"], response["day"], calendar_file)
        else:
            db.opera.update_db(t_id, "t_id", "db_tenant", ["inspection_flag"], ["null"])
            db.opera.update_db(response["m_id"], "m_id", "db_manager", ["inspection_plan"], ["null"])
            te_reject(response["m_email"], response["t_name"], response["m_name"], response["day"], False)
        msg = {"msg": "Store successfully"}
        return make_response(jsonify(msg), 200)


@ns.route('/show_plan/<id>', methods=['GET'])
class show_plan(Resource):
    @ns.doc(description=" Saving inspection plan ")
    @ns.response(200, 'OK')
    @ns.response(400, 'Invalid input')
    @ns.response(404, 'Not exist')
    @jwt_required()
    def get(self, id):
        msg = db.get_user_info("manager", id)
        if msg == 2:
            msg = {"msg": "The user with Identifier {} doesn't exist".format(id)}
            return make_response(jsonify(msg), 404)
        reponse = msg["inspection_plan"]
        if not reponse or reponse == "null":
            msg = {"msg": "The user with Identifier {} doesn't have any plan".format(id)}
            return make_response(jsonify(msg), 404)
        else:

            rout = json.loads(reponse)
            plan = {"result": rout["plan"], "duration": rout["duration"]}
        return make_response(jsonify(plan), 200)
