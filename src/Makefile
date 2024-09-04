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

fixup:
	$(Q) find $(DESTDIR) -name .gitignore -exec $(RM) {} \;

doc-fix:
	$(Q) for pdf in $$(find $(INSTALL_PATH)/share/doc -name "*.pdf") ; do   \
		gzip $$pdf  ; \
	     done
	$(Q) 
	$(Q) 

$(DESTDIR)$(TARGETDIR) $(DESTDIR)/opt/$(PACKAGE):
	$(Q) [ -d $@ ] || $(MKDIR) $@


clean:
	$(Q) $(RM) $(PACKAGE)_$(PKG_VER).* $(PACKAGE)_$(PKG_VER)_*
	$(Q) $(RM) data.tar.*  control.tar.* debian-binary
	$(Q) [ ! -d $(DESTDIR)/debian ] || (cd ${DESTDIR%debian*}debian/ && $(RM) -r debhelper-build-stamp *.substvars .debhelper)

clobber: clean
	$(Q) $(RMR) $(DESTDIR)


