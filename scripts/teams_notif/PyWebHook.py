# Import
import getopt
import sys
import pymsteams

# Load variables from config file
sys.path.append('/srv/eyesofnetwork/notifier/scripts/teams_notif')
from define import *


# Class

# Functions
def usage():
    print("""
Script to send monitoring notifications to Microsoft Teams.
Opts:
    -h, --help : Display script help
    -p, --priority : Set priority message
    -t, --type= : Define nagios type (host, service, application)
    -H, --host= : Define nagios host
    -d, --nagios-date= : Define nagios date
    -s, --service= : Define nagios service
    -o, --output= : Define nagios output
    -S, --state= : Define nagios state
    -a, --host-address= : Define nagios host address
    -u, --webhook-url : Define custom Teams webhook URL
""")
    sys.exit(3)


def check_vars(*argv):
    if argv[0] is None:
        print("Missing type value !\n")
        usage()
    elif argv[0] == 'host':
        if argv[1] is None or argv[1] == '':
            print("Missing host value !\n")
            usage()
    elif argv[0] == 'service' or argv[0] == 'application':
        if argv[3] is None or argv[3] == '':
            print("Missing service value !\n")
            usage()
    else:
        assert False, "[ERROR] unhandled type"

    if argv[2] is None or argv[2] == '':
        print("Missing date value !\n")
        usage()
    if argv[4] is None or argv[4] == '':
        print("Missing output value !\n")
        usage()
    if argv[5] is None or argv[5] == '':
        print("Missing state value !\n")
        usage()
    if argv[6] is None or argv[6] == '':
        print("Missing hostaddress value !\n")
        usage()


def build_message(*argv):
    myTeamsMessage = pymsteams.connectorcard(argv[0])
    myTeamsMessage.title(argv[2])
    if o_priority == 'high':
        # myTeamsMessage.text("@DN - Cellule de crise"+argv[3])
        myTeamsMessage.text("Priorito alert " + argv[3])
    else:
        myTeamsMessage.text(argv[3])
    myTeamsMessage.color(argv[4])

    if argv[1] == 'application':
        myMessageSection1 = pymsteams.cardsection()
        if argv[9] == 'OK':
            myMessageSection1.activityTitle("L'application " + argv[11].replace('_', '\_') + " est revenu a la normale")
        elif argv[9] == 'WARNING':
            myMessageSection1.activityTitle("L'application " + argv[11].replace('_', '\_') + " est en alerte")
        elif argv[9] == 'CRITICAL':
            myMessageSection1.activityTitle("L'application " + argv[11].replace('_', '\_') + " est indisponible")
        else:
            myMessageSection1.activityTitle("L'application " + argv[11].replace('_', '\_') + " est " + argv[9])
        myMessageSection1.addFact("Cause :", argv[6].replace('_', '\_'))
        myMessageSection1.addFact("Date :", argv[7].replace('_', '\_'))
    else:
        myMessageSection1 = pymsteams.cardsection()
        myMessageSection1.activityTitle(argv[5])
        myMessageSection1.addFact("Host :", argv[8].replace('_', '\_'))
        myMessageSection1.addFact("Address :", argv[10].replace('_', '\_'))
        if argv[1] == 'service':
            myMessageSection1.addFact("Service :", argv[11].replace('_', '\_'))
        myMessageSection1.addFact("State :", argv[9].replace('_', '\_'))
        myMessageSection1.addFact("Info : ", argv[6].replace('_', '\_'))
        myMessageSection1.addFact("Date :", argv[7])

    myTeamsMessage.addSection(myMessageSection1)

    return myTeamsMessage


# Variables
opts = None
o_priority = None
o_type = None
o_host = None
o_hostaddress = None
o_datetime = None
o_service = None
o_output = None
o_state = None
o_url = None
url = None

# Main
try:
    opts, args = getopt.getopt(sys.argv[1:], "t:H:d:s:o:S:a:u:hp",
                               ["type=", "host=", "nagios-date=", "service=", "output=", "state=", "help", "priority", "host-address", "webhook-url"])
except getopt.GetoptError as err:
    print("[ERROR]", err)
    usage()

for o, a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-p", "--priority"):
        o_priority = 'high'
    elif o in ("-t", "--type="):
        o_type = a
    elif o in ("-H", "--host="):
        o_host = a
    elif o in ("-d", "--nagios-date="):
        o_datetime = a
    elif o in ("-s", "--service"):
        o_service = a
    elif o in ("-o", "--output"):
        o_output = a
    elif o in ("-S", "--state"):
        o_state = a
    elif o in ("-a", "--host-address"):
        o_hostaddress = a
    elif o in ("-u", "--webhook-url"):
        o_url = a
    else:
        assert False, "[ERROR] unhandled option"

if o_priority == 'high':
    url = urlCelCrise
else:
    if o_url is None:
        if o_type == 'host' or o_type == 'service':
            url = urlStandard
        if o_type == 'application':
            url = urlApp
    else:
        url = o_url


check_vars(o_type, o_host, o_datetime, o_service, o_output, o_state, o_hostaddress)

if o_state == 'CRITICAL' or o_state == 'DOWN':
    color = colorCrit
elif o_state == 'WARNING':
    color = colorWarn
elif o_state == 'OK' or o_state == 'UP':
    color = colorOk
else:
    color = "000000"

# def build_message(url, type, title, text, color, actitle, info, date, host, state, service, o_priority ):
tMessage = build_message(url, o_type, cardTitle, cardText, color, activityTitleSvc, o_output, o_datetime, o_host,
                         o_state, o_hostaddress, o_service, o_priority)

# Send message to webhook
tMessage.send()
