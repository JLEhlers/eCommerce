# Django eCommerce Project

## Project Overview

This is a Django eCommerce website where users can register as buyers or vendors. Each user has access to different features depending on their role.

## Features

### Vendors

Vendors can:
- Create stores.
- Edit stores.
- Delete stores.
- Add products.
- Edit products.
- Delete products.

### Buyers

Buyers can:
- View available products.
- Add products to a shopping cart.
- Checkout.
- Leave product reviews.

### Authentication and Permissions

Users can:
- Register an account.
- Log in and log out.
- Reset their password.

Some pages require users to be logged in using Django's `@login_required` decorator. Permissions are also used to control access to certain products and actions.

## Installation

### 1. Create and Activate the Virtual Environment

Open a terminal in the project folder and run:

```powershell
python -m venv myvenv
.\myvenv\Scripts\Activate.ps1
```

### 2. Install Dependencies

Install Django:

```powershell
python -m pip install django
```

If the project has a `requirements.txt` file, install the other dependencies using:

```powershell
python -m pip install -r requirements.txt
```

## Database Setup

This project uses MariaDB/MySQL as its database.

Make sure the database server is running and the database settings are configured in `settings.py`.

Run the following commands to create and apply database migrations:

```powershell
python manage.py makemigrations
python manage.py migrate
```

## Run the Website

Start the Django development server:

```powershell
python manage.py runserver
```

Open the following address in your browser:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Technologies Used

- Python
- Django
- MariaDB/MySQL
- HTML
- CSS
- Bootstrap

## Project Purpose

The purpose of this project is to develop an eCommerce website that supports buyer and vendor accounts, store and product management, shopping carts, checkout, and product reviews.