# Music Scheduler
A computer science A-level mock NEA project

Allows dynamic scheduling of music lessons where timetable clashes with school lessons are optimised to take away least amount of time from subjects with little teaching time.

## Dev setup
- requires python 3.8+
- strongly recommend windows machine
- requires a functioning [mysql](https://dev.mysql.com/downloads/mysql/) server setup 

- open mysql line client
- enter `create database musicschedulerdb;`

- clone repository
```
git clone https://github.com/wongjack2332/musicScheduler
cd musicScheduler
```

- windows: `setup.bat`
- others: `python -m pip install -r requirements.txt`

## Starting Server
```
cd src
python main.py
```
or using waitress server
```
waitress-serve --port=5000 main:app
```

- modify username and password for database server in `main.py`

## external dependencies
- python Flask
- python Waitress
- python PyMySql
- python cryptography
- python bcrypt


### contributors:
- Jack Wong, Duy Nguyen, Joon Kang, Jiaming Tang
