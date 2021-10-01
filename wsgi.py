from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import secrets
import validators
import os
app = Flask(__name__)

app.config['FLASK_HOST'] = 'https://'+domain
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
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
@app.route("/shorten/<path:path>", methods=["POST"]) # Returns shortened URLs
def static_dir(path):

	if request.headers['Authorization'] != authorization:
		return "401 Unauthorised", 401

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

@app.route("/<url>") #handles shortned links
def urlSearch(url):
	dbloc = SiteRedir.query.filter_by(target=url).first()
	if dbloc is None:
		return "404 Not Found", 404
	else:
		return redirect(dbloc.original, 302)
