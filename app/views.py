from django.shortcuts import render
import psutil

# Create your views here.


def index(request):
    return render(request, 'app/index.html')


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
