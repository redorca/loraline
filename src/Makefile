#############################################################################
#                                                                           #
#        Copyright (C) 2019, Bill Rees                                      #
#                                                                           #
#                                                                           #
#                                                                           #
#                                                                           #
#############################################################################

PACKAGE = loraline-netmanage
PKG_VER = 1.1-1
#
# DESTDIR points to the root directory
#
# DESTDIR?=debian/$(PACKAGE)
DESTDIR ?= $(PACKAGE)
UNIT_FILES_PATH = lib/systemd/system
INSTALL_PATH = $(DESTDIR)$(TARGETDIR)
Q=@
RM = rm -f
RMR = $(RM) -r
CP = cp -a
MKDIR = mkdir -p

all:
	$(Q) echo "====================="

changelog:
	$(Q) echo "$(PACKAGE) ($(PKG_VER)) UNRELEASED; urgency=medium" > fupu
	$(Q) echo "\n\n * Initial release\n" >> fupu
	$(Q) echo "\t-- bill <bill@zglue.com>  Sat, 04 May 2019 23:28:32 -0700" >> fupu


install: package fixup
	@echo "===================================="

package: Foo=$(PACKAGE:gcc-%=%)
package: $(DESTDIR)$(TARGETDIR) $(DESTDIR)/opt/$(PACKAGE)
	$(Q) $(CP) etc/ $(DESTDIR)
	$(Q) $(CP) ../loglady cmds/ $(DESTDIR)/opt/${PACKAGE}
	$(Q) $(CP) *.py $(DESTDIR)/opt/${PACKAGE}
	$(Q) $(CP) debian/ $(DESTDIR)
	$(Q) $(CP) debian/Makefile $(DESTDIR)
	$(Q) $(CP) $(UNIT_FILES_PATH)/netmanage.service $(DESTDIR)/debian/loraline-netmanage.service
	$(Q) $(CP) $(UNIT_FILES_PATH)/netmanage.socket $(DESTDIR)/debian/loraline-netmanage.socket

fixup:
	$(Q) find $(DESTDIR) -name .gitignore -exec $(RM) {} \;

doc-fix:
	$(Q) for pdf in $$(find $(INSTALL_PATH)/share/doc -name "*.pdf") ; do   \
		gzip $$pdf  ; \
	     done

$(DESTDIR)$(TARGETDIR) $(DESTDIR)/opt/$(PACKAGE):
	$(Q) [ -d $@ ] || $(MKDIR) $@


clean:
	$(Q) $(RM) $(PACKAGE)_$(PKG_VER).* $(PACKAGE)_$(PKG_VER)_*
	# $(Q) $(RM) debian/*.service debian/*.socket
	$(Q) $(RM) data.tar.*  control.tar.* debian-binary
	$(Q) [ ! -d $(DESTDIR)/debian ] || (cd ${DESTDIR%debian*}debian/ && $(RM) -r debhelper-build-stamp *.substvars .debhelper)

clobber: clean
	$(Q) $(RMR) $(DESTDIR)


