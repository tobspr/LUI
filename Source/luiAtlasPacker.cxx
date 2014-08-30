
#include "luiAtlasPacker.h"

LUIAtlasPacker::LUIAtlasPacker(int size) : _size(size) {
  // Allocate memory
  values_bitmask = new bool*[_size];
  for (int i = 0; i < _size; ++i)
    values_bitmask[i] = new bool[_size];
  
  // Set to zero
  for (int x = 0; x < _size; x++) {
    for (int y = 0; y < _size; y++) {
      values_bitmask[x][y] = false;
    }
  }

}

LVector2 LUIAtlasPacker::find_position(int w, int h) {
  int search_w = _size - w;
  int search_h = _size - h;

  int step_size = 1;

  // Less accuracy when the atlas gets bigger
  if (_size >= 4096) step_size = 2;
  if (_size >= 8192) step_size = 4;


  for (int search_y = 0; search_y < search_h; search_y += step_size) {
    for (int search_x = 0; search_x < search_w; search_x += step_size) {
      if (!values_bitmask[search_x][search_y]) {
        // Possible match
        bool any_found = false;
        for (int offs_x = 0; offs_x < w && !any_found; offs_x ++) {
          for (int offs_y = 0; offs_y < h && !any_found; offs_y ++) {
            if (values_bitmask[search_x+offs_x][search_y+offs_y]) {
              any_found = true;
              break;
            }
          }
        }

        if (!any_found) {
          // Mark pixels as used
          for (int mark_x = 0; mark_x < w; mark_x ++) {
            for (int mark_y = 0; mark_y < h; mark_y ++) {
              values_bitmask[search_x + mark_x][search_y + mark_y] = true;
            }
          }
          return LVector2(search_x, search_y);
        }
      }
    }
  }

  return LVector2(-1, -1);

}

LUIAtlasPacker::~LUIAtlasPacker() {
  // De-Allocate memory to prevent memory leak
  for (int i = 0; i < _size; ++i)
    delete [] values_bitmask[i];
  delete [] values_bitmask;
}