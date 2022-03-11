db_name = "property_manager.db"

db_repo = """create table if not exists db_repo(
    repo_id integer primary key autoincrement unique not null,
    p_id integer not null,
    repo_content text not null,
    repo_title text not null,
    repo_date numeric not null,
    last_visit_time numeric not null
);"""

# t_info = t_name|||t_email -> manager input
db_property = """
create table if not exists db_property(
    p_id integer primary key autoincrement unique not null,
    m_id integer not null,
    t_info char(50) not null,
    address char(50) not null,
    postcode text not null,
    latitude char(50) not null,
    longitude char(50) not null,
    last_visit numeric not null,
    rent_start numeric not null,
    rent_end numeric not null
);
"""

db_manager = """
create table if not exists db_manager(
    m_id integer primary key autoincrement unique not null,
    m_email char(50) not null,
    m_user_password char(50) not null,
    m_user_name char(50) not null,
    m_phone char(50) not null,
    m_start_one char(200),
    m_start_two char(200),
    m_start_three char(200),
    inspection_plan char(200)
);
"""

db_tenant = """
create table if not exists db_tenant(
    t_id integer primary key autoincrement unique not null,
    p_id integer,
    m_id integer,
    t_email char(50) not null,
    t_user_password char(50) not null,
    t_user_name char(50) not null,
    t_phone char(50) not null,
    inspection_flag text 
);
"""