Summary:	Library for compound documents in GNOME
Summary(pl):	Biblioteka do ³±czenia dokumentów w GNOME
Summary(pt_BR):	Biblioteca para documentos compostos no GNOME
Name:		libbonobo
Version:	1.116.0
Release:	1
License:	GPL
Group:		X11/Libraries
Source0:	ftp://ftp.gnome.org/pub/gnome/pre-gnome2/sources/%{name}/%{name}-%{version}.tar.bz2
URL:		http://www.gnome.org/
BuildRequires:	bonobo-activation-devel >= 0.9.8
BuildRequires:	ORBit2-devel
BuildRequires:	glib2-devel >= 2.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/X11/GNOME2
%define		_prefix		/usr/X11R6

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
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}
Requires:	bonobo-activation-devel

%description devel
This package provides the necessary include files to allow you to
develop programs using the libbonobo document model.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe potrzebne do tworzenia programów
korzystaj±cych z modelu dokumentów libbonobo.

%package static
Summary:	Static libbonobo libraries
Summary(pl):	Biblioteki statyczne libbonobo
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static libbonobo libraries.

%description static -l pl
Biblioteki statyczne libbonobo.

%prep
%setup -q

%build
%configure \
	--enable-gtk-doc=no

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

gzip -9nf AUTHORS ChangeLog NEWS README

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_libdir}/bonobo/servers
%dir %{_libdir}/bonobo/monikers
%attr(755,root,root) %{_libdir}/bonobo-*
%attr(755,root,root) %{_libdir}/bonobo/monikers/lib*.??
%dir %{_libdir}/orbit-2.0
%attr(755,root,root) %{_libdir}/orbit-2.0/*.??
%{_datadir}/idl/bonobo-*

%files devel
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_libdir}/lib*.??
%{_pkgconfigdir}/*.pc
%{_includedir}/libbonobo-*
%{_datadir}/gtk-doc/html/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_libdir}/bonobo/monikers/lib*.a
%{_libdir}/orbit-2.0/*.a
