**COST MANAGER APP PROJECT**

I.The project aim is to allow users to register/login, store their budget, their expenses, their balance and allow to save the products names and prices that are often bought.

II. This project is written in Python programming language, using Flask framework. 
It consists of the main app: app.py and the microservice service.py. Visual representation (UI) has been created using HTML and CSS (see: templates).
File requirements.txt consists of all Python modules used in the project: Flask, flask_sqlalchemy, requests.

III. Production version of the project can be opened via creating a docker image, using following commands:

**docker build --tag python-docker . 

docker run -d -p 5000:5000 python docker**

File "wrapper.sh" allows us to run both app.py and service.py simultaneously.

IV. Once the application is working, it will create two databases (using SQLite) which store the input data.
Databases are stored in test.db and service.db.

V. Microservice service.py runs on port 5001. The application app.py runs on the port 5000.

This project is currently in the completed stage with a possibility of expanding it via adding new functionalities in the future.
The project would benefit from frequent commits if ever expanded. 











