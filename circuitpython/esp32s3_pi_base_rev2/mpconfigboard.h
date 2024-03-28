#define MICROPY_HW_BOARD_NAME "ESP32S3 Pi Base Rev2"
#define MICROPY_HW_MCU_NAME         "ESP32S3"

#define MICROPY_HW_NEOPIXEL         (&pin_GPIO21)

#define CIRCUITPY_BOARD_I2C         (1)
#define CIRCUITPY_BOARD_I2C_PIN     {{.scl = &pin_GPIO14, .sda = &pin_GPIO13}}

#define DEFAULT_SPI_BUS_SCK         (&pin_GPIO1)
#define DEFAULT_SPI_BUS_MISO        (&pin_GPIO42)
#define DEFAULT_SPI_BUS_MOSI        (&pin_GPIO2)

#define CIRCUITPY_BOARD_UART        (1)
#define CIRCUITPY_BOARD_UART_PIN    {{.tx = &pin_GPIO15, .rx = &pin_GPIO16}}
