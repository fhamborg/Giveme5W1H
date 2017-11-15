import asyncio
import os

from extractor.configuration import Configuration as Config

path_to_libs = Config.get()['Giveme5W-runtime-resources']


async def do_subprocess(task, command, path):
    dir = os.path.dirname(__file__)
    abs_path = os.path.join(dir, './../.' + path_to_libs + path)

    print(task + ':' + abs_path)

    proc = await asyncio.create_subprocess_shell(command, shell=True, cwd=abs_path)
    return_code = await proc.wait()
    print(task + 'closed.  Return code = %d' % return_code)


class StartupHelper:
    def __init__(self):
        self._tasks = []

    def do_command(self, log_name, command, cwd):
        self._tasks.append(asyncio.ensure_future(do_subprocess(log_name, command, cwd)))
        return self

    def forever(self):
        loop = asyncio.get_event_loop()
        loop.run_forever()
        loop.close()
