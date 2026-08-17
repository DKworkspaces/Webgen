import subprocess
import time

RUN_TIME = 5 * 60 * 60  # Exactly 5 hours in seconds
SLEEP_TIME = 10  # 10 seconds

if __name__ == "__main__":
  print("Starting Flask app for a single 5-hour run...")
  # Start the Flask server as a background subprocess
  process = subprocess.Popen(["python", "app.app.py"])

  # Let it run for exactly 5 hours
  time.sleep(RUN_TIME)

  print("5 hours reached. Stopping Flask app...")
  # Safely terminate the Flask process
  process.terminate()
  process.wait()

  print("Waiting 10 seconds before final exit...")
  time.sleep(SLEEP_TIME)

  print("Execution complete. Process stopped entirely.")
  
