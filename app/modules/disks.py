import psutil


def get_storage_data():
    disk_list = []
    disks = psutil.disk_partitions()
    for d in disks:
        disk = {
            'device': d.device,
            'mountpoint': d.mountpoint,
            'fstype': d.fstype,
            'options': d.opts,
            'memory_total': psutil.disk_usage(path=str(d.mountpoint)).total // 1048576 // 1024,
            'memory_used': psutil.disk_usage(path=str(d.mountpoint)).used // 1048576 // 1024,
            'memory_free': psutil.disk_usage(path=str(d.mountpoint)).free // 1048576 // 1024,
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
    return disk_list
