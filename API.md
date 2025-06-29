# 📚 API Documentation

## 🔐 Authentication

The API uses JWT tokens for authentication. After successful authorization, include the token in the `Authorization` header:
Authorization: Bearer <your_jwt_token>

## 👥 Users

### User Registration
```http
POST /api/v1/users/register/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword123",
    "password_check": "securepassword123"
}
```

**Response:**
```json
{
    "email": "user@example.com"
}
```

### User Authentication
```http
POST /api/v1/users/login/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

**Response:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Refresh Access Token
```http
POST /api/v1/users/refresh/
Content-Type: application/json

{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Get User Profile
```http
GET /api/v1/users/profile/
Authorization: Bearer <token>
```

**Response:**
```json
{
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "orders": [
        {
            "id": "uuid",
            "delivery_time": "2024-01-01T14:00:00Z",
            "is_ready": false,
            "items": [
                {
                    "id": "uuid",
                    "dish": {
                        "id": "uuid",
                        "name": "Borscht",
                        "description": "Delicious borscht with meat",
                        "price": "50.00",
                        "photo": "/media/dish/borsch.jpg",
                        "is_available": true
                    },
                    "quantity": 2
                }
            ]
        }
    ]
}
```

### Update User Profile
```http
PUT /api/v1/users/profile/
Authorization: Bearer <token>
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Smith"
}
```

**Response:**
```json
{
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "orders": []
}
```

## ��️ Menu

### Get Dishes List
```http
GET /api/v1/menu/dishes/
Authorization: Bearer <token>
```

**Response:**
```json
[
    {
        "id": "uuid",
        "name": "Borscht",
        "description": "Delicious borscht with meat",
        "price": "50.00",
        "photo": "/media/dish/borsch.jpg",
        "is_available": true
    },
    {
        "id": "uuid",
        "name": "Pizza Margherita",
        "description": "Classic pizza with tomato and mozzarella",
        "price": "75.00",
        "photo": "/media/dish/pizza.jpg",
        "is_available": true
    }
]
```

### Get Specific Dish
```http
GET /api/v1/menu/dishes/{id}/
Authorization: Bearer <token>
```

**Response:**
```json
{
    "id": "uuid",
    "name": "Borscht",
    "description": "Delicious borscht with meat",
    "price": "50.00",
    "photo": "/media/dish/borsch.jpg",
    "is_available": true
}
```

### Create Dish (Admin Only)
```http
POST /api/v1/menu/dishes/
Authorization: Bearer <admin_token>
Content-Type: multipart/form-data

{
    "name": "New Dish",
    "description": "Dish description",
    "price": "75.50",
    "photo": <file>,
    "is_available": true
}
```

### Update Dish (Admin Only)
```http
PUT /api/v1/menu/dishes/{id}/
Authorization: Bearer <admin_token>
Content-Type: multipart/form-data

{
    "name": "Updated Name",
    "price": "80.00"
}
```

### Delete Dish (Admin Only)
```http
DELETE /api/v1/menu/dishes/{id}/
Authorization: Bearer <admin_token>
```

## 🛒 Cart

### View Cart
```http
GET /api/v1/cart/
Authorization: Bearer <token>
```

**Response:**
```json
{
    "items": [
        {
            "id": "uuid",
            "dish": {
                "id": "uuid",
                "name": "Borscht",
                "description": "Delicious borscht with meat",
                "price": "50.00",
                "photo": "/media/dish/borsch.jpg",
                "is_available": true
            },
            "quantity": 2
        }
    ],
    "total": 100.00
}
```

### Add Dish to Cart
```http
POST /api/v1/cart/
Authorization: Bearer <token>
Content-Type: application/json

{
    "dish": "uuid",
    "quantity": 1
}
```

**Response:**
```json
{
    "id": "uuid",
    "dish": "uuid",
    "quantity": 1
}
```

### Update Cart Item
```http
PUT /api/v1/cart/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "dish": "uuid",
    "quantity": 3
}
```

**Response:**
```json
{
    "id": "uuid",
    "dish": {
        "id": "uuid",
        "name": "Borscht",
        "description": "Delicious borscht with meat",
        "price": "50.00",
        "photo": "/media/dish/borsch.jpg",
        "is_available": true
    },
    "quantity": 2
}
```

### Delete Cart Item
```http
DELETE /api/v1/cart/{id}/
Authorization: Bearer <token>
```

**Response:**
```json
{
    "message": "Item removed"
}
```

## �� Orders

### Create Order
```http
POST /api/v1/orders/
Authorization: Bearer <token>
Content-Type: application/json

{
    "delivery_time": "2024-01-01T14:00:00Z"
}
```

**Response:**
```json
{
    "id": "uuid",
    "delivery_time": "2024-01-01T14:00:00Z",
    "is_ready": false,
    "items": [
        {
            "id": "uuid",
            "dish": {
                "id": "uuid",
                "name": "Borscht",
                "description": "Delicious borscht with meat",
                "price": "50.00",
                "photo": "/media/dish/borsch.jpg",
                "is_available": true
            },
            "quantity": 2
        }
    ]
}
```

### Get Order Details
```http
GET /api/v1/orders/{id}/
Authorization: Bearer <token>
```

**Response:**
```json
{
    "id": "uuid",
    "delivery_time": "2024-01-01T14:00:00Z",
    "is_ready": false,
    "items": [
        {
            "id": "uuid",
            "dish": {
                "id": "uuid",
                "name": "Borscht",
                "description": "Delicious borscht with meat",
                "price": "50.00",
                "photo": "/media/dish/borsch.jpg",
                "is_available": true
            },
            "quantity": 2
        }
    ]
}
```

## 🔄 Celery Tasks

### Automatic Tasks

1. **Scan Ready Orders** - runs every minute
   - Checks orders with `is_ready=True` and `is_notified=False`
   - Sends email notifications to users
   - Marks orders as `is_notified=True`

### Environment Variables

```env
DEBUG=True
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=admin
DB_NAME=restaurant
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 📊 Error Responses

### Validation Error
```json
{
    "field_name": [
        "This field is required."
    ]
}
```

### Authentication Error
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Permission Error
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### Not Found Error
```json
{
    "detail": "Not found."
}
```

## �� API Base URL

- **Development**: `http://localhost:8000/api/v1/`
- **Production**: `https://your-domain.com/api/v1/`

## 📚 Swagger Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`