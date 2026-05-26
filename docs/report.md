# Meal Party Recruitment CUI Report

## Project Summary

This project is a Python CUI program for recruiting meal party members. It follows MVC architecture and will use Google Sheets as final persistent storage.

## Program Structure

- `models/`: data classes and business state.
- `views/`: console display and raw input.
- `controllers/`: program flow and validation coordination.
- `services/`: storage interfaces and implementations.
- `utils/`: shared helper functions.

## Main Algorithms

- Room status: the room starts as `모집중`; when remaining seats are within 10 percent of target people, it becomes `마감임박`; when the host completes it, it becomes `완료`.
- Join validation: the model rejects completed rooms, duplicate users, and rooms that reached target people.
- Split payment: total menu price is divided by member count using `math.ceil`.
- Clone room: a completed room can create a new room with default copied values and selected old menu items.

## Class Design

- `User`: stores the current user's name.
- `Room`: stores room data and core rules for joining, status, menu, chat, completion, payment, and cloning.
- `MenuItem`: stores item id, name, price, and quantity.
- `ChatMessage`: stores sender, message text, and created time.
- `PartyController`: coordinates user flow.
- `StorageService`: defines the storage interface.
- `LocalStorageService`: stores current test data in JSON.
- `GoogleSheetService`: placeholder for final Google Sheets storage.

## Demo Scenario

The final recording will run four terminals with different users and demonstrate room creation, joining, refresh, invalid input handling, menu changes, chat, completion, split payment, cloning, and restart persistence.
