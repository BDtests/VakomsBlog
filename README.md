# VakomsBlog


Simple django-based blog

In order to start the server locally, perform following actions:
1. install dependencies by running "pip install -r requirements.txt"
2. fill in required fields in local_settings.py from vacomsBlog/vaconsBlog/

# Accessing django-admin
1. register user through project's UI

Now you can manualy change 'is_staff' field to True in your database or follow the guide. 

2. python manage.py shell
3. from authentication.models import CustomUser
4. user = CustomUser.get_by_email('enter your email')
5. user.set_admin_rights(True)


While the blog has all required and additional functionality, it lacks docstrings, validators, PUT and error handlers, and requires some structural improvements. However, I am forced to submit the task due to the lack of time until Monday.

Thank you in advance for your check!
Feel free to contact me if you have any questions.
