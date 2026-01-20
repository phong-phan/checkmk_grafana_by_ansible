# Grafana Automation Playbooks

## A project to automate the deployment of Grafana and other actions related to dashboards

- Install latest Grafana server on Alma Linux 9.4 (Seafoam Ocelet), current version is 11.6.0
- Install Grafana server
- Creating service account and API for Ansible to talk with Granfana
- Install CheckMK opensource plugin
- Connecting with CheckMK
- Import dashboards from another Grafana Server

Install Grafana module for ansible:

```bash
    ansible-galaxy collection install community.grafana
```

Information  need to bee added to Vault file /home/ansible/variables/vars_file.yml
    - customer_name:
    - site:
    - grafana_user: 
    - grafana_secret: 
    - grafana_api_key (This will be automatically added after running API gen playbook)

## Structure:

```bash
├── ansible_api_key.txt					                            # API key file
├── dashboards                                                      # Storing all JSON dashboard files 
│   ├── DTA-QA.json
│   ├── DTA-QA-Procs.json
│   ├── DTA-QA-SVCs.json
│   ├── DTA-STG.json
│   ├── DTA-STG-Procs.json
│   ├── DTA-STG-SVCs.json
│   └── grafana-dashboard-hostname-uid-update.yml                   # Run on localhost, Update information (uid, server name, site name) before importing to new Grafana server.
├── datasource_uid.txt					                            # UID of current CheckMK datasource
├── grafana-api-creation.yml                                        # Create Service account and API
├── grafana-connection-creation.yml		                            # Create new connection from CheckMK Datasource with authentication info from CheckMK
├── grafana-dashboard-export.yml		                            # Export all dashboards from another Grafana server to use for importing
├── grafana-dashboard-import.yml		                            # Import all dashboards from another Grafana server to use for importing
├── grafana-dashboard-name-uid-get.yml	                            # Get all dashboards Title and UID from another Grafana server to use for importing
├── grafana-dashboard-name-update.yml	                            # Update name of servers, site before importing dashboards
├── grafana-datasource-uid-get.yml                                  # Get UID of CheckMK datasource (tribe-29-checkmk-datasource)
├── grafana-server-install.yml                                      # Install Grafana Server
├── README.md

```
## Usage:
```bash
# Install Grafana Server
ansible-playbook grafana-server-install.yml
```

## Flow to import dashboard:

Install Grafana Server -> Export dashboards from another Grafana (assuming dashboards can be re-use) -> Change all the information needed  (UID, site name, server name) -> Ansible service account creation and API gen -> Add a new connection to CheckMK server using "tribe-29-checkmk-datasource" plugin ->  Import edited dashboards into Grafana.
