# Student Daily Planner

A simple web application for students to plan their day effectively. It lets you combine your **academic timetable** with **extracurricular activities**, then save the timetable to **Google Calendar** (via ICS) or **save as PDF**.

## Features

- **Academic timetable** — Set your weekly class hours (start/end time per day). These appear as grey, blocked slots on the timetable.
- **Extracurricular activities** — Choose up to 10 activities (e.g. Studying, Workout, Reading, Meditation, Coding, Walk, etc.). The app can auto-fill them into your free slots.
- **Editable weekly grid** — View and edit a 8:00–21:00 weekly grid. Grey cells = class time; white cells = free time. Fill activities randomly, edit by hand, or enable “Grey Edit” to add class details in grey cells.
- **Save to Google Calendar** — Export your timetable as an **ICS file** (Sync to Google). Choose how many weeks (1–52) to export, then import the `.ics` file into Google Calendar.
- **Save as PDF** — Use **Save as PDF** to open the print dialog; choose “Save as PDF” (or print) to keep a copy of your timetable.

## Tech stack

- **Backend:** Django 5.x  
- **Database:** SQLite (default)  
- **Auth:** Django’s built-in user registration and login  

## Quick start

1. **From the project root**, create a virtual environment and install dependencies:

   ```bash
   cd student-daily-planner-web-app-main
   python -m venv venv
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

2. **Run migrations and start the server:**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

3. Open **http://127.0.0.1:8000/** in your browser. Register, log in, then:
   - Set your **Preferences** (class times per day),
   - Select **Activities**,
   - Build and edit your **Final Timetable**,
   - Use **Sync to Google (ICS)** or **Save as PDF** as needed.

## Project structure

- `config/` — Django project config (settings, URLs, WSGI/ASGI).
- `planner/` — Main app: models (UserProfile, UserPreference, Activity), views, templates, static files.
- `manage.py` — At project root.

## Clear the database

To reset all data (users, preferences, activities, timetable data):

1. Stop the server if it is running.
2. Delete the database file: remove `db.sqlite3` from the project root.
3. Run migrations again: `python manage.py migrate`.

A new empty database will be created.

## How export works

- **Google Calendar:** The “Sync to Google (ICS)” button downloads a `.ics` file. In Google Calendar: **Settings → Import & export → Import** and upload the file. Events are generated from your class windows and selected activities for the chosen number of weeks.
- **PDF:** “Save as PDF” triggers the browser print dialog; use “Save as PDF” (or “Print to PDF”) to get a PDF of the current timetable view.
