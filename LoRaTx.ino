/* Heltec Automation send communication test example
 *
 * Function:
 * 1. Send data from a esp32 device over hardware 
 *  
 * Description:
 * 
 * HelTec AutoMation, Chengdu, China
 * 成都惠利特自动化科技有限公司
 * www.heltec.org
 *
 * this project also realess in GitHub:
 * https://github.com/Heltec-Aaron-Lee/WiFi_Kit_series
 * */

 /* Example modified for Scorpio project testing
    IoTUC, Santiago, Chile
    Sebastián Silva
 */

  //  * \param [IN] modem        Radio modem to be used [0: FSK, 1: LoRa]
  //  * \param [IN] power        Sets the output power [dBm]
  //  * \param [IN] fdev         Sets the frequency deviation (FSK only)
  //  *                          FSK : [Hz]
  //  *                          LoRa: 0
  //  * \param [IN] bandwidth    Sets the bandwidth (LoRa only)
  //  *                          FSK : 0
  //  *                          LoRa: [0: 125 kHz, 1: 250 kHz,
  //  *                                 2: 500 kHz, 3: Reserved]
  //  * \param [IN] datarate     Sets the Datarate
  //  *                          FSK : 600..300000 bits/s
  //  *                          LoRa: [6: 64, 7: 128, 8: 256, 9: 512,
  //  *                                10: 1024, 11: 2048, 12: 4096  chips]
  //  * \param [IN] coderate     Sets the coding rate (LoRa only)
  //  *                          FSK : N/A ( set to 0 )
  //  *                          LoRa: [1: 4/5, 2: 4/6, 3: 4/7, 4: 4/8]
  //  * \param [IN] preambleLen  Sets the preamble length
  //  *                          FSK : Number of bytes
  //  *                          LoRa: Length in symbols (the hardware adds 4 more symbols)
  //  * \param [IN] fixLen       Fixed length packets [0: variable, 1: fixed]
  //  * \param [IN] crcOn        Enables disables the CRC [0: OFF, 1: ON]
  //  * \param [IN] freqHopOn    Enables disables the intra-packet frequency hopping
  //  *                          FSK : N/A ( set to 0 )
  //  *                          LoRa: [0: OFF, 1: ON]
  //  * \param [IN] hopPeriod    Number of symbols between each hop
  //  *                          FSK : N/A ( set to 0 )
  //  *                          LoRa: Number of symbols
  //  * \param [IN] iqInverted   Inverts IQ signals (LoRa only)
  //  *                          FSK : N/A ( set to 0 )
  //  *                          LoRa: [0: not inverted, 1: inverted]
  //  * \param [IN] timeout      Transmission timeout [ms]

#include "LoRaWan_APP.h"
#include "Arduino.h"

#define RF_FREQUENCY                                915000000 // Hz
#define TX_OUTPUT_POWER                             5        // dBm
#define LORA_BANDWIDTH                              1         // [0: 125 kHz,
                                                              //  1: 250 kHz,
                                                              //  2: 500 kHz,
                                                              //  3: Reserved]
#define LORA_SPREADING_FACTOR                       7         // [SF7..SF12]
#define LORA_CODINGRATE                             1         // [1: 4/5,
                                                              //  2: 4/6,
                                                              //  3: 4/7,
                                                              //  4: 4/8]
#define LORA_PREAMBLE_LENGTH                        8         // Same for Tx and Rx
#define LORA_SYMBOL_TIMEOUT                         0         // Symbols
#define LORA_FIX_LENGTH_PAYLOAD_ON                  false     // If False -> Implicit header = No
#define LORA_IQ_INVERSION_ON                        false
#define LORA_CRC_ON                                 true

#define RX_TIMEOUT_VALUE                            1000
#define BUFFER_SIZE                                 256 // Define the payload size here

char txpacket[BUFFER_SIZE];
char rxpacket[BUFFER_SIZE];

double txNumber;

bool lora_idle=true;

static RadioEvents_t RadioEvents;
void OnTxDone( void );
void OnTxTimeout( void );

void setup() {
    Serial.begin(115200);
    Mcu.begin(HELTEC_BOARD,SLOW_CLK_TPYE);
	
    txNumber=0;

    RadioEvents.TxDone = OnTxDone;
    RadioEvents.TxTimeout = OnTxTimeout;
    
    Radio.Init( &RadioEvents );
    Radio.SetChannel( RF_FREQUENCY );
    Radio.SetTxConfig( MODEM_LORA,                    // Type of modem -> LoRa
                       TX_OUTPUT_POWER,               // Tx power in dBm
                       0,                             // Frecuency deviation
                       LORA_BANDWIDTH,                // Bandwidth
                       LORA_SPREADING_FACTOR,         // Spreading factor
                       LORA_CODINGRATE,               // Coding rate
                       LORA_PREAMBLE_LENGTH,          // Preamble lenght
                       LORA_FIX_LENGTH_PAYLOAD_ON,    // Implicit header
                       LORA_CRC_ON ,                  // CRC On
                       false,                         // Frecuency Hop On
                       0,                             // Frecuency Hop period
                       LORA_IQ_INVERSION_ON,          // IQ inverted On 
                       3000 );                        // Timeout time
   }

void loop()
{
	if(lora_idle == true)
	{
    delay(30000); // 30 seconds between transmissions
		txNumber += 0.01;

    const char* satelliteId = "1604";
    bool crcOk = true;
    double latitude = 37.7749;
    double longitude = -122.4194;
    double altitude = 550.0;
    double rssi = -113.75;
    double snr = -8.5;
    double freqError = 10515.13672;

    snprintf(
      txpacket,
      BUFFER_SIZE,
      "{\"starlink_id\":\"%s\",\"crc_ok\":%s,\"lat\":%.4f,\"lon\":%.4f,\"alt\":%.1f,\"rssi\":%.2f,\"snr\":%.1f,\"freq_error\":%.5f}",
      satelliteId,
      crcOk ? "true" : "false",
      latitude,
      longitude,
      altitude,
      rssi,
      snr,
      freqError
    );
   
		Serial.printf("\r\nsending packet \"%s\" , length %d\r\n",txpacket, strlen(txpacket));

		Radio.Send( (uint8_t *)txpacket, strlen(txpacket) ); //send the package out	
    lora_idle = false;
	}
  Radio.IrqProcess( );
}

void OnTxDone( void )
{
	Serial.println("TX done......");
	lora_idle = true;
}

void OnTxTimeout( void )
{
    Radio.Sleep( );
    Serial.println("TX Timeout......");
    lora_idle = true;
}