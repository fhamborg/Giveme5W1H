import asyncio
import os
from subprocess import check_output

from Giveme5W1H.extractor.configuration import Configuration as Config

path_to_libs = Config.get()['Giveme5W-runtime-resources']


async def do_subprocess(task, command, path):
    path_runtime_res = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, path_to_libs, path))

    print(task + ':' + path_runtime_res)

    proc = await asyncio.create_subprocess_shell(command, shell=True, cwd=path_runtime_res)
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


class RuntimeResourcesInstaller:
    """
    Makes sure that the Runtime-Resources fulfill minimum requirements. Hence, this install the stanford corenlp server.
    """

    @staticmethod
    def check_and_install():
        path_runtime_res = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, path_to_libs))
        path_giveme5w_installation = os.path.abspath(os.path.join(path_runtime_res, os.pardir))
        file_stanford_models = os.path.abspath(os.path.join(path_runtime_res, 'stanford-corenlp-full-2017-06-09',
                                                            'stanford-english-corenlp-2017-06-09-models.jar'))

        if os.path.isfile(file_stanford_models):
            return

        # if the models file does not exist, we assume that the installation did not complete and install stanford.
        cmd = 'mkdir runtime-resources && cd runtime-resources && wget http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip && unzip stanford-corenlp-full-2017-06-09.zip && rm stanford-corenlp-full-2017-06-09.zip' \
              ' && wget http://nlp.stanford.edu/software/stanford-english-corenlp-2017-06-09-models.jar && mv stanford-english-corenlp-2017-06-09-models.jar stanford-corenlp-full-2017-06-09/ && cd ..'

        check_output(cmd, shell=True, cwd=path_giveme5w_installation)
