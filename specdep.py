#!/usr/bin/python

# see http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch16s04.html

import sys
import os
import platform
import urlparse
import pkg
import getopt

from scripts.lib import mappkgname


def build_type():
    debian_like = ["ubuntu", "debian"]
    rhel_like = ["fedora", "redhat", "centos"]

    dist = platform.linux_distribution(full_distribution_name=False)[0].lower()
    assert dist in debian_like + rhel_like

    if dist in debian_like:
        return "deb"
    elif dist in rhel_like:
        return "rpm"


def map_package_name_deb(name):
    """Map RPM package name to equivalent Deb names"""
    return mappkgname.map_package(name)


# Rules to build SRPM from SPEC
def build_srpm_from_spec(spec):
    srpmpath = spec.source_package_path()
    print '%s: %s %s' % (srpmpath, spec.specpath(),
                         " ".join(spec.source_paths()))



# Rules to download sources

# Assumes each RPM only needs one download - we have some multi-source
# packages but in all cases the additional sources are patches provided
# in the Git repository
def download_rpm_sources(spec):
    for (url, path) in zip(spec.source_urls(), spec.source_paths()):
        source = urlparse.urlparse(url)

        # Source comes from a remote HTTP server
        if source.scheme in ["http", "https"]:
            print '%s: %s' % (path, spec.specpath())
            print '\t@echo [CURL] $@'
            print '\t@curl --silent --show-error -L -o $@ %s' % url

        # Source comes from a local file or directory
        if source.scheme == "file":
            print '%s: %s $(shell find %s)' % (
                path, spec.specpath(), source.path)

            # Assume that the directory name is already what's expected by the
            # spec file, and prefix it with the version number in the tarball
            print '\t@echo [GIT] $@'
            dirname = "%s-%s" % (os.path.basename(source.path), spec.version())
            print '\t@git --git-dir=%s/.git '\
                'archive --prefix %s/ -o $@ HEAD' % (source.path, dirname)


# Rules to build RPMS from SRPMS (uses information from the SPECs to
# get packages)
def build_rpm_from_srpm(spec):
    # This doesn't generate the right Makefile fragment for a multi-target
    # rule - we may end up building too often, or not rebuilding correctly
    # on a partial build
    rpm_paths = spec.binary_package_paths()
    srpm_path = spec.source_package_path()
    for rpm_path in rpm_paths:
        print '%s: %s' % (rpm_path, srpm_path)


def package_to_rpm_map(specs):
    provides_to_rpm = {}
    for spec in specs:
        for provided in spec.provides():
            for rpmpath in spec.binary_package_paths():
                provides_to_rpm[provided] = rpmpath
    return provides_to_rpm


def buildrequires_for_rpm(spec, provides_to_rpm):
    for rpmpath in spec.binary_package_paths():
        for buildreq in spec.buildrequires():
            # Some buildrequires come from the system repository
            if provides_to_rpm.has_key(buildreq):
                buildreqrpm = provides_to_rpm[buildreq]
                print "%s: %s" % (rpmpath, buildreqrpm)


def usage(name):
    """
    Print usage information
    """
    print "usage: %s [-h] [-i PKG] SPEC [SPEC ...]" % name


def parse_cmdline():
    """
    Parse command line options
    """

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:d:", 
                                   ["help", "ignore=", "dist="])
    except getopt.GetoptError as err:
        usage(sys.argv[0])
        print str(err)
        sys.exit(1)

    ignore = []
    dist = ""
    for opt, val in opts:
        if opt == "-i" or opt == "--ignore":
            ignore.append(val)
        elif opt == "-d" or opt == "--dist":
            dist = val
        else:
            usage(sys.argv[0])
            print "unknown option: %s" % opt
            sys.exit(1)

    if len(args) == 0:
        usage(sys.argv[0])
        print "%s: error: too few arguments" % sys.argv[0]
        sys.exit(1)

    return {"ignore": ignore, "specs": args, "dist": dist}


def main():
    params = parse_cmdline()
    specs = {}

    for spec_path in params['specs']:
        try:
            if build_type() == "deb":
                spec = pkg.Spec(spec_path, target="deb",
                                map_name=map_package_name_deb)
            else:
                spec = pkg.Spec(spec_path, target="rpm", dist=params['dist'])
            pkg_name = spec.name()
            if pkg_name in params['ignore']:
                continue

            specs[os.path.basename(spec_path)] = spec

        except pkg.SpecNameMismatch as e:
            sys.stderr.write("error: %s\n" % e.message)
            sys.exit(1)


    provides_to_rpm = package_to_rpm_map(specs.values())

    for spec in specs.itervalues():
        build_srpm_from_spec(spec)
        download_rpm_sources(spec)
        build_rpm_from_srpm(spec)
        buildrequires_for_rpm(spec, provides_to_rpm)
        print ""

    # Generate targets to build all srpms and all rpms
    all_rpms = []
    all_srpms = []
    for spec in specs.itervalues():
        rpm_path = spec.binary_package_paths()[0]
        all_rpms.append(rpm_path)
        all_srpms.append(spec.source_package_path())
        print "%s: %s" % (spec.name(), rpm_path)
    print ""

    print "rpms: " + " \\\n\t".join(all_rpms)
    print ""
    print "srpms: " + " \\\n\t".join(all_srpms)
    print ""
    print "install: all"
    print "\t. scripts/%s/install.sh" % build_type()


if __name__ == "__main__":
    main()
