

PACKAGE = loraline-netmanage
VERSION = 1.1-1
DEBPKGDIR = debian/${PACKAGE}
MKDIR = mkdir -p
RM = rm -f
RMR = rm -rf
CP = cp -a

${DEBPKGDIR}:
	@${MKDIR} $@

install: ${DEBPKGDIR}
	@${MKDIR} ${DEBPKGDIR}/usr/lib
	@${CP} etc/ ${DEBPKGDIR}
	@${CP} opt/${PACKAGE}  ${DEBPKGDIR}/usr/lib
	@${CP} ../lib/systemd/system/netmanage.service debian/${PACKAGE}.service
	@${CP} ../lib/systemd/system/netmanage.socket debian/${PACKAGE}.socket

	@find ${DEBPKGDIR} -name .gitignore -exec rm {} \;

clean:
	${RMR} debian/${PACKAGE}
	${RM} debian/${PACKAGE}.socket debian/${PACKAGE}.service
