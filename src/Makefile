#
# Copyright (C) 2024, Bill Rees, all rights reserved.
#

PACKAGE = loraline-netmanage
VERSION = 1.1-1
BUILDDIR =  ${PACKAGE}_${VERSION}
CONFIGDIR = etc/loraline/
SYSTEMDIR = lib/systemd/system/
UNITFILES = ${PACKAGE}.service ${PACKAGE}.socket
CONFFILE  = netmanage.conf
SOURCES = cmds tests connections.py debian

MKDIR = mkdir -p
RM = rm -f
CP = cp

${SYSTEMDIR} ${CONFIGDIR} ${BUILDDIR}:
	@${MKDIR} $@

setup: ${BUILDDIR}
	@for name in ${SOURCES} ; do \
		${CP} -a $${name} ${BUILDDIR} ;\
	done
	@find ${BUILDDIR} -name .gitignore -exec rm {} \;
	@for target in $$(find ${BUILDDIR} -name __pycache__ -type d) ; do \
		echo "target $${target}" ;\
		rm -rf $${target} ; \
		done

build:
	debuild -i -us -uc -b

systemd: ${SYSTEMDIR}
	@cp lib/systemd/system/netmanage.s* debin/

config: ${CONFIGDIR}
	@cp etc/loraline/netmanage.conf debian/

rooted: ${CONFIGDIR:%=/%}
	@sudo cp ${CONFIGDIR}/${CONFFILE} $^

cleandeb:
	@${RM} -r ${BUILDDIR}

clean: cleandeb
