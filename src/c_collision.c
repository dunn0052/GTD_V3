
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
            return 1;
        }
    }
    return 0;
}