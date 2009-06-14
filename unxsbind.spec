Summary:	DNS BIND 9 telco quality manager with quality admin and end-user web interfaces. Also rrdtool graphics
Name:		unxsbind
Version:	1.11
Release:	0.1
License:	GPL
Group:		Networking/Admin
Source0:	http://unixservice.com/source/%{name}-%{version}.tar.gz
# Source0-md5:	e6e5e218f4c9449ca2f58fa42a50d638
URL:		http://openisp.net/openisp/unxsBind
Patch0:		%{name}-include.patch
BuildRequires:	mysql-devel
BuildRequires:	ucidr
BuildRequires:	zlib-devel
Requires:	bind >= 9.3.4
Requires:	bind-utils
Requires:	rrdtool
Requires:	unxsadmin >= 1.2

%description
unxsBind iDNS provides a professional DNS BIND 9 manager. For 1 to
1000's of NSs.

Main features supported:

1-. Multiple disjoint NS sets that can share same NS cluster nodes.
2-. Unlimited split horizon views (with no BIND xfer issues.) 3-. Bulk
zone and resource record operations. 4-. Traffic monitoring per zone
or per NS set (per NS or aggregated across cluster) with rrdtool
graphics. 5-. Wizards for CIDR based downstream delegation of arpa
zones. 6-. Hidden masters, external masters, all masters only clusters
(no BIND xfer problems.) 7-. Secondary only zone management for
customers running their own (hidden or public) masters. 8-.
Engineering and development friendly tech web interface backend. 9-.
Organization/Company contact web interface. Allows non skilled zone
owners to modify RRs. 10-. User friendly admin web interface for zone
and customer, contact management authorized users. 11-. Uses
company-contact-role model for allowing management partitioning
perfect for DNS as a service (ASP) deployments. The root ASP manages
the infrastructure, clients that are companies, NGOs or other
organizations have contacts (staff) that can be of diverse permission
levels for operating on their companies zones. 12-. Optional automatic
creation of rev dns PTR records. 13-. Support for upstream delegated
sub class C delegated rev dns zones. 14-. Migration and import tools.
15-. Database can fail and DNS services continue. 16-. Support for
large DKIM and other txt RRs. 17-. DNSSEC and international char
(IDNS) support available soon with just one "yum update unxsbind"
command.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	DESTDIR=$RPM_BUILD_ROOT \
	libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/unxs/cgi-bin

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/idns
install -d $RPM_BUILD_ROOT%{_datadir}/iDNS/data
install -d $RPM_BUILD_ROOT%{_datadir}/iDNS/setup9
install -d $RPM_BUILD_ROOT%{_datadir}/iDNS/admin/templates
install -d $RPM_BUILD_ROOT%{_datadir}/iDNS/org/templates
install -d $RPM_BUILD_ROOT%{_datadir}/unxs/html/{css,images}
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT/var/log/named

cp -u images/* $RPM_BUILD_ROOT%{_datadir}/unxs/html/images/
cp -u interfaces/admin/templates/images/* $RPM_BUILD_ROOT%{_datadir}/unxs/html/images/
cp -u interfaces/admin/templates/css/* $RPM_BUILD_ROOT%{_datadir}/unxs/html/css/
cp `find ./interfaces/admin/templates/ -type f -print` $RPM_BUILD_ROOT%{_datadir}/iDNS/admin/templates/
cp `find ./interfaces/org/templates/ -type f -print` $RPM_BUILD_ROOT%{_datadir}/iDNS/org/templates/
install data/*.txt $RPM_BUILD_ROOT%{_datadir}/iDNS/data/
install setup9/rndc.conf $RPM_BUILD_ROOT%{_sysconfdir}/rndc.conf
install setup9/rndc.key $RPM_BUILD_ROOT%{_sysconfdir}/rndc.key
install setup9/* $RPM_BUILD_ROOT%{_datadir}/iDNS/setup9/
install agents/mysqlcluster/mysqlcluster.sh $RPM_BUILD_ROOT%{_sbindir}
# %{_bindir}/dig @e.root-servers.net . ns > %{_prefix}/local/share/iDNS/setup9/root.cache

for i in admin errorlog org thit
do
%{__make} -C interfaces/$i install \
        DESTDIR=$RPM_BUILD_ROOT \
        libdir=%{_libdir}
done

install interfaces/thit/bind9-genstats.sh $RPM_BUILD_ROOT%{_sbindir}/bind9-genstats.sh

#export ISMROOT=%{_prefix}/local/share
#%{_datadir}/unxs/cgi-bin/iDNS.cgi installbind 127.0.0.1
#chmod -R og+x %{_datadir}/unxs/idns

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE INSTALL
%{_datadir}/iDNS
%dir %attr(740,mysql,mysql) %{_datadir}/iDNS/data
%{_sysconfdir}/rndc.key
%{_sysconfdir}/rndc.conf
%{_datadir}/idns
%dir %{_datadir}/unxs
%{_datadir}/unxs/cgi-bin/iDNS.cgi
%{_datadir}/unxs/cgi-bin/idnsAdmin.cgi
%{_datadir}/unxs/cgi-bin/idnsOrg.cgi
%attr(755,root,root) %{_sbindir}/tHitCollector
%attr(755,root,root) %{_sbindir}/bind9-genstats.sh
%attr(755,root,root) %{_sbindir}/idns-logerror
%{_datadir}/unxs/html/images/green.gif
%{_datadir}/unxs/html/images/red.gif
/var/log/named
%attr(755,root,root) %{_sbindir}/mysqlcluster.sh
