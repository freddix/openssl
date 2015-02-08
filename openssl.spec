# based on PLD Linux spec git://git.pld-linux.org/packages/openssl.git
%include	/usr/lib/rpm/macros.perl

Summary:	OpenSSL Toolkit for Secure Sockets Layer and Transport Layer Security
Name:		openssl
Version:	1.0.2
Release:	1
License:	Apache-like
Group:		Libraries
Source0:	ftp://ftp.openssl.org/source/%{name}-%{version}.tar.gz
# Source0-md5:	38373013fc85c790aabf8837969c5eba
Patch0:		%{name}-include.patch
Patch1:		%{name}-ldflags.patch
URL:		http://www.openssl.org/
BuildRequires:	perl-devel
BuildRequires:	rpm-perlprov
BuildRequires:	sed
Suggests:	ca-certificates
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags   -Wa,--noexecstack

%description
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, full-featured, and Open Source toolkit implementing
the Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS
v1) protocols with full-strength cryptography world-wide. The project
is managed by a worldwide community of volunteers that use the
Internet to communicate, plan, and develop the OpenSSL tookit and its
related documentation.

%package tools
Summary:	OpenSSL command line tool and utilities
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description tools
The OpenSSL Toolkit cmdline tool openssl and utility scripts.

%package tools-perl
Summary:	OpenSSL utilities written in Perl
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description tools-perl
OpenSSL Toolkit tools written in Perl.

%package devel
Summary:	Development part of OpenSSL Toolkit libraries
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development part of OpenSSL library.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
touch Makefile.*
./Configure \
	--openssldir=/etc//ssl	    \
	--libdir=%{_lib}	    \
	shared zlib		    \
%ifarch %{ix86}
	linux-elf		    \
%endif
%ifarch %{x8664}
	linux-x86_64		    \
	enable-ec_nistp_64_gcc_128  \
%endif
	%{rpmcppflags} %{rpmcflags} %{rpmldflags}
%{__make} depend
%{__make} -j1

%check
%{__make} -j1 test

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/ssl,%{_libdir}/%{name}} \
	$RPM_BUILD_ROOT{%{_mandir}/{pl/man1,man{1,3,5,7}},%{_datadir}/ssl} \
	$RPM_BUILD_ROOT%{_pkgconfigdir}

%{__make} -j1 install \
	INSTALLTOP=%{_prefix} \
	INSTALL_PREFIX=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}   \
	MANSUFFIX=ssl

mv -f $RPM_BUILD_ROOT/etc/ssl/misc/* $RPM_BUILD_ROOT%{_libdir}/%{name}
%{__sed} -i -e "s|./demoCA|/etc/ssl|g" \
    $RPM_BUILD_ROOT%{_libdir}/%{name}/* $RPM_BUILD_ROOT/etc/ssl/openssl.cnf
rm -rf $RPM_BUILD_ROOT/etc/ssl/misc

# not installed as individual utilities (see openssl dgst instead)
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{md2,md4,md5,mdc2,ripemd160,sha,sha1}.1ssl


%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES CHANGES.SSLeay LICENSE NEWS README doc/*.txt
%doc doc/openssl_button.gif doc/openssl_button.html
%attr(755,root,root) %{_libdir}/libcrypto.so.*.*.*
%attr(755,root,root) %{_libdir}/libssl.so.*.*.*
%dir %{_libdir}/engines
%attr(755,root,root) %{_libdir}/engines/*.so
%dir /etc/ssl
%dir /etc/ssl/certs
%dir /etc/ssl/private
%dir %{_datadir}/ssl

%files tools
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/ssl/openssl.cnf
%attr(755,root,root) %{_bindir}/%{name}

%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/CA.sh
%attr(755,root,root) %{_libdir}/%{name}/c_hash
%attr(755,root,root) %{_libdir}/%{name}/c_info
%attr(755,root,root) %{_libdir}/%{name}/c_issuer
%attr(755,root,root) %{_libdir}/%{name}/c_name

%{_mandir}/man1/asn1parse.1*
%{_mandir}/man1/ca.1*
%{_mandir}/man1/ciphers.1*
%{_mandir}/man1/crl.1*
%{_mandir}/man1/crl2pkcs7.1*
%{_mandir}/man1/dgst.1*
%{_mandir}/man1/dhparam.1*
%{_mandir}/man1/dsa.1*
%{_mandir}/man1/dsaparam.1*
%{_mandir}/man1/ec.1*
%{_mandir}/man1/ecparam.1*
%{_mandir}/man1/enc.1*
%{_mandir}/man1/errstr.1*
%{_mandir}/man1/gendsa.1*
%{_mandir}/man1/genpkey.1*
%{_mandir}/man1/genrsa.1*
%{_mandir}/man1/nseq.1*
%{_mandir}/man1/ocsp.1*
%{_mandir}/man1/openssl.1*
%{_mandir}/man1/passwd.1*
%{_mandir}/man1/pkcs12.1*
%{_mandir}/man1/pkcs7.1*
%{_mandir}/man1/pkcs8.1*
%{_mandir}/man1/pkey.1*
%{_mandir}/man1/pkeyparam.1*
%{_mandir}/man1/pkeyutl.1*
%{_mandir}/man1/rand.1*
%{_mandir}/man1/req.1*
%{_mandir}/man1/rsa.1*
%{_mandir}/man1/rsautl.1*
%{_mandir}/man1/s_client.1*
%{_mandir}/man1/s_server.1*
%{_mandir}/man1/s_time.1*
%{_mandir}/man1/sess_id.1*
%{_mandir}/man1/smime.1*
%{_mandir}/man1/speed.1*
%{_mandir}/man1/spkac.1*
%{_mandir}/man1/ts.1*
%{_mandir}/man1/tsget.1*
%{_mandir}/man1/verify.1*
%{_mandir}/man1/version.1*
%{_mandir}/man1/x509.1*
%{_mandir}/man5/config.5*
%{_mandir}/man5/x509v3_config.5*

%files tools-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/c_rehash
%attr(755,root,root) %{_libdir}/%{name}/CA.pl
%attr(755,root,root) %{_libdir}/%{name}/tsget
%{_mandir}/man1/CA.pl.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcrypto.so
%attr(755,root,root) %{_libdir}/libssl.so
%{_includedir}/%{name}
%{_pkgconfigdir}/libcrypto.pc
%{_pkgconfigdir}/libssl.pc
%{_pkgconfigdir}/openssl.pc
%{_mandir}/man3/*.3*
%{_mandir}/man7/des_modes.7*

