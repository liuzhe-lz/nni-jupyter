import json
from pathlib import Path
from notebook.utils import url_path_join
import requests
from tornado.web import RequestHandler

experiment_list_path = Path.home() / 'nni-experiments/.experiment'

class NniProxyHandler(RequestHandler):
    def get(self, uri):
        if not experiment_list_path.exists():
            self.set_status(404)
            return
        port = None
        for experiment in json.load(open(experiment_list_path)).values():
            if experiment['status'] != 'STOPPED':
                port = experiment['port']
        if port is None:
            self.set_status(404)
            return

        r = requests.get(f'http://localhost:{port}/{uri}')
        self.set_status(r.status_code)
        for key, value in r.headers.items():
            self.add_header(key, value)
        self.finish(r.content)

def setup_handlers(web_app):
    base_url = url_path_join(web_app.settings['base_url'], 'nni')
    proxy_url = url_path_join(base_url, 'nni/(.*)')
    handlers = [(proxy_url, NniProxyHandler)]
    web_app.add_handlers('.*$', handlers)
