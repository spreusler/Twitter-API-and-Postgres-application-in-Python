##Twitter Application

This repository is an example for querying the Twitter API and storing the data in a Postgres database. This way you can analyze tweets and create network studies.
My article on medium.com covers this project [in German language](https://medium.com/@stefan.preusler/twitter-api-und-postgres-implementierung-mittels-aws-rds-und-ec2-8be23708aec).

## 1. Requirements

Install libraries referenced in requirements.txt

## 2. Instructions

### 2. 1 Configuration files

`config_demo.py` includes examples for the desired Twitter keywords, Twitter API and Postgres credentials. Copy the file, rename it to `config.py` and store your personal data.

### 2.2 Run application

Run application via `python main.py`

## 3. Changelog

2019-07-08 Initial commit