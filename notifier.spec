Summary:   RGM Advanced Notifier
Name:      notifier
Version:   2.1.3
Release:   6.rgm
BuildRoot: /tmp/%{name}-%{version}
Group:     Applications/Base
#BuildArch: noarch
License:   GPLv2
URL:       https://gitlab.nf.svk.gs/vfricou/notifier
Packager:  Vincent FRICOU <vincent@fricouv.eu>

# git rev. to checkout for Version
#%define notifier_git_commit 495708a3f1a81d759d9e49f0b031d1cf4836e83e
Source:    %{name}-%{version}.tar.gz

Requires: perl
Requires: perl-XML-Simple
Requires: logrotate
Requires: mariadb-libs
Requires: perl-DBI
Requires: perl-DBD-MySQL
Requires: git
Requires: rgm-base
Requires: python36

BuildRequires: rpm-macros-rgm
BuildRequires: python36-virtualenv python36-pip python3-wheel python36-setuptools


%description
RGM advanced notifier can provide a fine configuration for nagios notifications.

%prep
%define _unpackaged_files_terminate_build 0
%setup -q -n %{name}-%{version}

%build
# create on the fly python3 venv for msteams script
python3 -m venv --copies venv
./venv/bin/pip3 install pymsteams
# clean and patch python3 venv root path
find ./venv -name *.pyc -exec rm -f {} \;
find ./venv -name *.pyo -exec rm -f {} \;
BUILD_ENV=$(dirname $(grep ^VIRTUAL_ENV= ./venv/bin/activate | cut -d '"' -f 2 ))
for FILE in $(grep -FlR "$BUILD_ENV" $BUILD_ENV); do
	sed -i "s|${BUILD_ENV}|%{rgm_path}/%{name}/var|g" $FILE
done


%install
	mkdir -p ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/{etc,bin,log,var}
	mkdir -p ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/var/{venv,www}
	mkdir -p ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/var/scripts/updates
	mkdir -p ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/var/scripts/msteams/screenshots
	mkdir -p ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/var/scripts/slack
	mkdir -p ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/etc/messages
	mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d
	mkdir -p ${RPM_BUILD_ROOT}/usr/share/doc/%{name}/{etc,sql,messages,doc,templates}

	#binary
	install -m 775 bin/notifier.pl ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/bin/

	# doc tree
	install -m 664 usr/share/doc/notifier/etc/* ${RPM_BUILD_ROOT}/usr/share/doc/%{name}/etc/
	install -m 664 usr/share/doc/notifier/messages/* ${RPM_BUILD_ROOT}/usr/share/doc/%{name}/messages/
	install -m 664 usr/share/doc/notifier/doc/*  ${RPM_BUILD_ROOT}/usr/share/doc/%{name}/doc/
	install -m 664 usr/share/doc/notifier/sql/*  ${RPM_BUILD_ROOT}/usr/share/doc/%{name}/sql/
	install -m 664 usr/share/doc/notifier/templates/*  ${RPM_BUILD_ROOT}/usr/share/doc/%{name}/templates/

	# etc tree
	install -m 664 -o %{rgm_user_nagios} -g %{rgm_group} usr/share/doc/notifier/etc/notifier.cfg ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/etc/
	install -m 664 -o %{rgm_user_nagios} -g %{rgm_group} usr/share/doc/notifier/etc/notifier.rules ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/etc/
	install -m 664 -o %{rgm_user_nagios} -g %{rgm_group} usr/share/doc/notifier/etc/dbi.ini ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/etc/
	install -m 664 -o %{rgm_user_nagios} -g %{rgm_group} usr/share/doc/notifier/etc/msteams.ini ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/etc/
	install -m 664 -o %{rgm_user_nagios} -g %{rgm_group} usr/share/doc/notifier/etc/slack.ini ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/etc/
	install -m 664 usr/share/doc/notifier/messages/* ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/etc/messages/
	install -m 664 usr/share/doc/notifier/etc/notifier.logrotate ${RPM_BUILD_ROOT}/etc/logrotate.d/notifier

	# scripts
	install -m 775 var/scripts/createxml2sms.sh ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/var/scripts/
	install -m 775 -D var/scripts/updates/* ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/var/scripts/updates/
	install -m 775 -D var/scripts/slack/* ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/var/scripts/slack/
	
	# msteams and it python3 env
	cp -a venv/* ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/var/venv/
	install -m 664 -D var/scripts/msteams/screenshots/* ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/var/scripts/msteams/screenshots/
	install -m 775 -D var/scripts/msteams/*.py ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/var/scripts/msteams/

	# web
	install -m 664  var/www/index.html ${RPM_BUILD_ROOT}%{rgm_path}/%{name}/var/www/index.html


%postun
	rm -rf %{rgm_path}/%{name}
	
%clean
	rm -rf ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{rgm_path}/%{name}/bin/
#%config %{rgm_path}/%{name}/etc/
%config /etc/logrotate.d/notifier
%doc /usr/share/doc/notifier
%{rgm_path}/%{name}/var/
%config %attr (664,%{rgm_user_nagios},%{rgm_group}) %{rgm_path}/%{name}/etc/notifier.cfg
%config %attr (664,%{rgm_user_nagios},%{rgm_group}) %{rgm_path}/%{name}/etc/notifier.rules
%config %attr (664,%{rgm_user_nagios},%{rgm_group}) %{rgm_path}/%{name}/etc/dbi.ini
%config %attr (664,%{rgm_user_nagios},%{rgm_group}) %{rgm_path}/%{name}/etc/msteams.ini
%config %attr (664,%{rgm_user_nagios},%{rgm_group}) %{rgm_path}/%{name}/etc/slack.ini
%attr (775,%{rgm_user_nagios},%{rgm_group}) %{rgm_path}/%{name}/log/

%changelog
* Thu Nov 21 2019 Vincent Fricou <vincent@fricouv.eu> - 2.1.3-5.rgm
- fix payload for slack notification scripts

* Wed Nov 20 2019 Eric Belhomme <ebelhomme@fr.scc.com> - 2.1.3-4.rgm
- fix missing SQL schema (rules tables)
- add Slack support as notification target

* Thu Sep 19 2019 Eric Belhomme <ebelhomme@fr.scc.com> - 2.1.3-3.rgm
- DBI now have its dedicated config file dbi.ini
- fix missing msteams.ini config file

* Thu Sep 19 2019 Eric Belhomme <ebelhomme@fr.scc.com> - 2.1.3-2.rgm
- directory tree refactoring
- MS teams notifier integration
- rework of SPEC file

* Tue Sep 17 2019 Eric Belhomme <ebelhomme@fr.scc.com> - 2.1.3-1.rgm
- merged SCC repo on vfricou repo. vfricou now the upstrem repo for notifier
- adapt SCC CI/CD for building rpm package with upstream SPEC file

* Wed May 08 2019 Vincent Fricou <vincent@fricouv.eu> - 2.1.3-0.rgm
- fix all content of notifier to directly adapt to RGM

* Tue Mar 19 2019 Eric Belhomme <ebelhomme@fr.scc.com> - 2.1.2-1.rgm
- fix mariadb dependency to mariadb-libs

* Sun Mar 17 2019 Eric Belhomme <ebelhomme@fr.scc.com> - 2.1.2-0.rgm
- RGM packaging from upstream

* Thu Nov 2 2017 Vincent Fricou <vincent@fricouv.eu> - 2.1.1
(Refer to Git release : https://github.com/EyesOfNetworkCommunity/notifier/releases/tag/2.1-1)
- Now username was checked instead of email into notification rules
- Updated documentation
- Added script to update from previous version (2.1)
- Added script to check notifier.rules fields configuration
- Added log line to print contact name
