#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	Library for compound documents in GNOME
Summary(pl.UTF-8):	Biblioteka do łączenia dokumentów w GNOME
Summary(pt_BR.UTF-8):	Biblioteca para documentos compostos no GNOME
Name:		libbonobo
Version:	2.32.1
Release:	11
License:	LGPL v2+ (libraries), GPL v2+ (programs)
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libbonobo/2.32/%{name}-%{version}.tar.bz2
# Source0-md5:	27fa902d4fdf6762ee010e7053aaf77b
Patch0:		%{name}-glib.patch
Patch1:		am.patch
URL:		http://www.gnome.org/
BuildRequires:	ORBit2-devel >= 1:2.14.19-10
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	bison
BuildRequires:	docbook-dtd412-xml
BuildRequires:	flex
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.5
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	sed >= 4.0
Requires:	ORBit2 >= 1:2.14.8
Requires:	glib2 >= 1:2.26.0
Requires:	libxml2 >= 1:2.6.31
Requires:	popt >= 1.5
Provides:	bonobo-activation = %{version}
Obsoletes:	bonobo-activation < 2.2.5
Obsoletes:	libbonobo0
Obsoletes:	libbonobo-libs < 2.32.1-8
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
Requires:	ORBit2-devel >= 1:2.14.8
Requires:	glib2-devel >= 1:2.26.0
Requires:	popt-devel >= 1.5
Provides:	bonobo-activation-devel = %{version}
Obsoletes:	bonobo-activation-devel < 2.2.5
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
Obsoletes:	bonobo-activation-static < 2.2.5

%description static
Static libbonobo libraries.

%description static -l pl.UTF-8
Biblioteki statyczne libbonobo.

%package apidocs
Summary:	libbonobo API documentation
Summary(pl.UTF-8):	Dokumentacja API libbonobo
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
libbonobo API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libbonobo.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%{__sed} -i -e 's|/lib|/%{_lib}|g' utils/bonobo-slay.in

# gtk-doc doesn't accept legacy encodings
for f in bonobo/bonobo-storage-memory.c bonobo/bonobo-storage-memory.h \
	bonobo/bonobo-generic-factory.c bonobo/bonobo-generic-factory.h \
	bonobo/bonobo-persist-client.c bonobo/bonobo-persist-client.h ; do
    iconv -f ISO-8859-1 -t UTF-8 -o "${f}.tmp" "$f"
    %{__mv} "${f}.tmp" "$f"
done

%build
%{__autopoint}
%{__gtkdocize}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}

# build seems racy
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no static orbit or bonobo modules and *.la for them;
# libraries *.la obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{bonobo/monikers,orbit-2.0}/*.la \
	$RPM_BUILD_ROOT%{_libdir}/lib*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{bonobo/monikers,orbit-2.0}/*.a
%endif
# Seems to be only test tool during build
%{__rm} $RPM_BUILD_ROOT%{_bindir}/bonobo-activation-run-query

%find_lang %{name}-2.0

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_sbindir}/bonobo-activation-sysconf --add-directory=%{_libdir}/bonobo/servers

%postun -p /sbin/ldconfig

%files -f %{name}-2.0.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO changes.txt
%attr(755,root,root) %{_bindir}/activation-client
%attr(755,root,root) %{_bindir}/bonobo-slay
%attr(755,root,root) %{_bindir}/echo-client-2
%attr(755,root,root) %{_sbindir}/bonobo-activation-sysconf
%attr(755,root,root) %{_libexecdir}/bonobo-activation-server
%attr(755,root,root) %{_libdir}/libbonobo-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbonobo-2.so.0
%attr(755,root,root) %{_libdir}/libbonobo-activation.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbonobo-activation.so.4
%dir %{_libdir}/bonobo-2.0
%dir %{_libdir}/bonobo-2.0/samples
%attr(755,root,root) %{_libdir}/bonobo-2.0/samples/bonobo-echo-2
%dir %{_libdir}/bonobo
%dir %{_libdir}/bonobo/monikers
%attr(755,root,root) %{_libdir}/bonobo/monikers/libmoniker_std_2.so
%dir %{_libdir}/bonobo/servers
%{_libdir}/bonobo/servers/Bonobo_CosNaming_NamingContext.server
%{_libdir}/bonobo/servers/Bonobo_Moniker_std.server
%{_libdir}/bonobo/servers/Bonobo_Sample_Echo.server
%attr(755,root,root) %{_libdir}/orbit-2.0/Bonobo_module.so
%{_datadir}/idl/bonobo-2.0
%{_datadir}/idl/bonobo-activation-2.0
%dir %{_sysconfdir}/bonobo-activation
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bonobo-activation/bonobo-activation-config.xml
%{_mandir}/man1/bonobo-activation-server.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbonobo-2.so
%attr(755,root,root) %{_libdir}/libbonobo-activation.so
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
%{_gtkdocdir}/bonobo-activation
%{_gtkdocdir}/libbonobo
