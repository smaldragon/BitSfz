#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "wave_gen.h"

/*Standard values for ChipSFZ audio*/
#define SUBCHUNK1SIZE   (16)
#define AUDIO_FORMAT    (1) /*For PCM*/
#define NUM_CHANNELS    (1)
#define SAMPLE_RATE     (56320)

#define BITS_PER_SAMPLE (16)

#define BYTE_RATE       (SAMPLE_RATE * NUM_CHANNELS * BITS_PER_SAMPLE / 8)
#define BLOCK_ALIGN     (NUM_CHANNELS * BITS_PER_SAMPLE / 8)

typedef struct wavfile_header_s
{
    char  ChunkID[4];          /*  4   */
    __uint32_t ChunkSize;      /*  4   */
    char    Format[4];         /*  4   */
    char    Subchunk1ID[4];    /*  4   */
    __uint32_t Subchunk1Size;  /*  4   */
    __uint16_t AudioFormat;    /*  2   */
    __uint16_t NumChannels;    /*  2   */
    __uint32_t SampleRate;     /*  4   */
    __uint32_t ByteRate;       /*  4   */
    __uint16_t BlockAlign;     /*  2   */
    __uint16_t BitsPerSample;  /*  2   */
    
    char    Subchunk2ID[4];
    __uint32_t Subchunk2Size;
} wavfile_header_t;

wavfile_header_t create_header(__uint32_t size) {
    wavfile_header_t header;
    memcpy(header.ChunkID, "RIFF",4);
    header.ChunkSize = size+44;
    memcpy(header.Format, "WAVE",4);
    memcpy(header.Subchunk1ID, "fmt ",4);
    header.Subchunk1Size = SUBCHUNK1SIZE;
    header.AudioFormat = AUDIO_FORMAT; // 1 = PCM
    header.NumChannels = NUM_CHANNELS;
    header.SampleRate = SAMPLE_RATE;
    header.BitsPerSample = BITS_PER_SAMPLE;
    header.ByteRate = BYTE_RATE;
    header.BlockAlign = BLOCK_ALIGN;
    memcpy(header.Subchunk2ID, "data",4);
    header.Subchunk2Size = size;

    return header;
}
int write_noise(char* filename, int level) {
    FILE *fp;
    fp = fopen(filename, "wb");
    
    __int16_t buff[0xFFFF*16];
    __uint16_t noise = 1;

    for (int i = 0; i < 0xFFFF;i++) {
        
        for (int u = 0; u < 16;u++) {
            if (noise&1)
                buff[i*16+u]=8000;
            else
                buff[i*16+u]=-8000;
        }
        int out = noise & 1;
        __uint8_t feedback = (noise&1)^((noise>>level)&1);
        noise = noise >> 1;
        noise += feedback<<15;
    }
    wavfile_header_t header = create_header(0xFFFF*16);
    fwrite(&header,sizeof(wavfile_header_t),1,fp);
    fwrite(buff,sizeof(short),0xFFFF*16,fp);

    return 0;
}
