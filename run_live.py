from engine.live_loop import start_live_loop

if __name__ == "__main__":
    # Run live loop every 5 minutes (300 seconds)
    start_live_loop(sleep_seconds=300)
