import socket
import pickle
import threading

class NetworkUtils:
    @staticmethod
    def send_data(sock, data):
        """직렬화된 데이터 전송"""
        serialized_data = pickle.dumps(data)
        sock.send(serialized_data)
    
    @staticmethod
    def receive_data(sock, buffer_size=4096):
        """직렬화된 데이터 수신"""
        data = sock.recv(buffer_size)
        return pickle.loads(data)