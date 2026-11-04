import psutil
import json
import logging
import os
import time
import argparse

from datetime import datetime, timezone


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(
    BASE_DIR, "config", "config.json"
)

LOG_DIR = os.path.join(BASE_DIR, "logs")
REPORT_DIR = os.path.join(BASE_DIR, "reports")


os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


logging.basicConfig(
    filename=os.path.join(LOG_DIR, "monitor.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


def load_config():

    with open(CONFIG_PATH, "r") as file:
        return json.load(file)


def collect_metrics():

    cpu = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()

    disk = psutil.disk_usage("/")

    uptime = time.time() - psutil.boot_time()

    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "username"]
    ):
        try:
            processes.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return {
        "cpu_usage": cpu,
        "memory_usage": memory.percent,
        "disk_usage": disk.percent,
        "uptime_seconds": int(uptime),
        "running_processes": len(processes)
    }


def evaluate_health(metrics, config):

    checks = {
        "cpu": (
            metrics["cpu_usage"],
            config["cpu_threshold"]
        ),
        "memory": (
            metrics["memory_usage"],
            config["memory_threshold"]
        ),
        "disk": (
            metrics["disk_usage"],
            config["disk_threshold"]
        )
    }

    results = {}

    for name, values in checks.items():

        current, threshold = values

        status = (
            "WARNING"
            if current >= threshold
            else "HEALTHY"
        )

        results[name] = {
            "usage": current,
            "threshold": threshold,
            "status": status
        }

    overall_status = (
        "WARNING"
        if any(
            item["status"] == "WARNING"
            for item in results.values()
        )
        else "HEALTHY"
    )

    return overall_status, results


def generate_report(metrics, health):

    report = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "overall_status": health[0],

        "metrics": metrics,

        "health_checks": health[1]
    }

    filename = datetime.now(
        timezone.utc
    ).strftime("report_%Y%m%d_%H%M%S.json")

    report_path = os.path.join(
        REPORT_DIR, filename
    )

    with open(report_path, "w") as file:
        json.dump(report, file, indent=4)

    return report_path


def monitor():

    config = load_config()

    metrics = collect_metrics()

    health = evaluate_health(metrics, config)

    report_path = generate_report(metrics, health)

    print("\n===== INFRASTRUCTURE HEALTH REPORT =====")

    print(f"CPU Usage: {metrics['cpu_usage']}%")

    print(f"Memory Usage: {metrics['memory_usage']}%")

    print(f"Disk Usage: {metrics['disk_usage']}%")

    print(f"Uptime: {metrics['uptime_seconds']} seconds")

    print(
        f"Running Processes: "
        f"{metrics['running_processes']}"
    )

    print(f"\nOverall Status: {health[0]}")

    print(f"Report saved: {report_path}")

    logging.info(
        "Monitoring completed. Status: %s",
        health[0]
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--watch",
        action="store_true",
        help="Run monitoring continuously"
    )

    args = parser.parse_args()

    if args.watch:

        config = load_config()

        while True:
            try:
                monitor()
            except Exception:
                logging.exception("Monitoring failed")

            time.sleep(config["check_interval"])

    else:

        try:
            monitor()
        except Exception:
            logging.exception("Monitoring failed")
            raise
