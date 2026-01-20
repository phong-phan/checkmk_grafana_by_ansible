# Install CheckMK Server
ansible-playbook playbooks/DEV-Monitoring.yml -i CORP2-inventory.yml --limit CORP2_CMK

# Install CheckMK Agent on all Linux hosts
# ansible-playbook playbooks/DEV-Monitoring.yml -i CORP2-inventory.yml --limit 'all:!CORP2_DC01:!CORP2_DC02' 
