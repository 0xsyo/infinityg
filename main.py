import os
import time
import random
import requests
import json
from colorama import Fore, Style, init
from fake_useragent import UserAgent

# Initialize colorama
init(autoreset=True)

# Function to display rainbow banner
def rainbow_banner():
    os.system("clear" if os.name == "posix" else "cls")
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    banner = """
  _______                          
 |     __|.--.--.---.-.-----.---.-.
 |__     ||  |  |  _  |-- __|  _  |
 |_______||___  |___._|_____|___._|
          |_____|                   
    """
    
    for i, char in enumerate(banner):
        print(colors[i % len(colors)] + char, end="")
        time.sleep(0.007)
    print(Fore.LIGHTYELLOW_EX + "\nPlease wait...")
    time.sleep(2)
    os.system("clear" if os.name == "posix" else "cls")
    for i, char in enumerate(banner):
        print(colors[i % len(colors)] + char, end="")
    print(Fore.LIGHTYELLOW_EX)

# Load tokens from token.txt
def load_tokens():
    if not os.path.exists('token.txt'):
        print(Fore.RED + "token.txt not found!")
        exit()
    with open('token.txt', 'r') as f:
        tokens = f.read().splitlines()
    return tokens

# Save tokens to token.txt
def save_tokens(tokens):
    with open('token.txt', 'w') as f:
        for token in tokens:
            f.write(token + '\n')

# Load proxies from proxy.txt
def load_proxies():
    proxies = []
    if os.path.exists('proxy.txt'):
        with open('proxy.txt', 'r') as f:
            proxies = f.read().splitlines()
    return proxies

# Save proxies to proxy.txt
def save_proxies(proxies):
    with open('proxy.txt', 'w') as f:
        for proxy in proxies:
            f.write(proxy + '\n')

# Load headers from headers.json
def load_headers():
    if os.path.exists('headers.json'):
        with open('headers.json', 'r') as f:
            headers = json.load(f)
    else:
        headers = {}
    return headers

# Save headers to headers.json
def save_headers(headers):
    with open('headers.json', 'w') as f:
        json.dump(headers, f, indent=4)

# Generate random User-Agent
def generate_user_agent():
    ua = UserAgent()
    return ua.random

# Get user info
def get_user_info(token, proxy, user_agent):
    url = "https://api.infinityg.ai/api/v1/user/info/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": user_agent,
        "Origin": "https://www.infinityg.ai",
        "Referer": "https://www.infinityg.ai/",
    }
    proxies = {}
    if proxy:
        if proxy.startswith('http'):
            proxies['http'] = proxy
            proxies['https'] = proxy
        elif proxy.startswith('socks4') or proxy.startswith('socks5'):
            proxies['http'] = proxy
            proxies['https'] = proxy
    try:
        response = requests.post(url, headers=headers, proxies=proxies if proxy else None)
        if response.status_code == 200:
            return response.json()
        else:
            print(Fore.RED + f"Failed to fetch user info: {response.status_code}")
            return None
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return None

# Get task list
def get_task_list(token, proxy, user_agent):
    url = "https://api.infinityg.ai/api/v1/task/list"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": user_agent,
        "Origin": "https://www.infinityg.ai",
        "Referer": "https://www.infinityg.ai/",
    }
    proxies = {}
    if proxy:
        if proxy.startswith('http'):
            proxies['http'] = proxy
            proxies['https'] = proxy
        elif proxy.startswith('socks4') or proxy.startswith('socks5'):
            proxies['http'] = proxy
            proxies['https'] = proxy
    try:
        response = requests.post(url, headers=headers, proxies=proxies if proxy else None)
        if response.status_code == 200:
            return response.json()
        else:
            print(Fore.RED + f"Failed to fetch task list: {response.status_code}")
            return None
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return None

# Complete a task
def complete_task(token, proxy, user_agent, task_id):
    url = "https://api.infinityg.ai/api/v1/task/complete"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": user_agent,
        "Origin": "https://www.infinityg.ai",
        "Referer": "https://www.infinityg.ai/",
        "Content-Type": "application/json",
    }
    payload = {"taskId": task_id}
    proxies = {}
    if proxy:
        if proxy.startswith('http'):
            proxies['http'] = proxy
            proxies['https'] = proxy
        elif proxy.startswith('socks4') or proxy.startswith('socks5'):
            proxies['http'] = proxy
            proxies['https'] = proxy
    try:
        response = requests.post(url, headers=headers, json=payload, proxies=proxies if proxy else None)
        if response.status_code == 200:
            return response.json()
        else:
            print(Fore.RED + f"Failed to complete task {task_id}: {response.status_code}")
            return None
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return None

# Claim task reward
def claim_task_reward(token, proxy, user_agent, task_id):
    url = "https://api.infinityg.ai/api/v1/task/claim"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": user_agent,
        "Origin": "https://www.infinityg.ai",
        "Referer": "https://www.infinityg.ai/",
        "Content-Type": "application/json",
    }
    payload = {"taskId": task_id}
    proxies = {}
    if proxy:
        if proxy.startswith('http'):
            proxies['http'] = proxy
            proxies['https'] = proxy
        elif proxy.startswith('socks4') or proxy.startswith('socks5'):
            proxies['http'] = proxy
            proxies['https'] = proxy
    try:
        response = requests.post(url, headers=headers, json=payload, proxies=proxies if proxy else None)
        if response.status_code == 200:
            return response.json()
        else:
            print(Fore.RED + f"Failed to claim task {task_id}: {response.status_code}")
            return None
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return None

# Check-in function
def perform_checkin(token, proxy, user_agent):
    url = "https://api.infinityg.ai/api/v1/task/checkIn/"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": user_agent,
        "Origin": "https://www.infinityg.ai",
        "Referer": "https://www.infinityg.ai/",
        "Content-Type": "application/json",
    }
    proxies = {}
    if proxy:
        if proxy.startswith('http'):
            proxies['http'] = proxy
            proxies['https'] = proxy
        elif proxy.startswith('socks4') or proxy.startswith('socks5'):
            proxies['http'] = proxy
            proxies['https'] = proxy
    try:
        response = requests.post(url, headers=headers, proxies=proxies if proxy else None)
        if response.status_code == 200:
            return response.json()
        else:
            print(Fore.RED + f"Failed to check in: {response.status_code}")
            return None
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return None

# Check if already checked in today
def is_already_checked_in(task_list):
    if not task_list or task_list.get("code") != "90000" or "checkInList" not in task_list.get("data", {}):
        return False
    
    check_in_list = task_list["data"]["checkInList"]
    for check_in in check_in_list:
        # Check if today's check-in exists and status is 1 (completed)
        if "date" in check_in and "status" in check_in:
            # Get current date in the format YYYY-MM-DD
            import datetime
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            if check_in["date"] == today and check_in["status"] == 1:
                return True
    return False

# Display user info in the desired format
def display_user_info(user_info):
    print(Fore.CYAN + "━" * 50)
    print(Fore.CYAN + f"Username: {user_info['data']['userName']}")
    print(Fore.CYAN + f"InviteCode: {user_info['data']['inviteCode']}")
    print(Fore.CYAN + f"Total Points: {user_info['data']['totalPoint']}")
    print(Fore.CYAN + f"Game Point: {user_info['data']['gamePoint']}")
    print(Fore.CYAN + f"Email: {user_info['data']['email']}")
    print(Fore.CYAN + f"Telegram: {user_info['data']['telegramAccount']}")
    print(Fore.CYAN + f"Wallet: {user_info['data']['walletAddress']}")

# Display countdown timer
def display_countdown(seconds):
    for i in range(seconds, 0, -1):
        print(Fore.YELLOW + f"Waiting for {i} seconds...", end="\r")
        time.sleep(1)
    print(Fore.YELLOW + " " * 30, end="\r")  # Clear the line

# Display check-in status
def display_checkin_status(task_list):
    if not task_list or task_list.get("code") != "90000" or "checkInList" not in task_list.get("data", {}):
        return
    
    check_in_list = task_list["data"]["checkInList"]
    print(Fore.MAGENTA + "\nCheck-in Status:")
    for check_in in check_in_list:
        status = "Completed" if check_in["status"] == 1 else "Pending"
        status_color = Fore.GREEN if check_in["status"] == 1 else Fore.YELLOW
        print(f"{Fore.CYAN}Date: {check_in['date']} | Day: {check_in['checkInNo']} | Points: {check_in['point']} | Status: {status_color}{status}")

# Main function
def main():
    rainbow_banner()
    tokens = load_tokens()
    proxies = load_proxies()
    user_agents = {}
    headers_dict = load_headers()

    for idx, token in enumerate(tokens):
        print(Fore.CYAN + f"Processing account {idx + 1}")

        # Assign a proxy if available and remove it from the list
        if proxies:
            proxy = proxies.pop(0)
            save_proxies(proxies)
        else:
            proxy = None

        print(Fore.CYAN + f"Using Proxy: {proxy}")

        # Generate or reuse User-Agent
        if token not in user_agents:
            user_agents[token] = generate_user_agent()
        user_agent = user_agents[token]

        # Create headers for the token
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": user_agent,
            "Origin": "https://www.infinityg.ai",
            "Referer": "https://www.infinityg.ai/",
        }
        headers_dict[token] = headers

        # Save updated headers
        save_headers(headers_dict)

        # Fetch user info
        user_info = get_user_info(token, proxy, user_agent)
        if user_info:
            display_user_info(user_info)

        # Fetch task list
        task_list = get_task_list(token, proxy, user_agent)
        
        # Check-in process
        if task_list and task_list.get("code") == "90000":
            display_checkin_status(task_list)
            
            # Check if already checked in today
            if is_already_checked_in(task_list):
                print(Fore.GREEN + "Already checked in today!")
            else:
                print(Fore.YELLOW + "Performing daily check-in...")
                check_in_result = perform_checkin(token, proxy, user_agent)
                if check_in_result and check_in_result.get("code") == "90000":
                    print(Fore.GREEN + "Check-in successful!")
                    # Delay after check-in
                    checkin_delay = random.randint(2, 5)
                    display_countdown(checkin_delay)
                    # Refresh task list to show updated check-in status
                    task_list = get_task_list(token, proxy, user_agent)
                    if task_list and task_list.get("code") == "90000":
                        display_checkin_status(task_list)
                else:
                    print(Fore.RED + "Failed to check in.")
        
        # Process tasks
        if task_list and task_list.get("code") == "90000":
            for task_group in task_list["data"]["taskModelResponses"]:
                print(Fore.MAGENTA + f"Task Group: {task_group['taskModelName']}")
                for task in task_group["taskResponseList"]:
                    if task["status"] == 0:  # Only process incomplete tasks
                        print(Fore.YELLOW + f"Task: {task['taskName']} (ID: {task['taskId']})")
                        print(Fore.YELLOW + f"Description: {task['taskDesc']}")
                        print(Fore.YELLOW + f"Reward: {task['taskReward']} points")
                        # Complete task
                        complete_response = complete_task(token, proxy, user_agent, task["taskId"])
                        if complete_response and complete_response.get("code") == "90000":
                            print(Fore.GREEN + "Task completed successfully!")
                            # Add delay before claiming
                            claim_delay = random.randint(1, 7)
                            print(Fore.YELLOW + f"Waiting to claim reward...")
                            display_countdown(claim_delay)
                            # Claim task reward
                            claim_response = claim_task_reward(token, proxy, user_agent, task["taskId"])
                            if claim_response and claim_response.get("code") == "90000":
                                print(Fore.GREEN + "Reward claimed successfully!")
                            else:
                                print(Fore.RED + "Failed to claim reward.")
                        else:
                            print(Fore.RED + "Failed to complete task.")
                        # Add delay between tasks
                        task_delay = random.randint(1, 7)
                        print(Fore.YELLOW + f"Waiting before next task...")
                        display_countdown(task_delay)
                    else:
                        print(Fore.GREEN + f"Task already completed: {task['taskName']}")

        # Random delay between accounts
        delay = random.randint(1, 7)
        print(Fore.YELLOW + f"Waiting before next account...")
        display_countdown(delay)
        print(Fore.CYAN + "━" * 50)
    # Random looping delay between 24 hours and 24 hours 77 minutes
    loop_delay = random.randint(86400, 87420)  # 86400 seconds = 24 hours, 87420 seconds = 24 hours 77 minutes
    print(Fore.MAGENTA + f"Next loop in: {time.strftime('%H:%M:%S', time.gmtime(loop_delay))}")
    display_countdown(loop_delay)

if __name__ == "__main__":
    while True:
        main()
