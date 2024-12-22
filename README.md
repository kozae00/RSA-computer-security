# RSA 기반 PKI 채팅 프로그램

## 프로그램 개요
이 프로그램은 PKI(Public Key Infrastructure) 기반의 암호화된 양자간 채팅 시스템입니다. RSA 암호화를 사용하여 안전한 메시지 교환을 구현했습니다.

## 주요 기능
1. 인증기관(서버) 기능
   - 자체 공개키/개인키 생성 및 관리
   - 클라이언트 키쌍 생성 및 배포
   - 공개키 인증을 위한 디지털 서명
   - 클라이언트 간 메시지 중계

2. 클라이언트 기능
   - 서버로부터 안전한 키 수신
   - 상대방 공개키 검증
   - RSA 암호화/복호화를 통한 메시지 송수신

## 시스템 요구사항
- Python 3.x
- pycryptodome 라이브러리

## 설치 방법
1. 저장소 클론
```bash
git clone https://github.com/your-username/RSA-computer-security.git
cd RSA-computer-security
```

2. 가상환경 생성 및 활성화
```bash
python -m venv myvenv
# Windows
.\myvenv\Scripts\activate
# Linux/Mac
source myvenv/bin/activate
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

## 실행 방법
1. 서버 실행 (첫 번째 터미널)
```bash
python -m src.server.main
```

2. Alice 클라이언트 실행 (두 번째 터미널)
```bash
python -m src.client.main Alice
```

3. Bob 클라이언트 실행 (세 번째 터미널)
```bash
python -m src.client.main Bob
```

## PKI 기반 통신 과정
1. 서버 초기화
   - 인증기관 서버가 자신의 공개키/개인키 쌍을 생성

2. 클라이언트 등록
   - 클라이언트(Alice/Bob)가 서버에 접속
   - 서버가 각 클라이언트를 위한 키쌍 생성
   - 생성된 키쌍을 해당 클라이언트에게 전달

3. 상호 인증
   - 서버가 각 클라이언트에게 상대방의 공개키와 서명을 전달
   - 클라이언트들이 서버의 공개키로 상대방 공개키의 유효성 검증

4. 암호화 통신
   - 메시지 송신 시: 상대방의 공개키로 암호화
   - 메시지 수신 시: 자신의 개인키로 복호화

## 프로젝트 구조
```
RSA-computer-security/
├── src/
│   ├── __init__.py
│   ├── server/
│   │   ├── __init__.py
│   │   ├── certification_authority.py
│   │   └── main.py
│   ├── client/
│   │   ├── __init__.py
│   │   ├── chat_client.py
│   │   └── main.py
│   └── utils/
│       ├── __init__.py
│       ├── crypto.py
│       └── network.py
└── tests/
    ├── __init__.py
    ├── test_crypto.py
    └── test_network.py
```

## 종료 방법
- 서버 종료: `Ctrl + C`
- 클라이언트 종료: `quit` 입력 또는 `Ctrl + C`

## 보안 특징
- RSA 2048비트 키 사용
- 인증기관을 통한 공개키 인증
- 종단간 암호화 통신
- 중간자 공격 방지를 위한 키 검증

## 주의사항
- 서버는 클라이언트보다 먼저 실행되어야 합니다
- 두 클라이언트가 모두 접속해야 채팅이 가능합니다
- 실제 운영 환경에서는 추가적인 보안 조치가 필요할 수 있습니다

## License
MIT License