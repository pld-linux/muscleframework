Summary:	MuscleCard PKCS#11 Framework
Summary(pl.UTF-8):	Szkielet MuscleCard PKCS#11
Name:		muscleframework
Version:	1.1.7
Release:	1
Epoch:		1
License:	BSD
Group:		Applications
#Source0Download: https://alioth.debian.org/frs/?group_id=30111
Source0:	https://alioth.debian.org/frs/download.php/3056/%{name}-%{version}.tar.gz
# Source0-md5:	5dcce65c60d35d9dfa9e10cc7ce7f72e
#Patch0:		%{name}-qt3.patch
Patch0:		%{name}-cryptoflex.patch
Patch1:		%{name}-pcsc.patch
Patch2:		%{name}-openssl.patch
URL:		http://www.musclecard.com/musclecard/index.html
BuildRequires:	libmusclecard-devel
BuildRequires:	openssl-devel >= 1.0.0
BuildRequires:	pam-devel
BuildRequires:	pcsc-lite-devel >= 1.1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MuscleCard PKCS#11 Framework.

%description -l pl.UTF-8
Szkielet MuscleCard PKCS#11.

%package -n pcsc-service-cryptoflex
Summary:	MuscleCard Cryptoflex Plugin
Summary(pl.UTF-8):	Wtyczka MuscleCard Cryptoflex
Group:		Libraries
Requires:	pcsc-lite

%description -n pcsc-service-cryptoflex
MuscleCard Cryptoflex Plugin.

%description -n pcsc-service-cryptoflex -l pl.UTF-8
Wtyczka MuscleCard Cryptoflex.

%package -n pcsc-service-musclecard
Summary:	MuscleCard Applet Plugin
Summary(pl.UTF-8):	Wtyczka MuscleCard Applet
Group:		Libraries
Requires:	pcsc-lite

%description -n pcsc-service-musclecard
MuscleCard Applet Plugin.

%description -n pcsc-service-musclecard -l pl.UTF-8
Wtyczka MuscleCard Applet.

%package -n pam-pam_musclecard
Summary:	PAM module for MuscleCard Framework
Summary(pl.UTF-8):	Moduł PAM dla szkieletu MuscleCard
Group:		Applications/System
Requires:	pam
Requires:	pcsc-lite
Obsoletes:	pam_musclecard

%description -n pam-pam_musclecard
PAM module for MuscleCard Framework.

%description -n pam-pam_musclecard -l pl.UTF-8
Moduł PAM dla szkieletu MuscleCard.

%package pkcs11
Summary:	PKCS#11 library
Summary(pl.UTF-8):	Biblioteka PKCS#11
Group:		Libraries

%description pkcs11
PKCS#11 library.

%description pkcs11 -l pl.UTF-8
Biblioteka PKCS#11.

%package pkcs11-devel
Summary:	PKCS#11 library header files
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki PKCS#11
Group:		Development/Libraries
Requires:	%{name}-pkcs11 = %{version}-%{release}
Requires:	libmusclecard-devel
Requires:	pcsc-lite-devel

%description pkcs11-devel
PKCS#11 library header files.

%description pkcs11-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki PKCS#11.

%package pkcs11-static
Summary:	PKCS#11 static library
Summary(pl.UTF-8):	Statyczna biblioteka PKCS#11
Group:		Development/Libraries
Requires:	%{name}-pkcs11-devel = %{version}-%{release}

%description pkcs11-static
PKCS#11 static library.

%description pkcs11-static -l pl.UTF-8
Statyczna biblioteka PKCS#11.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

ln README README.muscleframework
find CFlexPlugin/src/slbCryptoflex.bundle -name '*.orig' | xargs %{__rm}

%build
cd CFlexPlugin
%configure
%{__make}

cd ../MCardPlugin
%configure
%{__make}

cd ../MusclePAM
%{__make} \
	CC="%{__cc} %{rpmcflags} -fPIC"

cd ../libmusclepkcs11
%configure \
	--includedir=%{_includedir}/libmusclepkcs11
%{__make}

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

%{__make} -C libmusclepkcs11 install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	pkcs11 -p /sbin/ldconfig
%postun	pkcs11 -p /sbin/ldconfig

%files -n pcsc-service-cryptoflex
%defattr(644,root,root,755)
%doc CFlexPlugin/{AUTHORS,COPYING,ChangeLog,ChangeLog.svn,NEWS,README} README.muscleframework
%dir %{_libdir}/pcsc/services/slbCryptoflex.bundle
%dir %{_libdir}/pcsc/services/slbCryptoflex.bundle/Contents
%{_libdir}/pcsc/services/slbCryptoflex.bundle/Contents/Info.plist
%attr(755,root,root) %{_libdir}/pcsc/services/slbCryptoflex.bundle/Contents/Linux
%{_libdir}/pcsc/services/slbCryptoflex.bundle/Contents/PkgInfo
%{_libdir}/pcsc/services/slbCryptoflex.bundle/Contents/Resources

%files -n pcsc-service-musclecard
%defattr(644,root,root,755)
%doc MCardPlugin/{AUTHORS,COPYING,ChangeLog,ChangeLog.svn,NEWS,README} README.muscleframework
%dir %{_libdir}/pcsc/services/mscMuscleCard.bundle
%dir %{_libdir}/pcsc/services/mscMuscleCard.bundle/Contents
%{_libdir}/pcsc/services/mscMuscleCard.bundle/Contents/Info.plist
%attr(755,root,root) %{_libdir}/pcsc/services/mscMuscleCard.bundle/Contents/Linux
%{_libdir}/pcsc/services/mscMuscleCard.bundle/Contents/PkgInfo
%{_libdir}/pcsc/services/mscMuscleCard.bundle/Contents/Resources

%files -n pam-pam_musclecard
%defattr(644,root,root,755)
%doc MusclePAM/{COPYING,ChangeLog.svn,README} README.muscleframework
%attr(755,root,root) /%{_lib}/security/pam_musclecard.so
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pam-muscle.conf

%files pkcs11
%defattr(644,root,root,755)
%doc libmusclepkcs11/{AUTHORS,COPYING,ChangeLog,ChangeLog.svn,NEWS,README} README.muscleframework
%attr(755,root,root) %{_libdir}/libmusclepkcs11.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmusclepkcs11.so.0

%files pkcs11-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmusclepkcs11.so
%{_libdir}/libmusclepkcs11.la
%{_includedir}/libmusclepkcs11

%files pkcs11-static
%defattr(644,root,root,755)
%{_libdir}/libmusclepkcs11.a
