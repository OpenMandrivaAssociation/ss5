%if "%{distribution}" == "Mandriva Linux"
        %if %mdkversion < 200900
                %define _localstatedir /var
        %endif
%endif

Summary: Socks Server 5 
Name: ss5
Version: 3.8.7
Release: %mkrel 5
License: GPL 
Group: System/Servers
URL: http://sourceforge.net/projects/ss5
Source: http://prdownloads.sourceforge.net/ss5/ss5-%{version}-1.tar.gz
Patch0: ss5-make.diff
Patch1: ss5-ss5-ha-loc.diff
Patch2: ss5-init.diff
Patch3: ss5-noopt.diff
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: openldap-devel
BuildRequires: pam-devel
BuildRequires: openssl-devel 
BuildRequires: gssglue-devel
BuildRequires: krb5-devel
BuildRequires: mysql-devel

%description
ss5 is a socks server, which supports both SOCKS4 and SOCKS5 protocols,
that runs on Linux, Solaris and FreeBSD platforms. 

%prep
%setup -n ss5-%{version}
%patch0 -p0 -b .makedir
%patch1 -p0 -b .ss5ha
%patch2 -p0 -b .lsb
%patch3 -p0 -b .noopt

%build

%configure2_5x \
	--with-epollio \
	--with-gssapi \
	--with-mysql \
	--with-logpathbase=%{_logdir}/ss5 \
	--with-configfile=%{_sysconfdir}/ss5/ss5.conf \
	--with-passwordfile=%{_sysconfdir}/ss5/ss5.passwd \
	--with-logfile=%{_logdir}/ss5/ss5.log \
	--with-profilepath=%{_sysconfdir}/ss5 \
	--with-libpath=%{_libdir} \
	--with-tracepath=%{_logdir}/ss5 \
	--with-confpathbase=%{_sysconfdir}

make -j2 CXX="g++ %optflags" 

%install 
rm -rf %{buildroot}
%makeinstall dst_dir=%{?buildroot:%{buildroot}}

find %{?buildroot:%{buildroot}}/%_mandir -name "*.bz2" -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service ss5

%preun
%_preun_service squid

if [ $1 = 0 ]; then
#        /sbin/service ss5 stop > /dev/null 2>&1
        /sbin/chkconfig --del ss5
fi

%files
%defattr(755,root,root)
%{_sbindir}/ss5
%{_sbindir}/ss5srv
%{_initrddir}/ss5
%{_libdir}/ss5/

%defattr(644,root,root)
%dir %{_docdir}/ss5
%{_docdir}/ss5/License
%{_docdir}/ss5/README.pam
%dir %{_docdir}/ss5/examples
%{_docdir}/ss5/examples/ss5.pam
%{_docdir}/ss5/README.ldap
%{_docdir}/ss5/examples/slapd.conf
%{_docdir}/ss5/examples/entries.ldif
%{_docdir}/ss5/README.statmgr
%{_docdir}/ss5/README.balamgr

%{_mandir}/man1/ss5.1.*
%{_mandir}/man1/ss5srv.1.*
%{_mandir}/man5/ss5.passwd.5.*
%{_mandir}/man5/ss5.ha.5.*
%{_mandir}/man5/ss5.conf.5.*
%{_mandir}/man5/ss5.pam.5.*
%{_mandir}/man5/ss5_gss.5.*
%{_mandir}/man5/ss5_supa.5.*

%defattr(755,root,root)
%{_localstatedir}/log/ss5

%defattr(644,root,root)
%dir %{_sysconfdir}/ss5
%config(noreplace) %{_sysconfdir}/ss5/ss5.conf
%config(noreplace) %{_sysconfdir}/ss5/ss5.passwd
%config(noreplace) %{_sysconfdir}/ss5/ss5.ha
%config(noreplace) %{_sysconfdir}/pam.d/ss5
%config(noreplace) %{_sysconfdir}/sysconfig/ss5

