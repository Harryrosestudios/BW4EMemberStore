# BW4E Rewards Store - Headless CMS & API

## Description

The BW4E Rewards Store is a headless content management system (CMS) and API backend built with Django and Django REST Framework. It provides API endpoints for managing and redeeming products/services offered by various partners. The Django Admin panel serves as the primary interface for content management (Partners, Products, Users, etc.). This system is designed to be consumed by a separate frontend application or other services.

## Prerequisites

*   Python 3.8 or higher
*   pip (Python package installer)

## Setup Instructions

1.  **Clone the Repository / Obtain Project Files**:
    Ensure you have the project files. This `README.md` and `requirements.txt` should be in your main project directory (let's call it `project_root`). The Django application code is in a subdirectory named `bw4e_store` within `project_root`.

2.  **Navigate to the Project Root Directory**:
    Open your terminal and navigate to the `project_root` directory where this `README.md` and `requirements.txt` are located.
    ```bash
    cd path/to/project_root
    ```

3.  **Create a Python Virtual Environment**:
    From the `project_root` directory:
    ```bash
    python -m venv venv
    ```

4.  **Activate the Virtual Environment**:
    *   On Linux/macOS:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```

5.  **Install Dependencies**:
    Install the required packages from `requirements.txt` (still in `project_root`):
    ```bash
    pip install -r requirements.txt
    ```

6.  **Navigate to the Django Project Directory**:
    Change directory into the Django project folder to use `manage.py`.
    ```bash
    cd bw4e_store
    ```

7.  **Apply Database Migrations**:
    This command creates the database tables needed for the application.
    ```bash
    python manage.py migrate
    ```

8.  **Create a Superuser Account**:
    This allows you to access the Django admin panel to manage data and also to authenticate for API actions if using session authentication.
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set a username, email (optional), and password.

## Running the Development Server

1.  **Start the Server**:
    Make sure you are in the Django project directory (`project_root/bw4e_store`, which contains `manage.py`) and your virtual environment is activated.
    ```bash
    python manage.py runserver
    ```

2.  **Accessing the System**:
    *   **Django Admin Panel**: `http://127.0.0.1:8000/admin/`
        *   Log in with the superuser credentials you created. This is the primary interface for managing content.
    *   **API Endpoints**: Available under `http://127.0.0.1:8000/store/api/`. See the "API Endpoints" section below for details.
        *   Many endpoints are browsable via DRF's interface if you open them in a web browser (e.g., `http://127.0.0.1:8000/store/api/products/`).

## API Endpoints

The API provides the following main resources. By default, read-only operations are generally available to anyone, while creation/modification operations require authentication.

*   **Partners**:
    *   `GET /store/api/partners/`: List all partners.
    *   `GET /store/api/partners/{id}/`: Retrieve a specific partner by its ID.

*   **Products**:
    *   `GET /store/api/products/`: List all products.
    *   `GET /store/api/products/{id}/`: Retrieve a specific product by its ID.

*   **Redemptions** (Authentication Required for all actions):
    *   `GET /store/api/redemptions/`: List redemptions for the authenticated user.
    *   `POST /store/api/redemptions/`: Create a new redemption for the authenticated user.
        *   **Required JSON payload**: `{"product": <product_id>}` (where `<product_id>` is the integer ID of the product to redeem)
        *   **Optional JSON payload**: `{"notes": "Your optional notes for this redemption"}`
        *   Example `curl` command (replace `<product_id>`, `<session_cookie_value>`, and potentially the CSRF token if not using `force_authenticate` in tests):
            ```bash
            # First, log in via Django Admin in your browser to get a session.
            # Then, find your sessionid cookie value and CSRF token from browser dev tools.
            # For testing, using tools like Postman or Insomnia is easier to manage authentication.
            # If session authentication is used (default for browser interaction with DRF browsable API after admin login):
            curl -X POST http://127.0.0.1:8000/store/api/redemptions/ \
                 -H "Content-Type: application/json" \
                 -H "X-CSRFToken: <your_csrf_token>" \
                 -b "sessionid=<your_sessionid_cookie_value>" \
                 -d '{"product": 1, "notes": "My test redemption via curl"}'
            ```

**Authentication for API**:
*   The simplest way to test authenticated endpoints during development is to log in to the Django Admin panel in your browser. This will establish a session that DRF's browsable API can use.
*   For programmatic access or third-party clients, token-based authentication (e.g., DRF's `TokenAuthentication` or `django-rest-knox`) would typically be configured, but is not part of the default setup here.

## Populating Data

*   Use the Django admin panel (`http://127.0.0.1:8000/admin/`) to:
    *   Add `Partner` entities.
    *   Add `Product` entities, associating them with the created partners.
    *   Manage `User` accounts.

This provides a basic setup to get the BW4E Rewards Store API running locally.
