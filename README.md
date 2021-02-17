# Queue Order
This project is developed to provide the queue for next day based on the last queue of present day.

## REQUIREMENTS (For running Locally)
It needs [Python to be installed] (version >= 3.7).

## FILE DESCRIPTION
1. **downloads-> rules.pdf**: This file contains the rules based on which the queue for next day is computed.
2. **downloads-> Tool Guide.pdf**: This file contains the steps to use the tool by the use of screenshots for both Windows and MAC users.
3. **downloads-> FAQs.pdf**: This file contains the Frequently Asked Questions which people might come across while using the tool.
4. **requirements.txt**: This file contains the packages which needs to be installed for using the tool locally. See the first step in the Installation and Setup (For running Locally) field below in order to use this file.

## INSTALLATION AND SETUP (For running Locally)
```sh
$ pip3 install -r requirements.txt
$ python3 app.py
Open the following URL on browser:
localhost:5000/next_day_queue
```
## INSTALLATION AND SETUP (For running remotely)
```sh
Open the following URL on browser:
https://queue-for-next-day.herokuapp.com/	-->It will show the readme.md file content
https://queue-for-next-day.herokuapp.com/next_day_queue		-->To use the tool
```


