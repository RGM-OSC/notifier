#!/bin/bash
# usage: slack_notify_host.sh "$HOSTSTATE$" "$HOSTALIAS$" "$HOSTADDRESS$" "$LONGDATETIME$" "$SERVICEOUTPUT$"

source /srv/rgm/notifier/etc/slack.ini

HOSTSTATE="$1"
HOSTALIAS="$2"
HOSTADDRESS="$3"
SERVICEOUTPUT="$4"
LONGDATETIME="$5"

/usr/bin/curl -v -X POST --data-urlencode "payload= \
{ \
	\"channel\": \"${SLACK_CHANNEL}\", \
	\"username\": \"${SLACK_USER}\", \
	\"text\": \":skull_and_crossbones: *$NOTIFICATIONTYPE$ ($HOSTSTATE) sur $HOSTALIAS ($HOSTADDRESS)* \\nDate: *$LONGDATETIME* Additional Info: $SERVICEOUTPUT\", \
	\"icon_emoji\": \"${SLACK_EMOJI}\" \
}" ${SLACK_WEBHOOK}
