"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from dpccscrawler import DPCCAirScrawler

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/8dqUUbjDbujeXgEyPQBhjevQTjHJSHd748YqvphFdkQGTgP6QUh4tXcMUuWbGT2R7XDJqDjb4EhGjG7pVrFq3wQV4F4qmWTGaTrp')
def scrape():
    DPCCAirScrawler.scrape()
    return 'Scraping Done'

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
