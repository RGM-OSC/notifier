# README

This script permit to send notifications from monitoring platforms directly to Microsoft Teams channels by the bias of "Incoming Webhook" connector.

This script use [pymsteams](https://github.com/rveachkc/pymstreams) module to build card will send to Teams channels with needed informations.

## How to use

To could use correctly this script, you must copy the file __**define.orig.py**__ to define.py and correctly field all vars in this file. Specialy url to could send notifications to Teams Incoming Webhook.  
In same time, you must (if you’re not in RGM environment) change path in script __**PyWebHook.py**__.

```bash
git clone https://git.nf.svk.gs/vfricou/python_webhook.git
cd python_webhook
cp define.orig.py define.py
```

Replace line 7 in script with correct location path :

```python
sys.path.append('/srv/rgm/notifier/scripts/teams_notif')
```

Replace theses lines by your correct informations :
```python
server = "https://monitory.example.org"
cardTitle = "MonitoringSolution"
urlStandard = "<Microsoft_Teams_Incoming_Webhook_for_standard_notifications>"
urlApp = "<Microsoft_Teams_Incoming_Webhook_for_applications_notifications>"
urlCelCrise = "<Microsoft_Teams_Incoming_Webhook_for_prioritary_notifications>"
```

### CLI Usage

```bash
./venv/bin/python PyWebHook.py -h

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
```

The switch **-p** is specialy designed to could send notification in specific channel (different from standard for both other cases).

### Example

To send a basic host notification :

```bash
./venv/bin/python PyWebHook.py -t host -H localhost -a '10.1.0.41' -d 'Thu Nov 22 17:04:52 CET 2018' -o 'Test' -S 'OK'
```

To send a priority application notification :

```bash
./venv/bin/python PyWebHook.py -t application -H localhost -a '10.1.0.41' -d 'Thu Nov 22 17:04:52 CET 2018' -s 'Application Test' -o 'Test' -S 'CRITICAL' -p
```

## Screenshot

### Application card
![application_notif_up](./screenshot/application_notif_up.png)

### Service card
![standard_notif_critical_service](./screenshot/standard_notif_critical_service.png)
![standard_notif_warning_service](./screenshot/standard_notif_warning_service.png)
![standard_notif_up_service](./screenshot/standard_notif_up_service.png)

### Host card
![standard_notif_up_host](./screenshot/standard_notif_up_host.png)