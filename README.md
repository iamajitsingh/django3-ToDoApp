# django3-ToDoApp

<div align="center" >
<img height="100" src="https://scheduleit.pythonanywhere.com/static/notes/Logo.png" width="100" alt="logo"/>
</div>

Schedule.It is an app which allows you to create an account, create/update/track your important to-dos.
Some functionalities:
1. New user registration.
2. User Login, Logout.
3. Create, Update, View & Delete To-Dos.
4. Add description to your To-Dos.
5. Mark certain To-Dos as '**Important**': Assign Priority to your work!
6. Get notification emails for important To-Dos.

## Instructions to contribute
1. Fork the repo.
2. Clone the version of your fork locally.
3. Create a virtual environment and activate it. Not required but highly recommended. 
```bash
python -m venv env
.\env\Scripts\activate
```
The above command is for Windows only. For Linux based operating systems, use the below-mentioned command. 
```bash
python3 -m venv env
source env/bin/activate
```
3. Now, install the requirements. 
```bash
pip install -r requirements.txt
```
4. Now, migrate changes to the database and start the server. 
```
python manage.py migrate
python manage.py runserver
```
5. Head to [127.0.0.1:8000](http://127.0.0.1:8000/) and you should be able to see the development version of this app live. 
6. Create a superuser (```python manage.py createsuperuser ```) to access Django admin interface.
7. Go through the [CONTRIBUTING.md](CONTRIBUTING.md) file to get started with contributions.


## Any Questions?
Feel free to raise an issue. We'll try to answer this as soon as we can. 

## Contributing Guidelines
If there is any valid contribution, please raise an issue and feel free to create a pull request. We will review it and merge it to the master branch. 
