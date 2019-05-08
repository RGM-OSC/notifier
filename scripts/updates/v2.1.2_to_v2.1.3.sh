#!/bin/bash

PrevVersion="2.1.2"
NewVersion="2.1.3"
ScriptName="v${PrevVersion}_to_v${NewVersion}.sh"
PrevNotifier="/srv/rgm/notifier"
LatestNotifier="/srv/rgm/notifier-${NewVersion}"
NotAction=""

usage () {
        printf "This script is writted to simplify notifier version updates.
It'll be copy all configurations of previous version, and update symbolic link in case of standard usage.

Usage of ${ScriptName} :
        -h : Display this help
        -y : Force yes
        -l : No update symbolic link
        -p <path> : Specify previous notifier release path
        -n <path> : Specify new notifier path
        
        Example. Considering notifier is previous version and notifier-${NewVersion} is newer version :
                bash ./v${PrevVersion}_to_v${NewVersion}.sh -p /srv/rgm/notifier/ -n /srv/rgm/notifier-${NewVersion}/

        If you don't specify path, this script will use standard RGM notifier paths.
        The standard RGM deployement path :
          - /srv/rgm/notifier (symbolic link)
          - /srv/rgm/notifier-${Newversion} (folder containing notifier)

        Note : This script will automaticaly launch notifier.rules file check to sort all configuration line with missing arguments.\n"
        exit 128
}

while getopts hylp:n: arg
do
    case "$arg" in
        h) usage;;
        y) ASSUMEYES=1;;
        l) NotAction="symlink";;
        p) PrevNotifier="$OPTARG";;
        n) LatestNotifier="$OPTARG";;
    esac
done

ConfFolders="etc/*"
LogFolders="log"

if [ -z ${ASSUMEYES} ]
then
    printf "Copy configurations and logs from previous notifier version to new notifier version following command ? [Y/n]\n"
    printf "rsync -av ${PrevNotifier}/${ConfFolders} ${LatestNotifier} && rsync -av ${PrevNotifier}/${LogFolders} ${LatestNotifier} ? "
    read Choice
    if [[ "${Choice}" == "n" || "${Choice}" == "N" ]]
    then
            printf "Copy aborted\n"
            exit 2
    fi
    if [[ "${Choice}" == "Y" || "${Choice}" == "y" || "${Choice}" == "" ]]
    then
            rsync -av ${PrevNotifier}/${ConfFolders} ${LatestNotifier}/etc && rsync -av ${PrevNotifier}/${LogFolders} ${LatestNotifier}
            if [ $? == 0 ]
            then
                    printf "Copy success\n"
                    Status=0
            else
                    printf "Copy failed\n"
                    exit 3
            fi

            if [[ ${Status} == 0 && "${NotAction}" != "symlink" ]]
            then
                    rm ${PrevNotifier}
                    ln -s ${LatestNotifier} ${PrevNotifier}
            fi
    fi
else
    printf "Copy configurations and logs from previous notifier version to new notifier version.\n"
    rsync -av ${PrevNotifier}/${ConfFolders} ${LatestNotifier}/etc && rsync -av ${PrevNotifier}/${LogFolders} ${LatestNotifier}
    if [ $? == 0 ]
    then
            printf "Copy success\n"
            Status=0
    else
            printf "Copy failed\n"
            exit 3
    fi
    if [[ ${Status} == 0 && "${NotAction}" != "symlink" ]]
    then
        printf "Replace previous notifier symbolic link to v${NewVersion} ($LatestNotifier).\n"
        rm ${PrevNotifier}
        ln -s ${LatestNotifier} ${PrevNotifier}
    fi
fi

printf "Checking config file fields.\n"
bash ./check_config_file.sh ${LatestNotifier}/etc/notifier.rules

