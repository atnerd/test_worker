# Data Processing Application

## Description
This application is designed to process an array of natural numbers, leveraging a worker pool for computation and storing the results in a distributed KeyValue store.

Originally, it was developed using `flask` framework, but then I realized that the assignment specified not to use third-party libraries, so I also implemented it using default python `http` library too.

## Features
- Accepts an input array of natural numbers of length N.
- Processes the array using a single worker from a pool of `N_WORKERS`.
- Each worker calculates the sum of all elements in the array.
- The sum is then stored in a distributed KeyValue storage, with the new value being added to any existing value.

## Usage
**flask**:
 - pip install flask
 - export N_WORKERS=4
 - `python flask_app.py`
 - curl --location 'http://127.0.0.1:5000/submit' \ --header 'Content-Type: application/json' \ --data '{"numbers": [1,2,3,4,5]}' - add data
 - curl --location 'http://127.0.0.1:5000/result' \ - read data

**http**:
 - export N_WORKERS=4
 - `python base_http_server.py`
 - curl --location 'http://127.0.0.1:8000/submit' \ --header 'Content-Type: application/json' \ --data '{"numbers": [1,2,3,4,5]}' - add data
 - curl --location 'http://127.0.0.1:8000/result' \ - read data
