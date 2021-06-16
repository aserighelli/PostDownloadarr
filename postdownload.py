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
dt_string = datetime.now().strftime('%Y%m%d_%H%M%S.%f')
event_type = str(os.environ.get('%sARR_EVENTTYPE' % prefix))
if 'Grab' in event_type:
    titulo = str(os.environ.get('%sARR_RELEASE_TITLE' % prefix)).replace(' ', '.')
    filename = '%s%sARR_%s_%s.txt' % (logpath, prefix, event_type, titulo)
elif 'Download' in event_type:
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
legendas = glob(path + '\\*.srt')
if len(legendas) > 0:
    logfile.write('\nLegendas renomeadas:\n')
    for item in legendas:
        nomelegenda = os.path.splitext(os.path.basename(item))
        idioma = os.path.splitext(nomelegenda[0])
        if 'pt' not in idioma[1] and 'en' not in idioma[1]:
            nomenovo = str(path) + '\\' + nomelegenda[0] + '.pt-BR.srt'
            os.rename(r'%s' % item, r'%s' % nomenovo)
            logfile.write('%s -> %s\n' % (str(os.path.basename(item)), str(os.path.basename(nomenovo))))
else:
    logfile.write('\nSem legendas para renomear\n')
logfile.close()