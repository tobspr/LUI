

#include "luiVertexPool.h"

LUIVertexPool::LUIVertexPool(Texture *tex) : 
  _tex(tex), 
  _slots(0),
  _highest_index(-1), 
  _sprite_count(0)
{
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Constructed new LUIVertex pool" << endl;
  }

  CPT(GeomVertexFormat) format = GeomVertexFormat::get_v3c4t2();
  _vertex_data = new GeomVertexData("VertexPool", format, Geom::UH_dynamic);
  _vertex_data->set_num_rows(10);
}

LUIVertexPool::~LUIVertexPool() {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Destructed LUIVertex pool" << endl;
  }
}
