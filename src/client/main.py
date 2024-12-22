from src.client.chat_client import ChatClient
import sys

def main():
    if len(sys.argv) != 2:
        print("사용법: python main.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    client = ChatClient(username)
    
    try:
        client.connect_to_server()
        print(f"{username}으로 접속했습니다.")
        client.start()
    except KeyboardInterrupt:
        print("\n클라이언트를 종료합니다.")
    except Exception as e:
        print(f"클라이언트 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    main()