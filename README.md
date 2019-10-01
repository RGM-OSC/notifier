# RGM advanced notifier unit.

## NEWS

Version 2.1.3 release with new architecture adapted to RGM.

### Most important change on rules and commands configuration

* Introduce a new field in notifier.rules configuration line in end of line. This field manage notification tracking or not (0 == tracking disables, 1 == tracking enabled)
* VERY IMPORTANT : all notifications command (in notifier.cfg) MUST BE in standard format if you use specific notification with match on state !
 * Example if you have a specific command to send custom email on CRITICAL state, the command ___must be___ in format « command-nameSTATE ». You choose all name of « command-name » but the ending is compulsory in tune with nagios state. (See notifier.cfg for explicit examples)

## To think

Is necessary to create notifier database before start using RGM advanced notification since v2.0

### Create database

A script exist to automaticaly create database on running system if default mysql root password as not changed :
> usr/share/doc/notifier/sql/create_database.sh

Just launch this script to create database.

## Tools

A script has be writted to migrate one version to other more easier.  
You'll find it in var/scripts/updates/v2.1.2_to_v2.1.3.sh

## Nagios commands

Two commands are necessary to create into nagios (by lilac configuration into RGM).

rgm_host_notifier :

```bash
$USER17$/bin/notifier.pl -t host -c $USER17$/etc/notifier.cfg -r $USER17$/etc/notifier.rules -T "$LONGDATETIME$" -h "$HOSTNAME$" -e "$HOSTSTATE$" -i "$HOSTADDRESS$" -n "$NOTIFICATIONTYPE$" -C "$CONTACTNAME$" -M "$CONTACTEMAIL$" -O "$HOSTOUTPUT$" -A "$HOSTGROUPNAMES$" -G "$CONTACTGROUPNAMES$" -X "$TIME$" -Y "$HOSTNOTIFICATIONNUMBER$" -N "$CONTACTPAGER$"
```

rgm_service_notifier :

```bash
$USER17$/bin/notifier.pl -t service -c $USER17$/etc/notifier.cfg -r $USER17$/etc/notifier.rules -T "$LONGDATETIME$" -h "$HOSTNAME$" -s "$SERVICEDESC$" -e "$SERVICESTATE$" -i "$HOSTADDRESS$" -n "$NOTIFICATIONTYPE$" -C "$CONTACTNAME$" -M "$CONTACTEMAIL$" -O "$SERVICEOUTPUT$" -A "$HOSTGROUPNAMES$" -B "$SERVICEGROUPNAMES$" -G "$CONTACTGROUPNAMES$" -X "$TIME$" -Y "$SERVICENOTIFICATIONNUMBER$" -N "$CONTACTPAGER$"
```

### Nagios macro used

 - `$USER17$` : Nagios ressource corresponding to USER17. (Default : /srv/rgm/notifier)
 - `$LONGDATETIME$` : Human readable date (i.e. Mon Dec 18 08:35:12 CEST 1000)
 - `$HOSTNAME$` : Name of host
 - `$HOSTSTATE$` : State of host
 - `$HOSTADDRESS` : Address of host (IP / FQDN)
 - `$SERVICEDESC$` : Service description
 - `$SERVICESTATE$` : Service state
 - `$NOTIFICATIONTYPE$` : Type of notification
 - `$CONTACTNAME$` : Username of contact (login)
 - `$CONTACTEMAIL$` : e-mail of contact
 - `$HOSTOUTPUT$` : Output returned by nagios plugin
 - `$SERVICEOUTPUT$` : Output returned by nagios plugin
 - `$HOSTGROUPNAMES$` : Names of linked hosts groups
 - `$SERVICEGROUPNAMES$` : Names of linked services groups
 - `$CONTACTGROUPNAMES$` : Names of linked contacts groups
 - `$TIME` : Current time (i.e. 08:35:12)
 - `$HOSTNOTIFICATIONNUMBER` : Number of notification already sent for this host
 - `$SERVICENOTIFICATIONNUMBER` : Number of notification already sent for this service
 - `$CONTACTPAGER$` : Pager of contact (Mobile phone number)

## Troubleshooting

### Version 2.1.3

Notifier manual execution command :

```bash
# Generic command
./notifier.pl -t <host|service> -c <config_file_path> -r <rules_file_path> -T <YYYY-MM-DD-HH:mm:ss> -h <hostname> -A <hostgroup> -B <servicegroup> -s <servicename> -e <state> -i <hostaddress> -n <method> -C <contact_name> -M <contact_email> -O <output> -X <YYYY-MM-DD-HH:mm:ss> -Y <notification_number> -N <contact_pager>

# Exemple command
./notifier.pl -t service -c /srv/rgm/notifier/etc/notifier.cfg -r /srv/rgm/notifier/etc/notifier.rules -T 2017-07-27-10:05:00 -h localhost -A LINUX -B GENERIC-SERVICES -s memory -e CRITICAL -i 127.0.0.1 -n email -C admin -M "admin@localhost" -O "Test memory critical" -X 2017-07-27-10:05:00 -Y 1
```

### SQL Syntax error

If you have an SQL Syntax error at notifier execution, probably you've not authorized characters in message body as quote or doublequote. Check this.

### Tracking not work

1. Check if you’ve correctly activate tracking option in rules file (Last field on each rules file line).
2. Check if your command name have the correct form as <command_def><STATE> (example: sms-appCRITICAL).