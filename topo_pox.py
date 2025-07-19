#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import RemoteController, OVSSwitch
from mininet.log import setLogLevel, info

class TopoWithL3Switch(Topo):
    def build(self):
        # Switches
        s1 = self.addSwitch('s1')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')  # Optionnel

        # Hosts
        h1 = self.addHost('h1', ip='10.0.1.1/24')
        h2 = self.addHost('h2', ip='10.0.1.2/24')
        h3 = self.addHost('h3', ip='10.0.2.1/24')
        h4 = self.addHost('h4', ip='10.0.2.2/24')

        # Hôte routeur nommé 's2' (ce sera notre "switch L3")
        s2 = self.addHost('s2')  # Routeur Linux (de nom "s2")

        # Connexions hôtes - switches
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s3)
        self.addLink(h4, s3)

        # L3 switch (s2) connecté à s1 et s3
        self.addLink(s2, s1)
        self.addLink(s2, s3)

        # Optionnel : s1 et s3 connectés à un backbone
        self.addLink(s1, s4)
        self.addLink(s3, s4)

def run():
    setLogLevel('info')

    net = Mininet(topo=TopoWithL3Switch(), switch=OVSSwitch, controller=None, autoSetMacs=True)

    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    net.start()

    # Le "switch L3" Linux nommé s2
    s2 = net.get('s2')
    s2.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Configuration des IPs sur les interfaces de s2
    intf1 = s2.intfList()[0]  # vers s1
    intf2 = s2.intfList()[1]  # vers s3

    s2.cmd(f'ifconfig {intf1} 10.0.1.254/24')
    s2.cmd(f'ifconfig {intf2} 10.0.2.254/24')

    # Routes par défaut pour les hôtes
    host_gws = {
        'h1': '10.0.1.254',
        'h2': '10.0.1.254',
        'h3': '10.0.2.254',
        'h4': '10.0.2.254'
    }

    for host, gw in host_gws.items():
        net.get(host).cmd(f'ip route add default via {gw}')

    info("*** Test de connectivité inter-sous-réseaux ***\n")
    net.pingAll()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()
