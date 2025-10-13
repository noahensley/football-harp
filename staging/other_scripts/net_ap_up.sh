sudo nmcli con add con-name hotspot ifname wlan0 type wifi ssid "n8ssu1200"
sudo nmcli con modify hotspot wifi-sec.key-mgmt wpa-psk
sudo nmcli con modify hotspot wifi-sec.psk "SpotMe11"
sudo nmcli con modify hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
ip address
