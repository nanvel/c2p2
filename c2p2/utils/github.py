from tornado import gen
from tornado.process import Subprocess

from ..settings import settings


__all__ = ('github_pull',)


@gen.coroutine
def github_pull():

    sub_process = Subprocess(
        'git',
        stdin=Subprocess.STREAM,
        stdout=Subprocess.STREAM,
        stderr=Subprocess.STREAM
    )

    yield gen.Task(sub_process.stdin.write, ('pull origin {branch}'.format(branch=settings.GITHUB_BRANCH)).encode())
    sub_process.stdin.close()

    result, error = yield [
        gen.Task(sub_process.stdout.read_until_close),
        gen.Task(sub_process.stderr.read_until_close)
    ]

    raise gen.Return((result, error))
