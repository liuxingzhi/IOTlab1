/*
    UDPSendReceiveString:
    This sketch receives UDP message strings, prints them to the serial port
    and sends an "acknowledge" string back to the sender

    A Processing sketch is included at the end of file that can be used to send
    and received messages for testing with a computer.

    created 21 Aug 2010
    by Michael Margolis

    This code is in the public domain.
*/

#include <mcp_can.h>
#include <mcp_can_dfs.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#define CAN_INT 2

MCP_CAN CAN0(10);

byte mac[] = {
    0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
IPAddress ip(10, 42, 0, 237);

unsigned int localPort = 5005;      // local port to listen on

char packetBuffer[UDP_TX_PACKET_MAX_SIZE];  // buffer to hold incoming packet,
char ReplyBuffer[] = "0000";        // a string to send back

// An EthernetUDP instance to let us send and receive packets over UDP
EthernetUDP Udp;

bool flag;
float temp;
unsigned distance;
unsigned distance_temp;
int i;
byte data[] = {0, 0, 0, 0, 0, 0, 0, 0};

long unsigned int rxId;
unsigned char len = 0;
char rxBuf[8];
char msgString[128];

void setup() {
    Serial.begin(115200);
    while (!Serial);
    Ethernet.init(10);  // Most Arduino shields
    // start the Ethernet
    Serial.println("Start initialization");
    Ethernet.begin(mac, ip);
    // Check for Ethernet hardware present
    if (Ethernet.hardwareStatus() == EthernetNoHardware) {
        Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
        while (true) {
            delay(1); // do nothing, no point running without Ethernet hardware
        }
    }
    if (Ethernet.linkStatus() == LinkOFF) {
        Serial.println("Ethernet cable is not connected.");
    }

    // start UDP
    Udp.begin(localPort);
    if (CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_16MHZ) == CAN_OK) Serial.println("MCP2515 Initialized Successfully!");
    else Serial.println("Error Initializing MCP2515...");
    pinMode(CAN_INT, INPUT);
    CAN0.setMode(MCP_NORMAL);
}

void loop() {
    if (!digitalRead)
        CAN0.readMsgBuf(&rxId, &len, rxBuf);

    int packetSize = Udp.parsePacket();
    if (packetSize) {
        Serial.print("Received packet of size ");
        Serial.println(packetSize);
        Serial.print("From ");
        IPAddress remote = Udp.remoteIP();
        for (int i = 0; i < 4; i++) {
            Serial.print(remote[i], DEC);
            if (i < 3) {
                Serial.print(".");
            }
        }
        Serial.print(", port ");
        Serial.println(Udp.remotePort());

        // read the packet into packetBufffer
        Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
        Serial.println("Contents:");
        Serial.println(packetBuffer);
        flag = packetBuffer[0] == 'T';
        if (flag) {
            data[0] = 1;
        } else {
            data[0] = 0;
        }
        byte sndStat = CAN0.sendMsgBuf(0x100, 0, 8, data);
        if (sndStat == CAN_OK) {
            Serial.println("Message Sent Successfully!");
        } else {
            Serial.println("Error Sending Message...");
        }
        // send a reply to the IP address and port that sent us the packet we received
        Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
        Udp.write(rxBuf);
        Udp.endPacket();
    } else {
        Serial.println("No msg");
    }
    delay(100);
}
