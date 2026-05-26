from models.room import Room, STATUS_COMPLETED
from models.user import User

# A identity: YING LAN / 2023106179 / A - Controller and core Model structure


class PartyController:
    def __init__(self, view, storage_service):
        self.view = view
        self.storage_service = storage_service
        self.current_user = User("")
        self.rooms = self.storage_service.load_rooms()

    def run(self):
        self.set_user_name()

        while True:
            self.view.show_main_menu(self.current_user.name)
            choice = self.view.prompt("메뉴 선택: ").strip()

            if choice == "1":
                self.create_room()
            elif choice == "2":
                self.join_room()
            elif choice == "3":
                self.enter_room()
            elif choice == "4":
                self.clone_completed_room()
            elif choice == "0":
                self.save_rooms()
                self.view.show_message("저장했습니다. 프로그램을 종료합니다.")
                break
            else:
                self.view.show_error("잘못된 입력입니다. 0-4 중에서 선택하세요.")

            self.view.pause()

    def set_user_name(self):
        while True:
            name = self.view.prompt("사용자 이름을 입력하세요: ").strip()
            if name:
                self.current_user = User(name)
                return
            self.view.show_error("이름을 비워둘 수 없습니다.")

    def show_rooms(self):
        self.refresh_rooms()
        self.view.show_room_list(self.rooms)

    def create_room(self):
        title = self.view.prompt_required("식당명: ")
        target_people = self.view.prompt_int("목표 인원: ", minimum=1)
        use_max_people = self.view.prompt_yes_no("최대 인원 설정하시겠습니까? (Y/N): ")
        if use_max_people:
            max_people = self.view.prompt_int("최대 인원: ", minimum=target_people)
        else:
            max_people = target_people
        order_type = self.prompt_order_type()
        deadline_minutes = self.view.prompt_int("마감 시간 (현재로부터 몇 분): ", minimum=1)
        meal_time = self.view.prompt_required("식사 시간 (예: 12:30): ")

        room = Room(
            room_id=self.next_room_id(),
            title=title,
            host_name=self.current_user.name,
            target_people=target_people,
            max_people=max_people,
            order_type=order_type,
            deadline_minutes=deadline_minutes,
            meal_time=meal_time,
        )
        self.rooms.append(room)
        self.save_rooms()
        self.view.show_message(f"방 #{room.room_id}을 만들었습니다.")

    def prompt_order_type(self):
        valid_order_types = ["매장", "포장", "배달"]
        while True:
            order_type = self.view.prompt_required("식사 형태 (매장/포장/배달): ")
            if order_type in valid_order_types:
                return order_type
            self.view.show_error("식사 형태는 매장, 포장, 배달 중 하나여야 합니다.")

    def join_room(self):
        self.refresh_rooms()
        self.view.show_room_list(self.rooms)
        room = self.select_room("참여할 방 번호: ")
        if room is None:
            return

        success, message = room.join(self.current_user.name)
        if success:
            self.save_rooms()
            self.view.show_message(message)
        else:
            self.view.show_error(message)

    def enter_room(self):
        self.refresh_rooms()
        self.view.show_room_list(self.rooms)
        room = self.select_room("입장할 방 번호: ")
        if room is None:
            return
        if self.current_user.name not in room.members:
            self.view.show_error("방에 먼저 참여해야 입장할 수 있습니다.")
            return

        while True:
            self.view.show_room_detail(room)
            choice = self.view.prompt("메뉴 선택: ").strip()

            if choice == "1":
                self.add_menu_item(room)
            elif choice == "2":
                self.edit_menu_item(room)
            elif choice == "3":
                self.delete_menu_item(room)
            elif choice == "4":
                self.add_chat_message(room)
            elif choice == "5":
                self.complete_room(room)
            elif choice == "6":
                self.save_rooms()
                break
            else:
                self.view.show_error("잘못된 입력입니다. 1-6 중에서 선택하세요.")
                self.view.pause()

    def add_menu_item(self, room):
        name = self.view.prompt_required("메뉴 이름: ")
        price = self.view.prompt_int("가격: ", minimum=0)
        quantity = self.view.prompt_int("수량: ", minimum=1)
        item_id = room.add_menu_item(name, price, quantity)
        self.save_rooms()
        self.view.show_message(f"메뉴 #{item_id}을 추가했습니다.")
        self.view.pause()

    def edit_menu_item(self, room):
        item_id = self.view.prompt_int("편집할 메뉴 번호: ", minimum=1)
        if room.find_menu_item(item_id) is None:
            self.view.show_error("존재하지 않는 메뉴 번호입니다.")
            self.view.pause()
            return

        name = self.view.prompt_required("새 메뉴 이름: ")
        price = self.view.prompt_int("새 가격: ", minimum=0)
        quantity = self.view.prompt_int("새 수량: ", minimum=1)
        success, message = room.edit_menu_item(item_id, name, price, quantity)
        self._show_result(success, message)
        self.save_rooms()
        self.view.pause()

    def delete_menu_item(self, room):
        item_id = self.view.prompt_int("삭제할 메뉴 번호: ", minimum=1)
        success, message = room.delete_menu_item(item_id)
        self._show_result(success, message)
        self.save_rooms()
        self.view.pause()

    def add_chat_message(self, room):
        message = self.view.prompt_required("채팅 내용: ")
        room.add_chat_message(self.current_user.name, message)
        self.save_rooms()
        self.view.show_message("채팅을 입력했습니다.")
        self.view.pause()

    def complete_room(self, room):
        success, message = room.complete(self.current_user.name)
        self._show_result(success, message)
        if success:
            self.save_rooms()
        self.view.pause()

    def clone_completed_room(self):
        self.refresh_rooms()
        self.view.show_room_list(self.rooms)
        room = self.select_room("복제할 완료된 방 번호: ")
        if room is None:
            return
        if room.status != STATUS_COMPLETED:
            self.view.show_error("완료된 방만 복제할 수 있습니다.")
            return

        title = self.view.prompt_with_default("새 식당명", room.title)
        target_people = self.view.prompt_int_with_default("목표 인원", room.target_people, minimum=1)
        max_people = self.view.prompt_int_with_default("최대 인원", room.max_people, minimum=target_people)
        order_type = self.view.prompt_with_default("식사 형태", room.order_type)
        deadline_minutes = self.view.prompt_int_with_default(
            "마감 시간", room.deadline_minutes, minimum=1
        )
        meal_time = self.view.prompt_with_default("식사 시간", room.meal_time)
        menu_item_ids = self.view.prompt_id_list(
            "복사할 메뉴 번호를 쉼표로 입력하세요 (없으면 Enter): "
        )

        new_room = room.clone(
            new_room_id=self.next_room_id(),
            host_name=self.current_user.name,
            title=title,
            target_people=target_people,
            max_people=max_people,
            order_type=order_type,
            deadline_minutes=deadline_minutes,
            meal_time=meal_time,
            menu_item_ids=menu_item_ids,
        )
        self.rooms.append(new_room)
        self.save_rooms()
        self.view.show_message(f"방 #{new_room.room_id}으로 복제했습니다.")

    def refresh_rooms(self):
        self.rooms = self.storage_service.load_rooms()

    def save_rooms(self):
        self.storage_service.save_rooms(self.rooms)

    def select_room(self, prompt_text):
        room_id = self.view.prompt_int(prompt_text, minimum=1)
        room = self.find_room(room_id)
        if room is None:
            self.view.show_error("존재하지 않는 방 번호입니다.")
        return room

    def find_room(self, room_id):
        for room in self.rooms:
            if room.room_id == room_id:
                return room
        return None

    def next_room_id(self):
        if not self.rooms:
            return 1
        return max(room.room_id for room in self.rooms) + 1

    def _show_result(self, success, message):
        if success:
            self.view.show_message(message)
        else:
            self.view.show_error(message)
