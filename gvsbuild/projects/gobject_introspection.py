#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.

from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add
from gvsbuild.utils.simple_ui import log
from gvsbuild.utils.utils import python_find_libs_dir


@project_add
class GObjectIntrospection(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gobject-introspection",
            archive_url="https://download.gnome.org/sources/gobject-introspection/1.72/gobject-introspection-1.72.0.tar.xz",
            hash="02fe8e590861d88f83060dd39cda5ccaa60b2da1d21d0f95499301b186beaabc",
            dependencies=[
                "ninja",
                "meson",
                "msys2",
                "pkg-config",
                "glib",
            ],
            # https://gitlab.gnome.org/GNOME/gobject-introspection/-/issues/427
            patches=["incorrect-giscanner-path.patch"],
        )

    def build(self):
        # For finding gobject-introspection.pc
        self.builder.mod_env("PKG_CONFIG_PATH", ".")
        # For finding & using girepository.lib/.dll
        self.builder.mod_env("LIB", r".\girepository")
        self.builder.mod_env("PATH", r".\girepository")
        # For linking the _giscanner.pyd extension module when using a virtualenv
        py_dir = Project.get_tool_path("python")
        py_libs = python_find_libs_dir(py_dir)
        if py_libs:
            log.debug(f"Python library path is [{py_libs}]")
            self.builder.mod_env("LIB", py_libs, prepend=False)

        Meson.build(
            self,
            meson_params="-Dpython=%s\\python.exe -Dcairo_libname=cairo-gobject.dll"
            % (py_dir,),
        )
