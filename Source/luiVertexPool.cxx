

#include "luiVertexPool.h"
LUIVertexPool::LUIVertexPool(Texture *tex) : _tex(tex), _slots(0) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Constructed new LUIVertex pool" << endl;
  }

  CPT(GeomVertexFormat) format = GeomVertexFormat::get_v3c4t2();
  _vertex_data = new GeomVertexData("VertexPool", format, Geom::UH_dynamic);
  _vertex_data->set_num_rows(10);
}


INLINE void *LUIVertexPool::get_sprite_pointer(int slot) {
  return _vertex_data->modify_array(0)->modify_handle()->get_write_pointer() + sizeof(LUISprite::LUIVertexData) * 4 * slot;
}

LUIVertexPool::~LUIVertexPool() {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Destructed LUIVertex pool" << endl;
  }
}
