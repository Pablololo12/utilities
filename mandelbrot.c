/*
 * Author: Pablololo12
 */

/*
 * Order to compile with gcc:
 * gcc -O3 -o mandelbrot -fopenmp mandelbrot.c
 *
 * To execute first set number of threads
 * export OMP_NUM_THREADS=4
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>

const int SIZEX=4500;
//const int SIZEY=3000;
//const int SIZEX=450;
const int SIZEY=4500;
const int max_iter=2000;

int mandelbrot(double ix, double iy)
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

int julia(double ix, double iy)
{
	int iter=0;
	double x = ix, y =iy;
	double x2 = x*x, y2 = y*y;
	double c1=0.285;
	double c2=-0.01;

	while ((x2 + y2 < 4) && (iter < max_iter)) {
		y = 2*x*y + c2;
		x = x2 - y2 + c1;
		x2 = x*x;
		y2 = y*y;
		iter++;
	}	
	return(iter);
}

int write_picture(int *img[SIZEY], int x, int y) {
	FILE * imagen;
	int i,d, r, g, b, val;
	double color;

	imagen = fopen("mandelbrot.ppm", "w");
	fprintf(imagen, "P3 %d %d 255\n", x, y);

	for (i=0; i<y; i++) {
		for (d=0; d<x; d++) {
			color = (double) img[i][d]+1;
			color = log10(color);
			color = color/log10(max_iter);
			color = color*255;

			r = color;
			g = color;
			b = color;
			fprintf(imagen, "%d %d %d  ", r,g,b);
		}
	}
	fclose(imagen);
	return 1;
}

int main() {
	int i, d, j, y;
	double xv, yv;
	int *matrix[SIZEY];
	int valores[max_iter+1];
	for (i = 0; i < SIZEY; i++)
		matrix[i] = (int *) malloc(SIZEX*sizeof(int));

	int is_mandelbrot=0;

	if (is_mandelbrot) {
		#pragma omp parallel for
		for(y=0; y<SIZEY; y++) {
			for(int x=0; x<SIZEX;x++) {
				matrix[y][x] = mandelbrot(((3.0/SIZEX)*x)-2.0, ((2.0/SIZEY)*y)-1.0);
				//if (matrix[y][x]>255) matrix[y][x]=255;
				//matrix[y][x] = 255-matrix[y][x];
			} 
		}
	} else {
		#pragma omp parallel for
		for(y=0; y<SIZEY; y++) {
			for(int x=0; x<SIZEX;x++) {
				matrix[y][x] = julia(((2.0/SIZEX)*x)-1.0, ((3.0/SIZEY)*y)-1.5);
			} 
		}
	}
	write_picture(matrix, SIZEX, SIZEY);
}