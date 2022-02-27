# Google-Tasks-Automation-Bot

## This is a Google Tasks bot that I created for the arduous task of creating a weekly task list for myself every week and having to write down the tasks (namy of them repeated) every night before bed for the next day. I found myself forgetting to do this a lot and slacking off as a result, so I decided to see if I could automate the process with a bot.
<br>

## This bot is pretty simple in terms of what it does: it interacts with Google's Tasks API, doing a series of INSERT and GET requests to populate new tasks and task lists every Sunday night at 8 pm (this is done via the Scheduler package). The bot reads my usual preset tasks and weekly template from local JSON files and writes them to Google Tasks.
<br>

## I hope to make this bot more advanced in the future as I figure out what I like and don't like about it
<br>

## If you want to try this bot for yourself, clone this repository and cd into it. After that run ```pip install -r requirements.txt```, the requirements.txt file containing all dependencies needed to run the bot.
<br>

## A special shoutout to Jie Jenn on YouTube, whose tutorial I followed to get familar with using the Tasks API before I started this project. Also, I used his Google.py file to create the connection object for Google's APIs, so have to give credit for this as well! You can check Jie Jenn out [here](https://www.youtube.com/channel/UCvVZ19DRSLIC2-RUOeWx8ug)