from django.shortcuts import render
import psutil
from django.core. paginator import Paginator
# Create your views here.


def index(request):
    ctx = {
        'cpu': {
            'load_average': psutil.getloadavg(),
            'cores': psutil.cpu_count(logical=False),
            'threads': psutil.cpu_count(),
            'current_freq': psutil.cpu_freq(),
        },
        'memory': {
            'total': psutil.virtual_memory().total // 1048576,
            'available': psutil.virtual_memory().free // 1048576,
            'used': psutil.virtual_memory().used // 1048576,
            'percent_used': psutil.virtual_memory().percent
        },
        'network': {
            'status': psutil.net_if_addrs()['Loopback Pseudo-Interface 1'][0][1]
        },
        'disk': {
            'mountpoint': psutil.disk_partitions()[0][0],
            'fstype': psutil.disk_partitions()[0][2],

        },
        'swap': {
            'total': psutil.swap_memory().total // 1048576,
            'used': psutil.swap_memory().used // 1048576,
            'free': psutil.swap_memory().free // 1048576
        },
        'users': psutil.users()[0]

    }
    return render(request, 'app/index.html', ctx)


def processes(request):
    """
    :param request:
    :return:
    """
    ps = psutil.process_iter()
    process_list = []
    # Paginador, para limitar o número de objetos que serão exibidos na tela.

    for p in ps:
        process = {'pid': p.pid,
                   'name': p.name(),
                   # 'username': p.username(),
                   'status': p.status(),
                   'memory_percent': float(round(p.memory_percent(), 2)),
                   'cpu_percent': p.cpu_percent(interval=0),
                   'memory_info_rss': p.memory_info().rss//1048576,
                   'memory_info_vms': p.memory_info().vms//1048576,
                   }

        process_list.append(process)
    paginator = Paginator(process_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/list.html', {'page_obj': page_obj})


def process(request, pid):
    ctx = {"process": {
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
            'rss': psutil.Process(pid).memory_info().rss//1048576,
            'vms': psutil.Process(pid).memory_info().vms//1048576,
            # 'shared': psutil.Process(pid).memory_info().shared,
            # 'text': psutil.Process(pid).memory_info().text,
            # 'lib': psutil.Process(pid).memory_info().lib,
            # 'dirty': psutil.Process(pid).memory_info().dirty
        }
    }}
    return render(request, 'app/detail.html', ctx)


def disks(request):
    disk_list = []
    disks = psutil.disk_partitions()
    for d in disks:
        disk = {
            'device': d.device,
            'mountpoint': d.mountpoint,
            'fstype': d.fstype,
            'options': d.opts,
            'memory_total': psutil.disk_usage(path=str(d.mountpoint)).total//1048576//1024,
            'memory_used': psutil.disk_usage(path=str(d.mountpoint)).used//1048576//1024,
            'memory_free': psutil.disk_usage(path=str(d.mountpoint)).free//1048576//1024,
            'io_counter': {
                'read_count': psutil.disk_io_counters().read_count,
                'write_count': psutil.disk_io_counters().write_count,
                'read_bytes': psutil.disk_io_counters().read_bytes,
                'write_bytes': psutil.disk_io_counters().write_bytes,
                'read_time': psutil.disk_io_counters().read_time,
                'write_time': psutil.disk_io_counters().write_time
            }
        }

        disk_list.append(disk)
    ctx = {'disks': disk_list}
    return render(request, 'app/disks.html', ctx)


def network(request):
    net = psutil.net_if_addrs().items()
    net_status = psutil.net_io_counters(pernic=True)
    networks_list = []

    for item in net:
        network = {
            'name': item[0],
            'address': item[1][1][1],
            'bytes_sent': net_status[item[0]].bytes_sent,
            'bytes_rec': net_status[item[0]].bytes_recv,
            'packets_sent': net_status[item[0]].packets_sent,
            'packets_recv': net_status[item[0]].packets_recv,
            'errors_in': net_status[item[0]].errin,
            'errors_out': net_status[item[0]].errout,
            'drop_in': net_status[item[0]].dropin,
            'drop_out': net_status[item[0]].dropout,
        }
        networks_list.append(network)
    ctx = {'networks': networks_list}
    return render(request, 'app/network.html', ctx)
