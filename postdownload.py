import os
import sys
import pathlib
from glob import glob
from os import environ, path
from os.path import join
from datetime import datetime
# Bloco para criar o arquivo de log
logpath = 'C:\\ProgramData\\PostDownloadarr\\logs\\'
if 'SONARR_EVENTTYPE' in os.environ:
    prefix = 'SON'
    content = 'EPISODE'
elif 'RADARR_EVENTTYPE' in os.environ:
    prefix = 'RAD'
    content = 'MOVIE'
else:
    prefix = 'MANUAL'
if 'BJShare' in os.environ:
    now = datetime.now().strftime('%Y%m%d_%H%M%S.%f')
    event_type = str(os.environ.get('%sARR_EVENTTYPE' % prefix)).upper()
    if 'GRAB' in event_type:
        titulo = str(os.environ.get('%sARR_RELEASE_TITLE' % prefix)).replace(' ', '.')
        filename = '%s%sARR_%s_%s.txt' % (logpath, prefix, event_type, titulo)
    elif 'DOWNLOAD' in event_type:
        path = str(os.path.dirname(os.environ.get('%sARR_%sFILE_PATH' % (prefix, content))))
        titulo = str(os.environ.get('%sARR_%sFILE_SCENENAME' % (prefix, content))).replace(' ', '.')
        filename = '%s%sARR_%s_%s.txt' % (logpath, prefix, event_type, titulo)
    else:
        path = str(pathlib.Path().absolute())
        filename = '%s%s_%s.txt' % (logpath, prefix, dt_string)
    logfile = open(filename, 'x')
    for (item, value) in os.environ.items():
        if 'ARR' in item:
            logfile.write('{}: {}\n'.format(item, value))
#Bloco para renomear as legendas
    video = []
    for ext in ('*.mp4', '*.mkv'):
        video.extend(glob(join(path + '\\' + ext)))
    if len(video) > 0:
        legendas = glob(path + '\\*.srt')
        if len(legendas) > 0:
            logfile.write('\nLegendas renomeadas:\n')
            for item in legendas:
                nomelegenda = os.path.basename(item)
                nomelegenda = os.path.splitext(nomelegenda)
                nomelegenda = nomelegenda[0]
                idioma = os.path.splitext(nomelegenda)
                if 'pt' not in idioma[1] and 'en' not in idioma[1]:
                    nomeantigo = item
                    nomenovo = str(path) + '\\' + nomelegenda + '.pt-BR.srt'
                    os.rename(r'%s' % nomeantigo, r'%s' % nomenovo)
                    logfile.write('%s -> %s\n' % (str(os.path.basename(nomeantigo)), str(os.path.basename(nomenovo))))
    logfile.close()