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
DESTDIR ?= debian/$(PACKAGE)
DISTPKGS_DIR = lib/python3/dist-packages/

MKDIR = mkdir -p
RM = rm -f
RMR = rm -rf
CP = cp -a

install: $(DESTDIR)/usr/lib $(DESTDIR)/$(DISTPKGS_DIR)
	@$(CP) etc/ $(DESTDIR)
	@$(CP) $(DISTPKGS_DIR)$(PACKAGE)  $(DESTDIR)/$(DISTPKGS_DIR)
	@$(CP) ../lib/systemd/system/netmanage.service debian/$(PACKAGE).service
	@$(CP) ../lib/systemd/system/netmanage.socket debian/$(PACKAGE).socket
	@find $(DESTDIR) -name .gitignore -exec rm {} \;

$(DESTDIR)/usr/lib $(DESTDIR)/$(DISTPKGS_DIR):
	@$(MKDIR) $@
clean:
	$(RMR) debian/$(PACKAGE)
	$(RM) debian/$(PACKAGE).socket debian/$(PACKAGE).service
