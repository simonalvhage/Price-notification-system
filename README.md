# Price Notifier

Simple price notifier, written in Python, mySQL and HTML (Bootstrap 4)

## Description

A simple insertion form is presented to the user were the user can enter a link to the product he/she wants to follow. The user can also choose how much percentage the product must drop to trigger the notification script. The user also inserts his/hers email and submittes. If the mail is not in the database yet, a password will be generated to the user. This is used for deleting all the records. 

If the product-url is new, it gets inserted into the database and also the basic info like title, price, picture-url gets webscraped and also inserted to the same user record. The script is setup on my computer so the main.py script is runned 3 times everyday. The main.py script loops through all records (all prodcuts) and compares the price in the database with the newly webscraped price. If the webscraped price is less than the database price (or with the factor given), a notification email will be sent and the database will be updated.

The delete tab on the website will remove every record with the given email.

Everything is hosted with Flask.

## Getting Started

### Dependencies

Prerequisites: mysql, smtplib, ssl, email.mime

### Installing

Just run Web.py to host the website and its scripts. To check if there are new prices the main.py must me excecuted. I recommend at least one time a day.
I will also give a tutorial below on taskscheduling on ubuntu below.

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
Go fuck yourself
```

## Authors

Contributors names and contact info

Simon Alvhage

## License

This project is free to use but please buy me a coffee 

## Acknowledgments

Inspiration, code snippets, etc.
