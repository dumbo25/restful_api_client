#!/usr/bin/env python3

#########################
#
# Client-side script for RESTful API sever written in python3 using json
#
# Both client-side and server-side scripts are required for the API
#
#########################


#########################
#
# The script runs with this command:
#   $ python3 client_server.py
#
# This script requires the following:
#   Two raspberry pis: one running the server-side script and the other running the client-side script
#
#   Add the requests library:
#      $ pip install requests
#
#   ??? update scripts on github
#
#########################

#########################
# import needed libraries
import time
import datetime
import requests
import json
import sys
import getopt
import urllib3

# cert gives warning message because it is not using Fully Qualified Domain Name using DNS, but 
# instead a value entered during cert creation
# the lines above and  below suppresses the warning message
urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)


#########################
# use all CAPs for constants

#########################
# use first CAP for global variables
#
# use high numbered port (90xx) indicating it is using http port 80 or 444 for https
# Port must match the one used by the server-side script
Api = '/api'
InputFile = ''
Path = '/home/pi/api/'
LogFile = Path + 'rest_client.log'
Secure = 'http://'

#########################
#
# edit these parameters to match your settings
# replace the angle brackets with a port number, say 9080 or 9443
# 
Port = <your-port-number>
#
# the server name is either hostname.local or just hostname
# Server = '<hostname>.local'
Server = '<hostname>'
#
#########################

Use_cert = False
# these files are generated on the server-side raspberry pi and copied to this server using scp
ClientKeyFile = Path + 'client.key'
ServerCertFile = Path + 'server.crt'
ClientCertFile = Path + 'client.crt'


#########################
# Log messages should be time stamped
def timeStamp():
    t = time.time()
    s = datetime.datetime.fromtimestamp(t).strftime('%Y/%m/%d %H:%M:%S - ')
    return s

# Write messages in a standard format
def printMsg(s):
    if s == '':
        LogFileObject.write("\n")
    else:
        LogFileObject.write(timeStamp() + s + "\n")


def cmdLine(argv):
    global Api
    global InputFile
    global Port
    global LogFile
    global Secure
    global Server
    global Use_cert

    port_set = False

    try:
        # new options must be added here:
        validOpts = "ha:ci:l:p:sS:"
        opts, args = getopt.getopt(argv,validOpts,["help=", "cert", "api=","logfile=","port=","secure", "Server="])
    except getopt.GetoptError:
        print('client_server.py [options, ...]' )
        print('client_server.py -h' )
        sys.exit(2)

    for opt, arg in opts:
        # help option goes first and exits, regardless of other options
        if opt in ('-h', '--help'):
            print('Decription: ')
            print('  Client-side script for RESTful API sever written in python using json')
            print('  The server-side script should be running before starting this script')
            print('')
            print('Usage:')
            print('  python3 client_server.py [options...]')
            print('')
            print('Options:')
            print('  -h --help      This help')
            print('  -a --api       Path for API')
            print('  -c --cert      Use a cert. Must match webserver')
            print('  -i --inputfile Input json file')
            print('  -l --logfile   Write log messages to user specified file')
            print('  -p --port      User defined port. The default port is' + str(Port) + '.')
            print('                 Must match port used by rest_server.py')
            print('  -s --secure    Use HTTPS. Must match webserver')
            print('  -S --Server    User defined server')
            sys.exit()
        elif opt in ("-a", "--api"):
            Api = arg
        elif opt in ("-c", "--cert"):
            Use_cert = True
        elif opt in ("-i", "--inputfile"):
            InputFile = arg
        elif opt in ("-l", "--logfile"):
            LogFile = arg
        elif opt in ("-p", "--port"):
            Port = int(arg)
            port_set = True
        elif opt in ("-s", "--Secure"):
            Secure = "https://"
            if port_set:
                pass
            else:
                Port = 9443
        elif opt in ("-S", "--Server"):
            Server = arg
    return

def printCmdLine():
    printMsg('Command line arguments:')
    printMsg('  API = ' + Secure + Server + ':' + str(Port) + Api)
    printMsg('  Input file  = ' + InputFile)
    printMsg('  Log file = ' + LogFile)
    printMsg('  Port = ' + str(Port))
    printMsg('  Secure = ' + Secure)
    printMsg('  Server = ' + Server)
    printMsg('  Use_cert = ' + str(Use_cert))
    printMsg('')
    return

#########################
# The following is an example of how to use a RESTful api
# ??? this needs work
def apiGet(secure, server, port, api):
    # headers = {'Content-Type': 'application/json' }
    headers = {'Content-Type': 'application/json'}

    # ??? does task do anything
    # task = {"summary": "multiply two numbers", "num1": "num2" }

    cert = (ClientCertFile, ClientKeyFile)

    try:
        if Secure == "http://":
            # unsecure call
            printMsg('unsecure call')
            # resp = requests.get(secure + server + ':' + str(port) + api,  headers=headers, json=task, verify=False)
            print(secure + server + ':' + str(port) + api)
            resp = requests.get(secure + server + ':' + str(port) + api,  headers=headers, verify=False)
        else:
            # secure call
            if Use_cert:
                printMsg('secure call with cert')
                # resp = requests.get(secure + server + ':' + str(port) + api, cert=cert, headers=headers, json=task, verify=ServerCertFile)
                resp = requests.get(secure + server + ':' + str(port) + api, cert=cert, headers=headers, verify=ServerCertFile)
                print(secure + server + ':' + str(port) + api)
            else:
                printMsg('secure but no cert')
                # resp = requests.get(secure + server + ':' + str(port) + api, headers=headers, json=task, verify=False)
                print(secure + server + ':' + str(port) + api)
                resp = requests.get(secure + server + ':' + str(port) + api, headers=headers, verify=False)
        if resp.status_code != 200:
            print('GET status code = ', resp.status_code)
            return
        # instead of printing the return values, add code to handle the returned data
        # or return the data and process elsewhere
        print('Value = ')
        print(resp.text)
    except:
        print('Request failed: ' + server + ':' + str(port) + api)

    return

#########################
def main(sysargv):
    global LogFileObject

    # process command line arguments
    cmdLine(sysargv[1:])

    # open a log file. printMsg writes to the log file
    LogFileObject = open(LogFile, 'w+')

    printCmdLine()

    apiGet(Secure, Server, Port, Api)

    exit()

#########################
if __name__ == '__main__':
    # run as a script from command line
    main(sys.argv)
else:
    # ??? import to another module
    pass
