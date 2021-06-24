from notebook.utils import url_path_join
import requests
from tornado.web import RequestHandler

class NniProxyHandler(RequestHandler):
    def get(self, uri):
        r = requests.get('http://localhost:8080/' + uri)
        self.set_status(r.status_code)
        for key, value in r.headers.items():
            self.add_header(key, value)
        self.finish(r.text)

def setup_handlers(web_app):
    base_url = url_path_join(web_app.settings['base_url'], 'jlab-ext-example')
    proxy_url = url_path_join(base_url, 'nni/(.*)')
    handlers = [(proxy_url, NniProxyHandler)]
    web_app.add_handlers('.*$', handlers)
