Version: 0.9.8.6
Release: 1%{?dist}
Summary: The omake build system
Name: omake
URL: http://omake.metaprl.org/
Source0: http://pkgs.fedoraproject.org/repo/pkgs/ocaml-omake/omake-0.9.8.6-0.rc1.tar.gz/fe39a476ef4e33b7ba2ca77a6bcaded2/omake-0.9.8.6-0.rc1.tar.gz
Patch0: omake-1-warnings
License: GPL
Group: Development/Tools
BuildRequires: ocaml >= 3.09.2, make, ncurses-devel

%define debug_package %{nil}

%description

OMake is a build system, similar to GNU make, but with many additional
features, including:
- Support for large projects spanning multiple directories;
- Support for commands that produce several targets at once;
- Fast, accurate, automated dependency analysis using MD5 digests;
- Portability: omake provides a consistent interface on Win32
  and on Unix systems including Linux, OSX, and Cygwin;
- Builtin functions that provide the most common features of
  programs like grep, sed, and awk;
- Active filesystem monitoring, where the build automatically
  restarts whenever you modify a source file.

%prep
%setup -q
%patch0 -p1 -b ~omake-1-warnings

%build
INSTALL_ROOT=$RPM_BUILD_ROOT\
   PREFIX=%{_prefix}\
   BINDIR=%{_bindir}\
   LIBDIR=%{_libdir}\
   make all

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/omake

INSTALL_ROOT=$RPM_BUILD_ROOT\
   PREFIX=%{_prefix}\
   BINDIR=%{_bindir}\
   LIBDIR=%{_libdir}\
   make install

chmod +w $RPM_BUILD_ROOT/%{_bindir}/*


%files
%doc LICENSE LICENSE.OMake doc/txt/omake-doc.txt doc/ps/omake-doc.ps doc/ps/omake-doc.pdf doc/webpage CHANGELOG.txt

%attr(555,root,root) %{_bindir}/*
%{_libdir}/omake

%changelog
* Thu Nov 25 2010 Mike McClurg <mike.mcclurg@citrix.com> - 0.9.8.6-1
- Updated to 0.9.8.6 (revision 13252) to support OCaml 3.12.0.

* Fri May 14 2010 David Scott <dave.scott@eu.citrix.com>
- Customise for XCP

* Thu Dec 11 2006 Aleksey Nogin <rpm@nogin.org> [0.9.8-1]
- Updated for the new doc file list and the lack of the man pages.

* Thu Aug 16 2005 Aleksey Nogin <rpm@nogin.org>
- Updated to account for the new non-autoconf build style.

* Mon Sep  9 2004 Aleksey Nogin <rpm@nogin.org>
- Added doc files.

* Thu May  8 2003 Jason Hickey <jyh_@cs.caltech.edu>
- Added cvs_realclean

* Tue Apr 22 2003 Aleksey Nogin <rpm@nogin.org>
- Path updates

* Tue Apr 22 2003 Jason Hickey <jyh_@cs.caltech.edu>
- Initial build.
