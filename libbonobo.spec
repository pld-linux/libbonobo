Summary:	Library for compound documents in GNOME
Summary(pl):	Biblioteka do ³±czenia dokumentów w GNOME
Summary(pt_BR):	Biblioteca para documentos compostos no GNOME
Name:		libbonobo
Version:	2.8.1
Release:	2
License:	GPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/2.8/%{name}-%{version}.tar.bz2
# Source0-md5:	54f863c20016cf8a2cf25056f6c7cda7
URL:		http://www.gnome.org/
BuildRequires:	ORBit2-devel >= 1:2.12.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.4.1
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gtk-doc >= 1.1
BuildRequires:	intltool >= 0.29
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.4.20
BuildRequires:	perl-base
BuildRequires:	popt-devel >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.197
Requires(post):	/sbin/ldconfig
Requires:	ORBit2 >= 1:2.12.0
Provides:	bonobo-activation = %{version}
Obsoletes:	bonobo-activation
Obsoletes:	libbonobo0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libbonobo is a library that provides the necessary framework for
GNOME2 applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

%description -l pl
libbonobo jest bibliotek± daj±c± aplikacjom GNOME2 szkielet
pozwalaj±cy im pracowaæ ze z³o¿onymi dokumentami. Dziêki niemu mo¿na
np. osadziæ arkusz kalkulacyjny i grafikê w dokumencie edytora tekstu.

%description -l pt_BR
libbonobo é uma biblioteca que fornece uma camada necessária para os
aplicativos do GNOME2 funcionarem com documentos compostos, por
exemplo planilhas de cálculo e gráficos juntos num documento texto.

%package devel
Summary:	Include files for the libbonobo document model
Summary(pl):	Pliki nag³ówkowe biblioteki libbonobo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ORBit2-devel >= 1:2.12.0
Requires:	gtk-doc-common
Provides:	bonobo-activation-devel = %{version}
Obsoletes:	bonobo-activation-devel
Obsoletes:	libbonobo0-devel

%description devel
This package provides the necessary include files to allow you to
develop programs using the libbonobo document model.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe potrzebne do tworzenia programów
korzystaj±cych z modelu dokumentów libbonobo.

%package static
Summary:	Static libbonobo libraries
Summary(pl):	Biblioteki statyczne libbonobo
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	bonobo-activation-static = %{version}
Obsoletes:	bonobo-activation-static

%description static
Static libbonobo libraries.

%description static -l pl
Biblioteki statyczne libbonobo.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no static orbit or bonobo modules and *.la for them
rm -f $RPM_BUILD_ROOT%{_libdir}/{bonobo/monikers,orbit-2.0}/*.{la,a}
#Seems to be only test tool during build
rm -f $RPM_BUILD_ROOT%{_bindir}/bonobo-activation-run-query

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
for item in /usr/lib/bonobo/servers /usr/X11R6/lib/bonobo/servers; do
	/usr/sbin/bonobo-activation-sysconf --add-directory=$item
done

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%config(noreplace) %{_sysconfdir}/bonobo-activation/bonobo-activation-config.xml
%doc AUTHORS NEWS README changes.txt
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
%{_gtkdocdir}/%{name}
%{_gtkdocdir}/bonobo-activation

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
