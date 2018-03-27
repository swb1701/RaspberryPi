/*!
 * @file demo1-snow.cpp
 *
 * Simple example for Adafruit_PixelDust on Raspberry Pi.
 * REQUIRES rpi-rgb-led-matrix LIBRARY!
 * I2C MUST BE ENABLED using raspi-config!
 *
 */

#ifndef ARDUINO // Arduino IDE sometimes aggressively builds subfolders

#include <string.h>
#include "led-matrix-c.h"
#include <signal.h>
#include <math.h>

struct RGBLedMatrix *matrix  = NULL;
volatile bool        running = true;

// Signal handler allows matrix to be properly deinitialized.
int sig[] = { SIGHUP,SIGINT,SIGQUIT,SIGABRT,SIGKILL,SIGBUS,SIGSEGV,SIGTERM };
#define N_SIGNALS (int)(sizeof sig / sizeof sig[0])

void irqHandler(int dummy) {
	if(matrix) {
		led_matrix_delete(matrix);
		matrix = NULL;
	}
	for(int i=0; i<N_SIGNALS; i++) signal(sig[i], NULL);
	running = false;
}

int main(int argc, char **argv) {
	struct RGBLedMatrixOptions options;
	struct LedCanvas          *canvas;
	int                        width, height, i;

	for(i=0; i<N_SIGNALS; i++) signal(sig[i], irqHandler); // ASAP!

	// Initialize LED matrix defaults
	memset(&options, 0, sizeof(options));
	options.rows         = 64;
	options.cols         = 64;
	options.chain_length = 1;

	// Parse command line input.  --led-help lists options!
	matrix = led_matrix_create_from_options(&options, &argc, &argv);
	if(matrix == NULL) return 1;

	// Create offscreen canvas for double-buffered animation
	canvas = led_matrix_create_offscreen_canvas(matrix);
	led_canvas_get_size(canvas, &width, &height);
	fprintf(stderr, "Size: %dx%d. Hardware gpio mapping: %s\n",
	  width, height, options.hardware_mapping);

	double pi=3.1415;
	int offset=0;
	int color=0;
	int dir=1;
	while(running) {
		led_canvas_clear(canvas);
		draw_circle(canvas,32,32,25,0,255,0);
		draw_circle(canvas,32,32,28,0,255,0);
		//led_canvas_set_pixel(canvas,32,32,color,0,0);
		for(int i=0;i<360;i+=36) {
		  draw_line(canvas,32,32,32+25*cos((i+offset)*pi/180),32+25*sin((i+offset)*pi/180),255-color,0,color);
		}
		// Update matrix contents on next vertical sync
		// and provide a new canvas for the next frame.
		canvas = led_matrix_swap_on_vsync(matrix, canvas);
		offset+=2;
		if (offset>360) offset=0;
		color+=dir;
		if (color>254 || color<1) {
		  dir=-1*dir;
		}
	}

	return 0;
}

#endif // !ARDUINO
