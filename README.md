# The Class Register

A simple school register app built with Flet. Teachers can add, edit and
remove students and mark them present or absent. Data is saved to a JSON file.

## Features

- Add a student (with validation: all fields required, grade 1-12)
- Edit a student (replaces their details)
- Delete a student (with confirmation)
- Mark attendance with a checkbox
- Data saved in `students.json`

## How to run

1. Install Python and Flet: `pip install flet`
2. In the project folder, run: `flet run`

## Files

- `main.py` - the Flet views, routing and theme
- `models.py` - the Student class and JSON saving/loading
- `students.json` - saved student data
- `assets/` - background image
