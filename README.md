# Project Setup and Running Instructions

## Prerequisites

- Python 3.x
- pip (Python package installer)
- MySQL database

## Installation

1. Clone the repository:

```sh
$ git clone <repository-url>
$ cd <repository-directory>
```

2. Create a virtual environment and activate it:

```sh
$ python3 -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required packages:

```sh
$ pip install -r requirements.txt
```

## Database Setup

1. Install MySQL and create a database:

```sh
$ sudo apt-get install mysql-server  # On Ubuntu
$ brew install mysql  # On macOS
```

2. Log in to MySQL and create the database:

```sh
$ mysql -u root -p
mysql> CREATE DATABASE life_cost_management;
mysql> exit;
```

3. Update the `alembic.ini` file with your database connection details:

```ini
sqlalchemy.url = mysql+pymysql://<username>:<password>@<host>:<port>/life_cost_management
```

4. Run the database migrations:

```sh
$ alembic upgrade head
```

## Running the Project

1. Start the server:

```sh
$ python app.py
```

2. Open your web browser and go to `http://127.0.0.1:8050` to see the application running.
