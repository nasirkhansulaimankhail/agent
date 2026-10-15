import unittest

from agent import builder, legacy_uploaded_builder, web


class TestWebBuilderImports(unittest.TestCase):
    def test_native_route_imports_the_native_builder(self):
        self.assertIs(web.ImageBuilder, builder.ImageBuilder)

    def test_upload_route_imports_the_legacy_upload_directory(self):
        self.assertIs(web.get_image_build_context_directory,
                      legacy_uploaded_builder.get_image_build_context_directory)
