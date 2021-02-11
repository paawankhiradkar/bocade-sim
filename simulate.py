#!/usr/bin/python
import paramiko
import time
import os
import shutil
import zipfile
import optparse
from pathlib import Path
from cryptography.fernet import Fernet
#import netifaces
import re

class Simulate():
    SSH_RETRY_INTERVAL = 10
    ip_address = ""
    userName = ""
    password = ""
    output_zip_file = ""
    mode = ""
    VPNConnect = ""
    version = "0.1"

    def __init__(self):
        try:

            parser = optparse.OptionParser(version="Version : "+Simulate.version)
            parser.add_option('--mode', dest = 'mode')
            parser.add_option('--ip', dest = "ipAddress")
            parser.add_option('-u', dest = "username")
            parser.add_option('-p', dest = 'password')
            parser.add_option('--name',
                              action = "store", dest = "outputFile",
                              help = "query string", default = "spam")
            parser.add_option('--enc', dest = "encryption")
            parser.add_option('--VPNConnect', '--vc', dest="VPNConnect")
            parser.add_option('--VPNCommand', dest="VPNCommand")

            options, args = parser.parse_args()
            self.command_dict = {
                1: "switchShow",
                2: "firmwareshow --history",
                3: "ficonshow switchrnid",
                4: "switchshow -portcount",
                5: "sfpShow -all",
                6: "zoneShow",
                17: "lscfg --show",
                7: "agshow",
                8: "agshow --name",
                9: "islshow",
                10: "trunkshow",
                11: "nsshow -r -t",
                12: "sysmonitor --show cpu",
                13: "memshow -m",
                14: "version",
                15: "switchshow",
                16: "portStatsShow",
                18: "mapssam --show cpu",
                19: "portShow -i PORT_RANGE -f",
                20: "portbuffershow",
                21: "portShow PORT_NUMBER",
                22: "portstatsshow PORT_NUMBER"

            }

            self.output_zip_file = options.outputFile
            Simulate.output_zip_file = self.output_zip_file
            self.ip_address = options.ipAddress
            Simulate.ip_address = self.ip_address
            self.userName = options.username
            Simulate.userName = self.userName
            self.password = options.password
            Simulate.password = self.password
            self.mode = options.mode
            Simulate.mode = self.mode
            self.encryptionFlag = options.encryption
            Simulate.encryptionFlag = self.encryptionFlag  # True/False

            self.VPNConnect = options.VPNConnect  # True/False
            self.VPNCommand = options.VPNCommand  # string (command for VPN connect)

            self.enc_key = "mIfOxfsc8tnecIVxWsePcV08K6mvJjpNzYQTvSt4eD0="
            self.ssh = ""
            self.shell = ""

            # FID-Port mapping file
            self.port_FID_mapping = {}
            # for maintaining the count of keys in command dict
            self.command_dict_key = 21

        except Exception as e:
            print("Exception in intializaing Simulatr class: {}". format(e))

obj = Simulate()
if Simulate.mode == 'collection':
    if Simulate.ip_address and Simulate.output_zip_file and Simulate.userName and Simulate.password:
        print("In collection method")

    else:
        print(100 * '*')
        print("\nSyntax Error. please refer the following: from collection")
        print("\n1.For data collection on real brocade switch use following")
        print(
            "    python3.6 <path_to_Simulate.py> --mode collection --ip <ipaddr> --u <user_name> --p <password> --name <name_of_output_file>")
        print("\n2. For simulating brocade switch:")
        print("    python3.6 <path_to_Simulate.py> --mode simulation --name <name_for_zip_file>")
        print("\n--mode -> there are two modes 'collection' and 'simulation'")
        print(
            "         'collection' : collection mode collects data from real switch and create its zip file by given name.")
        print("         'simulation' : Simulate mode configures the given switch for simulating it")
        print("  --ip -> ip of real switch which has to be simulated.")
        print("   --u -> user name of real switch.")
        print("   --p -> password of real switch.")
        print("--name -> name fo zip file or full path of zip file to be created by Simulate.py.")
        print("\n*" * 100)
elif Simulate.mode == 'simulation':
    if Simulate.output_zip_file and not "spam" in Simulate.output_zip_file:
        print("In simulation method")
    else:
        # Checking for all mandatory parameters while running script Simulate.py
        print("-----------------------------------------------------------------")
        print("\nSyntex error. Please refer following: from simulation")
        print("\n2. For simulating  brocade switch:")
        print("    python3.6 <path_to_Simpulate.py> --mode simulation --name <name_for_zip_file>")
        print("\n--name -> name fo zip file or full path of zip file to be created by Simulate.py.")
        print("\n---------------------------------------------------------------")

else:
    print("-----------------------------------------------------------------")
    print("\nSyntex error. Please refer following: from last else")
    print("\n1.For data collection on real brocade switch use following")
    print(
        "    python3.6 <path_to_Simulate.py> --mode collection --ip <ipaddr> --u <user_name> --p <password> --name <name_of_output_file>")
    print("\n2. For simulating brocade switch:")
    print("    python3.6 <path_to_Simulate.py> --mode simulation --name <name_for_zip_file>")
    print("\n--mode -> There are two modes 'collection' and 'simulation'")
    print(
        "          'collection' : collection mode collects data from real switch and create its zip file by given name.")
    print("          'simulation' : Simulation mode configures the given switch for simulating it")
    print("  --ip -> ip of real switch which has to be simulated.")
    print("   --u -> user name of real switch.")
    print("   --p -> password of real switch.")
    print("--name -> name fo zip file or full path of zip file to be created by Simulate.py.")
    print("\n---------------------------------------------------------------")

