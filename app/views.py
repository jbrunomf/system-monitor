from django.shortcuts import render
import psutil
from django.core.paginator import Paginator

from .modules.network import get_network_data
from .modules.disks import get_storage_data
from .modules.process import get_process_info

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
            'status': get_network_data()
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
                   'memory_info_rss': p.memory_info().rss // 1048576,
                   'memory_info_vms': p.memory_info().vms // 1048576,
                   }

        process_list.append(process)
    paginator = Paginator(process_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/list.html', {'page_obj': page_obj})


def process(request, pid):
    context = {'process': get_process_info(pid)}
    return render(request, 'app/detail.html', context)


def disks(request):
    context = {'disks': get_storage_data()}
    return render(request, 'app/disks.html', context)


def network(request):
    context = {'networks': get_network_data()}
    return render(request, 'app/network.html', context)
