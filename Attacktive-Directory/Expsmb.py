import subprocess
from colorama import Fore, Style, init
import re

init(autoreset=True)

target_ip = input("Enter Target IP => ")
username = input("Enter username => ")
password = input("Enter password => ")

def discover_shares_folders():
    print(Fore.YELLOW + "[*] Enumerating shares...")
    try:
        result = subprocess.run(
            ["smbclient", "-L", f"//{target_ip}", "-U", f"{username}%{password}"],
            capture_output=True, text=True, timeout=10
        )

        if result.returncode != 0:
            print(Fore.RED + f"[!] Error: {result.stderr}")
            return []

        shares = []
        for line in result.stdout.splitlines():
            if "Disk" in line:
                parts = line.split()
                if parts:
                    shares.append(parts[0])

        print(Fore.GREEN + "[+] Share enumeration complete.")
        return shares

    except Exception as e:
        print(Fore.RED + f"[!] Exception: {e}")
        return []


def check_access(shares):
    accessible_shares = []
    for share in shares:
        print(Fore.CYAN + f"[*] Trying access to share: {share}")
        try:
            result = subprocess.run(
                ["smbclient", f"//{target_ip}/{share}", "-U", f"{username}%{password}", "-c", "ls"],
                capture_output=True, text=True, timeout=10
            )

            if "NT_STATUS_ACCESS_DENIED" in result.stderr:
                print(Fore.RED + f"[-] Access denied to {share}")
            else:
                print(Fore.GREEN + f"[+] Access granted to {share}")
                print(result.stdout)
                accessible_shares.append(share)

        except subprocess.TimeoutExpired:
            print(Fore.RED + f"[!] Timeout while connecting to {share}")
        except Exception as e:
            print(Fore.RED + f"[!] Error: {e}")
    return accessible_shares


def show_content(shares):
    for share in shares:
        print(Fore.MAGENTA + f"\n[*] Listing content of share: {share}")
        try:
            result = subprocess.run(
                ["smbclient", f"//{target_ip}/{share}", "-U", f"{username}%{password}", "-c", "ls"],
                capture_output=True, text=True, timeout=10
            )
            output = result.stdout
            print(output)

         
            txt_files = re.findall(r'(\S+\.txt)', output)

            for txt_file in txt_files:
                print(Fore.YELLOW + f"\n[!] Reading content of file: {txt_file}")
                read_result = subprocess.run(
                    ["smbclient", f"//{target_ip}/{share}", "-U", f"{username}%{password}", "-c", f"more {txt_file}"],
                    capture_output=True, text=True, timeout=10
                )
                print(Fore.GREEN + read_result.stdout)

        except Exception as e:
            print(Fore.RED + f"[!] Failed to list contents of {share}: {e}")



all_shares = discover_shares_folders()
if all_shares:
    accessible = check_access(all_shares)
    if accessible:
        show_content(accessible)
    else:
        print(Fore.RED + "[!] No accessible shares found.")
else:
    print(Fore.RED + "[!] No shares discovered.")
