import psutil


def get_process_info(pid):
    is_posix = psutil.POSIX

    context = {"process": {
        'name': psutil.Process(pid).name,
        'pid': psutil.Process(pid).pid,
        'parent': psutil.Process(pid).parent,
        'exe': psutil.Process(pid).exe,
        'user': psutil.Process(pid).username,
        # 'gids': psutil.Process(pid).gids,
        # 'uids': psutil.Process(pid).uids,
        # 'terminal': psutil.Process(pid).terminal,
        'status': psutil.Process(pid).status,
        'memory': {
            'rss': psutil.Process(pid).memory_info().rss // 1048576,
            'vms': psutil.Process(pid).memory_info().vms // 1048576,
            # 'shared': psutil.Process(pid).memory_info().shared,
            # 'text': psutil.Process(pid).memory_info().text,
            # 'lib': psutil.Process(pid).memory_info().lib,
            # 'dirty': psutil.Process(pid).memory_info().dirty,
            # 'posix': is_posix,
        }
    }}
    return context
