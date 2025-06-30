# 🍽️ Restaurant Website API

REST API for a restaurant website with order management, menu system, and user management.

## 📋 Features

### 👥 Users
- User registration and authentication
- JWT token-based authentication
- User profile management

### 🍽️ Menu
- Dish management (CRUD operations)
- Dish categories
- Dish photos
- Prices and descriptions

### 🛒 Cart
- Add/remove dishes from cart
- Change dish quantities
- Clear cart

### 📦 Orders
- Create orders from cart
- Set delivery time
- Order status tracking (ready/not ready)
- Automatic notifications for ready orders

### 🔄 Celery Tasks
- Automatic scanning of ready orders
- Email notifications

## 🛠️ Technologies

- **Backend**: Django 5.2.3 + Django REST Framework
- **Database**: PostgreSQL
- **Cache/Message Broker**: Redis
- **Task Queue**: Celery + Celery Beat
- **Authentication**: JWT
- **Documentation**: drf-yasg (Swagger)
- **Containerization**: Docker + Docker Compose

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Running the Project

1. **Clone the repository**
```bash
git clone <repository-url>
cd restaurantwebsite
```

2. **Run with Docker**
```bash
docker-compose up --build
```

3. **Access the API**
- API documentation: http://localhost:8000/swagger/
- Admin panel: http://localhost:8000/admin/
- API endpoints: http://localhost:8000/api/

### Superuser
Automatically created on first run:
- Email: `admin@restaurant.com`
- Password: `admin123`


## �� API Endpoints

### Users
- `POST /api/v1/users/register/` - User registration
- `POST /api/v1/users/login/` - User authentication
- `POST /api/v1/users/refresh/` - Refresh access token
- `GET /api/v1/users/profile/` - Get user profile
- `PUT /api/v1/users/profile/` - Update user profile

### Menu
- `GET /api/v1/menu/dishes/` - List all dishes
- `POST /api/v1/menu/dishes/` - Create dish (admin only)
- `GET /api/v1/menu/dishes/{id}/` - Get dish details
- `PUT /api/v1/menu/dishes/{id}/` - Update dish (admin only)
- `DELETE /api/v1/menu/dishes/{id}/` - Delete dish (admin only)

### Cart
- `GET /api/v1/cart/` - View cart with total
- `POST /api/v1/cart/` - Add item to cart
- `GET /api/v1/cart/{id}/` - Get cart item details
- `PUT /api/v1/cart/{id}/` - Update cart item quantity
- `DELETE /api/v1/cart/{id}/` - Remove item from cart

### Orders
- `POST /api/v1/orders/` - Create order from cart
- `GET /api/v1/orders/{id}/` - Get order details

## 🔧 Development

### Local Development

1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up database**
```bash
python manage.py migrate
```

4. **Create superuser**
```bash
python manage.py createsuperuser
```

5. **Run server**
```bash
python manage.py runserver
```

### Testing

```bash
# Run all tests
python manage.py test

# Run tests for specific module
python manage.py test src.users.tests
python manage.py test src.menu.tests
python manage.py test src.cart.tests
python manage.py test src.orders.tests
```

### Code Quality

```bash
# isort - import sorting
isort .

# flake8 - code style checking
flake8 .

# mypy - type checking
mypy .
```

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart specific service
docker-compose restart web

# Execute commands in container
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py test
```

## 📧 Email Configuration

To enable email notifications, create a `.env` file with the following variables:

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register** or **Login** to get access and refresh tokens
2. **Include the access token** in the Authorization header:
   ```
   Authorization: Bearer <your-access-token>
   ```
3. **Refresh the access token** when it expires using the refresh token

## 📊 Database Schema

### Users
- Custom User model with email as username
- UUID primary keys
- JWT authentication

### Menu
- Dishes with photos, prices, and descriptions
- Availability status

### Cart
- User-specific cart items
- Quantity management
- Automatic cart creation

### Orders
- Order items with quantities
- Delivery time scheduling
- Status tracking (ready/not ready)
- Email notifications

## 🚀 Deployment

### Production Setup

1. **Environment Variables**
```env
DEBUG=False
SECRET_KEY=your-secret-key
DB_HOST=your-db-host
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=your-db-name
REDIS_URL=your-redis-url
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-email-password
REDIS_URL=redis://redis:6379/0
```

2. **Static Files**
```bash
python manage.py collectstatic
```

3. **Database Migrations**
```bash
python manage.py migrate
```
