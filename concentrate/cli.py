import argparse
import subprocess
import time

HOSTS_FILE = "/etc/hosts"
REDIRECT_IP = "127.0.0.1"
DISTRACTING_SITES = [
    # Social Media
    "www.facebook.com", "facebook.com",
    "www.twitter.com", "twitter.com",
    "x.com",
    "www.instagram.com", "instagram.com",
    "www.reddit.com", "reddit.com",
    "www.tiktok.com", "tiktok.com",
    "www.pinterest.com", "pinterest.com",
    "www.tumblr.com", "tumblr.com",
    "www.snapchat.com", "snapchat.com",

    # News & Media
    "www.youtube.com", "youtube.com",
    "www.netflix.com", "netflix.com",
    "www.hulu.com", "hulu.com",
    "www.disneyplus.com", "disneyplus.com",
    "www.cnn.com", "cnn.com",
    "www.bbc.com", "bbc.com",
    "www.theguardian.com", "theguardian.com",
    "www.nytimes.com", "nytimes.com",
    "news.google.com",
    "www.huffpost.com", "huffpost.com",
    "www.buzzfeed.com", "buzzfeed.com",
    "www.9gag.com", "9gag.com",

    # Shopping
    "www.ebay.com", "ebay.com",
    "www.aliexpress.com", "aliexpress.com",
    "www.wish.com", "wish.com",
]

def main():
    parser = argparse.ArgumentParser(description="Block distracting websites.")
    parser.add_argument("command", nargs="?", choices=["start", "stop"], default="start")
    parser.add_argument("--hours", type=int, default=8)
    args = parser.parse_args()

    if args.command == "start":
        start_blocking(args.hours)
    elif args.command == "stop":
        stop_blocking()

def start_blocking(hours):
    print("Starting to block distracting websites...")
    try:
        # First, run stop_blocking to clear any previous blocks
        stop_blocking(quiet=True)

        with open(HOSTS_FILE, "a") as f:
            f.write("\n# Start Concentrate Block\n")
            for site in DISTRACTING_SITES:
                f.write(f"{REDIRECT_IP} {site}\n")
            f.write("# End Concentrate Block\n")

        print(f"Distracting websites will be blocked for {hours} hours.")
        subprocess.run(["at", "now", "+", str(hours), "hours"], input="concentrate stop", text=True, capture_output=True)
    except PermissionError:
        print(f"Permission denied. Please run with sudo: sudo concentrate")
    except FileNotFoundError:
        print("Error: 'at' command not found. Please install it.")


def stop_blocking(quiet=False):
    if not quiet:
        print("Stopping blocking...")
    try:
        with open(HOSTS_FILE, "r") as f:
            lines = f.readlines()

        with open(HOSTS_FILE, "w") as f:
            in_block = False
            # Use a flag to see if we actually removed anything
            removed_something = False
            new_lines = []
            for line in lines:
                if line.strip() == "# Start Concentrate Block":
                    in_block = True
                    removed_something = True
                    continue
                elif line.strip() == "# End Concentrate Block":
                    in_block = False
                    continue
                
                if not in_block:
                    new_lines.append(line)
            
            # Clean up trailing newlines
            while new_lines and new_lines[-1] == '\n':
                new_lines.pop()

            f.writelines(new_lines)
            # Add a single newline at the end if the file is not empty
            if new_lines:
                f.write('\n')


        if not quiet:
            if removed_something:
                print("Distracting websites unblocked.")
            else:
                print("No active block found.")

    except PermissionError:
        if not quiet:
            print(f"Permission denied. Please run with sudo: sudo concentrate stop")

if __name__ == "__main__":
    main()
