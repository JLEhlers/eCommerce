Django eCommerce Project

This is a Django eCommerce website where users can register as buyers or vendors.

Vendors can:
Create stores
Edit stores
Delete stores
Add products
Edit products
Delete products

Buyers can:
View products
Add products to a cart
Checkout
Leave reviews

Create and activate the virtual environment:

python -m venv myvenv
.\myvenv\Scripts\Activate.ps1

Install Django:

pip install django
Database

This project uses MariaDB/MySQL as the database.

After setting up the database, run:

python manage.py makemigrations

Then:

python manage.py migrate
Run the Website

Start the server:

python manage.py runserver

Open:

http://127.0.0.1:8000/
Authentication

Users can:

Register
Log in
Log out
Reset their password

Some pages require users to be logged in using @login_required.

Permissions are also used to control access to certain products and actions.