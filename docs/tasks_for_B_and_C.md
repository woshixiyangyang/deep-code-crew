# Tasks for B and C

## Current A-Side Foundation

Lan's A-side scope now provides the MVC skeleton, core model logic, controller flow, storage interface, and local JSON fallback. The program can run with `python3 main.py` and supports room creation, joining, entering rooms, menu add/edit/delete, chat messages, host-only completion, split payment, cloning completed rooms, and reload through `LocalStorageService`.

## B: Google Sheet Save/Load

Implement `services/google_sheet_service.py` without changing the controller interface.

Required methods:

- `load_rooms()`: read rooms, members, menu items, and chat messages from Google Sheets and return a list of `Room` objects.
- `save_rooms(rooms)`: write all room state back to Google Sheets.

Use the model `to_dict()` and `from_dict()` methods where possible. Keep credentials and sheet IDs out of source code. Use a small config file or environment variables if needed.

Suggested sheet structure:

- `rooms`: room id, title, host, target people, order type, deadline, meal time, status
- `members`: room id, user name
- `menu_items`: room id, item id, name, price, quantity
- `chat_messages`: room id, sender, message, created time

Do not put print or input logic in the service.

## C: View, CUI, Report, Screenshots, Recording

Improve `views/console_view.py` while keeping the same controller-facing methods unless the team agrees on a change.

Required final work:

- Make the CUI easier to read for the four-terminal demo.
- Support clean clear-screen presentation.
- Help demonstrate the 3-second refresh requirement as simply as possible.
- Prepare feature screenshots with operation explanations.
- Complete the final report sections in `docs/report.md`.
- Record the demo using four terminals: `김연세`, `Lan`, `신동해`, and `Nuoran`.

Do not move business rules into the view. The view should display text and receive raw input only.
