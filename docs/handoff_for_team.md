# 팀 인수인계 문서

## 현재 브랜치

- `a-foundation`

## 클론 및 실행 방법

```bash
git clone <repository-url>
cd 26_1_teamwork
python3 main.py
```

프로그램을 실행하면 매번 사용자 이름을 입력합니다. 네 명의 시연자는 각각 다른 터미널에서 `python3 main.py`를 실행하면 됩니다.

## 현재 A 파트 완료 상태

A 파트는 MVC 기본 구조, 핵심 Model, Controller 흐름, StorageService 인터페이스, LocalStorageService JSON 저장/불러오기 기반을 구현했습니다.

현재 가능한 기능:

- 방 만들기
- 방 참여
- 방 입장
- 메뉴 추가/편집/삭제
- 채팅 입력
- 방장만 완료 처리
- 완료된 방 복제
- 총액 및 1인당 금액 계산
- `local_storage.json`을 통한 임시 저장/불러오기

## B 파트: Google Sheet 저장/불러오기

B는 `services/google_sheet_service.py`를 구현합니다.

주요 작업:

- Google Sheet에서 방, 참여자, 메뉴, 채팅 데이터를 불러오기
- 프로그램의 Room 객체 목록을 Google Sheet에 저장하기
- Controller가 사용하는 `load_rooms()`와 `save_rooms(rooms)` 인터페이스 유지하기

## C 파트: CUI, 보고서, 스크린샷

C는 화면 구성과 제출 자료를 담당합니다.

주요 작업:

- `views/console_view.py`의 CUI 개선
- 3초 새로고침 화면 표현 개선
- 기능별 스크린샷과 설명 작성
- 보고서 완성
- 최종 화면 녹화 준비

## 주로 수정할 파일

- A: `controllers/party_controller.py`, `models/`, `services/storage_service.py`, `services/local_storage_service.py`
- B: `services/google_sheet_service.py`, 필요한 설정 문서
- C: `views/console_view.py`, `docs/report.md`, `screenshots/`

## 가능하면 수정하지 말 파일

- B는 Model 구조와 Controller 흐름을 불필요하게 바꾸지 않습니다.
- C는 Model의 비즈니스 로직과 StorageService 인터페이스를 바꾸지 않습니다.
- A/B/C 모두 다른 팀원의 담당 파일은 꼭 필요할 때만 상의 후 수정합니다.

## 최종 화면 녹화 요구사항

최종 녹화는 한 화면에 네 개의 터미널을 띄우고 진행합니다.

- 터미널 1: `김연세`
- 터미널 2: `Lan`
- 터미널 3: `신동해`
- 터미널 4: `Nuoran`

네 터미널 모두 `python3 main.py`를 실행하여 같은 방 목록과 상태 변화를 확인할 수 있어야 합니다.

## GitHub에 올리면 안 되는 파일

다음 파일은 절대 GitHub에 push하지 않습니다.

- `credentials.json`
- `service_account.json`
- `.env`
- `local_storage.json`

필요하면 `.gitignore`에 추가합니다.
