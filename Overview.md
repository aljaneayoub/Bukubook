# **Overview**
## Importing Dependencies
- `request`, `redirect`, `render_template`, `Flask`, `flash`, `session`, `url_for`, `send_file`: These are various Flask modules and functions used for handling requests, rendering templates, managing sessions, and sending files.
- `SQLAlchemy`: A popular Python ORM (Object-Relational Mapping) library for working with databases.
- `base64`: A module for encoding and decoding data in base64 format.
- `generate_password_hash`: A function from the Werkzeug library used for password hashing.
- `current_user`: A function from the Flask-Login library used to get the currently logged-in user.

## Flask Application Setup
- Create a Flask application instance and configure it with a secret key and a MySQL database URI.
- Initialize the SQLAlchemy extension with the Flask application.

## Database Models
- `Book`: Represents a book in the database with attributes like ID, title, author, categories, rate, cover image, and PDF.
- `User`: Represents a user in the database with attributes like username, email, password, library relationship, and admin status.
- `Library`: Represents a user's private library with attributes like ID, title, author, categories, rate, cover image, PDF, and the associated username.

## Routes and Views
- `/`: Renders the home page.
- `/top_books`: Renders a page displaying the top books.
- `/categories`: Renders a page displaying the available book categories.
- `/books_by_category`: Renders a page displaying books filtered by a specific category.
- `/authors`: Renders a page displaying authors and allows searching and sorting.
- `/register`: Handles user registration, form submission, and redirects based on the outcome.
- `/login`: Handles user login, form submission, and redirects based on the outcome.
- `/private-library`: Renders a user's private library page, requires authentication.
- `/user/books/create`: Handles the creation of a book by a user, requires authentication.
- `/add_book`: Handles adding a book to the user's private library, requires authentication.
- `/logout`: Handles user logout and redirects to the home page.
- `/admin`: Renders the admin dashboard, requires admin privileges.
- `/admin/books/create`: Handles the creation of a book by an admin, requires admin privileges.
- `/admin/books/update/<int:book_id>`: Handles updating an existing book by an admin, requires admin privileges.
- `/admin/books/delete/<int:book_id>`: Handles deleting an existing book by an admin, requires admin privileges.
- `/admin/users`: Renders the admin users page, listing all users, requires admin privileges.
- `/admin/users/create`: Handles the creation of a user by an admin, requires admin privileges.
- `/admin/users/edit/<user_name>`: Handles editing an existing user by an admin, requires admin privileges.
- `/admin/users/delete/<user_name>`: Handles deleting an existing user by an admin, requires admin privileges.
- `/download_pdf/<book_id>`: Allows downloading a PDF file of a book from the user's private library, requires authentication.

## Additional Templates
Various HTML templates are used to render different pages and forms based on the routes mentioned above.
