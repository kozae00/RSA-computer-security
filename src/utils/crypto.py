from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class CryptoUtils:
    @staticmethod
    def generate_key_pair():
        """RSA 키쌍 생성"""
        key = RSA.generate(2048)
        return key, key.publickey()
    
    @staticmethod
    def sign_key(private_key, public_key):
        """공개키 서명"""
        key_hash = SHA256.new(public_key.export_key())
        signature = pkcs1_15.new(private_key).sign(key_hash)
        return signature
    
    @staticmethod
    def verify_signature(ca_public_key, public_key, signature):
        """서명 검증"""
        try:
            key_hash = SHA256.new(public_key)
            pkcs1_15.new(ca_public_key).verify(key_hash, signature)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def encrypt_message(public_key, message):
        """메시지 암호화"""
        print(f"\n[암호화 과정]")
        print(f"원본 메시지: {message}")
        cipher = PKCS1_OAEP.new(public_key)
        encrypted = cipher.encrypt(message.encode())
        print(f"암호화된 메시지: {encrypted.hex()}")  # 16진수로 출력
        return encrypted
    
    @staticmethod
    def decrypt_message(private_key, encrypted_message):
        """메시지 복호화"""
        print(f"\n[복호화 과정]")
        print(f"수신된 암호화 메시지: {encrypted_message.hex()}")  # 16진수로 출력
        cipher = PKCS1_OAEP.new(private_key)
        decrypted = cipher.decrypt(encrypted_message).decode()
        print(f"복호화된 메시지: {decrypted}")
        return decrypted