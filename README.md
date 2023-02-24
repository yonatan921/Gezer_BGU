# Gezer Bot

Gezer Bot is a Python script that uses Selenium to automate the process of downloading exams from the Gezer website.

## Requirements

To run the Gezer Bot script, you must have the following packages installed:

- Chrome WebDriver
- Selenium

You can install the required packages using the following command:

pip install -r requirements.txt

## Usage

To use the Gezer Bot script, run the following command:

python Gezer_bot.py  {username} {password} {id} {course_id} {moed}

- `<username>` - Your Gezer username
- `<password>` - Your Gezer password
- `<id>` - Your ID
- `<cours_id>` - The ID of the course the exam is for
- `<moed>` - The moed (exam session) of the exam (e.g. A, B, C, etc.)

For example:

python ./Gezer_bot.py johndoe mypassword 12345 67890 B

The script will then automate the process of logging in to the Gezer website, navigating to the exam page, and downloading the exam. The downloaded exam will be saved to your current working directory.
