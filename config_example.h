#ifndef __CONFIG__H__
#define __CONFIG__H__

#include <stdio.h>
#include <stdbool.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "freertos/semphr.h"
#include "freertos/event_groups.h"
#include "driver/gpio.h"

#define CORE_0 0
#define CORE_1 1
#define PIN_SWITCH 19
#define PIN_LED 18
#define PIN_LED_WIFI 2

#define WIFI_SSID ""
#define WIFI_PASS ""

#define MQTT_URI   "mqtt://ip:1883"
#define MQTT_USER  "your mqtt user"
#define MQTT_PASS  "your mqtt pass"

#define MQTT_CLIID "grupo2"

#define TOPIC1 "/engcomp/sensor"

extern QueueHandle_t xQueueSwitch;
extern QueueHandle_t xQueueClicks;

typedef struct {
    int led;
	bool status;
} info_led_t;

typedef struct {
    int clicks;
} info_count_t;

extern info_led_t info_led;
extern info_count_t info_count;

#endif