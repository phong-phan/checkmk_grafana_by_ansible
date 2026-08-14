# Grafana Automation Playbooks

## A project to automate the deployment of Grafana and other actions related to dashboards

- Install latest Grafana server on AlmaLinux (RHEL-based), with optional HTTPS enforcement.
- Create a service account and API key for Ansible/automation to talk to Grafana.
- Install the CheckMK datasource plugin (and other plugins), from the internet or a local repo.
- Connect Grafana to CheckMK, either via basic auth or via the generated API key.
- Export/import dashboards between Grafana servers.
- Optional: LDAP/AD integration.

Install the Grafana collection for Ansible:

```bash
    ansible-galaxy collection install community.grafana
```

## Setup

Credentials are stored outside this repository on the Ansible control node, at:
```
/home/ansible/variables/vars_file.yml
```
See `sample_vars_files.yml` at the repo root for the full list of required keys (`grafana_user`,
`grafana_secret`, `grafana_viewer_user`, `grafana_viewer_secret`, `cmk_automation_user_secret`, ...).
`grafana_api_key` is written back into this same file automatically after running `grafana-api-creation.yml`.
Every playbook validates its required secrets via `commons/validate-vault-keys.yml` before doing anything else.

Non-secret, per-site configuration lives in:
```
sites/{{ customer_name }}/CM/{{ site }}/playbooks/GFN/site_vars.yml
```

## Structure:

```bash
├── dashboards                                   # Storing all JSON dashboard files
├── grafana-server-install.yml                   # Install Grafana Server (SSL, plugins, viewer user)
├── grafana-api-creation.yml                     # Create service account and API key
├── grafana-add-cmk-datasource.yml               # Create the CheckMK datasource using the Grafana API key
├── grafana-connection-creation.yml              # Create the CheckMK datasource using basic auth
├── grafana-ad-integration.yml                   # Configure LDAP/AD authentication in Grafana
├── grafana-dashboard-export.yml                 # Export all dashboards from another Grafana server
├── grafana-dashboard-import.yml                 # Import dashboards exported above into this Grafana server
├── grafana-dashboard-name-uid-get.yml           # Get all dashboards' Title and UID from another Grafana server
├── grafana-datasource-uid-get.yml               # Get UID of the CheckMK datasource
├── j2-template/                                 # Jinja2 templates used by the optional playbooks above
├── README.md

```
## Usage:
```bash
# Install Grafana Server
ansible-playbook grafana-server-install.yml
```

## Flow to import dashboards:

Install Grafana Server -> Export dashboards from another Grafana (assuming dashboards can be re-used) -> Change all the information needed (UID, site name, server name) -> Ansible service account creation and API key generation -> Add the CheckMK datasource -> Import edited dashboards into Grafana.
