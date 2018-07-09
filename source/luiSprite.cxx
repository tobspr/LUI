

#include "luiSprite.h"
#include "luiRoot.h"

// ROUND_MARGIN introduced to correct a rounding error on Radeon HD 2400 PRO (black lines between adjacent sprites)
#define ROUND_MARGIN 0.0001

int LUISprite::_instance_count = 0;
TypeHandle LUISprite::_type_handle;

NotifyCategoryDef(luiSprite, ":lui");

LUISprite::LUISprite(LUIText* parent_text)
  : LUIBaseElement(nullptr) {
  init((LUIObject*)parent_text, 0, 0, LColor(1));
  set_texture(nullptr, true);
}


// Initialize with a path to an image
LUISprite::LUISprite(PyObject* self, LUIObject* parent, const string& image,
                     float x, float y, float w, float h, const LColor& color)
  : LUIBaseElement(self) {
  init(parent, x, y, color);
  set_texture(image, true);
  init_size(w, h);
}

// Initialize with a texture handle
LUISprite::LUISprite(PyObject* self, LUIObject* parent, Texture* texture,
                     float x, float y, float w, float h, const LColor& color)
  : LUIBaseElement(self) {
  init(parent, x, y, color);
  set_texture(texture, true);
  init_size(w, h);
}

// Initialize with a atlas entry
LUISprite::LUISprite(PyObject* self, LUIObject* parent, const string& entry_id,
                     const string& atlas_id, float x, float y, float w, float h, const LColor& color)
  : LUIBaseElement(self) {
  init(parent, x, y, color);
  set_texture(entry_id, atlas_id, true);
  init_size(w, h);
}

void LUISprite::init(LUIObject* parent, float x, float y, const LColor& color) {

  // A lui sprite always needs a parent
  nassertv(parent != nullptr);


  _last_frame_visible = -1;
  _texture_index = -1;
  _sprite_index = -1;
  _instance_count ++;

  if (luiSprite_cat.is_spam()) {
    luiSprite_cat.spam() << "Constructed new LUISprite, (active: " << _instance_count << ")" << endl;
  }

  set_color(color);
  set_uv_range(0, 0, 1, 1);
  set_size(1, 1);
  set_pos(x, y);
  parent->add_child(this);
}

LUISprite::~LUISprite() {
  if (luiSprite_cat.is_spam()) {
    _instance_count --;
    luiSprite_cat.spam() << "Destructing LUISprite, instances left: " << _instance_count << endl;
  }

  unassign_sprite_index();
}


void LUISprite::ls(int indent) {
  cout << string(indent, ' ')  << "[LUISprite] pos = "
      << get_abs_pos().get_x() << ", " << get_abs_pos().get_y()
      << "; size = " << get_width() << " x " << get_height()
      << "; tex = " << _debug_source
      << "; z = " << _z_offset << endl;
}


void LUISprite::set_root(LUIRoot* root) {

  if (luiSprite_cat.is_spam()) {
    luiSprite_cat.spam() << "Root changed to " << root << " .." << endl;
  }

  if (_root != nullptr && _root != root) {
    luiSprite_cat.warning() << "Unregistering from old LUIRoot .. you should detach the sprite from the old root first .." << endl;
    unassign_sprite_index();
  }

  if (_root != root) {

    // Unregister from old root
    unregister_events();
    _root = root;

    // Register to new root
    register_events();
    assign_sprite_index();
  }

}

void LUISprite::assign_sprite_index() {

  // This should never happen, as all methods which call this method
  // should check if the root is already set. Otherwise something
  // went really wrong.
  nassertv(_root != nullptr);

  _sprite_index = _root->register_sprite(this);

  fetch_texture_index();

  if (luiSprite_cat.is_spam()) {
    luiSprite_cat.spam() << "Got sprite index: " << _sprite_index << " and texture index: " << _texture_index << endl;
  }

}

void LUISprite::update_vertex_pool() {
  if (_sprite_index >= 0 && _root != nullptr) {

    if (luiSprite_cat.is_spam()) {
      luiSprite_cat.spam() << "Updating vertex pool slot " << _sprite_index << endl;
    }

    void* write_pointer = _root->get_sprite_vertex_pointer(_sprite_index);

    // This should never happen
    nassertv(write_pointer != nullptr);

    if (luiSprite_cat.is_spam()) {
      luiSprite_cat.spam() << "Memcopying to " << write_pointer << endl;
    }

    memcpy(write_pointer, &_data, sizeof(LUIVertexData) * 4);
  }
}


void LUISprite::unassign_sprite_index() {
  if (luiSprite_cat.is_spam()) {
    luiSprite_cat.spam() << "Unassign vertex pool" << endl;
  }

  if (_sprite_index >= 0 && _root != nullptr) {
    _root->unregister_sprite(_sprite_index);
    _sprite_index = -1;
  }

  _texture_index = -1;
}

void LUISprite::recompute_vertices() {

  /*

  TODO: Use LVector2 to simplify the calculations

  */

  // Get current position
  float x1 = _abs_position.get_x();
  float y1 = _abs_position.get_y();
  float x2 = x1 + _effective_size.get_x();
  float y2 = y1 + _effective_size.get_y();

  // Get bounds
  float bnds_x1 = _abs_clip_bounds.get_x();
  float bnds_y1 = _abs_clip_bounds.get_y();
  float bnds_x2 = bnds_x1 + _abs_clip_bounds.get_w();
  float bnds_y2 = bnds_y1 + _abs_clip_bounds.get_h();

  // Clip position to bounds
  float nx1 = min(bnds_x2, max(bnds_x1, x1));
  float ny1 = min(bnds_y2, max(bnds_y1, y1));
  float nx2 = min(bnds_x2, max(bnds_x1, x2));
  float ny2 = min(bnds_y2, max(bnds_y1, y2));

  // Get current texcoord
  float u1 = _uv_begin.get_x() + ROUND_MARGIN;
  float v1 = _uv_begin.get_y() + ROUND_MARGIN;
  float u2 = _uv_end.get_x() - ROUND_MARGIN;
  float v2 = _uv_end.get_y() - ROUND_MARGIN;

  // Compute texcoord-per-pixel factor
  float upp = 0, vpp = 0;

  if (x2 - x1 != 0) {
    upp = (u2 - u1) / (x2 - x1);
  }

  if (y2 - y1 != 0) {
    vpp = (v2 - v1) / (y2 - y1);
  }

  // Adjust texcoord (clipping)
  u1 += (nx1 - x1) * upp;
  u2 += (nx2 - x2) * upp;
  v1 += (ny1 - y1) * vpp;
  v2 += (ny2 - y2) * vpp;

  // Update vertex positions
  _data[0].x = nx1;
  _data[0].z = ny1;
  _data[1].x = nx2;
  _data[1].z = ny1;
  _data[2].x = nx2;
  _data[2].z = ny2;
  _data[3].x = nx1;
  _data[3].z = ny2;

  // Update vertex texcoords
  _data[0].u = u1;
  _data[0].v = 1-v1;
  _data[1].u = u2;
  _data[1].v = 1-v1;
  _data[2].u = u2;
  _data[2].v = 1-v2;
  _data[3].u = u1;
  _data[3].v = 1-v2;

  for (int i = 0; i < 4; i++) {
    _data[i].texindex = _texture_index;
    _data[i].y = 0;
  }

  for (int i = 0; i < 4; i++) {
    _data[i].color[0] = (unsigned char) (_composed_color.get_x() * 255.0);
    _data[i].color[1] = (unsigned char) (_composed_color.get_y() * 255.0);
    _data[i].color[2] = (unsigned char) (_composed_color.get_z() * 255.0);
    _data[i].color[3] = (unsigned char) (_composed_color.get_w() * 255.0);
  }
}

void LUISprite::fetch_texture_index() {
  if (_tex != nullptr) {
    _texture_index = _root->alloc_index_by_texture(_tex);
  }
}

void LUISprite::render_recursive(bool is_topmost_pass, bool render_anyway) {

  if (!_visible) return;

  bool do_render = render_anyway || is_topmost_pass == _topmost;
  if (!do_render) return;

  _last_render_index = -1;

  // We should have a root
  nassertv(_root != nullptr);
  // We also should have a index
  nassertv(_sprite_index >= 0);

  fetch_render_index();
  recompute_vertices();
  update_vertex_pool();

  _last_frame_visible  = _root->get_frame_index();
  _root->add_sprite_to_render_list(_sprite_index);
}
