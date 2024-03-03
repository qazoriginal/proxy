import socket
import time
import datetime

def read_udp_packets(server_host, server_port):
    # Создаем сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
    server_socket.bind((server_host, server_port))

# Устанавливаем таймаут для сокета
    server_socket.settimeout(0.5)  # Таймаут в секундах

# Буфер для хранения полученных пакетов
    packet_buffer = []
    delta = 4.0
    cur = 1.0
    timestamp = 0.0
    try:
        while True:

            try:

                # Читаем UDP-пакет

                data, address = server_socket.recvfrom(8)  # Максимальный размер пакета для чтения
                print('TAKEN DATA ' + str(data))
                packet_buffer.append(data)
                print('CUR BUF:')
                print(packet_buffer)

# Если буфер заполнен, отправляем все пакеты на указанный адрес
                if timestamp < datetime.datetime.now().timestamp():
                    if len(packet_buffer) == 0:
                        pass
                    else:
                        if timestamp != 0.0:
                            send_buffered_packets()
                        else:
                            time.sleep(1)
                            for i in range(0, 3):
                                send_buffered_packets()
                        if len(packet_buffer[0]) == 0:
                            cur = 1.0
                            timestamp = 0.0
                            packet_buffer.pop(0)
                            time.sleep(cur + delta)
                            for i in range(0, 3):
                                send_buffered_packets()

                    if len(packet_buffer) > 0:
                        if len(packet_buffer[0]) > 0:
                            print('first element in packet buffer:')
                            print(packet_buffer[0][0])
                            if packet_buffer[0][0] == 48:
                                timestamp = datetime.datetime.now().timestamp() + cur
                                packet_buffer[0] = packet_buffer[0][1:]
                                print('want to sent 0')
                            else:
                                cur += delta
                                timestamp = datetime.datetime.now().timestamp() + cur
                                packet_buffer[0] = packet_buffer[0][1:]
                                print('want to sent 1')
            except socket.timeout:
                if timestamp < datetime.datetime.now().timestamp():
                    if len(packet_buffer) == 0:
                        pass
                    else:
                        if timestamp != 0.0:
                            send_buffered_packets()
                        if len(packet_buffer[0]) == 0:
                            cur = 1.0
                            timestamp = 0.0
                            packet_buffer.pop(0)
                            for i in range(0, 3):
                                send_buffered_packets()

                    if len(packet_buffer) > 0:
                        if timestamp == 0.0:
                            for i in range(0, 3):
                                send_buffered_packets()
                        if len(packet_buffer[0]) > 0:
                            print('first element in packet buffer:')
                            print(packet_buffer[0][0])
                            if packet_buffer[0][0] == 48:
                                timestamp = datetime.datetime.now().timestamp() + cur
                                packet_buffer[0] = packet_buffer[0][1:]
                                print('want to sent 0')
                            else:
                                cur += delta
                                timestamp = datetime.datetime.now().timestamp() + cur
                                packet_buffer[0] = packet_buffer[0][1:]
                                print('want to sent 1')
            time.sleep(0.1)  # Например, 0.1 секунды
    except KeyboardInterrupt:
        print("Прервано пользователем")

def send_buffered_packets():
    # Отправка пакетов из буфера на указанный адрес

    destination_address = ('10.111.0.1', 12345)  # Пример адреса и порта
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(b'0' * 8, destination_address)

    client_socket.close()

if __name__ == "__main__":
    # Адрес и порт сервера для приема UDP-пакетов

    server_host = '10.111.0.10'
    server_port = 12344

    read_udp_packets(server_host, server_port)
