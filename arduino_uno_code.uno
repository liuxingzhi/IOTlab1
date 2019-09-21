/*
   UIPEthernet UdpClient example.

   UIPEthernet is a TCP/IP stack that can be used with a enc28j60 based
   Ethernet-shield.

   UIPEthernet uses the fine uIP stack by Adam Dunkels <adam@sics.se>

        -----------------

   This UdpClient example tries to send a packet via udp to 192.168.0.1
   on port 5000 every 5 seconds. After successfully sending the packet it
   waits for up to 5 seconds for a response on the local port that has been
   implicitly opened when sending the packet.

   Copyright (C) 2013 by Norbert Truchsess (norbert.truchsess@t-online.de)
*/



#include <UIPEthernet.h>

EthernetUDP udp;
unsigned long next;


void setup() {
    uint8_t mac[6] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05};
    Ethernet.begin(mac, IPAddress(10, 42, 0, 237)
    );
    next = millis() + 5000;
}

void loop() {
    int success;
    int len = 0;
    if (millis() > next) {
        do {
            success = udp.beginPacket(IPAddress(10, 42, 0, 1), 5005);
            //beginPacket fails if remote ethaddr is unknown. In this case an
            //arp-request is send out first and beginPacket succeeds as soon
            //the arp-response is received.
        } while (!success && (millis() < next));
        if (success) {
            success = udp.write("hello world from arduino");
            success = udp.endPacket();
            do {
                //check for new udp-packet:
                success = udp.parsePacket();
            } while (!success && (millis() < next));
            if (success) {
                do {
                    char c = udp.read();
                    len++;
                } while ((success = udp.available()) > 0);
                //finish reading this packet:
                udp.flush();
            }
        }
        udp.stop();
        next = millis() + 5000;
    }
}