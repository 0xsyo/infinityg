import os
import time
import random
import requests
import json
from colorama import Fore, Style, init
from fake_useragent import UserAgent
from web3 import Web3

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

# Load private keys from pk.txt
def load_private_keys():
    if not os.path.exists('pk.txt'):
        print(Fore.RED + "pk.txt not found!")
        exit()
    with open('pk.txt', 'r') as f:
        private_keys = f.read().splitlines()
    return private_keys

# Save tokens to tokens.json
def save_token(wallet_address, token):
    try:
        with open('tokens.json', 'r') as f:
            tokens = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tokens = {}
    tokens[wallet_address] = token
    with open('tokens.json', 'w') as f:
        json.dump(tokens, f, indent=4)

# Load proxies from proxy.txt
def load_proxies():
    proxies = []
    if os.path.exists('proxy.txt'):
        with open('proxy.txt', 'r') as f:
            proxies = f.read().splitlines()
    return proxies

# Get random proxy
def get_proxy():
    proxies = load_proxies()
    if proxies:
        proxy = random.choice(proxies)
        return proxy
    return None

# Format proxy for requests
def format_proxy(proxy):
    if not proxy:
        return None
    proxies = {}
    if proxy.startswith('http'):
        proxies['http'] = proxy
        proxies['https'] = proxy
    elif proxy.startswith('socks4') or proxy.startswith('socks5'):
        proxies['http'] = proxy
        proxies['https'] = proxy
    return proxies if proxies else None

# Generate or get headers for wallet
def get_headers(wallet_address):
    try:
        with open('headers.json', 'r') as f:
            headers = json.load(f)
            if wallet_address in headers:
                return headers[wallet_address]
    except (FileNotFoundError, json.JSONDecodeError):
        headers = {}
    
    # Generate new headers
    ua = UserAgent()
    new_headers = {
        'User-Agent': ua.random,
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'id-ID,id;q=0.5',
        'Content-Type': 'application/json',
        'Origin': 'https://www.infinityg.ai',
        'Referer': 'https://www.infinityg.ai/',
    }
    
    # Save to headers.json
    headers[wallet_address] = new_headers
    with open('headers.json', 'w') as f:
        json.dump(headers, f, indent=4)
    
    return new_headers

# Login with wallet and get token
def login_and_get_token(private_key):
    url = 'https://api.infinityg.ai/api/v1/user/auth/wallet_login'
    # Derive wallet address from private key using web3.py
    w3 = Web3()
    account = w3.eth.account.from_key(private_key)
    wallet_address = account.address
    
    payload = {
        "loginChannel": "MAIN_PAGE",
        "walletChain": "Ethereum",
        "walletType": "metamask",
        "walletAddress": wallet_address
    }
    
    headers = get_headers(wallet_address)
    proxy = get_proxy()
    proxies = format_proxy(proxy)
    
    print(Fore.CYAN + f"Attempting login for wallet: {wallet_address[:10]}...")
    print(Fore.CYAN + f"Using Proxy: {proxy if proxy else 'None'}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, proxies=proxies)
        if response.status_code == 200 and response.json().get('code') == '90000':
            print(Fore.GREEN + "Login successful.")
            token = response.json().get('data', {}).get('token')
            if token:
                save_token(wallet_address, token)
                return token, wallet_address, headers
            else:
                print(Fore.RED + "Token not found in response.")
        else:
            print(Fore.RED + f"Login failed with status code {response.status_code}. Response: {response.text}")
    except Exception as e:
        print(Fore.RED + f"Error during login: {e}")
    
    return None, wallet_address, headers

# Get user info
def get_user_info(token, headers, proxy):
    url = "https://api.infinityg.ai/api/v1/user/info/query"
    auth_headers = headers.copy()
    auth_headers["Authorization"] = f"Bearer {token}"
    
    proxies = format_proxy(proxy)
    
    try:
        response = requests.post(url, headers=auth_headers, proxies=proxies)
        if response.status_code == 200:
            return response.json()
        else:
            print(Fore.RED + f"Failed to fetch user info: {response.status_code}")
            return None
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return None

# Get task list
def get_task_list(token, headers, proxy):
    url = "https://api.infinityg.ai/api/v1/task/list"
    auth_headers = headers.copy()
    auth_headers["Authorization"] = f"Bearer {token}"
    
    proxies = format_proxy(proxy)
    
    try:
        response = requests.post(url, headers=auth_headers, proxies=proxies)
        if response.status_code == 200:
            return response.json()
        else:
            print(Fore.RED + f"Failed to fetch task list: {response.status_code}")
            return None
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return None

# Complete a task
def complete_task(token, headers, proxy, task_id):
    url = "https://api.infinityg.ai/api/v1/task/complete"
    auth_headers = headers.copy()
    auth_headers["Authorization"] = f"Bearer {token}"
    
    payload = {"taskId": task_id}
    proxies = format_proxy(proxy)
    
    try:
        response = requests.post(url, headers=auth_headers, json=payload, proxies=proxies)
        if response.status_code == 200:
            return response.json()
        else:
            print(Fore.RED + f"Failed to complete task {task_id}: {response.status_code}")
            return None
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return None

# Claim task reward
def claim_task_reward(token, headers, proxy, task_id):
    url = "https://api.infinityg.ai/api/v1/task/claim"
    auth_headers = headers.copy()
    auth_headers["Authorization"] = f"Bearer {token}"
    
    payload = {"taskId": task_id}
    proxies = format_proxy(proxy)
    
    try:
        response = requests.post(url, headers=auth_headers, json=payload, proxies=proxies)
        if response.status_code == 200:
            return response.json()
        else:
            print(Fore.RED + f"Failed to claim task {task_id}: {response.status_code}")
            return None
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return None

# Check-in function
def perform_checkin(token, headers, proxy):
    url = "https://api.infinityg.ai/api/v1/task/checkIn/"
    auth_headers = headers.copy()
    auth_headers["Authorization"] = f"Bearer {token}"
    
    proxies = format_proxy(proxy)
    
    try:
        response = requests.post(url, headers=auth_headers, proxies=proxies)
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
    private_keys = load_private_keys()
    
    for idx, private_key in enumerate(private_keys):
        print(Fore.CYAN + f"Processing account {idx + 1}/{len(private_keys)}")
        
        # Get random proxy
        proxy = get_proxy()
        
        # Login with wallet and get token
        token, wallet_address, headers = login_and_get_token(private_key)
        
        if not token:
            print(Fore.RED + "Failed to authenticate. Skipping this account.")
            # Add delay before next account
            delay = random.randint(1, 7)
            print(Fore.YELLOW + f"Waiting before next account...")
            display_countdown(delay)
            print(Fore.CYAN + "━" * 50)
            continue
        
        # Fetch user info
        user_info = get_user_info(token, headers, proxy)
        if user_info:
            display_user_info(user_info)
        
        # Fetch task list
        task_list = get_task_list(token, headers, proxy)
        
        # Check-in process
        if task_list and task_list.get("code") == "90000":
            display_checkin_status(task_list)
            
            # Check if already checked in today
            if is_already_checked_in(task_list):
                print(Fore.GREEN + "Already checked in today!")
            else:
                print(Fore.YELLOW + "Performing daily check-in...")
                check_in_result = perform_checkin(token, headers, proxy)
                if check_in_result and check_in_result.get("code") == "90000":
                    print(Fore.GREEN + "Check-in successful!")
                    # Delay after check-in
                    checkin_delay = random.randint(2, 5)
                    display_countdown(checkin_delay)
                    # Refresh task list to show updated check-in status
                    task_list = get_task_list(token, headers, proxy)
                    if task_list and task_list.get("code") == "90000":
                        display_checkin_status(task_list)
                else:
                    print(Fore.RED + "Failed to check in.")
        
        # Process tasks
        if task_list and task_list.get("code") == "90000":
            if "taskModelResponses" in task_list["data"]:
                for task_group in task_list["data"]["taskModelResponses"]:
                    print(Fore.MAGENTA + f"Task Group: {task_group['taskModelName']}")
                    for task in task_group["taskResponseList"]:
                        if task["status"] == 0:  # Only process incomplete tasks
                            print(Fore.YELLOW + f"Task: {task['taskName']} (ID: {task['taskId']})")
                            print(Fore.YELLOW + f"Description: {task['taskDesc']}")
                            print(Fore.YELLOW + f"Reward: {task['taskReward']} points")
                            # Complete task
                            complete_response = complete_task(token, headers, proxy, task["taskId"])
                            if complete_response and complete_response.get("code") == "90000":
                                print(Fore.GREEN + "Task completed successfully!")
                                # Add delay before claiming
                                claim_delay = random.randint(1, 7)
                                print(Fore.YELLOW + f"Waiting to claim reward...")
                                display_countdown(claim_delay)
                                # Claim task reward
                                claim_response = claim_task_reward(token, headers, proxy, task["taskId"])
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
            else:
                print(Fore.YELLOW + "No task groups found.")
        
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
        try:
            main()
        except KeyboardInterrupt:
            print(Fore.RED + "\nProgram terminated by user.")
            break
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")
            print(Fore.YELLOW + "Restarting program in 60 seconds...")
            time.sleep(60)
