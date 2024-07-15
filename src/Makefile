#
# Copyright (C) 2024, Bill Rees, all rights reserved.
#

PACKAGE = loraline-netmanage
VERSION = 1.1-1
BUILDDIR =  ${PACKAGE}_${VERSION}
CONFIGDIR = etc/loraline/
SYSTEMDIR = lib/systemd/system/
UNITFILES = ${PACKAGE}.service ${PACKAGE}.socket

${SYSTEMDIR} ${CONFIGDIR}:
	@${MKDIR} $@

systemd: ${SYSTEMDIR}
	@cp lib/systemd/system/netmanage.s* debin/

config: ${CONFIGDIR}
	@cp etc/loraline/netmanage.conf debian/

