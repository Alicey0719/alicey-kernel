LANG=C
kver=6.12.47

do: clean dl_kernel build

clean:
	rm -rf BUILD/*
	rm -rf BUILDROOT/*
	rm -rf RPMS/*
	rm -f  SOURCES/linux-*.tar.xz

dl_kernel:
	wget -P SOURCES/ https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-${kver}.tar.xz

build:
	rpmbuild \
		-bb \
		--define "_topdir $(shell pwd)" \
		--define "_builddir %{_topdir}/BUILD" \
		SPECS/kernel.spec
	ls -lh RPMS/x86_64/

copy_current_config:
	echo $(uname -r)
	cp /boot/config-$(shell uname -r) SOURCES/config

menu_config:
	cp -v BUILD/linux-${kver}/.config BUILD/linux-${kver}/.config.old
	cp -v SOURCES/config BUILD/linux-${kver}/.config
	cd BUILD/linux-${kver} && make menuconfig
	cp -v SOURCES/config SOURCES/config.old
	cp -v BUILD/linux-${kver}/.config SOURCES/config

run_httpserver:
	# echo "http://172.16.1.55:12345/x86_64/"
	cd RPMS && python3 -m http.server 12345

