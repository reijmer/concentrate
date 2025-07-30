import argparse
import subprocess
import time
import os

HOSTS_FILE = "/etc/hosts"
REDIRECT_IP = "127.0.0.1"

def get_distracting_sites():
    # Get the path to the blocked_sites.txt file within the package
    package_dir = os.path.dirname(__file__)
    file_path = os.path.join(package_dir, "blocked_sites.txt")
    with open(file_path, "r") as f:
        # Read lines, filter out comments and empty lines
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

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

        distracting_sites = get_distracting_sites()
        with open(HOSTS_FILE, "a") as f:
            f.write("\n# Start Concentrate Block\n")
            for site in distracting_sites:
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
        distracting_sites = get_distracting_sites()
        final_lines = []
        for line in new_lines:
            # Check if the line contains any of the distracting sites
            if any(f" {site}" in line for site in distracting_sites):
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
