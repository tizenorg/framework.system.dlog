Name:       dlog
Summary:    Logging service
Version:	0.4.1
Release:    5.1
Group:      System/Main
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    packaging/99-android-logger.rules
Source101:  packaging/dlog-main.service
Source102:  packaging/dlog-radio.service
Source103:  packaging/dlog-system.service
Source1001: packaging/dlog.manifest 

Requires(post): /sbin/ldconfig
Requires(post): /usr/bin/systemctl
Requires(post): /usr/bin/vconftool
Requires(postun): /sbin/ldconfig
Requires(postun): /usr/bin/systemctl
Requires(preun): /usr/bin/systemctl

%description
dlog API library

%package -n libdlog
Summary:    Logging service dlog API
Group:      Development/Libraries

%description -n libdlog
dlog API library

%package -n libdlog-devel
Summary:    Logging service dlog API
Group:      Development/Libraries
Requires:   lib%{name} = %{version}-%{release}

%description -n libdlog-devel
dlog API library


%package -n dlogutil
Summary:    print log data to the screen
Group:      Development/Libraries
Requires:   lib%{name} = %{version}-%{release}
Requires(post): /bin/rm, /bin/ln

%description -n dlogutil
utilities for print log data



%prep
%setup -q 

%build
cp %{SOURCE1001} .
%autogen
%configure 
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}/%{_sysconfdir}/rc.d/rc3.d
mkdir -p %{buildroot}/%{_sysconfdir}/rc.d/rc5.d
rm -f %{buildroot}/%{_sysconfdir}/etc/rc.d/rc3.d/S05dlog
rm -f %{buildroot}/%{_sysconfdir}/etc/rc.d/rc5.d/S05dlog
ln -s ../etc/rc.d/init.d/dlog.sh %{buildroot}/%{_sysconfdir}/rc.d/rc3.d/S05dlog
ln -s ../etc/rc.d/init.d/dlog.sh %{buildroot}/%{_sysconfdir}/rc.d/rc5.d/S05dlog

mkdir -p %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants
mkdir -p %{buildroot}%{_libdir}/udev/rules.d

install -m 0644 %SOURCE101 %{buildroot}%{_libdir}/systemd/system/
install -m 0644 %SOURCE102 %{buildroot}%{_libdir}/systemd/system/
install -m 0644 %SOURCE103 %{buildroot}%{_libdir}/systemd/system/
install -m 0644 %SOURCE1 %{buildroot}%{_libdir}/udev/rules.d/

ln -s ../dlog-main.service %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants/dlog-main.service
ln -s ../dlog-radio.service %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants/dlog-radio.service
ln -s ../dlog-system.service %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants/dlog-system.service


%preun -n dlogutil
if [ $1 == 0 ]; then
    systemctl stop dlog-main.service
    systemctl stop dlog-radio.service
    systemctl stop dlog-system.service
fi

%post -n dlogutil
systemctl daemon-reload
if [ $1 == 1 ]; then
    systemctl restart dlog-main.service
    systemctl restart dlog-radio.service
    systemctl restart dlog-system.service
fi

%postun -n dlogutil
systemctl daemon-reload

%post -n libdlog -p /sbin/ldconfig

%postun -n libdlog -p /sbin/ldconfig


%files  -n dlogutil
%manifest dlog.manifest
%{_bindir}/dlogutil
%{_sysconfdir}/rc.d/init.d/dlog.sh
%{_sysconfdir}/rc.d/rc3.d/S05dlog
%{_sysconfdir}/rc.d/rc5.d/S05dlog
%{_libdir}/systemd/system/dlog-main.service
%{_libdir}/systemd/system/dlog-radio.service
%{_libdir}/systemd/system/dlog-system.service
%{_libdir}/systemd/system/multi-user.target.wants/dlog-main.service
%{_libdir}/systemd/system/multi-user.target.wants/dlog-radio.service
%{_libdir}/systemd/system/multi-user.target.wants/dlog-system.service
%{_libdir}/udev/rules.d/99-android-logger.rules

%files  -n libdlog
%manifest dlog.manifest
%doc LICENSE
%{_libdir}/libdlog.so.0
%{_libdir}/libdlog.so.0.0.0

%files -n libdlog-devel
%manifest dlog.manifest
%{_includedir}/dlog/dlog.h
%{_libdir}/pkgconfig/dlog.pc
%{_libdir}/libdlog.so

