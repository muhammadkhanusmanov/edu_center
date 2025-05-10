# API Documentation for Edu Center

## Overview

This API provides endpoints for managing users, courses, lesson schedules, monthly test results, and payments in an educational center. It uses Django REST Framework for building the API and requires authentication for most endpoints.

## Authentication

All endpoints require authentication. Use the following methods for authentication:

- **Token Authentication**: Include a token in the `Authorization` header:
  ```
  Authorization: Token <your_token>
  ```

## Endpoints

### 1. Login

- **URL**: `/api/login/`
- **Method**: `POST`
- **Request Body**:
  ```json
  Baic Auth
  ```
- **Response**:
  - **200 OK**:
    ```json
    {
        "token": "your_token",
        "user": {
            "id": 1,
            "username": "your_username",
            "email": "your_email",
            "status": "admin",
            "is_active": true,
            "is_staff": true
        }
    }
    ```
  - **401 Unauthorized**:
    ```json
    {
        "error": "Invalid credentials"
    }
    ```

### 2. Create Admin

- **URL**: `/api/create-admin/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
      "username": "admin_username",
      "email": "admin@example.com",
      "password": "secure_password",
      "status": "admin"
  }
  ```
- **Response**:
  - **201 Created**:
    ```json
    {
        "user_id": 1,
        "username": "admin_username",
        "status": "admin",
        "token": "generated_token"
    }
    ```
  - **400 Bad Request**: Validation errors.

### 3. Create Teacher

- **URL**: `/api/create-teacher/`
- **Method**: `POST`
- **Request Body**: Same as Create Admin.
- **Response**: Same as Create Admin.

### 4. Create Student

- **URL**: `/api/create-student/`
- **Method**: `POST`
- **Request Body**: Same as Create Admin.
- **Response**: Same as Create Admin.

### 5. Logout

- **URL**: `/api/logout/`
- **Method**: `POST`
- **Response**:
  - **200 OK**:
    ```json
    {
        "message": "Successfully logged out."
    }
    ```
  - **401 Unauthorized**: Not authenticated.

### 6. Monthly Test Result List

- **URL**: `/api/monthly-tests/`
- **Method**: `GET`
- **Response**:
  - **200 OK**: Returns a list of monthly test results.
    ```json
    [
        {
            "id": 1,
            "student": 1,
            "date": "2025-04-15",
            "score": 90,
            "comment": "Good job",
            "course": 3
        }
    ]
    ```

### 7. Monthly Test Result Create

- **URL**: `/api/monthly-tests/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
      "student": 1,
      "date": "2025-04-15",
      "score": 90,
      "comment": "Good job",
      "course": 3
  }
  ```
- **Response**:
  - **201 Created**:
    ```json
    {
        "id": 1,
        "student": 1,
        "date": "2025-04-15",
        "score": 90,
        "comment": "Good job",
        "course": 3
    }
    ```
  - **400 Bad Request**: Validation errors.

### 8. Monthly Test Result Detail

- **URL**: `/api/monthly-tests/<int:pk>/`
- **Method**: `GET`
- **Response**:
  - **200 OK**: Returns a specific monthly test result.
    ```json
    {
        "id": 1,
        "student": 1,
        "date": "2025-04-15",
        "score": 90,
        "comment": "Good job",
        "course": 3
    }
    ```
  - **404 Not Found**: If the test result does not exist.

### 9. Monthly Test Result Update

- **URL**: `/api/monthly-tests/<int:pk>/`
- **Method**: `PUT`
- **Request Body**:
  ```json
  {
      "student": 1,
      "date": "2025-04-15",
      "score": 95,
      "comment": "Excellent job",
      "course": 3
  }
  ```
- **Response**:
  - **200 OK**:
    ```json
    {
        "id": 1,
        "student": 1,
        "date": "2025-04-15",
        "score": 95,
        "comment": "Excellent job",
        "course": 3
    }
    ```
  - **400 Bad Request**: Validation errors.
  - **404 Not Found**: If the test result does not exist.

### 10. Monthly Test Result Delete

- **URL**: `/api/monthly-tests/<int:pk>/`
- **Method**: `DELETE`
- **Response**:
  - **204 No Content**: Successfully deleted.
  - **404 Not Found**: If the test result does not exist.

### 11. Monthly Payment List

- **URL**: `/api/payments/`
- **Method**: `GET`
- **Response**:
  - **200 OK**: Returns a list of monthly payments.
    ```json
    [
        {
            "id": 1,
            "student": 1,
            "month": "April 2025",
            "amount": "200000.00",
            "is_paid": true,
            "payment_date": "2025-04-05",
            "course": 3
        }
    ]
    ```

### 12. Monthly Payment Create

- **URL**: `/api/payments/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
      "student": 1,
      "month": "April 2025",
      "amount": "200000.00",
      "is_paid": true,
      "payment_date": "2025-04-05",
      "course": 3
  }
  ```
- **Response**:
  - **201 Created**:
    ```json
    {
        "id": 1,
        "student": 1,
        "month": "April 2025",
        "amount": "200000.00",
        "is_paid": true,
        "payment_date": "2025-04-05",
        "course": 3
    }
    ```
  - **400 Bad Request**: Validation errors.

### 13. Monthly Payment Detail

- **URL**: `/api/payments/<int:pk>/`
- **Method**: `GET`
- **Response**:
  - **200 OK**: Returns a specific monthly payment.
    ```json
    {
        "id": 1,
        "student": 1,
        "month": "April 2025",
        "amount": "200000.00",
        "is_paid": true,
        "payment_date": "2025-04-05",
        "course": 3
    }
    ```
  - **404 Not Found**: If the payment does not exist.

### 14. Monthly Payment Update

- **URL**: `/api/payments/<int:pk>/`
- **Method**: `PUT`
- **Request Body**:
  ```json
  {
      "student": 1,
      "month": "April 2025",
      "amount": "250000.00",
      "is_paid": false,
      "payment_date": "2025-04-05",
      "course": 3
  }
  ```
- **Response**:
  - **200 OK**:
    ```json
    {
        "id": 1,
        "student": 1,
        "month": "April 2025",
        "amount": "250000.00",
        "is_paid": false,
        "payment_date": "2025-04-05",
        "course": 3
    }
    ```
  - **400 Bad Request**: Validation errors.
  - **404 Not Found**: If the payment does not exist.

### 15. Monthly Payment Delete

- **URL**: `/api/payments/<int:pk>/`
- **Method**: `DELETE`
- **Response**:
  - **204 No Content**: Successfully deleted.
  - **404 Not Found**: If the payment does not exist.

### 16. Lesson Schedule List

- **URL**: `/api/schedules/`
- **Method**: `GET`
- **Response**:
  - **200 OK**: Returns a list of lesson schedules.
    ```json
    [
        {
            "id": 1,
            "course": 1,
            "weekday": "monday",
            "time": "10:00:00",
            "room": "101"
        }
    ]
    ```

### 17. Lesson Schedule Create

- **URL**: `/api/schedules/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
      "course": 1,
      "weekday": "monday",
      "time": "10:00:00",
      "room": "101"
  }
  ```
- **Response**:
  - **201 Created**:
    ```json
    {
        "id": 1,
        "course": 1,
        "weekday": "monday",
        "time": "10:00:00",
        "room": "101"
    }
    ```
  - **400 Bad Request**: Validation errors.

### 18. Lesson Schedule Detail

- **URL**: `/api/schedules/<int:pk>/`
- **Method**: `GET`
- **Response**:
  - **200 OK**: Returns a specific lesson schedule.
    ```json
    {
        "id": 1,
        "course": 1,
        "weekday": "monday",
        "time": "10:00:00",
        "room": "101"
    }
    ```
  - **404 Not Found**: If the schedule does not exist.

### 19. Lesson Schedule Update

- **URL**: `/api/schedules/<int:pk>/`
- **Method**: `PUT`
- **Request Body**:
  ```json
  {
      "course": 1,
      "weekday": "tuesday",
      "time": "11:00:00",
      "room": "102"
  }
  ```
- **Response**:
  - **200 OK**:
    ```json
    {
        "id": 1,
        "course": 1,
        "weekday": "tuesday",
        "time": "11:00:00",
        "room": "102"
    }
    ```
  - **400 Bad Request**: Validation errors.
  - **404 Not Found**: If the schedule does not exist.

### 20. Lesson Schedule Delete

- **URL**: `/api/schedules/<int:pk>/`
- **Method**: `DELETE`
- **Response**:
  - **204 No Content**: Successfully deleted.
  - **404 Not Found**: If the schedule does not exist.

### 21. Student Data Overview

- **URL**: `/api/data/overview/`
- **Method**: `GET`
- **Response**:
  - **200 OK**:
    ```json
    {
        "courses": [
            {
                "id": 1,
                "name": "Course Name",
                "duration_months": 6,
                "monthly_price": 100.00,
                "teacher": 1
            }
        ],
        "students": [
            {
                "id": 1,
                "user": {
                    "id": 1,
                    "username": "student_username",
                    "email": "student@example.com"
                },
                "phone": "1234567890",
                "status": "active",
                "registered_at": "2023-01-01T00:00:00Z",
                "courses": [
                    {
                        "id": 1,
                        "name": "Course Name"
                    }
                ]
            }
        ]
    }
    ```
  - **403 Forbidden**: Unauthorized access.

## Permissions

- **Admin**: Can create users, view all data, and manage payments and test results.
- **Teacher**: Can view and manage their students' test results and courses.
- **Student**: Can view their own data and results.

## Notes

- Ensure to replace placeholder values in request bodies with actual data.
- All responses are in JSON format.
- The API is designed to handle various user roles, ensuring that permissions are enforced based on the user's status.
