import psutil


def get_network_data():
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
    return networks_list
