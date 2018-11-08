#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os

class LibRdKafkaConan(ConanFile):
    name = "librdkafka"
    version = "0.11.6"
    description = "The Apache Kafka C/C++ client library"
    url = "https://github.com/raulbocanegra/librdkafka"
    homepage = "https://github.com/edenhill/librdkafka"
    license = "https://github.com/raulbocanegra/conan-librdkafka"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False], 
        "with_plugins": [True, False], 
        "with_sasl": [True, False], 
        "with_ssl":[True, False],
        "with_zlib": [True, False],
        "with_zstd": [True, False],
        "without_optimization": [True, False],
        "build_testing": [True, False],
        "build_examples": [True, False],
        "enable_devel": [True, False],
        "enable_refcnt_debug": [True, False],
        "enable_sharedptr_debug": [True, False]
    }
    default_options = "shared=False", "fPIC=True", "with_plugins=False", "with_sasl=False", "with_ssl=True", "with_zlib=True", "with_zstd=False", "without_optimization=False", "build_testing=False", "build_examples=False", "enable_devel=False", "enable_refcnt_debug=False", "enable_sharedptr_debug=False"

    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
        if self.settings.build_type == 'Release':
            self.options.enable_devel = False
            self.options.enable_refcnt_debug = False
            self.options.enable_sharedptr_debug = False
            self.options.build_examples = False

    def source(self):  
        source_url = "https://github.com/edenhill/librdkafka"
        tools.get("{0}/archive/v{1}.zip".format(source_url, self.version))
        extracted_dir = "librdkafka-" + self.version
        os.rename(extracted_dir, self.source_subfolder)        
        
    def configure_cmake(self):
        cmake = CMake(self)        
        cmake.definitions['ENABLE_DEVEL'] = "ON" if self.options.enable_devel else "OFF"
        cmake.definitions['ENABLE_REFCNT_DEBUG'] = "ON" if self.options.enable_refcnt_debug else "OFF"
        cmake.definitions['ENABLE_SHAREDPTR_DEBUG'] = "ON" if self.options.enable_sharedptr_debug else "OFF"
        cmake.definitions['RDKAFKA_BUILD_TESTS'] = "ON" if self.options.build_testing else "OFF"
        cmake.definitions['RDKAFKA_BUILD_EXAMPLES'] = "ON" if self.options.build_examples else "OFF"
        cmake.definitions['RDKAFKA_BUILD_STATIC'] = "ON" if not self.options.shared else "OFF"
        cmake.definitions['WITH_PLUGINS'] = "ON" if self.options.with_plugins else "OFF"
        cmake.definitions['WITH_SASL'] = "ON" if self.options.with_sasl else "OFF"
        cmake.definitions['WITH_SSL'] = "ON" if self.options.with_ssl else "OFF"
        cmake.definitions['WITH_ZLIB'] = "ON" if self.options.with_zlib else "OFF"
        cmake.definitions['WITH_ZSTD'] = "ON" if self.options.with_zstd else "OFF"
        cmake.definitions['WITHOUT_OPTIMIZATION'] = "ON" if self.options.without_optimization else "OFF"

        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def requirements(self):
        if self.options.with_zlib:
            self.requires("zlib/1.2.11@conan/stable")
        if self.options.with_ssl:
            self.requires("OpenSSL/1.1.0i@conan/stable")
        if self.options.with_zstd:
            self.requires("zstd/1.3.5@bincrafters/stable")
    
    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        
    def package(self):
        self.copy(pattern="LICENSE", dst="license", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()        

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows" and not self.options.shared:
            self.cpp_info.libs.append("crypt32")
            self.cpp_info.defines = ["LIBRDKAFKA_STATICLIB"]
        elif self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
