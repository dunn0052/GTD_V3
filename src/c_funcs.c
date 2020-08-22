// compile with cc -o c_funcs.so -shared -fPIC c_funcs.c

#if defined(__BORLANDC__)
    typedef unsigned char uint8_t;
    typedef __int64 int64_t;
    typedef unsigned long uintptr_t;
#elif defined(_MSC_VER)
    typedef unsigned char uint8_t;
    typedef __int64 int64_t;
#else
    #include <stdint.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TRUE 1
#define FALSE 0

#define NUM_SPRITE_COORDS 8

struct C_POINT
{
    float x;
    float y;
};


struct C_RECT
{
    struct C_POINT upper_left;
    struct C_POINT lower_right;
};

struct C_GL_SPRITE_COORDS
{
    struct C_RECT origin;
    float *coords;
};

typedef struct C_POINT C_POINT;
typedef struct C_RECT C_RECT;
typedef struct C_GL_SPRITE_COORDS C_COORDS;

int collide_rect(C_RECT caller, C_RECT other)
{   

    //printf("\nCaller.upper_left.x: %i\nOther.lower_right.x: %i", caller.upper_left.x, other.lower_right.x);
    return (caller.upper_left.x < other.lower_right.x && 
             caller.lower_right.x > other.upper_left.x && 
             caller.upper_left.y > other.lower_right.y && 
             caller.lower_right.y < other.upper_left.y);
}

int collide_sprite_group_rects(C_COORDS* caller, C_COORDS *others[], int length)
{
    int i = 0;
    for(i = 0; i < length; i++)
    {
        if( collide_rect(caller->origin, others[i]->origin) )
        {
            return i;
        }
    }
    // return an out of bounds index
    return -1;
}


C_COORDS *create_sprite_coords(float x1, float y1, float x2, float y2, void* vertices)
{
    C_COORDS coord = 
    {
        {
            {x1, y1},
            {x2, y2}
        },

        (float *) vertices
    };

    C_COORDS *instance = &coord;
    printf("vertices: %p\n", (float *) vertices);
    printf("instance: %p\n", (void *) instance);
    // initiate origin rect
    instance->origin.upper_left.x = x1;
    instance->origin.upper_left.y = y2;
    instance->origin.lower_right.x = x2;
    instance->origin.lower_right.y = y1;

    instance->coords = vertices;

    // initiate coordinates
    instance->coords[0] = x1;
    instance->coords[1] = y1;
    instance->coords[2] = x2;
    instance->coords[3] = y1;
    instance->coords[4] = x2;
    instance->coords[5] = y2;
    instance->coords[6] = x1;
    instance->coords[7] = y2;

    return instance;
}

C_COORDS *initiate_coords(float x1, float y1, float x2, float y2,  float p_vertex[NUM_SPRITE_COORDS] , C_COORDS *instance)
{
    // initiate origin rect
    instance->origin.upper_left.x = x1;
    instance->origin.upper_left.y = y2;
    instance->origin.lower_right.x = x2;
    instance->origin.lower_right.y = y1;

    instance->coords = p_vertex;

    // initiate coordinates
    instance->coords[0] = x1;
    instance->coords[1] = y1;
    instance->coords[2] = x2;
    instance->coords[3] = y1;
    instance->coords[4] = x2;
    instance->coords[5] = y2;
    instance->coords[6] = x1;
    instance->coords[7] = y2;

    return instance;
}

void update_sprite_group_coords(float x, float y, C_COORDS **draw_coords[], int length)
{
    float x1, x2, y1, y2 = 0;

    int i = 0;
    for(i = 0; i < length; i++)
    {

    x1 = (*draw_coords[i])->origin.upper_left.x + x;
    y2 = (*draw_coords[i])->origin.upper_left.y + y;
    x2 = (*draw_coords[i])->origin.lower_right.x + x;
    y1 = (*draw_coords[i])->origin.lower_right.y + y;

    (*draw_coords[i])->coords[0] = x1;
    (*draw_coords[i])->coords[1] = y1;
    (*draw_coords[i])->coords[2] = x2;
    (*draw_coords[i])->coords[3] = y1;
    (*draw_coords[i])->coords[4] = x2;
    (*draw_coords[i])->coords[5] = y2;
    (*draw_coords[i])->coords[6] = x1;
    (*draw_coords[i])->coords[7] = y2;
    }
}

void move_sprite(float x, float y, C_COORDS *sprite_coords)
{

    sprite_coords->origin.upper_left.x += x;
    sprite_coords->origin.upper_left.y += y;
    sprite_coords->origin.lower_right.x += x;
    sprite_coords->origin.lower_right.y =+ y;

// should have coordinates updated?

    float x1 = sprite_coords->origin.upper_left.x;
    float y2 = sprite_coords->origin.upper_left.y;
    float x2 = sprite_coords->origin.lower_right.x;
    float y1 = sprite_coords->origin.lower_right.y;

    sprite_coords->coords[0] = x1;
    sprite_coords->coords[1] = y1;
    sprite_coords->coords[2] = x2;
    sprite_coords->coords[3] = y1;
    sprite_coords->coords[4] = x2;
    sprite_coords->coords[5] = y2;
    sprite_coords->coords[6] = x1;
    sprite_coords->coords[7] = y2;
}


void update_sprite_group_vertices(float x, float y, C_COORDS *draw_coords[], float vertices[][NUM_SPRITE_COORDS], int length)
{
    float x1, x2, y1, y2 = 0;

    int i = 0;
    for(i = 0; i < length; i++)
    {

    x1 = draw_coords[i]->origin.upper_left.x + x;
    y2 = draw_coords[i]->origin.upper_left.y + y;
    x2 = draw_coords[i]->origin.lower_right.x + x;
    y1 = draw_coords[i]->origin.lower_right.y + y;

    draw_coords[i]->coords[0] = vertices[i][0] = x1;
    draw_coords[i]->coords[1] = vertices[i][1] = y1;
    draw_coords[i]->coords[2] = vertices[i][2] = x2;
    draw_coords[i]->coords[3] = vertices[i][3] = y1;
    draw_coords[i]->coords[4] = vertices[i][4] = x2;
    draw_coords[i]->coords[5] = vertices[i][5] = y2;
    draw_coords[i]->coords[6] = vertices[i][6] = x1;
    draw_coords[i]->coords[7] = vertices[i][7] = y2;
    }
}