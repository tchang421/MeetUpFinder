[![Build Status](https://travis-ci.com/uva-cs3240-f20/project-2-09.svg?token=dvwuMneQ9nxFNgioAUy2&branch=master)](https://travis-ci.com/uva-cs3240-f20/project-2-09)
# Project
This is the project for CS 3240: Advanced Software Development.

## Before you start
1. [Initialize](https://docs.python.org/3/library/venv.html) a virtural environment at \<project\>/venv
2. activate the virtual environment
3. run `pip install -r requirements.txt`

## Before opening a PR
1. If you have added new dependencies, run `pip freeze > requirements.txt`, commit and push the changes to requirements.txt

## Main Features to Note
1. Event Creation: Create event through "create event" button on home page.
2. Login: Google Login Required. Must be logged in to create, edit, delete events.
3. View: List of created events on the home page. 
4. Sorting: Sort events by date, type, or publish time using the "sort by" drop down menu.
5. Viewing Event: Click on the name of an event to visit its individual page. All infomation about the event is displayed on this page. 
6. Map and Directions: Each event has a map feature that pins its location on a map. You can move around or zoom on the map. There is also a "get directions" link that opens a link to google maps.
7. Edit and Delete: Click on an event you have created to and scroll down. There are two buttons giving you the option to edit or delete your event.
8. Profiles: Click on an event creator's name to view their profile. Click on your own name in the top right corner to view or edit your profile. 