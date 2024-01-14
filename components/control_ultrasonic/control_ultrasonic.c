#include "esp_err.h"
#include "locale.h"

#include "../../config.h"
#include "include/control_ultrasonic.h"
#include "../ultrasonic/ultrasonic.h"

#define MAX_DISTANCE_CM 400
#define TRIGGER_GPIO 26
#define ECHO_GPIO 25

void vTaskUltrasonic(void *pvParameters) {
    ultrasonic_sensor_t sensor = {
        .trigger_pin = TRIGGER_GPIO,
        .echo_pin    = ECHO_GPIO
    };
    
    ultrasonic_init(&sensor);

    while(true){
        uint32_t distance;
        esp_err_t res = ultrasonic_measure_cm(&sensor, MAX_DISTANCE_CM, &distance);

        if (res != ESP_OK) {
            printf("[ERRO %d] - ", res);
            switch (res) {
                case ESP_ERR_ULTRASONIC_PING:
                    printf("Não é possível executar o ping (o dispositivo está em estado inválido)\n");
                    break;
                case ESP_ERR_ULTRASONIC_PING_TIMEOUT:
                    printf("Tempo esgotado no Ping (nenhum dispositivo encontrado)\n");
                    break;
                case ESP_ERR_ULTRASONIC_ECHO_TIMEOUT:
                    printf("Tempo esgotado para eco (distância muito grande)\n");
                    break;
                default:
                printf("%s\n", esp_err_to_name(res));
            }
        } else {
            // printf("Distance: %0.04f cm\n", distance*100);
            printf("Distance: %d\n", distance);

        }
        vTaskDelay( 500 / portTICK_PERIOD_MS );
    }
}