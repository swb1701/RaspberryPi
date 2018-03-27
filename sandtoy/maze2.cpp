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
#include <unistd.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include "lis3dh.h"

Adafruit_LIS3DH      lis3dh;
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
typedef struct
{
	int x, y; //Node position - little waste of memory, but it allows faster generation
	void *parent; //Pointer to parent node
	char c; //Character to be displayed
	char dirs; //Directions that still haven't been explored
} Node;

Node *nodes; //Nodes array
int width=31;
int height=31; //Maze dimensions

int init( )
{
	int i, j;
	Node *n;
	
	//Allocate memory for maze
	nodes = calloc( width * height, sizeof( Node ) );
	if ( nodes == NULL ) return 1;
		
	//Setup crucial nodes
	for ( i = 0; i < width; i++ )
	{
		for ( j = 0; j < height; j++ )
		{
			n = nodes + i + j * width;
			if ( i * j % 2 ) 
			{
				n->x = i;
				n->y = j;
				n->dirs = 15; //Assume that all directions can be explored (4 youngest bits set)
				n->c = ' '; 
			}
			else n->c = '#'; //Add walls between nodes
		}
	}
	return 0;
}

Node *link( Node *n )
{
	//Connects node to random neighbor (if possible) and returns
	//address of next node that should be visited

	int x, y;
	char dir;
	Node *dest;
	
	//Nothing can be done if null pointer is given - return
	if ( n == NULL ) return NULL;
	
	//While there are directions still unexplored
	while ( n->dirs )
	{
		//Randomly pick one direction
		dir = ( 1 << ( rand( ) % 4 ) );
		
		//If it has already been explored - try again
		if ( ~n->dirs & dir ) continue;
		
		//Mark direction as explored
		n->dirs &= ~dir;
		
		//Depending on chosen direction
		switch ( dir )
		{
			//Check if it's possible to go right
			case 1:
				if ( n->x + 2 < width )
				{
					x = n->x + 2;
					y = n->y;
				}
				else continue;
				break;
			
			//Check if it's possible to go down
			case 2:
				if ( n->y + 2 < height )
				{
					x = n->x;
					y = n->y + 2;
				}
				else continue;
				break;
			
			//Check if it's possible to go left	
			case 4:
				if ( n->x - 2 >= 0 )
				{
					x = n->x - 2;
					y = n->y;
				}
				else continue;
				break;
			
			//Check if it's possible to go up
			case 8:
				if ( n->y - 2 >= 0 )
				{
					x = n->x;
					y = n->y - 2;
				}
				else continue;
				break;
		}
		
		//Get destination node into pointer (makes things a tiny bit faster)
		dest = nodes + x + y * width;
		
		//Make sure that destination node is not a wall
		if ( dest->c == ' ' )
		{
			//If destination is a linked node already - abort
			if ( dest->parent != NULL ) continue;
			
			//Otherwise, adopt node
			dest->parent = n;
			
			//Remove wall between nodes
			nodes[n->x + ( x - n->x ) / 2 + ( n->y + ( y - n->y ) / 2 ) * width].c = ' ';
			
			//Return address of the child node
			return dest;
		}
	}
	
	//If nothing more can be done here - return parent's address
	return n->parent;
}

void draw( )
{
	int i, j;

	//Outputs maze to terminal - nothing special
	for ( i = 0; i < height; i++ )
	{
		for ( j = 0; j < width; j++ )
		{
		  fprintf(stdout,"%c", nodes[j + i * width].c );
		}
		fprintf(stdout,"\n");
	}
}

int main(int argc, char **argv) {
	struct RGBLedMatrixOptions options;
	struct LedCanvas          *canvas;
	int                        w,h,i;
	int                        xx, yy, zz;

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
	led_canvas_get_size(canvas, &w, &h);
	fprintf(stderr, "Size: %dx%d. Hardware gpio mapping: %s\n",
	  w, h, options.hardware_mapping);

	double pi=3.1415;
	int offset=0;
	int color=0;
	int dir=1;

	Node *start, *last;
	fprintf(stdout,"Seeding Random...\n");
	srand(time(NULL));
	fprintf(stdout,"Initializing Maze...\n");
	init();
	//Setup start node
	start = nodes + 1 + width;
	start->parent = start;
	last = start;

	//Connect nodes until start node is reached and can't be left
	fprintf(stdout,"Computing Maze...\n");
        while ( ( last = link( last ) ) != start );
	fprintf(stdout,"Drawing Maze...\n");
	draw();
	int ballx=29;
	int bally=29;
	led_canvas_set_pixel(canvas,ballx,bally,255,0,0);
	canvas = led_matrix_swap_on_vsync(matrix, canvas);

	if(lis3dh.begin()) {
		puts("LIS3DH init failed");
		return 3;
	}

	int oq=-1;
	
	while(running) {
	  lis3dh.accelRead(&xx, &yy, &zz);
	  int16_t ax=-xx;
	  int16_t ay=-yy;
	  int16_t az=zz;
	  uint8_t scale=1;
          ax=(int32_t)ax*scale/256;
          ay=(int32_t)ay*scale/256;
          az=abs((int32_t)az*scale/2048);
	  az  = (az >= 4) ? 1 : 5 - az; // Clip & invert
	  ax -= az;                     // Subtract Z motion factor from X, Y,
	  ay -= az;                     // then...
	  /*
	  int8_t q = (int)(atan2(ay, ax) * 8.0 / M_PI); // -8 to +8
	  if (q!=oq) {
	    fprintf(stdout,"q=%d ax=%d ay=%d\n",q,ax,ay);
	    oq=q;
	  }
	  */
	  led_canvas_clear(canvas);

	int i0, j0;
	for ( i0 = 0; i0 < height; i0++ )
	{
		for ( j0 = 0; j0 < width; j0++ )
		{
		  if (nodes[j0+i0*width].c=='#') {
		    led_canvas_set_pixel(canvas,j0*2,i0*2,150,150,150);
		    led_canvas_set_pixel(canvas,j0*2,i0*2+1,150,150,150);
		    led_canvas_set_pixel(canvas,j0*2+1,i0*2,150,150,150);
		    led_canvas_set_pixel(canvas,j0*2+1,i0*2+1,150,150,150);
		  }
		}
	}
	/*
	int k,j;
	for(k=-1;k<=1;k++) {
	  for(j=-1;j<=1;j++) {
	    fprintf(stdout,"%c",nodes[bally+j+(ballx+k)*width].c);
	  }
	  fprintf(stdout,"\n");
	}
	fprintf(stdout,"\n");
	*/
          if (ax<0) { //left
	    if (nodes[ballx-1+bally*width].c!='#') {
	      if (ballx>0) ballx--;
	    }
	  }
	  if (ay<0) { //up
	    if (nodes[ballx+(bally-1)*width].c!='#') {
	      if (bally>0) bally--;
	    }
	  }
	  if (ay>0) { //down
	    if (nodes[ballx+(bally+1)*width].c!='#') {
	      if (bally<31) bally++;
	    }
	  }
	  if (ax>0) { //right
	    if (nodes[ballx+1+bally*width].c!='#') {
	      if (ballx<31) ballx++;
	    }
	  }
	  led_canvas_set_pixel(canvas,ballx*2,bally*2,255,0,0);
	  led_canvas_set_pixel(canvas,ballx*2,bally*2+1,255,0,0);
	  led_canvas_set_pixel(canvas,ballx*2+1,bally*2,255,0,0);
	  led_canvas_set_pixel(canvas,ballx*2+1,bally*2+1,255,0,0);
	  
	  led_canvas_set_pixel(canvas,1*2,1*2,0,255,0);
	  led_canvas_set_pixel(canvas,1*2,1*2+1,0,255,0);
	  led_canvas_set_pixel(canvas,1*2+1,1*2,0,255,0);
	  led_canvas_set_pixel(canvas,1*2+1,1*2+1,0,255,0);

	  canvas = led_matrix_swap_on_vsync(matrix, canvas);
          usleep(100000);
	}

	return 0;
}

#endif // !ARDUINO
