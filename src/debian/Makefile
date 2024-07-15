#
#
# Copyright (C) IoAire Inc, All rights Reserved. [brees@ioaire.com]
#
#

BINDIR ?= /usr/bin
ETCDIR ?= /etc/loraline/
SYSTEMDIR ?= /lib/systemd/system/
packageName = netmanage
packageVersion = 1.1-1
packageArch = any
BUILD_DIR = ${packageName}-${packageVersion}
DEB = ${packageName}_${packageVersion}.deb
RM = rm -f
MKDIR = mkdir -p
DIRS_LIST = ${SYSTEMDIR} ${ETCDIR} ${BINDIR}

.PHONY: install all

all:
	@echo "use the install target instead."

dirs:
	@for dir in $(addprefix ${BUILD_DIR}, ${DIRS_LIST}) ; do ${MKDIR} $${dir}; done

install: dirs dtb
	cp -a debian ${BUILD_DIR}

build:
	cd ${BUILD_DIR} && dpkg-buildpackage -b

clean: clean_dtb
	@[ ! -f ${DEB} ] || ${RM} $$(ar -t ${DEB})
	@[ ! -f ${BUILD_DIR}/debian/files ] || ${RM} $$(awk '{print $$1}' ${BUILD_DIR}/debian/files)
	@${RM} -r ${BUILD_DIR} ; ${RM} *.changes *.deb

boot_dir:
	@${MKDIR} ${BUILD_DIR}/boot/overlays

