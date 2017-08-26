import logging
import asyncio

import xml.etree.ElementTree as ET
import xmltodict, json

from dateutil.parser import parse

from extractor.configuration import Configuration as Config


# Heideltime
# - is a commandline tool (jar)
# - can only read and write files


async def _do_subprocess(filename, date, path, results):
    path_to_libs = Config.get()['Giveme5W-runtime-resources']
    command = 'java -jar de.unihd.dbs.heideltime.standalone.jar -t NEWS ' + filename + ' -dct ' + date
    proc = await asyncio.create_subprocess_shell(command,
                                                 shell=True, cwd=path_to_libs + '/' + path,
                                                 stdout=asyncio.subprocess.PIPE)
    results.append(await proc.stdout.read())


class Heideltime():
    def __init__(self):
        self.log = logging.getLogger('GiveMe5W-Enhancer')

    def enhance(self, document):
        filename = Config.get()['Giveme5W-runtime-resources'] + '/' + 'tmp.txt'
        # raw document date
        date = document.get_rawData().get('publish_date')

        answers = document.get_answers().get('when')

        if answers:
            # parsed document date
            date = parse(date)
            date = date.strftime('%Y-%m-%d')
            if date:

                for answer in answers:
                    answer_text = ''
                    for part in answer[0]:
                        answer_text = answer_text + ' ' + part[0]

                    if answer_text and len(answer_text) > 1:
                        # write the question as file to disc
                        outfile = open(filename, 'w')
                        outfile.write(answer_text)
                        outfile.close()

                        results = []
                        event_loop = asyncio.get_event_loop()
                        tasks = [asyncio.ensure_future(_do_subprocess(filename, date, 'heideltime-standalone', results))]
                        event_loop.run_until_complete(asyncio.wait(tasks))

                        # WARNING direct conversion to JSON, some information can`t be transferred
                        o = xmltodict.parse(results[0])
                        answer.append(json.dumps(o))

            else:
                self.log.error(document.get_document_id + ': ' + document.get_title())
                self.log.error(
                    "Heideltime need a publish date to parse news. Input:" + document.get_rawData().get('publish_date'))
        else:
            self.log.error(document.get_document_id + ': ' + document.get_title())
            self.log.error("Heideltime need EnvironmentExtractor results. skipped")