Name: mpfr
Version: 4.1.0
Release: 1
Summary: A C library for multiple-precision floating-point computations
URL: http://www.mpfr.org/
License: LGPLv3+ and GPLv3+ and GFDL
BuildRequires: autoconf libtool gmp-devel gcc git mpfr
Requires: /sbin/ldconfig
Requires: gmp >= 4.2.3

Source0: http://www.mpfr.org/%{name}-%{version}/%{name}-%{version}.tar.xz

%description
MPFR is a C library for arbitrary-precision binary floating-point computation 
with correct rounding, based on Multi-Precision Library. The computation is 
both efficient and has a well-defined semantics: the functions are completely 
specified on all the possible operands and the results do not depend on the 
platform. This is done by copying the ideas from the ANSI/IEEE-754 standard 
for fixed-precision floating-point arithmetic (correct rounding and exceptions, 
in particular)

%package devel
Summary: Development files for the MPFR library
Requires: %{name} = %{version}-%{release}
Requires: /sbin/install-info
Requires: gmp-devel

%description devel
Devel for %{name}

If you want to develop applications which will use the MPFR library,
you'll need to install the mpfr-devel package. You'll also need to
install the mpfr package.

%prep
%autosetup -p1

%build
%configure --disable-assert --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libmpfr.la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

rm -f $RPM_BUILD_ROOT%{_pkgdocdir}/COPYING  $RPM_BUILD_ROOT%{_pkgdocdir}/COPYING.LESSER
cp -a %{_libdir}/libmpfr.so.4 $RPM_BUILD_ROOT%{_libdir}
cp -a %{_libdir}/libmpfr.so.4.1.6 $RPM_BUILD_ROOT%{_libdir}

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
if [ -f %{_infodir}/mpfr.info.gz ]; then
    /sbin/install-info %{_infodir}/mpfr.info.gz %{_infodir}/dir || :
fi

%preun devel
if [ "$1" = 0 ]; then
    if [ -f %{_infodir}/mpfr.info.gz ]; then
	/sbin/install-info --delete %{_infodir}/mpfr.info.gz %{_infodir}/dir || :
    fi
fi

%files
%license COPYING COPYING.LESSER
%doc NEWS README AUTHORS BUGS TODO doc/FAQ.html
%{_libdir}/libmpfr.so.*

%files devel
%{_pkgdocdir}/examples
%{_libdir}/libmpfr.so
%{_includedir}/*.h
%{_infodir}/mpfr.info*
%{_libdir}/pkgconfig/mpfr.pc

%changelog
* Wed Aug 12 2020 xinghe <xinghe1@huawei.com> - 4.1.0-1
- update to 4.1.0

* Tue Aug 13 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.1.6-3
- Package init
