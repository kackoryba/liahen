import os
import socket
from time import time

from django.conf import settings

from submit.models import Submit


# koncovka -> jazyk
def get_lang_from_filename(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext not in Submit.EXTMAPPING:
        return False
    return Submit.EXTMAPPING[ext]


# posielanie submitu na testovac
# vracia dvojicu (ci je vsetko OK, detaily(id submitu/aka chyba))
def process_submit(f, task, language, user):
    if language == '.':
        lang = get_lang_from_filename(f.name)
        if not lang:
            return (False, 'file-error')
        language = lang

    submit = Submit(language=language, user=user, task=task)
    submit.save()

    data = f.read()
    user_id = 'liahen3-' + str(user.username)
    task_id = str(task.id)
    correct_filename = task_id + language
    original_name = f.name

    timestamp = int(time())

    raw = "LIAHEN3\n%s\n%s\n%s\n%d\n%s\n%s" % (
          submit.id, user_id, correct_filename, timestamp,
          original_name, data)

    # priprava lok. directories
    path = settings.PROJECT_PATH + '/../submit/submits'
    try:
        os.mkdir(path)
    except OSError:
        pass

    path += '/' + str(user.username)
    try:
        os.mkdir(path)
    except OSError:
        pass

    path += '/' + str(task.id)
    try:
        os.mkdir(path)
    except OSError:
        pass

    os.chmod(path, 0o777)

    # submity si odlozime aj u seba
    datafile = open(path + '/' + str(submit.id) + '.data', 'w')
    datafile.write(data)
    datafile.close()

    rawfile = open(path + '/' + str(submit.id) + '.raw', 'w')
    rawfile.write(raw)
    rawfile.close()

    # posleme na testovac Exeriment
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('10.0.0.3', 12347))
    except Exception:  # todo: log the error
        return False, 'connect-error'

    sock.send(raw)
    sock.close()

    return True, submit.id
