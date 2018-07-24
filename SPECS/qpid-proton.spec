%global proton_datadir %{_datadir}/proton-%{version}

# per https://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering#Preventing_files.2Fdirectories_from_being_scanned_for_deps_.28pre-scan_filtering.29
%global __provides_exclude_from ^%{proton_datadir}/examples/.*$
%global __requires_exclude_from ^%{proton_datadir}/examples/.*$

#  for older rpm, like el6, https://fedoraproject.org/wiki/EPEL:Packaging_Autoprovides_and_Requires_Filtering#Perl
%{?filter_setup:
%filter_provides_in %{proton_datadir}/examples/
%filter_requires_in %{proton_datadir}/examples/
%filter_setup
}

%global pythonx python2

%{!?__python2:%global __python2 %{__python}}
%{!?__python2:%global python2_sitelib %{python_sitelib}}
%{!?__python2:%global python2_sitearch %{python_sitearch}}
%{!?__python2:%global pythonx python}

Name:           qpid-proton
Version:        0.24.0
Release:        2%{?dist}
Group:          System Environment/Libraries
Summary:        A high performance, lightweight messaging library
License:        ASL 2.0
URL:            http://qpid.apache.org/proton/

Source0:        %{name}-%{version}.tar.gz
#Patch0:         proton.patch

Source1:        licenses.xml

%global proton_licensedir %{_licensedir}/proton-%{version}
%{!?_licensedir:%global license %doc}
%{!?_licensedir:%global proton_licensedir %{proton_datadir}}

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  swig
BuildRequires:  pkgconfig
BuildRequires:  doxygen
BuildRequires:  libuuid-devel
BuildRequires:  openssl-devel
BuildRequires: %{pythonx}-devel
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  python3-devel
%endif
BuildRequires:  epydoc
%if 0%{?fedora}
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  glibc-headers
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
%endif
BuildRequires:  cyrus-sasl-devel

%description
Proton is a high performance, lightweight messaging library. It can be used in
the widest range of messaging applications including brokers, client libraries,
routers, bridges, proxies, and more. Proton is based on the AMQP 1.0 messaging
standard. Using Proton it is trivial to integrate with the AMQP 1.0 ecosystem
from any platform, environment, or language.


%package c
Group:     System Environment/Libraries
Summary:   C libraries for Qpid Proton
Requires:  cyrus-sasl-lib
Obsoletes: qpid-proton

%description c
%{summary}.


%files c
%dir %{proton_datadir}
%license %{proton_licensedir}/LICENSE.txt
%license %{proton_licensedir}/licenses.xml
%doc %{proton_datadir}/README*
%{_libdir}/libqpid-proton.so.*
%{_libdir}/libqpid-proton-core.so.*
%{_libdir}/libqpid-proton-proactor.so.*

%post c -p /sbin/ldconfig

%postun c -p /sbin/ldconfig


%package   cpp
Group:     System Environment/Libraries
Summary:   C++ libraries for Qpid Proton
Requires:  qpid-proton-c%{?_isa} = %{version}-%{release} 

%description cpp
%{summary}.

%files cpp
%dir %{proton_datadir}
%license %{proton_licensedir}/LICENSE.txt
%license %{proton_licensedir}/licenses.xml
%doc %{proton_datadir}/README*
%{_libdir}/libqpid-proton-cpp.so.*

%post cpp -p /sbin/ldconfig

%postun cpp -p /sbin/ldconfig


%package c-devel
Group:     Development/System
Requires:  qpid-proton-c%{?_isa} = %{version}-%{release}
Summary:   Development libraries for writing messaging apps with Qpid Proton
Obsoletes: qpid-proton-devel

%description c-devel
%{summary}.

%files c-devel
%{_includedir}/proton
%exclude %{_includedir}/proton/*.hpp
%exclude %{_includedir}/proton/**/*.hpp
%{_libdir}/libqpid-proton.so
%{_libdir}/libqpid-proton-core.so
%{_libdir}/libqpid-proton-proactor.so
%{_libdir}/pkgconfig/libqpid-proton.pc
%{_libdir}/pkgconfig/libqpid-proton-core.pc
%{_libdir}/pkgconfig/libqpid-proton-proactor.pc
%{_libdir}/cmake/Proton


%package cpp-devel
Group:     Development/System
Requires:  qpid-proton-cpp%{?_isa} = %{version}-%{release}
Requires:  qpid-proton-c-devel%{?_isa} = %{version}-%{release}
Summary:   Development libraries for writing messaging apps with Qpid Proton

%description cpp-devel
%{summary}.

%files cpp-devel
%{_includedir}/proton/*.hpp
%{_includedir}/proton/**/*.hpp
%{_libdir}/pkgconfig/libqpid-proton-cpp.pc
%{_libdir}/libqpid-proton-cpp.so
%{_libdir}/cmake/ProtonCpp


%package c-docs
Summary:   Documentation for the C development libraries for Qpid Proton
BuildArch: noarch
Obsoletes: qpid-proton-c-devel-doc
Obsoletes: qpid-proton-c-devel-docs 

%description c-docs
%{summary}.

%files c-docs
%defattr(-,root,root,-)
%license %{proton_licensedir}/LICENSE.txt
%license %{proton_licensedir}/licenses.xml
%doc %{proton_datadir}/docs/api-c
%doc %{proton_datadir}/examples/c/ssl-certs
%doc %{proton_datadir}/examples/c/*.c
%doc %{proton_datadir}/examples/c/*.h
%doc %{proton_datadir}/examples/c/README.dox
%doc %{proton_datadir}/examples/c/CMakeLists.txt
%doc %{proton_datadir}/examples/c/example_test.py*


%package   cpp-docs
Summary:   Documentation for the C++ development libraries for Qpid Proton
BuildArch: noarch
Obsoletes: qpid-proton-cpp-devel-doc
Obsoletes: qpid-proton-cpp-devel-docs

%description cpp-docs
%{summary}.

%files cpp-docs
%defattr(-,root,root,-)
%license %{proton_licensedir}/LICENSE.txt
%license %{proton_licensedir}/licenses.xml
%{proton_datadir}/docs/api-cpp
%doc %{proton_datadir}/examples/cpp/*.cpp
%doc %{proton_datadir}/examples/cpp/*.hpp
%doc %{proton_datadir}/examples/cpp/README.dox
%doc %{proton_datadir}/examples/cpp/CMakeLists.txt
%doc %{proton_datadir}/examples/cpp/example_test.py*
%doc %{proton_datadir}/examples/cpp/ssl-certs
%doc %{proton_datadir}/examples/cpp/tutorial.dox


%package -n %{pythonx}-qpid-proton
%{?python_provide:%python_provide python2-qpid-proton}
Group:    System Environment/Libraries
Summary:  Python language bindings for the Qpid Proton messaging framework

Requires: qpid-proton-c%{?_isa} = %{version}-%{release}
Requires: %{pythonx}

%description -n %{pythonx}-qpid-proton
%{summary}.

%files -n %{pythonx}-qpid-proton
%defattr(-,root,root,-)
%license %{proton_licensedir}/LICENSE.txt
%license %{proton_licensedir}/licenses.xml
%{python2_sitearch}/*


%if 0%{?fedora} || 0%{?rhel} > 7
%package -n python3-qpid-proton
Group:    System Environment/Libraries
Summary:  Python language bindings for the Qpid Proton messaging framework
%{?python_provide:%python_provide python3-qpid-proton}

Requires: qpid-proton-c%{?_isa} = %{version}-%{release}
Requires: python3

%description -n python3-qpid-proton
%{summary}.

%files -n python3-qpid-proton
%{python3_sitearch}/*
%endif

%package -n python-qpid-proton-docs
Group:     Documentation
Summary:   Documentation for the Python language bindings for Qpid Proton
BuildArch: noarch
Obsoletes:  python-qpid-proton-doc

%description -n python-qpid-proton-docs
%{summary}.

%files -n python-qpid-proton-docs
%defattr(-,root,root,-)
%license %{proton_licensedir}/LICENSE.txt
%license %{proton_licensedir}/licenses.xml
%doc %{proton_datadir}/docs/api-py
%doc %{proton_datadir}/examples/python

%if 0%{?fedora}
%package -n perl-qpid-proton
Summary: Perl language bindings for Qpid Proton messaging framework

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:  qpid-proton-c = %{version}-%{release}

%description -n perl-qpid-proton
%{summary}.

%files -n perl-qpid-proton
%doc LICENSE.txt README*
%{perl_vendorarch}/*
%endif


%prep
%setup -q -n %{name}-%{version}
#%patch0 -p1


%build

%if 0%{?fedora}
export ADDCFLAGS=" -Wno-error=return-type"
%cmake \
    -DSYSINSTALL_BINDINGS=ON \
    -DCMAKE_SKIP_RPATH:BOOL=OFF \
    -DENABLE_FUZZ_TESTING=NO \
    "-DCMAKE_C_FLAGS=$CMAKE_C_FLAGS $CFLAGS $ADDCFLAGS" \
     -DCYRUS_SASL_INCLUDE_DIR=/usr/include \
    .
%endif
%if 0%{?rhel} && 0%{?rhel} <= 7
%cmake \
       -DCMAKE_EXE_LINKER_FLAGS="-Wl,-z,relro,-z,now" \
       -DCMAKE_SHARED_LINKER_FLAGS="-Wl,-z,relro" \
       -DCMAKE_MODULE_LINKER_FLAGS="-Wl,-z,relro" \
       -DSYSINSTALL_BINDINGS=ON \
       -DCMAKE_SKIP_RPATH:BOOL=OFF \
       -DENABLE_FUZZ_TESTING=NO \
       .
%endif

make all docs %{?_smp_mflags}
%if 0%{?fedora} || 0%{?rhel} > 7
(cd python/dist; %py3_build)
%endif

%install
rm -rf %{buildroot}

%make_install
%if 0%{?fedora} || 0%{?rhel} > 7
(cd python/dist; %py3_install)
%endif

CPROTON_BUILD=$PWD . ./config.sh

#chmod +x %{buildroot}%{python_sitearch}/_cproton.so
#find %{buildroot}%{proton_datadir}/examples/ -type f | xargs chmod -x 

%if 0%{?rhel} && 0%{?rhel} <= 6
install -pm 644 %{SOURCE1} %{buildroot}%{proton_datadir}/
%else
install -dm 755 %{buildroot}%{proton_licensedir}
install -pm 644 %{SOURCE1} %{buildroot}%{proton_licensedir}
install -pm 644 %{buildroot}%{proton_datadir}/LICENSE.txt %{buildroot}%{proton_licensedir}
rm -f %{buildroot}%{proton_datadir}/LICENSE.txt
%endif

# clean up files that are not shipped
rm -rf %{buildroot}%{_exec_prefix}/bindings
rm -rf %{buildroot}%{_libdir}/java
rm -rf %{buildroot}%{_libdir}/libproton-jni.so
rm -rf %{buildroot}%{_datarootdir}/java
rm -rf %{buildroot}%{_libdir}/proton.cmake
%if 0%{?rhel}
rm -rf %{buildroot}%{_libdir}/perl5
rm -rf %{buildroot}%{_libdir}/php
rm -rf %{buildroot}%{_libdir}/ruby
rm -rf %{buildroot}%{_datarootdir}/php
rm -rf %{buildroot}%{_datarootdir}/perl5
rm -rf %{buildroot}%{_datarootdir}/ruby
rm -rf %{buildroot}%{_sysconfdir}/php.d
%endif
rm -fr %{buildroot}%{proton_datadir}/examples/CMakeFiles
rm -f  %{buildroot}%{proton_datadir}/examples/Makefile
rm -f  %{buildroot}%{proton_datadir}/examples/*.cmake
rm -fr %{buildroot}%{proton_datadir}/examples/c/CMakeFiles
rm -f  %{buildroot}%{proton_datadir}/examples/c/*.cmake
rm -f  %{buildroot}%{proton_datadir}/examples/c/Makefile
rm -f  %{buildroot}%{proton_datadir}/examples/c/broker
rm -f  %{buildroot}%{proton_datadir}/examples/c/direct
rm -f  %{buildroot}%{proton_datadir}/examples/c/receive
rm -f  %{buildroot}%{proton_datadir}/examples/c/send
rm -f  %{buildroot}%{proton_datadir}/examples/c/send-abort
rm -f  %{buildroot}%{proton_datadir}/examples/c/send-ssl
rm -fr %{buildroot}%{proton_datadir}/examples/cpp/CMakeFiles
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/*.cmake
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/Makefile
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/broker
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/client
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/connection_options
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/direct_recv
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/direct_send
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/encode_decode
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/flow_control
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/helloworld
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/helloworld_direct
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/queue_browser
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/scheduled_send_03
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/scheduled_send
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/selected_recv
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/server
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/server_direct
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/service_bus
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/simple_connect
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/simple_recv
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/simple_send
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/ssl
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/ssl_client_cert
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/message_properties
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/multithreaded_client
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/multithreaded_client_flow_control
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/reconnect_client
rm -f  %{buildroot}%{proton_datadir}/examples/cpp/colour_send
rm -fr %{buildroot}%{proton_datadir}/examples/engine/java
rm -fr %{buildroot}%{proton_datadir}/examples/go
rm -fr %{buildroot}%{proton_datadir}/examples/java
rm -fr %{buildroot}%{proton_datadir}/examples/javascript
rm -fr %{buildroot}%{proton_datadir}/examples/ruby
rm -fr %{buildroot}%{proton_datadir}/examples/perl
rm -fr %{buildroot}%{proton_datadir}/examples/php


%check
%if 0%{?fedora}
# check perl bindings
pushd proton-c/bindings/perl
#make test
popd
%endif

%changelog
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Irina Boverman <iboverma@redhat.com> - 0.24.0-1
- Rebased to 0.24.0

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 0.21.0-4
- Perl 5.28 rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.21.0-3
- Perl 5.28 rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.21.0-2
- Rebuilt for Python 3.7

* Tue Mar 13 2018 Irina Boverman <iboverma@redhat.com> - 0.21.0-1
- Rebased to 0.21.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Merlin Mathesius <mmathesi@redhat.com> - 0.18.1-3
- Cleanup spec file conditionals

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.18.1-2
- Python 2 binary package renamed to python2-qpid-proton
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Nov 16 2017 Irina Boverman <iboverma@redhat.com> - 0.18.1-1
- Rebased to 0.18.1

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.17.0-8
- Python 2 binary package renamed to python2-qpid-proton
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug  9 2017 Irina Boverman <iboverma@redhat.com> - 0.17.0-7
- Resolves: PROTON-1526

* Tue Aug  8 2017 Irina Boverman <iboverma@redhat.com> - 0.17.0-6
- Added missing *.hpp files in qpid-proton-cpp-devel package

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.17.0-5
- Rebuild due to bug in RPM (RHBZ #1468476)

* Fri Jun 23 2017 Irina Boverman <iboverma@redhat.com> - 0.17.0-4
- Excluded *.hpp files from qpid-proton-c-devel

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.17.0-3
- Perl 5.26 rebuild

* Wed May 10 2017 Irina Boverman <iboverma@redhat.com> - 0.17.0-2
- Added 0001-PROTON-1466-proton-c-mixing-up-links-with-names-that.patch

* Tue Feb 21 2017 Irina Boverman <iboverma@redhat.com> - 0.17.0-1
- Rebased to 0.17.0
- Added *cpp* packages

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.14.0-3
- Rebuild for Python 3.6

* Wed Nov  9 2016 Irina Boverman <iboverma@redhat.com> - 0.14.0-2
- Renamed sub-packages qpid-proton-c-devel-docs/qpid-proton-cpp-devel-docs
  to qpid-proton-c-docs/qpid-proton-cpp-docs
- Removed binary and derived files from qpid-proton-cpp-docs package

* Tue Sep 6  2016 Irina Boverman <iboverma@redhat.com> - 0.14.0-1
- Added "-std=c++11" flag
- Rebased to 0.14.0

* Mon Aug 1  2016 Irina Boverman <iboverma@redhat.com> - 0.13.1-1
- Rebased to 0.13.1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 22 2016 Irina Boverman <iboverma@redhat.com> - 0.13.0-1
- Rebased to 0.13.0
- Changed *doc to *docs, moved examples to *docs

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.12.1-2
- Perl 5.24 rebuild

* Wed Mar 23 2016 Irina Boverman <iboverma@redhat.com> - 0.12.1-1
- Rebased to 0.12.1
- Added python3 installation

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep  8 2015 Irina Boverman <iboverma@redhat.com> - 0.10-2
- Added dependency on cyrus-sasl-devel and cyrus-sasl-lib
- Added 0001-PROTON-974-Accept-a-single-symbol-in-SASL-mechs-fram.patch
 
* Wed Sep  2 2015 Irina Boverman <iboverma@redhat.com> - 0.10-1
- Rebased to 0.10

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.9-4
- Perl 5.22 rebuild

* Wed Apr  8 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.9-3
- Added a global excludes macro to fix EL6 issues with example Perl modules.

* Wed Apr  8 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.9-2
- Marked the examples in -c-devel as doc.
- Turned off the executable flag on all files under examples.

* Mon Apr  6 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.9-1
- Rebased on Proton 0.9.
- Removed the proton binary from qpid-proton-c.
- Added the perl-qpid-proton subpackage.

* Tue Nov 18 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.8-1
- Rebased on Proton 0.8.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul  8 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.7-3
- Removed intra-package comments which cause error messages on package uninstall.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.7-1
- Rebased on Proton 0.7
- Added new CMake modules for Proton to qpid-proton-c-devel.

* Mon Feb 24 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.6-2
- Reorganized the subpackages.
- Merged up branches to get things back into sync.

* Thu Jan 16 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.6-1
- Rebased on Proton 0.6.
- Update spec to delete ruby and perl5 directories if Cmake creates them.
- Removed Java sub-packages - those will be packaged separate in future.

* Fri Sep  6 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.5-2
- Made python-qpid-proton-doc a noarch package.
- Resolves: BZ#1005058

* Wed Aug 28 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.5-1
- Rebased on Proton 0.5.
- Resolves: BZ#1000620

* Mon Aug 26 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-4
- Created the qpid-proton-c-devel-doc subpackage.
- Resolves: BZ#1000615

* Wed Jul 24 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-3
- Provide examples for qpid-proton-c
- Resolves: BZ#975723

* Fri Apr  5 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-2.2
- Added Obsoletes and Provides for packages whose names changed.
- Resolves: BZ#948784

* Mon Apr  1 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-2.1
- Fixed the dependencies for qpid-proton-devel and python-qpid-proton.

* Thu Mar 28 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-2
- Moved all C libraries to the new qpid-proton-c subpackage.

* Tue Feb 26 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-1
- Rebased on Proton 0.4.

* Thu Feb 21 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.3-4
- Fixes copying nested data.
- PROTON-246, PROTON-230

* Mon Jan 28 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.3-3
- Fixes build failure on non-x86 platforms.
- Resolves: BZ#901526

* Fri Jan 25 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.3-2
- Fixes build failure on non-x86 platforms.
- Resolves: BZ#901526

* Wed Jan 16 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.3-1
- Rebased on Proton 0.3.

* Fri Dec 28 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-2.4
- Moved ownership of the docs dir to the docs package.

* Wed Dec 19 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-2.3
- Fixed package dependencies, adding the release macro.

* Mon Dec 17 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-2.2
- Fixed subpackage dependencies on main package.
- Removed accidental ownership of /usr/include.

* Thu Dec 13 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-2.1
- Remove BR for ruby-devel.
- Removed redundant package name from summary.
- Removed debugging artifacts from specfile.
- Moved unversioned library to the -devel package.
- Added dependency on main package to -devel. 
- Fixed directory ownerships.

* Fri Nov 30 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-2
- Removed BR on help2man.
- Added patch for generated manpage.

* Mon Nov  5 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-1
- Initial packaging of the Qpid Proton.
