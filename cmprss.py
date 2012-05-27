import httplib2
import os
import psycopg2
import urlparse
from flask import Flask, g, render_template, request, redirect
from shortener import id_to_base64, base64_to_id

# Settings
ROOT = os.path.dirname(os.path.abspath(__file__))

# App Config
app = Flask(__name__)
app.url_map.strict_slashes = False

@app.before_request
def before_request():
    """Connect to database
    """
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ['HEROKU_POSTGRESQL_CRIMSON_URL'])
    g.db = psycopg2.connect("dbname=%s user=%s password=%s host=%s" % (
        url.path[1:],
        url.username,
        url.password,
        url.hostname)
    )

@app.teardown_request
def teardown_request(exception):
    """Disconnect from database
    """
    g.db.close()


def normalise_url(url):
    """A basic attempt at fixing any problems with a URL's format
    """
    url.strip().lower()
    if not url.startswith('http://'):
        url = 'http://{0}'.format(url)
    return url


def url_exists(url):
    """Get the headers of a web resource to check if it exists
    """
    h = httplib2.Http()
    try:
        resp = h.request(url, 'HEAD')
        if resp[0].status == 200:
            return True
    except (httplib2.RelativeURIError, httplib2.ServerNotFoundError):
        return False


def shorten_url(c, url):
    """Insert a new record to get its id, update the record with the key and
    query again for the record to return it.
    """
    c.execute('INSERT INTO urls (url) VALUES (%s) RETURNING urls.id', (url,))
    id = c.fetchone()[0]
    c.execute('UPDATE urls SET key = %s WHERE id = %s', (id_to_base64(id), id))
    c.execute('SELECT * FROM urls WHERE id = %s', (id,))
    return c.fetchone()[1]


@app.route('/', methods=['GET', 'POST'])
def shorten():
    """Display a form to request a URL and shorten it if it's not been shortened
    previously.
    """
    if request.method == 'POST':
        url = normalise_url(request.form.get('url', None))
        if url and url_exists(url):
            c = g.db.cursor()
            c.execute('SELECT * FROM urls WHERE url = %s', (url,))
            result = c.fetchone()
            if result:
                key = result[1]
            else:
                key = shorten_url(c, url)
            g.db.commit()
            c.close()
        else:
            error = True
    return render_template('shorten.html', **locals())


@app.route('/<base64>', methods=['GET'])
def expand(base64):
    """Check the database for a url with this key and permanently redirect if
    found, otherwise show an error page with a 404 status code.
    """
    c = g.db.cursor()
    c.execute('SELECT * FROM urls WHERE key = %s', (base64,))
    result = c.fetchone()
    g.db.commit()
    c.close()
    if result:
        return redirect(result[2], 301)
    else:
        return render_template('error.html'), 404

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    debug = True if port == 5000 else False
    app.run(host='0.0.0.0', port=port, debug=debug)

