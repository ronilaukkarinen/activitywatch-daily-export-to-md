import json
from collections import defaultdict
from datetime import datetime
import socket
import os
from dotenv import load_dotenv
import subprocess

# Load .env file
load_dotenv()

# Get the save directory from .env file
save_directory = os.getenv("SAVE_DIRECTORY")

# Get today's date and the current time for timestamp
today_str = datetime.now().strftime("%Y-%m-%d")
current_time = datetime.now().strftime("%H:%M:%S")

# Get the hostname of the machine
hostname = socket.gethostname()

# Fetch the ActivityWatch data using curl
aw_url = f"http://localhost:5600/api/0/buckets/aw-watcher-window_{hostname}/events"
response = subprocess.run(['curl', '-s', aw_url], capture_output=True, text=True)

# Check if the response is valid JSON
try:
    data = json.loads(response.stdout)
except json.JSONDecodeError:
    print("Error: Failed to fetch or parse ActivityWatch data.")
    exit(1)

# If no events were returned, print an error message
if not data:
    print("No events found.")
    exit(0)

# Create dictionary to store the process times
process_times = defaultdict(float)
total_time = 0

# Loop through events and calculate times
for event in data:
    # Extract the timestamp and ensure it's for today
    timestamp = event['timestamp']
    event_date = timestamp.split('T')[0]  # Extract the date part of the timestamp

    if event_date == today_str:
        # Get the duration from the event
        duration = event.get('duration', 0)

        # Get the app name (default to 'Unknown' if not present)
        process_name = event['data'].get('app', 'Unknown')

        # Store the process time
        process_times[process_name] += duration
        total_time += duration

# Sort the processes by time (from highest to lowest)
sorted_process_times = sorted(process_times.items(), key=lambda item: item[1], reverse=True)

# Prepare the markdown content
md_content = f"# ActivityWatch Summary for {today_str} ({hostname})\n\n"
md_content += f"**Total time spent on computer**: {total_time / 3600:.2f} hours. "
md_content += f"File saved at {current_time}.\n\n"
md_content += "## Top 20 processes\n\n"

for process, time in sorted_process_times[:20]:
    md_content += f"- **{process}**: {time / 3600:.2f} hours\n"

# Define the file path for markdown (hostname-yyyy-mm-dd.md)
md_file_path = os.path.join(save_directory, f"{hostname}-{today_str}.md")

# Save the markdown file
with open(md_file_path, "w") as f:
    f.write(md_content)

print(f"Markdown summary saved to: {md_file_path}")

# Prepare JSON data
json_data = {
    "date": today_str,
    "hostname": hostname,
    "total_time_hours": total_time / 3600,
    "top_processes": [
        {"process": process, "time_hours": time / 3600}
        for process, time in sorted_process_times[:20]
    ]
}

# Define the file path for JSON as markdown (hostname-yyyy-mm-dd.json.md)
json_md_file_path = os.path.join(save_directory, f"{hostname}-{today_str}.json.md")

# Save the JSON as markdown with ```json block
with open(json_md_file_path, "w") as f:
    f.write(f"```json\n{json.dumps(json_data, indent=4)}\n```")

print(f"JSON summary saved as markdown to: {json_md_file_path}")
