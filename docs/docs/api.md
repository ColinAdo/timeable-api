# API Reference

This page provides detailed information about the available API endpoints used in the Automatic Timetable Generation System (ATGS). All responses are in JSON format unless otherwise stated.

---

## 🔐 Base URL

http://127.0.0.1:8000/api/v1/

---

## Upload Excel File

Upload an Excel file containing the timetable source data (unit code, unit name, academic year, year-semester e.g., Y1S1, etc.).

### Endpoints

---

#### Upload Unites endpoint

```POST upload/units/```

##### Request (Form Data)

### Request (Form Data)

| Key  | Value                              |
|------|------------------------------------|
| file | Excel file (.xlsx) with unit data  |

##### Response

```json
{
  "message": "File uploaded successfully.",
  "filename": "uploaded_file.xlsx"
}
```

---

#### Generate timetable endpoint

```POST generate/timetable/```

##### Request Body

```json
{
    "batch_id": "timetable_1234",
    "start_time": "08:00",
    "end_time": "20:30",
    "first_constrain": "12:00", // optional
    "second_constrain": "12:30", // optional
    "duration": 3,
    "prompt": "Let unit AA to start at 5:30 PM" // optional
}
```

##### Response

```json
{
  "message": "Timetable generated successfully"
}
```

---

#### Get generated timetable

```GET timetable/<batch_Id>/```

##### Response

```json
[
    {
        "id": 100,
        "name": "timetable_938212934",
        "unit_code": "BCS 1101",
        "unit_name": "Introduction to programming",
        "day": "Thursday",
        "start_time": "16:00:00",
        "end_time": "19:00:00",
        "lecturer": "Prof Ado",
        "campus": "Limuru",
        "mode_of_study": "Physical",
        "lecture_room": "BR 101",
        "group": "0"
    },
    {
        "id": 101,
        "name": "timetable_938212934",
        "unit_code": "CSC 1102",
        "unit_name": "Discrete Structures I",
        "day": "Monday",
        "start_time": "11:00:00",
        "end_time": "14:00:00",
        "lecturer": "Mrs. Nancy",
        "campus": "Limuru",
        "mode_of_study": "Physical",
        "lecture_room": "BR 102",
        "group": "0"
    },
    '...'
]
```
---

#### Export timetable to email endpoint

```POST export/timetable/```

##### Request (Form Data)

| Key     | Value                               |
|---------|-------------------------------------|
| batch_id| <123454>                            |
| email   | emailadress@gmail.com               |

##### Response

```json
{
  "message": "Timetable sent to your email successfully.",
}
```

---

#### Subscription endpoint

```POST subscribe/```

##### Request Body

```json
{
    "phone_number": "07xxxxxxxx",
    "amount": "1",
}
```

##### Response

```json
{
  "message": "You subscribed successfully.",
}
```