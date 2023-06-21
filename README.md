# **Bukubook** 	![](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)  	![](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)  	![](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white) ![](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)

This is a Flask-based web application for managing a library of books called Bukubook.
It allows users to register, login, view and filter books, add books to their private library, 
and perform administrative tasks such as creating, updating, and deleting books and users.

## Requirements

- Python (version 3.11.4)
- Flask (version 2.3.2)
- Jinja2 (version 3.1.2)
- SQLAlchemy (version 2.0.16)
- Werkzeug (version 2.3.6)
  
## Installation

```shell
    #Clone the project
    git clone https://github.com/aljaneayoub/Bukubook.git
```
```bash
    cd Bukubook
```
```bash
    #Install the Dependencies
    pip install -r requirements.txt
```

## Configuration

Import the file bukubook.sql into your database management tool like e.g. mysql workbench, phpmyadmin.

**PS**: you should make some change in my.ini file 

    - max_allowed_packet=16M
    - innodb_lock_wait_timeout=28800
    - max_allowed_packet=512M

## Usage

1. Start the application:
```bash
    python app.py
```
2. Open your web browser and visit http://localhost:5000 to access the application.
3. Follow the instructions provided by the application to use its features.
