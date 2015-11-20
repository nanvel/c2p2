import json
import hmac
import logging

from ipaddress import ip_address, ip_network
from hashlib import sha1

from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError

from ..models import Site
from ..settings import settings
from ..utils import github_pull
from .base import C2P2Handler


__all__ = ('GitHubPullHandler',)


logger = logging.getLogger(__name__)


class GitHubPullHandler(C2P2Handler):

    SUPPORTED_METHODS = ('POST',)
    GITHUB_URL_META = 'https://api.github.com/meta'

    @gen.coroutine
    def post(self):
        if settings.GITHUB_VALIDATE_IP:
            remote_ip = self.request.headers.get('X-Real-IP')
            remote_ip = remote_ip or self.request.remote_ip
            remote_ip = ip_address(str(remote_ip))
            headers = {'Content-Type': 'application/json; charset=UTF-8', 'User-Agent': 'c2p2'}
            request = HTTPRequest(self.GITHUB_URL_META, method='GET', headers=headers)
            response = yield AsyncHTTPClient().fetch(request)
            white_list = json.loads(response.body.decode('utf8'))['hooks']

            for valid_ip in white_list:
                if remote_ip in ip_network(valid_ip):
                    break
            else:
                raise HTTPError(code=403)

        if settings.GITHUB_SECRET:
            # only SHA1 is supported
            sha_name, signature = self.request.headers.get('X-Hub-Signature').split('=')
            if sha_name != 'sha1':
                raise HTTPError(code=501)

            # HMAC requires the key to be bytes, but data is string
            mac = hmac.new(settings.GITHUB_SECRET.encode(), msg=self.request.body, digestmod=sha1)

            if not hmac.compare_digest(str(mac.hexdigest()), str(signature)):
                raise HTTPError(code=403)

        logging.warning('GitHub pull ...')

        event = self.request.headers.get('X-GitHub-Event', 'ping')
        self.set_header('Content-Type', 'application/json')

        # ping
        if event == 'ping':
            self.write(json.dumps({'msg': 'pong'}))
            return

        if event == 'push':
            data = json.loads(self.request.body.decode('utf8'))
            if data['ref'] == 'refs/heads/{branch}'.format(branch=settings.GITHUB_BRANCH):
                result, error = yield github_pull()
                logger.warning(result)
                logger.warning(error)
                # update
                Site().update()
