import argparse
import subprocess
import time

HOSTS_FILE = "/etc/hosts"
REDIRECT_IP = "127.0.0.1"
DISTRACTING_SITES = [
    # Social Media & Forums
    "www.facebook.com", "facebook.com", "m.facebook.com", "touch.facebook.com",
    "www.twitter.com", "twitter.com", "x.com", "mobile.twitter.com",
    "www.instagram.com", "instagram.com", "m.instagram.com",
    "www.reddit.com", "reddit.com", "old.reddit.com", "new.reddit.com", "np.reddit.com",
    "www.tiktok.com", "tiktok.com", "m.tiktok.com",
    "www.pinterest.com", "pinterest.com", "m.pinterest.com",
    "www.tumblr.com", "tumblr.com",
    "www.snapchat.com", "snapchat.com", "story.snapchat.com",
    "www.linkedin.com", "linkedin.com", # Can be distracting
    "www.quora.com", "quora.com",
    "www.discord.com", "discord.com", "discordapp.com",

    # News & Media
    "www.youtube.com", "youtube.com", "m.youtube.com", "music.youtube.com", "gaming.youtube.com",
    "www.netflix.com", "netflix.com",
    "www.hulu.com", "hulu.com",
    "www.disneyplus.com", "disneyplus.com",
    "www.amazon.com", "amazon.com", "www.amazon.co.uk", "smile.amazon.com", # Shopping part of amazon
    "www.primevideo.com", "primevideo.com",
    "www.twitch.tv", "twitch.tv", "m.twitch.tv",
    "www.cnn.com", "cnn.com", "edition.cnn.com",
    "www.bbc.com", "bbc.com", "www.bbc.co.uk", "news.bbc.co.uk",
    "www.theguardian.com", "theguardian.com",
    "www.nytimes.com", "nytimes.com",
    "news.google.com",
    "www.huffpost.com", "huffpost.com",
    "www.buzzfeed.com", "buzzfeed.com",
    "www.9gag.com", "9gag.com", "m.9gag.com",
    "www.espn.com", "espn.com",
    "bleacherreport.com",
    "www.foxnews.com", "foxnews.com",
    "www.msnbc.com", "msnbc.com",
    "www.dailymail.co.uk", "dailymail.co.uk",

    # Shopping
    "www.ebay.com", "ebay.com",
    "www.aliexpress.com", "aliexpress.com",
    "www.wish.com", "wish.com",
    "www.craigslist.org", "craigslist.org",
    "www.etsy.com", "etsy.com",
    "www.walmart.com", "walmart.com",
    "www.target.com", "target.com",
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
        # Ask for confirmation
        while True:
            response = input("Are you sure you want to stop blocking? (y/n): ").lower()
            if response in ["y", "yes"]:
                break
            elif response in ["n", "no"]:
                print("Aborted.")
                return

    if not quiet:
        print("Stopping blocking...")
    try:
        with open(HOSTS_FILE, "r") as f:
            lines = f.readlines()

        # This flag will track if we made any changes
        made_changes = False

        # First, remove the marked block
        new_lines = []
        in_block = False
        for line in lines:
            if line.strip() == "# Start Concentrate Block":
                in_block = True
                made_changes = True # We are about to make a change
                continue
            elif line.strip() == "# End Concentrate Block":
                in_block = False
                continue
            if not in_block:
                new_lines.append(line)

        # Now, filter the remaining lines to remove any old entries
        # that might not have been in a marked block.
        final_lines = []
        for line in new_lines:
            # Check if the line contains any of the distracting sites
            if any(f" {site}" in line for site in DISTRACTING_SITES):
                made_changes = True # We are about to make a change
                continue
            final_lines.append(line)

        # Clean up trailing newlines
        while final_lines and final_lines[-1].strip() == "":
            final_lines.pop()

        # Write the cleaned content back to the file
        with open(HOSTS_FILE, "w") as f:
            f.writelines(final_lines)
            # Add a single newline at the end if the file is not empty
            if final_lines:
                f.write('\n')

        if not quiet:
            if made_changes:
                print("Distracting websites unblocked.")
            else:
                print("No active block found.")

    except PermissionError:
        if not quiet:
            print(f"Permission denied. Please run with sudo: sudo concentrate stop")

if __name__ == "__main__":
    main()
