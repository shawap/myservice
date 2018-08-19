#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#define NUMBER_OF_LAYER {} 
#define NUMBER_OF_GAP  {} 

#define LOOP_INTERCHANGE     0


__attribute__((always_inline)) inline double RELU(const double x) lbrace return x > 0 ? x : 0; rbrace

int RunModel(double *input, double *output)
lbrace
    int err = 0;
    _NN_ nn;
    Init_NN(&nn);
    
    err = Test_NN(&nn, input, output);
    Free_NN(&nn);

    return err ? -1 : 0;

rbrace



int Init_NN(_NN_ *nn)
lbrace
    // dimension infos
    nn->numlay = NUMBER_OF_LAYER;
    nn->maxdim = {};
    memcpy(nn->laydim, {}, sizeof(int) * NUMBER_OF_LAYER);
    
 
    // extra space for storing results
    nn->temp[0] = (double *) malloc(sizeof(double) * nn->maxdim); assert(nn->temp[0] != NULL);
    nn->temp[1] = (double *) malloc(sizeof(double) * nn->maxdim); assert(nn->temp[1] != NULL);


    // construct nns
    int i, j, ofst = 0, err = 0;
    double coef[] = {}
    for(i = 0; i < NUMBER_OF_GAP; i++)
    lbrace
        int wdim = nn->laydim[i] * nn->laydim[i + 1];
        int bdim = nn->laydim[i + 1];
        nn->wei[i] = (double *) malloc(sizeof(double) * wdim); assert(nn->wei[i] != NULL);
        nn->bia[i] = (double *) malloc(sizeof(double) * bdim); assert(nn->bia[i] != NULL);
        memcpy(nn->wei[i], &coef[ofst], sizeof(double) * wdim);
        ofst += wdim;
        memcpy(nn->bia[i], &coef[ofst], sizeof(double) * bdim);
        ofst += bdim;
       
    rbrace

    return err;
    
rbrace


int GetNNInputSize(_NN_* nn)
lbrace
    assert(nn != NULL);
    return nn->laydim[0];
rbrace

int GetNNOutputSize(_NN_* nn)
lbrace
    assert(nn != NULL);
    return nn->laydim[nn->numlay - 1];
rbrace



int Test_NN(_NN_ *nn, double *input, double *output)
lbrace

    int i, t, m, n, k, iptdim, optdim, err = 0;
    iptdim = nn->laydim[0];
    // single test
    for(i = 0, t = 0; i < iptdim ; i++)
    lbrace

        nn->temp[t & 1][i] = input[i];
        if((i + 1) % iptdim == 0)  // every single test;
        lbrace
            //i = -1; 
            for(m = 0; m < nn->numlay - 1; m++)
            lbrace
                t++;
                memset(nn->temp[t & 1], 0, sizeof(double) * nn->maxdim);
                // set bias here
                memcpy(nn->temp[t & 1], nn->bia[m], sizeof(double) * nn->laydim[m + 1]); // should be m+1
                // weighting
#if LOOP_INTERCHANGE
                for(k = 0; k < nn->laydim[m + 1]; k++)
                lbrace
                    for(n = 0; n < nn->laydim[m]; n++)
                    lbrace
#else
                for(n = 0; n < nn->laydim[m]; n++)
                lbrace
                    for(k = 0; k < nn->laydim[m + 1]; k++)
                    lbrace
#endif
                        nn->temp[t & 1][k] += nn->temp[!(t & 1)][n] * nn->wei[m][n * nn->laydim[m+1] + k];
                    rbrace
                rbrace
                // activation functions here;
                for(k = 0; k < nn->laydim[m + 1]; k++)
                lbrace
                    nn->temp[t & 1][k] = RELU(nn->temp[t & 1][k]);
                rbrace
            rbrace
            optdim = nn->laydim[nn->numlay - 1];
            for(k = 0; k < optdim; k++)
            lbrace
                printf("[%d]:\t%lf\r\n", k, nn->temp[t & 1][k]);
                output[k] = nn->temp[t & 1][k];
            rbrace
        rbrace
    rbrace
    //fclose(fp);

    return err;
rbrace



void Free_NN(_NN_ *nn)
lbrace
    int i;
    int numgap = nn->numlay - 1;
    for(i = 0; i < numgap; i++)
    lbrace
        free(nn->wei[i]);
        free(nn->bia[i]);
    rbrace
    free(nn->temp[0]);
    free(nn->temp[1]);

rbrace