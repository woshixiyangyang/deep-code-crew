import os
from utils.screen import clear_screen


class ConsoleView:
    def __init__(self):
        self.system_footer = "----------------------------------------------------------\nTeam: Lan (A) | 신동해 (B) | WEN NUORAN (2025106121) (C)"

    def show_main_menu(self, user_name):
        clear_screen()
        print("----------------------------------------------------------")
        print("                 식사 파티 모집 시스템                    ")
        print("----------------------------------------------------------")
        print(" A: YING LAN (2023106179)") 
        print(" B: 신동해 (2023106180)")
        print(" C: WEN NUORAN (2025106121)")
        print(f" 현재 접속 사용자: {user_name} 님")
        print("----------------------------------------------------------")
        print("  1. 새 식사 방 만들기")
        print("  2. 개설된 방 목록 보기 (참여하기)")
        print("  3. 내 방 입장 / 메뉴 및 채팅 편집")
        print("  4. 완료된 과거 방 복제하기")
        print("  0. 프로그램 종료")
        print(self.system_footer)
        print()

    def show_room_list(self, rooms):
        clear_screen()
        print("----------------------------------------------------------")
        print("                 현재 개설된 식사 방 목록                  ")
        print("----------------------------------------------------------")
        
        if not rooms:
            print("\n        현재 개설된 식사 파티가 없습니다.\n")
            print("----------------------------------------------------------")
            return

        for room in rooms:
            status_display = room.status
            if room.status == "모집중":
                status_display = "[모집중]"
            elif room.status == "마감임박":
                status_display = "[마감임박]"
            elif "COMPLETED" in str(room.status).upper() or room.status == "완료":
                status_display = "[완료]"

            print(f" 방 번호: [{room.room_id}] | 식당명: {room.title}")
            print(f" 방장: {room.host_name} | 인원: {len(room.members)}/{room.target_people} 명 (최대: {room.max_people}명)")
            print(f" 상태: {status_display} | 형태: {room.order_type}")
            print(f" 시간: {room.deadline_minutes}분 후 마감 | 식사 예정: {room.meal_time}")
            print("----------------------------------------------------------")

    def show_room_detail(self, room):
        clear_screen()
        status_display = room.status
        if room.status == "모집중":
            status_display = "[모집중]"
        elif room.status == "마감임박":
            status_display = "[마감임박]"
        elif "COMPLETED" in str(room.status).upper() or room.status == "완료":
            status_display = "[완료]"

        print("----------------------------------------------------------")
        print(f" 방 #[{room.room_id}] {room.title} 상세 정보 {status_display}")
        print("----------------------------------------------------------")
        print(f" 방장 : {room.host_name}")
        print(f" 참여자 : {', '.join(room.members)}")
        print(f" 식사 형태 : {room.order_type} | 식사 시간: {room.meal_time}")
        print(f" 모집 목표 : {room.target_people}명 (최대 인원: {room.max_people}명)")
        print(f" 남은 시간 : {room.deadline_minutes}분 후 자동 마감")
        print("----------------------------------------------------------")
        
        print(" [정산 및 결제 현황]")
        print(f"   - 총 주문 금액 : {room.total_price():,} 원")
        print(f"   - 1인당 금액 (올림): {room.split_payment():,} 원")
        print("----------------------------------------------------------")
        
        print(" [주문 메뉴]")
        if not room.menu_items:
            print("   - 등록된 메뉴가 없습니다.")
        else:
            for item in room.menu_items:
                print(f"   #{item.item_id} {item.name} | {item.price:,}원 x {item.quantity}개")
        print("----------------------------------------------------------")
        
        print(" [실시간 대화]")
        if not room.chat_messages:
            print("   - 대화가 없습니다.")
        else:
            for message in room.chat_messages[-10:]:
                print(f"   [{message.created_at}] {message.sender_name}: {message.message}")
        print("----------------------------------------------------------")
        print("  1. 메뉴 추가 | 2. 메뉴 수정 | 3. 메뉴 삭제")
        print("  4. 채팅 입력 | 5. 모집 완료 | 6. 방 나가기")
        print("----------------------------------------------------------")
        print()

    def prompt(self, message):
        cleaned_message = message.replace("메뉴 선택: ", "▶ 메뉴 선택: ")
        cleaned_message = cleaned_message.replace("사용자 이름을 입력하세요: ", "사용자 이름을 입력하세요: ")
        return input(cleaned_message)

    def prompt_required(self, message):
        while True:
            value = self.prompt(message).strip()
            if value:
                return value
            self.show_error("필수 입력 항목입니다.")

    def prompt_int(self, message, minimum=None):
        while True:
            raw_value = self.prompt(message).strip()
            try:
                value = int(raw_value)
            except ValueError:
                self.show_error("올바른 숫자를 입력해 주세요.")
                continue

            if minimum is not None and value < minimum:
                self.show_error(f"{minimum} 이상의 숫자를 입력해야 합니다.")
                continue
            return value

    def prompt_yes_no(self, message):
        while True:
            value = self.prompt(message).strip().lower()
            if value == "y":
                return True
            if value == "n":
                return False
            self.show_error("Y 또는 N으로 입력해 주세요.")

    def prompt_with_default(self, label, default_value):
        raw_value = self.prompt(f" {label} (기본값 [{default_value}]): ").strip()
        if raw_value:
            return raw_value
        return default_value

    def prompt_int_with_default(self, label, default_value, minimum=None):
        while True:
            raw_value = self.prompt(f" {label} (기본값 [{default_value}]): ").strip()
            if not raw_value:
                return default_value
            try:
                value = int(raw_value)
            except ValueError:
                self.show_error("올바른 숫자를 입력해 주세요.")
                continue
            if minimum is not None and value < minimum:
                self.show_error(f"{minimum} 이상의 숫자를 입력해야 합니다.")
                continue
            return value

    def prompt_id_list(self, message):
        raw_value = self.prompt(message).strip()
        if not raw_value:
            return []

        item_ids = []
        for part in raw_value.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                item_ids.append(int(part))
            except ValueError:
                pass
        return item_ids

    def show_message(self, message):
        print(f"\n[안내] {message}")

    def show_error(self, message):
        print(f"\n[오류] {message}")

    def pause(self):
        print()
        input("계속하려면 [Enter] 키를 누르세요...")