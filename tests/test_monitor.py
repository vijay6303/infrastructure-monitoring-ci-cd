import sys
import os
import unittest

# Make monitoring/ available for importing monitor.py
sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "monitoring")
)

from monitor import evaluate_health


class TestInfrastructureMonitoring(unittest.TestCase):

    def setUp(self):
        self.config = {
            "cpu_threshold": 80,
            "memory_threshold": 80,
            "disk_threshold": 85
        }

    def test_all_resources_healthy(self):
        metrics = {
            "cpu_usage": 40,
            "memory_usage": 50,
            "disk_usage": 60
        }

        status, checks = evaluate_health(metrics, self.config)

        self.assertEqual(status, "HEALTHY")

    def test_cpu_threshold_exceeded(self):
        metrics = {
            "cpu_usage": 95,
            "memory_usage": 50,
            "disk_usage": 60
        }

        status, checks = evaluate_health(metrics, self.config)

        self.assertEqual(status, "WARNING")
        self.assertEqual(checks["cpu"]["status"], "WARNING")

    def test_memory_threshold_exceeded(self):
        metrics = {
            "cpu_usage": 40,
            "memory_usage": 90,
            "disk_usage": 60
        }

        status, checks = evaluate_health(metrics, self.config)

        self.assertEqual(status, "WARNING")
        self.assertEqual(checks["memory"]["status"], "WARNING")

    def test_disk_threshold_exceeded(self):
        metrics = {
            "cpu_usage": 40,
            "memory_usage": 50,
            "disk_usage": 95
        }

        status, checks = evaluate_health(metrics, self.config)

        self.assertEqual(status, "WARNING")
        self.assertEqual(checks["disk"]["status"], "WARNING")


if __name__ == "__main__":
    unittest.main()
