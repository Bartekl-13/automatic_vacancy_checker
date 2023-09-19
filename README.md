# Automatic registration for OGUN courses

This is a python-based application. It's functionality focuses on checking for vacant spots on the University of Warsaw registration site for OGUNs, language courses and PE.

### SETUP

To use this app you need to download it onto your computer ( or pull from github into a local repository ).\
Then, fill our four variables that need to be defined:

1. YOUR_USERNAME, where you write your PESEL number (which is usually a username for USOS Rejestracje Żetonowe )
2. YOUR_PASSWORD, where you write your password for USOS ( remember to not share the file with your password in it! )
3. INTERVAL, which is set to 1 hour as a default, it allows you to change the interval after which the site is scraped to check if there are free spots to register
4. course_url, where you paste the https://..... url for the course that you want to sign up for

If you don't have python installed go to this page:
https://www.python.org/downloads/windows/
and choose the latest release for your device.

After filling out those variables you need to open command line on your device by using shortcut WINDOWS+R and writing _cmd_ in there, or just searching it in the Windows tab.\
In your terminal you need to run the following command to install packages necessary for the program to run:

> pip install selenium pymsgbox\
The pip command should authomatically install along with Python.

Then navigate to the directory your webscrape.py file was downloaded for example:\
\
cd path/to/your/script/directory\
\
And run the script using the following command:\
python webscrape.py
\
New Google Chrome window should pop up, and if everything works correctly you will be logged in and you will get a notification with a prompt telling you if you were registered, or that there is no vacancies. Now you have to wait for INTERVAL seconds to get another notification.\
\
If you wish to run this app for multiple different courses, just copy-paste the webscrape.py file, change it name (for ex. webscrape2.py) and inside change the URL to the URL of your another class of interest.
