import os
import sqlite3
import httplib2
from flask import Flask, g, render_template, request, redirect
from shortener import id_to_base64, base64_to_id

# Settings
ROOT = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(ROOT, 'database.sqlite3')

# App Config
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.before_request
def before_request():
    """Connect to database
    """
    g.db = sqlite3.connect(DATABASE)


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
    c.execute('INSERT INTO urls VALUES (NULL, NULL, ?)', (url,))
    id = c.lastrowid
    c.execute('UPDATE urls SET key = ? WHERE id = ?', (id_to_base64(id), id))
    c.execute('SELECT * FROM urls WHERE id = ?', (id,))
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
            c.execute('SELECT * FROM urls WHERE url = ?', (url,))
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
    c.execute('SELECT * FROM urls WHERE key = ?', (base64,))
    result = c.fetchone()
    g.db.commit()
    c.close()
    if result:
        return redirect(result[2], 301)
    else:
        return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(debug=True)