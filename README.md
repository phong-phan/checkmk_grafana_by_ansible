# Checkmk and Grafana Automation

This repository contains Ansible playbooks for automating the installation and configuration of **Checkmk** and **Grafana**.

## Prerequisites

- An **ansible user** on your local machine or a dedicated control node.

## Configuration

### 1. Credentials

Create the credentials file at the following path:

```bash
/home/ansible/variables/vars_file.yml
```

This file will store all credentials required for the Checkmk and Grafana installation.

### 2. Inventory

Define your inventory file in the appropriate directory for the client environment:

```text
CORP/CM/{DEV/TEST/QA...}/
```

### 3. Site Variables

Configuration settings for Checkmk and Grafana are defined in:

```text
CORP/CM/DEV/playbooks/{CMK,GFN}/site_vars.yml
```

---

## Deployment Workflow

### Step 1: Server Installation & Setup

**Goal:** Install Checkmk and Grafana server, create users, folders, and add hosts to Checkmk.

1. Open `DEV-Monitoring.yml`.
2. **Uncomment** the first block (Server installation).
3. **Comment** the other blocks.
4. Run the deployment script:
   ```bash
   ./DEV-MONITORING.sh
   ```
5. After completion, **comment** the top Server block in `DEV-Monitoring.yml`.

### Step 2: Agent Installation

**Goal:** Install the Checkmk agent on the hosts listed in `cmk_monitored_hosts` (`site_vars.yml`).

The agent-install playbooks run as a single play that loops over `cmk_monitored_hosts` and uses
`delegate_to` to reach each host's IP, so they execute against the same host as the other steps
(e.g. `--limit CORP1_CMK`) — no separate inventory group or `--limit` override is needed here.

1. Open `DEV-Monitoring.yml`.
2. **Uncomment** the `Agent` block.
3. **Comment** the other blocks.
4. Run the deployment script:
   ```bash
   ./DEV-MONITORING.sh
   ```
5. After completion, **comment** the `Agent` block in `DEV-Monitoring.yml`.

### Step 3: Service Discovery & Activation

**Goal:** Run service discovery and activate changes to accept new data from all hosts.

1. Open `DEV-Monitoring.yml`.
2. **Uncomment** the last `Server` block (Service Discovery).
3. Open `DEV-MONITORING.sh`.
4. **Uncomment** the `Server` block.
5. Run the deployment script:
   ```bash
   ./DEV-MONITORING.sh
   ```

### Step 4: Verification

- Confirm that all new data and hosts have been correctly added to Checkmk.

### Optional playbooks

`DEV-Monitoring.yml` also has a commented-out block of optional playbooks you can uncomment and run
individually as needed: HTTPS enforcement, custom/built-in agent plugins, templated custom checks
(iLO health via Redfish, VMware snapshot summary), removing a host, and LDAP/AD integration for
both Checkmk and Grafana. See `services/checkmk/README.md` and `services/grafana/README.md` for details.
