# Meal Party Recruitment System

### 2. Google Sheets Configuration

To configure Google Sheets, please prepare the following:

*   Google Sheet ID
*   Service Account Credential File

Example:

```bash
export GOOGLE_SHEET_ID="YOUR_SHEET_ID"
export GOOGLE_CREDENTIALS_PATH="service_account.json"
```

### 3. Program Execution

To execute the program, run the following command:

```bash
python3 main.py
```

---

## Testing Scenarios

The final testing involved four users:

*   YING LAN
*   신동해
*   WEN NUORAN
*   김연세

The following functionalities were verified:

*   Room creation
*   Room participation
*   Menu management
*   Chat messaging
*   Recruitment completion
*   Cost calculation
*   Room duplication
*   Google Sheets save/load capabilities

---

## Important Notes

For security purposes, private files such as `service_account.json`, `credentials.json`, and `local_storage.json` are not included in the submission package. Users are required to provide their own Google Sheets credentials prior to project execution.
