Name:		shibboleth
Version:	2.5.1
Release:	1
Summary:	Open source system for attribute-based Web SSO
Group:		Productivity/Networking/Security
Vendor:		Shibboleth Consortium
License:	Apache 2.0
URL:		http://shibboleth.net/
Source:		%{name}-sp-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-sp-%{version}-root
Obsoletes:	shibboleth-sp = 2.5.0
Requires:	openssl
%if 0%{?rhel} >= 6 || 0%{?centos_version} >= 600
PreReq:		xmltooling-schemas%{?_isa} >= 1.5.0, opensaml-schemas%{?_isa} >= 2.5.0
%else
PreReq:         xmltooling-schemas >= 1.5.0, opensaml-schemas >= 2.5.0
%endif
%if 0%{?suse_version} > 1030 && 0%{?suse_version} < 1130
PreReq:		%{insserv_prereq} %{fillup_prereq}
BuildRequires:	libXerces-c-devel >= 2.8.0
%else
BuildRequires:	libxerces-c-devel >= 2.8.0
%endif
BuildRequires:	libxml-security-c-devel >= 1.4.0
BuildRequires:	libxmltooling-devel >= 1.5.0
BuildRequires:	libsaml-devel >= 2.5.0
%{?_with_log4cpp:BuildRequires: liblog4cpp-devel >= 1.0}
%{!?_with_log4cpp:BuildRequires: liblog4shib-devel >= 1.0.4}
%if 0%{?rhel} >= 6 || 0%{?centos_version} >= 600
Requires:	libcurl-openssl%{?_isa} >= 7.21.7
BuildRequires:	chrpath
%endif
BuildRequires:  gcc-c++, zlib-devel, boost-devel >= 1.32.0
%{!?_without_doxygen:BuildRequires: doxygen}
%{!?_without_odbc:BuildRequires:unixODBC-devel}
%{?_with_fastcgi:BuildRequires: fcgi-devel}
%if 0%{?centos_version} >= 600
BuildRequires:	libmemcached-devel
%endif
%{?_with_memcached:BuildRequires: libmemcached-devel}
%if "%{_vendor}" == "redhat"
%if 0%{?rhel} >= 6 || 0%{?centos_version} >= 600
%{!?_without_builtinapache:BuildRequires: httpd-devel%{?_isa}}
%else
%{!?_without_builtinapache:BuildRequires: httpd-devel}
%endif
BuildRequires: redhat-rpm-config
Requires(pre): shadow-utils
Requires(post): chkconfig
Requires(preun): chkconfig, initscripts
%endif
%if "%{_vendor}" == "suse"
Requires(pre): pwdutils
%{!?_without_builtinapache:BuildRequires: apache2-devel}
%endif

%define runuser shibd
%if "%{_vendor}" == "suse"
%define pkgdocdir %{_docdir}/shibboleth
%else
%define pkgdocdir %{_docdir}/shibboleth-%{version}
%endif

%description
Shibboleth is a Web Single Sign-On implementations based on OpenSAML
that supports multiple protocols, federated identity, and the extensible
exchange of rich attributes subject to privacy controls.

This package contains the Shibboleth Service Provider runtime libraries,
daemon, default plugins, and Apache module(s).

%package devel
Summary:	Shibboleth Development Headers
Group:		Development/Libraries/C and C++
Requires:	%{name} = %{version}-%{release}
Obsoletes:	shibboleth-sp-devel = 2.5.0
%if 0%{?suse_version} > 1030 && 0%{?suse_version} < 1130
Requires:	libXerces-c-devel >= 2.8.0
%else
Requires: 	libxerces-c-devel >= 2.8.0
%endif
Requires: 	libxml-security-c-devel >= 1.4.0
Requires: 	libxmltooling-devel >= 1.5.0
Requires: 	libsaml-devel >= 2.5.0
%{?_with_log4cpp:Requires: liblog4cpp-devel >= 1.0}
%{!?_with_log4cpp:Requires: liblog4shib-devel >= 1.0.4}

%description devel
Shibboleth is a Web Single Sign-On implementations based on OpenSAML
that supports multiple protocols, federated identity, and the extensible
exchange of rich attributes subject to privacy controls.

This package includes files needed for development with Shibboleth.

%prep
%setup -n %{name}-sp-%{version}

%build
%if 0%{?centos_version} >= 600
	%configure %{?_without_odbc:--disable-odbc} %{?_without_adfs:--disable-adfs} %{?_with_fastcgi} %{!?_without_memcached:--with-memcached} %{?shib_options}
%else
	%configure %{?_without_odbc:--disable-odbc} %{?_without_adfs:--disable-adfs} %{?_with_fastcgi} %{?_with_memcached} %{?shib_options}
%endif
%{__make} pkgdocdir=%{pkgdocdir}

%install
%{__make} install NOKEYGEN=1 DESTDIR=$RPM_BUILD_ROOT pkgdocdir=%{pkgdocdir}

%if "%{_vendor}" == "suse"
	%{__sed} -i "s/\/var\/log\/httpd/\/var\/log\/apache2/g" \
		$RPM_BUILD_ROOT%{_sysconfdir}/shibboleth/native.logger
%endif

# Plug the SP into the built-in Apache on a recognized system.
touch rpm.filelist
APACHE_CONFIG="no"
if [ -f $RPM_BUILD_ROOT%{_libdir}/shibboleth/mod_shib_13.so ] ; then
	APACHE_CONFIG="apache.config"
fi
if [ -f $RPM_BUILD_ROOT%{_libdir}/shibboleth/mod_shib_20.so ] ; then
	APACHE_CONFIG="apache2.config"
fi
if [ -f $RPM_BUILD_ROOT%{_libdir}/shibboleth/mod_shib_22.so ] ; then
	APACHE_CONFIG="apache22.config"
fi
if [ -f $RPM_BUILD_ROOT%{_libdir}/shibboleth/mod_shib_24.so ] ; then
	APACHE_CONFIG="apache24.config"
fi
%{?_without_builtinapache:APACHE_CONFIG="no"}
if [ "$APACHE_CONFIG" != "no" ] ; then
	APACHE_CONFD="no"
	if [ -d %{_sysconfdir}/httpd/conf.d ] ; then
		APACHE_CONFD="%{_sysconfdir}/httpd/conf.d"
	fi
	if [ -d %{_sysconfdir}/apache2/conf.d ] ; then
		APACHE_CONFD="%{_sysconfdir}/apache2/conf.d"
	fi
	if [ "$APACHE_CONFD" != "no" ] ; then
		%{__mkdir} -p $RPM_BUILD_ROOT$APACHE_CONFD
		%{__cp} -p $RPM_BUILD_ROOT%{_sysconfdir}/shibboleth/$APACHE_CONFIG $RPM_BUILD_ROOT$APACHE_CONFD/shib.conf 
		echo "%config(noreplace) $APACHE_CONFD/shib.conf" >> rpm.filelist
	fi
fi

# Establish location of sysconfig file, if any.
SYSCONFIG_SHIBD="no"
%if "%{_vendor}" == "redhat"
	%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
	echo "%config(noreplace) %{_sysconfdir}/sysconfig/shibd" >> rpm.filelist
	SYSCONFIG_SHIBD="$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/shibd"
%endif
%if "%{_vendor}" == "suse"
	%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/adm/fillup-templates
	echo "%{_localstatedir}/adm/fillup-templates/sysconfig.shibd" >> rpm.filelist
	SYSCONFIG_SHIBD="$RPM_BUILD_ROOT%{_localstatedir}/adm/fillup-templates/sysconfig.shibd"
%endif
if [ "$SYSCONFIG_SHIBD" != "no" ] ; then
	# Populate the sysconfig file.
	cat > $SYSCONFIG_SHIBD <<EOF
# Shibboleth SP init script customization

# User account for shibd
SHIBD_USER=%{runuser}
EOF
	%if 0%{?rhel} >= 6 || 0%{?centos_version} >= 600
		cat >> $SYSCONFIG_SHIBD <<EOF

# Override OS-supplied libcurl
export LD_LIBRARY_PATH=/opt/shibboleth/%{_lib}
EOF
		# Strip existing rpath to libcurl.
		chrpath -d $RPM_BUILD_ROOT%{_sbindir}/shibd
		chrpath -d $RPM_BUILD_ROOT%{_bindir}/mdquery
		chrpath -d $RPM_BUILD_ROOT%{_bindir}/resolvertest
	%endif
fi

%if "%{_vendor}" == "redhat" || "%{_vendor}" == "suse"
	# %{_initddir} not yet in RHEL5, use deprecated %{_initrddir}
	install -d -m 0755 $RPM_BUILD_ROOT%{_initrddir}
	install -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/shibboleth/shibd-%{_vendor} $RPM_BUILD_ROOT%{_initrddir}/shibd
%if "%{_vendor}" == "suse"
	install -d -m 0755 $RPM_BUILD_ROOT/%{_sbindir}
	%{__ln_s} -f %{_initrddir}/shibd $RPM_BUILD_ROOT%{_sbindir}/rcshibd
%endif
%endif

%check
%{__make} check

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{runuser} >/dev/null || groupadd -r %{runuser}
getent passwd %{runuser} >/dev/null || useradd -r -g %{runuser} \
	-d  %{_localstatedir}/run/shibboleth -s /sbin/nologin -c "Shibboleth SP daemon" %{runuser}
exit 0

%post
%ifnos solaris2.8 solaris2.9 solaris2.10 solaris2.11
/sbin/ldconfig
%endif

# Key generation or ownership fix
cd %{_sysconfdir}/shibboleth
if [ -f sp-key.pem ] ; then
	%{__chown} %{runuser}:%{runuser} sp-key.pem sp-cert.pem 2>/dev/null || :
else
	sh ./keygen.sh -b -u %{runuser} -g %{runuser}
fi

# Fix ownership of log files (even on new installs, if they're left from an older one).
%{__chown} %{runuser}:%{runuser} %{_localstatedir}/log/shibboleth/* 2>/dev/null || :

%if "%{_vendor}" == "redhat"
	if [ "$1" -gt "1" ] ; then
		# On Red Hat with shib.conf installed, clean up old Alias commands
		# by pointing them at new version-independent /usr/share/share tree.
		# Any Aliases we didn't create we assume are custom files.
		# This is to accomodate making shib.conf a noreplace config file.
		# We can't do this for SUSE, because they disallow changes to
		# packaged files in scriplets.
		APACHE_CONF="no"
		if [ -f %{_sysconfdir}/httpd/conf.d/shib.conf ] ; then
			APACHE_CONF="%{_sysconfdir}/httpd/conf.d/shib.conf"
		fi
		if [ "$APACHE_CONF" != "no" ] ; then
			%{__sed} -i "s/\/usr\/share\/doc\/shibboleth\(\-\(.\)\{1,\}\)\{0,1\}\/main\.css/\/usr\/share\/shibboleth\/main.css/g" \
				$APACHE_CONF
			%{__sed} -i "s/\/usr\/share\/doc\/shibboleth\(\-\(.\)\{1,\}\)\{0,1\}\/logo\.jpg/\/usr\/share\/shibboleth\/logo.jpg/g" \
				$APACHE_CONF
		fi
	fi

	# This adds the proper /etc/rc*.d links for the script
	/sbin/chkconfig --add shibd
%endif
%if "%{_vendor}" == "suse"
	# This adds the proper /etc/rc*.d links for the script
	# and populates the sysconfig/shibd file.
	cd /
	%{fillup_only -n shibd}
	%insserv_force_if_yast shibd
%endif

%preun
# On final removal, stop shibd and remove service, restart Apache if running.
%if "%{_vendor}" == "redhat"
	if [ "$1" -eq 0 ] ; then
		/sbin/service shibd stop >/dev/null 2>&1
		/sbin/chkconfig --del shibd
		%{!?_without_builtinapache:/etc/init.d/httpd status 1>/dev/null && /etc/init.d/httpd restart 1>/dev/null}
	fi
%endif
%if "%{_vendor}" == "suse"
	%stop_on_removal shibd
	if [ "$1" -eq 0 ] ; then
		%{!?_without_builtinapache:/etc/init.d/apache2 status 1>/dev/null && /etc/init.d/apache2 restart 1>/dev/null}
	fi
%endif
exit 0

%postun
%ifnos solaris2.8 solaris2.9 solaris2.10 solaris2.11
/sbin/ldconfig
%endif
%if "%{_vendor}" == "redhat"
	# On upgrade, restart components if they're already running.
	if [ "$1" -ge "1" ] ; then
		/etc/init.d/shibd status 1>/dev/null && /etc/init.d/shibd restart 1>/dev/null
		%{!?_without_builtinapache:/etc/init.d/httpd status 1>/dev/null && /etc/init.d/httpd restart 1>/dev/null}
		exit 0
	fi
%endif
%if "%{_vendor}" == "suse"
	cd / 
	%restart_on_update shibd
	%{!?_without_builtinapache:%restart_on_update apache2}
	%{insserv_cleanup}
%endif

%posttrans
# ugly hack if init script got removed during %postun by upgraded (buggy/2.1) package
%if "%{_vendor}" == "redhat"
	if [ ! -f %{_initrddir}/shibd ] ; then
		if [ -f %{_sysconfdir}/shibboleth/shibd-%{_vendor} ] ; then
			%{__cp} -p %{_sysconfdir}/shibboleth/shibd-%{_vendor} %{_initrddir}/shibd
			%{__chmod} 755 %{_initrddir}/shibd
			/sbin/chkconfig --add shibd
	fi
fi
%endif

%files -f rpm.filelist
%defattr(-,root,root,-)
%{_sbindir}/shibd
%{_bindir}/mdquery
%{_bindir}/resolvertest
%{_libdir}/libshibsp.so.*
%{_libdir}/libshibsp-lite.so.*
%dir %{_libdir}/shibboleth
%{_libdir}/shibboleth/*
%attr(0750,%{runuser},%{runuser}) %dir %{_localstatedir}/log/shibboleth
%attr(0755,%{runuser},%{runuser}) %dir %{_localstatedir}/run/shibboleth
%attr(0755,%{runuser},%{runuser}) %dir %{_localstatedir}/cache/shibboleth
%dir %{_datadir}/xml/shibboleth
%{_datadir}/xml/shibboleth/*
%dir %{_datadir}/shibboleth
%{_datadir}/shibboleth/*
%dir %{_sysconfdir}/shibboleth
%config(noreplace) %{_sysconfdir}/shibboleth/*.xml
%config(noreplace) %{_sysconfdir}/shibboleth/*.html
%config(noreplace) %{_sysconfdir}/shibboleth/*.logger
%if "%{_vendor}" == "redhat" || "%{_vendor}" == "suse"
%config %{_initrddir}/shibd
%endif
%if "%{_vendor}" == "suse"
%{_sbindir}/rcshibd
%endif
%{_sysconfdir}/shibboleth/*.dist
%{_sysconfdir}/shibboleth/apache*.config
%{_sysconfdir}/shibboleth/shibd-*
%attr(0755,root,root) %{_sysconfdir}/shibboleth/keygen.sh
%attr(0755,root,root) %{_sysconfdir}/shibboleth/metagen.sh
%{_sysconfdir}/shibboleth/*.xsl
%doc %{pkgdocdir}
%exclude %{pkgdocdir}/api

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libshibsp.so
%{_libdir}/libshibsp-lite.so
%doc %{pkgdocdir}/api

%changelog
* Tue Sep 25 2012  Scott Cantor  <cantor.2@osu.edu>  - 2.5.1-1
- Merge back various changes used in released packages
- Prep for 2.5.1 by pulling extra restart out

* Tue Aug 7 2012  Scott Cantor  <cantor.2@osu.edu>  - 2.5.0-2
- Changed package name back to shibboleth because of upgrade bugs
- Put back extra restart for this release only.

* Thu Mar 1 2012  Scott Cantor  <cantor.2@osu.edu>  - 2.5.0-1
- Move logo and stylesheet to version-independent tree
- Make shib.conf noreplace
- Post-fixup of Alias commands in older shib.conf
- Changes to run shibd as non-root shibboleth user
- Move init customizations to /etc/sysconfig/shibd
- Copy shibd restart for Red Hat to postun
- Add boost-devel dependency
- Build memcache plugin on RH6
- Add cachedir to install
- Add Apache 2.4 to install

* Sun Jun 26 2011  Scott Cantor  <cantor.2@osu.edu>  - 2.4.3-1
- Log files shouldn't be world readable.
- Explicit requirement for libcurl-openssl on RHEL6
- Uncomment LD_LIBRARY_PATH in init script for RHEL6 
- Remove rpath from binaries for RHEL6

* Fri Dec 25 2009  Scott Cantor  <cantor.2@osu.edu>  - 2.4-1
- Update dependencies.

* Mon Nov 23 2009 Scott Cantor  <cantor.2@osu.edu>  - 2.3.1-1
- Reset revision for 2.3.1 release

* Wed Aug 19 2009 Scott Cantor  <cantor.2@osu.edu>  - 2.2.1-2
- SuSE init script changes
- Restart Apache on removal, not just upgrade
- Fix scriptlet exit values when Apache is stopped

* Mon Aug 10 2009 Scott Cantor  <cantor.2@osu.edu>  - 2.2.1-1
- Doc handling changes
- SuSE init script

* Tue Aug 4 2009 Scott Cantor  <cantor.2@osu.edu>  - 2.2.1-1
- Initial version for 2.2.1, with shibd/httpd restart on upgrade

* Thu Jun 25 2009 Scott Cantor  <cantor.2@osu.edu>  - 2.2-3
- Add additional cleanup to posttrans fix

* Tue Jun 23 2009 Scott Cantor  <cantor.2@osu.edu>  - 2.2-2
- Reverse without_builtinapache macro test
- Fix init script handling on Red Hat to handle upgrades

* Wed Dec 3 2008  Scott Cantor  <cantor.2@osu.edu>  - 2.2-1
- Bump minor version.
- Make keygen.sh executable.
- Fixing SUSE Xerces dependency name.
- Optionally package shib.conf.

* Tue Jun 10 2008  Scott Cantor  <cantor.2@osu.edu>  - 2.1-1
- Change shib.conf handling to treat as config file.

* Mon Mar 17 2008  Scott Cantor  <cantor.2@osu.edu>  - 2.0-6
- Official release.

* Fri Jan 18 2008  Scott Cantor  <cantor.2@osu.edu>  - 2.0-5
- Release candidate 1.

* Sun Oct 21 2007 Scott Cantor  <cantor.2@osu.edu>  - 2.0-4
- libexec -> lib/shibboleth changes
- Added doc subpackage

* Thu Aug 16 2007 Scott Cantor  <cantor.2@osu.edu>  - 2.0-3
- First public beta.

* Fri Jul 13 2007 Scott Cantor	<cantor.2@osu.edu>  - 2.0-2
- Second alpha release.

* Sun Jun 10 2007 Scott Cantor	<cantor.2@osu.edu>  - 2.0-1
- First alpha release.

* Mon Oct 2 2006 Scott Cantor	<cantor.2@osu.edu>  - 1.3-11
- Applied fix for secadv 20061002
- Fix for metadata loader loop

* Wed Jun 15 2006 Scott Cantor  <cantor.2@osu.edu>  - 1.3-10
- Applied fix for sec 20060615

* Fri Apr 15 2006 Scott Cantor  <cantor.2@osu.edu>  - 1.3-9
- Misc. patches, SuSE, Apache 2.2, gcc 4.1, and 64-bit support

* Mon Jan 9 2006 Scott Cantor  <cantor.2@osu.edu>  - 1.3-8
- Applied new fix for secadv 20060109

* Tue Nov 8 2005 Scott Cantor  <cantor.2@osu.edu>  - 1.3-7
- Applied new fix for secadv 20050901 plus rollup

* Fri Sep 23 2005 Scott Cantor  <cantor.2@osu.edu>  - 1.3-6
- Minor patches and default config changes
- pidfile patch
- Fix shib.conf creation
- Integrated init.d script
- Prevent replacement of config files

* Thu Sep 1 2005  Scott Cantor  <cantor.2@osu.edu>  - 1.3-5
- Applied fix for secadv 20050901 plus rollup of NSAPI fixes

* Sun Apr 24 2005  Scott Cantor  <cantor.2@osu.edu>  - 1.3-1
- Updated test programs and location of schemas.
- move siterefresh to to sbindir

* Fri Apr  1 2005  Derek Atkins  <derek@ihtfp.com>  - 1.3-1
- Add selinux-targeted-policy package
- move shar to sbindir

* Tue Oct 19 2004  Derek Atkins  <derek@ihtfp.com>  - 1.2-1
- Create SPEC file based on various versions in existence.
