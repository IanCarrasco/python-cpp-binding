"""Install script for setuptools."""

from distutils import sysconfig
import fnmatch
import os
import posixpath
import re
import shutil
import sys

import setuptools
from setuptools.command import build_ext

__version__ = '0.0.1'

PROJECT_NAME = 'mylib'

REQUIRED_PACKAGES = []

WORKSPACE_PYTHON_HEADERS_PATTERN = re.compile(
    r'(?<=path = ").*(?=",  # May be overwritten by setup\.py\.)')

IS_WINDOWS = sys.platform.startswith('win')

class BazelExtension(setuptools.Extension):
  """A C/C++ extension that is defined as a Bazel BUILD target."""
  def __init__(self, bazel_target):
    self.bazel_target = bazel_target
    self.relpath, self.target_name = (
        posixpath.relpath(bazel_target, '//').split(':'))
    ext_name = os.path.join(
        self.relpath.replace(posixpath.sep, os.path.sep), self.target_name)
    setuptools.Extension.__init__(self, ext_name, sources=[])


class BuildBazelExtension(build_ext.build_ext):
  """A command that runs Bazel to build a C/C++ extension."""
  def run(self):
    for ext in self.extensions:
      self.bazel_build(ext)
    build_ext.build_ext.run(self)

  def bazel_build(self, ext):
    with open('WORKSPACE', 'r') as f:
      workspace_contents = f.read()

    with open('WORKSPACE', 'w') as f:
      f.write(WORKSPACE_PYTHON_HEADERS_PATTERN.sub(
          sysconfig.get_python_inc().replace(os.path.sep, posixpath.sep),
          workspace_contents))

    if not os.path.exists(self.build_temp):
      os.makedirs(self.build_temp)

    # Specify Build Command
    bazel_argv = [
        'bazel',
        'build',
        ext.bazel_target,
        '--symlink_prefix=' + os.path.join(self.build_temp, 'bazel-'),
        '--compilation_mode=' + ('dbg' if self.debug else 'opt'),
    ]

    if IS_WINDOWS:
      for library_dir in self.library_dirs:
        bazel_argv.append('--linkopt=/LIBPATH:' + library_dir)

    # Start Bazel Build
    self.spawn(bazel_argv)

    shared_lib_suffix = '.dll' if IS_WINDOWS else '.so'

    # Copy binary to destination path
    ext_bazel_bin_path = os.path.join(
        self.build_temp, 'bazel-bin',
        ext.relpath, ext.target_name + shared_lib_suffix)
    ext_dest_path = self.get_ext_fullpath(ext.name)
    ext_dest_dir = os.path.dirname(ext_dest_path)
    if not os.path.exists(ext_dest_dir):
      os.makedirs(ext_dest_dir)
    shutil.copyfile(ext_bazel_bin_path, ext_dest_path)

setuptools.setup(
    name="mylib",
    version=__version__,
    ext_modules=[
        BazelExtension('//mylib/cc/python:_example'),
    ],
    cmdclass=dict(build_ext=BuildBazelExtension),
    packages=setuptools.find_packages(),
)