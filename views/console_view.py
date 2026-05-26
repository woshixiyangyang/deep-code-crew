from utils.screen import clear_screen


class ConsoleView:
    # TODO(C): Improve final CUI layout, refresh presentation, screenshots, and recording flow.
    def show_main_menu(self, user_name):
        clear_screen()
        print("식사 파티 모집")
        print("==============")
        print("A: YING LAN (2023106179)")
        print("Role: A - Controller and core Model structure")
        print(f"사용자: {user_name}")
        print()
        print("1. 방 만들기")
        print("2. 방 참여")
        print("3. 방 입장 / 메뉴 편집")
        print("4. 완료된 방 복제")
        print("0. 종료")
        print()

    def show_room_list(self, rooms):
        clear_screen()
        print("방 목록")
        print("=======")
        if not rooms:
            print("아직 방이 없습니다.")
            return

        for room in rooms:
            print(
                f"[{room.room_id}] {room.title} | 방장: {room.host_name} | "
                f"{len(room.members)}/{room.target_people} | "
                f"[{room.status}] | {room.order_type} | "
                f"마감: {room.deadline_minutes}분 후"
            )

    def show_room_detail(self, room):
        clear_screen()
        print(f"방 #{room.room_id}: {room.title}")
        print("=" * (len(room.title) + 10))
        print(f"상태: {room.status}")
        print(f"방장: {room.host_name}")
        print(f"참여자: {', '.join(room.members)}")
        print(f"목표 인원: {room.target_people}")
        print(f"최대 인원: {room.max_people}")
        print(f"식사 형태: {room.order_type}")
        print(f"마감 시간: {room.deadline_minutes}분 후")
        print(f"식사 시간: {room.meal_time}")
        print(f"총액: {room.total_price()}")
        print(f"1인당 금액: {room.split_payment()}")
        print()
        print("메뉴 목록")
        if not room.menu_items:
            print("- 메뉴가 없습니다.")
        for item in room.menu_items:
            print(f"- #{item.item_id} {item.name}: {item.price} x {item.quantity}")
        print()
        print("채팅")
        if not room.chat_messages:
            print("- 채팅이 없습니다.")
        for message in room.chat_messages[-10:]:
            print(f"- [{message.created_at}] {message.sender_name}: {message.message}")
        print()
        print("1. 메뉴 추가")
        print("2. 메뉴 편집")
        print("3. 메뉴 삭제")
        print("4. 채팅 입력")
        print("5. 완료")
        print("6. 나가기")
        print()

    def prompt(self, message):
        return input(message)

    def prompt_required(self, message):
        while True:
            value = self.prompt(message).strip()
            if value:
                return value
            self.show_error("값을 비워둘 수 없습니다.")

    def prompt_int(self, message, minimum=None):
        while True:
            raw_value = self.prompt(message).strip()
            try:
                value = int(raw_value)
            except ValueError:
                self.show_error("숫자를 입력해 주세요.")
                continue

            if minimum is not None and value < minimum:
                self.show_error(f"{minimum} 이상의 숫자를 입력해 주세요.")
                continue
            return value

    def prompt_yes_no(self, message):
        while True:
            value = self.prompt(message).strip().lower()
            if value == "y":
                return True
            if value == "n":
                return False
            self.show_error("Y 또는 N을 입력해 주세요.")

    def prompt_with_default(self, label, default_value):
        raw_value = self.prompt(f"{label} [{default_value}]: ").strip()
        if raw_value:
            return raw_value
        return default_value

    def prompt_int_with_default(self, label, default_value, minimum=None):
        while True:
            raw_value = self.prompt(f"{label} [{default_value}]: ").strip()
            if not raw_value:
                return default_value
            try:
                value = int(raw_value)
            except ValueError:
                self.show_error("숫자를 입력해 주세요.")
                continue
            if minimum is not None and value < minimum:
                self.show_error(f"{minimum} 이상의 숫자를 입력해 주세요.")
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
                self.show_error(f"숫자가 아닌 번호는 무시했습니다: {part}")
        return item_ids

    def show_message(self, message):
        print()
        print(message)

    def show_error(self, message):
        print()
        print(f"오류: {message}")

    def pause(self):
        input("계속하려면 Enter를 누르세요...")
