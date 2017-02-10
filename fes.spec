# http://trac.sagemath.org/sage_trac/ticket/13162

Name:		fes
Version:	0.1
Release:	10%{?dist}
License:	GPLv3+
Group:		Applications/Engineering
Summary:	Fast Exhaustive Search
URL:		http://www.lifl.fr/~bouillag
Source0:	http://www.lifl.fr/~bouillag/download/fes-0.1.spkg
ExclusiveArch:	x86_64
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	python2
BuildRequires:	tetex
BuildRequires:	texlive-collection-science
Patch0:		%{name}-dynamic.patch

%description
This external library implements an efficient implement of exhaustive
search to solve systems of low-degree boolean equations. Exhaustive
search is asymptotically faster than computing a Groebner basis,
except in special cases. This particular implementation is
particularly efficient (in the good cases it tests 3 candidate
solutions per CPU cycle on each core).

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
This package contains the header files and development documentation
for %{name}.

%prep
%setup -q
%patch0 -p1

pushd src
    autoreconf -ifs
popd

%build
pushd src
    export CCASFLAGS="%{optflags} -Wa,--noexecstack"
    %configure --disable-static --enable-dynamic
    make %{?_smp_mflags}
    pushd doc
	pdflatex doc.tex
    popd
popd

%install
make install DESTDIR=%{buildroot} -C src
rm %{buildroot}%{_libdir}/libfes.la

%check
pushd src
    chmod +x test/test_suite.py
    make check
%if 0%{?fedora} > 18
    cat test/test_suite.py.log
%endif
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc src/AUTHORS
%doc src/COPYING
%{_libdir}/libfes.so.*

%files		devel
%doc src/TODO
%doc src/doc/doc.pdf
%{_includedir}/fes_interface.h
%{_libdir}/libfes.so

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun  8 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.1-4
- Add ldconfig to post and postun (#914936#c5).
- Mark stack as not executable in .s to .o compilation (#914936#c5).

* Fri Jun  7 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.1-3
- Add missing autoconf, automake and libtool build requires (#914936#c3).
- Remove the with_doc macro (#914936#c3).
- Change package to be x86_64 specific, as sse2 is not optional.

* Wed Jun  5 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.1-2
- Make python2 a build requires (#914936#c1).
- Patch the package to generate a dynamic library (#914936#c1).
- Add AUTHORS, COPYING and TODO to package documentation (#914936#c1).

* Fri Feb 22 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.1-1
- Initial fes spec.
