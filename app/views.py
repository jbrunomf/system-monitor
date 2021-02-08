from django.shortcuts import render
import psutil

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
            'total': psutil.virtual_memory().total//1048576,
            'available': psutil.virtual_memory().free//1048576,
            'used': psutil.virtual_memory().used//1048576,
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
            'total': psutil.swap_memory().total//1048576,
            'used': psutil.swap_memory().used//1048576,
            'free': psutil.swap_memory().free//1048576
        },
        'users': psutil.users()[0]


    }
    return render(request, 'app/index.html', ctx)


def processes(request):
    """
    :param request:
    :return:
    """
    ctx = {"processes": psutil.process_iter(['pid', 'name', 'username', 'status', 'memory_percent', 'cpu_percent', 'memory_info'])}
    return render(request, 'app/list.html', ctx)


def process(request, pid):
    ctx = {"process": psutil.Process(pid)}
    return render(request, 'app/detail.html', ctx)
