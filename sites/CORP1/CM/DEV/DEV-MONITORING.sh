# Install CheckMK Server
ansible-playbook playbooks/DEV-MONITORING.yml -i CORP1-inventory.yml --limit CORP1_CMK

# Install CheckMK Agent on all Linux hosts
# ansible-playbook playbooks/DEV-MONITORING.yml -i CORP1-inventory.yml --limit 'all:!CORP1_DC01:!CORP1_DC02' 