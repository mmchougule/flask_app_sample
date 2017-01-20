from sqlite3 import dbapi2 as sqlite3
import json
import pprint
from flask import Flask, request, session, jsonify, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack

# DB configuration
DATABASE = 'company.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

def get_db():
    # Connect to the database if you are not already connected
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

@app.route("/list_companies")
def list():
    temp = query_db("select * from company")
    companies = []
    for row in temp:
        company = {}
        # Set this manually for now.
        company['company_id'] = row[0]
        company['company_name'] = row[1]
        company['address'] = row[2]
        company['revenue'] = row[3]
        companies.append(company)
    data = [{'success': 'true', 'total': len(companies), 'data': companies}]
    return json.dumps(data)

@app.route("/add_company", methods=['POST'])
def add_company():
    print request.json['company_name']
    if request.json['company_name']:
        db = get_db()
        db.execute('''insert into company (company_name, address, revenue)
            values (?, ?, ?)''', (request.json['company_name'], request.json['address'], request.json['revenue']))
        db.commit()
        flash('Created a new company record')
    return '1'

@app.route("/list_employees")
def list_employees():
    temp = query_db("select * from employee as e join company as c on c.company_id = e.company_id")
    print(temp)
    employees = []
    for row in temp:
        employee = {}
        # Set this manually for now.
        employee['employee_id'] = row[0]
        employee['firstname'] = row[1]
        employee['lastname'] = row[2]
        employee['company_id'] = row[3]
        employee['email'] = row[4]
        employee['company_name'] = row[5]
        employee['address'] = row[6]
        employees.append(employee)
    data = [{'success': 'true', 'total': len(employees), 'data': employees}]
    return json.dumps(data)

@app.route("/add_employee", methods=['POST'])
def add_employee():
    if request.json['email']:
        db = get_db()
        db.execute('''insert into employee (firstname, lastname, company_id, email)
            values (?, ?, ?, ?)''', (request.json['firstname'], request.json['lastname'], request.json['company_id'], request.json['email']))
        db.commit()
        flash('Created a new employee record')
    return '1'

@app.route("/")
def hello():
    return "Hello to you!"

if __name__ == "__main__":
    app.run()
