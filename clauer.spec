%define name	clauer
%define version	3.0.2
%define beta	0
%if %{beta}
%define release		%mkrel 0.beta.4
%define filevers	%{version}-beta
%else
%define release		5
%define filevers	%{version}
%endif

#stop automatic dependencies
%if %{_use_internal_dependency_generator}
%define __noautoreq 'devel\\(.*\\)'
%else
%define _requires_exceptions devel(.*)
%endif

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Cryptographic keyring on a USB storage device
License:	BSD-like
Group:		System/Servers
URL:		http://clauer.nisu.org/
Source0:	ClauerLinux-%{filevers}.tar.gz
Source1:	clos
Source2:	install-clauer-firefox.html
Source3:	uninstall-clauer-firefox.html
Source4:	clauer.png
Source5:	clauer-uninstall.png
Patch0:		ClauerLinux-3.0.2-no-install-hooks.patch
Patch1:		ClauerLinux-3.0.2-fix-configure.patch
Patch2:		ClauerLinux-3.0.2-link.patch
Requires(pre):	rpm-helper
BuildRequires:	libopenssl-devel
BuildRequires:	imagemagick
BuildRequires:	autoconf
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
This is a software that converts a simple CD-ROM or a USB flash disk
into an authentication tool, capable of performing authentication with
several levels of security, in particular with X509 certificates.
The result is that you carry, with a simple USB "pen drive", all your
x509 certificates and use them in a transparent way.

%prep
%setup -q -n ClauerLinux-%{version}
%patch0 -p1 -b .nohooks
%patch1 -p1 -b .configure
%patch2 -p0 -b .link

%build
# required by patch0
autoreconf -fi

%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall

#remove unwanted files
rm -f	%{buildroot}%{_bindir}/firefox-install-pkcs11.sh \
	%{buildroot}%{_bindir}/firefox-uninstall-pkcs11.sh \
	%{buildroot}%{_bindir}/makeclos-rc \
	%{buildroot}%{_bindir}/unmakeclos-rc \
	%{buildroot}%{_libdir}/libclauerpkcs11.{la,a}
rm -f %{buildroot}%{_libdir}/{libclio.{so,la,a},libCRYPTOWrap.{so,la,a},libIMPORT.{so,la,a},libRT.{so,la,a}}

#init script
mkdir -p %{buildroot}%{_initrddir}
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}

#language files
mkdir -p %{buildroot}/usr/share/locale/es/LC_MESSAGES
install -m 644 clauer-utils/clauer-utils_es.mo %{buildroot}/usr/share/locale/es/LC_MESSAGES/clauer-utils.mo
mkdir -p %{buildroot}/usr/share/locale/ca/LC_MESSAGES
install -m 644 clauer-utils/clauer-utils_ca.mo %{buildroot}/usr/share/locale/ca/LC_MESSAGES/clauer-utils.mo

#html pages to install/uninstall pkcs11 module from firefox
mkdir -p %{buildroot}%{_datadir}/clauer
perl -pl -e "s,---LIBDIR---,%{_libdir},g" %{SOURCE2} > %{buildroot}%{_datadir}/clauer/install-clauer-firefox.html
install -m 644 %{SOURCE3} %{buildroot}%{_datadir}/clauer

#icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{64x64,48x48,32x32,16x16}/apps
install -m 644 %{SOURCE4} %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
install -m 644 %{SOURCE5} %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}-uninstall.png
convert -scale 48 %{SOURCE4} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 %{SOURCE4} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{SOURCE4} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert -scale 48 %{SOURCE5} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}-uninstall.png
convert -scale 32 %{SOURCE5} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}-uninstall.png
convert -scale 16 %{SOURCE5} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}-uninstall.png

#installation instructions
cat > README.urpmi << EOF 
If you want to use the clauer with firefox/mozilla then use the Mandriva
menu option "Install clauer in Firefox" or open the file
%{_datadir}/clauer/install-clauer-firefox.html
with Firefox.
To install it in Thunderbird follow the instructions in the README file.
Keep in mind that the module is in %{_libdir}/libclauerpkcs11.so

Si vol usar el clauer amb firefox/mozilla seleccioni el programa
"Instal·lar clauer en firefox" des del menu mandriva o obri el fitxer
%{_datadir}/clauer/install-clauer-firefox.html 
amb firefox. Per a usar-lo amb thunderbird segueixi les instruccions en el
fitxer README però tingui en compte que el modulo està en
%{_libdir}/libclauerpkcs11.so

Si quiere usar el clauer con firefox/mozilla seleccione el programa
"Instalar clauer en firefox" desde el menu mandriva o abra el
fichero
%{_datadir}/clauer/install-clauer-firefox.html
con firefox. Para usarlo con thunderbird siga las instrucciones en el fichero
README pero tenga en cuenta que el modulo está en
%{_libdir}/libclauerpkcs11.so
EOF

#menu entries
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-pkcs11-firefox-install.desktop << EOF
[Desktop Entry]
Name=Install Clauer in Firefox
Comment=Install Clauer in Firefox
Name[es]=Instala Clauer en Firefox
Comment[es]=Instala Clauer en Firefox
Name[ca]=Instal·la Clauer per a Firefox
Comment[ca]=Instal·la Clauer per Firefox
Exec=%{_bindir}/firefox %{_datadir}/clauer/install-clauer-firefox.html 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Network;WebBrowser;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-pkcs11-firefox-uninstall.desktop << EOF
[Desktop Entry]
Name=Uninstall Clauer from Firefox
Comment=Uninstall Clauer from Firefox
Name[es]=Desinstala Clauer en Firefox
Comment[es]=Desinstala Clauer en Firefox
Name[ca]=Desinstal·la Clauer per a Firefox
Comment[ca]=Desinstal·la Clauer per a Firefox
Exec=%{_bindir}/firefox %{_datadir}/clauer/uninstall-clauer-firefox.html 
Icon=%{name}-uninstall
Terminal=false
Type=Application
StartupNotify=false
Categories=Network;WebBrowser;
EOF

%find_lang %{name}-utils

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 200900
/sbin/ldconfig
%endif
%_post_service clos
/sbin/service clos reload > /dev/null 2>&1 || :

%preun
%_preun_service clos

%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%files -f %{name}-utils.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING INSTALL README THANKS README.urpmi
%{_bindir}/*
%{_sbindir}/*
%{_initrddir}/clos
%{_datadir}/clauer
%{_datadir}/applications/*
%{_iconsdir}/hicolor/*/apps/*
%{_libdir}/lib*



%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0.2-3mdv2011.0
+ Revision: 610141
- rebuild

* Wed Apr 21 2010 Funda Wang <fwang@mandriva.org> 3.0.2-2mdv2010.1
+ Revision: 537528
- fix linkage

* Fri Oct 09 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.0.2-2mdv2010.0
+ Revision: 456218
- fix build
- fix dependencies on x86_64

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Tue Dec 23 2008 Adam Williamson <awilliamson@mandriva.org> 3.0.2-1mdv2009.1
+ Revision: 317799
- various fixes from Luca Olivetti (#45347):
  	+ disable underlinking protection
  	+ more dependency exceptions
  	+ fix the substitution so it doesn't generate a 0-byte file
- new release 3.0.2

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 3.0.0-2mdv2008.1
+ Revision: 140694
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Sep 13 2007 Adam Williamson <awilliamson@mandriva.org> 3.0.0-2mdv2008.0
+ Revision: 85216
- fix %%post
- Import clauer

