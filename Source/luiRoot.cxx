

#include "luiRoot.h"
#include "shader.h"


LUIRoot::LUIRoot(float width, float height) : _requested_focus(NULL) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Constructing new LUIRoot ..\n";
  }
  _root = new LUIObject(NULL, 0.0, 0.0, width, height);
  _root->set_root(this);

  _sprites_rendered = 0;
  _frame_count = 0;
  _render_index = 0;

  // Create vertex chunks
  // CPT(GeomVertexFormat) format = GeomVertexFormat::get_v3c4t2();

  PT(GeomVertexArrayFormat) array_format = new GeomVertexArrayFormat();
  array_format->add_column(InternalName::make("vertex"), 3, Geom::NT_stdfloat, Geom::C_point);
  array_format->add_column(InternalName::make("color"), 4, Geom::NT_uint8, Geom::C_color);
  array_format->add_column(InternalName::make("texcoord"), 2, Geom::NT_stdfloat, Geom::C_texcoord);
  array_format->add_column(InternalName::make("texindex"), 2, Geom::NT_uint8, Geom::C_other);

  _sprite_vertex_pointer = NULL;

  PT(GeomVertexFormat) unregistered_format = new GeomVertexFormat();
  unregistered_format->add_array(array_format);

  CPT(GeomVertexFormat) format = GeomVertexFormat::register_format(unregistered_format);

  _index_buffer_size = 1000000;

  _vertex_data = new GeomVertexData("VertexPool", format, Geom::UH_dynamic);
  _vertex_data->reserve_num_rows(_index_buffer_size);

  _triangles = new GeomTriangles(Geom::UH_dynamic);
  _triangles->set_index_type(GeomEnums::NT_uint32);
  _triangles->make_indexed();

  _geom = new Geom(_vertex_data);
  _geom->add_primitive(_triangles);
  _geom->set_bounds(new OmniBoundingVolume());


  _triangle_index_buffer = new LUITriangleIndex[_index_buffer_size];
}

void LUIRoot::prepare_render() {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "\nPreparing sprite render" << endl;
  }

  PT(GeomVertexArrayDataHandle) array_data_handle = _vertex_data->modify_array(0)->modify_handle();
  _sprite_vertex_pointer = array_data_handle->get_write_pointer();

  _min_rendered_vertex = 999999999;
  _max_rendered_vertex = 0;
  _render_index = 0;
  _frame_count += 1;

  // prepare the geom triangle
  _sprites_rendered = 0;

  _triangles->clear_vertices();
  _triangles->make_indexed();
  _triangles->set_index_type(GeomEnums::NT_uint32);

  // Render normal elements
  _root->render_recursive(false, false);

  // Render topmost elements
  int sprites_before = _sprites_rendered;
  _root->render_recursive(true, false);
  int sprites_topmost = _sprites_rendered - sprites_before;


  if (_sprites_rendered > 0) {
    _triangles->modify_vertices()->unclean_set_num_rows(_sprites_rendered * 2 * 3);

    memcpy(_triangles->modify_vertices()->modify_handle()->get_write_pointer(), _triangle_index_buffer, _sprites_rendered * sizeof(LUITriangleIndex) * 2);

    nassertv(_min_rendered_vertex < _max_rendered_vertex);
    _triangles->set_minmax(_min_rendered_vertex, _max_rendered_vertex, NULL, NULL);
  }

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Rendered " << _triangles->get_num_vertices() << " vertices (" << _sprites_rendered << " Sprites)" << endl;
    lui_cat.spam() << sprites_topmost << " sprites rendered topmost vs " << sprites_before << " normal" << endl;
  }
}


LUIRoot::~LUIRoot() {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Destructed LUIRoot\n";
  }

  // Remove all children first
  _root->remove_all_children();
  _sprites.clear();
  _textures.clear();
}


PT(Shader) LUIRoot::create_object_shader() {
  return Shader::make(Shader::SL_GLSL,
    // Vertex
    "#version 150\n"
    "uniform mat4 p3d_ModelViewProjectionMatrix;\n"
    "in vec4 p3d_Vertex;\n"
    "in uvec2 texindex;\n"
    "in vec4 color;\n"
    "in vec2 p3d_MultiTexCoord0;\n"
    "out vec2 texcoord;\n"
    "flat out uvec2 textureIndex;\n"
    "out vec4 colorScale;\n"
    "void main() {\n"
    "texcoord = p3d_MultiTexCoord0;\n"
    "colorScale = color;\n"
    "textureIndex = texindex;\n"
    "gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;\n"
    "}\n"
    ,
    // Fragment
    "#version 150\n"
    "in vec2 texcoord;\n"
    "flat in uvec2 textureIndex;\n"
    "in vec4 colorScale;\n"
    "uniform sampler2D lui_texture_0;\n"
    "uniform sampler2D lui_texture_1;\n"
    "uniform sampler2D lui_texture_2;\n"
    "uniform sampler2D lui_texture_3;\n"
    "uniform sampler2D lui_texture_4;\n"
    "uniform sampler2D lui_texture_5;\n"
    "uniform sampler2D lui_texture_6;\n"
    "uniform sampler2D lui_texture_7;\n"
    "out vec4 color;\n"
    "void main() {\n"
    "vec4 sampledColor = vec4(0,0,0,1);\n"
    "if (textureIndex.x == 0u) sampledColor = texture(lui_texture_0, texcoord);\n"
    "if (textureIndex.x == 1u) sampledColor = texture(lui_texture_1, texcoord);\n"
    "if (textureIndex.x == 2u) sampledColor = texture(lui_texture_2, texcoord);\n"
    "if (textureIndex.x == 3u) sampledColor = texture(lui_texture_3, texcoord);\n"
    "if (textureIndex.x == 4u) sampledColor = texture(lui_texture_4, texcoord);\n"
    "if (textureIndex.x == 5u) sampledColor = texture(lui_texture_5, texcoord);\n"
    "if (textureIndex.x == 6u) sampledColor = texture(lui_texture_6, texcoord);\n"
    "if (textureIndex.x == 7u) sampledColor = texture(lui_texture_7, texcoord);\n"
    "color = vec4(sampledColor * colorScale);\n"
    "}\n"
    );

}
