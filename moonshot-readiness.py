#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import os
import socket
import sys
import stat
import re


print "\n\n===============================  MOONSHOT-READINESS  ==============================="
results = "====================================================================================\n\nTest complete, failed tests:\n"



#=================================  TESTS BASIC  ===========================================



def test_basic():
    global results
    print("\n\nTesting task basic...")


    cmd = os.popen("hostname -f")
    fqdn1 = (cmd.read()).strip()
    cmd = os.popen("dig " + fqdn1 + " +short")
    address = (cmd.read()).strip()
    cmd = os.popen("dig -x " + address + " +short")
    fqdn2 = (cmd.read()).strip()
    if fqdn1 + "." == fqdn2:
        print("    Hostname is FQDN...                            [OKAY]")
    else:
        print("    Hostname is FQDN...                            [FAIL]")
        results = results + "    Hostname is FQDN:\n        Your servers hostname is not fully qualified or resolvable. This is required in order to prevent certain classes of attack.\n"


    good_os = False
    if os.path.isfile("/etc/redhat-release") == True:
        fil = open("/etc/redhat-release", "r")
        name = (fil.read()).strip()
        fil.close()
        if (name == "RedHat release 6.3 (Final)" or name == "RedHat release 6.4 (Final)" or name == "RedHat release 6.5 (Final)" or name == "RedHat release 6.6 (Final)" or name == "CentOS release 6.3 (Final)" or name == "CentOS release 6.4 (Final)" or name == "CentOS release 6.5 (Final)" or name == "CentOS release 6.6 (Final)" or name == "Scientific Linux release 6.3 (Final)" or name == "Scientific Linux release 6.4 (Final)" or name == "Scientific Linux release 6.5 (Final)" or name == "Scientific Linux release 6.6 (Final)"):
            good_os = True
    elif os.path.isfile("/etc/os-release") == True:
        fil = open("/etc/os-release", "r")
        text = fil.read()
        fil.close()
        lines = text.split("\n")
        good_name = False
        good_version = False
        i = 0
        while i < len(lines):
            words = lines[i].split("=")
            if words[0] == "NAME":
                if words[1] == "\"Debian GNU/Linux\"":
                    good_name = True
            if words[0] == "VERSION_ID":
                if words[1] == "\"6\"" or words[1] == "\"7\"":
                    good_version = True
            i = i + 1
        if good_name == True and good_version == True:
            good_os = True
    if good_os == True:
        print("    Supported OS...                                [OKAY]")
    else:
        print("    Supported OS...                                [WARN]")
        results = results + "    Supported OS:\n        You are not running a supported OS. Moonshot may not work as indicated in the documentation.\n"


    cmd = os.popen("apt-cache search -n \"moonshot\"")
    cmd = cmd.read()
    if cmd.strip() != '':
        print("    Moonshot repositories configured...            [OKAY]")
    else:
        print("    Moonshot repositories configured...            [WARN]")
        results = results + "    Moonshot repositories configured:\n        The Moonshot repositories do not appear to exist on this system. You will not be able to upgrade Moonshot using your distributions package manager.\n"


    cmd = os.popen("apt-get -u upgrade --assume-no moonshot")
    cmd = cmd.read()
    if cmd.strip() == 'Reading package lists... Done\nBuilding dependency tree\nReading state information... Done\n0 upgraded, 0 newly installed, 0 to remove and\
 0 not upgraded.':
        print("    Monshot current version...                     [OKAY]\n\n")
    else:
        print("    Monshot current version...                     [WARN]\n\n")
        results = results + "    Moonshot current version:\n        You are not running the latest version of the Moonshot software.\n"



#=================================  TESTS RP  ===========================================



def test_rp():
    global results
    test_basic()
    print("Testing task rp...")

    cmd = os.path.isfile("/etc/radsec.conf")
    if cmd == True:
        print("    radsec.conf...                                 [OKAY]\n\n")
    else:
        print("    radsec.conf...                                 [FAIL]\n\n")
        results = results + "    radsec.conf:\n        /etc/radsec.conf could not be found - you may not be able to communicate with your rp-proxy.\n"



#=================================  TESTS RP-PROXY  ===========================================



def test_rp_proxy():
    global results
    test_rp()
    print("Testing task rp-proxy...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('apc.moonshot.ja.net', 2083))
    if result == 0:
        print("    APC...                                         [OKAY]")
    else:
        print("    APC...                                         [FAIL]")
        results = results + "    APC:\n        apc.moonshot.ja.net does not seem to be accessible. Please check the servers network connection, and see status.moonshot.ja.net for any downtime or maintenance issues.\n"


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('tr1.moonshot.ja.net', 12309))
    if result == 0:
        print("    Trust Router...                                [OKAY]\n\n")
    else:
        print("    Trust Router...                                [FAIL]\n\n")
        results = results + "    Trust Router:\n        tr1.moonshot.ja.net does not seem to be accessible. Please check the servers network connection, and see status.moonshot.ja.net for any downtime or maintenance issues.\n"



#=================================  TESTS IDP  ===========================================



def test_idp():
    global results
    test_rp()
    print("Testing task idp...")


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 2083))
    if result == 0:
        print("    Port 2083...                                   [OKAY]")
    else:
        print("    Port 2083...                                   [FAIL]")
        results = results + "    Port 2083:\n        Port 2083 appears to be closed. RP's will not be able to initiate connections to your IDP.\n"


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 12309))
    if result == 0:
        print("    Port 12309...                                  [OKAY]\n\n")
    else:
        print("    Port 12309...                                  [FAIL\n\n]")
        results = results + "    Port 12309:\n        Port 12309 appears to be closed. The trust router will not be able to initiate connections to your IDP.\n"



#=================================  TESTS CLIENT  ===========================================



def test_client():
    global results
    test_basic()
    print("Testing task client...")


    cmd = os.path.isfile("/usr/etc/gss/mech") 
    if cmd == True:
        mode = oct(stat.S_IMODE(os.stat("/usr/etc/gss/mech")[stat.ST_MODE]))
        if mode.strip() == "0644":
            
            string1 = "eap-aes128 1.3.6.1.5.5.15.1.1.17 mech_eap.so" 
            string2 = "eap-aes128 1.3.6.1.5.5.15.1.1.17 mech_eap.so"
            s1 = False
            s2 = False
            fil = open("/usr/etc/gss/mech","r")
            for line in fil:
                words=re.split(r'[ \t]+', line)
                i = 0
                str_reg = ""
                while i < len(words):
                    str_reg = str_reg + words[i] + " "
                    i = i+1
                if string1 == str_reg.strip():
                    s1 = True
                if string2 == str_reg.strip():
                    s2 = True
            fil.close()
            
            if (s1 == True and s2 == True):
                print("    gss/mech...                                    [OKAY]\n\n")
                return;

    print("    gss/mech...                                    [FAIL]\n\n")
    results = results + "    gss/mech:\n        The Moonshot mech file is missing mech_eap.so will not be loaded.\n"



#=================================  TESTS SSH-CLIENT  ===========================================



def test_ssh_client():
    global results
    test_client()
    print("Testing task ssh-client...")


    cmd = os.popen("augtool print /files/etc/ssh/ssh_config/Host/GSSAPIAuthentication")
    cmd = cmd.read()
    if cmd.strip() == "/files/etc/ssh/ssh_config/Host/GSSAPIAuthentication = \"yes\"":
        print("    GSSAPIAuthentication enabled...                [OKAY]")
    else:
        print("    GSSAPIAuthentication enabled...                [FAIL]")
        results = results + "    GSSAPIAuthentication enabled:\n        GSSAPIAuthentication must be enabled for Moonshot to function when using SSH.\n"


    cmd = os.popen("augtool print /files/etc/ssh/ssh_config/Host/GSSAPIKeyExchange")
    cmd = cmd.read()
    if cmd.strip() == "/files/etc/ssh/ssh_config/Host/GSSAPIKeyExchange = \"yes\"":
        print("    GSSAPIKeyExchange enabled...                   [OKAY]\n\n")
    else:
        print("    GSSAPIKeyExchange enabled...                   [WARN]\n\n")
        results = results + "    GSSAPIKeyExchange enabled:\n        GSSAPIKeyExchange should be enabled for Moonshot to function correctly when using SSH.\n"



#=================================  TESTS SSH-SERVER  ===========================================



def test_ssh_server():
    global results
    test_rp()
    print("Testing task ssh-client...")


    cmd = os.popen("augtool print /files/etc/ssh/sshd_config/UsePrivilegeSeparation")
    cmd = cmd.read()
    if cmd.strip() == "/files/etc/ssh/sshd_config/UsePrivilegeSeparation = \"no\"":
        print("    Privilege separation disabled...               [OKAY]")
    else:
        print("    Privilege separation disabled...               [FAIL]")
        results = results + "    Privilege separation disabled:\n        Moonshot currently requires that OpenSSH server has privilege separation disabled.\n"


    cmd = os.popen("augtool print /files/etc/ssh/sshd_config/GSSAPIAuthentication")
    cmd = cmd.read()
    if cmd.strip() == "/files/etc/ssh/sshd_config/GSSAPIAuthentication = \"yes\"":
        print("    GSSAPIAuthentication...                        [OKAY]\n\n")
    else:
        print("    GSSAPIAuthentication...                        [FAIL]\n\n")
        results = results + "    GSSAPIAuthentication:\n        GSSAPIAuthentication must be enabled for Moonshot to function when using SSH.\n"



#=================================  MAIN  ===========================================



size = len(sys.argv)

if size < 2 :
    print("\n\nUsage: moonshot-readiness [task] [task]...\n\n  Available tasks:\n    help\n    minimal (default)\n    client\n    rp\n    rp-proxy\n    idp-proxy\n    ssh-client\n    ssh-server\n\n")

else:
    i = 1
    while i < size:
        if (sys.argv[i]).strip() == 'help':
            print "\n\nUsage: moonshot-readiness [task] [task]...\n\n  Available tasks:\n    help\n    minimal (default)\n    client\n    rp\n    rp-proxy\n    idp-proxy\n    ssh-client\n    ssh-server\n\n  ¦---------------------------------------------------------------------------------------------------------------¦\n  ¦ TASK            ¦  DEPENDENCY  ¦  DESCRIPTION                                                                 ¦\n  ¦-----------------¦--------------¦------------------------------------------------------------------------------¦\n  ¦ basic           ¦  none        ¦  Basic set of test, required for Moonshot to function at all in any capacity ¦\n  ¦ client          ¦  basic       ¦  Fundamental tests required for Moonshot to function as a client             ¦\n  ¦ rp              ¦  basic       ¦  Fundamental tests required for Moonshot to function as an RP                ¦\n  ¦ rp-proxy        ¦  rp          ¦  Tests required for Moonshot to function as a RadSec RP                      ¦\n  ¦ idp             ¦  rp          ¦  Tests to verify if FreeRADIUS is correctly configured                       ¦\n  ¦ openssh-client  ¦  client      ¦  Tests to verify if the openssh-client is correctly configured               ¦\n  ¦ openssh-rp      ¦  rp          ¦  Tests to verify if the openssh-server is correctly configured               ¦\n  ¦ httpd-client    ¦  client      ¦  Tests to verify if mod-auth-gssapi is correctly configured                  ¦\n  ¦ httpd-rp        ¦  rp          ¦  Tests to verify if mod-auth-gssapi is correctly configured                  ¦\n  ¦-----------------¦--------------¦------------------------------------------------------------------------------¦\n\n"



            sys.exit()
        elif (sys.argv[i]).strip() == 'minimal':
            test_basic()
        elif (sys.argv[i]).strip() == 'client':
            test_client()
        elif (sys.argv[i]).strip() == 'rp':
            test_rp()
        elif (sys.argv[i]).strip() == 'rp-proxy':
            test_rp_proxy()
        elif (sys.argv[i]).strip() == 'idp-proxy':
            test_idp()
        elif (sys.argv[i]).strip() == 'ssh-client':
            test_ssh_client()
        elif (sys.argv[i]).strip() == 'ssh-server':
            test_ssh_server()
        else:
            print ("\n\nTask \"" + sys.argv[i] + "\" doesn't exist.\n  Available tasks:\n    minimal (default)\n    client\n    rp\n    rp-proxy\n    idp-proxy\n    ssh-client\n    ssh-server\n\n")
            sys.exit()
        i = i+1

    if results == "=========================================================================\n\nTest complete, failed tests:\n":
        results = "=========================================================================\n\nTest complete, 100% is OKAY\n\n"
    print results
