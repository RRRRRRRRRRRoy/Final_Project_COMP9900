import sqlite3
from db_config import *
import json
import time


class operation:
    def __init__(self):
        self.db_name = db_name
        self.db_init()

    def db_init(self):
        """
        Initiate database and tables
        """
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute(db_repo)
        conn.commit()
        cur.execute(db_property)
        conn.commit()
        cur.execute(db_manager)
        conn.commit()
        cur.execute(db_tenant)
        conn.commit()
        conn.close()

    def select_data(self, table, col, value):
        """
        SQL SELECT operation
        :param table:[str]  Name of table need be operate
        :param col:[str]   Attributes and their values eg. m_id, m_phone
        :param value:[str] Additional conditions eg. "m_id"=1
        :return:[list]  values selected from table
        """
        exist_value = []
        if value is None:
            com = "select {} from {}".format(col, table)
        else:
            com = "select {} from {} where {}".format(col, table, value)
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        reg = cursor.execute(com)
        for row in reg:
            if len(row) == 1:
                exist_value.append(row[0])
            else:
                exist_value.append(list(row))
        conn.close()
        return exist_value

    def insert_data(self, table, col, value):
        """
        SQL INSERT operation
        :param table:[str]  Name of table need be operate
        :param col:[str]   Attributes eg. m_id, m_phone
        :param value:[str] Attributes' values eg. "('{}','{}','{}','{}')"
        :return: None
        """
        com = "insert into {} ({}) values {} ".format(table, col, value)
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute(com)
        cur.close()
        conn.commit()
        conn.close()

    def delete_data(self, table, col, value):
        """
        SQL DELETE operation [delete single row]
        :param table:[str]  Name of table need be operate
        :param col:[str]   Attributes eg. m_id
        :param value:[str] Attributes' values eg. 1
        :return: None
        """
        com = "DELETE from {} where {} = {};".format(table, col, value)
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(com)
        conn.commit()
        conn.close()

    def update_db(self, attr, attr_name, table, col, value):
        """
        SQL UPDATE operation [update single attribute]
        :param attr_name:[str] Attribute used to locate row
        :param attr: [str] Attribute's values
        :param table:[str]  Name of table need be operate
        :param col:[list]   Attribute name list eg. [m_user_name, m_email]
        :param value:[list] Attribute's new values list eg. ["aaa", "example@example.com"]
        :return: None
        """
        sentence = f"UPDATE {table} set"
        for i in range(len(col)):
            sentence += f" {col[i]} = '{value[i]}',"
        sentence = sentence.strip(",")
        sentence += f" where {attr_name} = {attr}"
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(sentence)
        conn.commit()
        conn.close()


def user_role_check(user_role):
    """
    Selecting user table and return attributes' prefix in database
    :param user_role: [str] "manager" or "tenant"
    :return: table_name[str], attr_prefix[str]
    """
    table_name = ""
    attr_prefix = ""
    if user_role == "manager":
        table_name = "db_manager"
        attr_prefix = "m_"
    elif user_role == "tenant":
        table_name = "db_tenant"
        attr_prefix = "t_"
    return table_name, attr_prefix


def user_db_col(prefix, key):
    """
    Connecting attributes and adding corresponding prefix
    :param prefix:[str] Attributes' prefix
    :param key:[list] Attributes need be connected
    :return: col[str]
    """
    prefix_list = ["id", "email", "user_name", "user_password", "phone"]
    col = ""
    for i in key:
        if i in prefix_list:
            col = col + prefix + i + ", "
    col = col.strip(", ")
    return col


class DB:
    def __init__(self):
        self.opera = operation()

    def data_in_db(self, table, col, data):
        """
        Check the data existence
        :param table:[str]
        :param col:[str]
        :param data:[str]
        :return: [bool] False -> data do not exist; True -> data exist
        """
        exist_data = self.opera.select_data(table, col, None)
        if len(exist_data) == 0:
            return False
        if data in exist_data:
            return True
        elif data not in exist_data:
            return False

    def user_id_select(self, table, user_prefix, user_email, attribute):
        """
        Select user id based on email
        :param table:[str]
        :param user_prefix:[str] "m_" or "t_"
        :param user_email:[str]
        :param attribute:[str]
        :return: [str]
        """
        user_id_col = user_prefix + "id"
        condition = "{} = '{}'".format(attribute, user_email)
        user_id = self.opera.select_data(table, user_id_col, condition)
        return user_id[0]

    def property_id_select(self, table, address):
        """
        Select property id based on address
        :param table:[str]
        :param address:[str]
        :return: [str]
        """
        condition = "address = '{}'".format(address)
        property_id = self.opera.select_data(table, 'p_id', condition)
        return property_id[0]

    # auth-------------------------------------------------------------------------
    def save_user_data(self, users_info, user_role):
        """
        Data saving via register new user account
        :param users_info:[dict]
        :param user_role:[str]
        :return: [str]
        """
        key = ['email', 'user_password', 'user_name', 'phone']
        table, user_prefix = user_role_check(user_role)
        col = user_db_col(user_prefix, key)
        value = "('{}','{}','{}','{}')".format(users_info['email'], users_info['password'], users_info['username'],
                                               users_info['phone'])

        self.opera.insert_data(table, col, value)
        attribute = "{}email".format(user_prefix)
        user_id = self.user_id_select(table, user_prefix, users_info['email'], attribute)
        return user_id

    def user_email_exists(self, user_role, user_email):
        """
        Check email existence in the db
        :return: [bool] False -> user email do not exist; True -> user email exist
        """
        key = ["email"]
        table, user_prefix = user_role_check(user_role)
        col = user_db_col(user_prefix, key)
        return self.data_in_db(table, col, user_email)

    def valid_user(self, user_role, user_email, password):
        """
        Check user validation while login
        :param user_role:[str]
        :param user_email:[str]
        :param password:[str]
        :return:[str] None-> user do not valid
        """
        key = ["email", "user_password"]
        table, user_prefix = user_role_check(user_role)
        col = user_db_col(user_prefix, key)
        if self.data_in_db(table, col, [user_email, password]):
            attribute = "{}email".format(user_prefix)
            user_id = self.user_id_select(table, user_prefix, user_email, attribute)
            return user_id
        else:
            return None

    # user-------------------------------------------------------------------------
    def user_db_update(self, update_info, user_role, user_id):
        """
        Updating one user's information
        :param update_info: [str]
        :param user_role: [str]
        :param user_id: [str]
        :return: [bool] False -> user does not exist; True -> update successful
        """
        attr_dict = {"new_email": "email", "user_name": "user_name", "new_password": "user_password", "phone": "phone",
                     "1": "start_one", "2": "start_two", "3": "start_three"}
        table, user_prefix = user_role_check(user_role)
        col = user_db_col(user_prefix, ["id"])
        if not self.data_in_db(table, col, user_id):
            return False
        id_name = user_prefix + "id"
        values_list = []
        col_list = []
        for key in attr_dict.keys():
            if key in update_info.keys():
                values_list.append(str(update_info[key]))
                col_list.append(user_prefix + attr_dict[key])
        self.opera.update_db(user_id, id_name, table, col_list, values_list)
        return True

    def tenant_address_update(self, address, user_role, user_id):
        """
        link tenants with their manager based on address
        :param address: [str] address in db_property
        :param user_role: [str] "tenant"
        :param user_id: [str]
        :return: int(1)-> address did not exist
                int(2)->tenant did not exist
                int(3) -> success
        """
        table, user_prefix = user_role_check(user_role)
        col = user_db_col(user_prefix, ["id"])
        if not self.data_in_db("db_property", "address", address):
            return 1
        if not self.data_in_db(table, col, user_id):
            return 2
        id_list = self.opera.select_data("db_property", 'p_id, m_id', f'address = "{address}"')[0]
        plan = self.opera.select_data("db_manager", 'inspection_plan', f'm_id = "{id_list[1]}"')[0]
        col_list = ["p_id", "m_id","inspection_flag"]
        if plan and plan != "null":
            current_plan = json.loads(plan)
            p_list = current_plan["p_list"].split("|||")
            p_id = str(id_list[0])
            if p_id in p_list:
                id_list.append(current_plan["day"])
        else:
            id_list.append("null")
        self.opera.update_db(user_id, "t_id", table, col_list, id_list)

        return 3

    def get_user_info(self, role, uid):
        """
        Return user info base on id
        :param role:[str]
        :param uid: [str]
        :return: msg[dict]

        """
        if not self.data_in_db(f'db_{role}', f"{role[0]}_id", int(uid)):
            return 2
        userInfo = self.opera.select_data(f'db_{role}', '*', f'{role[0]}_id = {uid}')[0]
        msg = {
            'id': userInfo[0]
        }
        if role == "manager":
            msg["email"] = userInfo[1]
            msg["name"] = userInfo[3]
            msg["mobile"] = userInfo[4]
            msg["start_one"] = userInfo[5]
            msg["start_two"] = userInfo[6]
            msg["start_three"] = userInfo[7]
            msg["inspection_plan"] = userInfo[8]
        if role == "tenant":
            msg = {'email': userInfo[3],
                   'name': userInfo[5],
                   'mobile': userInfo[6],
                   "inspection_day": "null"}
            if userInfo[7] != "null" and userInfo[7] is not None:
                c_time = time.time()
                time_stp = float(time.mktime(time.strptime(userInfo[7], "%Y-%m-%d %H:%M:%S")))
                if c_time > time_stp:
                    self.opera.update_db(userInfo[0], "t_id", "db_tenant", ["inspection_flag"], ["null"])
                else:
                    msg["inspection_day"] = userInfo[7]
            attr_list = ['address', 'm_user_name', 'm_email', 'm_phone']
            for attr in attr_list:
                msg[attr] = "null"
            p_id = userInfo[1]
            m_id = userInfo[2]
            if p_id:
                address = self.opera.select_data(f'db_property', 'address', f'p_id = {p_id}')
                if len(address) > 0:
                    msg["address"] = address[0]
            if m_id:
                for attr in attr_list[1:]:
                    temp = self.opera.select_data(f'db_manager', attr, f'm_id = {m_id}')
                    if len(temp) > 0:
                        msg[attr] = temp[0]
        return msg

    def user_password_check(self, user_role, password):
        """
        Check user password existence in db
        :param user_role: [str]
        :param password: [str]
        :return: [bool] False -> password incorrect; True -> password correct
        """
        table, user_prefix = user_role_check(user_role)
        col = user_db_col(user_prefix, ["user_password"])
        if not self.data_in_db(table, col, password):
            return False
        else:
            return True

    # property----------------------------------------------------------------------
    def delete_property(self, p_id):
        """
        Delete one property info
        :param p_id: [str] property id
        :return: None
        """
        info = []
        m_id = None
        self.opera.delete_data("db_property", "p_id", p_id)
        t_info = self.opera.select_data("db_tenant", "t_id, m_id,t_user_name, t_email", f"p_id={p_id}")
        if len(t_info) > 0:
            for i in t_info:
                self.opera.update_db(i[0], "t_id", "db_tenant", ["p_id", "m_id"], ["null", "null"])
                m_id = i[1]
                info.append([i[2], i[3]])
        return m_id, info

    def add_property(self, property_info, manager_id):
        """
        adding one property infomation
        :param property_info: [str]
        :param manager_id: [str]
        :return: condition number[int]
        """
        if not self.data_in_db('db_manager', 'm_id', manager_id):
            return 2
        if self.data_in_db('db_property', 'address', property_info['address']):
            return 3
        table = 'db_property'
        col = ','.join(property_info.keys())
        value = "('" + "','".join([str(item) for item in property_info.values()]) + "')"
        self.opera.insert_data(table, col, value)
        return 4

    def get_property_info(self, mid):
        """
        Return property info base on id of manager
        :param mid: [int]
        :return: msg[dict]
        """
        propertyInfo = self.opera.select_data('db_property', '*', f'm_id = {mid}')
        propertyKey = ['p_id', 't_info', 'address', 'postcode', 'latitude', 'longitude', 'last_visit', 'rent_start',
                       'rent_end', 'property_Image']
        propertyInfoList = []
        if not propertyInfo:
            return False
        for item in propertyInfo:
            item.pop(1)
            propertyInfoList.append(dict(zip(propertyKey, item)))
        p_number = [str(i) for i in range(1, len(propertyKey) + 1)]
        propertyInfo = dict(zip(p_number, propertyInfoList))
        return propertyInfo

    def property_db_update(self, update_info, property_id):
        """
        Updating one user's information
        :param update_info: [str]
        :param property_id: [str]
        :return: [bool] False -> property does not exist; True -> update successful
        """
        if not self.data_in_db('db_property', 'p_id', property_id):
            return 2
        if self.opera.select_data('db_property', 'address', f"p_id = {property_id}")[0] != update_info['address']:
            if self.data_in_db('db_property', 'address', update_info['address']):
                return 3
        self.opera.update_db(property_id, 'p_id', 'db_property', [item for item in update_info.keys()],
                             [item for item in update_info.values()])
        return 4

    # inspection appointment----------------------------------------------------------
    def get_email_detail(self, p_id):
        t_name = []
        t_email = []
        p_id = p_id.split("|||")
        user_info = self.opera.select_data('db_property', 'm_id, t_info', f'p_id = {p_id[0]}')[0]
        m_name = self.opera.select_data(f'db_manager', "m_user_name", f'm_id = {user_info[0]}')[0]
        t_info = user_info[1].split("|||")
        t_name.append(t_info[0])
        t_email.append(t_info[1])
        if len(p_id) > 1:
            for i in p_id[1:]:
                user_info = self.opera.select_data('db_property', 't_info', f'p_id = {i}')[0]
                t_info = user_info.split("|||")
                t_name.append(t_info[0])
                t_email.append(t_info[1])
        return t_name, t_email, m_name

    def store_plan(self, m_id, plan, day, p_list, destinations, duration, in_plan):
        value_dict = {"day": str(day), "plan": plan.replace("'", "''"), "p_list": str(p_list),
                      "destinations": str(destinations), "duration": duration, "inPlan": in_plan}
        value = json.dumps(value_dict)
        if not self.data_in_db("db_manager", "m_id", int(m_id)):
            return 1
        self.opera.update_db(m_id, "m_id", "db_manager", ["inspection_plan"], [value])
        self.opera.update_db(m_id, "m_id", "db_tenant", ["inspection_flag"], [str(day)])
        return 2

    def tenant_inspection_check(self, t_id):
        if not self.data_in_db("db_tenant", "t_id", int(t_id)):
            return 1

        t_info = self.opera.select_data("db_tenant", "m_id, p_id, inspection_flag, t_user_name", f"t_id={t_id}")[0]
        if t_info[0] is None or t_info[0] == "null":
            return 2
        elif t_info[1] is None or t_info[1] == "null":
            return 3
        elif t_info[2] is None or t_info[2] == "null":
            return 4
        else:
            m_id = t_info[0]
            p_id = str(t_info[1])
            m_info = self.opera.select_data("db_manager", "m_user_name, m_email, inspection_plan", f"m_id={m_id}")[0]
            current_plan = json.loads(m_info[2])
            m_email = m_info[1]
            p_list = current_plan["p_list"].split("|||")
            p_list.remove(p_id)
            in_plan = json.loads(current_plan["inPlan"])
            in_plan["places"] = p_list
            in_plan = json.dumps(in_plan)
            addr = []
            for p in p_list:
                temp_addr = self.opera.select_data("db_property", "address", f"p_id={p}")[0]
                addr.append(temp_addr)
            response = {"day": current_plan["day"], "address": addr, "m_id": m_id, "p_list": p_list,
                        "destinations": current_plan["destinations"], "m_email": m_email, "m_name": m_info[0],
                        "t_name": t_info[3], "duration": current_plan["duration"], "in_plan": in_plan}
            return response

    # report-------------------------------------------------------------------------
    def delete_report(self, repo_id):
        self.opera.delete_data("db_repo", "repo_id", repo_id)

    def add_repo(self, repo_info, p_id):
        """
        adding one report infomation
        :param repo_info: [str]
        :param p_id: [str]
        :return: condition number[int]
        """
        if not self.data_in_db('db_property', 'p_id', p_id):
            return 1
        last_visit = self.opera.select_data('db_property', 'last_visit', f'p_id = {p_id}')[0]
        repo_info["last_visit_time"] = last_visit
        table = 'db_repo'
        col = ','.join(repo_info.keys())
        value = "('" + "','".join([str(item) for item in repo_info.values()]) + "')"
        self.opera.insert_data(table, col, value)
        return 2

    def get_report_info(self, mid):
        """
        Return property info base on id of manager
        :param mid: [int]
        :return: msg[dict]
        """
        p_id = self.opera.select_data('db_property', 'p_id', f'm_id = {mid}')
        report_info = []
        repo_key = ["repo_id", "p_id", "repo_content", "repo_title", "repo_date", "last_visit_time"]
        if not p_id:
            return 1
        for id in p_id:
            repo = self.opera.select_data('db_repo', '*', f'p_id = {id}')
            address = self.opera.select_data('db_property', "address", f'p_id = {id}')[0]
            if repo:
                for info in repo:
                    repo_dict = dict(zip(repo_key, info))
                    repo_dict["address"] = address
                    report_info.append(repo_dict)

        return report_info

    def report_update(self, update_info, repo_id):
        """
        Updating one user's information
        :param update_info: [str]
        :param repo_id: [str]
        :return: [bool] False -> property does not exist; True -> update successful
        """
        if not self.data_in_db('db_repo', 'repo_id', repo_id):
            return 2
        if not self.data_in_db('db_property', 'p_id', update_info["p_id"]):
            return 1
        self.opera.update_db(repo_id, 'repo_id', 'db_repo', [item for item in update_info.keys()],
                             [item for item in update_info.values()])
        return 3


if __name__ == '__main__':
    test = DB()
    opr = operation()

    user_info1 = {"username": "Doggy", 'password': "dog123", 'email': "doggy123@gmail.com", 'phone': "0416330312"}
    user_info2 = {"username": "Kitty", 'password': "cat88cat", 'email': "cat88cat@gmail.com", 'phone': "0428561225"}
    user_info3 = {"username": "Monkey", 'password': "987memes", 'email': "naughty@gmail.com", 'phone': "0421688256"}
    role = ["tenant"]
    for r in role:
        print(test.save_user_data(user_info1, r))
        print(test.save_user_data(user_info2, r))
        print(test.save_user_data(user_info3, r))
    # attr_name = "m_id"
    # attr = 1
    # table = "db_manager"
    # col = ["m_email", "m_user_password", "m_user_name", "m_phone"]
    # value = ["string", "string", "string", "string"]
    # opr.updat_db(attr, attr_name, table, col, value)
    # print(opr.select_data(table, "*", '"m_id"=1'))
    a = test.tenant_address_update("string", "tenant", 1)
    print(a)