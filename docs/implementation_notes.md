# Implementation Notes

## Architecture

The project follows MVC with a small service layer.

- `models/`: business objects and logic. These files do not use `print()` or `input()`.
- `views/`: console output and raw input.
- `controllers/`: user flow and coordination between models, views, and services.
- `services/`: persistence interface and storage implementations.
- `utils/`: shared helpers such as clear screen.

## A-Side Features Implemented

- First-run user name setup through the controller and view.
- Room creation with title, target people, order type, deadline minutes, and meal time.
- Join validation for duplicate users, completed rooms, and max people.
- Room status updates from `모집중` to `마감임박` when remaining seats are within 10 percent of target people.
- Room entry for joined members.
- Menu add, edit, and delete.
- Chat message storage with timestamps.
- Host-only room completion.
- Split payment using `math.ceil`.
- Clone completed room with default values and selected menu items.
- JSON save/load through `LocalStorageService`.

## Storage Interface

The controller depends on these methods:

- `load_rooms()`
- `save_rooms(rooms)`
- `load_user_name()`
- `save_user_name(user_name)`

B should keep `load_rooms()` and `save_rooms(rooms)` compatible when implementing Google Sheets. User name storage can remain local per terminal if the team prefers.

## Current Limitations

- The CUI is intentionally minimal and should be improved by C.
- The 3-second refresh requirement is not fully implemented yet; the current controller reloads rooms before room-list actions and room selection.
- Google Sheets is a placeholder and does not save data yet.
- There are no automated tests yet, but model logic is written so tests can be added easily.
