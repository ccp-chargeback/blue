# Copyright © 2026 CCP ehf.

import unittest


# Note that blue is imported by each test case rather than at module scope, as the blue module is
# mocked away while test cases are discovered and must not be touched at import time.


class TestBlueStatistics(unittest.TestCase):
    """
    A set of test cases for BlueStatistics.
    """

    def test_blueStatisticsTelemetryConfig(self):
        """
        Test access to the BlueStatisticsTelemetryConfig object.
        """
        import blue

        # Can we create an instance of it and populate its member attributes?
        config = blue.BlueStatisticsTelemetryConfig()
        config.applicationName = "test app"
        config.captureDuration = 42
        config.trackMemory = True

        # Does it have the expected attributes with the correct values?
        self.assertTrue(hasattr(config, "applicationName"))
        self.assertTrue(hasattr(config, "captureDuration"))
        self.assertTrue(hasattr(config, "trackMemory"))
        self.assertFalse(hasattr(config, "attributeDoesNotExist"))
        self.assertEqual(config.applicationName, "test app")
        self.assertEqual(config.captureDuration, 42)
        self.assertEqual(config.trackMemory, True)

    def test_registerTelemetryCategory(self):
        """
        Test registering a Telemetry category.
        """
        import blue

        testColor = blue.BlueTelemetryColor.Tomato

        category = blue.statistics.RegisterTelemetryCategory(
            "test category", testColor
        )

        self.assertEqual(category.name, "test category")
        self.assertEqual(category.color, testColor)

    def test_registerTelemetryCategoryWithColorObject(self):
        """
        Test that a category can be registered with the color of another category, and that the
        color it ends up with is the very same color it was registered with.
        """
        import blue

        first = blue.statistics.RegisterTelemetryCategory(
            "test category with a color", blue.BlueTelemetryColor.Tomato
        )
        second = blue.statistics.RegisterTelemetryCategory("test category sharing a color", first.color)

        self.assertEqual(second.color, first.color)
        self.assertEqual(second.color, blue.BlueTelemetryColor.Tomato)

    def test_registerTelemetryCategoryWithInvalidColor(self):
        """
        Test that a category cannot be registered with something that is not a color.
        """
        import blue

        with self.assertRaises(TypeError):
            blue.statistics.RegisterTelemetryCategory("test category with an invalid color", "Tomato")

        with self.assertRaises(TypeError):
            blue.statistics.RegisterTelemetryCategory("test category with a numeric color", 0xFF6347)

    def test_registerTelemetryCategoryTwice(self):
        """
        Test that registering an already registered category returns the existing one, keeping the
        color it was first registered with.
        """
        import blue

        first = blue.statistics.RegisterTelemetryCategory(
            "test category registered twice", blue.BlueTelemetryColor.Tomato
        )
        second = blue.statistics.RegisterTelemetryCategory(
            "test category registered twice", blue.BlueTelemetryColor.Teal
        )

        self.assertEqual(second.name, first.name)
        self.assertEqual(second.color, first.color)
        self.assertEqual(second.color, blue.BlueTelemetryColor.Tomato)

    def test_registerTelemetryCategoryWithoutName(self):
        """
        Test that a category without a name cannot be registered.
        """
        import blue

        with self.assertRaises(blue.TelemetryCategoryError):
            blue.statistics.RegisterTelemetryCategory("")

    def test_telemetryCategoryErrorIsARuntimeError(self):
        """
        Test that a category that cannot be registered can be caught as a RuntimeError.
        """
        import blue

        self.assertTrue(issubclass(blue.TelemetryCategoryError, RuntimeError))

        with self.assertRaises(RuntimeError):
            blue.statistics.RegisterTelemetryCategory("")

    def test_getRegisteredTelemetryCategories(self):
        """
        Test that the registered categories contain the built-in ones, the category registered by
        blue itself, and categories registered from Python.
        """
        import blue

        blue.statistics.RegisterTelemetryCategory("test category in category list")

        names = [category.name for category in blue.statistics.GetRegisteredTelemetryCategories()]

        self.assertIn("general", names)
        self.assertIn("cpp", names)
        self.assertIn("core", names)
        self.assertIn("blue", names)
        self.assertIn("test category in category list", names)
