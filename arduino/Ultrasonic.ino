#include <SPI.h>
#include <mcp_can.h>


#define ECHO 43
#define TRIG 42
#define LED_OUT 22
#define CAN_INT 2

long unsigned int rxId;
unsigned char len = 0;
unsigned char rxBuf[8];
char msgString[128];

unsigned distance;
float temp;
int i;

MCP_CAN CAN0(53);     // 53 if mega 2560
void setup() {
    Serial.begin(115200);
    if (CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_16MHZ) == CAN_OK)
        Serial.println("MCP2515 Initialized Successfully!");
    else
        Serial.println("Error Initializing MCP2515...");

    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);
    pinMode(LED_OUT, OUTPUT);
    digitalWrite(LED_OUT, LOW);
}

byte data[8] = {0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0};

void loop() {
    if (!digitalRead(CAN_INT))
        CAN0.readMsgBuf(&rxId, &len, rxBuf);
    
    digitalWrite(TRIG, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);


    temp = float(pulseIn(ECHO, HIGH));
    distance = (temp * 17) / 1000;
    for (i = 3; i >= 0; i--) {
        data[i] = distance % 10;
        distance /= 10;
    }
    if (rxBuf[0])
        digitalWrite(LED_OUT, HIGH);
    else
        digitalWrite(LED_OUT, LOW);

    Serial.print(distance);
    Serial.println(" cm");

    data[0] = distance & 0xff;
    data[1] = distance & 0xff00;
    Serial.println(data[0]);
    Serial.println(data[1]);
    byte sndStat = CAN0.sendMsgBuf(0x100, 0, 2, data);
    if (sndStat == CAN_OK) {
        Serial.println("Message Sent Successfully!");
    } else {
        Serial.println("Error Sending Message...");
    }
    delay(1000);
}
