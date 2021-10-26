#include <SPI.h>
#include <MFRC522.h>

   // Other hardware pins
    const byte rstPin =  9;                // Reset pin
    const byte  ssPin = 10;                // Slave Select pin
    
    // Instantiate MFRC522 object class
    MFRC522 rfidReader(ssPin, rstPin);
 
    // Other Global Constants 
    const long timeout = 30000;            
    char* myTags[100] = {};
    int tagsCount = 0;
    String tagID = "";

void setup() {
    // Initiating
    Serial.begin(9600);                     // Start the serial monitor
    SPI.begin();                            // Start SPI bus
    rfidReader.PCD_Init();                  // Start MFRC522 object

    while (!Serial);                        // Do nothing if no serial port is opened
}

void loop() {
    if (isTagPresent()==true){
        getTagID();
    } else {
        delay(50);
    }
    
}    
bool isTagPresent(){    
    bool returnValue = true;
    
    // NOT a new PICC_IsNewCardPresent in RFID reader
    //OR
    // NOT a PICC_ReadCardSerial active in Serial
    if ( !rfidReader.PICC_IsNewCardPresent() || !rfidReader.PICC_ReadCardSerial() ) { 
      returnValue = false;
    }
    return returnValue;
}

bool getTagID() {
    tagID = "";
    
//    Serial.print(F(" UID tag: "));
    for (byte i = 0; i < rfidReader.uid.size; i++){
        // The MIFARE PICCs that we use have 4 byte UID
        Serial.print(rfidReader.uid.uidByte[i] < 0x10 ? " 0" : " ");
        Serial.print(rfidReader.uid.uidByte[i], HEX);
        // Adds the bytes in a single String variable
        tagID.concat(String(rfidReader.uid.uidByte[i] < 0x10 ? " 0" : " "));
        tagID.concat(String(rfidReader.uid.uidByte[i], HEX));
    }
    tagID.toUpperCase();
    rfidReader.PICC_HaltA();
    Serial.println();
    // Stop reading
    return true;
}
