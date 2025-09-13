%define release_date %(date +%%Y%%m%%d)

Name:           kernel
Version:        6.12.47
Release:        %{release_date}.1%{?dist}_alk
Summary:        Alicey Linux Kernel
License:        GPLv2
Source0:        linux-%{version}.tar.xz
BuildRequires:  gcc, make, ncurses-devel, bc, bison, flex, elfutils-libelf-devel, openssl-devel, gcc-aarch64-linux-gnu
Requires:       grub2-tools, grubby
%global debug_package %{nil}

%description
Custom-built Alicey Linux Kernel for rhel.

%prep
%setup -q -n linux-%{version}

%build
make mrproper
#cp /boot/config-$(uname -r) .config
cp -v %{_sourcedir}/config .config
# make olddefconfig
# make defconfig
make oldconfig
make modules_prepare
make -j$(nproc) bzImage modules #V=1

%install
mkdir -p %{buildroot}/boot
mkdir -p %{buildroot}/lib/modules/%{version}

make INSTALL_MOD_PATH=%{buildroot} modules_install
cp arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{version}
cp System.map %{buildroot}/boot/System.map-%{version}
cp .config %{buildroot}/boot/config-%{version}


%files
/boot/vmlinuz-%{version}
/boot/System.map-%{version}
/boot/config-%{version}
/lib/modules/%{version}


%post
distro_name=$(source /etc/os-release && echo "$NAME")
distro_version=$(source /etc/os-release && echo "$VERSION_ID")

#/sbin/depmod %{version}-%{release}
#grub2-mkconfig -o /boot/grub2/grub.cfg
echo 'Create initramfs...'
/usr/bin/dracut --force --kver %{version} || true
if command -v grub2-mkconfig >/dev/null; then
    echo 'Update grub cfg'
    grub2-mkconfig --update-bls-cmdline -o /etc/grub2.cfg || true
fi

if command -v grubby >/dev/null; then
    grubby --add-kernel=/boot/vmlinuz-%{version} --title="${distro_name} ${distro_version} Alicey Linux Kernel %{version}" --initrd=/boot/initramfs-%{version}.img --copy-default || true
    grubby --set-default /boot/vmlinuz-%{version} --copy-default || true
    # grubby --info=ALL
fi

%postun
if [ "$1" = "0" ]; then
    # uninst
    rm -f /boot/initramfs-%{version}.img || true
    if command -v grub2-mkconfig >/dev/null; then
        grub2-mkconfig --update-bls-cmdline -o /etc/grub2.cfg || true
    fi
fi




%changelog
* Sun Sep 14 2025 Alicey <sirius@alicey.dev> - 6.12.47-1.el9_alk
- Initial build of Alicey Linux kernel (longterm).

