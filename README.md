# Infrastructure Monitoring & Automated CI/CD Platform

## Overview

A hands-on DevOps project that combines Linux system monitoring, Bash automation, Python scripting, CI/CD, containerization, configuration management, and Infrastructure as Code.

The project demonstrates how infrastructure monitoring and operational tasks can be automated using commonly used DevOps tools.

## Architecture

```text
                 GitHub Repository
                        |
                        v
                   Jenkins CI
                        |
              +---------+---------+
              |                   |
         Install Python       Run Unit Tests
              |                   |
              +---------+---------+
                        |
                        v
              Python Monitoring App
                        |
              +---------+---------+
              |         |         |
             CPU      Memory     Disk
              |         |         |
              +---------+---------+
                        |
                        v
                 JSON Health Reports

Additional DevOps Components:

Bash       -> Linux operational automation
Docker     -> Application containerization
Ansible    -> Linux configuration management
Terraform  -> Infrastructure as Code demonstration
```

## Technology Stack

- **Operating System:** Ubuntu 24.04 on WSL2
- **Programming:** Python, Bash
- **Monitoring:** psutil
- **Version Control:** Git, GitHub
- **CI/CD:** Jenkins
- **Containerization:** Docker
- **Configuration Management:** Ansible
- **Infrastructure as Code:** Terraform

## Project Structure

```text
infrastructure-monitoring-ci-cd/
│
├── monitoring/
│   ├── config/
│   │   └── config.json
│   ├── logs/
│   ├── reports/
│   ├── monitor.py
│   └── requirements.txt
│
├── scripts/
│   ├── system_health.sh
│   ├── service_check.sh
│   └── cleanup_logs.sh
│
├── tests/
│   └── test_monitor.py
│
├── docker/
│   └── Dockerfile
│
├── jenkins/
│   └── Dockerfile
│
├── ansible/
│   └── site.yml
│
├── terraform/
│   ├── main.tf
│   └── .gitignore
│
├── Jenkinsfile
├── .dockerignore
└── README.md
```

## Implemented Features

### 1. Python Infrastructure Monitoring

- Collects CPU utilization, memory utilization, disk utilization, system uptime, and running process count using psutil.
- Evaluates CPU, memory, and disk usage against configurable thresholds.
- Identifies resource usage that reaches configured warning thresholds.
- Generates timestamped JSON health reports.
- Maintains application logs for troubleshooting.
- Supports continuous monitoring using a configurable interval.

### 2. Bash Automation

- System health information using Linux utilities.
- Linux service status checking using systemctl.
- Automated cleanup of old log files.
- Dry-run mode to preview cleanup operations before deletion.

### 3. Git and GitHub

- Version control using Git.
- Repository management and commit history.
- `.gitignore` configuration to exclude generated files and virtual environments.

### 4. Jenkins CI Pipeline

- GitHub repository checkout.
- Python virtual environment setup.
- Dependency installation.
- Automated unit test execution.
- Monitoring application execution.
- Pipeline success and failure handling.

### 5. Docker

- Created a Docker image for the monitoring application.
- Installed application dependencies inside the image.
- Used volume mounts to persist monitoring logs and reports.

### 6. Ansible

- Automated local Linux environment configuration.
- Installed Python virtual environment support.
- Created application directories.
- Deployed application and configuration files.
- Created a Python virtual environment and installed dependencies.

### 7. Terraform

- Implemented Infrastructure as Code using the Local provider.
- Provisioned a local file resource.
- Practiced initialization, validation, planning, applying, state inspection, and resource destruction.

## Configuration

Example `monitoring/config/config.json`:

```json
{
    "cpu_threshold": 80,
    "memory_threshold": 80,
    "disk_threshold": 85,
    "check_interval": 60
}
```

Thresholds can be adjusted without modifying the monitoring application source code.

## Run Locally

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd infrastructure-monitoring-ci-cd
```

Create a virtual environment:

```bash
cd monitoring
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run monitoring:

```bash
python monitor.py
```

Run continuous monitoring:

```bash
python monitor.py --watch
```

## Run Automated Tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

## Run Bash Scripts

```bash
./scripts/system_health.sh

./scripts/service_check.sh ssh

./scripts/cleanup_logs.sh monitoring/logs 7 --dry-run
```

Use `--delete` instead of `--dry-run` to perform the cleanup after reviewing the files.

## Run Using Docker

From the project root:

```bash
docker build -t infrastructure-monitor:1.0 -f docker/Dockerfile .
```

Run:

```bash
docker run --rm \
  -v "$(pwd)/monitoring/logs:/app/logs" \
  -v "$(pwd)/monitoring/reports:/app/reports" \
  infrastructure-monitor:1.0
```

## Ansible Deployment

Run the local playbook:

```bash
ansible-playbook -i localhost, ansible/site.yml --ask-become-pass
```

## Terraform Workflow

From the Terraform directory:

```bash
cd terraform

terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
terraform state list
terraform destroy
```

The Terraform demonstration uses the Local provider to provision a local file. It does not provision cloud or VMware infrastructure.

## Current Lab Scope and Limitations

- The environment is Ubuntu 24.04 running through WSL2 on Windows.
- Jenkins is running in a Docker container.
- The Jenkins pipeline is manually triggered; automatic GitHub push triggers are not configured yet.
- Ansible deployment is demonstrated locally, not across multiple remote servers.
- Terraform demonstrates local resource provisioning, not cloud or VMware provisioning.
- VMware ESXi and vCenter concepts are studied, but an enterprise VMware lab has not been configured.
- Dockerized monitoring reports container-level resource information and should not be interpreted as complete physical-host monitoring.

## Learning Outcomes

- Linux administration and troubleshooting.
- Python-based infrastructure monitoring.
- Bash scripting and operational automation.
- Git version control and repository management.
- Jenkins CI pipeline development.
- Docker image creation and container execution.
- Ansible playbook development.
- Terraform fundamentals and Infrastructure as Code.

---

**Project Status:** Local DevOps lab implemented and tested across the components described above, subject to the scope and limitations documented here.
