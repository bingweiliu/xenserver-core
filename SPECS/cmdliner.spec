Name:           cmdliner
Version:        0.9.3
Release:        1%{?dist}
Summary:        Declarative definition of commandline interfaces for OCaml
License:        BSD3
Group:          Development/Other
URL:            http://erratique.ch/software/cmdliner
Source0:        http://erratique.ch/software/%{name}/releases/%{name}-%{version}.tbz
BuildRequires:  ocaml ocaml-findlib ocaml-ocamldoc
Requires:       ocaml ocaml-findlib

%description
Cmdliner is an OCaml module for the declarative definition of command line
interfaces. It provides a simple and compositional mechanism to convert
command line arguments to OCaml values and pass them to your functions.
The module automatically handles syntax errors, help messages and UNIX
man page generation. It supports programs with single or multiple commands
(like darcs or git) and respects most of the POSIX and GNU conventions.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Other

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q

%build
ocaml setup.ml -configure --destdir %{buildroot}/%{_libdir}/ocaml
ocaml setup.ml -build

%install
mkdir -p %{buildroot}/%{_libdir}/ocaml
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
ocaml setup.ml -install


%files
# This space intentionally left blank

%files devel
%doc README CHANGES
%{_libdir}/ocaml/cmdliner/*

%changelog
* Thu May 30 2013 David Scott <dave.scott@eu.citrix.com> - 0.9.3-1
- Initial package

