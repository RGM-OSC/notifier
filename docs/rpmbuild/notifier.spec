Summary:   RGM Advanced Notifier
Name:      notifier
Version:   2.1.3
Release:   1.rgm
BuildRoot: /tmp/%{name}-%{version}
Group:     Applications/Base
BuildArch: noarch
License:   GPLv2
URL:       https://gitlab.nf.svk.gs/vfricou/notifier
Packager:  Vincent FRICOU <vincent@fricouv.eu>

# git rev. to checkout for Version
%define notifier_git_commit 495708a3f1a81d759d9e49f0b031d1cf4836e83e
Source:    %{name}-%{version}.tar.gz

Requires: perl
Requires: perl-XML-Simple
Requires: logrotate
Requires: mariadb-libs
Requires: perl-DBI
Requires: perl-DBD-MySQL
Requires: git
Requires: rgm-base
BuildRequires: rpm-macros-rgm


%description
RGM advanced notifier can provide a fine configuration for nagios notifications.

%prep
%define _unpackaged_files_terminate_build 0
%setup -q -n %{name}-%{version}

%build

%install
	mkdir -p ${RPM_BUILD_ROOT}%{rgm_path}/
	mkdir -p ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/{bin,docs,etc,log,scripts,var}
	mkdir -p ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/docs/db
	mkdir -p ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/etc/{logrotate,messages}
	mkdir -p ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/scripts/updates
	mkdir -p ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/var/www

	install -m 775  bin/notifier.pl ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/bin/
	install -m 664  etc/notifier.cfg ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/etc/
	install -m 664 -o %{rgm_user_nagios} -g %{rgm_group} etc/notifier.rules ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/etc/
	install -m 664  etc/messages/sms-app-critical ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/etc/messages/
	install -m 664  etc/messages/sms-app-warning ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/etc/messages/
	install -m 664  etc/messages/sms-app-ok ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/etc/messages/
	install -m 664  etc/logrotate/%{name} ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/etc/logrotate/
	install -m 664  docs/notifier.cfg.md ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/docs/
	install -m 664  docs/notifier.rules.md ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/docs/
	install -m 664  docs/notifier_send.log.md ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/docs/
	install -m 664  docs/notifier_rules.log.md ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/docs/
	install -m 664  docs/platform.xsd.md ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/docs/
	install -m 664  docs/updates_scripts.md ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/docs/
	install -m 664  docs/db/notifier.sql ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/docs/db/
	install -m 775  scripts/createxml2sms.sh ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/scripts/createxml2sms.sh
	install -m 775 -D scripts/updates/*.sh ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/scripts/updates/
	install -m 664  var/www/index.html ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/var/www/index.html

	# retired from upstream
	# install -m 664  docs/db/create_database.sh ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/docs/db/
	# install -m 664  docs/db/create_user.txt ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}/docs/db/

%post
	cp -pr %{rgm_path}/%{name}/etc/* %{rgm_path}/%{name}-%{version}/etc
	cp -pr %{rgm_path}/%{name}/log/* %{rgm_path}/%{name}-%{version}/log
	cp -pr %{rgm_path}/%{name}/scripts/* %{rgm_path}/%{name}-%{version}/scripts
	# /usr/share/rgm/manage_sql.sh -d %{rgm_db_notifier} -s %{rgm_path}/%{name}-%{version}/docs/db/notifier.sql -u %{rgm_sql_internal_user} -p "%{rgm_sql_internal_pwd}"

%postun
	rm -rf %{rgm_path}/%{name}

%clean
	rm -rf ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{rgm_path}/%{name}-%{version}/bin/
%{rgm_path}/%{name}-%{version}/etc/
%{rgm_path}/%{name}-%{version}/docs/
%{rgm_path}/%{name}-%{version}/scripts/
%{rgm_path}/%{name}-%{version}/var/
%attr (664,%{rgm_user_nagios},%{rgm_group}) %{rgm_path}/%{name}-%{version}/etc/notifier.rules
%attr (775,%{rgm_user_nagios},%{rgm_group}) %{rgm_path}/%{name}-%{version}/log/
%attr (775,%{rgm_user_nagios},%{rgm_group}) %{rgm_path}/%{name}-%{version}/var/www/

%changelog
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
