Name: kernel
Version: 6.13.7
Release: alk_1%{?dist}
Summary: Alicey Linux Kernel 6.13.7 for RockyLinux 9
License: GPLv2
Source: linux-6.13.7.tar.xz
BuildRequires: gcc, make, elfutils-libelf-devel, openssl-devel, bc, bison, flex
Requires: grub2-tools, grubby
ExclusiveArch: x86_64

%global debugsource_package %{nil}

%description
This is a custom-built Linux kernel 6.13.7 for Rocky Linux 9.

%prep
%setup -q -n linux-6.13.7

%build
#cp -v /boot/config-$(uname -r) .config
cp -v %{_sourcedir}/config .config
make olddefconfig
make -j$(nproc)

%install
mkdir -p %{buildroot}/boot
make INSTALL_MOD_PATH=%{buildroot} modules_install
make INSTALL_PATH=%{buildroot}/boot install

%files
/boot/vmlinuz-6.13.7
#boot/initramfs-6.13.7.img
/boot/System.map-6.13.7
/lib/modules/6.13.7

%post
/usr/bin/dracut --force --kver %{version} || true
if command -v grub2-mkconfig >/dev/null; then
    grub2-mkconfig -o /boot/grub2/grub.cfg || true
fi

if command -v grubby >/dev/null; then
    grubby --set-default /boot/vmlinuz-%{version} || true
fi

%postun
if [ "$1" = "0" ]; then
    # uninst
    rm -f /boot/initramfs-%{version}.img
    if command -v grub2-mkconfig >/dev/null; then
        grub2-mkconfig -o /boot/grub2/grub.cfg || true
    fi
fi

%changelog
* Fri Mar 21 2025 Alicey <sirius@alicey.dev> - 6.13.7-1
- Build alicey linux kernel for Rocky Linux 9.

