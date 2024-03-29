#include "include/control_mqtt.h"

#include <stdint.h>
#include <stddef.h>
#include <string.h>

#include "esp_wifi.h"
#include "esp_system.h"
#include "esp_event.h"
#include "esp_netif.h"

#include "lwip/sockets.h"
#include "lwip/dns.h"
#include "lwip/netdb.h"

#include "esp_log.h"
#include "mqtt_client.h"
#include "../../config.h"

static const char *TAG = "MQTT_SENSOR";

uint32_t MQTT_STATUS_CONNECTED = 0;
info_sensor_t info_sensor;
info_led_t info_status_led;
bool status_led = false;

static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data) {
    ESP_LOGD(TAG, "Event dispatched from event loop base=%s, event_id=%d", base, event_id);
    esp_mqtt_event_handle_t event = event_data;
    esp_mqtt_client_handle_t client = event->client;
    int msg_id;
    switch ((esp_mqtt_event_id_t)event_id) {
    case MQTT_EVENT_CONNECTED:
        ESP_LOGI(TAG, "MQTT_EVENT_CONNECTED");
        MQTT_STATUS_CONNECTED=1;
        
        // Subscribe in TOPIC1
        msg_id = esp_mqtt_client_subscribe(client, TOPIC1, 0);
        ESP_LOGI(TAG, "sent subscribe successful, msg_id=%d", msg_id);

        break;
    case MQTT_EVENT_DISCONNECTED:
        ESP_LOGI(TAG, "MQTT_EVENT_DISCONNECTED");
        MQTT_STATUS_CONNECTED=0;
        // mqtt_app_start();
        break;

    case MQTT_EVENT_SUBSCRIBED:
        ESP_LOGI(TAG, "MQTT_EVENT_SUBSCRIBED, msg_id=%d", event->msg_id);
        break;
    case MQTT_EVENT_UNSUBSCRIBED:
        ESP_LOGI(TAG, "MQTT_EVENT_UNSUBSCRIBED, msg_id=%d", event->msg_id);
        break;
    case MQTT_EVENT_PUBLISHED:
        ESP_LOGI(TAG, "MQTT_EVENT_PUBLISHED, msg_id=%d", event->msg_id);
        break;
    case MQTT_EVENT_DATA:
        ESP_LOGI(TAG, "MQTT_EVENT_DATA");
        printf("TOPIC=%.*s\r\n", event->topic_len, event->topic);
        printf("DATA=%.*s\r\n", event->data_len, event->data);
        break;
    case MQTT_EVENT_ERROR:
        ESP_LOGI(TAG, "MQTT_EVENT_ERROR");
        break;
    default:
        ESP_LOGI(TAG, "Other event id:%d", event->event_id);
        break;
    }
}

esp_mqtt_client_handle_t client = NULL;

void mqtt_app_start(void) {
    ESP_LOGI(TAG, "STARTING MQTT");
    esp_mqtt_client_config_t mqttConfig = {
        .uri =       MQTT_URI,
        .username  = MQTT_USER,
        .password  = MQTT_PASS,
        .client_id = MQTT_CLIID
    };
    
    client = esp_mqtt_client_init(&mqttConfig);
    esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, mqtt_event_handler, client);
    esp_mqtt_client_start(client);
}

void vTaskPublisher(void *pvParameter) {
    while (true) {
        if(MQTT_STATUS_CONNECTED) {
            xQueueReceive( xQueueSensor, &info_sensor, portMAX_DELAY);

            int measure = info_sensor.measure;
            int time    = info_sensor.time;
            // char message[2];
            // sprintf(message, "%d", measure);
            // printf("\nDistance Received: %s\n", message);

            // Necessary size to string
            int required_size = snprintf(NULL, 0, "{\"measure\": %d, \"time\": %d}", measure, time);

            // Alocate space to string
            char *json_string = (char *)malloc(required_size + 1);

            // Create Json
            snprintf(json_string, required_size + 1, "{\"measure\": %d, \"time\": %d}", measure, time);

            esp_mqtt_client_publish(client, TOPIC1, json_string, 0, 0, 0);
            vTaskDelay(490 / portTICK_PERIOD_MS);
        }
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}