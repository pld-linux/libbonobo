Summary:	Library for compound documents in GNOME
Summary(pt_BR):	Biblioteca para documentos compostos no GNOME
Name:		libbonobo
Version:	1.109.0
Release:	1
License:	GPL
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Source0:	ftp://ftp.gnome.org/pub/GNOME/pre-gnome2/sources/%{name}/%{name}-%{version}.tar.bz2
URL:		http://www.gnome.org/
BuildRequires:	bonobo-activation-devel
BuildRequires:	ORBit2-devel
BuildRequires:	glib2-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/X11/GNOME2
%define		_prefix		/usr/X11R6

%description
libbonobo is a library that provides the necessary framework for GNOME2
applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

%description -l es
libbonobo is a library that provides the necessary framework for GNOME2
applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

%description -l pl
libbonobo jest bibliotek± daj±c± aplikacjom GNOME2 szkielet pozwalaj±cy im
pracowaÊ ze z≥oøonymi dokumentami. DziÍki niemu moøna np. osadziÊ
arkusz kalkulacyjny i grafikÍ w dokumencie edytora tekstu.

%description -l pt_BR
libbonobo È uma biblioteca que fornece uma camada necess·ria para os
aplicativos do GNOME2 funcionarem com documentos compostos, por exemplo
planilhas de c·lculo e gr·ficos juntos num documento texto.

%package devel
Summary:	Libraries and include files for the libbonobo document model
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	%{name} = %{version}
Requires:	bonobo-activation-devel

%description devel
This package provides the necessary development libraries and include
files to allow you to develop programs using the libbonobo document
model.

%package static
Summary:	Static libbonobo libraries
Summary(pl):	Biblioteki statyczne libbonobo
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	%{name}-devel = %{version}

%description static
Static libbonobo libraries.

%description -l pl static
Biblioteki statyczne libbonobo.

%prep
%setup  -q

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
%{_datadir}/idl/bonobo-*

%files devel
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_libdir}/lib*.??
%{_pkgconfigdir}/*.pc
%{_includedir}/libbonobo-*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_libdir}/bonobo/monikers/lib*.a
