import subprocess
import asyncio

from extractor.configuration import Configuration as Config

path_to_libs = Config.get()['Giveme5W-runtime-resources']


async def do_subprocess(task, command, path):
    print(task)
    proc = await asyncio.create_subprocess_shell(command,
                                                 shell=True, cwd=path_to_libs+'/'+path )
    return_code = await proc.wait()
    print(task + ' closed.  Return code = %d' % return_code)

loop = asyncio.get_event_loop()

# add or remove jars here
tasks = [
    #asyncio.ensure_future(do_subprocess('CoreNLP',
    #                                    'java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000',
    #                                    'stanford-corenlp-full-2016-10-31')),

   # asyncio.ensure_future(do_subprocess('AIDA-Web',
   #                                     'mvn jetty:run -Djetty.http.port=9001',
   #                                     'aida-3.0.4')),

    asyncio.ensure_future(do_subprocess('AIDA',
                                        'java -Xmx12G -cp target/aida-3.0.4-jar-with-dependencies.jar mpi.aida.CommandLineDisambiguator -t PRIOR -s -i "Einstein was born in Ulm"',
                                        'aida-3.0.4')),

   # asyncio.ensure_future(do_subprocess('Heideltime',
    #                                    'java -jar de.unihd.dbs.heideltime.standalone.jar -t NEWS -dct YYYY-MM-DD',
     #                                   'heideltime-standalone')),
]



loop.run_forever()
loop.close()


