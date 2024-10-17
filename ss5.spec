%if "%{distribution}" == "Mandriva Linux"
        %if %mdkversion < 200900
                %define _localstatedir /var
        %endif
%endif

Summary: Socks Server 5 
Name: ss5
Version: 3.8.9
Release: 2
License: GPL 
Group: System/Servers
URL: https://sourceforge.net/projects/ss5
Source: http://prdownloads.sourceforge.net/ss5/ss5-%{version}-5.tar.gz
Patch0: ss5-make.diff
Patch1: ss5-ss5-ha-loc.diff
Patch2: ss5-init.diff
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



%changelog
* Mon Jan 23 2012 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.8.9-1mdv2011.0
+ Revision: 767214
- 3.8.9-5 latest stable snapshoot

* Sat Jul 30 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.8.7-5
+ Revision: 692322
- P3 dropped
- trying to make this SPEC compatible with mageia so it will be easier for me
- rebuild for new gssglue

* Thu Jun 23 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.8.7-1
+ Revision: 686835
- 3.8.7

* Sat Apr 16 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.8.6-1
+ Revision: 653269
- 3.8.6

* Sun Mar 20 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.8.5-1
+ Revision: 647114
- 3.8.5

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 3.8.4-2
+ Revision: 645897
- relink against libmysqlclient.so.18

* Wed Dec 29 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.8.4-1mdv2011.0
+ Revision: 625828
- 3.8.4
- mysql support
- 3.8.3

* Fri Jul 16 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.8.2-2mdv2011.0
+ Revision: 554437
- Backport 2008.1-  support

* Tue Jul 13 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.8.2-1mdv2011.0
+ Revision: 552693
- 3.8.2

* Wed May 05 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.8.1-2mdv2010.1
+ Revision: 542710
- P2 for LSB complain init script

* Tue Apr 27 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.8.1-1mdv2010.1
+ Revision: 539627
- 3.8.1

* Mon Apr 05 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.7.9-4mdv2010.1
+ Revision: 531770
- Rebuild for new OpenSSL

* Thu Mar 18 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.7.9-3mdv2010.1
+ Revision: 524896
- Correct Group

* Sat Feb 27 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.7.9-2mdv2010.1
+ Revision: 512260
- P1 to fix ss5.ha looking for

* Fri Feb 26 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.7.9-1mdv2010.1
+ Revision: 512147
- Akdd krb5-devel as BR
- Correct group
- import ss5


*Sun Oct  11 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.9-2
        * SS5-v3.7.9-2 released
        * Fix mod socks4/5 (thx to Pasi Saarinen )

*Sun Aug  30 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.9-1
        * SS5-v3.7.9-1 released
        * Add infinite idle timeout

*Thu Aug  13 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.8-12
        * SS5-v3.7.8-12 released
        * Fix default thread stack restoring 128k
        * Bugs fix mod_socks (thx to Maurizio Caneve)

*Thu Jul  30 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.8-11
        * SS5-v3.7.8-11 released
        * Bugs fix epoll syscall

*Mon Jul  27 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.8-10
        * SS5-v3.7.8-10 released
        * Fix bugs
        * Fix default thread stack
        * Fix package (add EPOLL IO flag)

*Fri Jul  24 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.8-9
        * SS5-v3.7.8-9 released
        * Fix bugs
        * Fix packages

*Mon Jul  06 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.8-8
        * SS5-v3.7.8-8 released
        * Fix socks vulnerability
        * Add 64bit file size support

*Wed Jul  01 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.8-7
        * SS5-v3.7.8-7 released
        * Fix SOLARIS build
        * Fix GSSAPI build

*Tue Jun  30 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.8-6
        * SS5-v3.7.8-6 released
        * Fix EAP

*Fri Jun  12 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.8-5
        * SS5-v3.7.8-5 released
        * Fix dns resolution for thread-safe environment

*Sun Jun  01 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.8-4
        * SS5-v3.7.8-4 released
        * Fix mod_socks5 credential upstream proxy

*Sat May  30 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.8-3
        * SS5-v3.7.8-3 released
        * Fix core for memory leak

*Wed Apr  22 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.8-2
        * SS5-v3.7.8-2 released
        * Fix CORE

*Fri Apr  10 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.8-1
        * SS5-v3.7.8-1 released
        * Fix mod_socks5 udp routing

*Tue Apr  07 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.7-1
        * SS5-v3.7.7-1 released
        * Fix core
        * Fix hash
        * Add new commands to ss5srv tool

*Sat Mar  28 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.6-1
        * SS5-v3.7.6-1 released
        * Fix mod_bandwidth

*Wed Mar  25 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.5-2
        * SS5-v3.7.5-2 released
        * Fix UDP_ASSOCIATE to support multiple udp packets (RFC compliant)
        * Fix code

*Wed Mar  25 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.4-2
        * SS5-v3.7.4-2 released
        * Fix configure option for Solaris and GssApi

*Sun Mar  22 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.4-1
        * SS5-v3.7.4-1 released
        * Fix GSSAPI

*Thu Mar  19 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.3-1
        * SS5-v3.7.3-1 released
        * Fix SYSConfig environment
        * Add "dash" flag as group (equal to all users) for <bandwidth> directive
        * Fix UDP_ASSOCIATE

*Sun Feb  15 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.2-1
        * SS5-v3.7.2-1 released
        * Server manager update
        * Add icp (Internet Cache Protocol) support to module Filter
        * Add GSSApi authetication message support
        * Add syslog facility and level configuration option
        * Fix solaris CFLAGS
        * Fix bug HA file
        * Fix code

*Sun Jan  11 2009 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.7.1-12
        * SS5-v3.7.1-12 released
        * Fix code
        * Fix init script
        * Add SUPA support (Thanks to Raffaele DeLorenzo - raffaele.delorenzo@libero.it)
        * Add <bandwidth> directive to limit bandwidth and number 
          of connections per user

*Wed Jul  18 2007 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.6.4-4
        * SS5-v3.6.4-4 released
        * Fix mod_socksX

*Sun Jun  10 2007 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.6.4-3
        * SS5-v3.6.4-3 released
        * Fix code

*Wed May  28 2007 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.6.4-2
        * SS5-v3.6.4-2 released
        * Fix Utils

*Wed May  24 2007 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.6.4-1
        * SS5-v3.6.4-1 released
        * Change ss5.peers file

*Wed May  16 2007 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.6.3-2
        * SS5-v3.6.3-2 released
        * Fix man files

*Tue May  15 2007 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.6.3-1
        * SS5-v3.6.3-1 released
	* Fix mod_dump
        * Fix spec file    (see bugzilla)
        * Fix startup file (add sysconfig support)
	* Add flag to route

*Thu Apr  05 2007 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.6.2-1
        * SS5-v3.6.2-1 released
	* Fix core (stderr)
	* Fix setuid/gid (thx to Enrico Scholz)
        * Fix security   (file ss5.passwd)

*Thu Aug  24 2006 Matteo Ricchetti <matteo.ricchetti@libero.it> - 3.6.1-1
        * SS5-v3.6.1-1 released
	* Add BSD support
        * Fix ldap authorization
        * Extend "route" feature adding user group field
        * Extend "permit" feature adding expiration date field
        * Add cgi-bin for web statistics and balancing
        * Fix mod_balance
        * Fix mod_filter
        * Fix max network interfaces policy
	* Add set option to enable/disable web console
	* Fix configure.ac for Deb distribution (thx to Francisco Gimeno)
        * Fix Makefile uninstall section for Solaris

*Mon May  08 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.5.9-1 released
        * Fix replication feature
        * Fix DNS buffer as RFC

*Fri May  05 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
	* SS5-v3.5.8-2 released
        * Fix startup script

*Wed Apr  26 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.5.8-1 released
        * Fix EAP (thx to Jakob Perz)

*Mon Apr  24 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
	* SS5-v3.5.7-1 released
	* Fix replica feature
        * Fix configure file
        * Fix man file for ss5.peers

*Mon Apr  10 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
	* SS5-v3.5.6-1 released
        * Fix startup script 

*Thu Apr  06 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.5.5-1 released
        * Add mutex to PAM (some modules are not thread-safe)

*Tue Apr  04 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.5.4-2 released
        * Fix package for Fedora naming guidelines

*Wed Mar  22 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.5.4-1 released
        * Fix external authentication program 

*Sun Mar  19 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
	* SS5-v3.5.3-2 released
        * Fix package for Fedora naming guidelines

*Thu Mar  09 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
	* SS5-v3.5.3-1 released
        * Add security feature to centralized management

*Thu Mar  09 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.5.2-1 released
        * Fix centralized management

*Thu Mar  09 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.5.1-2 released
        * Strip debug from package

*Thu Mar  09 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.5.1-1 released
        * Add centralized management of the configuration file

*Tue Feb  28 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.4.4-1 released
        * Fix PAM

*Mon Feb  27 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.4.3-2 released
        * Fix package for RH naming guidelines

*Mon Feb  27 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.4.3-1 released
        * Fix package for RH naming guidlines

*Sat Feb  22 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.4r2 released
        * Fix mod_authorization

*Sat Feb  11 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.4r1 released
        * Add environment configuration variables
        * Fix Solaris 10 compatibility with ctime_r() call
        * Fix potential buffer overflow using PAM
        * Code restyling (thx to Walter Franzini)
        * New configure file (thx to Walter Franzini)

*Tue Feb  07 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
	* SS5-v3.3r5 released
        * Fix Solaris 10 compatibility with ctime_r() call
        * Fix netbios default domain

*Mon Feb  06 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.3r4 released
        * Add default netbios domain
	* Fix externalprogram

*Sat Feb  04 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.3r3 released
        * Fix PwdFileCheck
        * Fix ProfileFileCheck

*Wed Jan  25 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.3r2 released
        * Add gid setting with -u option
        * Add configure file

*Mon Jan  20 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.3r1 released
	* Add multiple directory store support
        * Add netbios compatibility in authorization module
        * Add noproxy rule in mod_socks5

*Fri Jan  02 2006 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.2r7 released
        * Add Solaris support

*Thu Dec  22 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.2r6 released
        * Fix module dump
        * Fix module authentication (pam)

*Mon Dec  16 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
	* SS5-v3.2r5 released
        * Fix makefile for gcc old version

*Mon Dec  04 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.2r4 released
        * Fix upstream
        * Fix post authorization
        * Fix proxy hash
        * Fix route hash

*Mon Nov  28 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.2r3 released
        * Fix mod bandwidth
        * Fix mod statistics
        * Fix man
        * Fix route
        * Add auto-refresh web console

*Wed Nov  23 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.2r2 released
        * Fix mod statistics
        * Fix mod balance

*Sun Nov  06 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.2r1 released
        * Add authorization cache
        * New load configuration mechanism
        * New log format
        * Add statistic features
        * Add epoll support

*Mon Nov  01 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.1r1 released
        * Add new dump module

*Mon Oct  27 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.0r10 released
        * Add log details
        * Fix log string
        * Fix recv call

*Mon Aug  22 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
	* SS5-v3.0r9 released
        * Fix SS5_AUTHCACHEAGE option

*Thu Aug  18 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.0r8 released
        * Fix SS5_VERBOSE option

*Mon Aug  08 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.0r7 released
        * Add log detail

*Sun Aug  07 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.0r6 released
        * Increase authorization buffer

*Thu May  10 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.0r5 released
	* Fix connect response using dns
        * Increase authentication buffer
	* Fix profiling bug
        * Modify package structure

*Thu Apr  10 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.0r4 released
        * Added comment into group file
	
*Thu Mar  10 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.0r3 released
        * Pam module fix

*Thu Mar  09 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.0r2 released
        * Pam module fix

*Thu Mar  01 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v3.0r1 released

*Thu Feb  07 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v2.4r10 released
        * SIGPIPE signal fix

*Thu Jan  12 2005 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v2.4r9 released
        * Change facility log
        * Case insensitive in file profiling
        * Buffer overflow fix

*Thu Jul  03 2004 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v2.4r8 released
        * Fix bug closing logfile

*Thu Jan  28 2004 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v2.4r7 released
        * Fix socks5 method

*Thu Jan  09 2004 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v2.4r6 released
        * Fix acl bug
        * Fix bad file descriptor in threaded mode
        * Log format restyling
        * Add -m option, to disable log
        * Add -c option, to check configuration file

*Thu Dec  30 2003 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v2.4r5 released
        * Fix Solaris documentation
	* Fix admin access check
        * Add statistics information

*Thu Dec  24 2003 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v2.4r4 released
        * Fix udp bind interface close to client

*Thu Dec  15 2003 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v2.4r3 released
        * Fix signal set on Solaris system

*Thu Nov  15 2003 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v2.4r2 released
        * Fix some potential buffer overflow 
	* Fix udp bind problem

*Thu Oct  29 2003 Matteo Ricchetti <matteo.ricchetti@libero.it>
	* SS5-v2.4r1 released
        * Add session affinity in balanced connections
        * Add socks statistics about connections
        * Add fake authentication
        * Add web support for virtual connections, session affinity and statistics
        * Add more detail on log messages
        * Fix source-if feature for connect operation
        * Fix access list bugs

*Thu Oct  21 2003 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v2.3r5 released
        * Fix access list bug

*Thu Oct  20 2003 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v2.3r4 released
        * Fix access list bug

*Thu Oct  11 2003 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v2.3r3 released
        * Fix crash for connections reset by peer

*Thu Sep  12  2003 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v2.3r2 released
        * Fix acl problem

*Thu Aug  26  2003 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * SS5-v2.3r1 released
        * Add source-if feature for connect operation
        * Add better control in ldap base configuration
	* Add better detail on log messages
	* Threads creation improvement
        * Fix automatic configuration reload (every 30 seconds)

*Thu Aug  14  2003 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * ss5-v2.2r1 released
        * Add ldap profile feature
        * Add PAM authentication
        * Add username for ss5 execution
	* Add server balancing feature !!!
        * Add ssl fixup
        * Add pop3 fixup
        * Add imap fixup
        * Fix case insensitive username check
        * Fix -b option

*Mon Jul  27  2003 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * ss5-v2.1r1 released
        * Add group profile feature
        * Add bandwidth control
        * Fix some potential buffer overflow 
        * Fix dns ordering problem

*Mon Jun  24  2003 Matteo Ricchetti <matteo.ricchetti@libero.it>
        * ss5-v2.0r1 released
        * Add thread support
        * Add bind port to -b option (-b ip:port)
        * Remove -f option for foreground execution
        * Fix access control list problem
        * Fix some potential buffer overflow 


