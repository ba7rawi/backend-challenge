# Set up Instructions
1. Downlaod the code from the repo to your local machine.(you gotta download python if you don't have it)
2. Create a virtual enviroment of your choice but here is a simple example
    a. `python3 -m venv env`
    b. `source env/bin/activate`
3. Use the requirements.txt file to populate your virtual enviroment `pip install -r requirements.txt`
4. Run django app using `python manage.py runserver`
5. Login credintals are: 
    1. username: `admin`, password: `admin`
    2. username: `ibrahim`, password: `admin`
6. Run the tests using `python manage.py test tasks.tests`