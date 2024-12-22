from src.utils.crypto import CryptoUtils
from src.utils.network import NetworkUtils
import threading
import socket  

class CertificationAuthority:
    def __init__(self):
        self.private_key, self.public_key = CryptoUtils.generate_key_pair()
        self.clients = {}  # {username: (connection, public_key)}
    
    def handle_client(self, conn, addr):
        """클라이언트 연결 처리"""
        try:
            # 사용자 등록
            username = NetworkUtils.receive_data(conn)
            priv_key, pub_key = CryptoUtils.generate_key_pair()
            
            # 키 전송
            key_data = {
                'private_key': priv_key.export_key(),
                'public_key': pub_key.export_key(),
                'ca_public_key': self.public_key.export_key()
            }
            NetworkUtils.send_data(conn, key_data)
            
            self.clients[username] = (conn, pub_key)
            
            # 다른 사용자가 접속할 때까지 대기
            while len(self.clients) < 2:
                pass
            
            # 상대방 정보 전송
            for other_username, (other_conn, other_pub_key) in self.clients.items():
                if other_username != username:
                    peer_data = {
                        'peer_username': other_username,
                        'peer_public_key': other_pub_key.export_key(),
                        'peer_key_signature': CryptoUtils.sign_key(self.private_key, other_pub_key)
                    }
                    NetworkUtils.send_data(conn, peer_data)
                    break
            
            # 메시지 중계
            while True:
                encrypted_msg = conn.recv(4096)
                if not encrypted_msg:
                    break
                
                # 다른 모든 클라이언트에게 전달
                for other_username, (other_conn, _) in self.clients.items():
                    if other_username != username:
                        other_conn.send(encrypted_msg)
        
        except Exception as e:
            print(f"클라이언트 처리 중 오류 발생: {e}")
        finally:
            if username in self.clients:
                del self.clients[username]
            conn.close()
    
    def start(self, host='localhost', port=5000):
        """서버 시작"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()
        
        print(f"인증기관 서버가 {host}:{port}에서 시작되었습니다.")
        
        while True:
            try:
                conn, addr = server.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
            except Exception as e:
                print(f"연결 수락 중 오류 발생: {e}")
