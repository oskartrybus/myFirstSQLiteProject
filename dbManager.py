import sqlite3

# ALL QUERIES:

CREATE_TEAM_MEMBERS_TABLE = """ CREATE TABLE IF NOT EXISTS team_members (
    member_id INTEGER PRIMARY KEY,
    name TEXT,
    surname TEXT,
    position TEXT,
    phone_number REAL
    );
"""
CREATE_PROJECTS_TABLE = """ CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT,
    deadline_date REAL,
    completed INTEGER
    );
"""
CREATE_PROJECT_MEMBER_TABLE = """ CREATE TABLE IF NOT EXISTS project_member (
    member_id INTEGER,
    project_id INTEGER,
    FOREIGN KEY(member_id) REFERENCES team_members(member_id),
    FOREIGN KEY(project_id) REFERENCES projects(project_id)
    );
"""

SELECT_ALL_TEAM_MEMBERS = "SELECT * FROM team_members;"
SELECT_MEMBER_BY_NAME = "SELECT * FROM team_members WHERE name LIKE ?;"
SELECT_MEMBER_BY_SURNAME = "SELECT * FROM team_members WHERE surname LIKE ?;"
INSERT_MEMBER = "INSERT INTO team_members(name, surname, position, phone_number) VALUES (?,?,?,?);"
DELETE_MEMBER = "DELETE FROM team_members WHERE name=? AND surname=?;"
INSERT_PROJECT = "INSERT INTO projects(project_name, deadline_date, completed) VALUES (?,?, 0);"
DELETE_PROJECT = "DELETE FROM projects WHERE project_name=?;"
SELECT_PROJECTS = "SELECT * FROM projects WHERE completed=? ORDER BY deadline_date;"
MAKE_PROJECT_COMPLETED = "UPDATE projects SET completed=1 WHERE project_name=?;"
SELECT_PROJECT_BY_NAME = "SELECT * FROM projects WHERE project_name=?;"
SELECT_PROJECT_BY_ID = "SELECT * FROM projects WHERE project_id=?;"
ASSIGN_MEMBER_TO_PROJECT = "INSERT INTO project_member VALUES (?,?);"
DISMISS_MEMBER_FROM_PROJECT = "DELETE FROM project_member WHERE member_id=? AND project_id=?;"
SELECT_MEMBER_PROJECTS = "SELECT * FROM project_member WHERE member_id=?"

connection = sqlite3.connect("database.db")


def create_tables():
    with connection:
        connection.execute(CREATE_TEAM_MEMBERS_TABLE)
        connection.execute(CREATE_PROJECTS_TABLE)
        connection.execute(CREATE_PROJECT_MEMBER_TABLE)


# MEMBERS:
def get_all_team_members():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ALL_TEAM_MEMBERS)
        return cursor.fetchall()


def get_member(searchBy: str, searchingPhrase):
    with connection:
        cursor = connection.cursor()
        if searchBy == "0":
            cursor.execute(SELECT_MEMBER_BY_NAME, (f"%{searchingPhrase}%",))
        else:
            cursor.execute(SELECT_MEMBER_BY_SURNAME, (f"%{searchingPhrase}%",))
        return cursor.fetchall()


def add_member(name, surname, position, phone_number):
    with connection:
        connection.execute(INSERT_MEMBER, (name, surname, position, phone_number))


def delete_member(name, surname):
    with connection:
        connection.execute(DELETE_MEMBER, (name, surname))


# PROJECTS:
def get_projects(completed: int):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_PROJECTS, (completed, ))
        return cursor.fetchall()


def add_project(project_name, deadline_date):
    with connection:
        connection.execute(INSERT_PROJECT, (project_name, deadline_date))


def delete_project(project_name):
    with connection:
        connection.execute(DELETE_PROJECT, (project_name, ))


def update_project(name):
    with connection:
        connection.execute(MAKE_PROJECT_COMPLETED, (name, ))


def get_project_by_name(name):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_PROJECT_BY_NAME, (name,))
        return cursor.fetchall()


def get_project_by_id(_id):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_PROJECT_BY_ID, (_id,))
        return cursor.fetchall()


# PROJECTS - MEMBERS
def assign_member_to_project(member_id, project_id):
    with connection:
        connection.execute(ASSIGN_MEMBER_TO_PROJECT, (member_id, project_id))


def dismiss_member_from_project(member_id, project_id):
    with connection:
        connection.execute(DISMISS_MEMBER_FROM_PROJECT, (member_id, project_id))


def get_projects_of_member(member_id):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_MEMBER_PROJECTS, (member_id,))
        return cursor.fetchall()
