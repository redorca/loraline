#############################################################################
#                                                                           #
#        Copyright (C) 2024, Bill Rees. All rights reserved.                #
#                                                                           #
#                                                                           #
#                                                                           #
#                                                                           #
#############################################################################


PACKAGE = loraline-netmanage
PKG_VER = 1.1-1
DESTDIR = debian/${PACKAGE}

MKDIR = mkdir -p
RM = rm -f
RMR = rm -rf
CP = cp -a

${DESTDIR}:
	@${MKDIR} $@

install: ${DESTDIR}
	@${MKDIR} ${DESTDIR}/usr/lib
	@${CP} etc/ ${DESTDIR}
	@${CP} opt/${PACKAGE}  ${DESTDIR}/usr/lib
	@${CP} ../lib/systemd/system/netmanage.service debian/${PACKAGE}.service
	@${CP} ../lib/systemd/system/netmanage.socket debian/${PACKAGE}.socket
	@find ${DESTDIR} -name .gitignore -exec rm {} \;

clean:
	${RMR} debian/${PACKAGE}
	${RM} debian/${PACKAGE}.socket debian/${PACKAGE}.service
