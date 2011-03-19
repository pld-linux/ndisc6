Summary:	Neighbor Discovery tools for IPv6
Summary(pl.UTF-8):	Narzędzia do rozpoznawania sąsiadów dla IPv6
Name:		ndisc6
Version:	1.0.1
Release:	1
License:	GPL v2
Group:		Networking/Admin
Source0:	http://www.remlab.net/files/ndisc6/%{name}-%{version}.tar.bz2
# Source0-md5:	d0b8233a60e29ad78d9aebb8cef0b3f2
Patch0:		%{name}-no_chown.patch
URL:		http://www.remlab.net/ndisc6/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NDisc6 is a small collection of useful tools for IPv6 networking.
It includes the following programs:
- ndisc6: ICMPv6 Neighbor Discovery tool
- rdisc6: ICMPv6 Router Discovery tool
- tcptraceroute6: lightweight IPv6 tcptraceroute
- traceroute6: IPv6 traceroute
- rdnssd: Recursive DNS Servers discovery Daemon

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
- rdnssd: demon do wykrywania rekursywnych serwerów DNS w sieciach
  IPv6

%prep
%setup -q
%patch0 -p1

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
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%dir %{_sysconfdir}/rdnssd
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rdnssd/merge-hook
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
%{_mandir}/man8/rdnssd.8*
%{_mandir}/man8/rltraceroute6.8*
%attr(644,root,root) %ghost %{_mandir}/man8/tcptraceroute6.8
%attr(644,root,root) %ghost %{_mandir}/man8/tracert6.8
