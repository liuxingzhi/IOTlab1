#include <mcp_can.h>
#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>

long unsigned int rxId;
unsigned char len = 0;
unsigned char rxBuf[8];
char msgString[128];                        // Array to store serial string
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];   //buffer for receive from raspberry pi

#define CAN0_INT 2                              // Set INT to pin 2
MCP_CAN CAN0(10);                               // Set CS to pin 10

byte mac[] = {0x00, 0x55, 0x66, 0xEE, 0xFF, 0xFF};
IPAddress      ip(192, 100, 50, 233);
//IPAddress    dest(10,195,39,251); // this address is my own computer's address
IPAddress dest(10,42,0,1)
unsigned int localPort = 8888;
unsigned int   remPort = 54321;

EthernetUDP UDP;

void setup()
{
  Serial.begin(115200);
  
  // Initialize MCP2515 running at 16MHz with a baudrate of 500kb/s and the masks and filters disabled.
  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_16MHZ) == CAN_OK)
    Serial.println("MCP2515 Initialized Successfully!");
  else
    Serial.println("Error Initializing MCP2515...");
  
  CAN0.setMode(MCP_NORMAL);                     // Set operation mode to normal so the MCP2515 sends acks to received data.

  pinMode(CAN0_INT, INPUT);                            // Configuring pin for /INT input

  Ethernet.begin(mac,ip);                          // Initialize Ethernet
  UDP.begin(localPort);
  Serial.println("CAN to Ethernet...");
}

void loop()
{
  if(!digitalRead(CAN0_INT))                         // If CAN0_INT pin is low, read receive buffer
  {
    CAN0.readMsgBuf(&rxId, &len, rxBuf);      // Read data: len = data length, buf = data byte(s)
    
    if((rxId & 0x80000000) == 0x80000000)     // Determine if ID is standard (11 bits) or extended (29 bits)
      sprintf(msgString, "Extended ID: 0x%.8lX  DLC: %1d  Data:", (rxId & 0x1FFFFFFF), len);
    else
      sprintf(msgString, "Standard ID: 0x%.3lX       DLC: %1d  Data:", rxId, len);
  
    Serial.print(msgString);
  
    if((rxId & 0x40000000) == 0x40000000){    // Determine if message is a remote request frame.
      sprintf(msgString, " REMOTE REQUEST FRAME");
      Serial.print(msgString);
    } else {
      for(byte i = 0; i<len; i++){
        sprintf(msgString, " 0x%.2X", rxBuf[i]);
        Serial.print(msgString);
      }
      UDP.beginPacket(dest, remPort);
      UDP.write(msgString);
      UDP.endPacket();
    }
        
    Serial.println();
    delay(100);
  }
}
