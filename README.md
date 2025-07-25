# Mininet L3 Router Implementation


A complete demonstration of Layer 3 routing in Mininet using a Linux host as router, with POX controller support.

## Features

- ✅ Custom topology with 4 hosts and 3 switches
- 🖧 Layer 3 routing between subnets
- 🐧 Linux-based router implementation
- 📊 Included Wireshark captures for analysis
- 🎛️ POX controller integration
- 🧪 Automated connectivity tests

## Prerequisites

- Mininet 2.3.0+
- Python 3.6+
- Wireshark (for capture analysis)
- POX controller (optional)

## Installation de POX

Cloner le dépôt officiel :
```bash
git clone https://github.com/noxrepo/pox
```

## Quick Start

```bash
# Clone repository
git clone https://github.com/your-username/mininet-pox-demo.git
cd mininet-pox-demo
```

### Run topology (without POX)
```bash
sudo python3 topo_pox.py
```

### Run POX controller (in separate terminal)
```bash
sudo python2 pox/pox.py forwarding.l2_learning
```
