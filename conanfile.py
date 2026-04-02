from conan import ConanFile
from conan.tools.cmake import cmake_layout, CMakeToolchain

class Uvs(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"

    qt_version = "6.8.3"

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires(f"qt/{self.qt_version}")
        self.requires("openssl/3.6.1")

    def configure(self):
        self.options["qt"].shared = True
        self.options["qt"].gui = True
        self.options["qt"].widgets = True
        self.options["qt"].with_sqlite3 = False
        self.options['qt'].qttools = True
        self.options["qt"].with_pq = False
        self.options["qt"].with_brotli = False
        self.options["qt"].with_openal = False
        self.options["qt"].with_md4c = False
        self.options["qt"].openssl = False
        self.options["qt"].qtquickcontrols = True
        self.options["qt"].qtshadertools = True
        self.options["qt"].qtdeclarative = True
        self.options["qt"].qtmultimedia = True

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

