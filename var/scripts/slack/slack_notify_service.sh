#!/bin/bash
# usage: slack_notify_service.sh "$HOSTSTATE$" "$HOSTALIAS$" "$HOSTADDRESS$" "$SERVICEDESC$" "$SERVICEOUTPUT$" "$LONGDATETIME$"

source /srv/rgm/notifier/etc/slack.ini

SERVICESTATE="$1"
HOSTALIAS="$2"
HOSTADDRESS="$3"
SERVICEDESC="$4"
SERVICEOUTPUT="$5"
LONGDATETIME="$6"

/usr/bin/curl -v -X POST --data-urlencode "payload= \
{ \
	\"channel\": \"${SLACK_CHANNEL}\", \
	\"username\": \"${SLACK_USER}\", \
	\"text\": \":skull_and_crossbones: *$NOTIFICATIONTYPE$ ($SERVICESTATE) sur $HOSTALIAS ($HOSTADDRESS)* \\nService: *$SERVICEDESC* \\nDate: $LONGDATETIME \\nAdditional Info: $SERVICEOUTPUT\",
	\"icon_emoji\": \"${SLACK_EMOJI}\" \
}" ${SLACK_WEBHOOK}
