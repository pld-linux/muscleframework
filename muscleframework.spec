Summary:	MuscleCard PKCS#11 Framework
Summary(pl):	Szkielet MuscleCard PKCS#11
Name:		muscleframework
Version:	1.1.3
Release:	2
Epoch:		1
License:	BSD
Group:		Applications
Source0:	http://www.musclecard.com/musclecard/files/%{name}-%{version}.tar.gz
# Source0-md5:	def0af167d56e3c6181edb626e6e34d7
Patch0:		%{name}-qt3.patch
Patch1:		%{name}-cryptoflex.patch
URL:		http://www.musclecard.com/musclecard/index.html
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pam-devel
BuildRequires:	pcsc-lite-devel >= 1.1.1
BuildRequires:	qt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MuscleCard PKCS#11 Framework.

%description -l pl
Szkielet MuscleCard PKCS#11.

%package -n pcsc-service-cryptoflex
Summary:	MuscleCard Cryptoflex Plugin
Summary(pl):	Wtyczka MuscleCard Cryptoflex
Group:		Libraries
Requires:	pcsc-lite

%description -n pcsc-service-cryptoflex
MuscleCard Cryptoflex Plugin.

%description -n pcsc-service-cryptoflex -l pl
Wtyczka MuscleCard Cryptoflex.

%package -n pcsc-service-musclecard
Summary:	MuscleCard Applet Plugin
Summary(pl):	Wtyczka MuscleCard Applet
Group:		Libraries
Requires:	pcsc-lite

%description -n pcsc-service-musclecard
MuscleCard Applet Plugin.

%description -n pcsc-service-musclecard -l pl
Wtyczka MuscleCard Applet.

%package -n pam-pam_musclecard
Summary:	PAM module for MuscleCard Framework
Summary(pl):	Modu³ PAM dla szkieletu MuscleCard
Group:		Applications/System
Requires:	pam
Requires:	pcsc-lite
Obsoletes:	pam_musclecard

%description -n pam-pam_musclecard
PAM module for MuscleCard Framework.

%description -n pam-pam_musclecard -l pl
Modu³ PAM dla szkieletu MuscleCard.

%package tools
Summary:	MuscleTool - personalization tool for smartcards
Summary(pl):	MuscleTool - narzêdzie do personalizacji kart procesorowych
Group:		Applications
Requires:	pcsc-lite

%description tools
MuscleTool - command line personalization tool for MuscleCard enabled
smartcards.

%description tools -l pl
MuscleTool - dzia³aj±ce z linii poleceñ narzêdzie do personalizacji
kart procesorowych obs³ugiwanych przez ¶rodowisko MuscleCard.

%package pkcs11
Summary:	PKCS#11 library
Summary(pl):	Biblioteka PKCS#11
Group:		Libraries

%description pkcs11
PKCS#11 library.

%description pkcs11 -l pl
Biblioteka PKCS#11.

%package pkcs11-devel
Summary:	PKCS#11 library header files
Summary(pl):	Pliki nag³ówkowe biblioteki PKCS#11
Group:		Development/Libraries
Requires:	%{name}-pkcs11 = %{version}-%{release}

%description pkcs11-devel
PKCS#11 library header files.

%description pkcs11-devel -l pl
Pliki nag³ówkowe biblioteki PKCS#11.

%package pkcs11-static
Summary:	PKCS#11 static library
Summary(pl):	Statyczna biblioteka PKCS#11
Group:		Development/Libraries
Requires:	%{name}-pkcs11-devel = %{version}-%{release}

%description pkcs11-static
PKCS#11 static library.

%description pkcs11-static -l pl
Statyczna biblioteka PKCS#11.

%package xcard
Summary:	XCardII - graphical smartcard administration tool
Summary(pl):	XCardII - graficzne narzêdzie do administrowania kartami procesorowymi
Group:		X11/Applications
Requires:	pcsc-lite

%description xcard
XCardII - graphical smartcard administration tool.

%description xcard -l pl
XCardII - graficzne narzêdzie do administrowania kartami
procesorowymi.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cd CFlexPlugin
%configure2_13
%{__make}

cd ../MCardPlugin
%configure2_13
%{__make}

cd ../MusclePAM
%{__make} \
	CC="%{__cc} %{rpmcflags} -fPIC"

cd ../MuscleTools
%{__make} \
	CC="%{__cc} %{rpmcflags}"

cd ../PKCS11
%configure2_13
%{__make}

cd ../XCardII/src
%{__make} \
	CPP="%{__cxx} %{rpmcflags} -fPIC -Wall -I/usr/X11R6/include/qt" \
	LIBS="-L/usr/X11R6/lib -lqt -lpcsclite -lpthread" \
	MOC=moc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/pcsc/services

cp -rf CFlexPlugin/src/slbCryptoflex.bundle $RPM_BUILD_ROOT%{_libdir}/pcsc/services
install -d $RPM_BUILD_ROOT%{_libdir}/pcsc/services/slbCryptoflex.bundle/Contents/Linux
install CFlexPlugin/src/.libs/libcryptoflex.so \
	$RPM_BUILD_ROOT%{_libdir}/pcsc/services/slbCryptoflex.bundle/Contents/Linux/slbCryptoflex

cp -rf MCardPlugin/src/mscMuscleCard.bundle $RPM_BUILD_ROOT%{_libdir}/pcsc/services
install -d $RPM_BUILD_ROOT%{_libdir}/pcsc/services/mscMuscleCard.bundle/Contents/Linux
install MCardPlugin/src/.libs/libmusclecardApplet.so \
	$RPM_BUILD_ROOT%{_libdir}/pcsc/services/mscMuscleCard.bundle/Contents/Linux/mscMuscleCard

install -d $RPM_BUILD_ROOT{/%{_lib}/security,%{_sysconfdir}}
install MusclePAM/pam_musclecard.so $RPM_BUILD_ROOT/%{_lib}/security
install MusclePAM/pam-muscle.conf $RPM_BUILD_ROOT%{_sysconfdir}

install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
install MuscleTools/muscleTool $RPM_BUILD_ROOT%{_bindir}
install MuscleTools/man/muscleTool.1 $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} -C PKCS11 install \
	DESTDIR=$RPM_BUILD_ROOT

install XCardII/src/xcard $RPM_BUILD_ROOT%{_bindir}
install XCardII/man/xcard.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	pkcs11 -p /sbin/ldconfig
%postun	pkcs11 -p /sbin/ldconfig

%files -n pcsc-service-cryptoflex
%defattr(644,root,root,755)
%doc CFlexPlugin/{AUTHORS,COPYING,ChangeLog,NEWS,README}
%dir %{_libdir}/pcsc/services/slbCryptoflex.bundle
%dir %{_libdir}/pcsc/services/slbCryptoflex.bundle/Contents
%{_libdir}/pcsc/services/slbCryptoflex.bundle/Contents/Info.plist
%attr(755,root,root) %{_libdir}/pcsc/services/slbCryptoflex.bundle/Contents/Linux
%{_libdir}/pcsc/services/slbCryptoflex.bundle/Contents/PkgInfo
%{_libdir}/pcsc/services/slbCryptoflex.bundle/Contents/Resources

%files -n pcsc-service-musclecard
%defattr(644,root,root,755)
%doc MCardPlugin/{AUTHORS,COPYING,ChangeLog,NEWS,README}
%dir %{_libdir}/pcsc/services/mscMuscleCard.bundle
%dir %{_libdir}/pcsc/services/mscMuscleCard.bundle/Contents
%{_libdir}/pcsc/services/mscMuscleCard.bundle/Contents/Info.plist
%attr(755,root,root) %{_libdir}/pcsc/services/mscMuscleCard.bundle/Contents/Linux
%{_libdir}/pcsc/services/mscMuscleCard.bundle/Contents/PkgInfo
%{_libdir}/pcsc/services/mscMuscleCard.bundle/Contents/Resources

%files -n pam-pam_musclecard
%defattr(644,root,root,755)
%doc MusclePAM/{LICENSE,README}
%attr(755,root,root) /%{_lib}/security/pam_musclecard.so
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pam-muscle.conf

%files tools
%defattr(644,root,root,755)
%doc MuscleTools/{COPYING,README}
%attr(755,root,root) %{_bindir}/muscleTool
%{_mandir}/man1/muscleTool.1*

%files pkcs11
%defattr(644,root,root,755)
%doc PKCS11/{AUTHORS,COPYING,ChangeLog,NEWS,README}
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files pkcs11-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h

%files pkcs11-static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files xcard
%defattr(644,root,root,755)
%doc XCardII/{COPYING,README}
%attr(755,root,root) %{_bindir}/xcard
%{_mandir}/man1/xcard.1*
