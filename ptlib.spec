Name:		ptlib
Summary:	Portable Tools Library
Version:	2.6.5
Release:	3%{?dist}
URL:		http://www.opalvoip.org/
Source0:	ftp://ftp.gnome.org/pub/gnome/sources/%{name}/2.6/%{name}-%{version}.tar.bz2
License:	MPLv1.0
Group:		System Environment/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Fix multilib issues in headers
Patch0:         ptlib-2.6.5-multilib.patch
# Fix strict aliasing errors
Patch1:         ptlib-2.6.5-strict-aliasing.patch

BuildRequires:	expat openssl-devel pkgconfig
BuildRequires:  alsa-lib-devel, libstdc++-devel, libv4l-devel
BuildRequires:  openldap-devel, expat-devel, flex, bison
BuildRequires:  SDL-devel
Obsoletes:	pwlib

%description
PTLib (Portable Tools Library) is a moderately large class library that 
has it's genesis many years ago as PWLib (portable Windows Library), a 
method to product applications to run on both Microsoft Windows and Unix 
systems. It has also been ported to other systems such as Mac OSX, VxWorks 
and other embedded systems.

It is supplied mainly to support the OPAL project, but that shouldn't stop
you from using it in whatever project you have in mind if you so desire. 

%package devel
Summary:	Development package for ptlib
Group:		Development/Libraries
Requires:	ptlib = %{version}-%{release}
Requires:	pkgconfig
Obsoletes:	pwlib-devel

%description devel
The ptlib-devel package includes the libraries and header files for ptlib.

%prep
%setup -q 

%patch0 -p1 -b .multilib
%patch1 -p1 -b .strict-aliasing

%build
export CFLAGS="$CFLAGS -DLDAP_DEPRECATED"
%configure --prefix=%{_prefix} --disable-static --enable-plugins --disable-oss --enable-v4l2 --disable-avc --disable-v4l
make %{?_smp_mflags} V=1

%install
rm -rf $RPM_BUILD_ROOT

make PREFIX=$RPM_BUILD_ROOT%{_prefix} LIBDIR=$RPM_BUILD_ROOT%{_libdir} install

# hack to fixup things for bug 197318
find $RPM_BUILD_ROOT%{_libdir} -name '*.so*' -type f -exec chmod +x {} \;

rm -rf $RPM_BUILD_ROOT%{_libdir}/libpt_s.a
rm -rf $RPM_BUILD_ROOT%{_datadir}/ptlib
rm -rf $RPM_BUILD_ROOT%{_bindir}/ptlib-config

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc History.txt ReadMe.txt mpl-1.0.htm
%attr(755,root,root) %{_libdir}/libpt*.so.*
%dir %{_libdir}/%{name}-%{version}
%dir %{_libdir}/%{name}-%{version}/devices
%dir %{_libdir}/%{name}-%{version}/devices/sound
%dir %{_libdir}/%{name}-%{version}/devices/videoinput
# List these explicitly so we don't get any surprises
%attr(755,root,root) %{_libdir}/%{name}-%{version}/devices/sound/alsa_pwplugin.so
%attr(755,root,root) %{_libdir}/%{name}-%{version}/devices/videoinput/v4l2_pwplugin.so

%files devel
%defattr(-,root,root)
%{_libdir}/libpt*.so
%{_includedir}/*
%{_libdir}/pkgconfig/ptlib.pc

%changelog
* Tue Jun 22 2010 Benjamin Otte <otte@redhat.com> - 2.6.5-3
- Remove ptlib-config binary
Resolves: #rhbz605100

* Tue Jun 22 2010 Benjamin Otte <otte@redhat.com> - 2.6.5-2
- Remove make scripts, they are unneeded (use pkg-config) and break multilib
- Add fix for strict aliasing problems
- Fix multilib issues in generated headers
Resolves: #rhbz605100

* Tue Sep 22 2009 Peter Robinson <pbrobinson@gmail.com> - 2.6.5-1
- New 2.6.5 stable release

* Sat Aug 22 2009 Tomas Mraz <tmraz@redhat.com> - 2.6.4-5
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 Peter Robinson <pbrobinson@gmail.com> - 2.6.4-1
- New 2.6.4 stable release

* Tue May 19 2009 Peter Robinson <pbrobinson@gmail.com> - 2.6.2-1
- New stable release for ekiga 3.2.1

* Wed Mar 18 2009 Peter Robinson <pbrobinson@gmail.com> - 2.6.1-1
- New stable release for ekiga 3.2.0

* Tue Mar  3 2009 Peter Robinson <pbrobinson@gmail.com> - 2.6.0-1
- New release for ekiga 3.1.2 beta

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 2.5.2-4
- rebuild with new openssl

* Tue Jan 13 2009 Peter Robinson <pbrobinson@gmail.com> - 2.5.2-3
- Add an extra build dep

* Tue Jan  6 2009 Peter Robinson <pbrobinson@gmail.com> - 2.5.2-2
- remove --enable-opal termpoarily, ironically so opal will compile

* Tue Jan  6 2009 Peter Robinson <pbrobinson@gmail.com> - 2.5.2-1
- New release for ekiga 3.1.0 beta

* Mon Oct 20 2008 Peter Robinson <pbrobinson@gmail.com> - 2.4.2-1
- Update to new stable release for ekiga 3.0.1

* Tue Sep 23 2008 Peter Robinson <pbrobinson@gmail.com> - 2.4.1-1
- Update to new stable release for ekiga 3, disable v4l1

* Wed Sep 10 2008 Peter Robinson <pbrobinson@gmail.com> - 2.3.1-2
- Build fixes from package review

* Sun Jun 8 2008 Peter Robinson <pbrobinson@gmail.com> - 2.3.1-1
- Initial version of ptlib
