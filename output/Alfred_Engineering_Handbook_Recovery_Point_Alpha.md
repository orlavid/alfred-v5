# Executive Summary

Generated: 2026-06-30T21:41:58.616512


## Purpose

This handbook documents Alfred Executive Operating System at Recovery Point Alpha. It is generated from collected engineering evidence and is intended to support rebuild, recovery, extension and onboarding.

## System Role

Alfred is an evidence-first executive operating system. It combines a human-readable Obsidian vault, deterministic routing, semantic retrieval, background enrichment, Telegram access and ChatGPT reasoning.

## Core Architecture

```text
Obsidian Vault
    ↓
Hermes / Second Brain enrichment and deterministic workflows
    ↓
Alfred Router and quality gates
    ↓
LlamaIndex evidence retrieval where required
    ↓
ChatGPT / OpenRouter reasoning path depending on interface
    ↓
Executive response
```

## Current Recovery State

Recovery Point Alpha preserves the restored platform, router, Telegram path, LlamaIndex evidence engine, Cloudflare routing and engineering evidence pack.

## Engineering Principle

The system should be evolved by preserving known-good components and making the smallest safe change that advances the current phase.

---

# System Platform

Generated: 2026-06-30T21:41:58.616526


## Purpose

Defines the VPS operating environment that hosts Alfred.

## Responsibilities

- Run Alfred services and timers.
- Provide network, Docker, Python and systemd runtime support.
- Expose required local ports for Cloudflare and internal services.

## Inputs

- Systemd services
- Timers
- Cron
- Listening ports

## Outputs

- Available runtime services
- Operational logs
- Health status

## Dependencies

- Ubuntu/Linux
- systemd
- Python
- Docker
- cloudflared

## Failure Modes

- Service stopped or disabled.
- Wrong local port exposed.
- Timer or cron job missing.
- Disk space exhaustion.

## Recovery Procedure

- Check systemctl status for affected services.
- Check listening ports with ss -ltnp.
- Review journalctl logs.
- Restore from Recovery Point Alpha if configuration drift is suspected.

## Source Evidence

### system/services.txt

Size: 22280 bytes

```text
  UNIT                                           LOAD      ACTIVE   SUB     DESCRIPTION
  alfred-bridge-v2.service                       loaded    inactive dead    Alfred Read-Only Intelligence Bridge
  alfred-overnight-batch.service                 loaded    inactive dead    Alfred Overnight Intelligence Batch
● alfred-retrieval-daily.service                 loaded    failed   failed  Alfred daily retrieval reliability health check
● alfred-retrieval-weekly.service                loaded    failed   failed  Alfred weekly full retrieval reliability test
  alfred-semantic-search.service                 loaded    inactive dead    Alfred Semantic Search Warm Server
  alfred-v2-overnight.service                    loaded    inactive dead    Alfred v2 nightly overnight batch (insight generation -> morning brief)
  alfred-v2-prod.service                         loaded    inactive dead    Alfred v2 (production)
  alfred-v2.service                              loaded    active   running Alfred v2 - Executive Operating System (FastAPI/uvicorn)
● alfred-v3-harness.service                      loaded    failed   failed  Alfred V3 Retrieval Harness
  apparmor.service                               loaded    active   exited  Load AppArmor profiles
  apport-autoreport.service                      loaded    inactive dead    Process error reports when automatic reporting is enabled
  apport.service                                 loaded    active   exited  automatic crash report generation
  apt-daily-upgrade.service                      loaded    inactive dead    Daily apt upgrade and clean activities
  apt-daily.service                              loaded    inactive dead    Daily apt download activities
● auditd.service                                 not-found inactive dead    auditd.service
  blk-availability.service                       loaded    active   exited  Availability of block devices
  cloud-config.service                           loaded    active   exited  Apply the settings specified in cloud-config
  cloud-final.service                            loaded    active   exited  Execute cloud user/final scripts
  cloud-init-hotplugd.service                    loaded    inactive dead    cloud-init hotplug hook daemon
  cloud-init-local.service                       loaded    active   exited  Initial cloud-init job (pre-networking)
  cloud-init.service                             loaded    active   exited  Initial cloud-init job (metadata service crawler)
  cloudflared.service                            loaded    active   running cloudflared
● connman.service                                not-found inactive dead    connman.service
● console-screen.service                         not-found inactive dead    console-screen.service
  console-setup.service                          loaded    active   exited  Set console font and keymap
  containerd.service                             loaded    active   running containerd container runtime
  cron.service                                   loaded    active   running Regular background program processing daemon
  dbus.service                                   loaded    active   running D-Bus System Message Bus
● display-manager.service                        not-found inactive dead    display-manager.service
  dm-event.service                               loaded    inactive dead    Device-mapper event daemon
  dmesg.service                                  loaded    inactive dead    Save initial kernel messages after boot
  docker.service                                 loaded    active   running Docker Application Container Engine
  dpkg-db-backup.service                         loaded    inactive dead    Daily dpkg database backup service
  e2scrub_all.service                            loaded    inactive dead    Online ext4 Metadata Check for All Filesystems
  e2scrub_reap.service                           loaded    inactive dead    Remove Stale Online ext4 Metadata Check Snapshots
  emergency.service                              loaded    inactive dead    Emergency Shell
  fail2ban.service                               loaded    active   running Fail2Ban Service
● fcoe.service                                   not-found inactive dead    fcoe.service
  finalrd.service                                loaded    active   exited  Create final runtime dir for shutdown pivot root
● firewalld.service                              not-found inactive dead    firewalld.service
  fstrim.service                                 loaded    inactive dead    Discard unused blocks on filesystems from /etc/fstab
  fwupd-refresh.service                          loaded    inactive dead    Refresh fwupd metadata and update motd
  getty-static.service                           loaded    inactive dead    getty on tty2-tty6 if dbus and logind are not available
  getty@tty1.service                             loaded    active   running Getty on tty1
  grub-common.service                            loaded    inactive dead    Record successful boot for GRUB
  grub-initrd-fallback.service                   loaded    inactive dead    GRUB failed boot detection
● hermes-5am-check.service                       loaded    failed   failed  Hermes 5am Self Check and Self Heal
  hermes-human-action-queue.service              loaded    active   running Hermes Human Action Queue Dashboard
  hermes-knowledge-api.service                   loaded    active   running Hermes Knowledge API read-only vault service
  hermes-semantic-reindex.service                loaded    inactive dead    Hermes Semantic Vault Reindex
  hermes-semantic.service                        loaded    active   running Hermes Persistent Semantic Search Service
  hermes-telegram.service                        loaded    active   running Hermes Telegram Bot
  hermes-trading-control-panel.service           loaded    active   running Hermes Trading Local Control Panel
  hermes-vps-backup.service                      loaded    inactive dead    Backup Hermes VPS configuration and runtime state
● hv_kvp_daemon.service                          not-found inactive dead    hv_kvp_daemon.service
  initrd-cleanup.service                         loaded    inactive dead    Cleaning Up and Shutting Down Daemons
  initrd-parse-etc.service                       loaded    inactive dead    Mountpoints Configured in the Real Root
  initrd-switch-root.service                     loaded    inactive dead    Switch Root
  initrd-udevadm-cleanup-db.service              loaded    inactive dead    Cleanup udev Database
● ip6tables.service                              not-found inactive dead    ip6tables.service
● ipset.service                                  not-found inactive dead    ipset.service
● iptables.service                               not-found inactive dead    iptables.service
● iscsi-shutdown.service                         not-found inactive dead    iscsi-shutdown.service
  iscsid.service                                 loaded    inactive dead    iSCSI initiator daemon (iscsid)
● kbd.service                                    not-found inactive dead    kbd.service
  keyboard-setup.service                         loaded    active   exited  Set the console keyboard layout
  kmod-static-nodes.service                      loaded    active   exited  Create List of Static Device Nodes
  ldconfig.service                               loaded    inactive dead    Rebuild Dynamic Linker Cache
  logrotate.service                              loaded    inactive dead    Rotate log files
● lvm2-activation-early.service                  not-found inactive dead    lvm2-activation-early.service
  lvm2-lvmpolld.service                          loaded    inactive dead    LVM2 poll daemon
  lvm2-monitor.service                           loaded    active   exited  Monitoring of LVM2 mirrors, snapshots etc. using dmeventd or progress polling
  man-db.service                                 loaded    inactive dead    Daily man-db regeneration
  ModemManager.service                           loaded    active   running Modem Manager
  modprobe@configfs.service                      loaded    inactive dead    Load Kernel Module configfs
  modprobe@dm_mod.service                        loaded    inactive dead    Load Kernel Module dm_mod
  modprobe@drm.service                           loaded    inactive dead    Load Kernel Module drm
  modprobe@efi_pstore.service                    loaded    inactive dead    Load Kernel Module efi_pstore
  modprobe@fuse.service                          loaded    inactive dead    Load Kernel Module fuse
  modprobe@loop.service                          loaded    inactive dead    Load Kernel Module loop
  monarx-agent.service                           loaded    active   running Monarx Agent - Security Scanner
  motd-news.service                              loaded    inactive dead    Message of the Day
  multipathd.service                             loaded    active   running Device-Mapper Multipath Device Controller
  netplan-ovs-cleanup.service                    loaded    inactive dead    OpenVSwitch configuration for cleanup
  networkd-dispatcher.service                    loaded    inactive dead    Dispatcher daemon for systemd-networkd
● networking.service                             not-found inactive dead    networking.service
● NetworkManager.service                         not-found inactive dead    NetworkManager.service
  nftables.service                               loaded    inactive dead    nftables
  nginx.service                                  loaded    active   running A high performance web server and a reverse proxy server
  obsidian-headless-sync-restart.service         loaded    inactive dead    Restart Obsidian Headless Sync
  obsidian-headless-sync.service                 loaded    active   exited  Obsidian Headless Sync for Hermes Vault
  obsidian-sync.service                          loaded    active   running Obsidian Headless Sync for Hermes Vault
  ollama.service                                 loaded    active   running Ollama Service
  open-iscsi.service                             loaded    inactive dead    Login to default iSCSI targets
  open-vm-tools.service                          loaded    inactive dead    Service for virtual machines hosted on VMware
● ovsdb-server.service                           not-found inactive dead    ovsdb-server.service
  plymouth-quit-wait.service                     loaded    active   exited  Hold until boot process finishes up
  plymouth-quit.service                          loaded    active   exited  Terminate Plymouth Boot Screen
  plymouth-read-write.service                    loaded    active   exited  Tell Plymouth To Write Out Runtime Data
  plymouth-start.service                         loaded    inactive dead    Show Plymouth Boot Screen
  plymouth-switch-root.service                   loaded    inactive dead    Plymouth switch root service
  polkit.service                                 loaded    active   running Authorization Manager
  pollinate.service                              loaded    inactive dead    Pollinate to seed the pseudo random number generator
  qemu-guest-agent.service                       loaded    active   running QEMU Guest Agent
● rbdmap.service                                 not-found inactive dead    rbdmap.service
  rc-local.service                               loaded    inactive dead    /etc/rc.local Compatibility
  rescue.service                                 loaded    inactive dead    Rescue Shell
  rsyslog.service                                loaded    active   running System Logging Service
  second-brain-gui.service                       loaded    active   running Alfred Classic / Second Brain GUI
  secureboot-db.service                          loaded    inactive dead    Secure Boot updates for DB and DBX
  serial-getty@ttyS0.service                     loaded    active   running Serial Getty on ttyS0
  setvtrgb.service                               loaded    active   exited  Set console scheme
  snap.docker.dockerd.service                    loaded    active   running Service for snap application docker.dockerd
  snap.docker.nvidia-container-toolkit.service   loaded    inactive dead    Service for snap application docker.nvidia-container-toolkit
  snapd.apparmor.service                         loaded    active   exited  Load AppArmor profiles managed internally by snapd
  snapd.autoimport.service                       loaded    inactive dead    Auto import assertions from block devices
  snapd.core-fixup.service                       loaded    inactive dead    Automatically repair incorrect owner/permissions on core devices
  snapd.failure.service                          loaded    inactive dead    Failure handling of the snapd snap
  snapd.recovery-chooser-trigger.service         loaded    inactive dead    Wait for the Ubuntu Core chooser trigger
  snapd.seeded.service                           loaded    active   exited  Wait until snapd is fully seeded
  snapd.service                                  loaded    active   running Snap Daemon
  snapd.snap-repair.service                      loaded    inactive dead    Automatically fetch and run repair assertions
  snapd.system-shutdown.service                  loaded    inactive dead    Ubuntu core (all-snaps) system shutdown helper setup service
  ssh.service                                    loaded    active   running OpenBSD Secure Shell server
● sshd-keygen.service                            not-found inactive dead    sshd-keygen.service
● sshd.service                                   not-found inactive dead    sshd.service
  sysstat-collect.service                        loaded    inactive dead    system activity accounting tool
  sysstat-summary.service                        loaded    inactive dead    Generate a daily summary of process accounting
  sysstat.service                                loaded    active   exited  Resets System Activity Logs
  systemd-ask-password-console.service           loaded    inactive dead    Dispatch Password Requests to Console
  systemd-ask-password-plymouth.service          loaded    inactive dead    Forward Password Requests to Plymouth
  systemd-ask-password-wall.service              loaded    inactive dead    Forward Password Requests to Wall
  systemd-battery-check.service                  loaded    inactive dead    Check battery level during early boot
  systemd-binfmt.service                         loaded    active   exited  Set Up Additional Binary Formats
  systemd-bsod.service                           loaded    inactive dead    Displays emergency message in full screen.
  systemd-firstboot.service                      loaded    inactive dead    First Boot Wizard
  systemd-fsck-root.service                      loaded    inactive dead    File System Check on Root Device
  systemd-fsck@dev-disk-by\x2dlabel-BOOT.service loaded    active   exited  File System Check on /dev/disk/by-label/BOOT
  systemd-fsck@dev-disk-by\x2dlabel-UEFI.service loaded    active   exited  File System Check on /dev/disk/by-label/UEFI
  systemd-fsckd.service                          loaded    inactive dead    File System Check Daemon to report status
  systemd-hibernate-resume.service               loaded    inactive dead    Resume from hibernation
  systemd-hibernate.service                      loaded    inactive dead    System Hibernate
  systemd-hwdb-update.service                    loaded    inactive dead    Rebuild Hardware Database
  systemd-hybrid-sleep.service                   loaded    inactive dead    System Hybrid Suspend+Hibernate
  systemd-initctl.service                        loaded    inactive dead    initctl Compatibility Daemon
  systemd-journal-catalog-update.service         loaded    inactive dead    Rebuild Journal Catalog
  systemd-journal-flush.service                  loaded    active   exited  Flush Journal to Persistent Storage
  systemd-journald.service                       loaded    active   running Journal Service
  systemd-logind.service                         loaded    active   running User Login Management
  systemd-machine-id-commit.service              loaded    inactive dead    Commit a transient machine-id on disk
  systemd-modules-load.service                   loaded    active   exited  Load Kernel Modules
  systemd-networkd-wait-online.service           loaded    active   exited  Wait for Network to be Configured
  systemd-networkd.service                       loaded    active   running Network Configuration
● systemd-oomd.service                           not-found inactive dead    systemd-oomd.service
  systemd-pcrmachine.service                     loaded    inactive dead    TPM2 PCR Machine ID Measurement
  systemd-pcrphase-initrd.service                loaded    inactive dead    TPM2 PCR Barrier (initrd)
  systemd-pcrphase-sysinit.service               loaded    inactive dead    TPM2 PCR Barrier (Initialization)
  systemd-pcrphase.service                       loaded    inactive dead    TPM2 PCR Barrier (User)
  systemd-pstore.service                         loaded    inactive dead    Platform Persistent Storage Archival
  systemd-quotacheck.service                     loaded    inactive dead    File System Quota Check
  systemd-random-seed.service                    loaded    active   exited  Load/Save OS Random Seed
  systemd-remount-fs.service                     loaded    active   exited  Remount Root and Kernel File Systems
  systemd-repart.service                         loaded    inactive dead    Repartition Root Disk
  systemd-resolved.service                       loaded    active   running Network Name Resolution
  systemd-rfkill.service                         loaded    inactive dead    Load/Save RF Kill Switch Status
  systemd-soft-reboot.service                    loaded    inactive dead    Reboot System Userspace
  systemd-suspend-then-hibernate.service         loaded    inactive dead    System Suspend then Hibernate
  systemd-suspend.service                        loaded    inactive dead    System Suspend
  systemd-sysctl.service                         loaded    active   exited  Apply Kernel Variables
  systemd-sysext.service                         loaded    inactive dead    Merge System Extension Images into /usr/ and /opt/
  systemd-sysusers.service                       loaded    inactive dead    Create System Users
  systemd-timesyncd.service                      loaded    active   running Network Time Synchronization
  systemd-tmpfiles-clean.service                 loaded    inactive dead    Cleanup of Temporary Directories
  systemd-tmpfiles-setup-dev-early.service       loaded    active   exited  Create Static Device Nodes in /dev gracefully
  systemd-tmpfiles-setup-dev.service             loaded    active   exited  Create Static Device Nodes in /dev
  systemd-tmpfiles-setup.service                 loaded    active   exited  Create Volatile Files and Directories
  systemd-tpm2-setup-early.service               loaded    inactive dead    TPM2 SRK Setup (Early)
  systemd-tpm2-setup.service                     loaded    inactive dead    TPM2 SRK Setup
  systemd-udev-settle.service                    loaded    inactive dead    Wait for udev To Complete Device Initialization
  systemd-udev-trigger.service                   loaded    active   exited  Coldplug All udev Devices
  systemd-udevd.service                          loaded    active   running Rule-based Manager for Device Events and Files
  systemd-update-done.service                    loaded    inactive dead    Update is Completed
  systemd-update-utmp-runlevel.service           loaded    inactive dead    Record Runlevel Change in UTMP
  systemd-update-utmp.service                    loaded    active   exited  Record System Boot/Shutdown in UTMP
  systemd-user-sessions.service                  loaded    active   exited  Permit User Sessions
● systemd-vconsole-setup.service                 not-found inactive dead    systemd-vconsole-setup.service
  tpm-udev.service                               loaded    inactive dead    Handle dynamically added tpm devices
● ua-auto-attach.service                         not-found inactive dead    ua-auto-attach.service
  ua-reboot-cmds.service                         loaded    inactive dead    Ubuntu Pro reboot cmds
  ua-timer.service                               loaded    inactive dead    Ubuntu Pro Timer for running repeated jobs
● ubuntu-advantage-cloud-id-shim.service         not-found inactive dead    ubuntu-advantage-cloud-id-shim.service
  ubuntu-advantage.service                       loaded    inactive dead    Ubuntu Pro Background Auto Attach
  udisks2.service                                loaded    active   running Disk Manager
  ufw.service                                    loaded    active   exited  Uncomplicated firewall
  unattended-upgrades.service                    loaded    active   running Unattended Upgrades Shutdown
  update-notifier-download.service               loaded    inactive dead    Download data for packages that failed at package install time
  update-notifier-motd.service                   loaded    inactive dead    Check to see whether there is a new version of Ubuntu available
  user-runtime-dir@0.service                     loaded    active   exited  User Runtime Directory /run/user/0
  user@0.service                                 loaded    active   running User Manager for UID 0
  uuidd.service                                  loaded    inactive dead    Daemon for generating UUIDs
  vgauth.service                                 loaded    inactive dead    Authentication service for virtual machines hosted on VMware
● zfs-mount.service                              not-found inactive dead    zfs-mount.service

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

202 loaded units listed.
To show all installed unit files use 'systemctl list-unit-files'.

```

### system/timers.txt

Size: 3648 bytes

```text
NEXT                            LEFT LAST                              PASSED UNIT                                 ACTIVATES
Sun 2026-06-28 22:20:00 IST 2min 55s Sun 2026-06-28 22:10:03 IST     7min ago sysstat-collect.timer                sysstat-collect.service
Sun 2026-06-28 23:08:45 IST    51min Sun 2026-06-28 22:11:54 IST     5min ago fwupd-refresh.timer                  fwupd-refresh.service
Sun 2026-06-28 23:39:15 IST 1h 22min Sat 2026-06-27 23:39:15 IST      22h ago update-notifier-download.timer       update-notifier-download.service
Sun 2026-06-28 23:49:15 IST 1h 32min Sat 2026-06-27 23:49:15 IST      22h ago systemd-tmpfiles-clean.timer         systemd-tmpfiles-clean.service
Mon 2026-06-29 00:00:00 IST 1h 42min Sun 2026-06-28 00:00:03 IST      22h ago dpkg-db-backup.timer                 dpkg-db-backup.service
Mon 2026-06-29 00:00:00 IST 1h 42min Sun 2026-06-28 00:00:03 IST      22h ago logrotate.timer                      logrotate.service
Mon 2026-06-29 00:02:07 IST 1h 45min Mon 2026-06-22 00:57:48 IST            - fstrim.timer                         fstrim.service
Mon 2026-06-29 00:07:00 IST 1h 49min Sun 2026-06-28 00:07:03 IST      22h ago sysstat-summary.timer                sysstat-summary.service
Mon 2026-06-29 02:00:00 IST 3h 42min Sun 2026-06-28 02:00:03 IST      20h ago alfred-overnight-batch.timer         alfred-overnight-batch.service
Mon 2026-06-29 02:00:00 IST 3h 42min Sun 2026-06-28 02:00:03 IST      20h ago alfred-v2-overnight.timer            alfred-v2-overnight.service
Mon 2026-06-29 05:00:00 IST       6h Sun 2026-06-28 05:00:03 IST      17h ago hermes-5am-check.timer               hermes-5am-check.service
Mon 2026-06-29 05:25:00 IST       7h Sun 2026-06-28 05:25:03 IST      16h ago obsidian-headless-sync-restart.timer obsidian-headless-sync-restart.service
Mon 2026-06-29 05:30:00 IST       7h Sun 2026-06-28 05:30:03 IST      16h ago hermes-vps-backup.timer              hermes-vps-backup.service
Mon 2026-06-29 05:40:00 IST       7h Sun 2026-06-28 05:40:03 IST      16h ago hermes-semantic-reindex.timer        hermes-semantic-reindex.service
Mon 2026-06-29 06:19:14 IST       8h Sun 2026-06-28 06:18:35 IST      15h ago alfred-retrieval-daily.timer         alfred-retrieval-daily.service
Mon 2026-06-29 06:34:40 IST       8h Sun 2026-06-28 06:29:56 IST      15h ago apt-daily-upgrade.timer              apt-daily-upgrade.service
Mon 2026-06-29 08:21:04 IST      10h Sun 2026-06-28 01:23:03 IST      20h ago man-db.timer                         man-db.service
Mon 2026-06-29 11:30:21 IST      13h Sun 2026-06-28 15:37:15 IST       6h ago motd-news.timer                      motd-news.service
Mon 2026-06-29 14:28:29 IST      16h Sun 2026-06-28 20:49:24 IST 1h 27min ago apt-daily.timer                      apt-daily.service
Sat 2026-07-04 13:32:37 IST   5 days Wed 2026-06-24 20:51:07 IST            - update-notifier-motd.timer           update-notifier-motd.service
Sun 2026-07-05 03:10:57 IST   6 days Sun 2026-06-28 03:10:25 IST      19h ago e2scrub_all.timer                    e2scrub_all.service
Sun 2026-07-05 07:07:02 IST   6 days Sun 2026-06-28 07:02:56 IST      15h ago alfred-retrieval-weekly.timer        alfred-retrieval-weekly.service
-                                  - -                                      - apport-autoreport.timer              apport-autoreport.service
-                                  - -                                      - snapd.snap-repair.timer              snapd.snap-repair.service
-                                  - -                                      - ua-timer.timer                       ua-timer.service

25 timers listed.

```

### system/listening_ports.txt

Size: 2856 bytes

```text
State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess                                                                      
LISTEN 0      128        127.0.0.1:40241      0.0.0.0:*    users:(("code-7e7950df89",pid=4471,fd=11))                                  
LISTEN 0      4096       127.0.0.1:11434      0.0.0.0:*    users:(("ollama",pid=732,fd=4))                                             
LISTEN 0      4096      127.0.0.54:53         0.0.0.0:*    users:(("systemd-resolve",pid=543,fd=17))                                   
LISTEN 0      4096       127.0.0.1:20241      0.0.0.0:*    users:(("cloudflared",pid=12879,fd=9))                                      
LISTEN 0      4096       127.0.0.1:65529      0.0.0.0:*    users:(("monarx-agent",pid=746,fd=11))                                      
LISTEN 0      5          127.0.0.1:8091       0.0.0.0:*    users:(("python3",pid=728,fd=3))                                            
LISTEN 0      5          127.0.0.1:8093       0.0.0.0:*    users:(("python3",pid=725,fd=3))                                            
LISTEN 0      4096         0.0.0.0:32768      0.0.0.0:*    users:(("docker-proxy",pid=9279,fd=8))                                      
LISTEN 0      4096         0.0.0.0:22         0.0.0.0:*    users:(("sshd",pid=4024,fd=3),("systemd",pid=1,fd=223))                     
LISTEN 0      4096         0.0.0.0:4874       0.0.0.0:*    users:(("docker-proxy",pid=3989,fd=8))                                      
LISTEN 0      5            0.0.0.0:4864       0.0.0.0:*    users:(("python3",pid=737,fd=3))                                            
LISTEN 0      4096   127.0.0.53%lo:53         0.0.0.0:*    users:(("systemd-resolve",pid=543,fd=15))                                   
LISTEN 0      511        127.0.0.1:4865       0.0.0.0:*    users:(("nginx",pid=765,fd=5),("nginx",pid=764,fd=5),("nginx",pid=762,fd=5))
LISTEN 0      2048       127.0.0.1:4880       0.0.0.0:*    users:(("uvicorn",pid=711,fd=13))                                           
LISTEN 0      5          127.0.0.1:8770       0.0.0.0:*    users:(("python3",pid=726,fd=3))                                            
LISTEN 0      2048       127.0.0.1:8788       0.0.0.0:*    users:(("python",pid=12758,fd=6))                                           
LISTEN 0      5          127.0.0.1:8765       0.0.0.0:*    users:(("python",pid=9652,fd=4))                                            
LISTEN 0      4096            [::]:32768         [::]:*    users:(("docker-proxy",pid=9284,fd=8))                                      
LISTEN 0      4096            [::]:22            [::]:*    users:(("sshd",pid=4024,fd=4),("systemd",pid=1,fd=224))                     
LISTEN 0      4096            [::]:4874          [::]:*    users:(("docker-proxy",pid=3996,fd=8))                                      

```

### system/cron.txt

Size: 1092 bytes

```text
5 0 * * * /opt/second-brain/scripts/create_daily_log.sh >> /var/log/second-brain-daily.log 2>&1
55 23 * * * /opt/second-brain/scripts/reflection_append.sh >> /var/log/second-brain-reflection.log 2>&1
50 23 * * * python3 /opt/second-brain/scripts/daily_synthesis.py >> /var/log/second-brain-synthesis.log 2>&1
10 7 * * * /docker/hermes-semantic/venv/bin/python /docker/hermes-semantic/dailybrief.py >> /var/log/second-brain-executive-brief.log 2>&1
30 23 * * * /opt/second-brain/scripts/nightly_cycle.sh >> /var/log/second-brain-nightly.log 2>&1
0 3 * * * /opt/second-brain/scripts/git_backup_push_only.sh >> /var/log/git-backup.log 2>&1
#45 5 * * * /opt/second-brain/scripts/morning_briefing.py >> /root/morning-briefing.log 2>&1
#15 6 * * * python3 /opt/second-brain/scripts/autonomous_watchlist.py >> /var/log/second-brain-watchlists.log 2>&1
#20 6 * * * /opt/second-brain/scripts/run_daily_intelligence.sh >> /var/log/daily-intelligence.log 2>&1
0 5 * * 1 ENTITY_CMD=refresh python3 /opt/second-brain/scripts/entity_registry_maintenance.py >> /var/log/entity-registry-maintenance.log 2>&1

```

---

# Obsidian Knowledge Platform

Generated: 2026-06-30T21:41:58.616545


## Purpose

Defines the live Obsidian vault as Alfred's authoritative source of truth.

## Responsibilities

- Store source notes, captures, daily logs, people, companies, projects and governance artefacts.
- Remain human-readable and recoverable without Alfred.
- Provide the evidence base for enrichment, routing and semantic retrieval.

## Inputs

- User notes
- Captures
- Daily logs
- Batch enrichments

## Outputs

- Markdown evidence
- Source paths
- Knowledge graph substrate

## Dependencies

- Obsidian Sync
- Markdown files
- Vault filesystem

## Failure Modes

- Vault stale or not synced.
- Wrong vault path indexed.
- Derived artefacts mistaken for source truth.

## Recovery Procedure

- Verify `/docker/obsidian-vault` exists.
- Check markdown count and recent files.
- Confirm sync markers or recent expected notes.
- Rebuild LlamaIndex from the live vault only.

## Source Evidence

### obsidian/vault_summary.txt

Size: 12391 bytes

```text
===== size =====
55M	/docker/obsidian-vault
===== md count =====
4538
===== top folders =====
/docker/obsidian-vault
/docker/obsidian-vault/00 Inbox
/docker/obsidian-vault/00 Inbox/AI Imports
/docker/obsidian-vault/00 Inbox/Captures
/docker/obsidian-vault/00 Inbox/Historical Backfill
/docker/obsidian-vault/01 Daily Logs
/docker/obsidian-vault/02 People
/docker/obsidian-vault/02 People/01. HR
/docker/obsidian-vault/03 Projects
/docker/obsidian-vault/03 Projects/0. Finance
/docker/obsidian-vault/04 Companies
/docker/obsidian-vault/04 Companies/IG
/docker/obsidian-vault/04 Decisions
/docker/obsidian-vault/05 Knowledge
/docker/obsidian-vault/05 Knowledge/01. Compliance
/docker/obsidian-vault/05 Knowledge/AI
/docker/obsidian-vault/05 Open Loops
/docker/obsidian-vault/06 Systems
/docker/obsidian-vault/06 Systems/Entity Registry
/docker/obsidian-vault/06 Systems/Second Brain Scripts
/docker/obsidian-vault/07 AI Memory
/docker/obsidian-vault/07 AI Memory/Agent Council
/docker/obsidian-vault/07 AI Memory/Agent State
/docker/obsidian-vault/07 AI Memory/Agents
/docker/obsidian-vault/07 AI Memory/Alfred v2
/docker/obsidian-vault/07 AI Memory/Delegations
/docker/obsidian-vault/07 AI Memory/Enriched Captures
/docker/obsidian-vault/07 AI Memory/Entities
/docker/obsidian-vault/07 AI Memory/Entity Intelligence
/docker/obsidian-vault/07 AI Memory/Entity Registry
/docker/obsidian-vault/07 AI Memory/Historical Ingestion
/docker/obsidian-vault/07 AI Memory/Reporting Evidence
/docker/obsidian-vault/07 AI Memory/Strategic Graph
/docker/obsidian-vault/07 AI Memory/Strategic Synthesis
/docker/obsidian-vault/07 Executive Briefings
/docker/obsidian-vault/08 Open Loops
/docker/obsidian-vault/08 Open Loops/Escalation
/docker/obsidian-vault/08 Strategic Analysis
/docker/obsidian-vault/08 Strategic Analysis/Image Artifacts
/docker/obsidian-vault/09 Governance
/docker/obsidian-vault/09 Governance/AI Agent Reviews
/docker/obsidian-vault/09 Governance/Agent Deployments
/docker/obsidian-vault/09 Governance/Agent Governance
/docker/obsidian-vault/09 Governance/Agent Opinions
/docker/obsidian-vault/09 Governance/Architecture
/docker/obsidian-vault/09 Governance/Board Packs
/docker/obsidian-vault/09 Governance/Board Secretary
/docker/obsidian-vault/09 Governance/Board Sessions
/docker/obsidian-vault/09 Governance/Capture Lifecycle
/docker/obsidian-vault/09 Governance/Capture Review
/docker/obsidian-vault/09 Governance/Change Management
/docker/obsidian-vault/09 Governance/Daily Governance
/docker/obsidian-vault/09 Governance/Decision Intelligence
/docker/obsidian-vault/09 Governance/Delegation Queue
/docker/obsidian-vault/09 Governance/Escalations
/docker/obsidian-vault/09 Governance/Executive Graph
/docker/obsidian-vault/09 Governance/Executive Metrics
/docker/obsidian-vault/09 Governance/Executive Signals
/docker/obsidian-vault/09 Governance/Governance Intelligence
/docker/obsidian-vault/09 Governance/Healthchecks
/docker/obsidian-vault/09 Governance/Human Action Queue
/docker/obsidian-vault/09 Governance/Objective Intelligence
/docker/obsidian-vault/09 Governance/Objectives
/docker/obsidian-vault/09 Governance/Open Loops
/docker/obsidian-vault/09 Governance/Organisation
/docker/obsidian-vault/09 Governance/Prompt Governance
/docker/obsidian-vault/09 Governance/Recovery
/docker/obsidian-vault/09 Governance/Reflection Intelligence
/docker/obsidian-vault/09 Governance/Reports
/docker/obsidian-vault/09 Governance/Retention Policies
/docker/obsidian-vault/09 Governance/Reviews
/docker/obsidian-vault/09 Governance/Runtime Registry
/docker/obsidian-vault/09 Governance/Service Ownership
/docker/obsidian-vault/09 Governance/State Registry
/docker/obsidian-vault/09 Governance/Tasks
/docker/obsidian-vault/09 Governance/Watchlists
/docker/obsidian-vault/09 Governance/Weekly Councils
/docker/obsidian-vault/10 Domains
/docker/obsidian-vault/10 Domains/Personal
/docker/obsidian-vault/10 Domains/Work
/docker/obsidian-vault/10 Intelligence
/docker/obsidian-vault/10 Intelligence/Agent Collaboration
/docker/obsidian-vault/10 Intelligence/Autonomous Signals
/docker/obsidian-vault/10 Intelligence/Entity Graphs
/docker/obsidian-vault/10 Intelligence/Executive Intelligence
/docker/obsidian-vault/10 Intelligence/Executive Visuals
/docker/obsidian-vault/10 Intelligence/Reasoning Reviews
/docker/obsidian-vault/10 Intelligence/Relationship Memory
/docker/obsidian-vault/10 Intelligence/Retrieval Quality
/docker/obsidian-vault/11 Strategic Intelligence
/docker/obsidian-vault/11 Strategic Intelligence/Contradictions
/docker/obsidian-vault/11 Strategic Intelligence/Decision Register
/docker/obsidian-vault/11 Strategic Intelligence/Executive Narrative
/docker/obsidian-vault/11 Strategic Intelligence/Strategic Drift
/docker/obsidian-vault/11 Strategic Intelligence/Theme Detection
/docker/obsidian-vault/98 Archive
/docker/obsidian-vault/98 Archive/Captures
/docker/obsidian-vault/98 Archive/Historical Backfill
/docker/obsidian-vault/98 Archive/Logs
/docker/obsidian-vault/AI
/docker/obsidian-vault/Alfred
/docker/obsidian-vault/Alfred/Reviews
/docker/obsidian-vault/Attachments
/docker/obsidian-vault/Finance
/docker/obsidian-vault/LLM Wiki
/docker/obsidian-vault/LLM Wiki/People
/docker/obsidian-vault/LLM Wiki/Suppliers
/docker/obsidian-vault/Minutes
/docker/obsidian-vault/People
/docker/obsidian-vault/Phillip @FML
/docker/obsidian-vault/Phillip @FML/IG
/docker/obsidian-vault/Phillip @FML/New Section 2
/docker/obsidian-vault/Phillip @FML/Risk Compliance
/docker/obsidian-vault/Phillip @FML/Strategy or Project
/docker/obsidian-vault/Phillip @FML/Talend and Mentor
/docker/obsidian-vault/Suppliers
/docker/obsidian-vault/Tools
/docker/obsidian-vault/Work import
/docker/obsidian-vault/Work import/Apple Notes
===== recent md =====
Test.md
Telegram.md
Note.md
Inbox.md
Are.md
2026-06-28 16:52 /docker/obsidian-vault/00 Inbox/Test Sync.md.md
2026-06-28 07:10 /docker/obsidian-vault/07 Executive Briefings/2026-06-28 Executive Brief.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Reflection Intelligence/Latest Reflection Intelligence.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Objective Intelligence/Latest Objective Intelligence Report.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Objective Intelligence/2026-06-28 Objective Intelligence Report.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Governance Intelligence/Latest Governance Intelligence.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Executive Metrics/Latest Executive Metrics.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Daily Governance/Latest Daily Governance Index.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Board Secretary/Latest Board Secretary Agenda.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Board Packs/Latest Board Pack.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Board Packs/BOARD-PACK-2026-06-28-020010-WEEKLY.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/AI Agent Reviews/Latest AI Agent Reviews.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/AI Agent Reviews/Executive Committee.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/AI Agent Reviews/Executive AI Briefing.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/AI Agent Reviews/AI Agent Debate.md
2026-06-28 00:16 /docker/obsidian-vault/__.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/vCISO.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Workday.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Vyanta.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Vodafone.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Version 1.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/VCOL Website.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Upguard.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Trintech - ADRA.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Testrail.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/TRAX.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Sync.com.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Synapx.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/SwissRe - CatNet.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Softcat website.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/SoftCat.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/SoftCat portal.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Sharepoint - Lime Risk.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Serium.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/SQL Spreads.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/SES.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/SAP Ariba.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Reg Network.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/QA.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/QA service.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Power BI.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/PolicyFly.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Pluralsite.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/PlacingHub.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Pine Walk.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/PaloAlto.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/PWD Google.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/PO Consilio.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/One Communications.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Obsidian.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Nettitude - Security as a service.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Netitude.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/NAVEX.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Mudlur.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Moodys.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Monday.Com.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Model Builder.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Managed Print.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/LloydsListIntelligence.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Lloyds list.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/LWR.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Kocho group limited.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Jira -Atlassian.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Insurance Insider.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Idera.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/IBA.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Hoyle.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Hillbrooke.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Hamilton hotel.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/HP.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Gamma.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Four Seasons.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Forcepoint.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Flight Radar.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Finscan.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/EE Proposal.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Dreamix.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Docusign.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Docosoft.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Digital Realty Trust.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Digicel.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/DEX.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Cyber Chain Alliance.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Crowdstrike.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Consilio.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Co-Pilot.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/CloudBridge.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Cloud Ally.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Cardio.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Blacksun.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/BitDefender.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/BeyondFS.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Backupify.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/BDO.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/BA OnBusiness.md

```

### trees/vault.json

Size: 872489 bytes

```text
[
  {
    "path": "/docker/obsidian-vault/LLM Wiki",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:02:12.985041"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:04:23.359791"
  },
  {
    "path": "/docker/obsidian-vault/04 Decisions",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:33.919265"
  },
  {
    "path": "/docker/obsidian-vault/Work import",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:03:08.912931"
  },
  {
    "path": "/docker/obsidian-vault/Finance",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T16:53:38.301398"
  },
  {
    "path": "/docker/obsidian-vault/08 Open Loops",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:14.524592"
  },
  {
    "path": "/docker/obsidian-vault/SSH Key.md",
    "type": "file",
    "size": 731,
    "mtime": "2026-06-10T22:17:13.989000"
  },
  {
    "path": "/docker/obsidian-vault/People",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T16:53:55.837341"
  },
  {
    "path": "/docker/obsidian-vault/__.md",
    "type": "file",
    "size": 23,
    "mtime": "2026-06-28T00:16:35.243999"
  },
  {
    "path": "/docker/obsidian-vault/Pinewalk migration.md",
    "type": "file",
    "size": 719,
    "mtime": "2026-06-28T00:16:35.226999"
  },
  {
    "path": "/docker/obsidian-vault/05 Open Loops",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:02:49.076969"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:35.068260"
  },
  {
    "path": "/docker/obsidian-vault/Procurement Policy.md",
    "type": "file",
    "size": 2669,
    "mtime": "2026-06-28T00:16:35.226999"
  },
  {
    "path": "/docker/obsidian-vault/Alfred",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:04:40.519759"
  },
  {
    "path": "/docker/obsidian-vault/02 People",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:32.006274"
  },
  {
    "path": "/docker/obsidian-vault/Nettitude.md",
    "type": "file",
    "size": 0,
    "mtime": "2026-06-28T00:16:35.216000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments",
    "type": "dir",
    "size": 12288,
    "mtime": "2026-06-28T00:05:54.607627"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:31.900562"
  },
  {
    "path": "/docker/obsidian-vault/AI",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T16:53:59.893327"
  },
  {
    "path": "/docker/obsidian-vault/Tools",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:03:56.778840"
  },
  {
    "path": "/docker/obsidian-vault/Phase 2 - Vendor Management.md",
    "type": "file",
    "size": 9029,
    "mtime": "2026-06-28T00:16:35.220000"
  },
  {
    "path": "/docker/obsidian-vault/03 Projects",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:05:48.244638"
  },
  {
    "path": "/docker/obsidian-vault/2026-05-07.md",
    "type": "file",
    "size": 404,
    "mtime": "2026-06-28T00:16:35.158999"
  },
  {
    "path": "/docker/obsidian-vault/KYC Company Due Diligence Report.md",
    "type": "file",
    "size": 10541,
    "mtime": "2026-06-28T00:16:35.163000"
  },
  {
    "path": "/docker/obsidian-vault/Minutes",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:04:48.970744"
  },
  {
    "path": "/docker/obsidian-vault/Untitled.base",
    "type": "file",
    "size": 39,
    "mtime": "2026-05-26T15:55:44.489000"
  },
  {
    "path": "/docker/obsidian-vault/Suppliers",
    "type": "dir",
    "size": 12288,
    "mtime": "2026-06-28T16:53:59.233330"
  },
  {
    "path": "/docker/obsidian-vault/Phillip @FML",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T16:53:58.012334"
  },
  {
    "path": "/docker/obsidian-vault/2026-05-14.md",
    "type": "file",
    "size": 0,
    "mtime": "2026-06-28T00:16:35.158999"
  },
  {
    "path": "/docker/obsidian-vault/01 Daily Logs",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:05:01.138722"
  },
  {
    "path": "/docker/obsidian-vault/2026-06-12.md",
    "type": "file",
    "size": 0,
    "mtime": "2026-06-12T23:05:40.555999"
  },
  {
    "path": "/docker/obsidian-vault/08 Strategic Analysis",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:16.378486"
  },
  {
    "path": "/docker/obsidian-vault/Untitled 1.canvas",
    "type": "file",
    "size": 28,
    "mtime": "2026-06-24T09:07:37.880000"
  },
  {
    "path": "/docker/obsidian-vault/09 Governance",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:32.667459"
  },
  {
    "path": "/docker/obsidian-vault/10 Intelligence",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:07.714501"
  },
  {
    "path": "/docker/obsidian-vault/98 Archive",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:32.295459"
  },
  {
    "path": "/docker/obsidian-vault/Untitled.canvas",
    "type": "file",
    "size": 2,
    "mtime": "2026-06-12T23:05:46.112999"
  },
  {
    "path": "/docker/obsidian-vault/2026-05-11.md",
    "type": "file",
    "size": 0,
    "mtime": "2026-06-28T00:16:35.158999"
  },
  {
    "path": "/docker/obsidian-vault/Pernix meeting.md",
    "type": "file",
    "size": 1988,
    "mtime": "2026-06-28T00:16:35.219000"
  },
  {
    "path": "/docker/obsidian-vault/00 Inbox",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T16:53:27.159435"
  },
  {
    "path": "/docker/obsidian-vault/Claude.md.md",
    "type": "file",
    "size": 3237,
    "mtime": "2026-05-08T20:36:27.176000"
  },
  {
    "path": "/docker/obsidian-vault/04 Companies",
    "type": "dir",
    "size": 12288,
    "mtime": "2026-06-28T00:08:15.453353"
  },
  {
    "path": "/docker/obsidian-vault/11 Strategic Intelligence",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:31.324461"
  },
  {
    "path": "/docker/obsidian-vault/07 Executive Briefings",
    "type": "dir",
    "size": 20480,
    "mtime": "2026-06-28T07:10:47.293694"
  },
  {
    "path": "/docker/obsidian-vault/10 Domains",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:05:07.876710"
  },
  {
    "path": "/docker/obsidian-vault/Jira.md",
    "type": "file",
    "size": 0,
    "mtime": "2026-06-28T00:16:35.163000"
  },
  {
    "path": "/docker/obsidian-vault/2026-05-26.md",
    "type": "file",
    "size": 0,
    "mtime": "2026-05-26T10:24:25.966000"
  },
  {
    "path": "/docker/obsidian-vault/Hermes Windows install.md",
    "type": "file",
    "size": 13854,
    "mtime": "2026-06-10T15:27:11.821000"
  },
  {
    "path": "/docker/obsidian-vault/LLM Wiki/People",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:31.937275"
  },
  {
    "path": "/docker/obsidian-vault/LLM Wiki/Suppliers",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:31.874275"
  },
  {
    "path": "/docker/obsidian-vault/LLM Wiki/index.md",
    "type": "file",
    "size": 2530,
    "mtime": "2026-05-09T05:24:36.519000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/EOF.md",
    "type": "file",
    "size": 70,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/JSON.md",
    "type": "file",
    "size": 71,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Add.md",
    "type": "file",
    "size": 70,
    "mtime": "2026-05-22T21:08:00.418999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Source\nTelegram.md",
    "type": "file",
    "size": 82,
    "mtime": "2026-05-21T21:23:14.490000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/GitHub.md",
    "type": "file",
    "size": 73,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/HOME.md",
    "type": "file",
    "size": 71,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Decisions.md",
    "type": "file",
    "size": 76,
    "mtime": "2026-05-21T09:01:17.443000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Needs.md",
    "type": "file",
    "size": 72,
    "mtime": "2026-05-20T22:50:13.153000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/InsTech 2026.md",
    "type": "file",
    "size": 8552,
    "mtime": "2026-06-11T16:47:10.045000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Iseconds.md",
    "type": "file",
    "size": 75,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Capture.md",
    "type": "file",
    "size": 74,
    "mtime": "2026-05-20T22:50:13.151999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Run.md",
    "type": "file",
    "size": 70,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Configure.md",
    "type": "file",
    "size": 76,
    "mtime": "2026-05-22T21:08:00.418999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Seed.md",
    "type": "file",
    "size": 71,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Content - Decision.md",
    "type": "file",
    "size": 83,
    "mtime": "2026-05-21T09:01:17.443000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Content - What.md",
    "type": "file",
    "size": 79,
    "mtime": "2026-05-21T09:01:17.443000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Set.md",
    "type": "file",
    "size": 70,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/PATH.md",
    "type": "file",
    "size": 71,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Ive.md",
    "type": "file",
    "size": 70,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Source - Telegram.md",
    "type": "file",
    "size": 82,
    "mtime": "2026-05-20T22:50:13.153000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Content - Procurement.md",
    "type": "file",
    "size": 86,
    "mtime": "2026-05-20T22:50:13.151999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/System.md",
    "type": "file",
    "size": 73,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/AI",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:33.487560"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/EUR.md",
    "type": "file",
    "size": 70,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Content\nNote.md",
    "type": "file",
    "size": 79,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Content - You.md",
    "type": "file",
    "size": 78,
    "mtime": "2026-05-21T10:01:24.845999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Example.md",
    "type": "file",
    "size": 74,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Procurement.md",
    "type": "file",
    "size": 88,
    "mtime": "2026-05-20T22:44:59.865999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Next.md",
    "type": "file",
    "size": 71,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/DORA.md",
    "type": "file",
    "size": 81,
    "mtime": "2026-05-20T22:48:38.637000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Content\nTest.md",
    "type": "file",
    "size": 79,
    "mtime": "2026-05-21T21:23:14.490000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/API.md",
    "type": "file",
    "size": 70,
    "mtime": "2026-05-22T21:08:00.418999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/USER.md",
    "type": "file",
    "size": 71,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Status - Inbox.md",
    "type": "file",
    "size": 79,
    "mtime": "2026-05-20T22:50:13.153000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/NousResearch.md",
    "type": "file",
    "size": 79,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Create.md",
    "type": "file",
    "size": 73,
    "mtime": "2026-05-22T21:08:00.418999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Entities.md",
    "type": "file",
    "size": 75,
    "mtime": "2026-05-20T22:50:13.151999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Status\nInbox.md",
    "type": "file",
    "size": 79,
    "mtime": "2026-05-21T21:23:14.490000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/01. Compliance",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:31.807275"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Untitled.canvas",
    "type": "file",
    "size": 2,
    "mtime": "2026-05-24T17:13:29.400000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Content\nAre.md",
    "type": "file",
    "size": 78,
    "mtime": "2026-05-21T23:21:34.651999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Keep.md",
    "type": "file",
    "size": 71,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Should.md",
    "type": "file",
    "size": 73,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/04 Decisions/Monthly Pursource Governance.md",
    "type": "file",
    "size": 13746,
    "mtime": "2026-05-24T15:13:13.342000"
  },
  {
    "path": "/docker/obsidian-vault/04 Decisions/Decision - Hermes Host Networking.md",
    "type": "file",
    "size": 1502,
    "mtime": "2026-05-24T17:13:46.496999"
  },
  {
    "path": "/docker/obsidian-vault/04 Decisions/Capture - 20260520-221048 Decision.md",
    "type": "file",
    "size": 462,
    "mtime": "2026-05-20T23:12:31.476999"
  },
  {
    "path": "/docker/obsidian-vault/04 Decisions/Mancom - ExCo.md",
    "type": "file",
    "size": 637,
    "mtime": "2026-05-24T15:12:28.029000"
  },
  {
    "path": "/docker/obsidian-vault/04 Decisions/Decision Template.md",
    "type": "file",
    "size": 377,
    "mtime": "2026-05-20T20:59:31.753999"
  },
  {
    "path": "/docker/obsidian-vault/Work import/Apple Notes",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:05:32.376666"
  },
  {
    "path": "/docker/obsidian-vault/Finance/Finance review.md",
    "type": "file",
    "size": 30333,
    "mtime": "2026-05-12T14:18:43"
  },
  {
    "path": "/docker/obsidian-vault/Finance/Finance discussion.md",
    "type": "file",
    "size": 13076,
    "mtime": "2026-05-12T14:21:20"
  },
  {
    "path": "/docker/obsidian-vault/Finance/VAT.md",
    "type": "file",
    "size": 2868,
    "mtime": "2026-05-08T22:34:15"
  },
  {
    "path": "/docker/obsidian-vault/Finance/Finance 2024 review.md",
    "type": "file",
    "size": 443,
    "mtime": "2026-06-28T00:16:35.161999"
  },
  {
    "path": "/docker/obsidian-vault/Finance/Finance lookup.md",
    "type": "file",
    "size": 2940,
    "mtime": "2026-05-12T14:20:56"
  },
  {
    "path": "/docker/obsidian-vault/Finance/CAPEX.md",
    "type": "file",
    "size": 1320,
    "mtime": "2026-06-28T00:16:35.161999"
  },
  {
    "path": "/docker/obsidian-vault/Finance/PO.md",
    "type": "file",
    "size": 2866,
    "mtime": "2026-05-14T13:59:46"
  },
  {
    "path": "/docker/obsidian-vault/Finance/Expense management.md",
    "type": "file",
    "size": 2049,
    "mtime": "2026-05-08T22:34:15"
  },
  {
    "path": "/docker/obsidian-vault/Finance/Finance.md",
    "type": "file",
    "size": 342,
    "mtime": "2026-06-28T00:16:35.163000"
  },
  {
    "path": "/docker/obsidian-vault/08 Open Loops/Open Loop Review.md",
    "type": "file",
    "size": 2922,
    "mtime": "2026-05-24T20:01:51"
  },
  {
    "path": "/docker/obsidian-vault/08 Open Loops/Open Loop Register.md",
    "type": "file",
    "size": 2615,
    "mtime": "2026-05-24T20:23:56"
  },
  {
    "path": "/docker/obsidian-vault/08 Open Loops/2026-05-20 Open Loops.md",
    "type": "file",
    "size": 3367,
    "mtime": "2026-05-20T23:08:32.818000"
  },
  {
    "path": "/docker/obsidian-vault/08 Open Loops/Escalation",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T02:00:10.293432"
  },
  {
    "path": "/docker/obsidian-vault/08 Open Loops/Hermes Open Loops.md",
    "type": "file",
    "size": 4873,
    "mtime": "2026-06-11T22:49:26.635999"
  },
  {
    "path": "/docker/obsidian-vault/08 Open Loops/Loop Candidates.md",
    "type": "file",
    "size": 5230,
    "mtime": "2026-05-24T20:14:22"
  },
  {
    "path": "/docker/obsidian-vault/People/Neil Lindo.md",
    "type": "file",
    "size": 1292,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Cindy Eves.md",
    "type": "file",
    "size": 3370,
    "mtime": "2026-05-12T14:24:10"
  },
  {
    "path": "/docker/obsidian-vault/People/James Plunkett.md",
    "type": "file",
    "size": 529,
    "mtime": "2026-06-28T00:16:35.217999"
  },
  {
    "path": "/docker/obsidian-vault/People/Olivia Brindle.md",
    "type": "file",
    "size": 2716,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Graham Dawe.md",
    "type": "file",
    "size": 35681,
    "mtime": "2026-06-28T00:16:35.217999"
  },
  {
    "path": "/docker/obsidian-vault/People/Lee Harper.md",
    "type": "file",
    "size": 923,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Eleen - Ali - AP.md",
    "type": "file",
    "size": 468,
    "mtime": "2026-06-28T00:16:35.217000"
  },
  {
    "path": "/docker/obsidian-vault/People/Suzanne Wells.md",
    "type": "file",
    "size": 5543,
    "mtime": "2026-05-19T10:06:05"
  },
  {
    "path": "/docker/obsidian-vault/People/Nigel Lee.md",
    "type": "file",
    "size": 1576,
    "mtime": "2026-05-12T14:26:45"
  },
  {
    "path": "/docker/obsidian-vault/People/Edison Lusha.md",
    "type": "file",
    "size": 2329,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Ricard Torres Marti.md",
    "type": "file",
    "size": 3021,
    "mtime": "2026-05-12T14:26:45"
  },
  {
    "path": "/docker/obsidian-vault/People/Rinku.md",
    "type": "file",
    "size": 7331,
    "mtime": "2026-05-12T14:26:45"
  },
  {
    "path": "/docker/obsidian-vault/People/Micheal Monks.md",
    "type": "file",
    "size": 687,
    "mtime": "2026-05-08T22:45:24"
  },
  {
    "path": "/docker/obsidian-vault/People/Debbie Lean.md",
    "type": "file",
    "size": 188,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Phil Murfet.md",
    "type": "file",
    "size": 4456,
    "mtime": "2026-06-28T00:16:35.219000"
  },
  {
    "path": "/docker/obsidian-vault/People/Julie Broom.md",
    "type": "file",
    "size": 3499,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Rhys Puddy - Finance-Expense-Purchase.md",
    "type": "file",
    "size": 3971,
    "mtime": "2026-05-12T14:21:23"
  },
  {
    "path": "/docker/obsidian-vault/People/Ash Bailey.md",
    "type": "file",
    "size": 287,
    "mtime": "2026-05-12T14:18:15"
  },
  {
    "path": "/docker/obsidian-vault/People/Alex Lott.md",
    "type": "file",
    "size": 11361,
    "mtime": "2026-05-12T14:26:45"
  },
  {
    "path": "/docker/obsidian-vault/People/Gary Whiston.md",
    "type": "file",
    "size": 5303,
    "mtime": "2026-05-12T14:24:10"
  },
  {
    "path": "/docker/obsidian-vault/People/Chris Sweetser.md",
    "type": "file",
    "size": 2070,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Dinesh.md",
    "type": "file",
    "size": 249,
    "mtime": "2026-06-28T00:16:35.217000"
  },
  {
    "path": "/docker/obsidian-vault/People/Phillip Doheny.md",
    "type": "file",
    "size": 933,
    "mtime": "2026-06-28T00:16:35.219000"
  },
  {
    "path": "/docker/obsidian-vault/People/Yvonne Lancaster - Risk.md",
    "type": "file",
    "size": 1440,
    "mtime": "2026-05-08T22:45:24"
  },
  {
    "path": "/docker/obsidian-vault/People/David Reid.md",
    "type": "file",
    "size": 1292,
    "mtime": "2026-05-12T14:20:57"
  },
  {
    "path": "/docker/obsidian-vault/People/Emily Puddifer.md",
    "type": "file",
    "size": 50,
    "mtime": "2026-06-28T00:16:35.217000"
  },
  {
    "path": "/docker/obsidian-vault/People/Denise Bareford.md",
    "type": "file",
    "size": 5400,
    "mtime": "2026-05-12T14:21:22"
  },
  {
    "path": "/docker/obsidian-vault/People/Gary McInally.md",
    "type": "file",
    "size": 1320,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/John Paul O'Hare.md",
    "type": "file",
    "size": 2092,
    "mtime": "2026-05-12T14:26:45"
  },
  {
    "path": "/docker/obsidian-vault/People/Gyorgy Penczu.md",
    "type": "file",
    "size": 4240,
    "mtime": "2026-05-18T13:59:00"
  },
  {
    "path": "/docker/obsidian-vault/People/Francesca Harrison.md",
    "type": "file",
    "size": 1184,
    "mtime": "2026-05-08T22:45:24"
  },
  {
    "path": "/docker/obsidian-vault/People/Stephen.md",
    "type": "file",
    "size": 1974,
    "mtime": "2026-05-08T22:34:12"
  },
  {
    "path": "/docker/obsidian-vault/People/Chika.md",
    "type": "file",
    "size": 1205,
    "mtime": "2026-05-22T18:09:02"
  },
  {
    "path": "/docker/obsidian-vault/People/Ali Ajaz.md",
    "type": "file",
    "size": 415,
    "mtime": "2026-06-28T00:16:35.217000"
  },
  {
    "path": "/docker/obsidian-vault/People/Mat Nieznanski.md",
    "type": "file",
    "size": 158,
    "mtime": "2026-06-28T00:16:35.219000"
  },
  {
    "path": "/docker/obsidian-vault/People/Mark Rowe - Compliance.md",
    "type": "file",
    "size": 5606,
    "mtime": "2026-05-12T14:21:23"
  },
  {
    "path": "/docker/obsidian-vault/People/Joe Bosberry.md",
    "type": "file",
    "size": 19751,
    "mtime": "2026-06-28T00:16:35.217999"
  },
  {
    "path": "/docker/obsidian-vault/People/Michael Hay.md",
    "type": "file",
    "size": 1239,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Marc Avery.md",
    "type": "file",
    "size": 836,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Matt Rudge.md",
    "type": "file",
    "size": 4304,
    "mtime": "2026-05-12T14:26:47"
  },
  {
    "path": "/docker/obsidian-vault/People/Will Thrower.md",
    "type": "file",
    "size": 2025,
    "mtime": "2026-05-08T22:34:12"
  },
  {
    "path": "/docker/obsidian-vault/People/Donal Glackin.md",
    "type": "file",
    "size": 1179,
    "mtime": "2026-05-12T14:18:43"
  },
  {
    "path": "/docker/obsidian-vault/People/Jake Groves - Infrastructure.md",
    "type": "file",
    "size": 531,
    "mtime": "2026-05-12T14:20:57"
  },
  {
    "path": "/docker/obsidian-vault/People/Megan.md",
    "type": "file",
    "size": 5920,
    "mtime": "2026-05-18T11:34:07"
  },
  {
    "path": "/docker/obsidian-vault/People/Mark Dean.md",
    "type": "file",
    "size": 10761,
    "mtime": "2026-05-12T14:24:10"
  },
  {
    "path": "/docker/obsidian-vault/People/Anna.md",
    "type": "file",
    "size": 2653,
    "mtime": "2026-05-08T22:45:24"
  },
  {
    "path": "/docker/obsidian-vault/People/Marcus Denison.md",
    "type": "file",
    "size": 85,
    "mtime": "2026-06-28T00:16:35.217999"
  },
  {
    "path": "/docker/obsidian-vault/People/Dee Pang.md",
    "type": "file",
    "size": 710,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Andy Wetmiller - CTO.md",
    "type": "file",
    "size": 1942,
    "mtime": "2026-05-08T22:45:24"
  },
  {
    "path": "/docker/obsidian-vault/People/Bernie 11.md",
    "type": "file",
    "size": 1077,
    "mtime": "2026-05-08T22:45:24"
  },
  {
    "path": "/docker/obsidian-vault/People/Neil Flanagan.md",
    "type": "file",
    "size": 2914,
    "mtime": "2026-05-12T14:20:57"
  },
  {
    "path": "/docker/obsidian-vault/People/Julia Weeks - Legal.md",
    "type": "file",
    "size": 4289,
    "mtime": "2026-05-12T14:26:45"
  },
  {
    "path": "/docker/obsidian-vault/People/Dan Clow.md",
    "type": "file",
    "size": 7135,
    "mtime": "2026-05-20T10:36:18"
  },
  {
    "path": "/docker/obsidian-vault/People/Tom Lawson.md",
    "type": "file",
    "size": 1518,
    "mtime": "2026-05-15T09:20:41"
  },
  {
    "path": "/docker/obsidian-vault/People/Annu Dhillon - Service Desk.md",
    "type": "file",
    "size": 1271,
    "mtime": "2026-05-12T14:18:15"
  },
  {
    "path": "/docker/obsidian-vault/People/Niall Purcell.md",
    "type": "file",
    "size": 656,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/John Hurworth.md",
    "type": "file",
    "size": 10352,
    "mtime": "2026-05-15T09:20:41"
  },
  {
    "path": "/docker/obsidian-vault/05 Open Loops/Open Loops.md",
    "type": "file",
    "size": 221,
    "mtime": "2026-05-20T23:17:21.569999"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/2026-05-25 Hermes Conversations.md",
    "type": "file",
    "size": 126,
    "mtime": "2026-05-25T18:44:55.351000"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Agent Council",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:04.832609"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Agent State",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:55.745521"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Reporting Evidence",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:17.688484"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Strategic Graph",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:36.057555"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Agents",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:17.648343"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Entities",
    "type": "dir",
    "size": 57344,
    "mtime": "2026-06-28T16:53:25.847439"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Alfred v2",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T02:00:03.909450"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Entity Intelligence",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:25.527471"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Historical Ingestion",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:01.316410"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Entity Registry",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:46.617537"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Strategic Synthesis",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:25.388471"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Operating Manual.md",
    "type": "file",
    "size": 1836,
    "mtime": "2026-05-20T21:02:46.763000"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Enriched Captures",
    "type": "dir",
    "size": 36864,
    "mtime": "2026-06-28T00:08:31.382277"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Delegations",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:00.542617"
  },
  {
    "path": "/docker/obsidian-vault/Alfred/Reviews",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:04:40.520759"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Neil Lindo.md",
    "type": "file",
    "size": 1294,
    "mtime": "2026-05-24T15:13:13.546000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Cindy Eves.md",
    "type": "file",
    "size": 12698,
    "mtime": "2026-06-10T08:55:34.234999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/James Plunkett.md",
    "type": "file",
    "size": 529,
    "mtime": "2026-05-08T22:34:11.831000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Olivia Brindle.md",
    "type": "file",
    "size": 2739,
    "mtime": "2026-05-24T15:13:13.548000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Graham Dawe.md",
    "type": "file",
    "size": 44778,
    "mtime": "2026-06-26T14:11:32.362999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Lee Harper.md",
    "type": "file",
    "size": 962,
    "mtime": "2026-05-24T15:13:13.540999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Eleen - Ali - AP.md",
    "type": "file",
    "size": 468,
    "mtime": "2026-05-08T22:45:24.220000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Suzanne Wells.md",
    "type": "file",
    "size": 5757,
    "mtime": "2026-05-24T15:13:13.552000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Nigel Lee.md",
    "type": "file",
    "size": 1670,
    "mtime": "2026-05-24T15:13:13.548000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Edison Lusha.md",
    "type": "file",
    "size": 2342,
    "mtime": "2026-05-24T15:13:13.533999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Ricard Torres Marti.md",
    "type": "file",
    "size": 3024,
    "mtime": "2026-05-24T15:13:13.551000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Oracle Procurement.md",
    "type": "file",
    "size": 82,
    "mtime": "2026-05-20T22:53:41.203000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Rinku.md",
    "type": "file",
    "size": 7539,
    "mtime": "2026-05-24T17:14:20.177000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Micheal Monks.md",
    "type": "file",
    "size": 700,
    "mtime": "2026-05-24T15:13:13.545000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Install Hermes.md",
    "type": "file",
    "size": 78,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Debbie Lean.md",
    "type": "file",
    "size": 214,
    "mtime": "2026-05-24T15:13:13.529999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Auto Links.md",
    "type": "file",
    "size": 74,
    "mtime": "2026-05-20T22:50:13.151999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Phil Murfet.md",
    "type": "file",
    "size": 4456,
    "mtime": "2026-05-08T22:34:12.010999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Julie Broom.md",
    "type": "file",
    "size": 3537,
    "mtime": "2026-05-24T17:14:20.176000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Rhys Puddy - Finance-Expense-Purchase.md",
    "type": "file",
    "size": 4010,
    "mtime": "2026-05-24T15:13:13.549999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Ash Bailey.md",
    "type": "file",
    "size": 292,
    "mtime": "2026-05-24T15:13:13.526000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/01. HR",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:04:29.919779"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Alex Lott.md",
    "type": "file",
    "size": 18776,
    "mtime": "2026-06-26T16:53:58.660000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Gary Whiston.md",
    "type": "file",
    "size": 5411,
    "mtime": "2026-05-24T17:14:20.170000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Chris Sweetser.md",
    "type": "file",
    "size": 2080,
    "mtime": "2026-05-24T15:12:28.030999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Content - Maria Jose Lloret Crespo.md",
    "type": "file",
    "size": 96,
    "mtime": "2026-05-20T22:53:41.203000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Dinesh.md",
    "type": "file",
    "size": 249,
    "mtime": "2026-05-08T22:34:11.721999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Verify Hermes.md",
    "type": "file",
    "size": 77,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Phillip Doheny.md",
    "type": "file",
    "size": 933,
    "mtime": "2026-05-08T22:47:18.542000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Processing Notes.md",
    "type": "file",
    "size": 80,
    "mtime": "2026-05-20T22:50:13.153000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Start Hermes.md",
    "type": "file",
    "size": 76,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Ensure Hermes.md",
    "type": "file",
    "size": 77,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Yvonne Lancaster - Risk.md",
    "type": "file",
    "size": 1450,
    "mtime": "2026-05-24T15:12:28.042999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/David Reid.md",
    "type": "file",
    "size": 1640,
    "mtime": "2026-06-08T16:17:09.069000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Emily Puddifer.md",
    "type": "file",
    "size": 50,
    "mtime": "2026-05-08T22:34:11.730999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Denise Bareford.md",
    "type": "file",
    "size": 5508,
    "mtime": "2026-05-24T17:14:20.168999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Garry Sweeney.md",
    "type": "file",
    "size": 1960,
    "mtime": "2026-05-28T14:31:36.783999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Gary McInally.md",
    "type": "file",
    "size": 1333,
    "mtime": "2026-05-24T15:13:13.535000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/John Paul O'Hare.md",
    "type": "file",
    "size": 2108,
    "mtime": "2026-05-24T15:13:13.539000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Gyorgy Penczu.md",
    "type": "file",
    "size": 9243,
    "mtime": "2026-06-22T13:47:14.868999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Francesca Harrison.md",
    "type": "file",
    "size": 1197,
    "mtime": "2026-05-24T15:13:13.533999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Stephen.md",
    "type": "file",
    "size": 1976,
    "mtime": "2026-05-24T15:13:13.552000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Obsidian Sync.md",
    "type": "file",
    "size": 77,
    "mtime": "2026-05-21T21:23:14.490000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Chika.md",
    "type": "file",
    "size": 3421,
    "mtime": "2026-06-23T16:50:34.321000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Ali Ajaz.md",
    "type": "file",
    "size": 415,
    "mtime": "2026-05-08T22:34:11.660000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Mat Nieznanski.md",
    "type": "file",
    "size": 1250,
    "mtime": "2026-06-23T16:20:19.763999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Mark Rowe - Compliance.md",
    "type": "file",
    "size": 5622,
    "mtime": "2026-05-24T15:13:13.542999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Joe Bosberry.md",
    "type": "file",
    "size": 27477,
    "mtime": "2026-06-26T14:08:25.401000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Auto Tags.md",
    "type": "file",
    "size": 73,
    "mtime": "2026-05-20T22:50:13.151999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Michael Hay.md",
    "type": "file",
    "size": 1252,
    "mtime": "2026-05-24T15:13:13.545000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Marc Avery.md",
    "type": "file",
    "size": 849,
    "mtime": "2026-05-24T15:13:13.542000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Create Hermes.md",
    "type": "file",
    "size": 77,
    "mtime": "2026-05-22T21:08:00.418999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Matt Rudge.md",
    "type": "file",
    "size": 4345,
    "mtime": "2026-05-25T10:23:20.973000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Will Thrower.md",
    "type": "file",
    "size": 2051,
    "mtime": "2026-05-24T15:13:13.553999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Donal Glackin.md",
    "type": "file",
    "size": 2428,
    "mtime": "2026-06-15T15:55:12.687999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Jake Groves - Infrastructure.md",
    "type": "file",
    "size": 547,
    "mtime": "2026-05-24T15:13:13.536999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Megan.md",
    "type": "file",
    "size": 5914,
    "mtime": "2026-06-15T11:06:43.665999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Mark Dean.md",
    "type": "file",
    "size": 10877,
    "mtime": "2026-05-24T17:14:20.177000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Anna.md",
    "type": "file",
    "size": 2666,
    "mtime": "2026-05-24T15:13:13.523999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Marcus Denison.md",
    "type": "file",
    "size": 85,
    "mtime": "2026-05-08T22:34:11.923000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/MSCI World UCITS.md",
    "type": "file",
    "size": 80,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Microsoft Azure.md",
    "type": "file",
    "size": 79,
    "mtime": "2026-05-20T22:50:13.153000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Dee Pang.md",
    "type": "file",
    "size": 712,
    "mtime": "2026-05-24T15:13:13.529999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Andy Wetmiller - CTO.md",
    "type": "file",
    "size": 1967,
    "mtime": "2026-05-24T15:13:13.523999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Bernie 11.md",
    "type": "file",
    "size": 1090,
    "mtime": "2026-05-24T15:13:13.526000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Neil Flanagan.md",
    "type": "file",
    "size": 3013,
    "mtime": "2026-05-24T15:13:13.546000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Jonathan Croud.md",
    "type": "file",
    "size": 2992,
    "mtime": "2026-06-25T10:24:04.759999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Julia Weeks - Legal.md",
    "type": "file",
    "size": 7797,
    "mtime": "2026-06-25T14:31:51.114000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Dan Clow.md",
    "type": "file",
    "size": 8528,
    "mtime": "2026-06-24T11:22:08.223000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Related Memories.md",
    "type": "file",
    "size": 80,
    "mtime": "2026-05-20T22:50:13.153000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Tom Lawson.md",
    "type": "file",
    "size": 1543,
    "mtime": "2026-05-24T15:13:13.552999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Decision Template.md",
    "type": "file",
    "size": 81,
    "mtime": "2026-05-21T09:01:17.443000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Pearly NG.md",
    "type": "file",
    "size": 184,
    "mtime": "2026-05-29T11:45:37.256000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Annu Dhillon - Service Desk.md",
    "type": "file",
    "size": 1289,
    "mtime": "2026-05-24T15:13:13.525000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Niall Purcell.md",
    "type": "file",
    "size": 768,
    "mtime": "2026-06-22T12:31:43.466000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/John Hurworth.md",
    "type": "file",
    "size": 10552,
    "mtime": "2026-05-24T15:13:13.539000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100138-0.png",
    "type": "file",
    "size": 264899,
    "mtime": "2026-05-07T10:01:39.874000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085306-1.png",
    "type": "file",
    "size": 318879,
    "mtime": "2026-05-07T08:53:08.302999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085142-0.png",
    "type": "file",
    "size": 191375,
    "mtime": "2026-05-07T08:51:43.625000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134509-10.png",
    "type": "file",
    "size": 181283,
    "mtime": "2026-05-07T13:45:10.269999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/f23fa4f1-6832-479a-822d-3f1b624f26bf (1).md",
    "type": "file",
    "size": 1555904,
    "mtime": "2026-06-04T15:37:02.006000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084307-0.png",
    "type": "file",
    "size": 720,
    "mtime": "2026-05-07T08:43:08.836999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134109-1.png",
    "type": "file",
    "size": 107232,
    "mtime": "2026-05-07T13:41:10.835999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134515-14.png",
    "type": "file",
    "size": 93748,
    "mtime": "2026-05-07T13:45:16.670000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100410-0.png",
    "type": "file",
    "size": 50311,
    "mtime": "2026-05-07T10:04:11.915999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100350-0.jpeg",
    "type": "file",
    "size": 6178,
    "mtime": "2026-05-07T10:03:51.828999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100252-0.png",
    "type": "file",
    "size": 97456,
    "mtime": "2026-05-07T10:02:57.381000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100417-1.png",
    "type": "file",
    "size": 63081,
    "mtime": "2026-05-07T10:04:19.023999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Pasted image 20260511162016.png",
    "type": "file",
    "size": 24973,
    "mtime": "2026-05-11T16:20:16.602999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100317-0.png",
    "type": "file",
    "size": 4962,
    "mtime": "2026-05-07T10:03:18.921999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134500-3.png",
    "type": "file",
    "size": 182029,
    "mtime": "2026-05-07T13:45:01.180999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100428-2.png",
    "type": "file",
    "size": 203431,
    "mtime": "2026-05-07T10:04:30.339999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085244-0.png",
    "type": "file",
    "size": 286514,
    "mtime": "2026-05-07T08:52:45.342000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085143-1.png",
    "type": "file",
    "size": 245913,
    "mtime": "2026-05-07T08:51:44.960000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134108-0.png",
    "type": "file",
    "size": 123179,
    "mtime": "2026-05-07T13:41:09.753999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100652-2.png",
    "type": "file",
    "size": 208072,
    "mtime": "2026-05-07T10:06:56.377000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100122-2.png",
    "type": "file",
    "size": 7448,
    "mtime": "2026-05-07T10:01:23.963999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085259-4.png",
    "type": "file",
    "size": 151293,
    "mtime": "2026-05-07T08:53:01.405999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084538-4.png",
    "type": "file",
    "size": 291225,
    "mtime": "2026-05-07T08:45:42.654999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100123-3.png",
    "type": "file",
    "size": 6323,
    "mtime": "2026-05-07T10:01:28.526999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134514-12.png",
    "type": "file",
    "size": 46690,
    "mtime": "2026-05-07T13:45:14.947000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084321-0.png",
    "type": "file",
    "size": 374,
    "mtime": "2026-05-07T08:43:26.648999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085126-1.png",
    "type": "file",
    "size": 37288,
    "mtime": "2026-05-07T08:51:27.711999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084959-1.png",
    "type": "file",
    "size": 17556,
    "mtime": "2026-05-07T08:50:00.089999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100120-0.png",
    "type": "file",
    "size": 21897,
    "mtime": "2026-05-07T10:01:21.305000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085245-1.png",
    "type": "file",
    "size": 192777,
    "mtime": "2026-05-07T08:52:46.720999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084542-5.png",
    "type": "file",
    "size": 266519,
    "mtime": "2026-05-07T08:45:43.772000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100323-5.png",
    "type": "file",
    "size": 13372,
    "mtime": "2026-05-07T10:03:27.420000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134510-11.png",
    "type": "file",
    "size": 119282,
    "mtime": "2026-05-07T13:45:14.128999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085237-0.png",
    "type": "file",
    "size": 123545,
    "mtime": "2026-05-07T08:52:39.105999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084331-0.png",
    "type": "file",
    "size": 105720,
    "mtime": "2026-05-07T08:43:32.904000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085301-5.png",
    "type": "file",
    "size": 174204,
    "mtime": "2026-05-07T08:53:02.450999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100132-7.png",
    "type": "file",
    "size": 25676,
    "mtime": "2026-05-07T10:01:33.776999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134114-5.png",
    "type": "file",
    "size": 288264,
    "mtime": "2026-05-07T13:41:15.545000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084500-0.png",
    "type": "file",
    "size": 374,
    "mtime": "2026-05-07T08:45:05.575999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100327-6.png",
    "type": "file",
    "size": 34487,
    "mtime": "2026-05-07T10:03:28.533999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134131-1.png",
    "type": "file",
    "size": 3659,
    "mtime": "2026-05-07T13:41:32.269000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084209-1.png",
    "type": "file",
    "size": 384,
    "mtime": "2026-05-07T08:42:10.368999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085125-0.png",
    "type": "file",
    "size": 6147,
    "mtime": "2026-05-07T08:51:26.637000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084535-2.png",
    "type": "file",
    "size": 303582,
    "mtime": "2026-05-07T08:45:37.125999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507095958-0.png",
    "type": "file",
    "size": 393310,
    "mtime": "2026-05-07T10:00:00.013000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100808-0.png",
    "type": "file",
    "size": 195989,
    "mtime": "2026-05-07T10:08:12.486999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085155-3.png",
    "type": "file",
    "size": 119221,
    "mtime": "2026-05-07T08:51:57.232000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085004-0.png",
    "type": "file",
    "size": 35924,
    "mtime": "2026-05-07T08:50:09.710000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085027-0.png",
    "type": "file",
    "size": 145623,
    "mtime": "2026-05-07T08:50:28.941999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100041-2.png",
    "type": "file",
    "size": 127965,
    "mtime": "2026-05-07T10:00:45.555000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134505-6.png",
    "type": "file",
    "size": 88493,
    "mtime": "2026-05-07T13:45:06.732000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085034-0.png",
    "type": "file",
    "size": 56989,
    "mtime": "2026-05-07T08:50:36.059000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085111-2.png",
    "type": "file",
    "size": 123744,
    "mtime": "2026-05-07T08:51:13.766000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084559-0.png",
    "type": "file",
    "size": 68095,
    "mtime": "2026-05-07T08:46:00.779999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084214-1.png",
    "type": "file",
    "size": 282148,
    "mtime": "2026-05-07T08:42:16.134000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134111-3.png",
    "type": "file",
    "size": 235279,
    "mtime": "2026-05-07T13:41:13.375999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100331-0.png",
    "type": "file",
    "size": 2326,
    "mtime": "2026-05-07T10:03:32.835000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100318-1.png",
    "type": "file",
    "size": 4599,
    "mtime": "2026-05-07T10:03:19.917999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Pasted image 20260526113344.png",
    "type": "file",
    "size": 259849,
    "mtime": "2026-05-26T11:33:44.447000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134507-8.png",
    "type": "file",
    "size": 15843,
    "mtime": "2026-05-07T13:45:08.601000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100416-0.png",
    "type": "file",
    "size": 287026,
    "mtime": "2026-05-07T10:04:17.703999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085135-5.png",
    "type": "file",
    "size": 16838,
    "mtime": "2026-05-07T08:51:36.450000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084543-6.png",
    "type": "file",
    "size": 406385,
    "mtime": "2026-05-07T08:45:45.040999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100319-2.png",
    "type": "file",
    "size": 14835,
    "mtime": "2026-05-07T10:03:21.115999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100034-0.png",
    "type": "file",
    "size": 233573,
    "mtime": "2026-05-07T10:00:35.388999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084453-0.png",
    "type": "file",
    "size": 1442,
    "mtime": "2026-05-07T08:44:54.016000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100246-0.png",
    "type": "file",
    "size": 58481,
    "mtime": "2026-05-07T10:02:47.753000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100038-0.png",
    "type": "file",
    "size": 343924,
    "mtime": "2026-05-07T10:00:39.667999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085247-3.png",
    "type": "file",
    "size": 139907,
    "mtime": "2026-05-07T08:52:59.813999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100228-0.png",
    "type": "file",
    "size": 80724,
    "mtime": "2026-05-07T10:02:29.431999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100000-1.png",
    "type": "file",
    "size": 800385,
    "mtime": "2026-05-07T10:00:02.010999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Pasted image 20260518162228.png",
    "type": "file",
    "size": 196597,
    "mtime": "2026-05-18T16:22:28.582999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134514-13.png",
    "type": "file",
    "size": 89440,
    "mtime": "2026-05-07T13:45:15.815000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134508-9.png",
    "type": "file",
    "size": 94418,
    "mtime": "2026-05-07T13:45:09.382999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100651-1.png",
    "type": "file",
    "size": 266772,
    "mtime": "2026-05-07T10:06:52.377000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084511-0.png",
    "type": "file",
    "size": 158117,
    "mtime": "2026-05-07T08:45:13.151000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100423-0.png",
    "type": "file",
    "size": 463869,
    "mtime": "2026-05-07T10:04:24.698999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085128-3.png",
    "type": "file",
    "size": 8095,
    "mtime": "2026-05-07T08:51:33.516999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085246-2.png",
    "type": "file",
    "size": 93976,
    "mtime": "2026-05-07T08:52:47.825999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134506-7.png",
    "type": "file",
    "size": 84047,
    "mtime": "2026-05-07T13:45:07.585999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085109-1.png",
    "type": "file",
    "size": 127915,
    "mtime": "2026-05-07T08:51:11.003000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100322-4.png",
    "type": "file",
    "size": 12713,
    "mtime": "2026-05-07T10:03:23.315999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084957-0.png",
    "type": "file",
    "size": 94370,
    "mtime": "2026-05-07T08:49:59.058000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100446-0.png",
    "type": "file",
    "size": 46912,
    "mtime": "2026-05-07T10:04:47.678999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100656-3.png",
    "type": "file",
    "size": 42648,
    "mtime": "2026-05-07T10:06:57.226999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084257-0.png",
    "type": "file",
    "size": 892531,
    "mtime": "2026-05-07T08:42:58.871000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100021-0.png",
    "type": "file",
    "size": 249489,
    "mtime": "2026-05-07T10:00:23.173000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084856-0.png",
    "type": "file",
    "size": 149616,
    "mtime": "2026-05-07T08:48:57.970999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100351-1.jpeg",
    "type": "file",
    "size": 6178,
    "mtime": "2026-05-07T10:03:53.542999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100321-3.png",
    "type": "file",
    "size": 8569,
    "mtime": "2026-05-07T10:03:22.068000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085144-2.png",
    "type": "file",
    "size": 102197,
    "mtime": "2026-05-07T08:51:55.924000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100046-4.png",
    "type": "file",
    "size": 217130,
    "mtime": "2026-05-07T10:00:48.407000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134531-0.png",
    "type": "file",
    "size": 19356,
    "mtime": "2026-05-07T13:45:32.164999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084907-0.png",
    "type": "file",
    "size": 92724,
    "mtime": "2026-05-07T08:49:08.517999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134118-0.png",
    "type": "file",
    "size": 169240,
    "mtime": "2026-05-07T13:41:19.516000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085108-0.png",
    "type": "file",
    "size": 31574,
    "mtime": "2026-05-07T08:51:09.822999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/a.md",
    "type": "file",
    "size": 2226,
    "mtime": "2026-06-04T16:42:17.871999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134110-2.png",
    "type": "file",
    "size": 231909,
    "mtime": "2026-05-07T13:41:11.892999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085305-0.png",
    "type": "file",
    "size": 264899,
    "mtime": "2026-05-07T08:53:06.423000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134516-15.png",
    "type": "file",
    "size": 210253,
    "mtime": "2026-05-07T13:45:17.648000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084445-0.png",
    "type": "file",
    "size": 116209,
    "mtime": "2026-05-07T08:44:46.124000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084315-0.png",
    "type": "file",
    "size": 93470,
    "mtime": "2026-05-07T08:43:16.470999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085136-6.png",
    "type": "file",
    "size": 17623,
    "mtime": "2026-05-07T08:51:37.487999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100333-2.png",
    "type": "file",
    "size": 1340,
    "mtime": "2026-05-07T10:03:34.898000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084208-0.png",
    "type": "file",
    "size": 384,
    "mtime": "2026-05-07T08:42:09.424000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134519-18.png",
    "type": "file",
    "size": 99767,
    "mtime": "2026-05-07T13:45:23.289999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085133-4.png",
    "type": "file",
    "size": 14833,
    "mtime": "2026-05-07T08:51:35.122999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134517-16.png",
    "type": "file",
    "size": 127275,
    "mtime": "2026-05-07T13:45:18.536999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100139-1.png",
    "type": "file",
    "size": 318879,
    "mtime": "2026-05-07T10:01:44.082000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084537-3.png",
    "type": "file",
    "size": 372877,
    "mtime": "2026-05-07T08:45:38.194999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084513-1.png",
    "type": "file",
    "size": 539,
    "mtime": "2026-05-07T08:45:14.227999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084441-0.png",
    "type": "file",
    "size": 1554,
    "mtime": "2026-05-07T08:44:42.311000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100114-0.png",
    "type": "file",
    "size": 1554,
    "mtime": "2026-05-07T10:01:16.153000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134518-17.png",
    "type": "file",
    "size": 121364,
    "mtime": "2026-05-07T13:45:19.398000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085206-0.png",
    "type": "file",
    "size": 208631,
    "mtime": "2026-05-07T08:52:07.927999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Pasted image 20260618090354.png",
    "type": "file",
    "size": 0,
    "mtime": "2026-06-18T09:03:54.516999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085137-7.png",
    "type": "file",
    "size": 35004,
    "mtime": "2026-05-07T08:51:38.808000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134457-0.png",
    "type": "file",
    "size": 59231,
    "mtime": "2026-05-07T13:44:58.404999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100159-0.png",
    "type": "file",
    "size": 62766,
    "mtime": "2026-05-07T10:02:00.375000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100437-0.png",
    "type": "file",
    "size": 65059,
    "mtime": "2026-05-07T10:04:38.256999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100129-5.png",
    "type": "file",
    "size": 66875,
    "mtime": "2026-05-07T10:01:31.315999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134459-2.png",
    "type": "file",
    "size": 184543,
    "mtime": "2026-05-07T13:45:00.253999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084442-1.png",
    "type": "file",
    "size": 45923,
    "mtime": "2026-05-07T08:44:43.082999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100332-1.png",
    "type": "file",
    "size": 1221,
    "mtime": "2026-05-07T10:03:33.785000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085127-2.png",
    "type": "file",
    "size": 9681,
    "mtime": "2026-05-07T08:51:28.752000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100131-6.png",
    "type": "file",
    "size": 1554,
    "mtime": "2026-05-07T10:01:32.464999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084532-0.png",
    "type": "file",
    "size": 244975,
    "mtime": "2026-05-07T08:45:34.723000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134113-4.png",
    "type": "file",
    "size": 242000,
    "mtime": "2026-05-07T13:41:14.427999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100128-4.png",
    "type": "file",
    "size": 5324,
    "mtime": "2026-05-07T10:01:29.864000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084214-0.png",
    "type": "file",
    "size": 65535,
    "mtime": "2026-05-07T08:42:14.970999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100002-2.png",
    "type": "file",
    "size": 531317,
    "mtime": "2026-05-07T10:00:03.470999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100133-8.png",
    "type": "file",
    "size": 1554,
    "mtime": "2026-05-07T10:01:34.963000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100121-1.png",
    "type": "file",
    "size": 19862,
    "mtime": "2026-05-07T10:01:22.769000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100315-0.png",
    "type": "file",
    "size": 195989,
    "mtime": "2026-05-07T10:03:16.786999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134505-5.png",
    "type": "file",
    "size": 102671,
    "mtime": "2026-05-07T13:45:05.937000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100202-0.png",
    "type": "file",
    "size": 212748,
    "mtime": "2026-05-07T10:02:04.039000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134134-0.png",
    "type": "file",
    "size": 1442,
    "mtime": "2026-05-07T13:41:35.655999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100424-1.png",
    "type": "file",
    "size": 18973,
    "mtime": "2026-05-07T10:04:28.973000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134458-1.png",
    "type": "file",
    "size": 180284,
    "mtime": "2026-05-07T13:44:59.236999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084534-1.png",
    "type": "file",
    "size": 22316,
    "mtime": "2026-05-07T08:45:35.841000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134501-4.png",
    "type": "file",
    "size": 92671,
    "mtime": "2026-05-07T13:45:05.009999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100650-0.png",
    "type": "file",
    "size": 199251,
    "mtime": "2026-05-07T10:06:51.266999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085337-1.png",
    "type": "file",
    "size": 13726,
    "mtime": "2026-05-07T08:53:42.200000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134127-0.png",
    "type": "file",
    "size": 2765,
    "mtime": "2026-05-07T13:41:31.290999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085336-0.png",
    "type": "file",
    "size": 19343,
    "mtime": "2026-05-07T08:53:37.516000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100039-1.png",
    "type": "file",
    "size": 48517,
    "mtime": "2026-05-07T10:00:41.187000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100045-3.png",
    "type": "file",
    "size": 39017,
    "mtime": "2026-05-07T10:00:46.892999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Obsidian 1.md",
    "type": "file",
    "size": 0,
    "mtime": "2026-05-21T22:48:22.598999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Hermes.md",
    "type": "file",
    "size": 81,
    "mtime": "2026-05-20T22:44:59.865000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Hermes Architecture.md",
    "type": "file",
    "size": 1141,
    "mtime": "2026-05-20T21:03:48.055999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/GitHub.md",
    "type": "file",
    "size": 4075,
    "mtime": "2026-05-10T22:08:35.444999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Demos.md",
    "type": "file",
    "size": 1576,
    "mtime": "2026-05-24T17:14:20.240000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Code blueprint.md",
    "type": "file",
    "size": 2868,
    "mtime": "2026-05-08T22:34:15.125000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Contract tooling.md",
    "type": "file",
    "size": 1244,
    "mtime": "2026-05-24T17:14:20.240000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/DF Training.md",
    "type": "file",
    "size": 2712,
    "mtime": "2026-05-24T17:14:20.240999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Second Brain Scripts",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:31.901562"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Hermes Sync Test.md",
    "type": "file",
    "size": 69,
    "mtime": "2026-05-20T18:59:35"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Hermes website instruction.md",
    "type": "file",
    "size": 12671,
    "mtime": "2026-05-11T19:44:31.701999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Claude command lines.jpeg",
    "type": "file",
    "size": 62652,
    "mtime": "2026-04-07T20:49:50.756000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Docker.md",
    "type": "file",
    "size": 81,
    "mtime": "2026-05-22T21:08:00.381000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Keys.md",
    "type": "file",
    "size": 975,
    "mtime": "2026-05-24T18:51:00.450000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Obsidian Sync Operating Model.md",
    "type": "file",
    "size": 858,
    "mtime": "2026-05-21T21:23:59.029000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/obsidian and hermes.md",
    "type": "file",
    "size": 5579,
    "mtime": "2026-05-11T07:40:27.358000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/WhatsApp.md",
    "type": "file",
    "size": 20495,
    "mtime": "2026-05-10T21:00:26.357000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Entity Registry",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:05:07.578711"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Microsoft.md",
    "type": "file",
    "size": 84,
    "mtime": "2026-05-20T22:48:38.637000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Azure.md",
    "type": "file",
    "size": 80,
    "mtime": "2026-05-20T22:48:38.637000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Obsidian.md",
    "type": "file",
    "size": 83,
    "mtime": "2026-05-21T21:23:14.464999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Perplexity.md",
    "type": "file",
    "size": 305,
    "mtime": "2026-05-10T23:12:48.720999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Telegram.md",
    "type": "file",
    "size": 83,
    "mtime": "2026-05-20T22:44:59.865999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Claude design.md",
    "type": "file",
    "size": 143,
    "mtime": "2026-05-08T22:34:15.114000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Perplexity company search.md",
    "type": "file",
    "size": 471,
    "mtime": "2026-05-11T11:03:59.671999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Hermes to do.md",
    "type": "file",
    "size": 722,
    "mtime": "2026-05-10T21:24:59.576999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/VPS Sync test.md",
    "type": "file",
    "size": 148,
    "mtime": "2026-05-25T16:55:46.346999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Hermes VPS Skills.md",
    "type": "file",
    "size": 17821,
    "mtime": "2026-05-19T23:46:21.299000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Oracle.md",
    "type": "file",
    "size": 81,
    "mtime": "2026-05-20T22:53:41.171000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Hermes 1.md",
    "type": "file",
    "size": 23728,
    "mtime": "2026-05-10T22:06:55.168999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/OpenRouter.md",
    "type": "f
```

---

# Alfred Router

Generated: 2026-06-30T21:41:58.616557


## Purpose

Defines the orchestration and quality gate layer used by Telegram and deterministic workflows.

## Responsibilities

- Classify user intent.
- Select the correct retrieval or deterministic strategy.
- Execute protected routes.
- Validate answers before returning them.
- Withhold unsupported answers rather than hallucinate.

## Inputs

- User query
- Strategy definitions
- Hermes compatibility path
- Evidence policies

## Outputs

- Validated answer
- Quality-gate rejection
- Audit trail

## Dependencies

- alfred_router.sh
- alfred_router.py
- strategies.py
- validation.py
- hermes_ask.sh

## Failure Modes

- Strategy returns non-zero exit code.
- Answer is empty.
- Container default points to stale runtime.
- OpenRouter key unavailable for legacy path.

## Recovery Procedure

- Run alfred_router.sh directly with a known query.
- Check strategies.py defaults.
- Check hermes_ask.sh environment handling.
- Confirm Telegram service environment matches working router configuration.

## Source Evidence

### key_files/opt__second-brain__scripts__alfred_router.sh

Size: 151 bytes

```text
#!/usr/bin/env bash
set -Eeuo pipefail

export PYTHONPATH="/opt/second-brain${PYTHONPATH:+:$PYTHONPATH}"

exec python3 -m retrieval.alfred_router "$@"

```

### key_files/opt__second-brain__retrieval__alfred_router.py

Size: 5719 bytes

```text
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

from .audit import append_audit
from .classifiers import classify_query
from .strategies import StrategyResult, execute_strategy
from .validators import validate_answer


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def output_hash(value: str) -> str:
    return hashlib.sha256(
        value.encode("utf-8", errors="ignore")
    ).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Alfred structured retrieval router",
    )

    parser.add_argument(
        "--explain",
        action="store_true",
        help="Classify and explain the route without answering.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Return a structured response envelope.",
    )

    parser.add_argument(
        "--no-audit",
        action="store_true",
        help="Do not append an audit event.",
    )

    parser.add_argument(
        "question",
        nargs="+",
        help="Natural-language question.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    question = " ".join(args.question).strip()
    decision = classify_query(question)

    if args.explain:
        print(
            json.dumps(
                decision.to_dict(),
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0

    started_monotonic = time.monotonic()
    started_at = utc_now()

    result = execute_strategy(
        decision=decision,
        question=question,
    )

    validation = validate_answer(
        decision=decision,
        question=question,
        answer=result.stdout,
        exit_code=result.exit_code,
    )

    rejected_output_path = None

    if not validation.passed:
        rejection_root = Path(
            "/opt/second-brain/logs/validation-rejections"
        )

        rejection_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        stamp = datetime.now(
            timezone.utc
        ).strftime("%Y%m%d-%H%M%S-%f")

        rejected_output = (
            rejection_root
            / f"rejected-{stamp}.txt"
        )

        rejected_output.write_text(
            "\n".join(
                [
                    f"Question: {question}",
                    f"Intent: {decision.intent}",
                    f"Strategy: {decision.strategy}",
                    "",
                    "Validation failures:",
                    *[
                        f"- {failure}"
                        for failure in validation.failures
                    ],
                    "",
                    "Rejected answer:",
                    result.stdout,
                    "",
                    "Retrieval stderr:",
                    result.stderr,
                ]
            ),
            encoding="utf-8",
        )

        rejected_output_path = str(
            rejected_output
        )

        controlled_message = "\n".join(
            [
                "Alfred withheld this answer because it "
                "did not meet the evidence-quality standard.",
                "",
                "Validation issues:",
                *[
                    f"- {failure}"
                    for failure in validation.failures
                ],
                "",
                "No unsupported answer has been returned.",
            ]
        ) + "\n"

        result = StrategyResult(
            stdout=controlled_message,
            stderr=result.stderr,
            exit_code=3,
            sources=result.sources,
            fallback_used=result.fallback_used,
        )

    duration_seconds = round(
        time.monotonic() - started_monotonic,
        3,
    )

    event: dict[str, Any] = {
        "timestamp": started_at,
        "question": question,
        "decision": decision.to_dict(),
        "result": {
            "exit_code": result.exit_code,
            "duration_seconds": duration_seconds,
            "output_characters": len(result.stdout),
            "output_sha256": output_hash(result.stdout),
            "sources": result.sources,
            "fallback_used": result.fallback_used,
        },
        "validation": {
            **validation.to_dict(),
            "rejected_output_path": rejected_output_path,
        },
        "runtime": {
            "hermes_container": os.environ.get(
                "HERMES_CONTAINER",
                "hermes-authoritative-vault",
            ),
            "router_version": "0.2.0",
        },
    }

    if not args.no_audit:
        append_audit(event)

    if args.json:
        envelope = {
            "route": decision.to_dict(),
            "result": {
                "answer": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.exit_code,
                "duration_seconds": duration_seconds,
                "sources": result.sources,
                "fallback_used": result.fallback_used,
            },
        }

        print(
            json.dumps(
                envelope,
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        if result.stdout:
            sys.stdout.write(result.stdout)

        if result.stderr:
            sys.stderr.write(result.stderr)

            if not result.stderr.endswith("\n"):
                sys.stderr.write("\n")

    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())

```

### key_files/opt__second-brain__retrieval__strategies.py

Size: 3960 bytes

```text
from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .models import RouteDecision


DAILY_READER = Path(
    "/opt/second-brain/scripts/get_daily_section.py"
)

LEGACY_ROUTER = Path(
    "/opt/second-brain/scripts/hermes_ask.sh"
)


@dataclass
class StrategyResult:
    stdout: str
    stderr: str
    exit_code: int
    sources: list[str]
    fallback_used: bool


def _run(
    command: list[str],
    timeout_seconds: int,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        env=env,
        check=False,
    )


def deterministic_daily_log(
    decision: RouteDecision,
) -> StrategyResult:
    outputs: list[str] = []
    errors: list[str] = []
    sources: list[str] = []
    exit_code = 0

    if not decision.date_reference:
        return StrategyResult(
            stdout="",
            stderr="Daily-log route did not receive a date.",
            exit_code=2,
            sources=[],
            fallback_used=False,
        )

    for section in decision.sections:
        completed = _run(
            [
                str(DAILY_READER),
                decision.date_reference,
                section,
            ],
            timeout_seconds=30,
        )

        if completed.stdout.strip():
            outputs.append(completed.stdout.strip())

        if completed.stderr.strip():
            errors.append(completed.stderr.strip())

        if completed.returncode != 0:
            exit_code = completed.returncode

    date_display = decision.date_reference

    if date_display not in {"today", "yesterday"}:
        sources.append(
            f"01 Daily Logs/{date_display}.md"
        )

    return StrategyResult(
        stdout="\n\n".join(outputs).strip() + "\n",
        stderr="\n".join(errors),
        exit_code=exit_code,
        sources=sources,
        fallback_used=False,
    )


def protected_legacy(
    decision: RouteDecision,
    question: str,
) -> StrategyResult:
    env = os.environ.copy()
    env.setdefault(
        "HERMES_CONTAINER",
        "hermes-agent-mctr-hermes-agent-1",
    )

    completed = _run(
        [
            str(LEGACY_ROUTER),
            question,
        ],
        timeout_seconds=650,
        env=env,
    )

    return StrategyResult(
        stdout=completed.stdout,
        stderr=completed.stderr,
        exit_code=completed.returncode,
        sources=[],
        fallback_used=True,
    )


def execute_strategy(
    decision: RouteDecision,
    question: str,
) -> StrategyResult:
    if decision.strategy == "reject_empty":
        return StrategyResult(
            stdout="No question was provided.\n",
            stderr="",
            exit_code=2,
            sources=[],
            fallback_used=False,
        )

    if decision.strategy == "deterministic_daily_log":
        return deterministic_daily_log(decision)

    if decision.strategy == "validated_tprm_evidence":
        return protected_legacy(
            decision=decision,
            question=f"__ALFRED_TPRM_EVIDENCE__ {question}",
        )

    if decision.strategy == "validated_cost_evidence":
        return protected_legacy(
            decision=decision,
            question=f"__ALFRED_COST_EVIDENCE__ {question}",
        )

    if decision.strategy in {
        "validated_objective_evidence",
        "protected_legacy_evidence",
        "protected_legacy_entity",
        "protected_legacy_general",
    }:
        return protected_legacy(
            decision=decision,
            question=question,
        )

    return StrategyResult(
        stdout="",
        stderr=(
            f"Unsupported retrieval strategy: "
            f"{decision.strategy}"
        ),
        exit_code=2,
        sources=[],
        fallback_used=False,
    )

```

### key_files/opt__second-brain__scripts__hermes_ask.sh

Size: 31008 bytes

```text
#!/bin/bash
set -euo pipefail

QUERY="$*"
printf "%s\n---\n" "$QUERY" >> /tmp/hermes_ask_queries.log

# Allow callers to select the Hermes runtime explicitly.
# Keep the previous runtime as the temporary default until migration is complete.
HERMES_CONTAINER="${HERMES_CONTAINER:-hermes-agent-mctr-hermes-agent-1}"

KEY_CONTAINER="${HERMES_KEY_CONTAINER:-hermes-agent-mctr-hermes-agent-1}"

if [ -n "${OPENROUTER_API_KEY:-}" ]; then
  REAL_KEY="$OPENROUTER_API_KEY"
else
  REAL_KEY=$(docker inspect "$KEY_CONTAINER" --format '{{range .Config.Env}}{{println .}}{{end}}' | grep '^OPENROUTER_API_KEY=<redacted>
fi

if [[ "${HERMES_SYNTHESIS_ONLY:-0}" == "1" ]]; then
  PROMPT="$QUERY"

  timeout 300 docker exec \
    -e HERMES_PROMPT="$PROMPT" \
    -e OPENROUTER_API_KEY=<redacted>
    "$HERMES_CONTAINER" \
    bash -lc '/opt/hermes/.venv/bin/hermes chat --provider openrouter -m openai/gpt-4o-mini -q "$HERMES_PROMPT" -Q' \
    2>/tmp/hermes_ask.err \
    | tr -d '\000' \
    | sed '/session_id:/d'

  exit ${PIPESTATUS[0]}
fi


if [ -z "$QUERY" ]; then
  echo "No query supplied."
  exit 1
fi

# Deterministic routing for structured daily-log requests.
# These requests must not use entity, direct-reference or semantic retrieval.
LOWER_QUERY=$(printf '%s' "$QUERY" | tr '[:upper:]' '[:lower:]')

# Deterministic routing for explicit ISO dates such as 2026-06-10.
# A structured date + section request must not fall through to semantic search.
EXPLICIT_ROUTE=$(
  python3 - "$QUERY" <<'PYROUTE'
import re
import sys

query = sys.argv[1].lower()

date_match = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", query)
if not date_match:
    raise SystemExit(0)

sections = []

if re.search(r"\bfollow[\s-]*ups?\b|\bfollow[\s-]*up actions?\b", query):
    sections.append("follow-ups")

if re.search(r"\bopen[\s-]*loops?\b", query):
    sections.append("open-loops")

if re.search(r"\bdecisions?\b", query):
    sections.append("decisions")

if sections:
    print(f"{date_match.group(1)}\t{','.join(sections)}")
PYROUTE
)

if [[ -n "$EXPLICIT_ROUTE" ]]; then
  IFS=$'\t' read -r EXPLICIT_DATE EXPLICIT_SECTIONS <<< "$EXPLICIT_ROUTE"
  IFS=',' read -r -a SECTION_LIST <<< "$EXPLICIT_SECTIONS"

  for INDEX in "${!SECTION_LIST[@]}"; do
    if (( INDEX > 0 )); then
      printf '\n'
    fi

    /opt/second-brain/scripts/get_daily_section.py       "$EXPLICIT_DATE"       "${SECTION_LIST[$INDEX]}"
  done

  exit 0
fi

case "$LOWER_QUERY" in
  *yesterday*"follow up"*"open loop"*|*yesterday*"open loop"*"follow up"*|*"follow up"*"open loop"*yesterday*|*"open loop"*"follow up"*yesterday*)
    /opt/second-brain/scripts/get_daily_section.py yesterday follow-ups
    printf '\n'
    exec /opt/second-brain/scripts/get_daily_section.py yesterday open-loops
    ;;
  *today*"follow up"*"open loop"*|*today*"open loop"*"follow up"*|*"follow up"*"open loop"*today*|*"open loop"*"follow up"*today*)
    /opt/second-brain/scripts/get_daily_section.py today follow-ups
    printf '\n'
    exec /opt/second-brain/scripts/get_daily_section.py today open-loops
    ;;
  *yesterday*"follow up"*|*"follow up"*yesterday*)
    exec /opt/second-brain/scripts/get_daily_section.py yesterday follow-ups
    ;;
  *today*"follow up"*|*"follow up"*today*)
    exec /opt/second-brain/scripts/get_daily_section.py today follow-ups
    ;;
  *yesterday*"open loop"*|*"open loop"*yesterday*)
    exec /opt/second-brain/scripts/get_daily_section.py yesterday open-loops
    ;;
  *today*"open loop"*|*"open loop"*today*)
    exec /opt/second-brain/scripts/get_daily_section.py today open-loops
    ;;
  *yesterday*"decision"*|*"decision"*yesterday*)
    exec /opt/second-brain/scripts/get_daily_section.py yesterday decisions
    ;;
  *today*"decision"*|*"decision"*today*)
    exec /opt/second-brain/scripts/get_daily_section.py today decisions
    ;;
esac

# Objective, HR-goal and performance-review questions use an exclusive,
# evidence-led route. They must not be contaminated by generic semantic
# results, generated Objective Intelligence reports, board packs, or prior
# AI-generated summaries.
if printf '%s' "$LOWER_QUERY" | grep -Eq \
  '(hr|team|annual|year|performance review|performance-review).*(objective|goal)|(objective|goal).*(hr|team|annual|year|performance review|performance-review)'
then
  OBJECTIVE_EVIDENCE=$(
    /opt/second-brain/scripts/objective_evidence_search.py \
      | sed -n '1,320p'
  )

  OBJECTIVE_PROMPT="
You are Alfred, Phillip's operational second brain and executive chief-of-staff AI.

The user is asking for HR, team, annual, or performance-review objectives.

Use ONLY the concrete source evidence supplied below.
Do not use semantic memory, generated governance reports, Objective Intelligence reports, board packs, executive briefings, AI Memory, archived summaries, or previous objective wording.

The objective is not to produce generic HR language. The objective is to identify the specific business needs evidenced in the vault and convert them into practical, measurable objectives.

STRICT RULES

1. Each objective must include at least two concrete business facts from the supplied evidence.

2. At least one fact must be one of:
   - a named initiative;
   - a control failure;
   - a regulatory obligation;
   - a delivery problem;
   - a financial amount;
   - an explicit target;
   - a missing process;
   - a documented risk;
   - a required remediation;
   - a named system, supplier, team or programme.

3. Use only the source paths and line numbers included in the supplied evidence.

4. Never invent:
   - percentages;
   - deadlines;
   - financial targets;
   - completion rates;
   - efficiency improvements;
   - implementation dates.

5. Where the evidence contains no agreed numerical target or date, write:
   Target and completion date to be agreed with the objective owner.

6. Do not use unsupported phrases such as:
   - improve efficiency;
   - enhance governance;
   - drive innovation;
   - support development;
   - strengthen capability;
unless you immediately state the specific process, control, deliverable, metric or business condition that will change.

7. Do not cite any source under:
   - 09 Governance
   - 07 AI Memory
   - 07 Executive Briefings
   - 98 Archive

8. Historical objective prose is not evidence. Base the answer on operational facts, problems, initiatives, risks, targets and obligations.

9. Produce one objective from each of the six supplied evidence themes:
   - Operational Governance and DORA
   - Supplier Risk and Contractual Control
   - Data, AI and Automation
   - People, Capability and Succession
   - Cost, Spend and Procurement Control
   - Performance, Reporting and Delivery

   Do not replace any of these with a generic management category.
   Where a theme lacks sufficient evidence, state that rather than inventing content.

10. For every objective, use exactly these headings:

### <number>. <specific objective title>

BUSINESS NEED
State the concrete source facts that justify the objective.

OBJECTIVE
State the specific result the team member or team must deliver.

DELIVERABLES
List tangible outputs such as a deployed process, completed remediation, approved policy, implemented control, dashboard, signed-off framework, training plan, or documented operating model.

MEASURES
Use only measures already explicit in the evidence. Where no agreed target exists, state that the target must be agreed.

SOURCES
List exact vault paths and line numbers.

INFERENCE
State precisely which parts of the objective or deliverables were synthesised by Alfred rather than explicitly stated in the notes.

11. End with:
Evidence coverage: Strong / Moderate / Weak
Source notes used: <paths>
Inferred or newly suggested content: <honest summary>

CONCRETE OBJECTIVE EVIDENCE:
$OBJECTIVE_EVIDENCE

USER QUESTION:
$QUERY

Produce a concise but operationally specific answer.
"

  OBJECTIVE_OUTPUT=$(mktemp /tmp/alfred-objective-output.XXXXXX)
  OBJECTIVE_ERROR=$(mktemp /tmp/alfred-objective-error.XXXXXX)

  cleanup_objective_files() {
    rm -f "$OBJECTIVE_OUTPUT" "$OBJECTIVE_ERROR"
  }

  validate_objective_answer() {
    local answer_file="$1"
    local objective_count
    local marker_count=0

    [[ -s "$answer_file" ]] || {
      echo "VALIDATION: answer was empty" >&2
      return 1
    }

    if grep -qiE \
      '09 Governance/Objective Intelligence|07 AI Memory|07 Executive Briefings|98 Archive|15% by|20% by|90% completion|nothing inferred|Inferred or newly suggested content:[[:space:]]*(None|none)' \
      "$answer_file"
    then
      echo "VALIDATION: forbidden source or unsupported claim detected" >&2
      return 1
    fi

    for heading in \
      "BUSINESS NEED" \
      "OBJECTIVE" \
      "DELIVERABLES" \
      "MEASURES" \
      "SOURCES" \
      "INFERENCE"
    do
      if ! grep -q "$heading" "$answer_file"; then
        echo "VALIDATION: required heading missing: $heading" >&2
        return 1
      fi
    done

    objective_count=$(
      grep -Ec '^###[[:space:]]+[1-6]\.' "$answer_file" || true
    )

    if (( objective_count < 6 )); then
      echo \
        "VALIDATION: expected six objectives, found $objective_count" \
        >&2
      return 1
    fi

    for marker in \
      'TPRM 2\.0' \
      'DORA' \
      '70011' \
      'duplicate invoice|£95k|95k' \
      'controllable OPEX|OPEX' \
      '\$1\.5m|1\.5m|savings' \
      'AI strategy|AI governance' \
      'key person|retention|succession' \
      'SLA|KPI|dashboard' \
      'subcontract|audit right|exit plan'
    do
      if grep -qiE "$marker" "$answer_file"; then
        marker_count=$((marker_count + 1))
      fi
    done

    if (( marker_count < 4 )); then
      echo \
        "VALIDATION: insufficient concrete business evidence markers: $marker_count/4" \
        >&2
      return 1
    fi

    if ! grep -qiE \
      'Inferred or newly suggested content:[[:space:]]*.+' \
      "$answer_file"
    then
      echo "VALIDATION: provenance footer missing" >&2
      return 1
    fi

    return 0
  }

  generate_objective_answer() {
    local prompt="$1"
    local output_file="$2"
    local error_file="$3"
    local status

    set +e

    timeout 300 docker exec \
      -e HERMES_PROMPT="$prompt" \
      -e OPENROUTER_API_KEY=<redacted>
      "$HERMES_CONTAINER" \
      bash -lc '/opt/hermes/.venv/bin/hermes chat --provider openrouter -m openai/gpt-4o-mini -q "$HERMES_PROMPT" -Q' \
      2>"$error_file" \
      | tr -d '\000' \
      | sed '/session_id:/d' \
      > "$output_file"

    status=${PIPESTATUS[0]}

    set -e

    return "$status"
  }

  if ! generate_objective_answer \
    "$OBJECTIVE_PROMPT" \
    "$OBJECTIVE_OUTPUT" \
    "$OBJECTIVE_ERROR"
  then
    cat "$OBJECTIVE_ERROR" > /tmp/hermes_ask.err
    cleanup_objective_files
    echo \
      "Alfred could not generate the objective answer because the model call failed."
    exit 1
  fi

  if ! validate_objective_answer "$OBJECTIVE_OUTPUT"; then
    CORRECTIVE_OBJECTIVE_PROMPT="$OBJECTIVE_PROMPT

QUALITY-CONTROL CORRECTION

The previous draft failed the evidence-quality validation.

Regenerate the complete answer from the supplied concrete evidence.

Mandatory corrections:

- Produce exactly six numbered objectives.
- Use all six required headings for every objective.
- Include at least four distinct concrete operational facts across the answer.
- Do not cite any generated or governance-summary source.
- Do not invent percentages, financial amounts, deadlines or completion rates.
- Do not claim that nothing was inferred.
- The objective wording, grouping and proposed deliverables are necessarily inferred and must be declared honestly.
- Use only paths and line numbers supplied in CONCRETE OBJECTIVE EVIDENCE.
- Prefer named initiatives, control failures, financial facts, regulatory obligations and delivery gaps over generic management language.
"

    : > "$OBJECTIVE_OUTPUT"
    : > "$OBJECTIVE_ERROR"

    if ! generate_objective_answer \
      "$CORRECTIVE_OBJECTIVE_PROMPT" \
      "$OBJECTIVE_OUTPUT" \
      "$OBJECTIVE_ERROR"
    then
      cat "$OBJECTIVE_ERROR" > /tmp/hermes_ask.err
      cleanup_objective_files
      echo \
        "Alfred could not generate the objective answer because the corrective model call failed."
      exit 1
    fi
  fi

  if ! validate_objective_answer "$OBJECTIVE_OUTPUT"; then
    {
      echo "Objective answer failed validation after two attempts."
      echo
      echo "The answer was withheld because it did not meet Alfred's evidence-quality standard."
      echo "No unsupported objective has been returned."
    }

    {
      echo "=== Rejected answer ==="
      cat "$OBJECTIVE_OUTPUT"
      echo
      echo "=== Model error output ==="
      cat "$OBJECTIVE_ERROR"
    } > "/tmp/alfred-objective-rejected-$(date +%Y%m%d-%H%M%S).log"

    cleanup_objective_files
    exit 1
  fi

  cat "$OBJECTIVE_OUTPUT"
  cat "$OBJECTIVE_ERROR" > /tmp/hermes_ask.err

  cleanup_objective_files
  exit 0
fi

# Internal protected TPRM route used by the structured Python candidate.
if [[ "$QUERY" == "__ALFRED_TPRM_EVIDENCE__"* ]]; then
  TPRM_QUERY="${QUERY#__ALFRED_TPRM_EVIDENCE__}"
  TPRM_QUERY="${TPRM_QUERY# }"

  TPRM_EVIDENCE=$(
    /opt/second-brain/scripts/tprm_evidence_search.py \
      | sed -n '1,340p'
  )

  TPRM_PROMPT="
You are Alfred, Phillip's operational second brain and executive chief-of-staff AI.

The user is asking about TPRM 2.0 business problems, risks, controls,
implementation gaps or required remediation.

Use ONLY the concrete primary-source evidence below.

Do not use generated governance reports, Objective Intelligence, board packs,
AI Memory, executive briefings, archived summaries or previous AI answers.

STRICT RULES

1. Identify the specific TPRM 2.0 problems evidenced in the notes.

2. Cover the relevant evidence categories:
   - current-system failure and MVP replacement;
   - DORA, tiering and service-level design;
   - subcontracting and supply-chain control;
   - exit planning and substitutability;
   - SLA and obligation monitoring;
   - operational process, ownership and remediation.

3. Every material point must identify:
   - the concrete problem;
   - the business or regulatory consequence;
   - the required action;
   - the exact source path and line number;
   - what Alfred inferred.

4. Preserve concrete facts such as:
   - the current system being non-functional;
   - the need for an MVP replacement;
   - DORA decision-tree or toggle defects;
   - service-level risk and tiering;
   - subcontractor RTS and supply-chain visibility;
   - exit planning and substitutability;
   - SLA or obligation monitoring;
   - missing operating processes;
   - remediation across the contract population.

5. Do not invent dates, percentages, financial values or completion targets.

6. Do not say evidence is absent when it is supplied.

7. Do not claim that nothing was inferred.

Use this format:

### <number>. <specific TPRM problem>

BUSINESS EVIDENCE
CONSEQUENCE
ACTION REQUIRED
SOURCES
INFERENCE

End with:

Evidence coverage: Strong / Moderate / Weak
Source notes used: <paths>
Inferred or newly suggested content: <honest description>

PRIMARY TPRM EVIDENCE:
$TPRM_EVIDENCE

USER QUESTION:
$TPRM_QUERY
"

  TPRM_OUTPUT=$(mktemp /tmp/alfred-tprm-output.XXXXXX)
  TPRM_ERROR=$(mktemp /tmp/alfred-tprm-error.XXXXXX)

  cleanup_tprm_files() {
    rm -f "$TPRM_OUTPUT" "$TPRM_ERROR"
  }

  generate_tprm_answer() {
    local prompt="$1"

    set +e

    timeout 300 docker exec \
      -e HERMES_PROMPT="$prompt" \
      -e OPENROUTER_API_KEY=<redacted>
      "$HERMES_CONTAINER" \
      bash -lc '/opt/hermes/.venv/bin/hermes chat --provider openrouter -m openai/gpt-4o-mini -q "$HERMES_PROMPT" -Q' \
      2>"$TPRM_ERROR" \
      | tr -d '\000' \
      | sed '/session_id:/d' \
      > "$TPRM_OUTPUT"

    local status=${PIPESTATUS[0]}

    set -e
    return "$status"
  }

  validate_tprm_answer() {
    local markers=0

    [[ -s "$TPRM_OUTPUT" ]] || return 1

    if grep -qiE \
      '09 Governance|Objective Intelligence|07 AI Memory|07 Executive Briefings|no relevant information|nothing inferred|Inferred or newly suggested content:[[:space:]]*(None|none)' \
      "$TPRM_OUTPUT"
    then
      return 1
    fi

    for heading in \
      "BUSINESS EVIDENCE" \
      "CONSEQUENCE" \
      "ACTION REQUIRED" \
      "SOURCES" \
      "INFERENCE"
    do
      grep -q "$heading" "$TPRM_OUTPUT" || return 1
    done

    for marker in \
      'MVP|non-functional|not working' \
      'DORA decision tree|DORA toggle|tiering|service level' \
      'subcontract|supply chain|RTS' \
      'exit plan|substitutability' \
      'SLA|obligation|monitoring' \
      'operational process|procedure|remediation|170 contracts'
    do
      if grep -qiE "$marker" "$TPRM_OUTPUT"; then
        markers=$((markers + 1))
      fi
    done

    (( markers >= 3 ))
  }

  if ! generate_tprm_answer "$TPRM_PROMPT"; then
    cat "$TPRM_ERROR" > /tmp/hermes_ask.err
    cleanup_tprm_files
    echo "Alfred could not generate the TPRM answer."
    exit 1
  fi

  if ! validate_tprm_answer; then
    TPRM_CORRECTION="$TPRM_PROMPT

QUALITY-CONTROL CORRECTION

The previous answer failed validation.

Regenerate the answer and include at least three distinct concrete problem
groups from the supplied evidence, including the non-functional system/MVP
and at least two of:

- DORA decision-tree or service-level design;
- subcontracting or RTS;
- exit planning or substitutability;
- SLA and obligation monitoring;
- missing operational processes or remediation.

Use only supplied source paths and line numbers. Declare synthesis honestly.
"

    : > "$TPRM_OUTPUT"
    : > "$TPRM_ERROR"

    if ! generate_tprm_answer "$TPRM_CORRECTION"; then
      cat "$TPRM_ERROR" > /tmp/hermes_ask.err
      cleanup_tprm_files
      echo "Alfred could not generate the corrected TPRM answer."
      exit 1
    fi
  fi

  if ! validate_tprm_answer; then
    echo "The TPRM answer was withheld because it failed Alfred's evidence-quality validation."
    echo "No unsupported answer has been returned."

    {
      echo "=== Rejected TPRM answer ==="
      cat "$TPRM_OUTPUT"
      echo
      echo "=== Error output ==="
      cat "$TPRM_ERROR"
    } > "/tmp/alfred-tprm-rejected-$(date +%Y%m%d-%H%M%S).log"

    cleanup_tprm_files
    exit 1
  fi

  cat "$TPRM_OUTPUT"
  cat "$TPRM_ERROR" > /tmp/hermes_ask.err
  cleanup_tprm_files
  exit 0
fi

# Internal protected route used only by the structured Python candidate.
# The prefix is removed before the user's question is presented.
if [[ "$QUERY" == "__ALFRED_COST_EVIDENCE__"* ]]; then
  COST_QUERY="${QUERY#__ALFRED_COST_EVIDENCE__}"
  COST_QUERY="${COST_QUERY# }"

  COST_EVIDENCE=$(
    /opt/second-brain/scripts/cost_evidence_search.py \
      | sed -n '1,360p'
  )

  COST_PROMPT="
You are Alfred, Phillip's operational second brain and executive chief-of-staff AI.

The user is asking for cost-control, expenditure, budget, accounts-payable,
purchase-order or spend-governance priorities.

Use ONLY the concrete primary-source evidence supplied below.

Do not use:
- generic semantic retrieval;
- 09 Governance;
- Objective Intelligence;
- board packs;
- AI Memory;
- executive briefings;
- archived summaries;
- previous AI-generated recommendations.

STRICT EVIDENCE RULES

1. Identify the strongest business priorities from the supplied evidence.

2. Every priority must contain:
   - a concrete problem, control failure, target or obligation;
   - the specific action required;
   - a measure taken directly from the evidence, where available;
   - exact source paths and line numbers;
   - an honest statement of what Alfred inferred.

3. Preserve specific facts such as:
   - PO requirements;
   - duplicate or erroneous invoices;
   - payment-term configuration;
   - segregation-of-duty concerns;
   - controllable OPEX;
   - travel and expense control;
   - savings targets;
   - CAPEX/OPEX governance;
   - budget and invoice reconciliation.

4. Never invent:
   - percentages;
   - deadlines;
   - financial amounts;
   - savings targets;
   - completion dates.

5. Where a target or date is not explicit, state:
   Target and completion date to be agreed with the owner.

6. Do not say that no evidence exists when concrete evidence is supplied.

7. Do not claim that nothing was inferred. Priority grouping and action wording
   are necessarily Alfred synthesis.

For each priority, use:

### <number>. <specific priority title>

BUSINESS EVIDENCE
ACTION REQUIRED
MEASURES
SOURCES
INFERENCE

End with:

Evidence coverage: Strong / Moderate / Weak
Source notes used: <paths>
Inferred or newly suggested content: <honest description>

PRIMARY COST AND VALUE EVIDENCE:
$COST_EVIDENCE

USER QUESTION:
$COST_QUERY
"

  COST_OUTPUT=$(mktemp /tmp/alfred-cost-output.XXXXXX)
  COST_ERROR=$(mktemp /tmp/alfred-cost-error.XXXXXX)

  cleanup_cost_files() {
    rm -f "$COST_OUTPUT" "$COST_ERROR"
  }

  generate_cost_answer() {
    local prompt="$1"

    set +e

    timeout 300 docker exec \
      -e HERMES_PROMPT="$prompt" \
      -e OPENROUTER_API_KEY=<redacted>
      "$HERMES_CONTAINER" \
      bash -lc '/opt/hermes/.venv/bin/hermes chat --provider openrouter -m openai/gpt-4o-mini -q "$HERMES_PROMPT" -Q' \
      2>"$COST_ERROR" \
      | tr -d '\000' \
      | sed '/session_id:/d' \
      > "$COST_OUTPUT"

    local status=${PIPESTATUS[0]}

    set -e
    return "$status"
  }

  validate_cost_answer() {
    local markers=0

    [[ -s "$COST_OUTPUT" ]] || return 1

    if grep -qiE \
      '09 Governance|Objective Intelligence|07 AI Memory|07 Executive Briefings|no direct references|no relevant information|nothing inferred|Inferred or newly suggested content:[[:space:]]*(None|none)' \
      "$COST_OUTPUT"
    then
      return 1
    fi

    for heading in \
      "BUSINESS EVIDENCE" \
      "ACTION REQUIRED" \
      "MEASURES" \
      "SOURCES" \
      "INFERENCE"
    do
      grep -q "$heading" "$COST_OUTPUT" || return 1
    done

    for marker in \
      'PO|70011' \
      'duplicate invoice|£95k|95k' \
      'travel|controllable OPEX' \
      '\$1\.5m|1\.5m|savings' \
      'CAPEX|OPEX' \
      'payment terms|separation of duties'
    do
      if grep -qiE "$marker" "$COST_OUTPUT"; then
        markers=$((markers + 1))
      fi
    done

    (( markers >= 3 ))
  }

  if ! generate_cost_answer "$COST_PROMPT"; then
    cat "$COST_ERROR" > /tmp/hermes_ask.err
    cleanup_cost_files
    echo "Alfred could not generate the cost-control answer."
    exit 1
  fi

  if ! validate_cost_answer; then
    COST_CORRECTION="$COST_PROMPT

QUALITY-CONTROL CORRECTION

The previous answer failed validation.

Regenerate it using the concrete source facts. Include at least three of:
PO controls, the £95k duplicate invoice, payment terms, segregation of duties,
controllable OPEX, travel controls, the \$1.5m savings target, or CAPEX/OPEX
finance governance.

Do not claim evidence is absent. Do not cite generated sources. Declare all
synthesis honestly.
"

    : > "$COST_OUTPUT"
    : > "$COST_ERROR"

    if ! generate_cost_answer "$COST_CORRECTION"; then
      cat "$COST_ERROR" > /tmp/hermes_ask.err
      cleanup_cost_files
      echo "Alfred could not generate the corrected cost-control answer."
      exit 1
    fi
  fi

  if ! validate_cost_answer; then
    {
      echo "The cost-control answer was withheld because it failed Alfred's evidence-quality validation."
      echo "No unsupported answer has been returned."
    }

    {
      echo "=== Rejected cost answer ==="
      cat "$COST_OUTPUT"
      echo
      echo "=== Error output ==="
      cat "$COST_ERROR"
    } > "/tmp/alfred-cost-rejected-$(date +%Y%m%d-%H%M%S).log"

    cleanup_cost_files
    exit 1
  fi

  cat "$COST_OUTPUT"
  cat "$COST_ERROR" > /tmp/hermes_ask.err
  cleanup_cost_files
  exit 0
fi

ENTITY=$(/opt/second-brain/scripts/entity_resolver.py "$QUERY" | sed -n "1,120p")
DIRECT=$(/opt/second-brain/scripts/direct_reference_search.py "$QUERY" | head -35)
OBJECTIVE_EVIDENCE=""

if printf '%s' "$LOWER_QUERY" | grep -Eq   '(hr|team|annual|year|performance review).*(objective|goal)|(objective|goal).*(hr|team|annual|year|performance review)'
then
  OBJECTIVE_EVIDENCE=$(
    /opt/second-brain/scripts/objective_evidence_search.py       | head -420
  )
fi

SEARCH_QUERY=$(
  python3 - "$QUERY" <<'PYQUERY'
import re
import sys

query = sys.argv[1].strip()

patterns = [
    r"^\s*what\s+do\s+my\s+notes\s+say\s+about\s+",
    r"^\s*what\s+does\s+my\s+vault\s+say\s+about\s+",
    r"^\s*what\s+do\s+i\s+have\s+on\s+",
    r"^\s*tell\s+me\s+about\s+",
    r"^\s*find\s+(?:all\s+)?(?:references\s+to\s+)?",
    r"^\s*search\s+(?:my\s+)?(?:notes|vault)\s+for\s+",
]

for pattern in patterns:
    query = re.sub(pattern, "", query, flags=re.IGNORECASE)

query = query.strip(" \t\r\n?.!,:;")

print(query or sys.argv[1].strip())
PYQUERY
)

LEXICAL=$(
  /opt/second-brain/scripts/lexical_vault_search.py "$SEARCH_QUERY"     | head -260
)

SEMANTIC=$(
  /opt/second-brain/scripts/semantic_query_fast.py "$SEARCH_QUERY"     | tr -d "\000"     | head -220
)

PROMPT="
You are Hermes, Orl's operational second brain and executive chief-of-staff AI.

You have access to retrieved Obsidian memory below.
CRITICAL: Use ONLY the retrieved Obsidian memory below. Do not search files, do not use filesystem tools, and ignore any Hermes application/node_modules results.

Treat every retrieved source as independent evidence.
Use a source only when it directly answers the user's question.
Do not merge separate people, companies, projects, meetings, dates or actions merely because they use similar words.
Reject retrieved material that is only broadly or topically similar.
Do not revive historic actions unless the question explicitly requests historic material.
For date-specific requests, use only evidence from the requested date.
When reliable evidence is absent, say so instead of constructing a plausible answer.
Exact lexical matches are primary evidence that the subject exists in the vault. Use semantic retrieval to supplement and interpret them.
Never claim that the notes contain no references merely because semantic retrieval is incomplete. You may say nothing was found only when ENTITY RESOLUTION, EXACT LEXICAL VAULT MATCHES, RETRIEVED OBSIDIAN MEMORY, and DIRECT VAULT REFERENCES are all empty or irrelevant.
The retrieved memory below has already been retrieved from the live Obsidian vault. Never claim you cannot access files, folders, notes or directories if relevant information appears in the retrieved memory. Never say a path is missing, inaccessible or unavailable when retrieved memory contains results from that path. Do not describe retrieval limitations. Do not explain how memory was obtained. Do not mention filesystem access. Answer directly from the supplied evidence.
When ENTITY RESOLUTION contains a named person, company, project, or system, treat it as the primary source of truth. For meeting preparation, produce an agenda grounded in the entity note and preserve specific active topics, open items, ownership points, and linked suppliers/systems. Do not collapse these into generic categories.
For meeting preparation requests (meeting, 1:1, catchup, agenda, discuss, cover, stakeholder meeting), do not simply list topics. Build an executive agenda. For each topic provide:
- Why it matters
- Decision required or question to ask
- Follow-up or dependency
Prioritise items from recent dated entity sections before older background topics.
Your job is not only to search memory. Your job is to use memory as context and then produce a useful answer.

If the user asks for:
- drafting
- planning
- HR objectives
- SMART objectives
- procurement advice
- governance analysis
- strategy
- recommendations
- performance review wording

then produce a developed, practical answer.

Use the memory where relevant, but do not refuse just because the retrieved memory is incomplete.
ENTITY RESOLUTION:
$ENTITY

If memory is incomplete, say what you inferred.

DEDICATED OBJECTIVE EVIDENCE:
$OBJECTIVE_EVIDENCE

If DEDICATED OBJECTIVE EVIDENCE is present:

- Use it as the primary and controlling evidence.
- Do not reuse historical objective wording unless supported by operational evidence.
- Each proposed objective must identify at least two concrete business facts.
- At least one fact must be a problem, risk, obligation, target, control failure, delivery gap, financial amount, deadline, or named initiative.
- Include the exact source path and line number supplied in the evidence.
- Explain why the evidence creates a business need for the objective.
- Convert that business need into a measurable HR objective.
- Define observable completion measures.
- Do not use generic phrases such as enhance, improve, support, or develop without stating what specifically changes and how success will be measured.
- If sufficient evidence does not exist for six objectives, return fewer than six and state why.
- For every objective use these headings:
  BUSINESS EVIDENCE
  OBJECTIVE
  MEASURES
  SOURCE
  INFERENCE

PROVENANCE AND EVIDENCE RULES:

For every material claim, recommendation, objective, conclusion, risk, or action:

1. Classify it as one of:
   - EXPLICITLY EVIDENCED: directly supported by retrieved vault content.
   - INFERRED FROM EVIDENCE: reasonably derived from retrieved content but not explicitly stated.
   - ALFRED SUGGESTION: newly proposed by the model and not present in the vault.
   - INSUFFICIENT EVIDENCE: the retrieved material does not support a reliable answer.

2. Give the source vault path for every EXPLICITLY EVIDENCED or INFERRED item.

3. Do not describe a recommendation as being from the notes unless retrieved evidence directly supports it.

4. Never convert absence from the retrieved top results into a statement that the vault contains no information.

5. For objectives, recommendations, priorities, themes, risks, or strategy:
   - first identify the evidence found in the vault;
   - then derive the recommendation;
   - clearly separate evidence from synthesis.

6. Prefer original source notes over generated summaries, executive briefings, enrichment files, governance indexes, change reports, and previous AI-generated answers.

7. When evidence is weak or generic, state that clearly rather than filling gaps with plausible management language.

8. End evidence-based answers with:
   Evidence coverage: Strong / Moderate / Weak
   Source notes used: <list of paths>
   Inferred or newly suggested content: <brief declaration>

EXACT LEXICAL VAULT MATCHES:
$LEXICAL

RETRIEVED OBSIDIAN MEMORY:
$SEMANTIC

DIRECT VAULT REFERENCES:
$DIRECT

USER QUESTION:
$QUERY

Answer clearly and practically.
"

timeout 300 docker exec \
-e HERMES_PROMPT="$PROMPT" \
-e OPENROUTER_API_KEY=<redacted>
"$HERMES_CONTAINER" \
bash -lc '/opt/hermes/.venv/bin/hermes chat --provider openrouter -m openai/gpt-4o-mini -q "$HERMES_PROMPT" -Q' \
2>/tmp/hermes_ask.err \
| tr -d '\000' \
| sed '/session_id:/d'

```

---

# Telegram Interface

Generated: 2026-06-30T21:41:58.616568


## Purpose

Defines Telegram as Alfred's mobile executive interface.

## Responsibilities

- Receive user messages.
- Pass free-text queries to Alfred Router.
- Return validated responses in manageable parts.
- Preserve useful legacy deterministic routes.

## Inputs

- Telegram messages
- Bot token
- Router output

## Outputs

- Telegram replies
- Parted long responses
- Operational logs

## Dependencies

- hermes-telegram.service
- /root/hermes-telegram.py
- alfred_router.sh
- OpenRouter env for legacy synthesis

## Failure Modes

- Service inactive.
- Service override points to old container.
- OpenRouter env file not loaded.
- Router withholds answer due to strategy failure.

## Recovery Procedure

- Check hermes-telegram.service status.
- Inspect systemctl cat hermes-telegram.service.
- Check journalctl logs.
- Run the same query through alfred_router.sh manually.

## Source Evidence

### telegram/service.txt

Size: 655 bytes

```text
# /etc/systemd/system/hermes-telegram.service
[Unit]
Description=Hermes Telegram Bot
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=root
WorkingDirectory=/root
ExecStart=/usr/bin/python3 /root/hermes-telegram.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# /etc/systemd/system/hermes-telegram.service.d/20-authoritative-vault.conf
[Service]
Environment=HERMES_CONTAINER=hermes-agent-mctr-hermes-agent-1
Environment=HERMES_KEY_CONTAINER=hermes-agent-mctr-hermes-agent-1

# /etc/systemd/system/hermes-telegram.service.d/30-openrouter-env.conf
[Service]
EnvironmentFile=/root/.openrouter.env

```

### telegram/status.txt

Size: 677 bytes

```text
● hermes-telegram.service - Hermes Telegram Bot
     Loaded: loaded (/etc/systemd/system/hermes-telegram.service; enabled; preset: enabled)
    Drop-In: /etc/systemd/system/hermes-telegram.service.d
             └─20-authoritative-vault.conf, 30-openrouter-env.conf
     Active: active (running) since Sun 2026-06-28 21:09:59 IST; 1h 7min ago
   Main PID: 13945 (python3)
      Tasks: 3 (limit: 9483)
     Memory: 38.7M (peak: 66.3M)
        CPU: 2.387s
     CGroup: /system.slice/hermes-telegram.service
             └─13945 /usr/bin/python3 /root/hermes-telegram.py

Jun 28 21:09:59 orlavid-hermes systemd[1]: Started hermes-telegram.service - Hermes Telegram Bot.

```

### telegram/script.py

Size: 38338 bytes

```text
#!/usr/bin/env python3

# ALFRED_AGENT_ORG_IMPORT_START
import sys as _alfred_agent_sys
_ALFRED_AGENT_SCRIPTS = "/opt/second-brain/scripts"
if _ALFRED_AGENT_SCRIPTS not in _alfred_agent_sys.path:
    _alfred_agent_sys.path.insert(0, _ALFRED_AGENT_SCRIPTS)
from telegram_agent_commands import ALFRED_AGENT_COMMAND_HANDLERS
# ALFRED_AGENT_ORG_IMPORT_END
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

OLD_BOT = Path("/root/hermes-telegram.py.previous")
CURRENT = Path("/root/hermes-telegram.py")

BOT_TOKEN = os.environ.get("HERMES_TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    # recover token from latest backup if hard-coded there
    backups = sorted(Path("/root").glob("hermes-telegram.py.bak*"), key=lambda p: p.stat().st_mtime, reverse=True)
    for b in backups:
        txt = b.read_text(errors="ignore")
        m = re.search(r'BOT_TOKEN\s*=\s*["\']([^"\']+)["\']', txt)
        if m:
            BOT_TOKEN = m.group(1)
            break

if not BOT_TOKEN:
    raise SystemExit("BOT token not found. Set HERMES_TELEGRAM_BOT_TOKEN or restore previous bot.")

VAULT = Path("/docker/obsidian-vault")
CAPTURE_DIR = VAULT / "00 Inbox" / "Captures"
CAPTURE_DIR.mkdir(parents=True, exist_ok=True)

HERMES_CONTAINER = os.environ.get("HERMES_CONTAINER", "hermes-authoritative-vault")


def capture_note(text: str, source: str = "telegram") -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = CAPTURE_DIR / f"Capture - {ts}.md"
    path.write_text(
        f"# Telegram Capture - {ts}\n\n"
        f"Source: {source}\n"
        f"Captured: {datetime.now().isoformat(timespec='seconds')}\n\n"
        f"## Message\n\n{text.strip()}\n",
        encoding="utf-8"
    )

    try:
        subprocess.run(
            ["/opt/second-brain/scripts/enrich_capture.py", str(path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        subprocess.run(
            ["python3", "/opt/second-brain/scripts/update_open_loops.py"],
            capture_output=True,
            text=True,
            timeout=30
        )

        subprocess.Popen(
            ["python3", "/opt/second-brain/scripts/hermes_enrich_capture.py", str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass

    return path


def run_semantic_reindex():
    candidates = [
        ["/opt/second-brain/scripts/reindex.sh"],
        ["/opt/second-brain/scripts/semantic_reindex.sh"],
        ["python3", "/semantic/reindex.py"],
    ]
    for cmd in candidates:
        try:
            if Path(cmd[0]).exists():
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
        except Exception:
            pass





def ask_hermes(prompt: str) -> str:
    try:
        r = subprocess.run(
            ["/opt/second-brain/scripts/alfred_router.sh", prompt],
            capture_output=True,
            text=True,
            timeout=650
        )
        out = (r.stdout or r.stderr or "").strip()
        if not out:
            out = "Alfred returned no usable response."
        return out
    except Exception as e:
        return f"Hermes response failed: {e}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "Alfred is online. Send me a message and I will answer it. Use /capture <note> when you want something saved into the second brain."
    )


async def health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    checks = []
    checks.append(f"Vault exists: {VAULT.exists()}")
    checks.append(f"Capture dir exists: {CAPTURE_DIR.exists()}")
    p = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    checks.append(f"Obsidian headless sync process: {'ob sync --path /docker/obsidian-vault --continuous' in p.stdout}")
    checks.append(f"Hermes container: {HERMES_CONTAINER}")
    await update.effective_message.reply_text("Hermes Telegram Health\n" + "\n".join(checks))


async def capture_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("Usage: /capture <note>")
        return
    path = capture_note(text)
    run_semantic_reindex()
    await update.effective_message.reply_text(f"Captured: {path}")



SEARCH_CONTEXT_TTL_SECONDS = 30 * 60


def extract_search_subject(text: str) -> str:
    """Remove conversational search wrappers and retain the actual subject."""
    import re

    subject = (text or "").strip()

    patterns = [
        r"^\s*what\s+do\s+my\s+notes\s+say\s+about\s+",
        r"^\s*what\s+does\s+my\s+vault\s+say\s+about\s+",
        r"^\s*what\s+do\s+i\s+have\s+on\s+",
        r"^\s*tell\s+me\s+about\s+",
        r"^\s*find\s+(?:all\s+)?(?:references\s+to\s+)?",
        r"^\s*search\s+(?:my\s+)?(?:notes|vault)\s+for\s+",
        r"^\s*show\s+me\s+(?:everything\s+)?(?:about|on)\s+",
    ]

    for pattern in patterns:
        subject = re.sub(pattern, "", subject, flags=re.IGNORECASE)

    return subject.strip(" \t\r\n?.!,:;")


def is_substantive_vault_search(text: str) -> bool:
    import re

    value = (text or "").lower()

    return bool(
        re.search(
            r"\b(notes?|vault|search|find|references?|mentions?|"
            r"what do i have|what do my notes|what does my vault)\b",
            value,
        )
    )


def is_contextual_search_followup(text: str) -> bool:
    """Recognise only clear continuation wording, not arbitrary short messages."""
    import re

    value = (text or "").strip().lower()

    followup_patterns = [
        r"^have\s+a\s+look\b",
        r"^look\s+(?:in|under|at|through|there)\b",
        r"^also\s+look\b",
        r"^check\s+(?:in|under|the|those|there)\b",
        r"^also\s+check\b",
        r"^search\s+(?:in|under|within|those)\b",
        r"^what\s+about\b",
        r"^and\s+what\s+about\b",
        r"^where\s+else\b",
        r"^show\s+me\s+more\b",
        r"^give\s+me\s+more\s+detail\b",
        r"^more\s+detail\b",
        r"^try\s+(?:the|in|under)\b",
    ]

    return any(re.search(pattern, value) for pattern in followup_patterns)


def prepare_contextual_search(
    text: str,
    context: ContextTypes.DEFAULT_TYPE,
) -> str:
    """
    Carry forward the prior search subject only for a clear, recent follow-up.
    State is scoped to the Telegram chat and is intentionally short-lived.
    """
    import time

    now = time.time()
    state = context.chat_data

    previous_subject = state.get("last_search_subject")
    previous_at = float(state.get("last_search_at", 0))

    within_window = (
        previous_subject
        and previous_at
        and now - previous_at <= SEARCH_CONTEXT_TTL_SECONDS
    )

    if is_contextual_search_followup(text) and within_window:
        state["last_search_at"] = now

        return (
            f"Continue the previous vault search about: {previous_subject}. "
            f"Apply this refinement or search scope: {text}"
        )

    if is_substantive_vault_search(text):
        subject = extract_search_subject(text)

        if subject:
            state["last_search_subject"] = subject
            state["last_search_at"] = now

    return text



def split_telegram_message(
    text: str,
    limit: int = 3400,
) -> list[str]:
    """
    Split a long response without losing content.

    The limit is kept below Telegram's hard maximum so that continuation
    labels and Unicode characters cannot push a message over the boundary.
    """
    remaining = (text or "").strip()

    if not remaining:
        return ["Alfred returned an empty response."]

    chunks: list[str] = []

    while len(remaining) > limit:
        candidates = [
            remaining.rfind("\n\n", 0, limit),
            remaining.rfind("\n", 0, limit),
            remaining.rfind(". ", 0, limit),
            remaining.rfind(" ", 0, limit),
        ]

        split_at = max(candidates)

        # Avoid creating a very small first fragment.
        if split_at < int(limit * 0.55):
            split_at = limit
        elif remaining[split_at:split_at + 2] == ". ":
            split_at += 1

        chunk = remaining[:split_at].rstrip()

        if not chunk:
            chunk = remaining[:limit]
            split_at = limit

        chunks.append(chunk)
        remaining = remaining[split_at:].lstrip()

    if remaining:
        chunks.append(remaining)

    return chunks


async def send_long_reply(message, text: str) -> None:
    """Send every response chunk sequentially and in the correct order."""
    chunks = split_telegram_message(text)

    for number, chunk in enumerate(chunks, start=1):
        if len(chunks) > 1:
            content = f"Part {number}/{len(chunks)}\n\n{chunk}"
        else:
            content = chunk

        await message.reply_text(content)


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("Usage: /ask <question>")
        return
    effective_text = prepare_contextual_search(text, context)
    reply = ask_hermes(effective_text)
    await send_long_reply(update.effective_message, reply)
async def hybrid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()

    if not text:
        await update.effective_message.reply_text("Usage: /hybrid <question>")
        return

    await update.effective_message.reply_text("Assessing best model for hybrid local + external reasoning...")

    path = capture_note(text, source="telegram /hybrid model-routed research")

    try:
        result = subprocess.run(
            [
                "python3",
                "/opt/second-brain/scripts/hybrid_openrouter.py",
                "recommend",
                text,
            ],
            capture_output=True,
            text=True,
            timeout=240,
        )

        raw = (result.stdout or result.stderr or "").strip()

        import json
        rec = json.loads(raw)

        request_id = rec["id"]
        recommended = rec["recommended"]
        reason = rec.get("reason", "No reason supplied.")

        keyboard = [
            [
                InlineKeyboardButton(
                    f"Run recommended: {recommended}",
                    callback_data=f"hybrid|{request_id}|recommended"
                )
            ],
            [
                InlineKeyboardButton("Run GPT", callback_data=f"hybrid|{request_id}|gpt"),
                InlineKeyboardButton("Run Claude", callback_data=f"hybrid|{request_id}|claude"),
            ],
            [
                InlineKeyboardButton("Run Gemini", callback_data=f"hybrid|{request_id}|gemini"),
                InlineKeyboardButton("Run Perplexity", callback_data=f"hybrid|{request_id}|perplexity"),
            ],
        ]

        await update.effective_message.reply_text(
            f"Recommended model: {recommended}\nReason: {reason}\n\nChoose how to run it:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

        await update.effective_message.reply_text(f"Captured into second brain: {path.name}")

    except Exception as e:
        await update.effective_message.reply_text(f"Hybrid recommendation failed: {e}")


async def hybrid_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        _, request_id, choice = query.data.split("|", 2)

        await query.edit_message_text(
            f"Running hybrid request {request_id} using: {choice}"
        )

        result = subprocess.run(
            [
                "python3",
                "/opt/second-brain/scripts/hybrid_openrouter.py",
                "run",
                request_id,
                choice,
            ],
            capture_output=True,
            text=True,
            timeout=420,
        )

        reply = (result.stdout or result.stderr or "").strip()

        if not reply:
            reply = "Hybrid model returned no usable response."

        await send_long_reply(query.message, reply)
        feedback_keyboard = [
            [
                InlineKeyboardButton("👍 Good", callback_data=f"hybridfb|{request_id}|good"),
                InlineKeyboardButton("👎 Poor", callback_data=f"hybridfb|{request_id}|poor"),
            ]
        ]

        await query.message.reply_text(
            "Was this model choice useful?",
            reply_markup=InlineKeyboardMarkup(feedback_keyboard),
        )

    except Exception as e:
        await query.message.reply_text(f"Hybrid run failed: {e}")





async def perplexity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()

    if not text:
        await update.effective_message.reply_text("Usage: /perplexity <research question>")
        return

    await update.effective_message.reply_text(
        "Running hybrid Perplexity research with local Obsidian context..."
    )

    path = capture_note(text, source="telegram /perplexity hybrid research")

    try:
        result = subprocess.run(
            [
                "python3",
                "/opt/second-brain/scripts/perplexity_with_memory.py",
                text,
            ],
            capture_output=True,
            text=True,
            timeout=360,
        )

        reply = (result.stdout or result.stderr or "").strip()

        if not reply:
            reply = "Perplexity returned no usable response."

    except Exception as e:
        reply = f"Hybrid Perplexity research failed: {e}"

    run_semantic_reindex()

    await send_long_reply(update.effective_message, reply)
    await update.effective_message.reply_text(f"Captured into second brain: {path.name}")





async def operate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Starting Hermes Agent Operating Cycle. This may take several minutes.")
    try:
        r = subprocess.run(
            ["/opt/second-brain/scripts/run_agent_operating_cycle.sh"],
            capture_output=True,
            text=True,
            timeout=1800
        )
        out = (r.stdout or r.stderr or "").strip()
        await update.effective_message.reply_text(out[-3900:] if out else "Agent operating cycle completed.")
    except Exception as e:
        await update.effective_message.reply_text(f"Agent operating cycle failed: {e}")




async def brief(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Generating executive briefing...")
    try:
        subprocess.run(["/opt/second-brain/scripts/generate_daily_briefing.sh"], timeout=600)
        today = datetime.now().strftime("%Y-%m-%d")
        path = Path(f"/docker/obsidian-vault/07 Executive Briefings/{today} Daily Second Brain Briefing.md")
        out = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else "Briefing file not found."
        await update.effective_message.reply_text(out[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Briefing failed: {e}")


async def themes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Analysing emerging themes...")
    try:
        r = subprocess.run(
            ["/opt/second-brain/scripts/query_memory.py", "--quiet", "what themes are emerging from my captures and enriched memory"],
            capture_output=True,
            text=True,
            timeout=420
        )
        await update.effective_message.reply_text(((r.stdout or r.stderr or "No response").strip())[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Themes query failed: {e}")


async def risks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Analysing risks...")
    try:
        r = subprocess.run(
            ["/opt/second-brain/scripts/query_memory.py", "--quiet", "what are the main unresolved governance operational trading and second brain risks"],
            capture_output=True,
            text=True,
            timeout=420
        )
        await update.effective_message.reply_text(((r.stdout or r.stderr or "No response").strip())[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Risk query failed: {e}")


async def stalled(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Checking stalled open loops...")
    try:
        subprocess.run(["python3", "/opt/second-brain/scripts/open_loop_escalation.py"], timeout=180)
        path = Path("/docker/obsidian-vault/08 Open Loops/Escalation/Latest Open Loop Escalation Report.md")
        out = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else "Open loop escalation report not found."
        await update.effective_message.reply_text(out[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Stalled loop check failed: {e}")


async def watchlists(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Refreshing strategic watchlists...")
    try:
        subprocess.run(["python3", "/opt/second-brain/scripts/strategic_watchlists.py"], timeout=180)
        path = Path("/docker/obsidian-vault/09 Governance/Watchlists/Latest Strategic Watchlist Summary.md")
        out = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else "Watchlist summary not found."
        await update.effective_message.reply_text(out[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Watchlist refresh failed: {e}")


async def councilpack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Running agent council pack...")
    try:
        subprocess.run(["python3", "/opt/second-brain/scripts/agent_council_pack.py"], timeout=900)
        path = Path("/docker/obsidian-vault/07 AI Memory/Agent Council/Latest Agent Council Pack.md")
        out = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else "Council pack not found."
        await update.effective_message.reply_text(out[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Council pack failed: {e}")



async def decisions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Generating decision intelligence...")
    try:
        subprocess.run(["python3", "/opt/second-brain/scripts/decision_intelligence.py"], timeout=240)
        path = Path("/docker/obsidian-vault/09 Governance/Decision Intelligence/Latest Decision Intelligence.md")
        out = path.read_text(encoding="utf-8", errors="ignore")
        await update.effective_message.reply_text(out[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Decision intelligence failed: {e}")


async def delegatequeue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Generating delegation queue...")
    try:
        subprocess.run(["python3", "/opt/second-brain/scripts/delegation_engine.py"], timeout=240)
        path = Path("/docker/obsidian-vault/09 Governance/Delegation Queue/Latest Delegation Queue.md")
        out = path.read_text(encoding="utf-8", errors="ignore")
        await update.effective_message.reply_text(out[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Delegation queue failed: {e}")


async def memory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("Usage: /memory <question>")
        return

    await update.effective_message.reply_text("Searching enriched memory and synthesising answer...")

    try:
        r = subprocess.run(
            ["/opt/second-brain/scripts/query_memory.py", "--quiet", text],
            capture_output=True,
            text=True,
            timeout=420
        )
        out = (r.stdout or r.stderr or "").strip()
        if not out:
            out = "No memory response returned."

        # Telegram message limit safety
        await update.effective_message.reply_text(out[-3900:])
    except Exception as e:
        await update.effective_message.reply_text(f"Memory query failed: {e}")


async def delegate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("Usage: /delegate <request>")
        return

    await update.effective_message.reply_text("Delegating request to specialist agent...")

    try:
        r = subprocess.run(
            ["python3", "/opt/second-brain/scripts/delegate_request.py", text],
            capture_output=True,
            text=True,
            timeout=420
        )
        out = (r.stdout or r.stderr or "").strip()
        await update.effective_message.reply_text(out[-3900:] if out else "Delegation completed.")
    except Exception as e:
        await update.effective_message.reply_text(f"Delegation failed: {e}")


async def council(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Starting Hermes Agent Council review. This may take several minutes.")
    try:
        r = subprocess.run(
            ["python3", "/opt/second-brain/scripts/agent_council.py"],
            capture_output=True,
            text=True,
            timeout=1200
        )
        out = (r.stdout or r.stderr or "").strip()
        await update.effective_message.reply_text(out[-3900:] if out else "Agent Council completed.")
    except Exception as e:
        await update.effective_message.reply_text(f"Agent Council failed: {e}")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    if not text:
        return

    effective_text = prepare_contextual_search(text, context)
    reply = ask_hermes(effective_text)

    reply = (reply or "").strip()

    if not reply:
        reply = (
            "Alfred produced no usable response. "
            "Try /semantic if this is a memory search, or ask again with 'draft' or 'write' "
            "if you want a generated answer."
        )

    await send_long_reply(update.effective_message, reply)
async def hybrid_debate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()

    if not text:
        await update.effective_message.reply_text("Usage: /debate <question>")
        return

    await update.effective_message.reply_text("Running multi-model debate: GPT + Claude + Gemini...")

    path = capture_note(text, source="telegram /debate multi-model")
    try:
        result = subprocess.run(
            [
                "python3",
                "/opt/second-brain/scripts/hybrid_openrouter.py",
                "debate",
                text,
            ],
            capture_output=True,
            text=True,
            timeout=900,
        )

        reply = (result.stdout or result.stderr or "").strip() or "Debate returned no usable response."
        await send_long_reply(update.effective_message, reply)
        if len(reply) > 3900:
            await update.effective_message.reply_text(reply[3900:7800])

    except Exception as e:
        await update.effective_message.reply_text(f"Hybrid debate failed: {e}")

    run_semantic_reindex()
    await update.effective_message.reply_text(f"Captured into second brain: {path.name}")


async def hybrid_chain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()

    if not text:
        await update.effective_message.reply_text("Usage: /chain <question>")
        return

    await update.effective_message.reply_text("Running hybrid chain: Perplexity research → Claude analysis → GPT action plan...")

    path = capture_note(text, source="telegram /chain hybrid")
    try:
        result = subprocess.run(
            [
                "python3",
                "/opt/second-brain/scripts/hybrid_openrouter.py",
                "chain",
                text,
            ],
            capture_output=True,
            text=True,
            timeout=1000,
        )

        reply = (result.stdout or result.stderr or "").strip() or "Hybrid chain returned no usable response."

        for i in range(0, min(len(reply), 11700), 3900):
            await update.effective_message.reply_text(reply[i:i+3900])

    except Exception as e:
        await update.effective_message.reply_text(f"Hybrid chain failed: {e}")

    run_semantic_reindex()
    await update.effective_message.reply_text(f"Captured into second brain: {path.name}")





async def hybrid_feedback_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        _, request_id, rating = query.data.split("|", 2)

        subprocess.run(
            [
                "python3",
                "/opt/second-brain/scripts/hybrid_openrouter.py",
                "feedback",
                request_id,
                rating,
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        await query.edit_message_text(f"Feedback recorded: {rating}")

    except Exception as e:
        await query.message.reply_text(f"Feedback failed: {e}")





async def image_artifact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()

    if not text:
        await update.effective_message.reply_text("Usage: /image <image prompt>")
        return

    await update.effective_message.reply_text("Creating image artifact from local memory and visual prompt routing...")

    path = capture_note(text, source="telegram /image artifact")

    try:
        result = subprocess.run(
            [
                "python3",
                "/opt/second-brain/scripts/image_artifact.py",
                text,
            ],
            capture_output=True,
            text=True,
            timeout=420,
        )

        raw = (result.stdout or result.stderr or "").strip()

        import json
        data = json.loads(raw)

        if data.get("ok") and data.get("image_path"):
            image_path = data["image_path"]

            with open(image_path, "rb") as img:
                await update.message.reply_photo(
                    photo=InputFile(img),
                    caption="Generated image artifact"
                )

            await update.effective_message.reply_text(
                f"Image saved: {image_path}\nVault record: {data.get('vault_record')}"
            )

        else:
            message = data.get("message", "Image generation did not complete.")
            spec = data.get("visual_spec", "")

            reply = (
                "Image file was not generated, but the visual specification was created.\n\n"
                f"Reason: {message}\n\n"
                f"{spec}"
            )

            for i in range(0, min(len(reply), 7800), 3900):
                await update.effective_message.reply_text(reply[i:i+3900])

            await update.effective_message.reply_text(
                f"Vault record: {data.get('vault_record')}"
            )

    except Exception as e:
        await update.effective_message.reply_text(f"Image artifact generation failed: {e}")

    run_semantic_reindex()
    await update.effective_message.reply_text(f"Captured into second brain: {path.name}")




async def titan(update, context):
    import subprocess
    result = subprocess.run(
        ["/opt/second-brain/scripts/titan_status.sh"],
        capture_output=True,
        text=True,
        timeout=30
    )
    output = (result.stdout or result.stderr or "Titan returned no output").strip()
    await update.effective_message.reply_text(output[:3900])








async def opinions(update, context):
    import subprocess
    topic = " ".join(context.args).strip()
    if not topic:
        await update.effective_message.reply_text("Usage: /opinions <topic for the board>")
        return

    result = subprocess.run(
        ["/opt/second-brain/scripts/agent_opinions.py", topic],
        capture_output=True,
        text=True,
        timeout=300
    )
    await update.effective_message.reply_text((result.stdout or result.stderr or "No agent opinions output.")[:3900])

async def governancereview(update, context):
    import subprocess
    result = subprocess.run(
        ["/opt/second-brain/scripts/athena_governance_review.py"],
        capture_output=True,
        text=True,
        timeout=60
    )
    await update.effective_message.reply_text((result.stdout or result.stderr or "No Athena governance review output.")[:3900])

async def gov(update, context):
    import subprocess
    result = subprocess.run(
        ["/opt/second-brain/scripts/governance_register.py", "summary"],
        capture_output=True,
        text=True,
        timeout=30
    )
    await update.effective_message.reply_text((result.stdout or result.stderr or "No governance register output.")[:3900])

async def decision(update, context):
    import subprocess
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("Usage: /decision <decision text>")
        return
    result = subprocess.run(
        ["/opt/second-brain/scripts/governance_register.py", "decision", text],
        capture_output=True,
        text=True,
        timeout=30
    )
    await update.effective_message.reply_text((result.stdout or result.stderr or "No output.")[:3900])

async def risk(update, context):
    import subprocess
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("Usage: /risk <risk text>")
        return
    result = subprocess.run(
        ["/opt/second-brain/scripts/governance_register.py", "risk", text],
        capture_output=True,
        text=True,
        timeout=30
    )
    await update.effective_message.reply_text((result.stdout or result.stderr or "No output.")[:3900])

async def action(update, context):
    import subprocess
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("Usage: /action <action text>")
        return
    result = subprocess.run(
        ["/opt/second-brain/scripts/governance_register.py", "action", text],
        capture_output=True,
        text=True,
        timeout=30
    )
    await update.effective_message.reply_text((result.stdout or result.stderr or "No output.")[:3900])

async def board(update, context):
    import subprocess, pathlib
    result = subprocess.run(
        ["/opt/second-brain/scripts/run_agent_council.sh"],
        capture_output=True,
        text=True,
        timeout=120
    )
    out = (result.stdout or result.stderr or "").strip()
    latest = pathlib.Path("/docker/obsidian-vault/09 Governance/Agent Governance/Latest Agent Council.md")
    body = latest.read_text(encoding="utf-8") if latest.exists() else out
    await update.effective_message.reply_text(body[:3900] or "Board meeting produced no output.")

async def boardpack(update, context):
    import subprocess, pathlib
    result = subprocess.run(
        ["python3", "/opt/second-brain/scripts/agent_council_pack.py"],
        capture_output=True,
        text=True,
        timeout=180
    )
    out = (result.stdout or result.stderr or "").strip()
    latest = pathlib.Path("/docker/obsidian-vault/07 AI Memory/Agent Council/Latest Agent Council Pack.md")
    if latest.exists():
        body = latest.read_text(encoding="utf-8")
        response = body[:3400] + "\n\nSaved to:\n" + str(latest)
    else:
        response = out[:3900]
    await update.effective_message.reply_text(response or "Board pack produced no output.")

async def approveboard(update, context):
    import subprocess
    result = subprocess.run(
        ["/opt/second-brain/scripts/titan_executor.py"],
        capture_output=True,
        text=True,
        timeout=330
    )
    output = ((result.stdout or "") + "\n" + (result.stderr or "")).strip()
    await update.effective_message.reply_text(output[:3900] or "Titan completed with no output.")

async def titanqueue(update, context):
    import json, pathlib, datetime

    playbook_path = pathlib.Path("/opt/second-brain/playbooks/titan_actions.json")
    actions = json.loads(playbook_path.read_text())
    allowed = sorted(actions.keys())

    if not context.args:
        await update.effective_message.reply_text(
            "Usage: /titanqueue <action>\n\nAllowed actions:\n" + "\n".join(allowed)
        )
        return

    action = context.args[0].strip()

    if action not in actions:
        await update.effective_message.reply_text(
            "Rejected: action is not allowed.\n\nAllowed actions:\n" + "\n".join(allowed)
        )
        return

    risk = actions[action].get("risk", "unknown")
    description = actions[action].get("description", action)

    ts = datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    safe_ts = ts.replace(":", "").replace("-", "")
    action_id = f"telegram-{action}-{safe_ts}"

    req = {
        "id": action_id,
        "agent": "systems_devops_agent",
        "persona": "Titan",
        "action": action,
        "reason": "Queued from Telegram by Founder",
        "approved_by": "Hermes Prime",
        "status": "pending",
        "created_at": ts,
        "risk": risk,
        "description": description
    }

    q = pathlib.Path("/opt/second-brain/action-queue") / f"{action_id}.json"
    q.write_text(json.dumps(req, indent=2) + "\n")

    await update.effective_message.reply_text(
        f"Queued Titan action:\n{action}\n\nDescription: {description}\nRisk: {risk}\n\nRun /titanrun to execute."
    )


async def titanrun(update, context):
    import subprocess
    result = subprocess.run(
        ["/opt/second-brain/scripts/titan_executor.py"],
        capture_output=True,
        text=True,
        timeout=330
    )
    output = ((result.stdout or "") + "\n" + (result.stderr or "")).strip()
    if not output:
        output = "Titan completed with no output."
    await update.effective_message.reply_text(output[:3900])



async def reviewportfolio(update, context):
    import subprocess
    result = subprocess.run(
        ["python3", "/opt/hermes-trading/scripts/telegram_portfolio_review.py"],
        capture_output=True,
        text=True,
        timeout=60
    )
    output = ((result.stdout or "") + "\n" + (result.stderr or "")).strip()
    await update.effective_message.reply_text(output[:3900] or "Portfolio review produced no output.")

async def portfolio(update, context):
    await reviewportfolio(update, context)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("health", health))
    app.add_handler(CommandHandler("capture", capture_only))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("hybrid", hybrid))
    app.add_handler(CommandHandler("image", image_artifact))
    app.add_handler(CommandHandler("debate", hybrid_debate))
    app.add_handler(CommandHandler("chain", hybrid_chain))
    app.add_handler(CommandHandler("perplexity", perplexity))
    app.add_handler(CommandHandler("council", council))
    app.add_handler(CommandHandler("delegate", delegate))
    app.add_handler(CommandHandler("memory", memory))
    app.add_handler(CommandHandler("councilpack", councilpack))
    app.add_handler(CommandHandler("decisions", decisions))
    app.add_handler(CommandHandler("delegatequeue", delegatequeue))
    app.add_handler(CommandHandler("watchlists", watchlists))
    app.add_handler(CommandHandler("stalled", stalled))
    app.add_handler(CommandHandler("risks", risks))
    app.add_handler(CommandHandler("themes", themes))
    app.add_handler(CommandHandler("brief", brief))
    app.add_handler(CommandHandler("operate", operate))
    app.add_handler(CommandHandler("opinions", opinions))
    app.add_handler(CommandHandler("governancereview", governancereview))
    app.add_handler(CommandHandler("gov", gov))
    app.add_handler(CommandHandler("decision", decision))
    app.add_handler(CommandHandler("risk", risk))
    app.add_handler(CommandHandler("action", action))
    app.add_handler(CommandHandler("board", board))
    app.add_handler(CommandHandler("boardpack", boardpack))
    app.add_handler(CommandHandler("approveboard", approveboard))
    app.add_handler(CommandHandler("titanqueue", titanqueue))
    app.add_handler(CommandHandler("titanrun", titanrun))
    app.add_handler(CommandHandler("titan", titan))
    app.add_handler(CommandHandler("reviewportfolio", reviewportfolio))
    app.add_handler(CommandHandler("portfolio", portfolio))

    # ALFRED_AGENT_ORG_REGISTER_START
    for _alfred_agent_command, _alfred_agent_handler in ALFRED_AGENT_COMMAND_HANDLERS.items():
        try:
            app.add_handler(CommandHandler(_alfred_agent_command, _alfred_agent_handler), group=-1)
        except TypeError:
            app.add_handler(CommandHandler(_alfred_agent_command, _alfred_agent_handler))
    # ALFRED_AGENT_ORG_REGISTER_END


    app.add_handler(CallbackQueryHandler(hybrid_callback, pattern="^hybrid\\|"))
    app.add_handler(CallbackQueryHandler(hybrid_feedback_callback, pattern="^hybridfb\\|"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()


if __name__ == "__main__":
    main()

```

---

# LlamaIndex Evidence Engine

Generated: 2026-06-30T21:41:58.616587


## Purpose

Defines semantic retrieval and ChatGPT Action evidence packaging.

## Responsibilities

- Index the live Obsidian vault.
- Retrieve semantically relevant evidence.
- Package evidence for ChatGPT reasoning.
- Support the Custom GPT Action endpoint.

## Inputs

- /docker/obsidian-vault
- Embedding model
- User question

## Outputs

- Evidence package
- Source paths
- Similarity-scored nodes

## Dependencies

- FastAPI app
- alfred.py
- LlamaIndex index folder
- Python virtual environment

## Failure Modes

- API not running.
- Index stale or missing.
- Evidence package returned but GPT instructions misaligned.
- Subprocess output includes warnings before JSON.

## Recovery Procedure

- Run alfred.py directly with --json.
- Test local API on 127.0.0.1:8788.
- Rebuild index from the live vault if needed.
- Confirm GPT Action instructions treat API output as evidence package.

## Source Evidence

### llamaindex/index_summary.txt

Size: 2621 bytes

```text
===== index size =====
170M	/opt/llamaindex-bakeoff/index
===== files =====
2026-06-28 17:39 1093927 /opt/llamaindex-bakeoff/index/index_store.json
2026-06-28 17:39 117946088 /opt/llamaindex-bakeoff/index/default__vector_store.json
2026-06-28 17:39 18 /opt/llamaindex-bakeoff/index/graph_store.json
2026-06-28 17:39 58865656 /opt/llamaindex-bakeoff/index/docstore.json
2026-06-28 17:39 72 /opt/llamaindex-bakeoff/index/image__vector_store.json
===== requirements =====
aiohappyeyeballs==2.6.2
aiohttp==3.14.1
aiosignal==1.4.0
aiosqlite==0.22.1
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.14.1
attrs==26.1.0
banks==2.4.4
certifi==2026.6.17
charset-normalizer==3.4.7
click==8.4.2
colorama==0.4.6
cuda-bindings==13.3.1
cuda-pathfinder==1.5.5
cuda-toolkit==13.0.2
dataclasses-json==0.6.7
Deprecated==1.3.1
dirtyjson==1.0.8
distro==1.9.0
fastapi==0.138.1
filelock==3.29.4
filetype==1.2.0
frozenlist==1.8.0
fsspec==2026.6.0
greenlet==3.5.3
griffe==2.1.0
griffecli==2.1.0
griffelib==2.1.0
h11==0.16.0
hf-xet==1.5.1
httpcore==1.0.9
httpx==0.28.1
huggingface_hub==1.21.0
idna==3.18
Jinja2==3.1.6
jiter==0.15.0
joblib==1.5.3
llama-index==0.14.23
llama-index-core==0.14.23
llama-index-embeddings-huggingface==0.7.0
llama-index-embeddings-openai==0.6.0
llama-index-instrumentation==0.5.0
llama-index-llms-openai==0.7.9
llama-index-workflows==2.22.1
markdown-it-py==4.2.0
MarkupSafe==3.0.3
marshmallow==3.26.2
mdurl==0.1.2
mpmath==1.3.0
multidict==6.7.1
mypy_extensions==1.1.0
narwhals==2.22.1
nest-asyncio==1.6.0
networkx==3.6.1
nltk==3.9.4
numpy==2.5.0
nvidia-cublas==13.1.1.3
nvidia-cuda-cupti==13.0.85
nvidia-cuda-nvrtc==13.0.88
nvidia-cuda-runtime==13.0.96
nvidia-cudnn-cu13==9.20.0.48
nvidia-cufft==12.0.0.61
nvidia-cufile==1.15.1.6
nvidia-curand==10.4.0.35
nvidia-cusolver==12.0.4.66
nvidia-cusparse==12.6.3.3
nvidia-cusparselt-cu13==0.8.1
nvidia-nccl-cu13==2.29.7
nvidia-nvjitlink==13.0.88
nvidia-nvshmem-cu13==3.4.5
nvidia-nvtx==13.0.85
openai==2.44.0
packaging==26.2
pillow==12.2.0
platformdirs==4.10.0
propcache==0.5.2
pydantic==2.13.4
pydantic_core==2.46.4
Pygments==2.20.0
PyYAML==6.0.3
regex==2026.5.9
requests==2.34.2
rich==15.0.0
safetensors==0.8.0
scikit-learn==1.9.0
scipy==1.18.0
sentence-transformers==5.6.0
setuptools==81.0.0
shellingham==1.5.4
sniffio==1.3.1
SQLAlchemy==2.0.51
starlette==1.3.1
sympy==1.14.0
tenacity==9.1.4
threadpoolctl==3.6.0
tiktoken==0.13.0
tinytag==2.2.1
tokenizers==0.22.2
torch==2.12.1
tqdm==4.68.3
transformers==5.12.1
triton==3.7.1
typer==0.25.1
typing-inspect==0.9.0
typing-inspection==0.4.2
typing_extensions==4.15.0
urllib3==2.7.0
uvicorn==0.49.0
wrapt==2.2.2
yarl==1.24.2

```

### key_files/opt__llamaindex-bakeoff__app.py

Size: 15157 bytes

```text
from fastapi import FastAPI, Form, Body, Header, HTTPException
from fastapi.responses import HTMLResponse
from functools import lru_cache
from html import escape
from pathlib import Path
from urllib.parse import unquote

PERSIST = "/opt/llamaindex-bakeoff/index"

app = FastAPI(title="Alfred Retrieval Harness")

@lru_cache(maxsize=1)
def get_retriever():
    from llama_index.core import StorageContext, load_index_from_storage, Settings
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Settings.llm = None

    storage_context = StorageContext.from_defaults(persist_dir=PERSIST)
    index = load_index_from_storage(storage_context)
    return index.as_retriever(similarity_top_k=20)

ROUTES = {
    "attention": [
        "09 Governance/Human Action Queue",
        "09 Governance/Escalations",
        "09 Governance/Open Loops",
        "09 Governance/Objectives",
        "09 Governance/Watchlists",
        "09 Governance/Daily Governance",
    ],
    "people": [
        "/02 People/",
        "02 People",
        "/People/",
        "LLM Wiki/People",
        "07 AI Memory/Entities",
    ],
    "companies": [
        "04 Companies",
        "Suppliers",
        "LLM Wiki/Suppliers",
        "LLM Wiki/Companies",
    ],
    "projects": [
        "03 Projects",
    ],
}

ROUTE_QUERIES = {
    "attention": [
        "Required Human Actions work",
        "Latest Governance Escalation action required work",
        "active open loop work recommended action",
        "objectives status work",
        "watchlist material development work",
    ],
    "people": [
        "02 People Graham Dawe",
        "People Graham Dawe",
        "{query}",
    ],
    "companies": ["{query}"],
    "projects": ["{query}"],
}

EXCLUDE = [
    "/10 Domains/Personal/",
    "/Trading/",
    "/Finance/Trading/",
    "/98 Archive/",
]

DOMAIN_EXCLUDE = [
    "ibkr",
    "trading dashboard",
    "portfolio",
    "degiro",
    "xlf",
    "vig",
    "fog",
    "pba exception",
    "etf",
    "mtum",
    "ieur",
    "xlk",
    "iusn",
    "is3n",
    "meud",
    "vwce",
]

def classify_route(query: str):
    q = query.lower()
    if any(x in q for x in ["attention", "priority", "priorities", "work items", "deserves attention", "top ten issues", "issues to face", "top ten", "top issues", "issues"]):
        return "attention"
    if any(x in q for x in ["who is", "person", "people", "graham", "grahame", "dawe"]):
        return "people"
    if any(x in q for x in ["company", "supplier", "barclays", "codec", "softcat"]):
        return "companies"
    if "project" in q:
        return "projects"
    return None

def routed_queries(query: str, route: str | None):
    if not route:
        return [query]
    return [x.format(query=query) for x in ROUTE_QUERIES.get(route, [query])]

def allowed_by_route(path: str, route: str | None):
    if not route:
        return True
    prefixes = ROUTES.get(route, [])
    return any(prefix in path for prefix in prefixes)

def object_type(path: str):
    p = path.lower()
    if "/09 governance/human action queue/" in p:
        return "HUMAN ACTION"
    if "/09 governance/escalations/" in p:
        return "ESCALATION"
    if "/09 governance/open loops/" in p:
        return "OPEN LOOP"
    if "/09 governance/objectives/" in p:
        return "OBJECTIVE"
    if "/09 governance/watchlists/" in p:
        return "WATCHLIST"
    if "/09 governance/daily governance/" in p:
        return "DAILY GOVERNANCE"
    if "/07 ai memory/entities/" in p:
        return "ENTITY"
    if "/02 people/" in p:
        return "PERSON RECORD"
    if "/llm wiki/people/" in p:
        return "PERSON WIKI"
    if "/04 companies/" in p:
        return "COMPANY RECORD"
    if "/llm wiki/suppliers/" in p:
        return "SUPPLIER WIKI"
    if "/llm wiki/companies/" in p:
        return "COMPANY WIKI"
    if "/03 projects/" in p:
        return "PROJECT RECORD"
    if "historical capture" in p:
        return "EVIDENCE"
    if "enriched capture" in p:
        return "ENRICHED INSIGHT"
    if "/07 executive briefings/" in p:
        return "GENERATED BRIEFING"
    if "/98 archive/" in p:
        return "ARCHIVE"
    return "OTHER"


def filename_people_matches(query: str):
    root = Path("/docker/obsidian-vault")
    q = query.lower()
    candidates = []

    aliases = {
        "grahame dawe": "graham dawe",
        "graham dawe": "graham dawe",
    }

    target = None
    for k, v in aliases.items():
        if k in q:
            target = v
            break

    if not target:
        return []

    wanted = target.replace(" ", "*")

    search_dirs = [
        root / "02 People",
        root / "People",
        root / "LLM Wiki" / "People",
    ]

    for d in search_dirs:
        if not d.exists():
            continue
        for f in d.rglob("*.md"):
            name = f.stem.lower().replace("-", " ")
            if target in name:
                candidates.append(f)

    return candidates


def page(query="", results=""):
    return f"""<html>
<head>
<title>Alfred Retrieval Harness</title>
<style>
body {{ font-family: Arial; max-width: 1100px; margin: 2rem auto; }}
textarea {{ width: 100%; height: 90px; }}
.result {{ border: 1px solid #ddd; padding: 1rem; margin: 1rem 0; border-radius: 8px; }}
.path {{ font-weight: bold; color: #333; }}
.score {{ color: #666; }}
pre {{ white-space: pre-wrap; }}
</style>
</head>
<body>
<h1>Alfred Retrieval Harness</h1>
<p>Read-only LlamaIndex test over Obsidian vault copy.</p>
<form method="post">
<textarea name="query">{escape(query)}</textarea><br><br>
<button type="submit">Search</button>
</form>
<hr>
{results}
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
def home():
    return page("What work items deserve attention?", "")

@app.post("/", response_class=HTMLResponse)
def search(query: str = Form(...)):
    retriever = get_retriever()
    route = classify_route(query)

    raw = []
    for rq in routed_queries(query, route):
        raw.extend(retriever.retrieve(rq))

    rows = []
    seen = set()
    themes = {}

    if route == "people":
        import subprocess
        try:
            summary = subprocess.check_output(
                ["python3", "entity_summary.py", "person", (
                    query.lower()
                    .replace("who is ", "")
                    .replace("tell me about ", "")
                    .replace("what do you know about ", "")
                    .strip(" ?.")
                )],
                text=True,
                timeout=30
            )
        except Exception as e:
            summary = f"People summary failed: {e}"

        return page(query, f"""
        <div class="result">
          <div class="path">[PEOPLE INTELLIGENCE]</div>
          <div class="score">route=people | source=entity_summary.py</div>
          <pre>{escape(summary[:8000])}</pre>
        </div>
        """)

    if route == "people":
        for f in filename_people_matches(query):
            path = str(f)
            if path in seen:
                continue
            seen.add(path)
            typ = object_type(path)
            try:
                raw_text = f.read_text(errors="ignore")
            except Exception:
                raw_text = ""
            safe_path = escape(path, quote=True)
            rows.append(f"""
            <div class="result">
              <div class="path">
                [{escape(typ)}]
                <a href="/view?path={safe_path}">{safe_path}</a>
              </div>
              <div class="score">route=people | source=filename-match</div>
              <pre>{escape(raw_text[:1200])}</pre>
            </div>
            """)

    theme_terms = [
        "strategic_drift",
        "dora",
        "supplier_risk",
        "platform_resilience",
        "cyber_incidents",
        "ai_regulation",
    ]

    for r in raw:
        path = r.metadata.get("file_path", "unknown")
        raw_text = str(r.node.text)
        raw_text_lower = raw_text.lower()

        if any(x in path for x in EXCLUDE):
            continue
        if not allowed_by_route(path, route):
            continue
        if route == "attention" and any(term in raw_text_lower for term in DOMAIN_EXCLUDE):
            continue

        if route == "people":
            low_value_entity = (
                "/07 AI Memory/Entities/" in path
                and (
                    "appears " in raw_text_lower
                    or "curation status" in raw_text_lower
                    or "review description" in raw_text_lower
                    or "confirm whether this is a strategic theme" in raw_text_lower
                )
            )
            if low_value_entity:
                continue
        if path in seen:
            continue

        seen.add(path)
        typ = object_type(path)
        score = r.score or 0
        text = escape(raw_text[:1200])
        safe_path = escape(path, quote=True)

        theme = None
        lower_path = path.lower()
        for t in theme_terms:
            if t in lower_path:
                theme = t
                break

        if route == "attention" and theme:
            if theme not in themes:
                themes[theme] = {
                    "count": 0,
                    "path": path,
                    "type": typ,
                    "score": score,
                }
            themes[theme]["count"] += 1
            continue

        rows.append(f"""
        <div class="result">
          <div class="path">
            [{escape(typ)}]
            <a href="/view?path={safe_path}">{safe_path}</a>
          </div>
          <div class="score">route={escape(str(route))} | score={score:.4f}</div>
          <pre>{text}</pre>
        </div>
        """)

    if route == "attention":
        for theme, data in sorted(themes.items(), key=lambda x: x[1]["count"], reverse=True):
            label = theme.replace("_", " ").title()
            rows.append(f"""
            <div class="result">
              <div class="path">
                [{escape(data['type'])}]
                <a href="/view_theme?theme={theme}">{escape(label)}</a>
              </div>
              <div class="score">occurrences={data['count']} | route=attention</div>
            </div>
            """)

    results = "\n".join(rows) if rows else "<p>No results after filters.</p>"
    return page(query, results)



@app.get("/view_theme", response_class=HTMLResponse)
def view_theme(theme: str):

    root = Path("/docker/obsidian-vault")

    matches = []

    allowed_dirs = [
        "/09 Governance/Open Loops/",
        "/09 Governance/Watchlists/",
        "/09 Governance/Escalations/",
        "/09 Governance/Objectives/",
        "/09 Governance/Human Action Queue/",
    ]

    for md in root.rglob("*.md"):
        sp = str(md)
        if not any(d in sp for d in allowed_dirs):
            continue
        name = md.name.lower()
        t = theme.lower()

        if t == "dora":
            ok = (
                name.endswith("watchlist - dora.md")
                or name.endswith("open loop - watchlist - dora.md")
            )
        elif t == "supplier_risk":
            ok = "supplier_risk" in name or "supplier risk" in name
        elif t == "strategic_drift":
            ok = "strategic_drift" in name or "strategic drift" in name
        elif t == "platform_resilience":
            ok = "platform_resilience" in name or "platform resilience" in name
        elif t == "cyber_incidents":
            ok = "cyber_incidents" in name or "cyber incidents" in name
        elif t == "ai_regulation":
            ok = "ai_regulation" in name or "ai regulation" in name
        else:
            ok = t in name

        if ok:
            matches.append(md)

    matches = sorted(matches, reverse=True)

    groups = {}

    for m in matches:
        typ = object_type(str(m))
        groups.setdefault(typ, []).append(m)

    sections = []

    for typ, files in sorted(groups.items()):
        rows = []
        files = sorted(files, reverse=True)[:5]

        for m in files:
            rows.append(
                f'<li><a href="/view?path={escape(str(m), quote=True)}">{escape(m.name)}</a></li>'
            )

        sections.append(f"""
        <h3>{escape(typ)} ({len(files)})</h3>
        <ul>
          {''.join(rows)}
        </ul>
        """)

    return f"""
    <html>
    <body style="font-family: Arial; max-width: 1200px; margin: 2rem auto;">
      <p><a href="/">Back to search</a></p>
      <h2>{escape(theme)}</h2>

      <p><b>Latest Watchlist:</b><br>
      {escape(next((m.name for m in sorted(matches, reverse=True) if 'watchlist' in m.name.lower() and 'open loop' not in m.name.lower()), 'None'))}
      </p>

      <p><b>Latest Open Loop:</b><br>
      {escape(next((m.name for m in sorted(matches, reverse=True) if 'open loop' in m.name.lower()), 'None'))}
      </p>

      <p><b>Occurrences:</b> {len(matches)}</p>

      <h3>Outstanding Actions</h3>

      <ul>
      {
        ''.join(
          f'<li>{escape(line.strip()[2:])}</li>'
          for line in [
            line
            for line in next(
              (
                Path(m).read_text(errors='ignore').splitlines()
                for m in sorted(matches, reverse=True)
                if 'open loop' in m.name.lower()
              ),
              []
            )
            if line.strip().startswith('- ')
          ][:5]
        )
      }
      </ul>

      {''.join(sections)}
    </body>
    </html>
    """

@app.get("/view", response_class=HTMLResponse)
def view(path: str):
    p = Path(unquote(path))

    if not p.exists():
        return "<h1>File not found</h1>"

    try:
        content = p.read_text(errors="ignore")
    except Exception as e:
        return f"<h1>Error</h1><pre>{escape(str(e))}</pre>"

    return f"""
    <html>
    <body style="font-family: Arial; max-width: 1200px; margin: 2rem auto;">
      <p><a href="/">Back to search</a></p>
      <h2>{escape(str(p))}</h2>
      <pre style="white-space: pre-wrap;">{escape(content)}</pre>
    </body>
    </html>
    """



@app.post("/alfred")
def alfred_api(payload: dict = Body(...), authorization: str | None = Header(default=None)):
    import subprocess
    import sys

    expected = Path("/opt/llamaindex-bakeoff/.alfred_api_token").read_text().strip()
    if authorization != f"Bearer {expected}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    question = (payload.get("question") or "").strip()
    if not question:
        return {"error": "Missing question"}

    try:
        answer = subprocess.check_output(
            [sys.executable, "alfred.py", "--json", question],
            cwd="/opt/llamaindex-bakeoff",
            text=True,
            timeout=300,
        )
        import json
        return json.loads(answer.splitlines()[-1])
    except subprocess.TimeoutExpired:
        return {"error": "Alfred timed out"}
    except Exception as e:
        return {"error": str(e)}


```

### key_files/opt__llamaindex-bakeoff__alfred.py

Size: 1790 bytes

```text
#!/usr/bin/env python3
import json
import sys
from pathlib import Path
import contextlib

BASE = Path(__file__).parent
PERSIST = str(BASE / "index")

args = sys.argv[1:]
json_mode = False

if args and args[0] == "--json":
    json_mode = True
    args = args[1:]

if not args:
    raise SystemExit('Usage: alfred.py [--json] "question"')

question = " ".join(args)

with contextlib.redirect_stdout(sys.stderr):
    from llama_index.core import StorageContext, load_index_from_storage, Settings
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Settings.llm = None

    storage_context = StorageContext.from_defaults(persist_dir=PERSIST)
    index = load_index_from_storage(storage_context)
    retriever = index.as_retriever(similarity_top_k=12)

    nodes = retriever.retrieve(question)

evidence = []
for i, node in enumerate(nodes, 1):
    meta = getattr(node.node, "metadata", {}) or {}
    path = meta.get("file_path") or meta.get("filename") or meta.get("source") or "unknown"
    text = node.node.get_content()[:2500]
    score = getattr(node, "score", None)
    evidence.append(
        f"### Evidence {i}\n"
        f"Source: {path}\n"
        f"Score: {score}\n\n"
        f"{text}"
    )

answer = f"""You are Alfred's evidence package.

Question:
{question}

Instructions for ChatGPT:
Use only the evidence below. If the evidence is insufficient, say so clearly. Do not use public knowledge or memory.

Evidence:
{chr(10).join(evidence)}
"""

payload = {
    "question": question,
    "answer": answer,
    "quality_gate": "EVIDENCE_PACKAGE_ONLY_CHATGPT_MUST_REASON",
    "source": "alfred.py",
}

print(json.dumps(payload) if json_mode else answer)

```

### key_files/opt__llamaindex-bakeoff__test_index.py

Size: 707 bytes

```text
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

VAULT = "/docker/obsidian-vault"
PERSIST = "./index"

Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
Settings.llm = None

print(f"Loading markdown files from: {VAULT}")
docs = SimpleDirectoryReader(
    VAULT,
    recursive=True,
    required_exts=[".md"],
).load_data()

print(f"Loaded documents: {len(docs)}")
print("Building index...")
index = VectorStoreIndex.from_documents(docs)

print(f"Persisting index to: {PERSIST}")
index.storage_context.persist(persist_dir=PERSIST)

print("Index build complete")

```

---

# Docker and Cloudflare

Generated: 2026-06-30T21:41:58.616595


## Purpose

Defines container/runtime exposure and public HTTPS routing.

## Responsibilities

- Provide any required container runtime compatibility.
- Expose public Alfred endpoints through Cloudflare Tunnel.
- Map hostnames to correct local ports.

## Inputs

- Docker containers
- Cloudflare tunnel config
- Local services

## Outputs

- Public HTTPS endpoints
- Container runtime state

## Dependencies

- Docker
- cloudflared
- Cloudflare ingress configuration

## Failure Modes

- Cloudflare points to wrong local port.
- Container name exists historically but is not valid for current path.
- Service returns 502 because local target is not listening.

## Recovery Procedure

- Use ss -ltnp to confirm local listeners.
- Check /etc/cloudflared/config.yml.
- Restart cloudflared only after confirming local target.
- Inspect containers before assuming they are current production runtime.

## Source Evidence

### docker/containers.txt

Size: 368 bytes

```text
NAMES                              STATUS                   IMAGE                                        PORTS
hermes-agent-lp1i-hermes-agent-1   Exited (0) 6 weeks ago   ghcr.io/hostinger/hvps-hermes-agent:latest   
hermes-agent-mctr-hermes-agent-1   Up 17 hours              ghcr.io/hostinger/hvps-hermes-agent:latest   0.0.0.0:32768->4860/tcp, [::]:32768->4860/tcp

```

### docker/images.txt

Size: 294 bytes

```text
WARNING: This output is designed for human readability. For machine-readable output, please use --format.
IMAGE                                        ID             DISK USAGE   CONTENT SIZE   EXTRA
ghcr.io/hostinger/hvps-hermes-agent:latest   97e901c56cbd       9.84GB         3.04GB   U    

```

### cloudflare/config.yml

Size: 384 bytes

```text
tunnel: 297ae52c-a42f-4431-83d4-a3b49cc486f5
credentials-file: /root/.cloudflared/297ae52c-a42f-4431-83d4-a3b49cc486f5.json

ingress:
  - hostname: alfred.alfreddoheny.cloud
    service: http://localhost:4865

  - hostname: v2.alfreddoheny.cloud
    service: http://127.0.0.1:4880

  - hostname: api.alfreddoheny.cloud
    service: http://127.0.0.1:8788

  - service: http_status:404

```

---

# Python Codebase Catalogue

Generated: 2026-06-30T21:41:58.616601


## Purpose

Summarises discovered Python modules, imports, functions and classes.

## Responsibilities

- Provide a searchable engineering inventory.
- Support future architecture documentation generation.
- Expose likely extension points without manual inspection.

## Inputs

- AST parser output
- Python source files

## Outputs

- Module catalogue
- Function inventory
- Class inventory

## Dependencies

- Python source code
- Evidence collector

## Failure Modes

- Syntax warnings from source files.
- Generated catalogue becomes stale if not regenerated after changes.

## Recovery Procedure

- Regenerate engineering evidence pack.
- Review parsing errors in catalogue output.

## Source Evidence

### python/second_brain_python_inventory.json

Size: 322265 bytes

```text
[
  {
    "file": "/opt/second-brain/tests/test_alfred_validators.py",
    "imports": [
      "__future__",
      "pathlib",
      "retrieval",
      "sys",
      "unittest"
    ],
    "functions": [
      "test_valid_compound_daily_answer",
      "test_missing_daily_section_fails",
      "test_generated_source_fails",
      "test_false_inference_fails",
      "test_nonexistent_source_fails",
      "test_invalid_line_fails"
    ],
    "classes": [
      "DailyValidationTests",
      "ObjectiveValidationTests",
      "SourceValidationTests"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/tests/test_alfred_router.py",
    "imports": [
      "__future__",
      "pathlib",
      "retrieval",
      "sys",
      "unittest"
    ],
    "functions": [
      "test_explicit_daily_compound",
      "test_daily_reverse_wording",
      "test_objective_route_is_protected",
      "test_tprm_route",
      "test_cost_route",
      "test_primary_source",
      "test_generated_source",
      "test_primary_only_rejects_generated"
    ],
    "classes": [
      "QueryClassifierTests",
      "SourcePolicyTests"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/tests/run_retrieval_regression.py",
    "imports": [
      "__future__",
      "argparse",
      "json",
      "os",
      "pathlib",
      "re",
      "subprocess",
      "time",
      "typing"
    ],
    "functions": [
      "normalise",
      "run_one",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/tests/run_routing_paraphrase_matrix.py",
    "imports": [
      "__future__",
      "json",
      "pathlib",
      "retrieval",
      "sys"
    ],
    "functions": [
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/reporting/render_report.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "render_dashboard"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/retrieval/alfred_router.py",
    "imports": [
      "__future__",
      "argparse",
      "audit",
      "classifiers",
      "datetime",
      "hashlib",
      "json",
      "os",
      "pathlib",
      "strategies",
      "sys",
      "time",
      "typing",
      "validators"
    ],
    "functions": [
      "utc_now",
      "output_hash",
      "parse_args",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/retrieval/source_policy.py",
    "imports": [
      "__future__",
      "dataclasses"
    ],
    "functions": [
      "classify_source",
      "allowed_for_policy"
    ],
    "classes": [
      "SourceClassification"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/retrieval/__init__.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": "Alfred structured retrieval and routing package."
  },
  {
    "file": "/opt/second-brain/retrieval/models.py",
    "imports": [
      "__future__",
      "dataclasses",
      "typing"
    ],
    "functions": [
      "to_dict"
    ],
    "classes": [
      "RouteDecision"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/retrieval/validators.py",
    "imports": [
      "__future__",
      "dataclasses",
      "models",
      "pathlib",
      "re",
      "subprocess",
      "typing"
    ],
    "functions": [
      "_normalise_cited_path",
      "_extract_sources",
      "_validate_source",
      "_contains_forbidden_source",
      "_has_no_evidence_claim",
      "_has_false_inference_claim",
      "_has_obvious_unsupported_target",
      "_lexical_evidence_exists",
      "_count_markers",
      "_require_headings",
      "_validate_daily",
      "_validate_objectives",
      "_validate_cost",
      "_validate_tprm",
      "validate_answer",
      "to_dict"
    ],
    "classes": [
      "ValidationResult"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/retrieval/strategies.py",
    "imports": [
      "__future__",
      "dataclasses",
      "models",
      "os",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "_run",
      "deterministic_daily_log",
      "protected_legacy",
      "execute_strategy"
    ],
    "classes": [
      "StrategyResult"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/retrieval/audit.py",
    "imports": [
      "__future__",
      "fcntl",
      "json",
      "pathlib",
      "typing"
    ],
    "functions": [
      "append_audit"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/retrieval/classifiers.py",
    "imports": [
      "__future__",
      "models",
      "re"
    ],
    "functions": [
      "_daily_sections",
      "_date_reference",
      "classify_query"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/gui/server.py",
    "imports": [
      "datetime",
      "email",
      "html",
      "http",
      "json",
      "math",
      "os",
      "ownership_router",
      "pathlib",
      "re",
      "secrets",
      "subprocess",
      "sys",
      "time",
      "urllib"
    ],
    "functions": [
      "load_auth_env",
      "load_auth_state",
      "save_auth_state",
      "now_ts",
      "send_magic_link",
      "esc",
      "shell",
      "file_table",
      "load_state",
      "save_state",
      "registry_page",
      "ai_format_entity",
      "trading_dashboard_files",
      "trading_title",
      "explain_trading_score_html",
      "trading_concentration_fingerprint",
      "inject_trading_concentration_review",
      "count_files",
      "latest_file_time",
      "executive_home",
      "briefing_table",
      "chat_page",
      "run_chat",
      "eos_load_json",
      "eos_write_json",
      "workflow_now",
      "operation_id",
      "operation_entry_defaults",
      "append_operation",
      "start_operation",
      "update_operation",
      "load_operation_events",
      "operations_latest",
      "operation_timeline",
      "latest_operation",
      "operations_worker_script",
      "process_operation_now",
      "retry_operation",
      "terminal_operation_update",
      "handle_operation_control",
      "operation_control_buttons",
      "advisory_memo_engine_script",
      "advisory_memo_index",
      "advisory_source_key",
      "latest_advisory_memo_summary",
      "safe_advisory_memo_path",
      "advisory_source_type",
      "advisory_payload_for",
      "advisory_memo_controls",
      "run_advisory_memo_generation",
      "handle_advisory_memo_action",
      "memo_text",
      "memo_sentences",
      "memo_paragraph",
      "render_paragraph_section",
      "render_supporting_value",
      "advisory_memo_metadata",
      "render_advisory_memo_sections",
      "render_executive_briefing_memo",
      "advisory_memo_page",
      "normalised_operation_output_link",
      "safe_operation_output_path",
      "review_list",
      "operation_output_page",
      "run_tracked_subprocess",
      "operation_monitor_counts",
      "operation_status_badge",
      "operation_monitor_page",
      "operation_detail_page",
      "load_workflow_state",
      "save_workflow_state",
      "workflow_key",
      "workflow_item",
      "canonical_lifecycle_state",
      "lifecycle_is_active",
      "lifecycle_is_history",
      "lifecycle_target_state",
      "lifecycle_audit_entry",
      "route_governance_owner",
      "explicit_owner_value",
      "apply_record_lifecycle",
      "record_workflow_event",
      "governance_activity_entry",
      "governance_record_title",
      "governance_record_description",
      "append_governance_activity",
      "workflow_history_for",
      "render_activity_history",
      "update_workflow_object",
      "governance_action_path",
      "governance_escalation_path",
      "daily_governance_index_path",
      "daily_governance_state_path",
      "normalize_governance_escalation_status",
      "load_governance_escalation_registry",
      "save_governance_escalation_registry",
      "normalize_governance_escalation_record",
      "governance_escalation_records",
      "governance_escalation_candidate_records",
      "update_governance_escalations",
      "create_governance_escalation",
      "promote_governance_attention_to_escalation",
      "update_governance_actions",
      "governance_registry_config",
      "update_governance_register_records",
      "create_governance_action",
      "item_detail_href",
      "eos_count",
      "eos_objectives",
      "eos_objective_status",
      "eos_objectives_summary_html",
      "eos_dashboard_counts",
      "eos_intelligence",
      "objective_console_status",
      "objective_console_confidence",
      "objective_console_agent_status",
      "objective_console_records",
      "objective_console_record",
      "objective_console_contributors",
      "objective_console_improvement_actions",
      "objective_operation_outputs",
      "objective_recommendation_valid",
      "objective_recommendation_from_output",
      "objective_console_recommendations",
      "objective_console_agent_views",
      "objective_console_action_buttons",
      "objective_console_detail_page",
      "objective_operating_console_page",
      "handle_objective_console_action",
      "eos_recent_activity_html",
      "eos_people_company_html",
      "eos_objective_intelligence_page",
      "alfred_execution_edit_page",
      "alfred_lifecycle_data",
      "alfred_technical_debt_data",
      "alfred_technical_debt_page",
      "alfred_board_session_data",
      "alfred_board_session_page",
      "alfred_board_secretary_data",
      "alfred_board_secretary_page",
      "alfred_executive_committee_data",
      "alfred_executive_committee_page",
      "alfred_ai_agent_debate_data",
      "alfred_ai_agent_debate_page",
      "ai_office_nav",
      "ai_office_preamble",
      "alfred_ai_executive_office_page",
      "alfred_executive_ai_briefing_data",
      "alfred_executive_ai_briefing_page",
      "alfred_ai_agent_reviews_data",
      "alfred_agent_workspace_page",
      "alfred_agent_triage_data",
      "alfred_agent_triage_summary",
      "alfred_agent_triage_page",
      "alfred_governance_intelligence_data",
      "governance_attention_record_id",
      "governance_attention_records",
      "governance_escalations_page",
      "alfred_governance_intelligence_page",
      "alfred_dashboard_cache",
      "command_centre_severity_rank",
      "command_centre_severity_label",
      "command_centre_action_query",
      "command_centre_action_button",
      "command_centre_action_controls",
      "command_centre_hidden_fields",
      "command_centre_card",
      "command_centre_objective_controls",
      "command_centre_objective_card",
      "command_centre_objective_items",
      "command_centre_governance_items",
      "command_centre_action_items",
      "command_centre_risk_items",
      "command_centre_decision_items",
      "command_centre_open_loop_items",
      "command_centre_portfolio_item",
      "command_centre_daily_record_items",
      "command_centre_items",
      "command_centre_item_list",
      "command_centre_attention_drawer_items",
      "command_centre_attention_panel",
      "command_centre_priority_panel",
      "command_centre_kpi_card",
      "command_centre_radar_segment",
      "command_centre_agent_card",
      "command_centre_handle_action",
      "create_objective_reevaluation_request",
      "alfred_objective_reevaluation_feedback_page",
      "alfred_objective_reevaluation_status_page",
      "alfred_dashboard_cached_page",
      "alfred_dashboard_v2",
      "alfred_execution_page",
      "alfred_sitemap_page",
      "alfred_administration_page",
      "alfred_overnight_jobs_data",
      "alfred_overnight_jobs_page",
      "alfred_health_dashboard_data",
      "alfred_rag_badge",
      "alfred_health_dashboard_page",
      "alfred_access_data",
      "alfred_access_allowed",
      "alfred_access_page",
      "alfred_reflection_intelligence_page",
      "alfred_actions_data",
      "alfred_objectives_options",
      "alfred_action_edit_page",
      "update_legacy_action_record",
      "alfred_ownership_page",
      "alfred_daily_governance_data",
      "alfred_daily_type_label",
      "markdown_excerpt_for_daily_record",
      "alfred_daily_governance_page",
      "update_daily_records",
      "update_agent_recommendations",
      "update_open_loop_lifecycle",
      "update_workflow_lifecycle",
      "apply_lifecycle_transition",
      "apply_batch_lifecycle_transition",
      "handle_functional_lifecycle_action",
      "handle_functional_lifecycle_batch_action",
      "alfred_governance_edit_page",
      "handle_governance_save",
      "governance_record_is_visible",
      "alfred_governance_workspace_page",
      "alfred_board_minutes_page",
      "alfred_board_capture_page",
      "alfred_board_pack_data",
      "alfred_status_badge",
      "alfred_board_pack_page",
      "alfred_org_data",
      "alfred_org_operational_counts",
      "alfred_owner_key_for_profile",
      "org_preview_0812",
      "org_preview_1017",
      "org_preview_1020",
      "alfred_titan_rca_data",
      "alfred_titan_rca_for_id",
      "alfred_titan_find_record",
      "alfred_titan_outcome_detail_page",
      "alfred_titan_outcomes_page",
      "alfred_titan_incidents_page",
      "alfred_athena_governance_watch_page",
      "athena_apply_finding_action",
      "alfred_athena_finding_detail_page",
      "alfred_titan_rca_page",
      "alfred_titan_metrics_page",
      "alfred_titan_data",
      "alfred_titan_control_page",
      "load_first_json",
      "load_canonical_identity_contract",
      "load_organisation_profiles",
      "load_jsonl_records",
      "canonical_identity_records",
      "canonical_identity_index",
      "organisation_profile_index",
      "canonical_profile_id_map",
      "resolve_profile_for_canonical_id",
      "portrait_directory_candidates",
      "resolve_portrait_filename",
      "resolve_identity_portrait",
      "identity_aliases",
      "matches_identity",
      "active_workload_items",
      "workload_items_for_identity",
      "authority_text",
      "authority_rights_text",
      "authority_delegation_text",
      "operating_cadence_text",
      "profile_human_detail",
      "render_identity_workload_html",
      "render_profile_detail",
      "alfred_agent_directory_page",
      "alfred_organisation_chart_page",
      "alfred_authority_matrix_page",
      "alfred_workload_view_page",
      "alfred_agent_profile_page",
      "alfred_clean_organisation_page",
      "org_preview_1124",
      "alfred_org_page",
      "alfred_metrics",
      "alfred_metric_rows",
      "alfred_status_icon",
      "alfred_kpi_cards_html",
      "alfred_executive_summary_html",
      "alfred_executive_metrics_page",
      "eos_home_body",
      "eos_objectives_page",
      "alfred_org_chart_page",
      "alfred_board_office_intelligence_data",
      "alfred_board_decision_queue_data",
      "alfred_echo_timeline_data",
      "alfred_board_decision_queue_page",
      "alfred_board_decision_detail_page",
      "alfred_board_decision_lifecycle_page",
      "alfred_echo_timeline_page",
      "alfred_echo_timeline_detail_page",
      "alfred_executive_committee_review_data",
      "alfred_executive_committee_page",
      "alfred_executive_committee_review_page",
      "alfred_executive_committee_member_page",
      "alfred_strategic_memory_page",
      "alfred_agent_council_page",
      "alfred_board_office_intelligence_page",
      "eos_board_page",
      "eos_emergency_board_page",
      "create_emergency_board_session",
      "eos_governance_page",
      "load_agent_registry",
      "latest_matching_file",
      "agents_page",
      "run_agent_council",
      "ask_specific_agent",
      "canonical_agent_slug",
      "agent_review_buttons",
      "contextual_engine_script",
      "agent_outputs_dir",
      "load_agent_review_history",
      "safe_agent_output_path",
      "review_mode_label",
      "first_review_value",
      "review_output_parts",
      "summarize_review_evidence",
      "executive_review_summary",
      "alfred_agent_review_history_page",
      "alfred_agent_review_output_page",
      "render_agent_review_result_page",
      "render_agent_review_provenance",
      "run_contextual_agent_review",
      "alfred_agent_context_review_page",
      "load_open_loops",
      "save_open_loops",
      "load_open_loop_archive",
      "save_open_loop_archive",
      "open_loop_record",
      "open_loop_edit_page",
      "handle_open_loop_save",
      "governance_attention_edit_page",
      "handle_governance_attention_save",
      "open_loop_display_record",
      "open_loop_matches_filters",
      "open_loops_manager",
      "main",
      "render_value",
      "rows_for",
      "block",
      "ul",
      "table",
      "opts",
      "is_open",
      "due",
      "card",
      "rows",
      "batch_form",
      "block",
      "kpi",
      "item_table",
      "card",
      "table",
      "page_url",
      "get_cookie",
      "authorised",
      "login_page",
      "require_auth",
      "send_html",
      "redirect",
      "do_GET",
      "do_POST",
      "bullets",
      "list_html",
      "list_html",
      "list_html",
      "list_html",
      "list_html"
    ],
    "classes": [
      "Handler"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/semantic/index_vault.py",
    "imports": [
      "faiss",
      "hashlib",
      "json",
      "numpy",
      "pathlib",
      "re",
      "sentence_transformers"
    ],
    "functions": [
      "clean_text",
      "chunk_text"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/semantic/search_vault_server.py",
    "imports": [
      "faiss",
      "http",
      "json",
      "numpy",
      "pathlib",
      "sentence_transformers",
      "sys",
      "urllib"
    ],
    "functions": [
      "do_GET",
      "log_message"
    ],
    "classes": [
      "Handler"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/semantic/search_vault.py",
    "imports": [
      "faiss",
      "json",
      "numpy",
      "pathlib",
      "sentence_transformers",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_resolver.py",
    "imports": [
      "__future__",
      "argparse",
      "dataclasses",
      "json",
      "pathlib",
      "sys",
      "typing"
    ],
    "functions": [
      "main",
      "can_execute_as_agent",
      "to_dict",
      "__init__",
      "default_root",
      "_load_json",
      "normalise",
      "_build_alias_index",
      "local_path",
      "resolve",
      "resolve_agent",
      "resolve_agent_id",
      "validate_authority",
      "validate_domain",
      "all_aliases",
      "add"
    ],
    "classes": [
      "AgentResolutionError",
      "AgentAuthorityError",
      "AgentDomainError",
      "ResolvedIdentity",
      "AgentResolver"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/validate_operating_rhythm.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "datetime",
      "pathlib",
      "run_daily_executive_briefing",
      "run_executive_council",
      "run_monthly_governance_review",
      "shutil",
      "sys",
      "tempfile",
      "typing"
    ],
    "functions": [
      "repo_second_brain_root",
      "make_temp_root",
      "assert_true",
      "seed_queue",
      "unique_values",
      "validate",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/trading_governance_synthesis.py",
    "imports": [
      "datetime",
      "pathlib",
      "subprocess"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/open_loop_review.py",
    "imports": [
      "datetime",
      "pathlib",
      "subprocess"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/close_agent_task.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "argparse",
      "json",
      "sys"
    ],
    "functions": [
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/morning_briefing.py",
    "imports": [
      "datetime",
      "pathlib",
      "subprocess"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/knowledge_service.py",
    "imports": [
      "json",
      "pathlib",
      "time",
      "urllib"
    ],
    "functions": [
      "read_file",
      "norm",
      "score_name",
      "get_note",
      "get_recent_changes",
      "find_best_notes",
      "get_objectives",
      "get_open_loops",
      "get_company",
      "get_person",
      "get_project",
      "get_risks",
      "get_decisions",
      "get_executive_state",
      "scan_base"
    ],
    "classes": [
      "KnowledgeService"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/direct_reference_search.py",
    "imports": [
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "extract_terms",
      "excluded",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_signal_engine.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/governance_lifecycle.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "update"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/daily_synthesis.py",
    "imports": [
      "datetime",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/ai_agent_review_layer.py",
    "imports": [
      "agent_resolver",
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "call_hermes",
      "fallback_review",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/governance_lifecycle_review.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/lexical_vault_search.py",
    "imports": [
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "clean_query",
      "query_terms",
      "matching_snippets",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/hybrid_openrouter.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "load_env",
      "call_openrouter",
      "call_model_choice",
      "semantic_context",
      "infer_agent",
      "load_learning_hint",
      "recommend",
      "build_prompt",
      "run",
      "debate",
      "chain",
      "feedback",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/athena_governance_review.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "parse_dt",
      "age_days",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/entity_resolver.py",
    "imports": [
      "datetime",
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "norm",
      "excluded",
      "candidate_phrases",
      "score_path",
      "read_excerpt",
      "recent_dated_sections",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/open_loop_manager_patch.py",
    "imports": [
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/validate_delegation_queue.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "pathlib",
      "shutil",
      "tempfile"
    ],
    "functions": [
      "fail",
      "require",
      "prepare_temp_root",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_synthesis.py",
    "imports": [
      "datetime",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "read_tail"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/link_related.py",
    "imports": [
      "pathlib",
      "subprocess"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/entity_intelligence.py",
    "imports": [
      "collections",
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/open_loop_escalation.py",
    "imports": [
      "collections",
      "contextual_recommendation_engine",
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "contextualize",
      "normalise_previous_record",
      "safe_seen_count",
      "preserve_ux02_fields"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/init_open_loop_register.py",
    "imports": [
      "datetime",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/approve_loop_candidate.py",
    "imports": [
      "pathlib",
      "re",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/extract_entities_ai.py",
    "imports": [
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_action_triage.py",
    "imports": [
      "datetime",
      "json",
      "ownership_router",
      "pathlib",
      "recommendation_quality"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "infer_owner",
      "closure_recommendation",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/action_register.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "normalise_action",
      "update",
      "close",
      "reopen",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/cost_evidence_search.py",
    "imports": [
      "__future__",
      "collections",
      "pathlib",
      "re"
    ],
    "functions": [
      "candidate_files",
      "path_priority",
      "score",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/generate_domain_briefing.py",
    "imports": [
      "datetime",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "read",
      "recent_matching_files",
      "ask_hermes",
      "generate_one"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_council_action.py",
    "imports": [
      "agent_resolver",
      "agent_task_queue",
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/extract_entities.py",
    "imports": [
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/orchestrate_agents.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/entity_consolidation.py",
    "imports": [
      "collections",
      "datetime",
      "difflib",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "clean",
      "normalise",
      "acronym"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/board_capture.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "next_id",
      "add_decision",
      "add_risk",
      "add_action",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/email_daily_change_briefing.py",
    "imports": [
      "datetime",
      "email",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "load_env"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/access_control.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "norm",
      "valid",
      "add",
      "remove",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/open_loop.py",
    "imports": [
      "datetime",
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "read",
      "write",
      "next_id",
      "add_loop",
      "list_loops",
      "close_loop",
      "show"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/email_daily_briefing.py",
    "imports": [
      "datetime",
      "email",
      "markdown",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "load_env",
      "markdown_to_html",
      "send_briefing"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/query_memory.py",
    "imports": [
      "json",
      "pathlib",
      "re",
      "subprocess",
      "sys",
      "urllib"
    ],
    "functions": [
      "classify_intent",
      "classify_entity",
      "run",
      "keyword_hits"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/build_reporting_evidence_bundle.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "read"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/run_monthly_governance_review.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "argparse",
      "collections",
      "datetime",
      "json",
      "pathlib",
      "run_executive_council",
      "sys",
      "typing",
      "uuid"
    ],
    "functions": [
      "now",
      "parse_date",
      "is_open",
      "stale_actions",
      "count_by",
      "council_effectiveness",
      "build_review",
      "task_line",
      "write_review",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/autonomous_watchlist.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "run_chain",
      "materiality_score",
      "should_create_open_loop",
      "write_watchlist_report",
      "write_open_loop",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/delegation_engine.py",
    "imports": [
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/run_executive_council.py",
    "imports": [
      "__future__",
      "agent_resolver",
      "agent_task_queue",
      "argparse",
      "datetime",
      "json",
      "pathlib",
      "recommendation_quality",
      "subprocess",
      "sys",
      "typing",
      "uuid"
    ],
    "functions": [
      "now",
      "default_root",
      "load_jsonl",
      "append_jsonl",
      "generate_run_id",
      "split_csv",
      "mode_defaults",
      "select_by_domain",
      "resolve_unique",
      "fallback_agent_view",
      "live_agent_view",
      "derive_agreements",
      "derive_disagreements",
      "create_action_tasks",
      "write_markdown_summary",
      "run_council",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/update_open_loops.py",
    "imports": [
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_memory.py",
    "imports": [
      "datetime",
      "pathlib",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/unresolved_intelligence_report.py",
    "imports": [
      "datetime",
      "html",
      "pathlib"
    ],
    "functions": [
      "esc",
      "cls"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/titan_reset_circuit_breaker.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/validate_executive_council.py",
    "imports": [
      "__future__",
      "agent_resolver",
      "agent_task_queue",
      "pathlib",
      "run_executive_council",
      "shutil",
      "tempfile"
    ],
    "functions": [
      "fail",
      "require",
      "prepare_temp_root",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/strategic_watchlists.py",
    "imports": [
      "collections",
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "load_entity_state"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/retrieve_memory.py",
    "imports": [
      "json",
      "sys",
      "urllib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/decision_intelligence.py",
    "imports": [
      "collections",
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "read"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/image_artifact.py",
    "imports": [
      "base64",
      "datetime",
      "json",
      "os",
      "pathlib",
      "subprocess",
      "sys",
      "urllib"
    ],
    "functions": [
      "load_env_file",
      "semantic_context",
      "openrouter_text",
      "build_visual_spec",
      "extract_prompt",
      "generate_with_openrouter",
      "generate_with_openai",
      "write_vault_record",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/validate_telegram_agent_commands.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "os",
      "pathlib",
      "shutil",
      "telegram_agent_commands",
      "tempfile"
    ],
    "functions": [
      "require",
      "prepare_temp_root",
      "main",
      "__init__",
      "reply_text",
      "__init__",
      "__init__"
    ],
    "classes": [
      "FakeMessage",
      "FakeUpdate",
      "FakeContext"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/daily_governance_index.py",
    "imports": [
      "datetime",
      "json",
      "ownership_router",
      "pathlib"
    ],
    "functions": [
      "now",
      "load_json",
      "save_json",
      "backup_json",
      "next_registry_id",
      "record_provenance",
      "route_record_owner",
      "mark_linked",
      "date_for_file",
      "norm_heading",
      "split_items",
      "extract_from_file",
      "entry_id",
      "discover_files",
      "rebuild",
      "write_markdown",
      "sync_follow_up_actions",
      "sync_open_loops",
      "mutate",
      "create_action_from_record",
      "promote_decision_record",
      "promote_decision_from_record",
      "promote_decisions",
      "promote_all_decisions",
      "promote_problem_from_record",
      "promote_problems",
      "sync_all",
      "main",
      "flush"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/hermes_enrich_latest_capture.py",
    "imports": [
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_opinions.py",
    "imports": [
      "agent_resolver",
      "datetime",
      "pathlib",
      "sys"
    ],
    "functions": [
      "now",
      "stance",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/perplexity_with_memory.py",
    "imports": [
      "json",
      "os",
      "pathlib",
      "subprocess",
      "sys",
      "urllib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/governance_intelligence.py",
    "imports": [
      "datetime",
      "json",
      "ownership_router",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "parse_date",
      "main",
      "add"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/historical_ingestion_candidates.py",
    "imports": [
      "collections",
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [
      "excluded",
      "score_file"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_council_pack.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "subprocess",
      "textwrap"
    ],
    "functions": [
      "ask_once"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/governance_register.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "sys"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "next_id",
      "add_decision",
      "add_risk",
      "add_action",
      "summary",
      "usage",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_ai_briefing.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "recommendation_quality"
    ],
    "functions": [
      "now",
      "load",
      "extract_lines",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/board_secretary.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "call_hermes",
      "fallback",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_committee_review.py",
    "imports": [
      "agent_resolver",
      "collections",
      "datetime",
      "json",
      "pathlib",
      "recommendation_quality"
    ],
    "functions": [
      "now",
      "load"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/recommendation_quality.py",
    "imports": [
      "__future__",
      "datetime",
      "hashlib",
      "json",
      "typing"
    ],
    "functions": [
      "today_plus",
      "stable_id",
      "normalise_agent",
      "default_owner",
      "is_generic_text",
      "confidence_score",
      "build_contract",
      "enrich_record_recommendation",
      "degraded_agent_review",
      "validate_contract",
      "validate_recommendations",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/run_daily_executive_briefing.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "argparse",
      "datetime",
      "json",
      "pathlib",
      "run_executive_council",
      "sys",
      "typing",
      "uuid"
    ],
    "functions": [
      "now",
      "parse_date",
      "is_open",
      "priority_rank",
      "load_recent_agent_outputs",
      "recent_council_decisions",
      "build_briefing",
      "task_line",
      "write_briefing",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/telegram_agent_commands.py",
    "imports": [
      "__future__",
      "agent_resolver",
      "agent_task_queue",
      "os",
      "pathlib",
      "run_daily_executive_briefing",
      "run_executive_council",
      "run_monthly_governance_review",
      "sys",
      "typing"
    ],
    "functions": [
      "second_brain_root",
      "ensure_script_path",
      "load_runtime",
      "context_args",
      "safe_handler",
      "format_aliases",
      "agents_response",
      "delegate_response",
      "open_tasks",
      "tasks_response",
      "task_response",
      "council_response",
      "dailybrief_response",
      "govreview_response",
      "register_agent_commands"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/panel_agents.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/titan_rca.py",
    "imports": [
      "collections",
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "load"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/reflection_intelligence.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_task_queue.py",
    "imports": [
      "__future__",
      "agent_resolver",
      "datetime",
      "json",
      "pathlib",
      "typing",
      "uuid"
    ],
    "functions": [
      "now",
      "default_root",
      "__init__",
      "ensure_storage",
      "load_tasks",
      "save_tasks",
      "generate_task_id",
      "audit_event",
      "resolve_assignment",
      "create_task",
      "get_task",
      "update_task",
      "close_task",
      "write_task_result"
    ],
    "classes": [
      "TaskQueueError",
      "AgentTaskQueue"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/enrich_capture.py",
    "imports": [
      "datetime",
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "has_any"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/strategic_memory_synthesis.py",
    "imports": [
      "datetime",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "read",
      "recent_files"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/alfred_overnight_jobs_status.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "run",
      "file_age",
      "rag_from_timer",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/ask_hybrid_agent.py",
    "imports": [
      "agent_resolver",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/titan_self_heal.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "run",
      "find_recovery",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/alfred_health_dashboard.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "zoneinfo"
    ],
    "functions": [
      "now",
      "run",
      "file_age_hours",
      "status_from_bool",
      "timer_status",
      "service_status",
      "file_fresh",
      "log_check",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/get_daily_section.py",
    "imports": [
      "__future__",
      "argparse",
      "datetime",
      "pathlib",
      "re",
      "sys",
      "zoneinfo"
    ],
    "functions": [
      "normalise_heading",
      "resolve_date",
      "extract_section",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/alfred_board_pack_generator.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "now",
      "load",
      "safe_text",
      "run_if_exists",
      "action_accountability",
      "section",
      "table",
      "build_pack"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/email_markdown_file.py",
    "imports": [
      "email",
      "html",
      "markdown",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/route_agents.py",
    "imports": [
      "agent_resolver",
      "agent_task_queue",
      "argparse",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/curate_entities.py",
    "imports": [
      "collections",
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [
      "norm",
      "safe_filename"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/entity_registry_maintenance.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "load_state",
      "save_state",
      "norm",
      "approved_names",
      "removed_names",
      "extract_companies_from_vault",
      "ai_match_entity",
      "refresh",
      "render_html",
      "init",
      "main",
      "esc",
      "approved_rows",
      "proposed_rows",
      "removed_rows",
      "unmatched_rows"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/intelligence_postprocess.py",
    "imports": [
      "datetime",
      "hashlib",
      "html",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "load_state",
      "save_state",
      "norm",
      "fp",
      "severity",
      "rank",
      "esc",
      "cls",
      "latest_watchlist_files",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/build_knowledge_graph.py",
    "imports": [
      "datetime",
      "pathlib",
      "re",
      "yaml"
    ],
    "functions": [
      "slugify",
      "ensure_entity_page",
      "inject_links"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/chatgpt_bridge.py",
    "imports": [
      "json",
      "knowledge_service",
      "sys"
    ],
    "functions": [
      "emit",
      "executive_state",
      "company",
      "person",
      "project",
      "risks",
      "decisions",
      "open_loops",
      "recent",
      "usage"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/create_agent_task.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "argparse",
      "json",
      "sys"
    ],
    "functions": [
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/rebuild_agent_registry.py",
    "imports": [
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "title_from_file",
      "infer_domain",
      "first_meaningful_line"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/task_lifecycle.py",
    "imports": [
      "datetime",
      "hashlib",
      "json",
      "pathlib"
    ],
    "functions": [
      "tid"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/athena_governance_watch.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "recommendation_quality"
    ],
    "functions": [
      "now",
      "load"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/process_capture_lifecycle.py",
    "imports": [
      "datetime",
      "pathlib",
      "shutil"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/entity_registry_server.py",
    "imports": [
      "datetime",
      "http",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "load_state",
      "save_state",
      "make_approved_from_match",
      "make_removed_from_match",
      "norm_name",
      "state_dedup",
      "safe_json_extract",
      "ai_format_entity",
      "main",
      "redirect",
      "do_GET",
      "do_POST"
    ],
    "classes": [
      "Handler"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/list_agent_tasks.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "argparse",
      "json"
    ],
    "functions": [
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_triage_approve.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "approve",
      "reject"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/board_session_from_secretary.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "stamp",
      "load",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/strategic_memory_action.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/ask_with_memory.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_council.py",
    "imports": [
      "agent_resolver",
      "datetime",
      "json",
      "pathlib",
      "recommendation_quality"
    ],
    "functions": [
      "now",
      "load",
      "latest_jsonl"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/second_brain_dashboard_server.py",
    "imports": [
      "datetime",
      "http",
      "json",
      "pathlib",
      "urllib"
    ],
    "functions": [
      "now",
      "esc",
      "load_loops",
      "save_loops",
      "next_id",
      "commands",
      "command_guide_html",
      "reindex",
      "do_GET",
      "do_POST",
      "render"
    ],
    "classes": [
      "H"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_committee.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "call_hermes",
      "fallback",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/classify_recent_captures.py",
    "imports": [
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/historical_ingest.py",
    "imports": [
      "datetime",
      "pathlib",
      "re",
      "subprocess"
    ],
    "functions": [
      "is_excluded",
      "safe_name"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/hermes_enrich_capture.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "re",
      "subprocess",
      "sys"
    ],
    "functions": [
      "ask_hermes",
      "extract_json",
      "yaml_list"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/strategic_memory.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/titan_control.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "allowed_ops",
      "request",
      "approve",
      "reject",
      "execute",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/board_decision_engine.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "stable_id",
      "add_event"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/technical_debt_monitor.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_state_scorecard.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/contextual_recommendation_engine.py",
    "imports": [
      "__future__",
      "argparse",
      "datetime",
      "hashlib",
      "json",
      "os",
      "pathlib",
      "re",
      "subprocess",
      "sys",
      "typing"
    ],
    "functions": [
      "now",
      "review_date",
      "runtime_path",
      "safe_read",
      "load_json",
      "save_json",
      "compact_text",
      "stable_id",
      "issue_query",
      "keywords",
      "score_text",
      "normalise_identity",
      "executable_agent_id",
      "json_context_sources",
      "iter_records",
      "search_json_context",
      "vault_roots",
      "search_obsidian_context",
      "run_command",
      "hermes_provider_required",
      "run_hermes_provider",
      "semantic_search",
      "collect_context",
      "should_attempt_openrouter",
      "agent_prompt",
      "call_agent",
      "degraded_view",
      "concrete_fallback_recommendation",
      "run_multi_model_review",
      "section_excerpt",
      "hermes_text_from_views",
      "is_trading_relevant",
      "contains_generic_only",
      "synthesise",
      "infer_owner",
      "source_references",
      "generate_contextual_recommendation",
      "enrich_recommendation_record",
      "run_agent_review",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/retrieval_planner.py",
    "imports": [
      "json",
      "re",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/ownership_router.py",
    "imports": [
      "__future__",
      "datetime",
      "typing"
    ],
    "functions": [
      "utc_now",
      "canonical_object_type",
      "clean_owner",
      "is_placeholder_owner",
      "assignment_source_is_manual",
      "assignment_source_is_automatic",
      "automatic_source_hint",
      "owner_is_replaceable",
      "context_text",
      "score_domains",
      "route_owner",
      "apply_ownership_route"
    ],
    "classes": [],
    "docstring": "Canonical Alfred governance ownership router."
  },
  {
    "file": "/opt/second-brain/scripts/alfred_operations_worker.py",
    "imports": [
      "__future__",
      "argparse",
      "datetime",
      "json",
      "os",
      "pathlib",
      "re",
      "subprocess",
      "sys",
      "time",
      "typing",
      "urllib"
    ],
    "functions": [
      "now",
      "read_json",
      "write_json",
      "append_jsonl",
      "load_events",
      "latest_operations",
      "operation_transition",
      "operation_output_link",
      "agent_output_link",
      "advisory_memo_link",
      "queued_operations",
      "normalised_status",
      "normalised_operation_type",
      "operation_by_id",
      "objective_id_for",
      "find_objective",
      "objective_evidence",
      "current_objective_score",
      "evaluate_objective",
      "concrete_objective_recommendation",
      "hermes_provider_script",
      "parse_json_output",
      "advisory_memo_engine_script",
      "run_executive_advisory_memo",
      "invoke_hermes_provider",
      "invoke_contextual_objective_review",
      "safe_filename",
      "create_action_for_objective",
      "agent_from_operation",
      "run_agent_review",
      "process_operation",
      "process_once",
      "process_operation_id",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/entity_registry.py",
    "imports": [
      "collections",
      "json",
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "load_registry",
      "registry_terms",
      "scan_vault",
      "propose",
      "suggest_category",
      "summary",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/objective_evidence_search.py",
    "imports": [
      "collections",
      "pathlib",
      "re"
    ],
    "functions": [
      "excluded",
      "priority",
      "is_generic_objective_text",
      "line_score",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_advisory_memo_engine.py",
    "imports": [
      "__future__",
      "argparse",
      "datetime",
      "hashlib",
      "json",
      "os",
      "pathlib",
      "re",
      "subprocess",
      "sys",
      "typing"
    ],
    "functions": [
      "now",
      "parse_time",
      "safe_filename",
      "stable_hash",
      "load_json",
      "write_json",
      "compact",
      "sentence",
      "scrub_internal_artifacts",
      "sanitize_section_value",
      "source_label",
      "owner_for",
      "score_or_status",
      "hermes_provider_script",
      "invoke_contextual_engine",
      "extract_provenance",
      "context_narrative",
      "multi_model_narrative",
      "option_paragraphs",
      "section_lines",
      "section_text",
      "context_record_count",
      "evidence_considered_text",
      "build_sections",
      "text_for_section",
      "is_generic",
      "contains_internal_artifact",
      "validate_memo_sections",
      "generate_memo",
      "memo_path",
      "latest_index_path",
      "source_key",
      "store_memo",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/propose_loops.py",
    "imports": [
      "datetime",
      "pathlib",
      "subprocess"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/hermes_intelligence_provider.py",
    "imports": [
      "__future__",
      "argparse",
      "datetime",
      "hashlib",
      "json",
      "os",
      "pathlib",
      "re",
      "subprocess",
      "sys",
      "typing"
    ],
    "functions": [
      "now",
      "runtime_path",
      "safe_filename",
      "stable_id",
      "compact",
      "load_json",
      "safe_read",
      "write_json",
      "append_jsonl",
      "operation_transition",
      "tokens",
      "score_record",
      "top_related",
      "records_from",
      "advisory_memo_records",
      "open_loop_records",
      "watchlist_findings",
      "obsidian_context",
      "build_context_pack",
      "hybrid_chain_script",
      "build_prompt",
      "run_hybrid_chain",
      "fallback_output",
      "extract_sections",
      "quality_gate",
      "lines",
      "build_result",
      "context_files",
      "context_records_considered",
      "source_references",
      "generate_intelligence",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/semantic_query_fast.py",
    "imports": [
      "json",
      "sys",
      "urllib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/ask_agent.py",
    "imports": [
      "json",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/delegate_request.py",
    "imports": [
      "agent_resolver",
      "agent_task_queue",
      "argparse",
      "datetime",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "choose_agent"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/orchestrate_agents_parallel.py",
    "imports": [
      "concurrent",
      "subprocess",
      "sys"
    ],
    "functions": [
      "run_agent"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/openrouter_research.py",
    "imports": [
      "json",
      "os",
      "pathlib",
      "requests",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/chief_delegate.py",
    "imports": [
      "agent_resolver",
      "agent_task_queue",
      "argparse",
      "concurrent",
      "datetime",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "run_agent"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/update_agent_task.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "argparse",
      "json",
      "sys"
    ],
    "functions": [
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/email_intelligence_digest.py",
    "imports": [
      "datetime",
      "email",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "load_env"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/contextual_watchlists.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "load_registry",
      "load_watchlists",
      "build_prompt",
      "run_chain",
      "extract_severity",
      "should_create_open_loop",
      "write_report",
      "write_open_loop",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/state_registry.py",
    "imports": [
      "datetime",
      "hashlib",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "oid"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/board_minutes.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "stamp",
      "run_capture",
      "create_minutes"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/run_agent_task.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "argparse",
      "subprocess",
      "sys"
    ],
    "functions": [
      "build_fallback_output",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/hermes_knowledge_api.py",
    "imports": [
      "http",
      "json",
      "knowledge_service",
      "pathlib",
      "time",
      "urllib"
    ],
    "functions": [
      "read_file",
      "list_recent",
      "norm",
      "score_name",
      "find_best_notes",
      "semantic_search",
      "read_url",
      "write_json",
      "scan_base",
      "do_GET",
      "log_message"
    ],
    "classes": [
      "Handler"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/strategic_memory_graph.py",
    "imports": [
      "collections",
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "normalise",
      "detect_domain"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/ask_agent_with_memory.py",
    "imports": [
      "json",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/tprm_evidence_search.py",
    "imports": [
      "__future__",
      "collections",
      "pathlib",
      "re"
    ],
    "functions": [
      "candidate_files",
      "path_priority",
      "evidence_score",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/board_meeting_engine.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "session_id",
      "latest_intel",
      "objective_snapshot",
      "make_session",
      "write_markdown",
      "list_sessions",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/athena_auto_escalation.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_intelligence_layer.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "now",
      "safe_read",
      "discover_dirs",
      "candidate_files",
      "classify_objectives",
      "title_for_file",
      "make_excerpt",
      "smart_evidence_context",
      "is_low_quality_evidence",
      "score_status",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_metrics_registry.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "trend_for",
      "board_recommendation",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/execution_update.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/board_office_intelligence.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/athena_finding_action.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/validate_agent_identity.py",
    "imports": [
      "__future__",
      "json",
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "fail",
      "load_json",
      "local_path",
      "normalise_alias",
      "require_non_empty",
      "scan_known_personas",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_dashboard_cache.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/render_daily_report_design.py",
    "imports": [
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [
      "status_card",
      "write_dashboard",
      "wrap_existing_brief",
      "render_governance_dashboard",
      "render_5am_dashboard",
      "render_reporting_pack_catalogue",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/titan_executor.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "shutil",
      "subprocess"
    ],
    "functions": [
      "now",
      "load_json",
      "write_json",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_knowledge_graph.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "now",
      "read",
      "classify_objectives",
      "is_bad_signal",
      "has_outcome_language",
      "excerpt_for",
      "discover_files",
      "structured_records",
      "file_records",
      "build_graph",
      "write_outputs",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/ai_agent_debate.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "call_hermes",
      "fallback",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/chatgpt_vault_answer.py",
    "imports": [
      "json",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "bridge"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/baselines/2026-06-28/engineering-spec/collect_alfred_inventory.py",
    "imports": [
      "ast",
      "datetime",
      "pathlib"
    ],
    "functions": [
  
```

### python/alfred_v2_python_inventory.json

Size: 619266 bytes

```text
[
  {
    "file": "/opt/alfred-v2/batch.py",
    "imports": [
      "__future__",
      "app",
      "datetime",
      "json",
      "pathlib",
      "sys",
      "traceback"
    ],
    "functions": [
      "_utcnow",
      "run",
      "step"
    ],
    "classes": [],
    "docstring": "Alfred v2 overnight batch runner.\n\nPer the spec Operating Model:\n  3. Overnight batch runs.\n  4. Alfred updates runtime state.\n  5. Morning Brief generated.\n\nOrder matters \u2014 insights are generated FIRST, then the Morning Brief consumes\nthem. Invoked by systemd timers:\n\n  daily   (every night 02:00)  ->  python batch.py daily\n  weekly  (Mon 02:00)          ->  python batch.py weekly\n  monthly (1st of month 02:00) ->  python batch.py monthly\n\nA monthly run implicitly includes weekly + daily; a weekly run includes daily.\nEvery run writes a machine-readable status file to data/last_batch.json and\nprints a summary (captured by journalctl)."
  },
  {
    "file": "/opt/alfred-v2/seed.py",
    "imports": [
      "__future__",
      "app"
    ],
    "functions": [
      "seed"
    ],
    "classes": [],
    "docstring": "Seed Alfred v2 with realistic sample objects so the app is clickable.\n\nIdempotent: only seeds if the DB has no objectives yet. Does NOT call the LLM\n(keeps seeding fast and offline-safe); workspaces/briefs are generated lazily\non first view, which is where the real Hermes calls happen."
  },
  {
    "file": "/opt/alfred-v2/app/auth.py",
    "imports": [
      "__future__",
      "email",
      "json",
      "os",
      "pathlib",
      "secrets",
      "subprocess",
      "time"
    ],
    "functions": [
      "_env",
      "allowed_emails",
      "_load",
      "_save",
      "_now",
      "_prune",
      "request_link",
      "verify_token",
      "session_email",
      "destroy_session"
    ],
    "classes": [],
    "docstring": "Alfred v2 authentication \u2014 passwordless magic-link, echoing Alfred Classic.\n\nSame mechanism Classic uses (/opt/second-brain/gui/server.py):\n  * ALLOWED_EMAILS whitelist\n  * one-time token emailed as a magic link via msmtp (-t)\n  * token expires in TOKEN_MINUTES; verifying it mints a session cookie\n  * session lasts SESSION_HOURS\n\nState persists in data/auth_state.json so logins survive restarts.\nReuses the same SMTP sender (msmtp 'hermes' / orlavid@gmail.com) and, by\ndefault, the SAME allowed-email list as Classic."
  },
  {
    "file": "/opt/alfred-v2/app/engine.py",
    "imports": [
      "__future__",
      "datetime",
      "json"
    ],
    "functions": [
      "_as_text",
      "classify_activity",
      "create_tracked_item_from_activity",
      "gather_evidence",
      "generate_forward_view",
      "_global_state_summary",
      "build_workspace",
      "get_or_build_workspace",
      "converse",
      "generate_morning_brief",
      "_prune_briefs",
      "latest_brief",
      "generate_review",
      "run_board_discussion",
      "add_intelligence",
      "archive_low_priority_intel",
      "overlap"
    ],
    "classes": [],
    "docstring": "Alfred v2 core engine.\n\nImplements the spec's behavioural rules:\n  * Classification Rules (new activity -> tracked item / project / objective / operational)\n  * Morning Brief (FIXED 6-section order, 30-day retention)\n  * Workspace generation (fixed section set, 5 types)\n  * Conversation (context inherited from workspace)\n  * Forward View (3 horizons: Tomorrow / Next 7 Days / Next 30 Days)\n  * External Intelligence (summarise / prioritise / de-noise / archive)\n  * Reviews (weekly / monthly / annual; summary editable, evidence not)\n  * Board Discussion (all enabled agents; auto draft minutes)\n\nHuman-controlled write-back: nothing here writes to Obsidian. Saving is an\nexplicit, separate user action handled by app.obsidian.save()."
  },
  {
    "file": "/opt/alfred-v2/app/watchlist.py",
    "imports": [
      "__future__",
      "json",
      "os",
      "pathlib",
      "re"
    ],
    "functions": [
      "available",
      "_norm_summary",
      "_rank",
      "load_findings",
      "external_intelligence",
      "briefing_lines",
      "evidence_text"
    ],
    "classes": [],
    "docstring": "Watchlist bridge \u2014 connects Alfred Classic's daily watchlist to Alfred v2's\nExternal Intelligence (per the spec's External Intelligence behaviour:\nSummarise / Prioritise / Remove noise / Archive automatically).\n\nREAD-ONLY. v2 never writes to Classic's watchlist state. The watchlist is the\nlive feed; v2 derives its External Intelligence view from it at read time.\n\nSource: /opt/second-brain/state/intelligence/watchlist_state.json\n  shape: {\"findings\": {<key>: {first_seen,last_seen,seen_count,severity,\n                                status,watchlist,report_path,summary}}, \"runs\":[...]}"
  },
  {
    "file": "/opt/alfred-v2/app/obsidian.py",
    "imports": [
      "__future__",
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [
      "_slug",
      "ensure_structure",
      "_is_within",
      "save",
      "search_vault",
      "recent_notes",
      "_yaml_val"
    ],
    "classes": [],
    "docstring": "Obsidian layer for Alfred v2.\n\nREAD: Alfred v2 may read the entire vault.\nWRITE: Alfred v2 may write NEW FILES ONLY, and ONLY under\n       07 AI Memory/Alfred v2/<category>/, and ONLY on explicit user approval\n       (\"Save to Obsidian\").\n\nHard guarantees enforced here (defence in depth, per spec write-back rules):\n  * Never write outside VAULT_WRITE_ROOT.\n  * Never overwrite an existing file (new files only) unless allow_overwrite.\n  * Never touch Daily Notes, existing Projects/Objectives, historical notes,\n    or source evidence."
  },
  {
    "file": "/opt/alfred-v2/app/insights.py",
    "imports": [
      "__future__",
      "datetime",
      "json"
    ],
    "functions": [
      "_today",
      "_parse_insights_json",
      "_store",
      "_degraded_item",
      "_daily_evidence",
      "_objective_project_state",
      "generate_daily_insights",
      "generate_weekly_insights",
      "generate_monthly_insights",
      "unconsumed_daily_insights",
      "mark_consumed",
      "recent"
    ],
    "classes": [],
    "docstring": "Alfred v2 Insight Engine.\n\nInsights are the OUTPUT of the overnight batch and the INPUT to the Morning\nBrief. They are first-class, drillable, save-able objects generated on three\ncadences, each with its own specification:\n\n  DAILY   \u2014 runs every night. Examines: yesterday's daily notes, new/changed\n            tracked items, open loops, and active external intelligence.\n            Produces: tactical \"what changed / what needs attention today\"\n            insights. These FEED that morning's brief (feeds_brief=1).\n\n  WEEKLY  \u2014 rolls up the last 7 days of DAILY insights + objective/project\n            health + the week's tracked-item closures. Produces pattern-level\n            insights (drift, recurring risk, momentum). Feeds the Weekly Review\n            and Monday's brief.\n\n  MONTHLY \u2014 rolls up the month's WEEKLY insights + objective progress vs intent.\n            Produces strategic insights. Feeds the Monthly Review.\n\nCascade: weekly consumes daily; monthly consumes weekly. Every insight records\n`rolled_up_from` (source insight ids) so the derivation is drillable.\n\nAll generation is evidence-led and degrades gracefully (explicitly labelled) if\nthe Hermes/OpenRouter path is unavailable \u2014 never fabricated."
  },
  {
    "file": "/opt/alfred-v2/app/agents.py",
    "imports": [
      "__future__",
      "json"
    ],
    "functions": [
      "seed_agents",
      "enabled_agents",
      "_prompt",
      "run_agent",
      "run_panel",
      "outputs_for"
    ],
    "classes": [],
    "docstring": "Agent framework for Alfred v2.\n\nCore Agents (spec): Alfred, Chief of Staff, Risk, Governance, Delivery,\nIntelligence, Knowledge, Strategy, Architecture, Compliance.\nUsers may create additional agents.\n\nEach agent produces drillable outputs: observations, recommendations, risks,\nchallenges, minority views. Outputs are persisted per object so individual\nagent opinions are drillable."
  },
  {
    "file": "/opt/alfred-v2/app/__init__.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": "Alfred v2 application package."
  },
  {
    "file": "/opt/alfred-v2/app/db.py",
    "imports": [
      "__future__",
      "contextlib",
      "datetime",
      "json",
      "pathlib",
      "sqlite3",
      "typing"
    ],
    "functions": [
      "now",
      "connect",
      "init_db",
      "insert",
      "update",
      "get",
      "query",
      "all_rows",
      "jdump",
      "jload"
    ],
    "classes": [],
    "docstring": "SQLite runtime state for Alfred v2.\n\nPer spec: SQLite = Runtime State, and Alfred v2 uses a SEPARATE runtime\ndatabase from Alfred Classic. This file is the only writer of that DB.\n\nSchema covers every Core Object and feature in the spec:\n  objectives, projects, tracked_items (with classification), operational_items,\n  agents, agent_outputs (observations/recommendations/risks/challenges/minority\n  views \u2014 drillable per agent), workspaces, conversation_messages,\n  reviews (weekly/monthly/annual), board_discussions + board_minutes,\n  forward_view, external_intelligence, morning_briefs (30-day retention),\n  writeback_log (audit of every Save to Obsidian)."
  },
  {
    "file": "/opt/alfred-v2/app/hermes.py",
    "imports": [
      "__future__",
      "json",
      "os",
      "pathlib",
      "urllib"
    ],
    "functions": [
      "_load_env",
      "available",
      "_call",
      "generate"
    ],
    "classes": [],
    "docstring": "Hermes processing layer for Alfred v2.\n\nReuses the SAME OpenRouter convention as the existing Classic hybrid router\n(/opt/second-brain/scripts/hybrid_openrouter.py): same endpoint, same model\nlanes, same fallback discipline, same /root/.openrouter.env credentials.\n\nPer spec: 'Evidence before conclusions' and 'Simplicity over complexity'.\nIf the model path is unavailable the system DEGRADES GRACEFULLY rather than\nfabricating conclusions \u2014 every degraded output is explicitly labelled."
  },
  {
    "file": "/opt/alfred-v2/app/config.py",
    "imports": [
      "__future__",
      "os",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": "Alfred v2 configuration.\n\nSingle-user Executive Operating System. Runs in PARALLEL with Alfred Classic.\n- Obsidian  = Memory (system of record)\n- Alfred    = User Experience (this app)\n- Hermes    = Processing Layer (OpenRouter via the proven hybrid path)\n- SQLite    = Runtime State (separate DB from Classic)"
  },
  {
    "file": "/opt/alfred-v2/app/main.py",
    "imports": [
      "__future__",
      "fastapi",
      "json",
      "pathlib"
    ],
    "functions": [
      "auth_login",
      "auth_request",
      "auth_verify",
      "auth_logout",
      "_startup",
      "page",
      "landing",
      "health",
      "v2_home",
      "v2_brief",
      "v2_brief_generate",
      "v2_object",
      "v2_rebuild",
      "v2_chat",
      "create_objective",
      "create_project",
      "create_tracked",
      "close_tracked",
      "v2_reviews",
      "gen_review",
      "v2_review",
      "edit_review",
      "v2_board",
      "create_board",
      "v2_board_detail",
      "edit_minutes",
      "v2_intel",
      "add_intel",
      "archive_low",
      "v2_search",
      "save_to_obsidian",
      "v2_writeback_log",
      "v2_insights",
      "v2_agents",
      "create_agent",
      "toggle_agent"
    ],
    "classes": [],
    "docstring": "Alfred v2 FastAPI application \u2014 routes + server-rendered UI.\n\nMounts a single landing page (Classic vs v2 selector) at /, and the full\nAlfred v2 workspace-first UX under /v2. All intelligence flows through the\nHermes processing layer; all write-back is explicit (\"Save to Obsidian\")."
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/typing_extensions.py",
    "imports": [
      "_socket",
      "abc",
      "annotationlib",
      "asyncio",
      "builtins",
      "collections",
      "contextlib",
      "enum",
      "functools",
      "inspect",
      "io",
      "keyword",
      "operator",
      "sys",
      "types",
      "typing",
      "warnings"
    ],
    "functions": [
      "IntVar",
      "_get_protocol_attrs",
      "_caller",
      "_set_default",
      "_set_module",
      "_create_concatenate_alias",
      "_concatenate_getitem",
      "_unpack_args",
      "_has_generic_or_protocol_as_origin",
      "_is_unpacked_typevartuple",
      "__repr__",
      "_should_collect_from_parameters",
      "_should_collect_from_parameters",
      "__init__",
      "__getattr__",
      "__mro_entries__",
      "__repr__",
      "__reduce__",
      "__call__",
      "__or__",
      "__ror__",
      "__instancecheck__",
      "__subclasscheck__",
      "__getitem__",
      "__repr__",
      "final",
      "disjoint_base",
      "_flatten_literal_params",
      "_value_and_type_iter",
      "overload",
      "get_overloads",
      "clear_overloads",
      "_is_dunder",
      "_allow_reckless_class_checks",
      "_no_init",
      "_type_check_issubclass_arg_1",
      "_proto_hook",
      "runtime_checkable",
      "_get_typeddict_qualifiers",
      "_create_typeddict",
      "TypedDict",
      "is_typeddict",
      "assert_type",
      "_strip_extras",
      "get_type_hints",
      "_could_be_inserted_optional",
      "_clean_optional",
      "get_origin",
      "get_args",
      "TypeAlias",
      "__instancecheck__",
      "Concatenate",
      "TypeGuard",
      "TypeIs",
      "TypeForm",
      "LiteralString",
      "Self",
      "Never",
      "Required",
      "NotRequired",
      "ReadOnly",
      "_is_unpack",
      "Unpack",
      "_is_unpack",
      "reveal_type",
      "assert_never",
      "dataclass_transform",
      "override",
      "_is_param_expr",
      "_is_param_expr",
      "_check_generic",
      "_check_generic",
      "_collect_type_vars",
      "_collect_parameters",
      "_make_nmtuple",
      "_namedtuple_mro_entries",
      "NamedTuple",
      "get_original_bases",
      "is_protocol",
      "get_protocol_members",
      "get_annotations",
      "_eval_with_owner",
      "evaluate_forward_ref",
      "__init__",
      "__repr__",
      "__getstate__",
      "type_repr",
      "__instancecheck__",
      "__repr__",
      "__new__",
      "__eq__",
      "__hash__",
      "__init__",
      "__getitem__",
      "__init__",
      "__setattr__",
      "__getitem__",
      "__new__",
      "__init__",
      "__subclasscheck__",
      "__instancecheck__",
      "__eq__",
      "__hash__",
      "__init_subclass__",
      "__int__",
      "__float__",
      "__complex__",
      "__bytes__",
      "__index__",
      "__abs__",
      "__round__",
      "read",
      "write",
      "__setattr__",
      "__new__",
      "__repr__",
      "__reduce__",
      "__new__",
      "__repr__",
      "__reduce__",
      "__new__",
      "__subclasscheck__",
      "__call__",
      "__mro_entries__",
      "__new__",
      "__init_subclass__",
      "__copy__",
      "__deepcopy__",
      "__init__",
      "__repr__",
      "__eq__",
      "__init__",
      "__repr__",
      "__eq__",
      "_type_convert",
      "__init__",
      "__repr__",
      "__hash__",
      "__call__",
      "__parameters__",
      "copy_with",
      "__getitem__",
      "__call__",
      "__init__",
      "__typing_unpacked_tuple_args__",
      "__typing_is_unpacked_typevartuple__",
      "__getitem__",
      "decorator",
      "__init__",
      "__call__",
      "__new__",
      "__call__",
      "__init__",
      "__mro_entries__",
      "__repr__",
      "__reduce__",
      "_is_unionable",
      "_is_unionable",
      "__init__",
      "__setattr__",
      "__delattr__",
      "_raise_attribute_error",
      "__repr__",
      "_check_parameters",
      "__getitem__",
      "__reduce__",
      "__init_subclass__",
      "__call__",
      "__init__",
      "__repr__",
      "__hash__",
      "__eq__",
      "__call__",
      "__or__",
      "__ror__",
      "_tvar_prepare_subst",
      "__new__",
      "__init_subclass__",
      "args",
      "kwargs",
      "__init__",
      "__repr__",
      "__hash__",
      "__eq__",
      "__reduce__",
      "__call__",
      "copy_with",
      "__getitem__",
      "__new__",
      "__init_subclass__",
      "__iter__",
      "__init__",
      "__repr__",
      "__hash__",
      "__eq__",
      "__reduce__",
      "__init_subclass__",
      "__or__",
      "__ror__",
      "__getattr__",
      "_check_single_param",
      "__or__",
      "__ror__",
      "__annotate__",
      "_paramspec_prepare_subst",
      "_typevartuple_prepare_subst",
      "__init_subclass__",
      "__new__",
      "__init_subclass__",
      "__init_subclass__",
      "wrapper"
    ],
    "classes": [
      "_Sentinel",
      "_SpecialForm",
      "_ExtensionsSpecialForm",
      "_DefaultMixin",
      "_TypeVarLikeMeta",
      "_EllipsisDummy",
      "Sentinel",
      "_AnyMeta",
      "Any",
      "_LiteralGenericAlias",
      "_LiteralForm",
      "_SpecialGenericAlias",
      "_ProtocolMeta",
      "Protocol",
      "SupportsInt",
      "SupportsFloat",
      "SupportsComplex",
      "SupportsBytes",
      "SupportsIndex",
      "SupportsAbs",
      "SupportsRound",
      "Reader",
      "Writer",
      "SingletonMeta",
      "NoDefaultType",
      "NoExtraItemsType",
      "_TypedDictMeta",
      "_TypedDictSpecialForm",
      "TypeVar",
      "_Immutable",
      "ParamSpecArgs",
      "ParamSpecKwargs",
      "_ConcatenateGenericAlias",
      "_TypeFormForm",
      "_UnpackSpecialForm",
      "_UnpackAlias",
      "deprecated",
      "_NamedTupleMeta",
      "Buffer",
      "NewType",
      "TypeAliasType",
      "Doc",
      "Format",
      "ParamSpec",
      "ParamSpec",
      "_ConcatenateGenericAlias",
      "TypeVarTuple",
      "TypeVarTuple",
      "_TypeAliasGenericAlias",
      "Dummy"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/concurrency.py",
    "imports": [
      "__future__",
      "anyio",
      "functools",
      "sys",
      "typing",
      "typing_extensions",
      "warnings"
    ],
    "functions": [
      "_next"
    ],
    "classes": [
      "_StopIteration"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/routing.py",
    "imports": [
      "__future__",
      "contextlib",
      "enum",
      "functools",
      "inspect",
      "re",
      "starlette",
      "traceback",
      "types",
      "typing",
      "warnings"
    ],
    "functions": [
      "iscoroutinefunction_or_partial",
      "request_response",
      "websocket_session",
      "get_name",
      "replace_params",
      "compile_path",
      "_wrap_gen_lifespan_context",
      "__init__",
      "matches",
      "url_path_for",
      "__init__",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "routes",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "routes",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "wrapper",
      "__init__",
      "__call__",
      "__init__",
      "url_path_for",
      "__eq__",
      "mount",
      "host",
      "add_route",
      "add_websocket_route",
      "route",
      "websocket_route",
      "add_event_handler",
      "on_event",
      "decorator",
      "decorator",
      "decorator"
    ],
    "classes": [
      "NoMatchFound",
      "Match",
      "BaseRoute",
      "Route",
      "WebSocketRoute",
      "Mount",
      "Host",
      "_AsyncLiftContextManager",
      "_DefaultLifespan",
      "Router"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/templating.py",
    "imports": [
      "__future__",
      "jinja2",
      "os",
      "starlette",
      "typing",
      "warnings"
    ],
    "functions": [
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "_create_env",
      "_setup_env_defaults",
      "get_template",
      "TemplateResponse",
      "TemplateResponse",
      "TemplateResponse",
      "url_for"
    ],
    "classes": [
      "_TemplateResponse",
      "Jinja2Templates"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/requests.py",
    "imports": [
      "__future__",
      "anyio",
      "http",
      "json",
      "multipart",
      "python_multipart",
      "starlette",
      "typing"
    ],
    "functions": [
      "cookie_parser",
      "__init__",
      "__getitem__",
      "__iter__",
      "__len__",
      "app",
      "url",
      "base_url",
      "headers",
      "query_params",
      "path_params",
      "cookies",
      "client",
      "session",
      "auth",
      "user",
      "state",
      "url_for",
      "__init__",
      "method",
      "receive",
      "form"
    ],
    "classes": [
      "ClientDisconnect",
      "HTTPConnection",
      "Request"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/schemas.py",
    "imports": [
      "__future__",
      "inspect",
      "re",
      "starlette",
      "typing",
      "yaml"
    ],
    "functions": [
      "render",
      "get_schema",
      "get_endpoints",
      "_remove_converter",
      "parse_docstring",
      "OpenAPIResponse",
      "__init__",
      "get_schema"
    ],
    "classes": [
      "OpenAPIResponse",
      "EndpointInfo",
      "BaseSchemaGenerator",
      "SchemaGenerator"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/_utils.py",
    "imports": [
      "__future__",
      "contextlib",
      "exceptiongroup",
      "functools",
      "inspect",
      "starlette",
      "sys",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "is_async_callable",
      "is_async_callable",
      "is_async_callable",
      "collapse_excgroups",
      "get_route_path",
      "__init__",
      "__await__"
    ],
    "classes": [
      "AwaitableOrContextManager",
      "SupportsAsyncClose",
      "AwaitableOrContextManagerWrapper"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/status.py",
    "imports": [
      "__future__"
    ],
    "functions": [],
    "classes": [],
    "docstring": "HTTP codes\nSee HTTP Status Code Registry:\nhttps://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml\n\nAnd RFC 2324 - https://tools.ietf.org/html/rfc2324"
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/websockets.py",
    "imports": [
      "__future__",
      "enum",
      "json",
      "starlette",
      "typing"
    ],
    "functions": [
      "__init__",
      "__init__",
      "_raise_on_disconnect",
      "__init__"
    ],
    "classes": [
      "WebSocketState",
      "WebSocketDisconnect",
      "WebSocket",
      "WebSocketClose"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/__init__.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/applications.py",
    "imports": [
      "__future__",
      "starlette",
      "sys",
      "typing",
      "typing_extensions",
      "warnings"
    ],
    "functions": [
      "__init__",
      "build_middleware_stack",
      "routes",
      "url_path_for",
      "on_event",
      "mount",
      "host",
      "add_middleware",
      "add_exception_handler",
      "add_event_handler",
      "add_route",
      "add_websocket_route",
      "exception_handler",
      "route",
      "websocket_route",
      "middleware",
      "decorator",
      "decorator",
      "decorator",
      "decorator"
    ],
    "classes": [
      "Starlette"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/authentication.py",
    "imports": [
      "__future__",
      "functools",
      "inspect",
      "starlette",
      "sys",
      "typing",
      "typing_extensions",
      "urllib"
    ],
    "functions": [
      "has_required_scope",
      "requires",
      "decorator",
      "__init__",
      "is_authenticated",
      "display_name",
      "identity",
      "__init__",
      "is_authenticated",
      "display_name",
      "is_authenticated",
      "display_name",
      "sync_wrapper"
    ],
    "classes": [
      "AuthenticationError",
      "AuthenticationBackend",
      "AuthCredentials",
      "BaseUser",
      "SimpleUser",
      "UnauthenticatedUser"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/_exception_handler.py",
    "imports": [
      "__future__",
      "starlette",
      "typing"
    ],
    "functions": [
      "_lookup_exception_handler",
      "wrap_app_handling_exceptions"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/datastructures.py",
    "imports": [
      "__future__",
      "shlex",
      "starlette",
      "typing",
      "urllib"
    ],
    "functions": [
      "__init__",
      "components",
      "scheme",
      "netloc",
      "path",
      "query",
      "fragment",
      "username",
      "password",
      "hostname",
      "port",
      "is_secure",
      "replace",
      "include_query_params",
      "replace_query_params",
      "remove_query_params",
      "__eq__",
      "__str__",
      "__repr__",
      "__new__",
      "__init__",
      "make_absolute_url",
      "__init__",
      "__repr__",
      "__str__",
      "__bool__",
      "__init__",
      "__len__",
      "__getitem__",
      "__iter__",
      "__repr__",
      "__str__",
      "__init__",
      "getlist",
      "keys",
      "values",
      "items",
      "multi_items",
      "__getitem__",
      "__contains__",
      "__iter__",
      "__len__",
      "__eq__",
      "__repr__",
      "__setitem__",
      "__delitem__",
      "pop",
      "popitem",
      "poplist",
      "clear",
      "setdefault",
      "setlist",
      "append",
      "update",
      "__init__",
      "__str__",
      "__repr__",
      "__init__",
      "content_type",
      "_in_memory",
      "__repr__",
      "__init__",
      "__init__",
      "raw",
      "keys",
      "values",
      "items",
      "getlist",
      "mutablecopy",
      "__getitem__",
      "__contains__",
      "__iter__",
      "__len__",
      "__eq__",
      "__repr__",
      "__setitem__",
      "__delitem__",
      "__ior__",
      "__or__",
      "raw",
      "setdefault",
      "update",
      "append",
      "add_vary_header",
      "__init__",
      "__setattr__",
      "__getattr__",
      "__delattr__"
    ],
    "classes": [
      "Address",
      "URL",
      "URLPath",
      "Secret",
      "CommaSeparatedStrings",
      "ImmutableMultiDict",
      "MultiDict",
      "QueryParams",
      "UploadFile",
      "FormData",
      "Headers",
      "MutableHeaders",
      "State"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/types.py",
    "imports": [
      "starlette",
      "typing"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/exceptions.py",
    "imports": [
      "__future__",
      "collections",
      "http"
    ],
    "functions": [
      "__init__",
      "__str__",
      "__repr__",
      "__init__",
      "__str__",
      "__repr__"
    ],
    "classes": [
      "HTTPException",
      "WebSocketException"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/formparsers.py",
    "imports": [
      "__future__",
      "dataclasses",
      "enum",
      "multipart",
      "python_multipart",
      "starlette",
      "tempfile",
      "typing",
      "urllib"
    ],
    "functions": [
      "_user_safe_decode",
      "__init__",
      "__init__",
      "on_field_start",
      "on_field_name",
      "on_field_data",
      "on_field_end",
      "on_end",
      "__init__",
      "on_part_begin",
      "on_part_data",
      "on_part_end",
      "on_header_field",
      "on_header_value",
      "on_header_end",
      "on_headers_finished",
      "on_end"
    ],
    "classes": [
      "FormMessage",
      "MultipartPart",
      "MultiPartException",
      "FormParser",
      "MultiPartParser"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/config.py",
    "imports": [
      "__future__",
      "os",
      "pathlib",
      "typing",
      "warnings"
    ],
    "functions": [
      "__init__",
      "__getitem__",
      "__setitem__",
      "__delitem__",
      "__iter__",
      "__len__",
      "__init__",
      "__call__",
      "__call__",
      "__call__",
      "__call__",
      "__call__",
      "__call__",
      "get",
      "_read_file",
      "_perform_cast"
    ],
    "classes": [
      "undefined",
      "EnvironError",
      "Environ",
      "Config"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/background.py",
    "imports": [
      "__future__",
      "starlette",
      "sys",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "__init__",
      "__init__",
      "add_task"
    ],
    "classes": [
      "BackgroundTask",
      "BackgroundTasks"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/endpoints.py",
    "imports": [
      "__future__",
      "json",
      "starlette",
      "typing"
    ],
    "functions": [
      "__init__",
      "__await__",
      "__init__",
      "__await__"
    ],
    "classes": [
      "HTTPEndpoint",
      "WebSocketEndpoint"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/testclient.py",
    "imports": [
      "__future__",
      "anyio",
      "concurrent",
      "contextlib",
      "httpx",
      "inspect",
      "io",
      "json",
      "math",
      "starlette",
      "sys",
      "types",
      "typing",
      "typing_extensions",
      "urllib",
      "warnings"
    ],
    "functions": [
      "_is_asgi3",
      "__init__",
      "__init__",
      "__init__",
      "__enter__",
      "__exit__",
      "_raise_on_close",
      "send",
      "send_text",
      "send_bytes",
      "send_json",
      "close",
      "receive",
      "receive_text",
      "receive_bytes",
      "receive_json",
      "__init__",
      "handle_request",
      "__init__",
      "_portal_factory",
      "request",
      "get",
      "options",
      "head",
      "post",
      "put",
      "patch",
      "delete",
      "websocket_connect",
      "__enter__",
      "__exit__",
      "reset_portal",
      "wait_shutdown"
    ],
    "classes": [
      "_WrapASGI2",
      "_AsyncBackend",
      "_Upgrade",
      "WebSocketDenialResponse",
      "WebSocketTestSession",
      "_TestClientTransport",
      "TestClient"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/responses.py",
    "imports": [
      "__future__",
      "anyio",
      "datetime",
      "email",
      "functools",
      "hashlib",
      "http",
      "json",
      "mimetypes",
      "os",
      "re",
      "secrets",
      "starlette",
      "stat",
      "typing",
      "urllib",
      "warnings"
    ],
    "functions": [
      "__init__",
      "render",
      "init_headers",
      "headers",
      "set_cookie",
      "delete_cookie",
      "__init__",
      "render",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "set_stat_headers",
      "_should_use_range",
      "_parse_range_header",
      "generate_multipart"
    ],
    "classes": [
      "Response",
      "HTMLResponse",
      "PlainTextResponse",
      "JSONResponse",
      "RedirectResponse",
      "StreamingResponse",
      "MalformedRangeHeader",
      "RangeNotSatisfiable",
      "FileResponse"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/convertors.py",
    "imports": [
      "__future__",
      "math",
      "typing",
      "uuid"
    ],
    "functions": [
      "register_url_convertor",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string"
    ],
    "classes": [
      "Convertor",
      "StringConvertor",
      "PathConvertor",
      "IntegerConvertor",
      "FloatConvertor",
      "UUIDConvertor"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/staticfiles.py",
    "imports": [
      "__future__",
      "anyio",
      "email",
      "errno",
      "importlib",
      "os",
      "starlette",
      "stat",
      "typing"
    ],
    "functions": [
      "__init__",
      "__init__",
      "get_directories",
      "get_path",
      "lookup_path",
      "file_response",
      "is_not_modified"
    ],
    "classes": [
      "NotModifiedResponse",
      "StaticFiles"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/annotated_types/__init__.py",
    "imports": [
      "dataclasses",
      "datetime",
      "math",
      "sys",
      "types",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "__gt__",
      "__ge__",
      "__lt__",
      "__le__",
      "__mod__",
      "__div__",
      "__is_annotated_types_grouped_metadata__",
      "__iter__",
      "__iter__",
      "__iter__",
      "__repr__",
      "__call__",
      "__init_subclass__",
      "__iter__",
      "doc"
    ],
    "classes": [
      "SupportsGt",
      "SupportsGe",
      "SupportsLt",
      "SupportsLe",
      "SupportsMod",
      "SupportsDiv",
      "BaseMetadata",
      "Gt",
      "Ge",
      "Lt",
      "Le",
      "GroupedMetadata",
      "Interval",
      "MultipleOf",
      "MinLen",
      "MaxLen",
      "Len",
      "Timezone",
      "Unit",
      "Predicate",
      "Not",
      "DocInfo"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/annotated_types/test_cases.py",
    "imports": [
      "annotated_types",
      "datetime",
      "decimal",
      "math",
      "sys",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "cases",
      "__iter__"
    ],
    "classes": [
      "Case",
      "MyCustomGroupedMetadata"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/_yaml/__init__.py",
    "imports": [
      "sys",
      "warnings",
      "yaml"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/events.py",
    "imports": [],
    "functions": [
      "__init__",
      "__repr__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__"
    ],
    "classes": [
      "Event",
      "NodeEvent",
      "CollectionStartEvent",
      "CollectionEndEvent",
      "StreamStartEvent",
      "StreamEndEvent",
      "DocumentStartEvent",
      "DocumentEndEvent",
      "AliasEvent",
      "ScalarEvent",
      "SequenceStartEvent",
      "SequenceEndEvent",
      "MappingStartEvent",
      "MappingEndEvent"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/nodes.py",
    "imports": [],
    "functions": [
      "__init__",
      "__repr__",
      "__init__",
      "__init__"
    ],
    "classes": [
      "Node",
      "ScalarNode",
      "CollectionNode",
      "SequenceNode",
      "MappingNode"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/parser.py",
    "imports": [
      "error",
      "events",
      "scanner",
      "tokens"
    ],
    "functions": [
      "__init__",
      "dispose",
      "check_event",
      "peek_event",
      "get_event",
      "parse_stream_start",
      "parse_implicit_document_start",
      "parse_document_start",
      "parse_document_end",
      "parse_document_content",
      "process_directives",
      "parse_block_node",
      "parse_flow_node",
      "parse_block_node_or_indentless_sequence",
      "parse_node",
      "parse_block_sequence_first_entry",
      "parse_block_sequence_entry",
      "parse_indentless_sequence_entry",
      "parse_block_mapping_first_key",
      "parse_block_mapping_key",
      "parse_block_mapping_value",
      "parse_flow_sequence_first_entry",
      "parse_flow_sequence_entry",
      "parse_flow_sequence_entry_mapping_key",
      "parse_flow_sequence_entry_mapping_value",
      "parse_flow_sequence_entry_mapping_end",
      "parse_flow_mapping_first_key",
      "parse_flow_mapping_key",
      "parse_flow_mapping_value",
      "parse_flow_mapping_empty_value",
      "process_empty_scalar"
    ],
    "classes": [
      "ParserError",
      "Parser"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/tokens.py",
    "imports": [],
    "functions": [
      "__init__",
      "__repr__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__"
    ],
    "classes": [
      "Token",
      "DirectiveToken",
      "DocumentStartToken",
      "DocumentEndToken",
      "StreamStartToken",
      "StreamEndToken",
      "BlockSequenceStartToken",
      "BlockMappingStartToken",
      "BlockEndToken",
      "FlowSequenceStartToken",
      "FlowMappingStartToken",
      "FlowSequenceEndToken",
      "FlowMappingEndToken",
      "KeyToken",
      "ValueToken",
      "BlockEntryToken",
      "FlowEntryToken",
      "AliasToken",
      "AnchorToken",
      "TagToken",
      "ScalarToken"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/emitter.py",
    "imports": [
      "error",
      "events"
    ],
    "functions": [
      "__init__",
      "__init__",
      "dispose",
      "emit",
      "need_more_events",
      "need_events",
      "increase_indent",
      "expect_stream_start",
      "expect_nothing",
      "expect_first_document_start",
      "expect_document_start",
      "expect_document_end",
      "expect_document_root",
      "expect_node",
      "expect_alias",
      "expect_scalar",
      "expect_flow_sequence",
      "expect_first_flow_sequence_item",
      "expect_flow_sequence_item",
      "expect_flow_mapping",
      "expect_first_flow_mapping_key",
      "expect_flow_mapping_key",
      "expect_flow_mapping_simple_value",
      "expect_flow_mapping_value",
      "expect_block_sequence",
      "expect_first_block_sequence_item",
      "expect_block_sequence_item",
      "expect_block_mapping",
      "expect_first_block_mapping_key",
      "expect_block_mapping_key",
      "expect_block_mapping_simple_value",
      "expect_block_mapping_value",
      "check_empty_sequence",
      "check_empty_mapping",
      "check_empty_document",
      "check_simple_key",
      "process_anchor",
      "process_tag",
      "choose_scalar_style",
      "process_scalar",
      "prepare_version",
      "prepare_tag_handle",
      "prepare_tag_prefix",
      "prepare_tag",
      "prepare_anchor",
      "analyze_scalar",
      "flush_stream",
      "write_stream_start",
      "write_stream_end",
      "write_indicator",
      "write_indent",
      "write_line_break",
      "write_version_directive",
      "write_tag_directive",
      "write_single_quoted",
      "write_double_quoted",
      "determine_block_hints",
      "write_folded",
      "write_literal",
      "write_plain"
    ],
    "classes": [
      "EmitterError",
      "ScalarAnalysis",
      "Emitter"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/scanner.py",
    "imports": [
      "error",
      "tokens"
    ],
    "functions": [
      "__init__",
      "__init__",
      "check_token",
      "peek_token",
      "get_token",
      "need_more_tokens",
      "fetch_more_tokens",
      "next_possible_simple_key",
      "stale_possible_simple_keys",
      "save_possible_simple_key",
      "remove_possible_simple_key",
      "unwind_indent",
      "add_indent",
      "fetch_stream_start",
      "fetch_stream_end",
      "fetch_directive",
      "fetch_document_start",
      "fetch_document_end",
      "fetch_document_indicator",
      "fetch_flow_sequence_start",
      "fetch_flow_mapping_start",
      "fetch_flow_collection_start",
      "fetch_flow_sequence_end",
      "fetch_flow_mapping_end",
      "fetch_flow_collection_end",
      "fetch_flow_entry",
      "fetch_block_entry",
      "fetch_key",
      "fetch_value",
      "fetch_alias",
      "fetch_anchor",
      "fetch_tag",
      "fetch_literal",
      "fetch_folded",
      "fetch_block_scalar",
      "fetch_single",
      "fetch_double",
      "fetch_flow_scalar",
      "fetch_plain",
      "check_directive",
      "check_document_start",
      "check_document_end",
      "check_block_entry",
      "check_key",
      "check_value",
      "check_plain",
      "scan_to_next_token",
      "scan_directive",
      "scan_directive_name",
      "scan_yaml_directive_value",
      "scan_yaml_directive_number",
      "scan_tag_directive_value",
      "scan_tag_directive_handle",
      "scan_tag_directive_prefix",
      "scan_directive_ignored_line",
      "scan_anchor",
      "scan_tag",
      "scan_block_scalar",
      "scan_block_scalar_indicators",
      "scan_block_scalar_ignored_line",
      "scan_block_scalar_indentation",
      "scan_block_scalar_breaks",
      "scan_flow_scalar",
      "scan_flow_scalar_non_spaces",
      "scan_flow_scalar_spaces",
      "scan_flow_scalar_breaks",
      "scan_plain",
      "scan_plain_spaces",
      "scan_tag_handle",
      "scan_tag_uri",
      "scan_uri_escapes",
      "scan_line_break"
    ],
    "classes": [
      "ScannerError",
      "SimpleKey",
      "Scanner"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/representer.py",
    "imports": [
      "datetime",
      "error",
      "nodes"
    ],
    "functions": [
      "__init__",
      "represent",
      "represent_data",
      "add_representer",
      "add_multi_representer",
      "represent_scalar",
      "represent_sequence",
      "represent_mapping",
      "ignore_aliases",
      "ignore_aliases",
      "represent_none",
      "represent_str",
      "represent_binary",
      "represent_bool",
      "represent_int",
      "represent_float",
      "represent_list",
      "represent_dict",
      "represent_set",
      "represent_date",
      "represent_datetime",
      "represent_yaml_object",
      "represent_undefined",
      "represent_complex",
      "represent_tuple",
      "represent_name",
      "represent_module",
      "represent_object",
      "represent_ordered_dict"
    ],
    "classes": [
      "RepresenterError",
      "BaseRepresenter",
      "SafeRepresenter",
      "Representer"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/resolver.py",
    "imports": [
      "error",
      "nodes",
      "re"
    ],
    "functions": [
      "__init__",
      "add_implicit_resolver",
      "add_path_resolver",
      "descend_resolver",
      "ascend_resolver",
      "check_resolver_prefix",
      "resolve"
    ],
    "classes": [
      "ResolverError",
      "BaseResolver",
      "Resolver"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/__init__.py",
    "imports": [
      "cyaml",
      "dumper",
      "error",
      "events",
      "io",
      "loader",
      "nodes",
      "tokens"
    ],
    "functions": [
      "warnings",
      "scan",
      "parse",
      "compose",
      "compose_all",
      "load",
      "load_all",
      "full_load",
      "full_load_all",
      "safe_load",
      "safe_load_all",
      "unsafe_load",
      "unsafe_load_all",
      "emit",
      "serialize_all",
      "serialize",
      "dump_all",
      "dump",
      "safe_dump_all",
      "safe_dump",
      "add_implicit_resolver",
      "add_path_resolver",
      "add_constructor",
      "add_multi_constructor",
      "add_representer",
      "add_multi_representer",
      "__init__",
      "from_yaml",
      "to_yaml"
    ],
    "classes": [
      "YAMLObjectMetaclass",
      "YAMLObject"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/serializer.py",
    "imports": [
      "error",
      "events",
      "nodes"
    ],
    "functions": [
      "__init__",
      "open",
      "close",
      "serialize",
      "anchor_node",
      "generate_anchor",
      "serialize_node"
    ],
    "classes": [
      "SerializerError",
      "Serializer"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/constructor.py",
    "imports": [
      "collections",
      "error",
      "nodes"
    ],
    "functions": [
      "__init__",
      "check_data",
      "check_state_key",
      "get_data",
      "get_single_data",
      "construct_document",
      "construct_object",
      "construct_scalar",
      "construct_sequence",
      "construct_mapping",
      "construct_pairs",
      "add_constructor",
      "add_multi_constructor",
      "construct_scalar",
      "flatten_mapping",
      "construct_mapping",
      "construct_yaml_null",
      "construct_yaml_bool",
      "construct_yaml_int",
      "construct_yaml_float",
      "construct_yaml_binary",
      "construct_yaml_timestamp",
      "construct_yaml_omap",
      "construct_yaml_pairs",
      "construct_yaml_set",
      "construct_yaml_str",
      "construct_yaml_seq",
      "construct_yaml_map",
      "construct_yaml_object",
      "construct_undefined",
      "get_state_keys_blacklist",
      "get_state_keys_blacklist_regexp",
      "construct_python_str",
      "construct_python_unicode",
      "construct_python_bytes",
      "construct_python_long",
      "construct_python_complex",
      "construct_python_tuple",
      "find_python_module",
      "find_python_name",
      "construct_python_name",
      "construct_python_module",
      "make_python_instance",
      "set_python_instance_state",
      "construct_python_object",
      "construct_python_object_apply",
      "construct_python_object_new",
      "find_python_module",
      "find_python_name",
      "make_python_instance",
      "set_python_instance_state"
    ],
    "classes": [
      "ConstructorError",
      "BaseConstructor",
      "SafeConstructor",
      "FullConstructor",
      "UnsafeConstructor",
      "Constructor"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/loader.py",
    "imports": [
      "composer",
      "constructor",
      "parser",
      "reader",
      "resolver",
      "scanner"
    ],
    "functions": [
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__"
    ],
    "classes": [
      "BaseLoader",
      "FullLoader",
      "SafeLoader",
      "Loader",
      "UnsafeLoader"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/error.py",
    "imports": [],
    "functions": [
      "__init__",
      "get_snippet",
      "__str__",
      "__init__",
      "__str__"
    ],
    "classes": [
      "Mark",
      "YAMLError",
      "MarkedYAMLError"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/composer.py",
    "imports": [
      "error",
      "events",
      "nodes"
    ],
    "functions": [
      "__init__",
      "check_node",
      "get_node",
      "get_single_node",
      "compose_document",
      "compose_node",
      "compose_scalar_node",
      "compose_sequence_node",
      "compose_mapping_node"
    ],
    "classes": [
      "ComposerError",
      "Composer"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/reader.py",
    "imports": [
      "codecs",
      "error"
    ],
    "functions": [
      "__init__",
      "__str__",
      "__init__",
      "peek",
      "prefix",
      "forward",
      "get_mark",
      "determine_encoding",
      "check_printable",
      "update",
      "update_raw"
    ],
    "classes": [
      "ReaderError",
      "Reader"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/dumper.py",
    "imports": [
      "emitter",
      "representer",
      "resolver",
      "serializer"
    ],
    "functions": [
      "__init__",
      "__init__",
      "__init__"
    ],
    "classes": [
      "BaseDumper",
      "SafeDumper",
      "Dumper"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/cyaml.py",
    "imports": [
      "constructor",
      "representer",
      "resolver",
      "serializer",
      "yaml"
    ],
    "functions": [
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__"
    ],
    "classes": [
      "CBaseLoader",
      "CSafeLoader",
      "CFullLoader",
      "CUnsafeLoader",
      "CLoader",
      "CBaseDumper",
      "CSafeDumper",
      "CDumper"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/pydantic_core/core_schema.py",
    "imports": [
      "__future__",
      "collections",
      "datetime",
      "decimal",
      "pydantic_core",
      "re",
      "sys",
      "typing",
      "typing_extensions",
      "warnings"
    ],
    "functions": [
      "simple_ser_schema",
      "plain_serializer_function_ser_schema",
      "wrap_serializer_function_ser_schema",
      "format_ser_schema",
      "to_string_ser_schema",
      "model_ser_schema",
      "invalid_schema",
      "computed_field",
      "any_schema",
      "none_schema",
      "bool_schema",
      "int_schema",
      "float_schema",
      "decimal_schema",
      "complex_schema",
      "str_schema",
      "bytes_schema",
      "date_schema",
      "time_schema",
      "datetime_schema",
      "timedelta_schema",
      "literal_schema",
      "enum_schema",
      "missing_sentinel_schema",
      "is_instance_schema",
      "is_subclass_schema",
      "callable_schema",
      "uuid_schema",
      "filter_seq_schema",
      "list_schema",
      "tuple_positional_schema",
      "tuple_variable_schema",
      "tuple_schema",
      "set_schema",
      "frozenset_schema",
      "generator_schema",
      "filter_dict_schema",
      "dict_schema",
      "no_info_before_validator_function",
      "with_info_before_validator_function",
      "no_info_after_validator_function",
      "with_info_after_validator_function",
      "no_info_wrap_validator_function",
      "with_info_wrap_validator_function",
      "no_info_plain_validator_function",
      "with_info_plain_validator_function",
      "with_default_schema",
      "nullable_schema",
      "union_schema",
      "tagged_union_schema",
      "chain_schema",
      "lax_or_strict_schema",
      "json_or_python_schema",
      "typed_dict_field",
      "typed_dict_schema",
      "model_field",
      "model_fields_schema",
      "model_schema",
      "dataclass_field",
      "dataclass_args_schema",
      "dataclass_schema",
      "arguments_parameter",
      "arguments_schema",
      "arguments_v3_parameter",
      "arguments_v3_schema",
      "call_schema",
      "custom_error_schema",
      "json_schema",
      "url_schema",
      "multi_host_url_schema",
      "definitions_schema",
      "definition_reference_schema",
      "_dict_not_none",
      "iter_union_choices",
      "field_before_validator_function",
      "general_before_validator_function",
      "field_after_validator_function",
      "general_after_validator_function",
      "field_wrap_validator_function",
      "general_wrap_validator_function",
      "field_plain_validator_function",
      "general_plain_validator_function",
      "__getattr__",
      "include",
      "exclude",
      "context",
      "mode",
      "by_alias",
      "exclude_unset",
      "exclude_defaults",
      "exclude_none",
      "exclude_computed_fields",
      "serialize_as_any",
      "polymorphic_serialization",
      "round_trip",
      "mode_is_json",
      "__str__",
      "__repr__",
      "field_name",
      "context",
      "config",
      "mode",
      "data",
      "field_name",
      "__call__",
      "__call__"
    ],
    "classes": [
      "CoreConfig",
      "SerializationInfo",
      "FieldSerializationInfo",
      "ValidationInfo",
      "SimpleSerSchema",
      "PlainSerializerFunctionSerSchema",
      "SerializerFunctionWrapHandler",
      "WrapSerializerFunctionSerSchema",
      "FormatSerSchema",
      "ToStringSerSchema",
      "ModelSerSchema",
      "InvalidSchema",
      "ComputedField",
      "AnySchema",
      "NoneSchema",
      "BoolSchema",
      "IntSchema",
      "FloatSchema",
      "DecimalSchema",
      "ComplexSchema",
      "StringSchema",
      "BytesSchema",
      "DateSchema",
      "TimeSchema",
      "DatetimeSchema",
      "TimedeltaSchema",
      "LiteralSchema",
      "EnumSchema",
      "MissingSentinelSchema",
      "IsInstanceSchema",
      "IsSubclassSchema",
      "CallableSchema",
      "UuidSchema",
      "IncExSeqSerSchema",
      "ListSchema",
      "TupleSchema",
      "SetSchema",
      "FrozenSetSchema",
      "GeneratorSchema",
      "IncExDictSerSchema",
      "DictSchema",
      "NoInfoValidatorFunctionSchema",
      "WithInfoValidatorFunctionSchema",
      "_ValidatorFunctionSchema",
      "BeforeValidatorFunctionSchema",
      "AfterValidatorFunctionSchema",
      "ValidatorFunctionWrapHandler",
      "NoInfoWrapValidatorFunctionSchema",
      "WithInfoWrapValidatorFunctionSchema",
      "WrapValidatorFunctionSchema",
      "PlainValidatorFunctionSchema",
      "WithDefaultSchema",
      "NullableSchema",
      "UnionSchema",
      "TaggedUnionSchema",
      "ChainSchema",
      "LaxOrStrictSchema",
      "JsonOrPythonSchema",
      "TypedDictField",
      "TypedDictSchema",
      "ModelField",
      "ModelFieldsSchema",
      "ModelSchema",
      "DataclassField",
      "DataclassArgsSchema",
      "DataclassSchema",
      "ArgumentsParameter",
      "ArgumentsSchema",
      "ArgumentsV3Parameter",
      "ArgumentsV3Schema",
      "CallSchema",
      "CustomErrorSchema",
      "JsonSchema",
      "UrlSchema",
      "MultiHostUrlSchema",
      "DefinitionsSchema",
      "DefinitionReferenceSchema"
    ],
    "docstring": "This module contains definitions to build schemas which `pydantic_core` can\nvalidate and serialize."
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/pydantic_core/__init__.py",
    "imports": [
      "__future__",
      "_pydantic_core",
      "core_schema",
      "sys",
      "typing",
      "typing_extensions"
    ],
    "functions": [],
    "classes": [
      "ErrorDetails",
      "InitErrorDetails",
      "ErrorTypeInfo",
      "MultiHostHost"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/concurrency.py",
    "imports": [
      "anyio",
      "contextlib",
      "starlette",
      "typing"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/routing.py",
    "imports": [
      "asyncio",
      "contextlib",
      "dataclasses",
      "email",
      "enum",
      "fastapi",
      "inspect",
      "json",
      "pydantic",
      "starlette",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "_prepare_response_content",
      "_merge_lifespan_context",
      "get_request_handler",
      "get_websocket_app",
      "__init__",
      "matches",
      "__init__",
      "get_route_handler",
      "matches",
      "__init__",
      "route",
      "add_api_route",
      "api_route",
      "add_api_websocket_route",
      "websocket",
      "websocket_route",
      "include_router",
      "get",
      "put",
      "post",
      "delete",
      "options",
      "head",
      "patch",
      "trace",
      "on_event",
      "decorator",
      "decorator",
      "decorator",
      "decorator",
      "decorator"
    ],
    "classes": [
      "APIWebSocketRoute",
      "APIRoute",
      "APIRouter"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/templating.py",
    "imports": [
      "starlette"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/exception_handlers.py",
    "imports": [
      "fastapi",
      "starlette"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/requests.py",
    "imports": [
      "starlette"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/logger.py",
    "imports": [
      "logging"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/cli.py",
    "imports": [
      "fastapi_cli"
    ],
    "functions": [
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/utils.py",
    "imports": [
      "dataclasses",
      "fastapi",
      "pydantic",
      "re",
      "routing",
      "typing",
      "typing_extensions",
      "warnings",
      "weakref"
    ],
    "functions": [
      "is_body_allowed_for_status_code",
      "get_path_param_names",
      "create_model_field",
      "create_cloned_field",
      "generate_operation_id_for_path",
      "generate_unique_id",
      "deep_dict_update",
      "get_value_or_default"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/param_functions.py",
    "imports": [
      "fastapi",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "Path",
      "Query",
      "Header",
      "Cookie",
      "Body",
      "Form",
      "File",
      "Depends",
      "Security"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/encoders.py",
    "imports": [
      "_compat",
      "collections",
      "dataclasses",
      "datetime",
      "decimal",
      "enum",
      "fastapi",
      "ipaddress",
      "pathlib",
      "pydantic",
      "re",
      "types",
      "typing",
      "typing_extensions",
      "uuid"
    ],
    "functions": [
      "isoformat",
      "decimal_encoder",
      "generate_encoders_by_class_tuples",
      "jsonable_encoder"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/__main__.py",
    "imports": [
      "fastapi"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/websockets.py",
    "imports": [
      "starlette"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/params.py",
    "imports": [
      "_compat",
      "enum",
      "fastapi",
      "pydantic",
      "typing",
      "typing_extensions",
      "warnings"
    ],
    "functions": [
      "__init__",
      "__repr__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__repr__",
      "__init__",
      "__init__",
      "__init__",
      "__repr__",
      "__init__"
    ],
    "classes": [
      "ParamTypes",
      "Param",
      "Path",
      "Query",
      "Header",
      "Cookie",
      "Body",
      "Form",
      "File",
      "Depends",
      "Security"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/__init__.py",
    "imports": [
      "applications",
      "background",
      "datastructures",
      "exceptions",
      "param_functions",
      "requests",
      "responses",
      "routing",
      "starlette",
      "websockets"
    ],
    "functions": [],
    "classes": [],
    "docstring": "FastAPI framework, high performance, easy to learn, fast to code, ready for production"
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/applications.py",
    "imports": [
      "enum",
      "fastapi",
      "starlette",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "__init__",
      "openapi",
      "setup",
      "add_api_route",
      "api_route",
      "add_api_websocket_route",
      "websocket",
      "include_router",
      "get",
      "put",
      "post",
      "delete",
      "options",
      "head",
      "patch",
      "trace",
      "websocket_route",
      "on_event",
      "middleware",
      "exception_handler",
      "decorator",
      "decorator",
      "decorator",
      "decorator",
      "decorator"
    ],
    "classes": [
      "FastAPI"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/datastructures.py",
    "imports": [
      "fastapi",
      "starlette",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "Default",
      "__get_validators__",
      "validate",
      "_validate",
      "__get_pydantic_json_schema__",
      "__get_pydantic_core_schema__",
      "__init__",
      "__bool__",
      "__eq__",
      "__modify_schema__"
    ],
    "classes": [
      "UploadFile",
      "DefaultPlaceholder"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/_compat.py",
    "imports": [
      "collections",
      "copy",
      "dataclasses",
      "enum",
      "fastapi",
      "functools",
      "pydantic",
      "pydantic_core",
      "starlette",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "_regenerate_error_with_loc",
      "_annotation_is_sequence",
      "field_annotation_is_sequence",
      "value_is_sequence",
      "_annotation_is_complex",
      "field_annotation_is_complex",
      "field_annotation_is_scalar",
      "field_annotation_is_scalar_sequence",
      "is_bytes_or_nonable_bytes_annotation",
      "is_uploadfile_or_nonable_uploadfile_annotation",
      "is_bytes_sequence_annotation",
      "is_uploadfile_sequence_annotation",
      "get_cached_model_fields",
      "get_annotation_from_field_info",
      "_normalize_errors",
      "_model_rebuild",
      "_model_dump",
      "_get_model_config",
      "get_schema_from_model_field",
      "get_compat_model_name_map",
      "get_definitions",
      "is_scalar_field",
      "is_sequence_field",
      "is_scalar_sequence_field",
      "is_bytes_field",
      "is_bytes_sequence_field",
      "copy_field_info",
      "serialize_sequence_value",
      "get_missing_field_error",
      "create_body_model",
      "get_model_fields",
      "with_info_plain_validator_function",
      "get_model_definitions",
      "is_pv1_scalar_field",
      "is_pv1_scalar_sequence_field",
      "_normalize_errors",
      "_model_rebuild",
      "_model_dump",
      "_get_model_config",
      "get_schema_from_model_field",
      "get_compat_model_name_map",
      "get_definitions",
      "is_scalar_field",
      "is_sequence_field",
      "is_scalar_sequence_field",
      "is_bytes_field",
      "is_bytes_sequence_field",
      "copy_field_info",
      "serialize_sequence_value",
      "get_missing_field_error",
      "create_body_model",
      "get_model_fields",
      "alias",
      "required",
      "default",
      "type_",
      "__post_init__",
      "get_default",
      "validate",
      "serialize",
      "__hash__"
    ],
    "classes": [
      "BaseConfig",
      "ErrorWrapper",
      "ModelField",
      "GenerateJsonSchema",
      "PydanticSchemaGenerationError"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/types.py",
    "imports": [
      "enum",
      "pydantic",
      "types",
      "typing"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/exceptions.py",
    "imports": [
      "pydantic",
      "starlette",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "__init__",
      "__init__",
      "__init__",
      "errors",
      "__init__",
      "__init__",
      "__str__"
    ],
    "classes": [
      "HTTPException",
      "WebSocketException",
      "FastAPIError",
      "ValidationException",
      "RequestValidationError",
      "WebSocketRequestValidationError",
      "ResponseValidationError"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/background.py",
    "imports": [
      "starlette",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "add_task"
    ],
    "classes": [
      "BackgroundTasks"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/testclient.py",
    "imports": [
      "starlette"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/responses.py",
    "imports": [
      "orjson",
      "starlette",
      "typing",
      "ujson"
    ],
    "functions": [
      "render",
      "render"
    ],
    "classes": [
      "UJSONResponse",
      "ORJSONResponse"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/staticfiles.py",
    "imports": [
      "starlette"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/uvicorn/importer.py",
    "imports": [
      "importlib",
      "typing"
    ],
    "functions": [
      "import_from_string"
    ],
    "classes": [
      "ImportFromStringError"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/uvicorn/__main__.py",
    "imports": [
      "uvicorn"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/uvicorn/__init__.py",
    "imports": [
      "uvicorn"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/uvicorn/logging.py",
    "imports": [
      "__future__",
      "click",
      "copy",
      "http",
      "logging",
      "sys",
      "typing"
    ],
    "functions": [
      "__init__",
      "color_level_name",
      "should_use_colors",
      "formatMessage",
      "should_use_colors",
      "get_status_code",
      "formatMessage",
      "default",
      "default"
    ],
    "classes": [
      "ColourizedFormatter",
      "DefaultFormatter",
      "AccessFormatter"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/uvicorn/workers.py",
    "imports": [
      "__future__",
      "asyncio",
      "gunicorn",
      "logging",
      "signal",
      "sys",
      "typing",
      "uvicorn",
      "warnings"
    ],
    "functions": [
      "__init__",
      "init_process",
      "init_signals",
      "_install_sigquit_handler",
      "run"
    ],
    "classes": [
      "UvicornWorker",
      "UvicornH11Worker"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/uvicorn/_types.py",
    "imports": [
      "__future__",
      "sys",
      "types",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "__init__"
    ],
    "classes": [
      "ASGIVersions",
      "HTTPScope",
      "WebSocketScope",
      "LifespanScope",
      "HTTPRequestEvent",
      "HTTPResponseDebugEvent",
      "HTTPResponseStartEvent",
      "HTTPResponseBodyEvent",
      "HTTPResponseTrailersEvent",
      "HTTPServerPushEvent",
      "HTTPDisconnectEvent",
      "WebSocketConnectEvent",
      "WebSocketAcceptEvent",
      "_WebSocketReceiveEventBytes",
      "_WebSocketReceiveEventText",
      "_WebSocketSendEventBytes",
      "_WebSocketSendEventText",
      "WebSocketResponseStartEvent",
      "WebSocketResponseBodyEvent",
      "WebSocketDisconnectEvent",
      "WebSocketCloseEvent",
      "LifespanStartupEvent",
      "LifespanShutdownEvent",
      "LifespanStartupCompleteEvent",
      "LifespanStartupFa
```

### python/llamaindex_python_inventory.json

Size: 13252730 bytes

```text
[
  {
    "file": "/opt/llamaindex-bakeoff/prompt_builder.py",
    "imports": [
      "pathlib"
    ],
    "functions": [
      "load",
      "build_prompt"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/people_evidence.py",
    "imports": [
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/people_summary.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/entity_answer.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/intent_classifier.py",
    "imports": [
      "json",
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "clean_entity",
      "classify"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/heading_search.py",
    "imports": [
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/routed_retrieval.py",
    "imports": [
      "llama_index",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/people_graham.py",
    "imports": [
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/filter_test.py",
    "imports": [
      "llama_index",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/app.py",
    "imports": [
      "fastapi",
      "functools",
      "html",
      "json",
      "llama_index",
      "pathlib",
      "subprocess",
      "sys",
      "urllib"
    ],
    "functions": [
      "get_retriever",
      "classify_route",
      "routed_queries",
      "allowed_by_route",
      "object_type",
      "filename_people_matches",
      "page",
      "home",
      "search",
      "view_theme",
      "view",
      "alfred_api"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/validate_retrieval.py",
    "imports": [
      "llama_index",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/ask.py",
    "imports": [
      "json",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/entity_synthesise.py",
    "imports": [
      "pathlib",
      "prompt_builder",
      "subprocess",
      "sys"
    ],
    "functions": [
      "load_doc",
      "executive_reasoning_mode"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/people_summarise.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/entity_summary.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/review_answer.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/entity_evidence_v2.py",
    "imports": [
      "entity_config",
      "pathlib",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/entity_evidence.py",
    "imports": [
      "entity_config",
      "pathlib",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/improve_answer.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/test_index.py",
    "imports": [
      "llama_index"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/alfred.py",
    "imports": [
      "contextlib",
      "json",
      "llama_index",
      "pathlib",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/entity_config.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_synthesise.modewire.20260627-120237.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "executive_reasoning_mode"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/ask.pre-intent.20260627-181815.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/alfred.gate.20260627-190548.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys",
      "tempfile"
    ],
    "functions": [
      "run"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/alfred.pre-json.20260627-221612.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys",
      "tempfile"
    ],
    "functions": [
      "run"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/app.pre-json-alfred.20260627-221612.py",
    "imports": [
      "fastapi",
      "functools",
      "html",
      "llama_index",
      "pathlib",
      "subprocess",
      "urllib"
    ],
    "functions": [
      "get_retriever",
      "classify_route",
      "routed_queries",
      "allowed_by_route",
      "object_type",
      "filename_people_matches",
      "page",
      "home",
      "search",
      "view_theme",
      "view",
      "alfred_api"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_answer.cli.20260627-120653.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_synthesise.pre-governance.20260627-182938.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "executive_reasoning_mode"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/improve_answer.truth.20260627-185943.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/app.pre-alfred-api.20260627-212408.py",
    "imports": [
      "fastapi",
      "functools",
      "html",
      "llama_index",
      "pathlib",
      "subprocess",
      "urllib"
    ],
    "functions": [
      "get_retriever",
      "classify_route",
      "routed_queries",
      "allowed_by_route",
      "object_type",
      "filename_people_matches",
      "page",
      "home",
      "search",
      "view_theme",
      "view"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/review_answer.fix.20260627-185314.py",
    "imports": [
      "json",
      "os",
      "pathlib",
      "requests",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_synthesise.debug.20260627-183128.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "load_doc",
      "executive_reasoning_mode"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/review_answer.pre-openrouter.20260627-184743.py",
    "imports": [
      "json",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/alfred.pre-self-improve.20260627-185615.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "run"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_synthesise.pre-promptbuilder.20260627-183612.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "load_doc",
      "executive_reasoning_mode"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/alfred.pipeline.20260627-185649.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "run"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_synthesise.reasoning.20260627-120155.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_answer.pre-intent.20260627-181815.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_answer.debug.20260627-190216.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_synthesise.cli.20260627-120653.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "executive_reasoning_mode"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/review_answer.pre-openrouter-reuse.20260627-184928.py",
    "imports": [
      "json",
      "os",
      "pathlib",
      "requests",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/baseline-20260627-113531/entity_answer.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/baseline-20260627-113531/routed_retrieval.py",
    "imports": [
      "llama_index",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/baseline-20260627-113531/app.py",
    "imports": [
      "fastapi",
      "functools",
      "html",
      "llama_index",
      "pathlib",
      "subprocess",
      "urllib"
    ],
    "functions": [
      "get_retriever",
      "classify_route",
      "routed_queries",
      "allowed_by_route",
      "object_type",
      "filename_people_matches",
      "page",
      "home",
      "search",
      "view_theme",
      "view"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/baseline-20260627-113531/entity_synthesise.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/baseline-20260627-113531/entity_evidence_v2.py",
    "imports": [
      "entity_config",
      "pathlib",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-evidence-contract-20260627-114554/entity_answer.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-evidence-contract-20260627-114554/entity_synthesise.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-evidence-contract-20260627-114554/entity_evidence_v2.py",
    "imports": [
      "entity_config",
      "pathlib",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-evidence-contract-20260627-114554/entity_config.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-alfred-runtime-20260627-184554/prompt_builder.py",
    "imports": [
      "pathlib"
    ],
    "functions": [
      "load",
      "build_prompt"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-alfred-runtime-20260627-184554/entity_answer.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-alfred-runtime-20260627-184554/intent_classifier.py",
    "imports": [
      "json",
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "clean_entity",
      "classify"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-alfred-runtime-20260627-184554/ask.py",
    "imports": [
      "json",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-alfred-runtime-20260627-184554/entity_synthesise.py",
    "imports": [
      "pathlib",
      "prompt_builder",
      "subprocess",
      "sys"
    ],
    "functions": [
      "load_doc",
      "executive_reasoning_mode"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-alfred-runtime-20260627-184554/review_answer.py",
    "imports": [
      "json",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/isympy.py",
    "imports": [
      "IPython",
      "argparse",
      "os",
      "sympy",
      "sys"
    ],
    "functions": [
      "main"
    ],
    "classes": [],
    "docstring": "Python shell for SymPy.\n\nThis is just a normal Python shell (IPython shell if you have the\nIPython package installed), that executes the following commands for\nthe user:\n\n    >>> from __future__ import division\n    >>> from sympy import *\n    >>> x, y, z, t = symbols('x y z t')\n    >>> k, m, n = symbols('k m n', integer=True)\n    >>> f, g, h = symbols('f g h', cls=Function)\n    >>> init_printing()\n\nSo starting 'isympy' is equivalent to starting Python (or IPython) and\nexecuting the above commands by hand.  It is intended for easy and quick\nexperimentation with SymPy.  isympy is a good way to use SymPy as an\ninteractive calculator. If you have IPython and Matplotlib installed, then\ninteractive plotting is enabled by default.\n\nCOMMAND LINE OPTIONS\n--------------------\n\n-c CONSOLE, --console=CONSOLE\n\n     Use the specified shell (Python or IPython) shell as the console\n     backend instead of the default one (IPython if present, Python\n     otherwise), e.g.:\n\n        $isympy -c python\n\n    CONSOLE must be one of 'ipython' or 'python'\n\n-p PRETTY, --pretty PRETTY\n\n    Setup pretty-printing in SymPy. When pretty-printing is enabled,\n    expressions can be printed with Unicode or ASCII. The default is\n    to use pretty-printing (with Unicode if the terminal supports it).\n    When this option is 'no', expressions will not be pretty-printed\n    and ASCII will be used:\n\n        $isympy -p no\n\n    PRETTY must be one of 'unicode', 'ascii', or 'no'\n\n-t TYPES, --types=TYPES\n\n    Setup the ground types for the polys.  By default, gmpy ground types\n    are used if gmpy2 or gmpy is installed, otherwise it falls back to python\n    ground types, which are a little bit slower.  You can manually\n    choose python ground types even if gmpy is installed (e.g., for\n    testing purposes):\n\n        $isympy -t python\n\n    TYPES must be one of 'gmpy', 'gmpy1' or 'python'\n\n    Note that the ground type gmpy1 is primarily intended for testing; it\n    forces the use of gmpy version 1 even if gmpy2 is available.\n\n    This is the same as setting the environment variable\n    SYMPY_GROUND_TYPES to the given ground type (e.g.,\n    SYMPY_GROUND_TYPES='gmpy')\n\n    The ground types can be determined interactively from the variable\n    sympy.polys.domains.GROUND_TYPES.\n\n-o ORDER, --order ORDER\n\n    Setup the ordering of terms for printing.  The default is lex, which\n    orders terms lexicographically (e.g., x**2 + x + 1). You can choose\n    other orderings, such as rev-lex, which will use reverse\n    lexicographic ordering (e.g., 1 + x + x**2):\n\n        $isympy -o rev-lex\n\n    ORDER must be one of 'lex', 'rev-lex', 'grlex', 'rev-grlex',\n    'grevlex', 'rev-grevlex', 'old', or 'none'.\n\n    Note that for very large expressions, ORDER='none' may speed up\n    printing considerably but the terms will have no canonical order.\n\n-q, --quiet\n\n    Print only Python's and SymPy's versions to stdout at startup.\n\n-d, --doctest\n\n    Use the same format that should be used for doctests.  This is\n    equivalent to -c python -p no.\n\n-C, --no-cache\n\n    Disable the caching mechanism.  Disabling the cache may slow certain\n    operations down considerably.  This is useful for testing the cache,\n    or for benchmarking, as the cache can result in deceptive timings.\n\n    This is equivalent to setting the environment variable\n    SYMPY_USE_CACHE to 'no'.\n\n-a, --auto-symbols (requires at least IPython 0.11)\n\n    Automatically create missing symbols.  Normally, typing a name of a\n    Symbol that has not been instantiated first would raise NameError,\n    but with this option enabled, any undefined name will be\n    automatically created as a Symbol.\n\n    Note that this is intended only for interactive, calculator style\n    usage. In a script that uses SymPy, Symbols should be instantiated\n    at the top, so that it's clear what they are.\n\n    This will not override any names that are already defined, which\n    includes the single character letters represented by the mnemonic\n    QCOSINE (see the \"Gotchas and Pitfalls\" document in the\n    documentation). You can delete existing names by executing \"del\n    name\".  If a name is defined, typing \"'name' in dir()\" will return True.\n\n    The Symbols that are created using this have default assumptions.\n    If you want to place assumptions on symbols, you should create them\n    using symbols() or var().\n\n    Finally, this only works in the top level namespace. So, for\n    example, if you define a function in isympy with an undefined\n    Symbol, it will not work.\n\n    See also the -i and -I options.\n\n-i, --int-to-Integer (requires at least IPython 0.11)\n\n    Automatically wrap int literals with Integer.  This makes it so that\n    things like 1/2 will come out as Rational(1, 2), rather than 0.5.  This\n    works by preprocessing the source and wrapping all int literals with\n    Integer.  Note that this will not change the behavior of int literals\n    assigned to variables, and it also won't change the behavior of functions\n    that return int literals.\n\n    If you want an int, you can wrap the literal in int(), e.g. int(3)/int(2)\n    gives 1.5 (with division imported from __future__).\n\n-I, --interactive (requires at least IPython 0.11)\n\n    This is equivalent to --auto-symbols --int-to-Integer.  Future options\n    designed for ease of interactive use may be added to this.\n\n-D, --debug\n\n    Enable debugging output.  This is the same as setting the\n    environment variable SYMPY_DEBUG to 'True'.  The debug status is set\n    in the variable SYMPY_DEBUG within isympy.\n\n-- IPython options\n\n    Additionally you can pass command line options directly to the IPython\n    interpreter (the standard Python shell is not supported).  However you\n    need to add the '--' separator between two types of options, e.g the\n    startup banner option and the colors option. You need to enter the\n    options as required by the version of IPython that you are using, too:\n\n    in IPython 0.11,\n\n        $isympy -q -- --colors=NoColor\n\n    or older versions of IPython,\n\n        $isympy -q -- -colors NoColor\n\nSee also isympy --help."
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/threadpoolctl.py",
    "imports": [
      "abc",
      "argparse",
      "contextlib",
      "ctypes",
      "functools",
      "importlib",
      "itertools",
      "json",
      "os",
      "pyodide_js",
      "re",
      "sys",
      "textwrap",
      "typing",
      "warnings"
    ],
    "functions": [
      "register",
      "_format_docstring",
      "_realpath",
      "threadpool_info",
      "_main",
      "__init__",
      "info",
      "set_additional_attributes",
      "num_threads",
      "get_num_threads",
      "set_num_threads",
      "get_version",
      "_find_affixes",
      "_get_symbol",
      "_find_affixes",
      "set_additional_attributes",
      "get_num_threads",
      "set_num_threads",
      "get_version",
      "_get_threading_layer",
      "_get_architecture",
      "set_additional_attributes",
      "get_num_threads",
      "set_num_threads",
      "get_version",
      "_get_threading_layer",
      "_get_architecture",
      "loaded_backends",
      "current_backend",
      "info",
      "set_additional_attributes",
      "get_num_threads",
      "set_num_threads",
      "get_version",
      "_get_backend_list",
      "_get_current_backend",
      "switch_backend",
      "set_additional_attributes",
      "get_num_threads",
      "set_num_threads",
      "get_version",
      "_get_threading_layer",
      "get_num_threads",
      "set_num_threads",
      "get_version",
      "decorator",
      "__init__",
      "__enter__",
      "__exit__",
      "wrap",
      "restore_original_limits",
      "get_original_num_threads",
      "_check_params",
      "_set_threadpool_limits",
      "__init__",
      "__enter__",
      "__init__",
      "wrap",
      "__init__",
      "_from_controllers",
      "info",
      "select",
      "_get_params_for_sequential_blas_under_openmp",
      "limit",
      "wrap",
      "__len__",
      "_load_libraries",
      "_find_libraries_with_dl_iterate_phdr",
      "_find_libraries_with_dyld",
      "_find_libraries_with_enum_process_module_ex",
      "_find_libraries_pyodide",
      "_make_controller_from_path",
      "_check_prefix",
      "_warn_if_incompatible_openmp",
      "_get_libc",
      "_get_windll",
      "match_library_callback"
    ],
    "classes": [
      "_dl_phdr_info",
      "LibController",
      "OpenBLASController",
      "BLISController",
      "FlexiBLASController",
      "MKLController",
      "OpenMPController",
      "_ThreadpoolLimiter",
      "_ThreadpoolLimiterDecorator",
      "threadpool_limits",
      "ThreadpoolController"
    ],
    "docstring": "threadpoolctl\n\nThis module provides utilities to introspect native libraries that relies on\nthread pools (notably BLAS and OpenMP implementations) and dynamically set the\nmaximal number of threads they can use."
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/typing_inspect.py",
    "imports": [
      "collections",
      "mypy_extensions",
      "sys",
      "types",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "_gorg",
      "is_generic_type",
      "is_callable_type",
      "is_tuple_type",
      "is_optional_type",
      "is_final_type",
      "is_union_type",
      "is_literal_type",
      "is_typevar",
      "is_classvar",
      "is_new_type",
      "is_forward_ref",
      "get_last_origin",
      "get_origin",
      "get_parameters",
      "get_last_args",
      "_eval_args",
      "get_args",
      "get_bound",
      "get_constraints",
      "get_generic_type",
      "get_generic_bases",
      "typed_dict_keys",
      "get_forward_arg",
      "_replace_arg",
      "_remove_dups_flatten",
      "_subs_tree",
      "_union_subs_tree",
      "_generic_subs_tree",
      "_tuple_subs_tree",
      "_has_type_var",
      "_union_has_type_var",
      "_tuple_has_type_var",
      "_callable_has_type_var",
      "_generic_has_type_var",
      "_get_origin",
      "_get_args"
    ],
    "classes": [],
    "docstring": "Defines experimental API for runtime inspection of types defined\nin the standard \"typing\" module.\n\nExample usage::\n    from typing_inspect import is_generic_type"
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/typing_extensions.py",
    "imports": [
      "_socket",
      "abc",
      "annotationlib",
      "asyncio",
      "builtins",
      "collections",
      "contextlib",
      "enum",
      "functools",
      "inspect",
      "io",
      "keyword",
      "operator",
      "sys",
      "types",
      "typing",
      "warnings"
    ],
    "functions": [
      "IntVar",
      "_get_protocol_attrs",
      "_caller",
      "_set_default",
      "_set_module",
      "_create_concatenate_alias",
      "_concatenate_getitem",
      "_unpack_args",
      "_has_generic_or_protocol_as_origin",
      "_is_unpacked_typevartuple",
      "__repr__",
      "_should_collect_from_parameters",
      "_should_collect_from_parameters",
      "__init__",
      "__getattr__",
      "__mro_entries__",
      "__repr__",
      "__reduce__",
      "__call__",
      "__or__",
      "__ror__",
      "__instancecheck__",
      "__subclasscheck__",
      "__getitem__",
      "__repr__",
      "final",
      "disjoint_base",
      "_flatten_literal_params",
      "_value_and_type_iter",
      "overload",
      "get_overloads",
      "clear_overloads",
      "_is_dunder",
      "_allow_reckless_class_checks",
      "_no_init",
      "_type_check_issubclass_arg_1",
      "_proto_hook",
      "runtime_checkable",
      "_get_typeddict_qualifiers",
      "_create_typeddict",
      "TypedDict",
      "is_typeddict",
      "assert_type",
      "_strip_extras",
      "get_type_hints",
      "_could_be_inserted_optional",
      "_clean_optional",
      "get_origin",
      "get_args",
      "TypeAlias",
      "__instancecheck__",
      "Concatenate",
      "TypeGuard",
      "TypeIs",
      "TypeForm",
      "LiteralString",
      "Self",
      "Never",
      "Required",
      "NotRequired",
      "ReadOnly",
      "_is_unpack",
      "Unpack",
      "_is_unpack",
      "reveal_type",
      "assert_never",
      "dataclass_transform",
      "override",
      "_is_param_expr",
      "_is_param_expr",
      "_check_generic",
      "_check_generic",
      "_collect_type_vars",
      "_collect_parameters",
      "_make_nmtuple",
      "_namedtuple_mro_entries",
      "NamedTuple",
      "get_original_bases",
      "is_protocol",
      "get_protocol_members",
      "get_annotations",
      "_eval_with_owner",
      "evaluate_forward_ref",
      "__init__",
      "__repr__",
      "__getstate__",
      "type_repr",
      "__instancecheck__",
      "__repr__",
      "__new__",
      "__eq__",
      "__hash__",
      "__init__",
      "__getitem__",
      "__init__",
      "__setattr__",
      "__getitem__",
      "__new__",
      "__init__",
      "__subclasscheck__",
      "__instancecheck__",
      "__eq__",
      "__hash__",
      "__init_subclass__",
      "__int__",
      "__float__",
      "__complex__",
      "__bytes__",
      "__index__",
      "__abs__",
      "__round__",
      "read",
      "write",
      "__setattr__",
      "__new__",
      "__repr__",
      "__reduce__",
      "__new__",
      "__repr__",
      "__reduce__",
      "__new__",
      "__subclasscheck__",
      "__call__",
      "__mro_entries__",
      "__new__",
      "__init_subclass__",
      "__copy__",
      "__deepcopy__",
      "__init__",
      "__repr__",
      "__eq__",
      "__init__",
      "__repr__",
      "__eq__",
      "_type_convert",
      "__init__",
      "__repr__",
      "__hash__",
      "__call__",
      "__parameters__",
      "copy_with",
      "__getitem__",
      "__call__",
      "__init__",
      "__typing_unpacked_tuple_args__",
      "__typing_is_unpacked_typevartuple__",
      "__getitem__",
      "decorator",
      "__init__",
      "__call__",
      "__new__",
      "__call__",
      "__init__",
      "__mro_entries__",
      "__repr__",
      "__reduce__",
      "_is_unionable",
      "_is_unionable",
      "__init__",
      "__setattr__",
      "__delattr__",
      "_raise_attribute_error",
      "__repr__",
      "_check_parameters",
      "__getitem__",
      "__reduce__",
      "__init_subclass__",
      "__call__",
      "__init__",
      "__repr__",
      "__hash__",
      "__eq__",
      "__call__",
      "__or__",
      "__ror__",
      "_tvar_prepare_subst",
      "__new__",
      "__init_subclass__",
      "args",
      "kwargs",
      "__init__",
      "__repr__",
      "__hash__",
      "__eq__",
      "__reduce__",
      "__call__",
      "copy_with",
      "__getitem__",
      "__new__",
      "__init_subclass__",
      "__iter__",
      "__init__",
      "__repr__",
      "__hash__",
      "__eq__",
      "__reduce__",
      "__init_subclass__",
      "__or__",
      "__ror__",
      "__getattr__",
      "_check_single_param",
      "__or__",
      "__ror__",
      "__annotate__",
      "_paramspec_prepare_subst",
      "_typevartuple_prepare_subst",
      "__init_subclass__",
      "__new__",
      "__init_subclass__",
      "__init_subclass__",
      "wrapper"
    ],
    "classes": [
      "_Sentinel",
      "_SpecialForm",
      "_ExtensionsSpecialForm",
      "_DefaultMixin",
      "_TypeVarLikeMeta",
      "_EllipsisDummy",
      "Sentinel",
      "_AnyMeta",
      "Any",
      "_LiteralGenericAlias",
      "_LiteralForm",
      "_SpecialGenericAlias",
      "_ProtocolMeta",
      "Protocol",
      "SupportsInt",
      "SupportsFloat",
      "SupportsComplex",
      "SupportsBytes",
      "SupportsIndex",
      "SupportsAbs",
      "SupportsRound",
      "Reader",
      "Writer",
      "SingletonMeta",
      "NoDefaultType",
      "NoExtraItemsType",
      "_TypedDictMeta",
      "_TypedDictSpecialForm",
      "TypeVar",
      "_Immutable",
      "ParamSpecArgs",
      "ParamSpecKwargs",
      "_ConcatenateGenericAlias",
      "_TypeFormForm",
      "_UnpackSpecialForm",
      "_UnpackAlias",
      "deprecated",
      "_NamedTupleMeta",
      "Buffer",
      "NewType",
      "TypeAliasType",
      "Doc",
      "Format",
      "ParamSpec",
      "ParamSpec",
      "_ConcatenateGenericAlias",
      "TypeVarTuple",
      "TypeVarTuple",
      "_TypeAliasGenericAlias",
      "Dummy"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/mypy_extensions.py",
    "imports": [
      "sys",
      "typing",
      "warnings"
    ],
    "functions": [
      "_check_fails",
      "_dict_new",
      "_typeddict_new",
      "Arg",
      "DefaultArg",
      "NamedArg",
      "DefaultNamedArg",
      "VarArg",
      "KwArg",
      "trait",
      "mypyc_attr",
      "_warn_deprecation",
      "__getattr__",
      "__new__",
      "__init__",
      "__getitem__",
      "__getitem__",
      "__instancecheck__",
      "__new__",
      "__new__",
      "__new__",
      "__new__"
    ],
    "classes": [
      "_TypedDictMeta",
      "_DEPRECATED_NoReturn",
      "_FlexibleAliasClsApplied",
      "_FlexibleAliasCls",
      "_NativeIntMeta",
      "i64",
      "i32",
      "i16",
      "u8"
    ],
    "docstring": "Defines experimental extensions to the standard \"typing\" module that are\nsupported by the mypy typechecker.\n\nExample usage:\n    from mypy_extensions import TypedDict"
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/nest_asyncio.py",
    "imports": [
      "asyncio",
      "contextlib",
      "heapq",
      "os",
      "sys",
      "threading",
      "tornado"
    ],
    "functions": [
      "apply",
      "_patch_asyncio",
      "_patch_policy",
      "_patch_loop",
      "_patch_tornado",
      "run",
      "_get_event_loop",
      "get_event_loop",
      "run_forever",
      "run_until_complete",
      "_run_once",
      "manage_run",
      "manage_asyncgens",
      "_check_running"
    ],
    "classes": [],
    "docstring": "Patch asyncio to allow nested event loops."
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/concurrency.py",
    "imports": [
      "__future__",
      "anyio",
      "collections",
      "functools",
      "starlette",
      "typing",
      "warnings"
    ],
    "functions": [
      "_next"
    ],
    "classes": [
      "_StopIteration"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/routing.py",
    "imports": [
      "__future__",
      "collections",
      "contextlib",
      "enum",
      "functools",
      "inspect",
      "re",
      "starlette",
      "traceback",
      "types",
      "typing",
      "warnings"
    ],
    "functions": [
      "request_response",
      "websocket_session",
      "get_name",
      "replace_params",
      "compile_path",
      "_wrap_gen_lifespan_context",
      "__init__",
      "matches",
      "url_path_for",
      "__init__",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "routes",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "routes",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "wrapper",
      "__init__",
      "__call__",
      "__init__",
      "url_path_for",
      "__eq__",
      "mount",
      "host",
      "add_route",
      "add_websocket_route"
    ],
    "classes": [
      "NoMatchFound",
      "Match",
      "BaseRoute",
      "Route",
      "WebSocketRoute",
      "Mount",
      "Host",
      "_AsyncLiftContextManager",
      "_DefaultLifespan",
      "Router"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/templating.py",
    "imports": [
      "__future__",
      "collections",
      "jinja2",
      "os",
      "starlette",
      "typing"
    ],
    "functions": [
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "_setup_env_defaults",
      "get_template",
      "TemplateResponse",
      "url_for"
    ],
    "classes": [
      "_TemplateResponse",
      "Jinja2Templates"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/requests.py",
    "imports": [
      "__future__",
      "anyio",
      "collections",
      "http",
      "json",
      "multipart",
      "python_multipart",
      "starlette",
      "sys",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "cookie_parser",
      "__init__",
      "__getitem__",
      "__iter__",
      "__len__",
      "app",
      "url",
      "base_url",
      "headers",
      "query_params",
      "path_params",
      "cookies",
      "client",
      "session",
      "auth",
      "user",
      "state",
      "url_for",
      "__init__",
      "method",
      "receive",
      "form"
    ],
    "classes": [
      "ClientDisconnect",
      "HTTPConnection",
      "Request"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/schemas.py",
    "imports": [
      "__future__",
      "collections",
      "inspect",
      "re",
      "starlette",
      "typing",
      "yaml"
    ],
    "functions": [
      "render",
      "get_schema",
      "get_endpoints",
      "_remove_converter",
      "parse_docstring",
      "OpenAPIResponse",
      "__init__",
      "get_schema"
    ],
    "classes": [
      "OpenAPIResponse",
      "EndpointInfo",
      "BaseSchemaGenerator",
      "SchemaGenerator"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/_utils.py",
    "imports": [
      "__future__",
      "anyio",
      "asyncio",
      "collections",
      "contextlib",
      "exceptiongroup",
      "functools",
      "inspect",
      "starlette",
      "sys",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "is_async_callable",
      "is_async_callable",
      "is_async_callable",
      "get_route_path",
      "__init__",
      "__await__"
    ],
    "classes": [
      "AwaitableOrContextManager",
      "SupportsAsyncClose",
      "AwaitableOrContextManagerWrapper",
      "BaseExceptionGroup"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/status.py",
    "imports": [
      "__future__",
      "starlette",
      "warnings"
    ],
    "functions": [
      "__getattr__",
      "__dir__"
    ],
    "classes": [],
    "docstring": "HTTP codes\nSee HTTP Status Code Registry:\nhttps://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml\n\nAnd RFC 9110 - https://www.rfc-editor.org/rfc/rfc9110"
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/websockets.py",
    "imports": [
      "__future__",
      "collections",
      "enum",
      "json",
      "starlette",
      "typing"
    ],
    "functions": [
      "__init__",
      "__init__",
      "_raise_on_disconnect",
      "__init__"
    ],
    "classes": [
      "WebSocketState",
      "WebSocketDisconnect",
      "WebSocket",
      "WebSocketClose"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/__init__.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/applications.py",
    "imports": [
      "__future__",
      "collections",
      "starlette",
      "typing"
    ],
    "functions": [
      "__init__",
      "build_middleware_stack",
      "routes",
      "url_path_for",
      "mount",
      "host",
      "add_middleware",
      "add_exception_handler",
      "add_route"
    ],
    "classes": [
      "Starlette"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/authentication.py",
    "imports": [
      "__future__",
      "collections",
      "functools",
      "inspect",
      "starlette",
      "typing",
      "urllib"
    ],
    "functions": [
      "has_required_scope",
      "requires",
      "decorator",
      "__init__",
      "is_authenticated",
      "display_name",
      "identity",
      "__init__",
      "is_authenticated",
      "display_name",
      "is_authenticated",
      "display_name",
      "sync_wrapper"
    ],
    "classes": [
      "AuthenticationError",
      "AuthenticationBackend",
      "AuthCredentials",
      "BaseUser",
      "SimpleUser",
      "UnauthenticatedUser"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py",
    "imports": [
      "__future__",
      "starlette",
      "typing"
    ],
    "functions": [
      "_lookup_exception_handler",
      "wrap_app_handling_exceptions"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/datastructures.py",
    "imports": [
      "__future__",
      "collections",
      "re",
      "shlex",
      "starlette",
      "typing",
      "urllib"
    ],
    "functions": [
      "__init__",
      "components",
      "scheme",
      "netloc",
      "path",
      "query",
      "fragment",
      "username",
      "password",
      "hostname",
      "port",
      "is_secure",
      "replace",
      "include_query_params",
      "replace_query_params",
      "remove_query_params",
      "__eq__",
      "__str__",
      "__repr__",
      "__new__",
      "__init__",
      "make_absolute_url",
      "__init__",
      "__repr__",
      "__str__",
      "__bool__",
      "__init__",
      "__len__",
      "__getitem__",
      "__iter__",
      "__repr__",
      "__str__",
      "__init__",
      "getlist",
      "keys",
      "values",
      "items",
      "multi_items",
      "__getitem__",
      "__contains__",
      "__iter__",
      "__len__",
      "__eq__",
      "__repr__",
      "__setitem__",
      "__delitem__",
      "pop",
      "popitem",
      "poplist",
      "clear",
      "setdefault",
      "setlist",
      "append",
      "update",
      "__init__",
      "__str__",
      "__repr__",
      "__init__",
      "content_type",
      "_in_memory",
      "_will_roll",
      "__repr__",
      "__init__",
      "__init__",
      "raw",
      "keys",
      "values",
      "items",
      "getlist",
      "mutablecopy",
      "__getitem__",
      "__contains__",
      "__iter__",
      "__len__",
      "__eq__",
      "__repr__",
      "__setitem__",
      "__delitem__",
      "__ior__",
      "__or__",
      "raw",
      "setdefault",
      "update",
      "append",
      "add_vary_header",
      "__init__",
      "__setattr__",
      "__getattr__",
      "__delattr__",
      "__getitem__",
      "__setitem__",
      "__delitem__",
      "__iter__",
      "__len__"
    ],
    "classes": [
      "Address",
      "URL",
      "URLPath",
      "Secret",
      "CommaSeparatedStrings",
      "ImmutableMultiDict",
      "MultiDict",
      "QueryParams",
      "UploadFile",
      "FormData",
      "Headers",
      "MutableHeaders",
      "State"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/types.py",
    "imports": [
      "collections",
      "contextlib",
      "starlette",
      "typing"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/exceptions.py",
    "imports": [
      "__future__",
      "collections",
      "http"
    ],
    "functions": [
      "__init__",
      "__str__",
      "__repr__",
      "__init__",
      "__str__",
      "__repr__"
    ],
    "classes": [
      "HTTPException",
      "WebSocketException",
      "StarletteDeprecationWarning"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/formparsers.py",
    "imports": [
      "__future__",
      "collections",
      "dataclasses",
      "enum",
      "multipart",
      "python_multipart",
      "starlette",
      "tempfile",
      "typing",
      "urllib"
    ],
    "functions": [
      "_user_safe_decode",
      "__init__",
      "__init__",
      "on_field_start",
      "on_field_name",
      "on_field_data",
      "on_field_end",
      "on_end",
      "__init__",
      "on_part_begin",
      "on_part_data",
      "on_part_end",
      "on_header_field",
      "on_header_value",
      "on_header_end",
      "on_headers_finished",
      "on_end"
    ],
    "classes": [
      "FormMessage",
      "MultipartPart",
      "MultiPartException",
      "FormParser",
      "MultiPartParser"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/config.py",
    "imports": [
      "__future__",
      "collections",
      "os",
      "pathlib",
      "typing",
      "warnings"
    ],
    "functions": [
      "__init__",
      "__getitem__",
      "__setitem__",
      "__delitem__",
      "__iter__",
      "__len__",
      "__init__",
      "__call__",
      "__call__",
      "__call__",
      "__call__",
      "__call__",
      "__call__",
      "get",
      "_read_file",
      "_perform_cast"
    ],
    "classes": [
      "undefined",
      "EnvironError",
      "Environ",
      "Config"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/background.py",
    "imports": [
      "__future__",
      "collections",
      "starlette",
      "typing"
    ],
    "functions": [
      "__init__",
      "__init__",
      "add_task"
    ],
    "classes": [
      "BackgroundTask",
      "BackgroundTasks"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/endpoints.py",
    "imports": [
      "__future__",
      "collections",
      "json",
      "starlette",
      "typing"
    ],
    "functions": [
      "__init__",
      "__await__",
      "__init__",
      "__await__"
    ],
    "classes": [
      "HTTPEndpoint",
      "WebSocketEndpoint"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/testclient.py",
    "imports": [
      "__future__",
      "anyio",
      "collections",
      "concurrent",
      "contextlib",
      "httpx",
      "httpx2",
      "inspect",
      "io",
      "json",
      "math",
      "starlette",
      "sys",
      "types",
      "typing",
      "typing_extensions",
      "urllib",
      "warnings"
    ],
    "functions": [
      "_is_asgi3",
      "__init__",
      "__init__",
      "__init__",
      "__enter__",
      "__exit__",
      "_raise_on_close",
      "send",
      "send_text",
      "send_bytes",
      "send_json",
      "close",
      "receive",
      "receive_text",
      "receive_bytes",
      "receive_json",
      "__init__",
      "handle_request",
      "__init__",
      "_portal_factory",
      "request",
      "get",
      "options",
      "head",
      "post",
      "put",
      "patch",
      "delete",
      "websocket_connect",
      "__enter__",
      "__exit__",
      "reset_portal",
      "wait_shutdown"
    ],
    "classes": [
      "_WrapASGI2",
      "_AsyncBackend",
      "_Upgrade",
      "WebSocketDenialResponse",
      "WebSocketTestSession",
      "_TestClientTransport",
      "TestClient"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/responses.py",
    "imports": [
      "__future__",
      "anyio",
      "collections",
      "datetime",
      "email",
      "functools",
      "hashlib",
      "http",
      "json",
      "mimetypes",
      "os",
      "secrets",
      "starlette",
      "stat",
      "sys",
      "typing",
      "urllib"
    ],
    "functions": [
      "__init__",
      "render",
      "init_headers",
      "headers",
      "set_cookie",
      "delete_cookie",
      "_wrap_websocket_denial_send",
      "__init__",
      "render",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "set_stat_headers",
      "_should_use_range",
      "_parse_range_header",
      "_parse_ranges",
      "generate_multipart"
    ],
    "classes": [
      "Response",
      "HTMLResponse",
      "PlainTextResponse",
      "JSONResponse",
      "RedirectResponse",
      "StreamingResponse",
      "MalformedRangeHeader",
      "RangeNotSatisfiable",
      "FileResponse"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/convertors.py",
    "imports": [
      "__future__",
      "math",
      "typing",
      "uuid"
    ],
    "functions": [
      "register_url_convertor",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string"
    ],
    "classes": [
      "Convertor",
      "StringConvertor",
      "PathConvertor",
      "IntegerConvertor",
      "FloatConvertor",
      "UUIDConvertor"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/staticfiles.py",
    "imports": [
      "__future__",
      "anyio",
      "email",
      "errno",
      "importlib",
      "os",
      "starlette",
      "stat",
      "typing"
    ],
    "functions": [
      "__init__",
      "__init__",
      "get_directories",
      "get_path",
      "lookup_path",
      "file_response",
      "is_not_modified"
    ],
    "classes": [
      "NotModifiedResponse",
      "StaticFiles"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/annotated_types/__init__.py",
    "imports": [
      "dataclasses",
      "datetime",
      "math",
      "sys",
      "types",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "__gt__",
      "__ge__",
      "__lt__",
      "__le__",
      "__mod__",
      "__div__",
      "__is_annotated_types_grouped_metadata__",
      "__iter__",
      "__iter__",
      "__iter__",
      "__repr__",
      "__call__",
      "__init_subclass__",
      "__iter__",
      "doc"
    ],
    "classes": [
      "SupportsGt",
      "SupportsGe",
      "SupportsLt",
      "SupportsLe",
      "SupportsMod",
      "SupportsDiv",
      "BaseMetadata",
      "Gt",
      "Ge",
      "Lt",
      "Le",
      "GroupedMetadata",
      "Interval",
      "MultipleOf",
      "MinLen",
      "MaxLen",
      "Len",
      "Timezone",
      "Unit",
      "Predicate",
      "Not",
      "DocInfo"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/annotated_types/test_cases.py",
    "imports": [
      "annotated_types",
      "datetime",
      "decimal",
      "math",
      "sys",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "cases",
      "__iter__"
    ],
    "classes": [
      "Case",
      "MyCustomGroupedMetadata"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/triton/_utils.py",
    "imports": [
      "__future__",
      "functools",
      "language",
      "typing"
    ],
    "functions": [
      "get_iterable_path",
      "set_iterable_path",
      "is_iterable",
      "apply_with_path",
      "find_paths_if",
      "is_power_of_two",
      "validate_block_shape",
      "canonicalize_dtype",
      "canonicalize_ptr_dtype",
      "get_primitive_bitwidth",
      "is_namedtuple",
      "_tuple_create",
      "_impl"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/triton/_filecheck.py",
    "imports": [
      "functools",
      "inspect",
      "os",
      "subprocess",
      "tempfile",
      "triton"
    ],
    "functions": [
      "run_filecheck",
      "run_parser",
      "run_filecheck_test",
      "filecheck_test",
      "__init__",
      "__str__",
      "test_fn"
    ],
    "classes": [
      "MatchError"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/triton/__init__.py",
    "imports": [
      "compiler",
      "errors",
      "runtime"
    ],
    "functions": [
      "cdiv",
      "next_power_of_2"
    ],
    "classes": [],
    "docstring": "isort:skip_file"
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/triton/testing.py",
    "imports": [
      "contextlib",
      "functools",
      "math",
      "matplotlib",
      "numpy",
      "os",
      "pandas",
      "psutil",
      "runtime",
      "statistics",
      "subprocess",
      "sys",
      "torch",
      "typing"
    ],
    "functions": [
      "nvsmi",
      "_quantile",
      "_summarize_statistics",
      "do_bench_cudagraph",
      "do_bench",
      "assert_close",
      "perf_report",
      "get_dram_gbps",
      "get_max_tensorcore_tflops",
      "cuda_memcheck",
      "set_gpu_clock",
      "get_max_simd_tflops",
      "get_quantile",
      "__init__",
      "__init__",
      "_run",
      "run",
      "decorator",
      "wrapper"
    ],
    "classes": [
      "Benchmark",
      "Mark"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/triton/errors.py",
    "imports": [],
    "functions": [],
    "classes": [
      "TritonError"
    ],
    "docstring": "Base class for all errors raised by Triton"
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/triton/knobs.py",
    "imports": [
      "__future__",
      "compiler",
      "contextlib",
      "dataclasses",
      "functools",
      "importlib",
      "os",
      "pathlib",
      "re",
      "runtime",
      "subprocess",
      "sysconfig",
      "triton",
      "typing"
    ],
    "functions": [
      "setenv",
      "toenv",
      "refresh_knobs",
      "__init__",
      "__set_name__",
      "__get__",
      "get",
      "__set__",
      "__delete__",
      "transform",
      "__init__",
      "get",
      "__init__",
      "get",
      "__init__",
      "get",
      "__init__",
      "get",
      "__init__",
      "get",
      "from_path",
      "__init__",
      "get",
      "transform",
      "get",
      "get",
      "total_lowering",
      "total",
      "__call__",
      "knob_descriptors",
      "knobs",
      "copy",
      "reset",
      "scope",
      "__call__",
      "backend_dirs",
      "get_triton_dir",
      "__call__",
      "__call__",
      "__init__",
      "add",
      "remove",
      "__call__",
      "__call__",
      "__call__"
    ],
    "classes": [
      "Env",
      "env_base",
      "env_str",
      "env_str_callable_default",
      "env_bool",
      "env_int",
      "env_class",
      "NvidiaTool",
      "env_nvidia_tool",
      "env_opt_str",
      "env_opt_bool",
      "CompileTimes",
      "CompilationListener",
      "base_knobs",
      "BuildImpl",
      "build_knobs",
      "redis_knobs",
      "cache_knobs",
      "compilation_knobs",
      "autotuning_knobs",
      "LaunchHook",
      "InitHandleHook",
      "HookChain",
      "JITHookCompileInfo",
      "JITHook",
      "PipelineStagesHook",
      "runtime_knobs",
      "language_knobs",
      "nvidia_knobs",
      "amd_knobs",
      "proton_knobs"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/triton/_internal_testing.py",
    "imports": [
      "numpy",
      "os",
      "pytest",
      "re",
      "torch",
      "triton",
      "typing"
    ],
    "functions": [
      "is_interpreter",
      "get_current_target",
      "is_cuda",
      "is_ampere_or_newer",
      "is_blackwell",
      "is_blackwell_ultra",
      "is_hopper_or_newer",
      "is_hopper",
      "is_sm12x",
      "is_hip",
      "is_hip_cdna2",
      "is_hip_cdna3",
      "is_hip_cdna4",
      "is_hip_rdna3",
      "is_hip_rdna4",
      "is_hip_gfx1250",
      "is_hip_cdna",
      "is_hip_rdna",
      "get_hip_lds_size",
      "is_xpu",
      "get_arch",
      "numpy_random",
      "to_triton",
      "str_to_triton_dtype",
      "torch_dtype_name",
      "to_numpy",
      "supports_tma",
      "supports_ws",
      "tma_skip_msg",
      "default_alloc_fn",
      "unwrap_tensor",
      "_fresh_knobs_impl",
      "fresh_function",
      "reset_function"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/markup.py",
    "imports": [
      "_emoji_replace",
      "ast",
      "emoji",
      "errors",
      "operator",
      "re",
      "rich",
      "style",
      "text",
      "typing"
    ],
    "functions": [
      "escape",
      "_parse",
      "render",
      "__str__",
      "markup",
      "escape_backslashes",
      "pop_style"
    ],
    "classes": [
      "Tag"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/tree.py",
    "imports": [
      "_loop",
      "console",
      "jupyter",
      "measure",
      "rich",
      "segment",
      "style",
      "styled",
      "typing"
    ],
    "functions": [
      "__init__",
      "add",
      "__rich_console__",
      "__rich_measure__",
      "make_guide"
    ],
    "classes": [
      "Tree"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/box.py",
    "imports": [
      "_loop",
      "console",
      "rich",
      "table",
      "text",
      "typing"
    ],
    "functions": [
      "__init__",
      "__repr__",
      "__str__",
      "substitute",
      "get_plain_headed_box",
      "get_top",
      "get_row",
      "get_bottom"
    ],
    "classes": [
      "Box"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/color.py",
    "imports": [
      "_palettes",
      "color_triplet",
      "colorsys",
      "console",
      "enum",
      "functools",
      "re",
      "repr",
      "style",
      "sys",
      "table",
      "terminal_theme",
      "text",
      "typing"
    ],
    "functions": [
      "parse_rgb_hex",
      "blend_rgb",
      "__repr__",
      "__str__",
      "__repr__",
      "__rich__",
      "__rich_repr__",
      "system",
      "is_system_defined",
      "is_default",
      "get_truecolor",
      "from_ansi",
      "from_triplet",
      "from_rgb",
      "default",
      "parse",
      "get_ansi_codes",
      "downgrade"
    ],
    "classes": [
      "ColorSystem",
      "ColorType",
      "ColorParseError",
      "Color"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/json.py",
    "imports": [
      "argparse",
      "highlighter",
      "json",
      "pathlib",
      "rich",
      "sys",
      "text",
      "typing"
    ],
    "functions": [
      "__init__",
      "from_data",
      "__rich__"
    ],
    "classes": [
      "JSON"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/syntax.py",
    "imports": [
      "__future__",
      "_loop",
      "abc",
      "argparse",
      "cells",
      "color",
      "console",
      "jupyter",
      "measure",
      "os",
      "pathlib",
      "pygments",
      "re",
      "rich",
      "segment",
      "style",
      "sys",
      "text",
      "textwrap",
      "typing"
    ],
    "functions": [
      "_get_code_index_for_syntax_position",
      "get_style_for_token",
      "get_background_style",
      "__init__",
      "get_style_for_token",
      "get_background_style",
      "__init__",
      "get_style_for_token",
      "get_background_style",
      "__get__",
      "__set__",
      "get_theme",
      "__init__",
      "from_path",
      "guess_lexer",
      "_get_base_style",
      "_get_token_color",
      "lexer",
      "default_lexer",
      "highlight",
      "stylize_range",
      "_get_line_numbers_color",
      "_numbers_column_width",
      "_get_number_styles",
      "__rich_measure__",
      "__rich_console__",
      "_get_syntax",
      "_apply_stylized_ranges",
      "_process_code",
      "line_tokenize",
      "tokens_to_spans"
    ],
    "classes": [
      "SyntaxTheme",
      "PygmentsSyntaxTheme",
      "ANSISyntaxTheme",
      "_SyntaxHighlightRange",
      "PaddingProperty",
      "Syntax"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/_palettes.py",
    "imports": [
      "palette"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/control.py",
    "imports": [
      "console",
      "rich",
      "segment",
      "time",
      "typing"
    ],
    "functions": [
      "strip_control_codes",
      "escape_control_codes",
      "__init__",
      "bell",
      "home",
      "move",
      "move_to_column",
      "move_to",
      "clear",
      "show_cursor",
      "alt_screen",
      "title",
      "__str__",
      "__rich_console__",
      "get_codes"
    ],
    "classes": [
      "Control"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/_windows_renderer.py",
    "imports": [
      "rich",
      "typing"
    ],
    "functions": [
      "legacy_windows_render"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/markdown.py",
    "imports": [
      "__future__",
      "_loop",
      "_stack",
      "argparse",
      "console",
      "containers",
      "dataclasses",
      "io",
      "jupyter",
      "markdown_it",
      "pydoc",
      "rich",
      "rule",
      "segment",
      "style",
      "syntax",
      "sys",
      "text",
      "typing"
    ],
    "functions": [
      "create",
      "on_enter",
      "on_text",
      "on_leave",
      "on_child_close",
      "__rich_console__",
      "on_enter",
      "on_text",
      "on_leave",
      "create",
      "__init__",
      "__rich_console__",
      "create",
      "on_enter",
      "__init__",
      "__rich_console__",
      "create",
      "__init__",
      "__rich_console__",
      "__init__",
      "on_child_close",
      "__rich_console__",
      "__rich_console__",
      "__init__",
      "on_child_close",
      "__rich_console__",
      "__init__",
      "on_child_close",
      "__init__",
      "on_child_close",
      "__init__",
      "on_child_close",
      "create",
      "__init__",
      "on_text",
      "create",
      "__init__",
      "on_child_close",
      "__rich_console__",
      "__init__",
      "on_child_close",
      "render_bullet",
      "render_number",
      "create",
      "__init__",
      "create",
      "__init__",
      "on_enter",
      "__rich_console__",
      "__init__",
      "current_style",
      "on_text",
      "enter_style",
      "leave_style",
      "__init__",
      "_flatten_tokens",
      "__rich_console__"
    ],
    "classes": [
      "MarkdownElement",
      "UnknownElement",
      "TextElement",
      "Paragraph",
      "HeadingFormat",
      "Heading",
      "CodeBlock",
      "BlockQuote",
      "HorizontalRule",
      "TableElement",
      "TableHeaderElement",
      "TableBodyElement",
      "TableRowElement",
      "TableDataElement",
      "ListElement",
      "ListItem",
      "Link",
      "ImageItem",
      "MarkdownContext",
      "Markdown"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/spinner.py",
    "imports": [
      "_spinners",
      "console",
      "live",
      "measure",
      "style",
      "table",
      "text",
      "time",
      "typing"
    ],
    "functions": [
      "__init__",
      "__rich_console__",
      "__rich_measure__",
      "render",
      "update"
    ],
    "classes": [
      "Spinner"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/default_styles.py",
    "imports": [
      "argparse",
      "io",
      "rich",
      "style",
      "typing"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/columns.py",
    "imports": [
      "align",
      "collections",
      "console",
      "constrain",
      "itertools",
      "jupyter",
      "measure",
      "operator",
      "os",
      "padding",
      "table",
      "text",
      "typing"
    ],
    "functions": [
      "__init__",
      "add_renderable",
      "__rich_console__",
      "iter_renderables"
    ],
    "classes": [
      "Columns"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/jupyter.py",
    "imports": [
      "IPython",
      "rich",
      "segment",
      "terminal_theme",
      "typing"
    ],
    "functions": [
      "_render_segments",
      "display",
      "print",
      "__init__",
      "_repr_mimebundle_",
      "_repr_mimebundle_",
      "escape"
    ],
    "classes": [
      "JupyterRenderable",
      "JupyterMixin"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/styled.py",
    "imports": [
      "console",
      "measure",
      "rich",
      "segment",
      "style",
      "typing"
    ],
    "functions": [
      "__init__",
      "__rich_console__",
      "__rich_measure__"
    ],
    "classes": [
      "Styled"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/_export_format.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/diagnose.py",
    "imports": [
      "os",
      "platform",
      "rich"
    ],
    "functions": [
      "report"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/_ratio.py",
    "imports": [
      "dataclasses",
      "fractions",
      "math",
      "typing"
    ],
    "functions": [
      "ratio_resolve",
      "ratio_reduce",
      "ratio_distribute"
    ],
    "classes": [
      "Edge",
      "E"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/rule.py",
    "imports": [
      "align",
      "cells",
      "console",
      "jupyter",
      "measure",
      "rich",
      "style",
      "sys",
      "text",
      "typing"
    ],
    "functions": [
      "__init__",
      "__repr__",
      "__rich_console__",
      "_rule_line",
      "__rich_measure__"
    ],
    "classes": [
      "Rule"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/padding.py",
    "imports": [
      "console",
      "jupyter",
      "measure",
      "rich",
      "segment",
      "style",
      "typing"
    ],
    "functions": [
      "__init__",
      "indent",
      "unpack",
      "__repr__",
      "__rich_console__",
      "__rich_measure__"
    ],
    "classes": [
      "Padding"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/cells.py",
    "imports": [
      "__future__",
      "functools",
      "operator",
      "rich",
      "typing"
    ],
    "functions": [
      "get_character_cell_size",
      "cached_cell_len",
      "cell_len",
      "_cell_len",
      "split_graphemes",
      "_split_text",
      "split_text",
      "set_cell_size",
      "chop_cells"
    ],
    "classes": [
      "CellTable"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/themes.py",
    "imports": [
      "default_styles",
      "theme"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/_timer.py",
    "imports": [
      "contextlib",
      "time",
      "typing"
    ],
    "functions": [
      "timer"
    ],
    "classes": [],
    "docstring": "Timer context manager, only used in debug."
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/screen.py",
    "imports": [
      "_loop",
      "console",
      "rich",
      "segment",
      "style",
      "typing"
    ],
    "functions": [
      "__init__",
      "__rich_console__"
    ],
    "classes": [
      "Screen"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/_emoji_codes.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/status.py",
    "imports": [
      "console",
      "jupyter",
      "live",
      "spinner",
      "style",
      "time",
      "types",
      "typing"
    ],
    "functions": [
      "__init__",
      "renderable",
      "console",
      "update",
      "start",
      "stop",
      "__rich__",
      "__enter__",
      "__exit__"
    ],
    "classes": [
      "Status"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/_win32_console.py",
    "imports": [
      "ctypes",
      "rich",
      "sys",
      "time",
      "typing"
    ],
    "functions": [
      "GetStdHandle",
      "GetConsoleMode",
      "FillConsoleOutputCharacter",
      "FillConsoleOutputAttribute",
      "SetConsoleTextAttribute",
      "GetConsoleScreenBufferInfo",
      "SetConsoleCursorPosition",
      "GetConsoleCursorInfo",
      "SetConsoleCursorInfo",
      "SetConsoleTitle",
      "from_param",
      "__init__",
      "cursor_position",
      "screen_size",
      "write_text",
      "write_styled",
      "move_cursor_to",
      "erase_line",
      "erase_end_of_line",
      "erase_start_of_line",
      "move_cursor_up",
      "move_cursor_down",
      "move_cursor_forward",
      "move_cursor_to_column",
      "move_cursor_backward",
      "hide_cursor",
      "show_cursor",
      "set_title",
      "_get_cursor_size"
    ],
    "classes": [
      "Le
```

---

# Build and Recovery Guide

Generated: 2026-06-30T21:41:58.616631


## Restore Order

1. Provision the VPS operating system.
2. Install Python, Docker, systemd-compatible services and cloudflared.
3. Restore `/opt/second-brain`.
4. Restore `/opt/llamaindex-bakeoff`.
5. Restore `/opt/alfred-v2`.
6. Restore `/docker/obsidian-vault`.
7. Restore `/etc/cloudflared`.
8. Restore systemd service files and overrides.
9. Restore environment files without exposing secrets.
10. Start Cloudflare.
11. Start LlamaIndex API.
12. Start Telegram.
13. Validate ChatGPT Action.
14. Validate Telegram.
15. Validate Obsidian vault freshness.

## Validation Tests

```bash
curl -I https://v2.alfreddoheny.cloud
curl -s http://127.0.0.1:8788/docs | head
/opt/second-brain/scripts/alfred_router.sh "tell me about the barclays meeting tomorrow"
systemctl status hermes-telegram.service --no-pager -l
```

## Expected Functional Questions

- Prepare me for tomorrow's Barclays meeting.
- Tell me about the Barclays meeting tomorrow.
- Who is Graham Dawe?
- Find the test sync note containing 641923.

## Recovery Rule

During recovery, do not redesign. Restore the smallest broken component that returns the system to intended behaviour.
