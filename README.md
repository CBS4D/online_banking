
# Online Banking System - FlaskRest API (Python)



## Prerequisites
* Python
* Docker


# Steps

 - [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation
**To run on local system**
Create virtual environment

    python -m virtualenv (specify environment name)
Activate virtual environment.

    .\vnv\Scripts\activate

Install the Python client library using pip:

    pip install -r requirements.txt
Start application

    python main.py

**To run inside container**

Project has Dockerfile for application image, and a docker compose file to setup whole application all together. (Web App, PostgreSQL DB and Redis).
build all necessary images using below command.

     docker compose build
After successful build run all images in 3 different containers using below command.

     docker compose up -d
To check all containers are up and running use below command.
`-a` option to see all non running containers as well.

     docker ps -a
Now our application is up and running we can test it using Postman.

## Usage

- Register new user
- Login user to get jwt auth token.
- Use the jwt token in every request's header.
- Can check user balance, make credit or debit transactions and can also transfer money from self account to different account.
- User can check his past transactions.
- Logout user to revoke existing jwt token.


## License

This library is released under the [MIT License][license].

[license]: LICENSE.txt
