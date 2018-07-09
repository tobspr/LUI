
#include "luiVertexChunk.h"


LUIVertexChunk::LUIVertexChunk(int chunk_size)
  : _chunk_size(chunk_size), _sprite_count(0) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Constructed new chunk of size " << chunk_size << endl;
  }

  CPT(GeomVertexFormat) format = GeomVertexFormat::get_v3c4t2();
  _vertex_data = new GeomVertexData("VertexPool", format, Geom::UH_dynamic);
  _vertex_data->set_num_rows(chunk_size * 4);

  GeomVertexWriter write_vertex(_vertex_data, "vertex");
  GeomVertexWriter write_texcoord(_vertex_data, "texcoord");
  GeomVertexWriter write_color(_vertex_data, "color");

  for (int i = 0; i < chunk_size*4; i++) {
    write_vertex.add_data3f(0, 0, 0);
    write_color.add_data4f(1,1,1,1);
    write_texcoord.add_data2f(0, 0);
  }

  _triangles = new GeomTriangles(Geom::UH_dynamic);
  _triangles->reserve_num_vertices(chunk_size * 2);

  // Initialize triangles, each sprite emits 4, we use indexing to create 2 tris from that
  for (int i = 0; i < chunk_size; i++) {
    int vtx_index = i * 4;
    // _triangles->add_vertices(vtx_index + 0, vtx_index + 1, vtx_index + 2);
    // _triangles->add_vertices(vtx_index + 0, vtx_index + 2, vtx_index + 3);

    _triangles->add_vertices(vtx_index + 2, vtx_index + 1, vtx_index + 0);
    _triangles->add_vertices(vtx_index + 3, vtx_index + 2, vtx_index + 0);
  }

  _geom = new Geom(_vertex_data);
  _geom->add_primitive(_triangles);

  _write_pointer = _vertex_data->modify_array(0)->modify_handle()->get_write_pointer();

  // Initialize child array
  _children = new LUISprite*[chunk_size];

  for (int i = 0; i < chunk_size; i++) {
    _children[i] = nullptr;
  }

}

LUIVertexChunk::~LUIVertexChunk() {
  // TODO: I probably missed something here
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Destructed vertex chunk" << endl;
  }
  delete [] _children;
}
