import traceback

from tornado.httpclient import HTTPError
from tornado.web import RequestHandler


__all__ = ('C2P2Handler',)


class C2P2Handler(RequestHandler):

    def write_error(self, status_code, **kwargs):

        if self.settings.get('serve_traceback') and 'exc_info' in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs['exc_info']):
                self.write(line)
            self.finish()
        else:
            try:
                if 'exc_info' in kwargs:
                    error = kwargs['exc_info'][1]
                    if isinstance(error, HTTPError):
                        status_code = error.code
                self.set_status(status_code=status_code)
                if status_code == 404:
                    self.render('404.html')
                else:
                    self.render('500.html')
            except Exception:
                self.finish(
                    "<html><title>{code}: {message}</title>"
                    "<body>{code}: {message}</body></html>".format({
                            "code": status_code,
                            "message": self._reason,
                    })
                )
