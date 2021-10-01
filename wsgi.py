from flask import Flask, request, redirect, jsonify
#, send_from_directory, render_template, request
#from jinja2 import Environment
#from jinja2.loaders import FileSystemLoader
from flask_sqlalchemy import SQLAlchemy
import secrets
import validators
import os
app = Flask(__name__)

app.config['FLASK_HOST'] = 'https://s.hypr.ax'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['FLASK_ENV']='development'
app.config['TEMPLATES_AUTO_RELOAD'] = True
authorization = os.environ.get('AUTHORIZATION')
domain = os.environ.get('DOMAIN')

db = SQLAlchemy(app)

class SiteRedir(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	original = db.Column(db.Text)
	target = db.Column(db.String(10))

#if path.exists("db.sqlite") == True:
#    print("Database exists")
#else:
#    print("Creating database")
db.create_all()

@app.route("/")
def index():
	return ("<script>location.replace('https://[YOUR_HOMEPAGE_URL]');</script>")
@app.route('/robots.txt', methods=['GET'])
def robots():
	text = """
User-agent: AhrefsBot
Disallow: *

User-agent: SemrushBot
Disallow: *

User-agen: DiscordBot
User-agent: *
Disallow: *
	"""
	resp = app.response_class(response=text,status=200,mimetype="text/plain")
	return resp
@app.route("/shorten/<path:path>", methods=["POST"])
def static_dir(path):
#	print(path)
	#print(request.data)
#	req_data = request.get_json()
#	Auth = req_data['authorization']
#	original = req_data['original']
#	print(original)
	if request.headers['Authorization'] != authorization:
		return "401 Unauthorised", 401
#	else:
#		print("Authorised!")
#	print(original)
	target = secrets.token_urlsafe(5)
	dbloc = SiteRedir.query.filter_by(target=target).first()
	original = request.url.replace("http://"+domain+"/shorten/", "", 1)
	print(original)
	valid=validators.url(original)
	if not valid:
		return "Invalid URL", 400
	while dbloc is not None:
		target = secrets.token_urlsafe(5)
		dbloc = SiteRedir.query.filter_by(target=target).first()
	dbwrite = SiteRedir(original=original,target=target)
	db.session.add(dbwrite)
	db.session.commit()
	return "https://"+domain+"/"+str(target), 200

@app.route("/<url>")
def urlSearch(url):
	dbloc = SiteRedir.query.filter_by(target=url).first()
	if dbloc is None:
		return "404 Not Found", 404
	else:
#		return "<script>location.replace('"+str(dbloc.original)+"');</script>"
		return redirect(dbloc.original, 302)

#@app.route("/login")

#@appr.route("/login/)
