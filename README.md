# BW4E Rewards Store

## Description

The BW4E Rewards Store is a web application built with Django that allows users to redeem products and services offered by various partners. Users can browse a catalog of available items, view details, and make redemptions. The system tracks redemptions and manages product stock (if applicable).

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
    This allows you to access the Django admin panel to manage data.
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

2.  **Access the Application**:
    Open your web browser and go to:
    *   Login page: `http://127.0.0.1:8000/accounts/login/` (Start here to log in)
    *   Home page (after login): `http://127.0.0.1:8000/store/home/`
    *   Products page (after login): `http://127.0.0.1:8000/store/products/`

3.  **Access the Admin Panel**:
    *   Admin panel: `http://127.0.0.1:8000/admin/`
    *   Log in with the superuser credentials you created.

## Populating Data

*   Use the Django admin panel (`/admin/`) to add `Partner` entities first.
*   Then, add `Product` entities, associating them with the created partners.
*   Users can be managed via the admin panel as well (part of Django's built-in auth system).

This provides a basic setup to get the BW4E Rewards Store running locally for development and testing.
