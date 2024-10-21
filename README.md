# ActivityWatch - Daily export to markdown

This Python script fetches [ActivityWatch](https://github.com/ActivityWatch/activitywatch) usage data via its API, processes it to calculate total computer usage time and the top 20 applications, and saves the output in both Markdown and JSON formats. The script uses an `.env` file to specify the save location and automatically overwrites the file for the same day with the latest data.

Most suitable for macOS and Linux desktops.

## Features

- Fetches ActivityWatch data using `curl`.
- Calculates the total computer usage time for the day.
- Lists the top 20 applications by usage time.
- Saves the output in both Markdown and JSON files, dated as `YYYY-MM-DD.md` and `YYYY-MM-DD.json`.
- Uses the hostname of the machine in the report.
- Automatically updates the report for the same day to avoid duplicates.

## Requirements

- Python 3.x
- ActivityWatch installed and running
- `python-dotenv` for environment variable management

## Installation

1. Clone the repository and navigate to the project folder.
2. Install the required Python libraries:

    ```bash
    pip3 install -r requirements.txt
    ```

    on macOS:

    ```bash
    python3 -m venv path/to/venv
    source path/to/venv/bin/activate
    python3 -m pip install python-dotenv
    ```

3. Create a `.env` file in the project directory with the following content:

    ```bash
    SAVE_DIRECTORY=/path/to/your/save/directory
    ```

4. Modify the script to point to the correct URL for the ActivityWatch API (this is based on your hostname).

## Usage

Run the script to generate the daily summary:

```bash
python3 process.py
```

## Cron job

To automate the process, you can set up a cron job to run the script daily. Open the crontab editor with:

```bash
crontab -e
```

Add the following line to run the for every 1 minute:

```bash
* * * * * /usr/bin/python3 /path/to/process.py >/dev/null 2>&1
```

Or use the cron.sh provided for venv.

```bash
* * * * * /bin/bash /path/to/cron.sh >/dev/null 2>&1
```