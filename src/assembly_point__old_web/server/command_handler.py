
'''
{'id': '', 'type':'start', 'cmd': str} -> {'id': str, 'type':'start', 'args':args, 'kwargs': kwargs}
{'id': str, 'type':'progress'} -> {'id': str, 'type':'progress', 'progress': float, 'ready': bool}

{'id': str, 'type':'data'} -> {'id': str, 'type':'data', 'data': {}, 'files': {}}

{'id': str, 'type':'kill'} -> {'id': str, 'type':'kill'}
{'id': str, 'type':'keep', 'time': int} -> {'id': str, 'type':'keep', 'time': int}

{'type':'exit'} -> {'type':'exit'}
'''

import threading
import queue
import time
import os

from src.assembly_point__old_web.server import command_task

QUEUE_SIZE = 10
THREAD_COUNT = 5

run_status = False

running_commands = {}
cmd_handlers = {}

commands_queue = queue.Queue(QUEUE_SIZE)

def process(cmd):
    
    try:
        res = {'id': cmd.get('id', ''), 'type': cmd['type']}

        if cmd['type'] == 'start':
            cmd_handler = cmd_handlers.get(cmd['cmd'])
            if cmd_handler is None:
                return {'id': '', 'type': 'error', 'text': 'Команда не существует'}
            task = command_task.Task(cmd_handler, cmd['args'], cmd['kwargs'])
            uid = task.uid
            try:
                commands_queue.put_nowait(task)
            except queue.Full:
                return {'id': uid, 'type': 'error', 'text': 'Очередь выполнения заполнена, подождите'}
            running_commands[uid] = task

            res['id'] = uid
        elif cmd['type'] == 'exit':
            stop()
        elif cmd['type'] == 'tmppath':
            res.update({'path': os.path.join(os.getcwd(), 'tmp', '')})
        else:
            uid = res['id'] = cmd['id']
            task = running_commands.get(uid)
            if task is None:
                return {'id': uid, 'type': 'error', 'text': 'Задача с запрошенным идентификатором не существует'}

            task.updateTime()
            if cmd['type'] == 'progress':
                res.update({'progress': task.progress, 'ready': task.ready})
            elif cmd['type'] == 'data':
                if task.error: return {'id': uid, 'type': 'error', 'text': task.error}
                res.update({'data': task.data, 'files': task.files})
                res.update({'path': os.path.join(os.getcwd(), 'tmp', '')})
            elif cmd['type'] == 'kill':
                del running_commands[uid]
                task.kill()
            elif cmd['type'] == 'stop':
                task.stop()
            elif cmd['type'] == 'keep':
                pass
            

    except Exception as e:
        return {'id': 0, 'type': 'error', 'text': str(e)}
    return res

def procedure_proc():
    while True:
        task = commands_queue.get()
        if task is None: break
        task.run()
        
        
threads = []


def test_handler(task, timeout = 10.0):
    t = 0.0

    f = task.open('blablabla', 'w')

    while t < timeout:
        time.sleep(0.1)
        t += 0.1

        task.setProgress(t / timeout)
        if task.checkBreak(): break

remove_thread = None

def remove_proc():
    while run_status:
        time.sleep(1)
        del_keys = []
        for key, task in running_commands.items():
            if time.time() > task.last_time + task.end_timeout:
                del_keys.append(key)
                task.kill()
        for key in del_keys:
            del running_commands[key]

def start():
    global cmd_handlers
    global remove_thread
    global run_status

    if not os.path.exists('tmp'): os.mkdir('tmp')
    tmp_files = os.listdir('tmp/')
    for filename in tmp_files:
        try:
            os.remove('tmp/'+filename)
        except Exception: pass
    '''
    import cmd_check_statistics
    import cmd_report
    import cmd_report_condition
    import cmd_stend_versions
    import cmd_stend_versions_log
    import cmd_fail_statistics
    import cmd_erased
    cmd_handlers['test'] = test_handler
    cmd_handlers['check_statistics'] = cmd_check_statistics.check_statistics
    cmd_handlers['fail_statistics'] = cmd_fail_statistics.fail_statistics
    cmd_handlers['report'] = cmd_report.report
    cmd_handlers['report_condition'] = cmd_report_condition.report_condition
    cmd_handlers['stend_versions'] = cmd_stend_versions.stend_versions
    cmd_handlers['stend_versions_log'] = cmd_stend_versions_log.stend_versions_log
    cmd_handlers['erased'] = cmd_erased.erased_devices'''

    import importlib.util

    
    cmd_files = os.listdir()
    for file in cmd_files:
        if file[:3] == 'cmd' and file[-3:] == '.py':
            module_name = file[4:-3]
            spec = importlib.util.spec_from_file_location(module_name, file)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            cmd_list = getattr(m, 'method_list', [])
            for cmd in cmd_list:
                cmd_handlers[cmd] = getattr(m, cmd, None)
            def_cmd = getattr(m, module_name, None)
            if def_cmd: cmd_handlers[module_name] = def_cmd

    run_status = True
    remove_thread = threading.Thread(target=remove_proc, name='remove_thread')
    remove_thread.start()

    for i in range(THREAD_COUNT):
        th = threading.Thread(target=procedure_proc, name='procedure_thread_{}'.format(i))
        th.start()
        threads.append(th)

    

def stop():
    global run_status
    run_status = False

    for task in running_commands.values():
        task.kill()
    running_commands.clear()

    try:
        while True:
            commands_queue.get_nowait()
    except queue.Empty: pass

    for i in range(len(threads)):
        commands_queue.put(None)

    if remove_thread: remove_thread.join()
    for th in threads:
        th.join()