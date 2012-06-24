Summary:	Neighbor Discovery tools for IPv6
Summary(pl):	Narz�dzia do rozpoznawania s�siad�w dla IPv6
Name:		ndisc6
Version:	0.4.1
Release:	1
License:	GPL v2
Group:		Networking/Admin
Source0:	http://people.via.ecp.fr/~rem/ndisc6/%{name}-%{version}.tar.bz2
# Source0-md5:	7dad76e8ade1c0d233ca2f4b4cb93be5
URL:		http://people.via.ecp.fr/~rem/ndisc6/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ndisc6 consists of two small command line tools (ndisc6 and rdisc6)
that perform ICMPv6 Neighbor Discovery and ICMPv6 Router Discovery
respectively. It is primarily meant for IPv6 networking diagnostics or
to detect rogue IPv6 nodes or routers on an Ethernet segment.

%description -l pl
ndisc6 zawiera dwa ma�e narz�dzia dzia�aj�ce z linii polece� (ndisc6 i
rdisc6) wykonuj�ce odpowiednio ICMPv6 Neighbor Discovery
(rozpoznawanie s�siad�w) i ICMPv6 Router Discovery (rozpoznawanie
router�w). S� przeznaczone g��wnie do diagnostyki sieci IPv6 oraz
wykrywania bezprawnych w�z��w lub router�w IPv6 w segmencie sieci
Ethernet.

%prep
%setup -q

%build
%{__make} ndisc6 rdisc6 \
	CC=%{__cc} \
	CFLAGS="%{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}

install ndisc6 rdisc6 $RPM_BUILD_ROOT%{_sbindir}
install ndisc6.8 rdisc6.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
