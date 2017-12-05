# -*- coding: utf-8 -*-

from deplint.model.package_releases import PackageReleases
from deplint.parsers.pip_search import PipSearchParser


SEARCH_EXAMPLE_SIX = '''
aio (0.1)                          - A CPython extension module wrapping the POSIX aio_* syscalls
aio-pipe (0.1.1)                   - POSIX Pipe async helper
AoikSixyIO (0.1.0)                 - Make Python string encoding and IO code 2*3 compatible, mess-
                                     free, and error-proof.
asgi_ipc (1.4.1)                   - Posix IPC-backed ASGI channel layer implementation
astralnetworking (0)               - A very high level gaming network protocol built on top of
                                     podsixnet
ax88179_178a-pinger (1.0)          - A helper to work around regular failure of the ax88179_178a
                                     driver for the ASIX A88179 and A88178 USB3.0-to-Gigabit-Ethernet
                                     adapters.
bobtemplates.sixfeetup (1.0)       - Unified buildout template for Plone projects.
bvcopula (0.9.0)                   - Probability and sampling functions for six common seen bivariate
                                     copulas
classix (0.5)                      - Declarative way to associate classes with lxml XML elements.
Sixpack-client (1.2.0)             - Python client for Sixpack, an A/B testing framework under active
                                     development at SeatGeek
clom (0.8.0a1)                     - The easiest way to use the command line with Python. Command
                                     Line Object Mapper. A library for building POSIX command line
                                     arguments, commands, and parameters. Very useful for Fabric
                                     tasks.
clyent (1.2.1)                     - Command line client Library for windwos and posix
daemonator (0.4.1.1)               - Lightweight and no-nonsense POSIX daemon library for Python
                                     (2.x.x/3.x.x)
dash_h (0.1)                       - Automatically generate POSIX-standard shell utilities from the
                                     shell.
django-sixpack (1.0.5)             - A django-friendly wrapper for sixpack-py
django-tasix (0.3.0)               - Simple django app to allow/block IP addresses and ranges outside
                                     the Tas-IX network
django-six (1.0.2)                 - Django-six —— Django Compatibility Library
django-unixtimestampfield (0.3.9)  - Django Unix timestamp (POSIX type) field
docpie (0.3.6)                     - An easy and Pythonic way to create your POSIX command line
                                     interface
docsix (0.1)                       - Doctests on Python 2 & 3
dots-editor (0.3.7)                - A six-key brailler emulator written in python.
drop_privileges (0.1)              - Drop root privileges on a POSIX system.
drunken_child_in_the_fog (0.3.1)   - PDF parser API inspired by Django QuerySet, using PDFMiner.six
envr (0.3.5)                       - Manipulate and transform .env files that are a subset of POSIX-
                                     compliant shell scripts.
esix (1.3.1)                       - Python frontend for the e621 JSON API.
exclusiveprocess (0.9.4)           - Exclusive process locking to ensure that your code does not
                                     execute concurrently, using POSIX file locking.
executed (0.9.0.2)                 - A package providing a process execution facility on top of the
                                     POSIX fork/exec model.
exitstatus (1.2.0)                 - POSIX exit status codes
fadvise (6.0.0)                    - Python interface to posix_fadvise(2)
fallocate (1.6.2)                  - Module to expose posix_fallocate(3), posix_fadvise(3) and
                                     fallocate(2)
Flask-Sixpack (0.0.1)              - Flask wrapper for Sixpack
flufl.lock (3.2)                   - NFS-safe file locking with timeouts for POSIX systems.
sync-github-forks (0.1.2)          - Extension for os module, for POSIX systems only
fsnix (0.2)                        - Expose more advanced posix/file system APIs to Python
fullChart (0.1.a)                  - generate charts (using gdchart) from mosix log files
getent (0.2)                       - Python interface to the POSIX getent family of commands
htmlmerge (1.2.7)                  - Merges html files that are created by pdfminer.six using exact
                                     option
indico_sixpay (1.2.2)              - Indico EPayment Sub-Plugin to use SixPay services
infi.mountoolinux (0.1.17)         - Python library for handling POSIX mounts
ipcqueue (0.9.4)                   - Ipcqueue provides POSIX and SYS V message queues functionality
                                     to exchange data among processes.
jsoncmd (0.0)                      - half-baked support for adding --json support to POSIX commands
libsixel-python (0.4.0)            - libsixel binding for Python
linkat (1.1)                       - Python support for the POSIX/Linux functions linkat and
                                     symlinkat.
locknix (1.0.3)                    - NFS-safe file locking with timeouts for POSIX systems.
micropython-posixpath (0.0.1)      - Dummy posixpath module for MicroPython
mkdir-p (0.1.1)                    - Python 2 and 3 compatible POSIX mkdir -p.
momentx (0.2.3)                    - A lightweight wrapper around datetime with a focus on timezone
                                     handling and few dependencies (datetime, pytz and six).
musixmatch (0.9)                   - Package to interface with the Musixmatch API
shared-ndarray (1.1.1)             - A pickleable wrapper for sharing NumPy ndarrays between
                                     processes using POSIX shared memory.
nester_sixsan (1.1.0)              - Para imprimir listas anidadas
nine (1.0.0)                       - Python 2 / 3 compatibility, like six, but favouring Python 3
python-ninethreesix (0.1.1)        - a password generator inspired by http://xkcd.com/936/
opendir (0.0.1)                    - Implements POSIX opendir
OSExtension (0.1.5)                - Extension for os module, for POSIX systems only
pdfminer.six (20170720)            - PDF parser and analyzer
pdftables.six (0.0.5)              - Parses PDFs and extracts what it believes to be tables.
plivo-six (0.11.5)                 - Plivo Python library
ploghandler (0.5.0)                - Provides concurrent rotating file handler for posix-compatible
                                     OSes.
plonetheme.solemnity (0.7)         - An installable theme for Plone 3.0 based on the solemnity theme
                                     by Six Shooter Media.
posix-spawn (0.2.post7)            - CFFI bindings to posix_spawn.
posix_ipc (1.0.0)                  - POSIX IPC primitives (semaphores, shared memory and message
                                     queues) for Python
posix_timers (0.1.3)               - Provides access to posix timers (clock_gettime etc.) from
                                     Python.
PosixTimeZone (0.9.4)              - datetime tzinfo class to hook into the OS timezone libraries
prego (0.20170123)                 - System test framework over POSIX shells
py3compat (0.4)                    - Small Python2/3 helpers to avoid depending on six.
pylibacl (0.5.3)                   - POSIX.1e ACLs for python
pymusixmatch (0.1)                 - Simple integrate of API musixmatch.com with python
PySixel (0.1.11)                   - View full-pixel color graphics on SIXEL-supported
                                     terminals(xterm/mlterm/DECterm/Reflection/RLogin/tanasinn/yaft)
qtsix (1.1)                        - Compatibility layer for different Qt bindings.
querycontacts (0.2.1)              - Query network abuse contacts on the command-line for a given ip
                                     address on abuse-contacts.abusix.org
rosixdocs (0.1.3)                  - Theme for Sphinx from Rosix projects.
shm (0.1)                          - A CPython extension module wrapping the POSIX shm_open and
                                     shm_unlink syscalls
SimpleTALSix (6.2.0.dev4)          - Stand alone Python implementation of the TAL, TALES and METAL
                                     specifications used in Zope to power HTML and XML templates.
six (1.11.0)                       - Python 2 and 3 compatibility utilities
  INSTALLED: 1.10.0
  LATEST:    1.11.0
sixelplot (0.0.3)                  - thin-wrapper for pysixel and matplotlib.
sixelterm (0.0.10)                 - Display JPEG/PNG image with cat command, on some terminals
                                     support SIXEL (RLogin/mlterm/tanasinn). Inspired by GateOne.
  INSTALLED: 1.28.0
  LATEST:    1.29.0
sixer (1.6)                        - Add Python 3 support to Python 2 applications using the six
                                     module.
sixfeetup.customfolderalert (1.3)  - Is there evil in your site? This product will let you know.
sixfeetup.workflow.chained (1.9)   - Override the state menu to show all states in the workflow chain
sixfoh (0.1.3)                     - Generates base sixfoh-encoded images for yer websites.
sixfour (1.3.3)                    - base64 Image Encoder and Embedder for HTML, CSS, Markdown, LESS,
                                     SASS
sixgill (0.2.4)                    - six-frame genome-inferred libraries for LC-MS/MS
sixieskel (5.4.6)                  - UNKNOWN
SixIsles (0.0.3)                   - PyMongo Based ActiveRecord Pattern O/R Mapper
sixoclock (0.1.0)                  - Simple personal backup tool
Sixpack (2.6.2)                    - A/B testing framework under active development at SeatGeek
sixs (1.0.2)                       - 6s Python wrappers
statedump (1.0a2)                  - A Python package helping to dump and restore posix state
                                     (user/group/permissions) of files.
stor (1.4.6)                       - Cross-compatible API for accessing Posix and OBS storage systems
Sublimescheme (1.0.7)              - Easily create a Sublime text Color Scheme with as little as six
                                     lines of code
SysExtension (0.1.2)               - Extension for sys module, for POSIX systems only
SystemEvent (0.9.0)                - System-wide Event synchonization for posix (emulating the
                                     threading.Event api)
tasix (0.0.1)                      - Tas-IX package
unittest2six (0.0.0)               - Meta-package for unittest2 functionality on both Python 2 and
                                     Python 3
whs.utils.pyman (0.9.0)            - Utility for easy creation of help POSIX man-like pages
xmlcmd (0.1.2)                     - half-baked support for adding --xml support to POSIX commands
'''

SEARCH_EXAMPLE_GARBAGE = '''
AASDFA~!@#$!@#
Some junk that cannot be parsed, but we do not crash the parser.
@#$!@34/1
'''


def test_pip_search_parser():
    pkg_rels_expected = PackageReleases(
        name='six',
        versions=('1.10.0', '1.11.0'),
    )

    parser = PipSearchParser(content=SEARCH_EXAMPLE_SIX)
    pkg_rels = parser.parse(package_name='six')

    assert pkg_rels_expected == pkg_rels


def test_pip_search_parser_garbage():
    parser = PipSearchParser(content=SEARCH_EXAMPLE_GARBAGE)
    parser.parse(package_name='six')  # does not raise
