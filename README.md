# flask_app_sample
A simple example using Flask microframework for Python. Database for companies and employee.

Steps to run:
<ul>
<li>1. Set up a virtualenv pip install virtualenv</li>
<li>2. virtualenv env (env will be the directory for this new virtual environment)</li>
<li>3. Activate this environment:<br/> source bin/activate</li>
<li>4. Export the right application to Flask:
    export FLASK_APP=app.py</li>
<li>5. Initialize the database:<br/>
    flask initdb</li>
<li>6: Run the app<br/>
flask run</li>
</ul>

Endpoints:
1. Add companies information (POST) request:
    curl -H "Content-Type: application/json" -X POST -d '{"company_name": "Microsoft", "address": "Redmond, WA", "revenue": "$299 Billion"}' http://localhost:5000/add_company

2. List companies data:
    http://localhost:5000/list_companies
