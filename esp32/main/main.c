#include <stdio.h>
#include "esp_log.h"
#include "nvs_flash.h"
#include "../config.h"

#include "../components/control_led/include/control_led.h"
#include "../components/control_wifi/include/control_wifi.h"
#include "../components/control_mqtt/include/control_mqtt.h"
#include "../components/control_ultrasonic/include/control_ultrasonic.h"

QueueHandle_t xQueueSwitch;
QueueHandle_t xQueueSensor;

void init_app(void);

void app_main(void) {
    init_app();

    xTaskCreatePinnedToCore( vTaskLed, "TaskLed", configMINIMAL_STACK_SIZE + 2048, NULL, 4, NULL, CORE_0 );
    xTaskCreatePinnedToCore( vTaskWifi, "TaskWifi", configMINIMAL_STACK_SIZE + 2048, NULL, 6, NULL, CORE_1);
    xTaskCreatePinnedToCore( vTaskPublisher, "TaskPublisher", configMINIMAL_STACK_SIZE + 1024*5, NULL, 4, NULL, CORE_1 );
    xTaskCreatePinnedToCore( vTaskUltrasonic, "TaskUltrasonic", configMINIMAL_STACK_SIZE + 1024, NULL, 4, NULL, CORE_1 );
}

void init_app(void) {
    // initialize nvs, else wifi don't works
    ESP_ERROR_CHECK(nvs_flash_init());

    initWifi();
    xQueueSwitch = xQueueCreate( 5, sizeof(info_led) );
    xQueueSensor = xQueueCreate( 5, sizeof(info_sensor) );
}