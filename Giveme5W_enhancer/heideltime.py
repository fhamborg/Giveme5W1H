import asyncio
import logging

import xmltodict
from dateutil.parser import parse

from .abs_enhancer import AbsEnhancer, target
from extractor.configuration import Configuration as Config


# Heideltime
# - is a commandline tool (jar)
# - can only read and write files
async def _do_subprocess(filename, date, path, results):
    path_to_libs = Config.get()['Giveme5W-runtime-resources']
    command = 'java -jar de.unihd.dbs.heideltime.standalone.jar -it -t NEWS ' + filename + ' -dct ' + date
    proc = await asyncio.create_subprocess_shell(command,
                                                 shell=True, cwd=path_to_libs + '/' + path,
                                                 stdout=asyncio.subprocess.PIPE)
    results.append(await proc.stdout.read())


class Heideltime(AbsEnhancer):
    def __init__(self, questions):
        self.log = logging.getLogger('GiveMe5W-Enhancer')
        self._questions = questions

    def process(self, document):
        filename = Config.get()['Giveme5W-runtime-resources'] + '/' + 'tmp.txt'
        # raw document date
        date = document.get_rawData().get('publish_date')

        # parsed document date
        date = parse(date)
        date = date.strftime('%Y-%m-%d')

        if date:
            # write the question as file to disc
            outfile = open(filename, 'w')
            outfile.write(document.get_fullText())
            outfile.close()

            results = []
            event_loop = asyncio.get_event_loop()
            tasks = [
                asyncio.ensure_future(_do_subprocess(filename, date, 'heideltime-standalone', results))]
            event_loop.run_until_complete(asyncio.wait(tasks))

            # WARNING direct conversion to JSON, some information can`t be transferred
            o = xmltodict.parse(results[0])
            document.set_enhancement('heideltime', o)
        else:
            self.log.error('')
            self.log.error(document.get_document_id() + ': ' + document.get_title())
            self.log.error(
                "         Heideltime needs a publish date to parse news. Input:" + document.get_rawData().get('publish_date'))

    def enhance(self, document):
        # TODO
        return None