# Google Sheets 설정 방법

초기 제출 draft는 Google Sheets 저장소를 사용할 수 있습니다. 로컬 테스트만 할 때는 설정하지 않아도 `LocalStorageService`로 실행됩니다.

## 1. 패키지 설치

```bash
python3 -m pip install -r requirements.txt
```

## 2. 환경 변수 설정

```bash
export GOOGLE_SHEET_ID="1kLZg0xS68mPHyn4GdiM2JhBL141LlkQaDVbwQH6PZak"
export GOOGLE_CREDENTIALS_PATH="service_account.json"
```

`GOOGLE_CREDENTIALS_PATH`를 생략하면 기본값은 `service_account.json`입니다.

## 3. Google Sheet 공유

서비스 계정 JSON 파일 안의 `client_email` 값을 확인한 뒤, 해당 이메일을 Google Sheet 편집자로 공유합니다.

사용할 Sheet:

```text
https://docs.google.com/spreadsheets/d/1kLZg0xS68mPHyn4GdiM2JhBL141LlkQaDVbwQH6PZak/edit
```

## 4. 실행

```bash
python3 main.py
```

프로그램은 `rooms`, `members`, `menu_items`, `chat_messages` 워크시트를 자동으로 만들고 필요한 헤더를 설정합니다.

## 주의

다음 파일은 GitHub에 올리면 안 됩니다.

- `service_account.json`
- `credentials.json`
- `.env`
- `local_storage.json`
