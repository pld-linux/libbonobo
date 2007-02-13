#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Library for compound documents in GNOME
Summary(pl.UTF-8):	Biblioteka do łączenia dokumentów w GNOME
Summary(pt_BR.UTF-8):	Biblioteca para documentos compostos no GNOME
Name:		libbonobo
Version:	2.16.0
Release:	2
License:	GPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/libbonobo/2.16/%{name}-%{version}.tar.bz2
# Source0-md5:	30cdcf2b5316888f10fea6362b38499c
URL:		http://www.gnome.org/
BuildRequires:	ORBit2-devel >= 1:2.14.3
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.12.3
BuildRequires:	gnome-common >= 2.12.0
BuildRequires:	gtk-doc >= 1.7
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.26
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.197
Requires:	ORBit2 >= 1:2.14.3
Provides:	bonobo-activation = %{version}
Obsoletes:	bonobo-activation
Obsoletes:	libbonobo0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libbonobo is a library that provides the necessary framework for
GNOME2 applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

%description -l pl.UTF-8
libbonobo jest biblioteką dającą aplikacjom GNOME2 szkielet
pozwalający im pracować ze złożonymi dokumentami. Dzięki niemu można
np. osadzić arkusz kalkulacyjny i grafikę w dokumencie edytora tekstu.

%description -l pt_BR.UTF-8
libbonobo é uma biblioteca que fornece uma camada necessária para os
aplicativos do GNOME2 funcionarem com documentos compostos, por
exemplo planilhas de cálculo e gráficos juntos num documento texto.

%package devel
Summary:	Include files for the libbonobo document model
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbonobo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ORBit2-devel >= 1:2.14.3
Requires:	popt-devel >= 1.5
Provides:	bonobo-activation-devel = %{version}
Obsoletes:	bonobo-activation-devel
Obsoletes:	libbonobo0-devel

%description devel
This package provides the necessary include files to allow you to
develop programs using the libbonobo document model.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów
korzystających z modelu dokumentów libbonobo.

%package static
Summary:	Static libbonobo libraries
Summary(pl.UTF-8):	Biblioteki statyczne libbonobo
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	bonobo-activation-static = %{version}
Obsoletes:	bonobo-activation-static

%description static
Static libbonobo libraries.

%description static -l pl.UTF-8
Biblioteki statyczne libbonobo.

%package apidocs
Summary:	libbonobo API documentation
Summary(pl.UTF-8):	Dokumentacja API libbonobo
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libbonobo API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libbonobo.

%prep
%setup -q
sed -i -e 's|/lib|/%{_lib}|g' utils/bonobo-slay.in

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	%{!?with_static_libs:--disable-static}
%{__make}


%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no static orbit or bonobo modules and *.la for them
rm -f $RPM_BUILD_ROOT%{_libdir}/{bonobo/monikers,orbit-2.0}/*.{la,a}
#Seems to be only test tool during build
rm -f $RPM_BUILD_ROOT%{_bindir}/bonobo-activation-run-query


%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/usr/sbin/bonobo-activation-sysconf --add-directory=/usr/lib/bonobo/servers

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README changes.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bonobo-activation/bonobo-activation-config.xml
%attr(755,root,root) %{_bindir}/activation-client
%attr(755,root,root) %{_bindir}/bonobo-slay
%attr(755,root,root) %{_bindir}/echo-client-2
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/bonobo-*
%attr(755,root,root) %{_libdir}/bonobo/monikers/lib*.so
%attr(755,root,root) %{_libdir}/orbit-2.0/*.so
%dir %{_sysconfdir}/bonobo-activation
%dir %{_libdir}/bonobo
%dir %{_libdir}/bonobo/monikers
%dir %{_libdir}/bonobo/servers
%{_libdir}/bonobo/servers/*
%{_datadir}/idl/bonobo-*
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%doc ChangeLog TODO
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/libbonobo-*
%{_includedir}/bonobo-activation-2.0
%{_pkgconfigdir}/*.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}
%{_gtkdocdir}/bonobo-activation
