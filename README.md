CodeBot Notifier

==============

A simple script to notify about new alerts, posts and conversation messages on [CodeBot](https://www.codebot.de).

Please note that currently the script expects the website to be in German language and that it will create German notifications!



Installation

-----------------

1. Clone this repository or download it as a zip file

2. Install all required module by running

	`pip install -r requirements.txt`

3. Download [PhantomJS](http://phantomjs.org/download.html) and put it into the script directory as "phantomjs.exe"



Usage

---------

Run the script using

>`python CodebotNotifier.py`



Enter username and password. The script will now try to login.

If prompted, enter your 2FA code.



That's it, the script will now check the website every 10 seconds and will send a windows desktop notification if new content exists


