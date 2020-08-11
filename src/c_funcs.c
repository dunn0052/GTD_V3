// compile with cc -o c_collision.so -shared -fPIC c_collision.c

#include <stdio.h>

#define TRUE 1
#define FALSE 0

struct C_POINT
{
    int x;
    int y;
};


struct C_RECT
{
    struct C_POINT upper_left;
    struct C_POINT lower_right;
};

typedef struct C_POINT C_POINT;
typedef struct C_RECT C_RECT;

// If one rectangle is on left side of other or if one rectangle is above other
int rectangle_collide(int c_top, int c_left, int c_down, int c_right, int o_top, int o_left, int o_down, int o_right)
{
    return  !(c_left >= o_right || o_left >= c_right || c_top >= o_down || o_top >= c_down);
}

int collide_group(int c_top, int c_left, int c_down, int c_right, int group[], int length)
{
    int i = 0;
    for(i = 0; i < length; i += 4)
    {
        if( rectangle_collide(c_top, c_left, c_down, c_right, group[i], group[i+1], group[i+2], group[i+3]) )
        {
            return i>>2;
        }
    }
    return -1;
}

int any_collide_group(int c_top, int c_left, int c_down, int c_right, int group[], int length)
{
    int i = 0;
    for(i = 0; i < length; i += 4)
    {
        if( rectangle_collide(c_top, c_left, c_down, c_right, group[i], group[i+1], group[i+2], group[i+3]) )
        {
            return TRUE;
        }
    }
    return FALSE;
}

int collide_rect(C_RECT caller, C_RECT other)
{   

    //printf("\nCaller.upper_left.x: %i\nOther.lower_right.x: %i", caller.upper_left.x, other.lower_right.x);
    return (caller.upper_left.x < other.lower_right.x && 
             caller.lower_right.x > other.upper_left.x && 
             caller.upper_left.y > other.lower_right.y && 
             caller.lower_right.y < other.upper_left.y);
}

int collide_rects(C_RECT caller, C_RECT others[], int length)
{
    int i = 0;
    for(i = 0; i < length; i++)
    {
        if( collide_rect(caller, others[i]) )
        {
            //printf("Hit sprite: %i\n", i);
            return i;
        }
    }
    // return an out of bounds index
    return -1;
}

void update_points(int x, int y, C_POINT group[], int length)
{
    int i = 0;
    for(i = 0; i < length; i++)
    {
        group[i].x = group[i].x + x;
        group[i].y = group[i].y + y;
    }
}

void update_group_coords(int x, int y, int draw_coords[][8], int length)
{
    int i = 0;
    for(i = 0; i < length; i++)
    {
        draw_coords[i][0] = draw_coords[i][0] + x;
        draw_coords[i][1] = draw_coords[i][1] + y;
        draw_coords[i][2] = draw_coords[i][2] + x;
        draw_coords[i][3] = draw_coords[i][3] + y;
        draw_coords[i][4] = draw_coords[i][4] + x;
        draw_coords[i][5] = draw_coords[i][5] + y;
        draw_coords[i][6] = draw_coords[i][6] + x;
        draw_coords[i][7] = draw_coords[i][7] + y;
    }
}