Sure, here is the same information in Markdown format:

```markdown
# Setting Up NAT on a Linux Machine

Setting up a Network Address Translation (NAT) on a Linux machine involves configuring the interfaces, enabling IP forwarding, and configuring the firewall. 

**Note:** These steps require superuser access. 

## Step 1: Configure Network Interfaces

First, you'll need to set up your interfaces. This step will vary depending on your specific network. 

## Step 2: Enable IP Forwarding

For NAT to work properly, you need to enable IP forwarding in the kernel. 

To do this in both Ubuntu and RHEL:

1. Open the `/etc/sysctl.conf` file and add (or uncomment) the following line: 

    ```shell
    net.ipv4.ip_forward=1
    ```

2. After saving the file, reload the sysctl settings:

    ```shell
    sudo sysctl -p
    ```

## Step 3: Configure the Firewall

The steps for configuring the firewall depend on whether you're using Ubuntu (ufw) or RHEL (firewalld).

### Ubuntu

1. Open the `before.rules` file located at `/etc/ufw/before.rules`.

2. Add the following NAT rules:

    ```shell
    *nat
    :POSTROUTING ACCEPT [0:0]
    -A POSTROUTING -s 192.168.0.0/16 -o eth0 -j MASQUERADE
    COMMIT
    ```

    Replace `192.168.0.0/16` with the subnet of your local network and `eth0` with your WAN interface.

3. Enable ufw:

    ```shell
    sudo ufw enable
    ```

### RHEL

1. Check your zone settings:

    ```shell
    sudo firewall-cmd --get-active-zones
    ```

2. Set your interfaces to the appropriate zones:

    ```shell
    sudo firewall-cmd --zone=external --add-interface=eth0
    sudo firewall-cmd --zone=internal --add-interface=eth1
    ```

    Replace `eth0` and `eth1` with your actual WAN and LAN interfaces, respectively.

3. Enable masquerading on the external zone:

    ```shell
    sudo firewall-cmd --zone=external --add-masquerade
    ```

    Or use direct rules:

    ```shell
    sudo firewall-cmd --direct --add-rule ipv4 nat POSTROUTING 0 -o eth0 -j MASQUERADE
    ```

## Step 4: Apply the Settings

For `ufw`, the changes you made will be applied immediately. 

For `firewalld`, make the changes permanent and then reload the firewall:

```shell
sudo firewall-cmd --runtime-to-permanent
sudo firewall-cmd --reload
```

Your Linux machine should now be set up to use NAT.
