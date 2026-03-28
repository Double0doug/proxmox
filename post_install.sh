#!/bin/bash
# PVE-01 Optimization Script for Ryzen 5700G / 64GB RAM

echo "Starting Post-Install Optimizations..."

# 1. Fix Repositories
sed -i 's/^deb/#deb/' /etc/apt/sources.list.d/pve-enterprise.list
echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list

# 2. Remove Subscription Nag
sed -Ezi.bak "s/(function ?\(orig_cmd\) \{)/\1\n\torig_cmd\(\);\n\treturn;/g" /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js
systemctl restart pveproxy.service

# 3. Set CPU Performance Governor
echo "performance" | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# 4. Limit ZFS ARC to 16GB
echo "options zfs zfs_arc_max=17179869184" > /etc/modprobe.d/zfs.conf
update-initramfs -u

echo "Done! Please reboot to apply ZFS changes."