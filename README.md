# EasyEatsOnline

EasyEatsOnline is an online food service platform built with Flask and Flask-RESTx. It offers a user-friendly and streamlined culinary experience, leveraging a modular architecture inspired by Spring Boot. PostgreSQL is utilized as the primary database for secure and efficient data storage.


## Features

### User Authentication

- Signup: Users can create accounts to access the platform.
- Login: Secure user login for authenticated sessions.
- Token Refresh: Ability to refresh authentication tokens.

### Shopping Cart

- Add to Cart: Users can add products to their shopping cart.
- Delete from Cart: Remove items from the shopping cart.
- Retrieve Cart: View the current state of the shopping cart.

### Product Management

- List Products: Retrieve a list of available products.
- Create Product: Add new products to the platform.
- Update Product: Modify existing product details.
- Delete Product: Remove products from the system.

### Category Management

- List Categories: Retrieve a list of available product categories.
- Create Category: Add new categories.
- Update Category: Modify existing category details.
- Delete Category: Remove categories from the system.

### Order Management

- List Orders: View a list of placed orders.
- Update Order Quantity: Modify the quantity of products in an order.

### User Management
- List Users: Retrieve a list of registered users.
- Update Current User: Modify details of the currently authenticated user.

### API Documentation

- Swagger UI: Access detailed API documentation for developers at http://localhost:5000/api/docs.
- Swagger specifications: Go to Swagger specifications at http://localhost:5000/api/swagger.json.


## Prerequisites

Ensure you have the following installed:

- Python 3.10 or later
- Poetry: Dependency management tool
- Dependencies listed in `pyproject.toml`
- Docker (optional): For containerization
- SQLite (default) or PostgreSQL: Database for data storage


## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/Macktireh/EasyEatsOnlineApi.git
```
```bash
cd EasyEatsOnlineApi
```

### 2. Copy the `.env.example` file to `.env` and configure the environment variables as needed.

### 3. With Docker

1. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

### 4. Without Docker

1. Create a virtual environment and install dependencies:
    ```bash
    poetry install
    ```

2. Apply database migrations:

    ```bash
    poetry run flask db upgrade
    ```

3. Run the application:

    ```bash
    poetry run flask run
    ```

### 5. Access the Application
Visit [http://localhost:5000](http://localhost:5000) in your web browser.



## Testing

Run tests with the following command:

```bash
poetry run flask test
```


## Postman Collection

Generate the Postman collection with the following command:

```bash
poetry run flask postman --export=True
```

The collection will be available in the postman directory.


## License

This project is licensed under the [MIT License](LICENSE).
