#define MICROPY_HW_BOARD_NAME "ESP32S3 Zero Base Rev1"
#define MICROPY_HW_MCU_NAME         "ESP32S3"

#define MICROPY_HW_NEOPIXEL         (&pin_GPIO21)

#define CIRCUITPY_BOARD_I2C         (1)
#define CIRCUITPY_BOARD_I2C_PIN     {{.scl = &pin_GPIO14, .sda = &pin_GPIO13}}

#define DEFAULT_SPI_BUS_SCK         (&pin_GPIO35)
#define DEFAULT_SPI_BUS_MISO        (&pin_GPIO37)
#define DEFAULT_SPI_BUS_MOSI        (&pin_GPIO36)

#define CIRCUITPY_BOARD_UART        (1)
#define CIRCUITPY_BOARD_UART_PIN    {{.tx = &pin_GPIO11, .rx = &pin_GPIO12}}
