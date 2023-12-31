# Project Weblog

This is a demo project built with Django, serving as the backend for a Medium-like platform.

## Description

The project aims to showcase the backend functionality required for a content sharing platform, similar to Medium. It provides a foundation for creating, managing, and retrieving articles, user authentication, and other essential features.

The frontend part of the project is yet to be developed, and this repository focuses solely on the backend implementation.

## Features

- User authentication: Register, login, and logout functionality.
- Article creation: Users can create articles with a title, content, and other relevant details.
- Article management: Edit, delete, and update articles.
- Article retrieval: Get a list of all articles or fetch a specific article by its ID.
- User profiles: View user profiles with information such as username and bio.
- Category : Associate an Article with category

## Installation

1. First Clone the repository:

```
git clone https://github.com/Amirhossein-code/djnago-blog.git
```

2. Navigate to the project directory (where manage.py is located):

```
cd project-directory
```

3.Install the project dependencies using pipenv:

```
pipenv install
```

4.Activate the virtual environment:

```
pipenv shell
```

5.Run database migrations:

```
python manage.py migrate
```

6.Start the development server:

```
python manage.py runserver
```

7.Access the API at : http://localhost:8000

## Seting up the MySQL Database

1.Create a .env file at root directory and set the required fields
The .env file :

```
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
```

Note : The databse will be automatically created when runiing python manage.py migrate
if not open a query console and run : (db : MySQL)

```
CREATE DATABASE IF NOT EXISTS DB_name;
```

Make Sure to properly set up the .env file
