LANG=C
kver=6.13.10

do: clean build

clean:
	rm -rf BUILD/*
	rm -rf BUILDROOT/*
	rm -rf RPMS/*

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
	cd RPMS && python3 -m http.server 12345

