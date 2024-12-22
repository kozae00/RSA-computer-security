from src.utils.crypto import CryptoUtils
from src.utils.network import NetworkUtils
import threading
import socket
from Crypto.PublicKey import RSA

class ChatClient:
    def __init__(self, username):
        self.username = username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.private_key = None
        self.public_key = None
        self.ca_public_key = None
        self.peer_public_key = None
    
    def connect_to_server(self, host='localhost', port=5000):
        """서버 연결 및 키 수신"""
        try:
            print(f"서버에 연결 시도 중...")
            self.socket.connect((host, port))
            print(f"서버 연결 성공!")
            
            print(f"{self.username}으로 서버에 등록 중...")
            NetworkUtils.send_data(self.socket, self.username)
            
            print("키 정보 수신 대기 중...")
            # 키 수신
            key_data = NetworkUtils.receive_data(self.socket)
            self.private_key = RSA.import_key(key_data['private_key'])
            self.public_key = RSA.import_key(key_data['public_key'])
            self.ca_public_key = RSA.import_key(key_data['ca_public_key'])
            print("키 정보 수신 완료!")
            
            print("상대방 접속 대기 중...")
            # 피어 정보 수신
            peer_data = NetworkUtils.receive_data(self.socket)
            peer_public_key = RSA.import_key(peer_data['peer_public_key'])
            
            # 서명 검증
            if CryptoUtils.verify_signature(
                self.ca_public_key,
                peer_data['peer_public_key'],
                peer_data['peer_key_signature']
            ):
                print(f"피어 {peer_data['peer_username']}의 공개키가 확인되었습니다.")
                self.peer_public_key = peer_public_key
                print("\n채팅이 준비되었습니다. 메시지를 입력하세요:")
            else:
                raise Exception("피어의 공개키 검증에 실패했습니다.")
                
        except Exception as e:
            print(f"연결 중 오류 발생: {e}")
            raise e
    
    def send_message(self, message):
        """메시지 전송"""
        print(f"\n[{self.username}의 메시지 전송]")
        print(f"상대방의 공개키로 암호화를 시작합니다.")
        encrypted_message = CryptoUtils.encrypt_message(self.peer_public_key, message)
        self.socket.send(encrypted_message)

    def receive_messages(self):
        """메시지 수신"""
        while True:
            try:
                encrypted_message = self.socket.recv(4096)
                if not encrypted_message:
                    break
                print(f"\n[{self.username}의 메시지 수신]")
                print(f"개인키로 복호화를 시작합니다.")
                message = CryptoUtils.decrypt_message(self.private_key, encrypted_message)
                print(f"\n받은 메시지: {message}")
            except Exception as e:
                print(f"메시지 수신 중 오류 발생: {e}")
                break    
    def start(self):
        """채팅 클라이언트 시작"""
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        print("\n메시지를 입력하세요 (종료하려면 'quit' 입력):")
        while True:
            try:
                message = input(f"{self.username}> ")
                if message.lower() == 'quit':
                    break
                self.send_message(message)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"메시지 전송 중 오류 발생: {e}")
                break
        
        self.socket.close()