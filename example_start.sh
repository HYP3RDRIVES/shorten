export AUTHORIZATION=<YOUR_TOKEN_HERE>
export DOMAIN=<DOMAIN_HERE>
export FLASK_HOST=https://<DOMAIN_HERE>
export FLASK_APP=wsgi.py
export FLASK_ENV=production
export TEMPLATES_AUTO_RELOAD=true
/usr/bin/gunicorn --bind 0.0.0.0:<PORT_HERE> wsgi:app
