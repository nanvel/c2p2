import os.path

from tornado import gen
from tornado.options import options
from tornado.process import Subprocess
from tornado.httpclient import HTTPError

from .path import rel


__all__ = ('github_pull',)


@gen.coroutine
def github_pull():

    script_path = os.path.join(rel(options.SOURCE_FOLDER), 'pull.sh')
    if not os.path.exists(script_path):
        raise gen.Return(None)

    sub_process = Subprocess(
        'bash',
        stdin=Subprocess.STREAM,
        stdout=Subprocess.STREAM,
        stderr=Subprocess.STREAM
    )

    yield gen.Task(sub_process.stdin.write, script_path.encode())
    sub_process.stdin.close()

    result, error = yield [
        gen.Task(sub_process.stdout.read_until_close),
        gen.Task(sub_process.stderr.read_until_close)
    ]

    raise gen.Return((result, error))
