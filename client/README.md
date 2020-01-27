# Capstone Project - Scheduler

### About:

This application will allow users to save events that include the name of the event, when it takes place, and a short description of what the event is about. Users may also look up what time it is currently in different timezones.

### Features:

- Displays all events for the user currently logged in.

- Events can be deleted from the list displayed when a user is logged in.

- Automatically converts and stores datetime objects from the user input into UTC and then reconverts datetime data to be displayed in the local time of the device viewing it when retrieved.

## Getting started:

First, fork the github repository.

### Prerequisits:

You'll need the following installed.

- node(v10.16.3)

- python(3.7.1)

- Web browser such as chrome or firefox

### Running locally:

- You'll need to create a .env file to connect to a database. It should include the following fields:
~~~~
DB_USER=(the user responsible for your database)
DB_PASS=(password to grant access to your database)
DB_URL=(directory to your database)
DB_NAME=(name of your database)
~~~~
Keep in mind the application is currently intended to make use of AWS RDS - Postgres database.

- From the root directory, navigate to the **client** folder and run
~~~~
npm run build
~~~~
The application will automatically watch for changes and update them.

- Next navigate back to the root directory and then to the **server** directory. Run
~~~~
pipenv run python main.py
~~~~
Or alternatively, depending on how you installed python, you may have to run
~~~~
pipenv run python3 main.py
~~~~

- In your browser, navigate to *http://localhost:5000/*

### Caveats:

There is currently a known issue where axios responses don't always execute the code as expected. Sometimes the displayed list of events wont update when expected. An "Update my events" button was added to relieve this.

Sometimes hitting the "Delete event" button malfunctions. Refreshing the page will restore it's functionality.

### Next steps:

This application could use a round of bug fixes to improve the responsiveness of expected results.

The current user system is crude and insecure. Adding authentication would be necissary before deploying publicly.

Improved layout and manual display options would greatly enhance the user experience for this application

Graphical display for events would also improve user experience.

Adding location information to each event would greatly improve practical uses in the real world.

Adding more control over timezone information is also practical.

Sharing events between users is a very useful feature to include after the previous changes have been made.

## Deployment configuration: