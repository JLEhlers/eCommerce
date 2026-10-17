# Django eCommerce Project

## Project Overview

This is a Django eCommerce website where users can register as buyers or vendors. Each user has access to different features depending on their role.

## Features

### Vendors
- Create, edit, and delete stores.
- Add, edit, and delete products.

### Buyers
- View available products.
- Add products to a shopping cart.
- Checkout.
- Leave product reviews.

### Authentication and Permissions
- Register an account.
- Log in and log out.
- Reset a password.
- Use Django authentication and permissions to control access to pages and actions.

## Technologies Used

- Python
- Django
- MySQL/MariaDB
- HTML and CSS
- Bootstrap

## Installation and Setup

### 1. Clone the GitHub Repository

Open PowerShell or a terminal and navigate to the location where you want to save the project.

Run the following command, replacing the URL with your GitHub repository URL:

```powershell
git clone https://github.com/JLEhlers/eCommerce.git
```

Enter the cloned project folder:

```powershell
cd eCommerce
```

**Important:** The project root folder should contain `manage.py`, `requirements.txt`, `README.md`, the Django settings folder (such as `eCommerce`), and the application folder (such as `shop`). Do not enter an additional nested project folder unless your repository is structured that way.

### 2. Create and Activate the Virtual Environment

From the project root folder, create a virtual environment:

```powershell
python -m venv myenv
```

Activate it in Windows PowerShell:

```powershell
.\myenv\Scripts\Activate.ps1
```

If you are using Command Prompt instead, run:

```cmd
myenv\Scripts\activate.bat
```

### 3. Install the Project Dependencies

Make sure the virtual environment is activated, then run:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

This installs the packages listed in `requirements.txt`, including Django and any other required dependencies.

If `requirements.txt` is missing, check the repository before continuing. The project dependencies should be recorded in this file.

### 4. Create the MySQL Database

Make sure MySQL is installed and the MySQL server is running.

Open the MySQL terminal from PowerShell or Command Prompt:

```powershell
mysql -u root -p
```

Enter your MySQL root password when prompted. The password will not appear as you type.

If the `mysql` command is not recognised, open the MySQL command-line client from your MySQL installation or add the MySQL `bin` directory to your system PATH.

Once you are in the MySQL terminal, create the database:

```sql
CREATE DATABASE ecommerce_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Check that the database was created:

```sql
SHOW DATABASES;
```

Exit the MySQL terminal:

```sql
EXIT;
```

The database name used above is `ecommerce_db`. Use the same name in your Django settings.

### 5. Configure the Django Database Settings

Open the Django settings file, usually:

```text
eCommerce/settings.py
```

Find the `DATABASES` setting and configure it to use MySQL:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "ecommerce_db",
        "USER": "root",
        "PASSWORD": "YOUR_MYSQL_PASSWORD",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

Replace `YOUR_MYSQL_PASSWORD` with your MySQL password.

**Security note:** Do not commit real database passwords, Django secret keys, or other credentials to GitHub. For a safer setup, load these values from environment variables or a `.env` file that is excluded from version control.

If your project already uses environment variables or a different database configuration, follow the existing project setup rather than replacing it blindly.

### 6. Create and Apply Database Migrations

From the project root folder, where `manage.py` is located, run:

```powershell
python manage.py makemigrations
python manage.py migrate
```

These commands create migration files for model changes and apply the migrations to the configured database.

If the repository already includes migration files, keep them and apply them with `python manage.py migrate`.

### 7. Create a Django Administrator Account (Optional)

To access the Django administration site, run:

```powershell
python manage.py createsuperuser
```

Follow the prompts to create an administrator username, email address, and password.

### 8. Run the Website

Start the Django development server:

```powershell
python manage.py runserver
```

Open the website in your browser:

http://127.0.0.1:8000/

To access the Django administration site, visit:

http://127.0.0.1:8000/admin/

Stop the development server by pressing `Ctrl + C` in the terminal.

## Troubleshooting

- **`No module named django`:** Check that the virtual environment is activated and run `pip install -r requirements.txt`.
- **MySQL connection error:** Make sure the MySQL server is running and the database name, username, password, host, and port are correct.
- **`mysql` is not recognised:** Use the MySQL command-line client or configure the MySQL `bin` directory in PATH.
- **Missing tables:** Run `python manage.py migrate`.
- **Missing dependencies:** Check that `requirements.txt` contains all required packages.

## Project Purpose

The purpose of this project is to demonstrate a Django eCommerce website with buyer and vendor accounts, store and product management, shopping cart functionality, checkout, and product reviews.
