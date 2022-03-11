from flask_restx import Resource, reqparse, Namespace
from flask import jsonify, make_response, current_app
import sys
import threading
from flask_jwt_extended import jwt_required
sys.path.append("..")
from init import mail, db
# from app import app
from templates.E_content import mail_content


ns = Namespace("email", description='Api auto send email')
parser = reqparse.RequestParser()
parser.add_argument('email', type=str)
parser.add_argument('require_type', type=str)
parser.add_argument('id', type=str)
parser.add_argument('day', type=str)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(e_msg):
    app = current_app._get_current_object()
    thr = threading.Thread(target=send_async_email, args=[app, e_msg])
    thr.start()
    # mail.send(e_msg)


def property_delete_notification(email, tenant, manager_name):
    e_msg = mail_content.property_delete(email, tenant, manager_name)
    send_email(e_msg)


def manager_request(day, p_id):
    """
    manager sending emails to initial inspections with multiple tenants
    :param day:
    :param p_id: [str] property id join with |||
    :return:
    """
    if day and p_id:
        t_name, t_email, m_name = db.get_email_detail(p_id)
        m_name = m_name.strip("\n")
        for email, name in zip(t_email, t_name):
            email = email.strip("\n")
            name = name.strip("\n")
            e_msg = mail_content.manager_initial(email, name, m_name, day)
            send_email(e_msg)


def manager_notify(m_id, calendar_file):
    """
    manager sending emails to initial inspections with multiple tenants
    :param calendar_file: calender file name
    :param day:
    :param m_id: [str] manager id
    :return:
    """
    if m_id:
        u_info = db.get_user_info("manager", m_id)
        email = u_info["email"]
        name = u_info["name"]
        email = email.strip("\n")
        name = name.strip("\n")
        e_msg = mail_content.manager_reminder(email, name)
        app = current_app._get_current_object()
        with app.open_resource(calendar_file) as fp:
            e_msg.attach("plan.ics", "text/calendar", fp.read())
        send_email(e_msg)


def te_reject(email, t_name, m_name, day, new_plan):
    if new_plan:
        sentence = "We have arranged an new plan for you which shows as the attachment."
        e_msg = mail_content.t_reject(email, t_name, m_name, day, sentence)
        print(new_plan)
        app = current_app._get_current_object()
        with app.open_resource(new_plan) as fp:
            e_msg.attach("plan.ics", "text/calendar", fp.read())
        send_email(e_msg)
    else:
        sentence = "Currently, you do not have any inspection plan in {}".format(day)
        e_msg = mail_content.t_reject(email, t_name, m_name, day, sentence)
        send_email(e_msg)


@ns.route('/Validation', methods=["POST"])
@ns.param('email', 'Valid email address.', require=True, example='kadawit657@smuvaj.com')
@ns.param('require_type', "Specific the usage of email. 'c' -> create account; 'r' -> reset "
          "password; 'e' -> change email address", require=True, example="c")
class verification_email(Resource):
    @ns.response(200, 'OK')
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'User Not Found')
    @ns.doc(description=" Verify user email when creating account")
    def post(self):
        try:
            e_msg = None
            verdi_code = None
            args = parser.parse_args()
            user_email = args.get('email')
            require_type = args.get("require_type")
            if require_type == "c":
                e_msg, verdi_code = mail_content.create_account(user_email)
            elif require_type == "r":
                e_msg, verdi_code = mail_content.password_change(user_email)
            elif require_type == "e":
                e_msg, verdi_code = mail_content.email_change(user_email)
            if e_msg is not None and verdi_code is not None:
                send_email(e_msg)
                print(verdi_code)
                msg = {"msg": "successful", "v_code": "{}".format(verdi_code)}
                return make_response(jsonify(msg), 200)
            else:
                ns.abort(400, "Email send failed")
        except ValueError:
            msg = {"msg": "Email send failed due to value error."}
            return make_response(jsonify(msg), 400)


@ns.route('/t_inspection', methods=["POST"])
@ns.param('id', 'Tenant user id', require=True)
@ns.param('day', "the time of inspection", require=True)
class tenant_request(Resource):
    @ns.response(200, 'OK')
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'User Not Found')
    @ns.doc(description=" Verify user email when creating account")
    @jwt_required()
    def post(self):
        try:
            args = parser.parse_args()
            day = args.get("day")
            uid = args.get('id')
            if day and uid:
                role = "tenant"
                user_info = db.get_user_info(role, uid)
                # tenant sending a email to initial an inspection to manager
                email = user_info["m_email"].strip("\n")
                e_msg = mail_content.tenant_initial(email, user_info["m_user_name"],
                                                    user_info["name"], day)
                send_email(e_msg)
                msg = {"msg": "successful"}
                return make_response(jsonify(msg), 200)
            else:
                ns.abort(400, "Email send failed, u_id or day missing")
        except ValueError:
            msg = {"msg": "Email send failed due to value error."}
            return make_response(jsonify(msg), 400)
