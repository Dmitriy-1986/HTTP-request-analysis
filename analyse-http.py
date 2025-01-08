import psutil

def get_http_connections():
    connections = psutil.net_connections(kind='inet')  # Сетевые соединения
    http_connections = []

    for conn in connections:
        # Фильтруем только соединения с портами 80 (HTTP) и 443 (HTTPS)
        if conn.status == psutil.CONN_ESTABLISHED and conn.raddr:
            remote_port = conn.raddr.port
            if remote_port in (80, 443):  # HTTP и HTTPS порты
                try:
                    process = psutil.Process(conn.pid)
                    process_info = {
                        'pid': conn.pid,
                        'name': process.name(),
                        'exe': process.exe(), 
                        'local_address': conn.laddr.ip,
                        'local_port': conn.laddr.port,
                        'remote_address': conn.raddr.ip,
                        'remote_port': remote_port
                    }
                    http_connections.append(process_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

    return http_connections

if __name__ == '__main__':
    connections = get_http_connections()
    if connections:
        for conn in connections:
            print(f"Идентификатор процесса: {conn['pid']}, \n" 
                  f"Имя процесса: {conn['name']}, \n"
                  f"Исполнимый файл: {conn['exe']}, \n"
                  f"Локальный IP и Локальный порт: {conn['local_address']}:{conn['local_port']}, \n"
                  f"Удалённый IP и Удалённый порт: {conn['remote_address']}:{conn['remote_port']} \n")
    else:
        print("No HTTP/HTTPS connections found.")
