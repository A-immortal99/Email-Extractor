import sys
import re
import os
import time
import math
import platform

from concurrent.futures import ThreadPoolExecutor, as_completed

def set_title(title):
    if platform.system() == 'Windows':
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        sys.stdout.write(f"\x1b]2;{title}\x07")
        sys.stdout.flush()

def convert_size(size_bytes):
    """
    Convert size in bytes to human-readable format
    """
    if size_bytes == 0:
        return "0 bytes"
    # Define suffixes
    suffixes = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    # Calculate index of appropriate suffix
    i = int(math.floor(math.log(size_bytes, 1024)))
    # Calculate size in appropriate unit
    p = math.pow(1024, i)
    size = round(size_bytes / p, 2)
    return "{} {}".format(size, suffixes[i])

def count_total_lines(input_file):
    """
    Count total lines in the input file.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)

def seconds_to_hours_minutes(seconds):
    """
    Convert seconds to hours and minutes.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return hours, minutes, seconds

def progress_bar(current, total, bar_length=90):
    """
    Generate a progress bar.
    """
    progress = current / total
    arrow = '>' * int(progress * bar_length)
    spaces = ' ' * (bar_length - len(arrow))
    return f'[{arrow.ljust(bar_length)}] {int(progress * 100)}%'

def source_file_summary(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        num_lines = sum(1 for line in f)
    print("\033[96mSource file:\033[0m", input_file)
    print("\033[96mSize:\033[0m", convert_size(os.path.getsize(input_file)))
    print("\033[96mTotal Lines:\033[0m", num_lines)
    print()  # Add a blank line
    return num_lines

def extract_emails(input_file, output_file):
    total_lines = count_total_lines(input_file)
    set_title("Email Extractor")

    # Open the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regular expression pattern to match email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    # Extract email addresses from the content
    emails = re.findall(email_pattern, content)

    # Remove duplicates using set and sort by domain
    unique_emails = sorted(set(emails), key=lambda x: x.split('@')[1])

    # Write the sorted unique email addresses to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        total_emails = len(unique_emails)
        valid_emails = 0
        start_time = time.time()
        for i, email in enumerate(unique_emails, 1):
            f.write(email + '\n')
            valid_emails += 1

            # Print progress bar and ETA
            elapsed_time = time.time() - start_time
            avg_time_per_email = elapsed_time / i if i > 0 else 0
            remaining_emails = total_emails - i
            estimated_remaining_time = remaining_emails * avg_time_per_email
            remaining_hours, remaining_minutes, remaining_seconds = seconds_to_hours_minutes(estimated_remaining_time)
            eta_str = f"{remaining_hours}h {remaining_minutes}m {remaining_seconds}s" if remaining_hours > 0 else f"{remaining_minutes}m {remaining_seconds}s"
            print(f"{progress_bar(i, total_emails)} ETA: {eta_str}", end='\r')

    print()  # Add a newline after progress bar
    print("\n\033[92mTask completed.\033[0m\n")
    print("\033[96mOutput file:\033[0m", output_file)
    print("\033[96mSize:\033[0m", convert_size(os.path.getsize(output_file)))
    print("\033[96mTotal Lines:\033[0m", total_emails)
    print("\033[96mRemoved Duplicates:\033[0m", len(emails) - len(unique_emails))
    print()  # Add a blank line

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\033[94m")
        print(r"""
          ______                       _   _     ______          _                           _                  
         |  ____|                     (_) | |   |  ____|        | |                         | |                 
         | |__     _ __ ___     __ _   _  | |   | |__    __  __ | |_   _ __    __ _    ___  | |_    ___    _ __ 
         |  __|   | '_ ` _ \   / _` | | | | |   |  __|   \ \/ / | __| | '__|  / _` |  / __| | __|  / _ \  | '__|
         | |____  | | | | | | | (_| | | | | |   | |____   >  <  | |_  | |    | (_| | | (__  | |_  | (_) | | |   
         |______| |_| |_| |_|  \__,_| |_| |_|   |______| /_/\_\  \__| |_|     \__,_|  \___|  \__|  \___/  |_| 
          
                             https://t.me/A_immortal99  -  https://github.com/A-immortal99""")
        print()  # Add some empty lines
        # Tip information
        print("\033[96mTip:\033[0m If you found this script helpful, consider buying me a coffee as a token of appreciation:")
        print()  # Add some empty lines
        print("          - BTC: 1JtGqVD9xyQzrdbPpoBB4QjGoGxqhQMmCo")
        print("          - USDT (TRC 20): TAMLo5m9qKQpqQao1Qk4ZH3xRwkLw5Q2Vj")
        print("          - ETH: 0x6e82b2bc4132050b31b0bb2dbb0cfd600ba949f7\n")
        print("\n")  # Add some empty lines
        print("\033[91mPlease drag and drop the source file onto this script file.\033[0m")
        input("\n\033[94mPress Enter to exit...\033[0m\n")
        sys.exit(1)

    input_file = sys.argv[1]
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_emails{ext}"

    print("\033[94m")
    print(r"""
          ______                       _   _     ______          _                           _                  
         |  ____|                     (_) | |   |  ____|        | |                         | |                 
         | |__     _ __ ___     __ _   _  | |   | |__    __  __ | |_   _ __    __ _    ___  | |_    ___    _ __ 
         |  __|   | '_ ` _ \   / _` | | | | |   |  __|   \ \/ / | __| | '__|  / _` |  / __| | __|  / _ \  | '__|
         | |____  | | | | | | | (_| | | | | |   | |____   >  <  | |_  | |    | (_| | | (__  | |_  | (_) | | |   
         |______| |_| |_| |_|  \__,_| |_| |_|   |______| /_/\_\  \__| |_|     \__,_|  \___|  \__|  \___/  |_| 
          
                             https://t.me/A_immortal99  -  https://github.com/A-immortal99""")
    print()  # Add some empty lines
    # Tip information
    print("\033[96mTip:\033[0m If you found this script helpful, consider buying me a coffee as a token of appreciation:")
    print()  # Add some empty lines
    print("          - BTC: 1JtGqVD9xyQzrdbPpoBB4QjGoGxqhQMmCo")
    print("          - USDT (TRC 20): TAMLo5m9qKQpqQao1Qk4ZH3xRwkLw5Q2Vj")
    print("          - ETH: 0x6e82b2bc4132050b31b0bb2dbb0cfd600ba949f7\n")

    time.sleep(3)
    source_lines = source_file_summary(input_file)

    extract_emails(input_file, output_file)

    input("\n\033[94mPress Enter to exit...\033[0m\n")
