LANG=C

do: clean build

clean:
	rm -rf BUILD/*
	rm -rf BUILDROOT/*

build:
	rpmbuild \
		-bb \
		--define "_topdir $(shell pwd)" \
		--define "_builddir %{_topdir}/BUILD" \
		SPECS/kernel.spec

