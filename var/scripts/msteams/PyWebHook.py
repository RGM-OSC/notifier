#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4:

__author__ = 'Vincent Fricou'
__copyright__ = '2019, VincentFricou, SCC'
__credits__ = ['Vincent Fricou', 'Eric Belhomme']
__license__ = "GPL"
__version__ = "0.0.2"
__maintainer__ = ['Vincent Fricou', 'Eric Belhomme']

import sys
import pymsteams
import argparse
import configparser


def build_message(priority, ntype, host, host_addr, service, date, state, output, message):
    teamscnx = None
    try:
        teamscnx = pymsteams.connectorcard(message['webhook'])
    except Exception as e:
        error_and_die(e)

    teamscnx.title(message['title'])
    if priority == 'high':
        teamscnx.text("Alerte prioritaire {}".format(message['msg_body']))
    else:
        teamscnx.text(message['msg_body'])

    msgSection = pymsteams.cardsection()
    if ntype == 'application':
        if state == 'OK':
            msgSection.activityTitle("L'application {} est revenu a la normale".format(service.replace('_', '\_')))
        elif state == 'WARNING':
            msgSection.activityTitle("L'application {} est en alerte".format(service.replace('_', '\_')))
        elif state == 'CRITICAL':
            msgSection.activityTitle("L'application {} est indisponible".format(service.replace('_', '\_')))
        else:
            msgSection.activityTitle("L'application {} est à l'état {}".format(service.replace('_', '\_'), state))
        msgSection.addFact("Cause :", output.replace('_', '\_'))
        msgSection.addFact("Date :", date.replace('_', '\_'))
    else:
        msgSection.activityTitle(message['service_title'])
        msgSection.addFact("Host :", host.replace('_', '\_'))
        msgSection.addFact("Address :", host_addr.replace('_', '\_'))
        if ntype == 'service':
            msgSection.addFact("Service :", service.replace('_', '\_'))
        msgSection.addFact("State :", state.replace('_', '\_'))
        msgSection.addFact("Info : ", output.replace('_', '\_'))
        msgSection.addFact("Date :", date)

    teamscnx.addSection(msgSection)
    teamscnx.send()


def error_and_die(message):
    print("Fatal error: {}".format(message))
    sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
            Script to send RGM notifications to Microsoft Teams messenger
        """,
        usage="""
        """,
        epilog="version {}, copyright {}".format(__version__, __copyright__))

    parser.add_argument('-c', '--config', type=str, help='set config file', default='/srv/rgm/notifier/etc/msteams.ini')
    parser.add_argument(
        '-p', '--priority', type=str,help='set message priority', default='default',
        choices=['low', 'default', 'high']
    )
    parser.add_argument(
        '-t', '--type', type=str, help='define nagios type (host, service, application)', required=True,
        choices=['host', 'service', 'application']
        )
    parser.add_argument('-H', '--host', type=str, help='define nagios host')
    parser.add_argument('-d', '--nagios-date', type=str, help='define nagios date', required=True)
    parser.add_argument('-s', '--service', type=str, help='define nagios service')
    parser.add_argument('-o', '--output', type=str, help='define nagios output', required=True)
    parser.add_argument('-S', '--state', type=str, help='define nagios state', required=True)
    parser.add_argument('-a', '--host-address', type=str, help='define nagios host address', required=True)
    parser.add_argument('-u', '--webhook-url', type=str, help='define custom Teams webhook URL', default=None)
    args = parser.parse_args()

    cfgfile = configparser.ConfigParser()
    try:
        cfgfile.read(args.config)
    except Exception as e:
        error_and_die("Error while loading config file {}. Error was: {}".format(args.config, e))

    if 'webhooks' not in cfgfile:
        error_and_die('no [webhooks] section in config file')
    if 'default' not in cfgfile['webhooks']:
        error_and_die('no default webhook specified')

    message_params = {
        'webhook': cfgfile['webhooks']['default'],
        'title': 'RGM monitoring',
        'service_title': '---',
        'msg_body': 'A new RGM notification occured',
        'color': '000000'
    }
    colors = [
        '00ff00',  # 0 -> ok/up
        'fbfb00',  # 1 -> warning
        'ff0000',  # 2 -> critical/down
    ]

    if args.priority in cfgfile['webhooks']:
        message_params['webhook'] = cfgfile['webhooks'][args.priority]
    if args.webhook_url is not None:
        message_params['webhook'] = args.webhook_url

    if 'message' in cfgfile:
        for item in ['title', 'body', 'service_title']:
            if item in cfgfile['message']:
                message_params['item'] = cfgfile['message'][item]

    if 'color' in cfgfile:
        for idx, item in [(0, 'ok'), (1, 'warning'), (2, 'critical')]:
            if item in cfgfile['color']:
                colors[idx] = cfgfile['color'][item]
    
    if args.state.upper() in ('CRITICAL', 'DOWN'):
        message_params['color'] = colors[2]
    elif args.state.upper() in ('OK', 'UP'):
        message_params['color'] = colors[0]
    elif args.state.upper() == 'WARNING':
        message_params['color'] = colors[1]

    build_message(
        priority=args.priority,
        ntype=args.type.lower(),
        host=args.host,
        host_addr=args.host_address,
        service=args.service,
        date=args.nagios_date,
        state=args.state.upper(),
        output=args.output,
        message=message_params
    )
