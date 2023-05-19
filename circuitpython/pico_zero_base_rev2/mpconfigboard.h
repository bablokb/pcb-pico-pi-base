#define MICROPY_HW_BOARD_NAME "Pico Zero Base Rev2"
#define MICROPY_HW_MCU_NAME "rp2040"

#define MICROPY_HW_LED_STATUS (&pin_GPIO25)

#define CIRCUITPY_BOARD_I2C         (1)
#define CIRCUITPY_BOARD_I2C_PIN     {{.scl = &pin_GPIO3, .sda = &pin_GPIO2}}

#define DEFAULT_SPI_BUS_SCK         (&pin_GPIO10)
#define DEFAULT_SPI_BUS_MISO        (&pin_GPIO12)
#define DEFAULT_SPI_BUS_MOSI        (&pin_GPIO11)


#define CIRCUITPY_BOARD_UART        (1)
#define CIRCUITPY_BOARD_UART_PIN    {{.tx = &pin_GPIO0, .rx = &pin_GPIO1}}
