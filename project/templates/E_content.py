from flask_mail import Message
import random
from flask import render_template
import time


class mail_content:

    time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @staticmethod
    def create_account(user_email):
        sentence = "Please verify your email to complete your registration in Rental_Inspection.com with the one-time " \
                   "code below:"
        verdi_code = random.randint(1000, 9999)
        msg = Message(subject='Verification for creating account',
                      recipients=[user_email],
                      body="Hello {} is the verification code "
                           "for creating your account".format(verdi_code),
                      html=render_template("./html_template/account_validation.html", head="Account creating",
                                           code=verdi_code, timestamp=time, sentence=sentence))
        return msg, verdi_code

    @staticmethod
    def email_change(user_email):
        sentence = "We have received a request to change your email address. Please verify your email with the one-time "\
                   "code below:"
        verdi_code = random.randint(1000, 9999)
        msg = Message(subject='Verification of change email',
                      recipients=[user_email],
                      body="Hello {} is the verification code "
                           "for changing your email address".format(verdi_code),
                      html=render_template("./html_template/account_validation.html", head="Email changing", code=verdi_code, timestamp=time,
                                           sentence=sentence))
        return msg, verdi_code

    @staticmethod
    def password_change(user_email):
        verdi_code = random.randint(1000, 9999)
        msg = Message(subject='Verification of reset password',
                      recipients=[user_email],
                      html=render_template("./html_template/retrieve_password.html", code=verdi_code, timestamp=time))
        return msg, verdi_code

    @staticmethod
    def tenant_initial(to_email, manager_name, tenant, day):
        msg = Message(subject='An inspection require from your tenant',
                      recipients=[to_email],
                      html=render_template("./html_template/tenant_request.html", manager_name=manager_name,
                                           tenant=tenant, day=day, timestamp=time))
        return msg

    @staticmethod
    def manager_initial(to_email, tenant, manager_name, day):
        msg = Message(subject='An inspection require from your manager',
                      recipients=[to_email],
                      html=render_template("./html_template/manager_request.html", manager_name=manager_name,
                                           tenant=tenant, day=day, timestamp=time))
        return msg

    @staticmethod
    def manager_reminder(to_email, manager_name):
        msg = Message(subject='An inspection plan notification',
                      recipients=[to_email],
                      html=render_template("./html_template/manager_reminder.html", manager_name=manager_name,
                                           timestamp=time))
        return msg

    @staticmethod
    def property_delete(to_email, tenant, manager_name):
        msg = Message(subject='Notification for data updating',
                      recipients=[to_email],
                      html=render_template("./html_template/property_delete.html", manager_name=manager_name,
                                           tenant=tenant, timestamp=time))
        return msg

    @staticmethod
    def t_reject(to_email, tenant, manager_name, day, sentence):
        msg = Message(subject='An rejection from your tenant',
                      recipients=[to_email],
                      html=render_template("./html_template/tenant_reject.html", manager_name=manager_name, tenant=tenant,
                                           timestamp=time, sentence=sentence, day=day))
        return msg