Summary:	Library for compound documents in GNOME
Summary(pl):	Biblioteka do ��czenia dokument�w w GNOME
Summary(pt_BR):	Biblioteca para documentos compostos no GNOME
Name:		libbonobo
Version:	2.3.1
Release:	3
License:	GPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/2.3/%{name}-%{version}.tar.bz2
Patch0:		%{name}-GNOME_COMPILE_WARNINGS.patch
Patch1:		%{name}-destdir.patch
Patch2:		%{name}-locale-sr.patch
URL:		http://www.gnome.org/
BuildRequires:	ORBit2-devel >= 2.7.1
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 2.2.1
BuildRequires:	gtk-doc >= 1.1
BuildRequires:	libtool
BuildRequires:	rpm-build >= 4.1-10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Provides:	bonobo-activation = %{version}
Obsoletes:	libbonobo0
Obsoletes:	bonobo-activation

%description
libbonobo is a library that provides the necessary framework for
GNOME2 applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

%description -l pl
libbonobo jest bibliotek� daj�c� aplikacjom GNOME2 szkielet
pozwalaj�cy im pracowa� ze z�o�onymi dokumentami. Dzi�ki niemu mo�na
np. osadzi� arkusz kalkulacyjny i grafik� w dokumencie edytora tekstu.

%description -l pt_BR
libbonobo � uma biblioteca que fornece uma camada necess�ria para os
aplicativos do GNOME2 funcionarem com documentos compostos, por
exemplo planilhas de c�lculo e gr�ficos juntos num documento texto.

%package devel
Summary:	Include files for the libbonobo document model
Summary(pl):	Pliki nag��wkowe biblioteki libbonobo
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	gtk-doc-common
Provides:	bonobo-activation-devel = %{version}
Obsoletes:	libbonobo0-devel
Obsoletes:	bonobo-activation-devel

%description devel
This package provides the necessary include files to allow you to
develop programs using the libbonobo document model.

%description devel -l pl
Ten pakiet zawiera pliki nag��wkowe potrzebne do tworzenia program�w
korzystaj�cych z modelu dokument�w libbonobo.

%package static
Summary:	Static libbonobo libraries
Summary(pl):	Biblioteki statyczne libbonobo
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}
Provides:	bonobo-activation-static = %{version}
Obsoletes:	bonobo-activation-static

%description static
Static libbonobo libraries.

%description static -l pl
Biblioteki statyczne libbonobo.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

# sr_YU is latin2, sr_YU@cyrillic is cyrillic in glibc
mv -f po/{sr.po,sr@cyrillic.po}
mv -f po/{sr@Latn.po,sr.po}

%build
rm -f missing
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

# no static modules
rm -f $RPM_BUILD_ROOT%{_libdir}/{bonobo/monikers,orbit-2.0}/*.a

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
%{_libdir}/bonobo/monikers/lib*.la
%{_libdir}/bonobo/servers/*
%{_libdir}/orbit-2.0/*.la
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

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
