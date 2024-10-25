import subprocess
import time
import sys

def run_script(script_name):
    return subprocess.Popen([sys.executable, script_name])

def main():
    print("Starting Avrioc system...")

    # Start data generator
    print("Starting data generator...")
    data_generator = run_script('data_generator.py')

    # Start consumer and aggregator
    print("Starting consumer and aggregator...")
    consumer_aggregator = run_script('consumer_aggregator.py')

    # Start dashboard
    print("Starting dashboard...")
    dashboard = run_script('dashboard.py')

    print("All components started. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all components...")
        data_generator.terminate()
        consumer_aggregator.terminate()
        dashboard.terminate()
        print("All components stopped. Avrioc system shut down.")

if __name__ == "__main__":
    main()
