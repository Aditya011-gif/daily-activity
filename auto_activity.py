#!/usr/bin/env python3
import os
import random
import subprocess
from datetime import datetime, timedelta

USER_NAME = os.getenv("GIT_USER_NAME", "Aditya")
USER_EMAIL = os.getenv("GIT_USER_EMAIL", "adityajaspal04@gmail.com")
# Set to 50 commits per day by default
COMMITS_COUNT = int(os.getenv("COMMITS_COUNT", "50"))
SKIP_WEEKENDS = os.getenv("SKIP_WEEKENDS", "false").lower() in ("true", "1", "yes")

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}\n{result.stderr}")
    return result

def main():
    now = datetime.now()
    
    # Skip weekends if requested
    if SKIP_WEEKENDS and now.weekday() >= 5:
        print(f"Skipping commits today ({now.strftime('%A')}) because SKIP_WEEKENDS is enabled.")
        return

    num_commits = max(1, COMMITS_COUNT)
    print(f"Generating {num_commits} commits for {now.strftime('%Y-%m-%d')}...")

    # Configure Git Author
    run_cmd(f'git config user.name "{USER_NAME}"')
    run_cmd(f'git config user.email "{USER_EMAIL}"')

    activity_file = "ACTIVITY.md"
    
    # Spread commit timestamps over the day for realistic contribution spread
    base_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
    
    for i in range(num_commits):
        # Stagger commit times every few minutes across the day
        commit_date = base_time + timedelta(minutes=i * 12 + random.randint(1, 5))
        formatted_date = commit_date.strftime("%Y-%m-%d %H:%M:%S")
        
        entry = f"- Contribution #{i + 1}/{num_commits} recorded on {formatted_date}\n"
        
        with open(activity_file, "a", encoding="utf-8") as f:
            f.write(entry)
            
        run_cmd(f"git add {activity_file}")
        # Commit with specific date and message
        run_cmd(f'git commit --date="{formatted_date}" -m "Contribution update #{i + 1} - {formatted_date}"')

    print(f"Successfully generated and recorded {num_commits} commits!")

if __name__ == "__main__":
    main()
