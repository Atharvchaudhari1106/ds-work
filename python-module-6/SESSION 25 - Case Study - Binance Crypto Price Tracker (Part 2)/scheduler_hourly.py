import time
import schedule
from crypto_tracker_part2 import run_pipeline

def job():
    print(f"\n[CRON] Scheduled execution triggered at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    run_pipeline()

def start_scheduler(run_now=True):
    """
    Task 5:
    Automates the crypto data fetch and analysis by scheduling the script
    to run every hour using the `schedule` library.
    """
    print("=" * 65)
    print("⏰ BINANCE CRYPTO TRACKER HOURLY SCHEDULER STARTED")
    print("=" * 65)
    print("Schedule configured: Every 1 hour.")
    print("Press Ctrl+C to stop the scheduler.")
    
    # Schedule job every hour
    schedule.every(1).hours.do(job)

    # Optionally run immediately once upon launch
    if run_now:
        print("\n[INIT] Performing initial analysis run...")
        job()

    # Loop to check pending scheduled tasks
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[STOPPED] Scheduler terminated by user.")

if __name__ == "__main__":
    # For demonstration, runs initial job and awaits the hourly schedule
    start_scheduler(run_now=True)
