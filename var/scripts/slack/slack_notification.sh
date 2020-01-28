#!/bin/bash
# usage: slack_notify_host.sh "$HOSTSTATE$" "$HOSTALIAS$" "$HOSTADDRESS$" "$LONGDATETIME$" "$SERVICEOUTPUT$"
ScriptName='slack_notification.sh'
ScriptVersion='v0.0.2'
# Initial version Samuel RONCIAUX
# Updated by Vincent FRICOU
# Script to send rgm notifications events into slack channel

source /srv/rgm/notifier/etc/slack.ini

function build_host_notification() {
  if [ "${HOSTSTATE}" != 'UP' ]
  then
    text=":bangbang: $LONGDATETIME -- *($HOSTSTATE) on $HOSTALIAS ($HOSTADDRESS)* -- $SERVICEOUTPUT"
  else
    text=":heavy_check_mark: $LONGDATETIME -- *($HOSTSTATE) on $HOSTALIAS ($HOSTADDRESS)* -- $SERVICEOUTPUT"
  fi
  printf "${text}"
}

function build_service_notification() {
  if [ "${SERVICESTATE}" == 'CRITICAL' ]
  then
    text=":bangbang: $LONGDATETIME -- *($SERVICESTATE)  on $HOSTALIAS ($HOSTADDRESS)* - *$SERVICEDESC* --  $SERVICEOUTPUT"
  elif [ "${SERVICESTATE}" == 'WARNING' ]
  then
    text=":warning: $LONGDATETIME -- *($SERVICESTATE)  on $HOSTALIAS ($HOSTADDRESS)* - *$SERVICEDESC* --  $SERVICEOUTPUT"
  elif [ "${SERVICESTATE}" == 'OK' ]
  then
    text=":heavy_check_mark: $LONGDATETIME -- *($SERVICESTATE)  on $HOSTALIAS ($HOSTADDRESS)* - *$SERVICEDESC* --  $SERVICEOUTPUT"
  else
    text=":question: $LONGDATETIME -- *($SERVICESTATE)  on $HOSTALIAS ($HOSTADDRESS)* - *$SERVICEDESC* --  $SERVICEOUTPUT"
  fi
  printf "${text}"
}

function usage() {
  printf "Usage of ${ScriptName} (${ScriptVersion}) :\n"
  printf '  -T : Equipment type (host/service)
  -H : Equipment name ($HOSTALIAS$)
  -a : Equipment address ($HOSTADDRESS$)
  -S : Equipment state ($HOSTSTATE$)
  -s : Service state ($SERVICESTATE$)
  -n : Service description ($SERVICEDESC$)
  -o : Service / Host check output ($SERVICEOUTPUT$)
  -d : Nagios long date time ($LONGDATETIME$)
  -h : Display this help
'
  exit 3
}

while getopts "hT:H:a:S:s:n:o:d:" opts
do
  case ${opts} in
      T) Type=${OPTARG^^} ;;
      H) HOSTALIAS=${OPTARG} ;;
      a) HOSTADDRESS=${OPTARG} ;;
      S) HOSTSTATE=${OPTARG} ;;
      s) SERVICESTATE=${OPTARG} ;;
      n) SERVICEDESC=${OPTARG} ;;
      o) SERVICEOUTPUT=${OPTARG} ;;
      d) LONGDATETIME=${OPTARG} ;;
      h) usage ;;
      *)
        printf "Option not recognized.\n"
        usage
      ;;
  esac
done


if [ "${Type}" == 'service' ]
then
  build_service_notification
else
  build_host_notification
fi

/usr/bin/curl -v -X POST --data-urlencode "payload= \
{ \
	\"channel\": \"${SLACK_CHANNEL}\", \
	\"username\": \"${SLACK_USER}\", \
	\"text\": \"${text}\", \
	\"icon_emoji\": \"${SLACK_EMOJI}\" \
}" ${SLACK_WEBHOOK}
