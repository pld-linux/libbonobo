#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Library for compound documents in GNOME
Summary(pl.UTF-8):	Biblioteka do łączenia dokumentów w GNOME
Summary(pt_BR.UTF-8):	Biblioteca para documentos compostos no GNOME
Name:		libbonobo
Version:	2.32.0
Release:	2
License:	GPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libbonobo/2.32/%{name}-%{version}.tar.bz2
# Source0-md5:	bc2b25b03ca57866a61e04852f2f53fd
URL:		http://www.gnome.org/
BuildRequires:	ORBit2-devel >= 1:2.14.8
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	bison
BuildRequires:	dbus-glib-devel
BuildRequires:	docbook-dtd412-xml
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{version}-%{release}
Provides:	bonobo-activation = %{version}
Obsoletes:	bonobo-activation
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
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

%package libs
Summary:	libbonobo library itself
Summary(pl.UTF-8):	Sama biblioteka libbonobo
Group:		Libraries
Requires(post):	/sbin/ldconfig
Requires:	ORBit2 >= 1:2.14.8
Obsoletes:	libbonobo0

%description libs
libbonobo library itself.

%description libs -l pl.UTF-8
Sama biblioteka libbonobo.

%package devel
Summary:	Include files for the libbonobo document model
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbonobo
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	ORBit2-devel >= 1:2.14.8
Requires:	glib2-devel >= 1:2.26.0
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
%{__sed} -i -e 's/^en@shaw//' po/LINGUAS
rm -f po/en@shaw.po

%build
%{__gtkdocize}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
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
# Seems to be only test tool during build
rm -f $RPM_BUILD_ROOT%{_bindir}/bonobo-activation-run-query


%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/bonobo-activation-sysconf --add-directory=%{_libdir}/bonobo/servers

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README changes.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bonobo-activation/bonobo-activation-config.xml
%attr(755,root,root) %{_bindir}/activation-client
%attr(755,root,root) %{_bindir}/bonobo-slay
%attr(755,root,root) %{_bindir}/echo-client-2
%attr(755,root,root) %{_sbindir}/bonobo-activation-sysconf
%dir %{_sysconfdir}/bonobo-activation
%{_datadir}/idl/bonobo-*
%{_mandir}/man1/*.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbonobo-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbonobo-2.so.0
%attr(755,root,root) %{_libdir}/libbonobo-activation.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbonobo-activation.so.4
%attr(755,root,root) %{_libdir}/bonobo-*
%attr(755,root,root) %{_libdir}/bonobo/monikers/lib*.so
%attr(755,root,root) %{_libdir}/orbit-2.0/*.so
%dir %{_libdir}/bonobo
%dir %{_libdir}/bonobo/monikers
%dir %{_libdir}/bonobo/servers
%{_libdir}/bonobo/servers/*.server

%files devel
%defattr(644,root,root,755)
%doc ChangeLog TODO
%attr(755,root,root) %{_libdir}/libbonobo-2.so
%attr(755,root,root) %{_libdir}/libbonobo-activation.so
%{_libdir}/libbonobo-2.la
%{_libdir}/libbonobo-activation.la
%{_includedir}/libbonobo-2.0
%{_includedir}/bonobo-activation-2.0
%{_pkgconfigdir}/bonobo-activation-2.0.pc
%{_pkgconfigdir}/libbonobo-2.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbonobo-2.a
%{_libdir}/libbonobo-activation.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}
%{_gtkdocdir}/bonobo-activation
