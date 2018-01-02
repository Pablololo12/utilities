/*
 * Author: Pablololo12
 */

/*
 * Order to compile with gcc:
 * gcc -o mandelbrot -fopenmp mandelbrot.c
 *
 * To execute first set number of threads
 * export OMP_NUM_THREADS=4
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

const int SIZEX=4500;
const int SIZEY=3000;
const int max_iter=2000;

int inset(double ix, double iy)
{
	int iter = 0;
	double x = ix, y =iy;
	double x2 = x*x, y2 = y*y;
	
	while ((x2 + y2 < 4) && (iter < max_iter)) {
		y = 2*x*y + iy;
		x = x2 - y2 + ix;
		x2 = x*x;
		y2 = y*y;
		iter++;
	}
	return(iter);
}

int write_picture(int *img[SIZEY], int x, int y) {
	FILE * imagen;
	int i,d, max;
	double color;

	max = 0;
	for (i=0; i<y; i++) {
		for (d=0; d<x; d++) {
			if (img[i][d]>max) max = img[i][d];
		}
	}

	imagen = fopen("madelbrot.ppm", "w");
	fprintf(imagen, "P3 %d %d 255\n", x, y);

	for (i=0; i<y; i++) {
		for (d=0; d<x; d++) {
			color = (double)(img[i][d])/(double)(max_iter);
			color = color*255;
			fprintf(imagen, "%d %d %d  ", (int)color,(int)color,(int)color);
		}
	}
	fclose(imagen);
	return 1;
}

int main() {
	int i, d, j, y;
	double xv, yv;
	int *matrix[SIZEY];
	for (i = 0; i < SIZEY; i++)
		matrix[i] = (int *) malloc(SIZEX*sizeof(int));
	
	#pragma omp parallel for
	for(y=0; y<SIZEY; y++) {
		for(int x=0; x<SIZEX;x++) {
			matrix[y][x] = inset(((3.0/SIZEX)*x)-2.0, ((2.0/SIZEY)*y)-1.0);
		} 
	}
	int max = 0;
	write_picture(matrix, SIZEX, SIZEY);
}