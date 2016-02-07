
#include "luiAtlasPacker.h"

/**
 * @brief Constructs a new atlas packer
 * @details This constructs a new atlas packer. The size controls the size of the
 *   atlas in pixels.
 *
 * @param size Size of the atlas in pixels
 */
LUIAtlasPacker::LUIAtlasPacker(size_t size) : _size(size) {
  // Allocate memory
  values_bitmask = new bool[_size * _size];
  memset(values_bitmask, 0x0, sizeof(bool) * _size * _size);
}

/**
 * @brief Finds a region in the atlas
 * @details This attempts to find a place for the given dimensions in the atlas.
 *   If a region is found, returns the upper left coordinate of the region in
 *   pixels. If no region was found, (-1, -1) is returned.
 *
 * @param w Width of the region in pixels
 * @param h Height of the region in pixels
 *
 * @return Either coordinate of the region, or (-1, -1) if no free spot was found
 */
LVector2f LUIAtlasPacker::find_position(size_t w, size_t h) {

  // Region exceeds atlas size
  if (w > _size || h > _size)
    return LVector2f(-1, -1);

  size_t search_w = _size - w;
  size_t search_h = _size - h;

  size_t step_size = 1;

  // Less accuracy when the atlas gets bigger
  if (_size >= 4096) step_size = 2;
  if (_size >= 8192) step_size = 4;

  // Iterate over every pixel (brute force)
  for (size_t search_y = 0; search_y <= search_h; search_y += step_size) {
    for (size_t search_x = 0; search_x <= search_w; search_x += step_size) {

      // If the pixel is free
      if (!get_value(search_x, search_y)) {

        // Possible match, check if the given region would fit in there
        bool any_found = false;
        for (size_t offs_x = 0; offs_x < w && !any_found; offs_x ++) {
          for (size_t offs_y = 0; offs_y < h && !any_found; offs_y ++) {
            if (get_value(search_x+offs_x, search_y+offs_y)) {
              any_found = true;
              break;
            }
          }
        }

        // If no pixel in the region was taken, we found a place to store the region
        if (!any_found) {

          // Mark pixels as used
          for (size_t mark_x = 0; mark_x < w; ++mark_x) {
            for (size_t mark_y = 0; mark_y < h; ++mark_y) {
              set_value(search_x + mark_x, search_y + mark_y, true);
            }
          }
          return LVector2f(search_x, search_y);
        }
      }
    }
  }

  return LVector2f(-1, -1);
}

/**
 * @brief Destructor
 * @details Destructs the atlas packer, freeing all used resources
 */
LUIAtlasPacker::~LUIAtlasPacker() {
  delete [] values_bitmask;
}
