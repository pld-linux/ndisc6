Summary:	Neighbor Discovery tools for IPv6
Summary(pl.UTF-8):	Narzędzia do rozpoznawania sąsiadów dla IPv6
Name:		ndisc6
Version:	1.0.1
Release:	2
License:	GPL v2
Group:		Networking/Admin
Source0:	http://www.remlab.net/files/ndisc6/%{name}-%{version}.tar.bz2
# Source0-md5:	d0b8233a60e29ad78d9aebb8cef0b3f2
Source1:	rdnssd.init
Source2:	rdnssd.sysconfig
Source3:	rdnssd.upstart
Patch0:		%{name}-no_chown.patch
Patch1:		rdnssd-uid.patch
URL:		http://www.remlab.net/ndisc6/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NDisc6 is a small collection of useful tools for IPv6 networking.
It includes the following programs:
- ndisc6: ICMPv6 Neighbor Discovery tool
- rdisc6: ICMPv6 Router Discovery tool
- tcptraceroute6: lightweight IPv6 tcptraceroute
- traceroute6: IPv6 traceroute

%description -l pl.UTF-8
NDisc6 jest małym zestawem użytecznych narzędzi do dla sieci IPv6.
Zawiera następujące programy:
- ndisc6: narzędzie do wykrywania sąsiednich wezłów za pomocą
  protokołu
  ICMPv6 Neighbor Discovery
- rdisc6: narzędzie do wykrywania routerów za pomocą protokołu
  ICMPv6 Router Discovery
- tcptraceroute6: lekki program do pokazywania trasy pakietów TCP
  w sieciach IPv6
- traceroute6: program do pokazywania trasy pakietów w sieciach IPv6

%package rdnssd
Summary:	Recursive DNS Servers discovery Daemon
Summary(pl.UTF-8):	Demon wykrywający rekursywne serwerów DNS w sieciach IPv6
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts >= 0.4.3.0
Requires:	%{name} = %{version}-%{release}
Provides:	group(rdnssd)
Provides:	user(rdnssd)

%description rdnssd
Recursive DNS Servers discovery Daemon.

%description -l pl.UTF-8 rdnssd
Demon do wykrywania rekursywnych serwerów DNS w sieciach IPv6.

%package rdnssd-upstart
Summary:	Upstart job sescription for rdnssd
Summary(pl.UTF-8):	Opis zadania Upstart dla rdnssd
Group:		Networking/Daemons
Requires:	upstart >= 0.6
Requires:	%{name}-rdnssd = %{version}-%{release}

%description rdnssd-upstart
Upstart job description for the Recursive DNS Servers discovery
Daemon.

%description -l pl.UTF-8 rdnssd-upstart
Opis zadania Upstart dla demona do wykrywania rekursywnych serwerów
DNS w sieciach IPv6.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make} \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,init}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

touch $RPM_BUILD_ROOT/var/run/rdnssd/resolv.conf

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rdnssd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rdnssd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/init/rdnssd.conf

%find_lang %{name}

%pre rdnssd
%groupadd -g 269 rdnssd
%useradd -u 269 -d /usr/share/empty -s /bin/false -c "rdnssd" -g rdnssd rdnssd

%post rdnssd
/sbin/chkconfig --add rdnssd
%service rdnssd restart "RDNSS daemon"

%preun rdnssd
if [ "$1" = "0" ]; then
	%service rdnssd stop
	/sbin/chkconfig --del rdnssd
fi

%postun rdnssd
if [ "$1" = "0" ]; then
        %userremove rdnssd
        %groupremove rdnssd
fi

%post rdnssd-upstart
%upstart_post rdnssd

%postun rdnssd-upstart
%upstart_postun rdnssd

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/dnssort
%attr(755,root,root) %{_bindir}/name2addr
%attr(755,root,root) %ghost %{_bindir}/addr2name
%attr(4754,root,adm) %{_bindir}/ndisc6
%attr(4754,root,adm) %{_bindir}/rdisc6
%attr(4754,root,adm) %{_bindir}/rltraceroute6
%attr(755,root,root) %{_bindir}/tcptraceroute6
%attr(755,root,root) %ghost %{_bindir}/tracert6
%attr(755,root,root) %{_bindir}/tcpspray
%attr(755,root,root) %ghost %{_bindir}/tcpspray6
%attr(755,root,root) %{_sbindir}/rdnssd
%{_mandir}/man1/addr2name.1*
%attr(644,root,root) %ghost %{_mandir}/man1/name2addr.1
%{_mandir}/man1/dnssort.1*
%{_mandir}/man1/tcpspray.1*
%attr(644,root,root) %ghost %{_mandir}/man1/tcpspray6.1
%{_mandir}/man8/ndisc6.8*
%{_mandir}/man8/rdisc6.8*
%{_mandir}/man8/rltraceroute6.8*
%attr(644,root,root) %ghost %{_mandir}/man8/tcptraceroute6.8
%attr(644,root,root) %ghost %{_mandir}/man8/tracert6.8

%files rdnssd
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/rdnssd
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rdnssd
%dir %{_sysconfdir}/rdnssd
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rdnssd/merge-hook
%{_mandir}/man8/rdnssd.8*
%attr(775,root,rdnssd) %dir /var/run/rdnssd
%ghost %attr(644,rdnssd,rdnssd) /var/run/rdnssd/resolv.conf

%files rdnssd-upstart
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/init/rdnssd.conf
