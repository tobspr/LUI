

#include "luiSprite.h"
#include "luiRoot.h"

int LUISprite::_instance_count = 0;
TypeHandle LUISprite::_type_handle;


NotifyCategoryDef(luiSprite, ":lui");

// Initialize with a path to an image  
LUISprite::LUISprite(PyObject *self, LUIObject* parent, const string &image, float x, float y, float w, float h, const LColor &color) : LUIBaseElement(self) {
  init(parent, x, y, color);
  set_texture(image, true);
  init_size(w, h);
}

// Initialize with a texture handle
LUISprite::LUISprite(PyObject *self, LUIObject* parent, Texture *texture, float x, float y, float w, float h, const LColor &color) : LUIBaseElement(self) {
  init(parent, x, y, color);
  set_texture(texture, true);
  init_size(w, h);
}

// Initialize with a atlas entry
LUISprite::LUISprite(PyObject *self, LUIObject* parent, const string &entry_id, const string &atlas_id, float x, float y, float w, float h, const LColor &color) : LUIBaseElement(self) {
  init(parent, x, y, color);
  set_texture(entry_id, atlas_id, true);
  init_size(w, h);
}




void LUISprite::init(LUIObject *parent, float x, float y, const LColor &color) {

  // A lui sprite always needs a parent
  nassertv(parent != NULL);

  _chunk_descriptor = NULL;
  _instance_count ++;

  if (luiSprite_cat.is_spam()) {
    luiSprite_cat.spam() << "Constructed new LUISprite, (active: " << _instance_count << ")" << endl;  
  }

  // Prevent recomputation of the position while we initialize the sprite
  begin_update_section();

  set_color(color);
  set_uv_range(0, 0, 1, 1);
  set_size(1, 1);
  set_pos(x, y); 
  set_z_offset(0);
  end_update_section();

  parent->add_child(this);

}

LUISprite::~LUISprite() {
  if (luiSprite_cat.is_spam()) {
    _instance_count --;
    luiSprite_cat.spam() << "Destructing LUISprite, instances left: " << _instance_count << endl;
  }

  if (_chunk_descriptor != NULL) {
    luiSprite_cat.spam() << "Released chunk descriptor, as sprite did not get detached" << endl;
    _chunk_descriptor->release();
    delete _chunk_descriptor;
    _chunk_descriptor = NULL;
  }
}


void LUISprite::ls(int indent) {
  cout << string(indent, ' ')  << "[LUISprite] pos = " 
      << _pos_x << ", " << _pos_y 
      << "; size = " << _size.get_x() << " x " << _size.get_y() 
      << "; tex = " << (_tex != NULL ? _tex->get_name() : "none")
      << "; z_index = " << _z_index << " (+ " << _local_z_index << ")";


  if (_chunk_descriptor == NULL) {
    cout << "; no chunk ";
  } else {
    cout << "; chunk = " << _chunk_descriptor ->get_slot();
  }
  cout << endl;
} 


void LUISprite::set_root(LUIRoot* root) {

  if (luiSprite_cat.is_spam()) {
    luiSprite_cat.spam() << "Root changed .." << endl;
  }

  if (_root != NULL && _root != root) {
    luiSprite_cat.warning() << "Unregistering from old LUIRoot .. you should detach the sprite from the old root first .." << endl;
    unassign_vertex_pool();
  }

  if (_root != root) {

    // Unregister from old root
    unregister_events();
    _root = root;

    // Register to new root
    register_events();

    if (_tex != NULL) {
      assign_vertex_pool();
    }
  }  
}

void LUISprite::assign_vertex_pool() {

  // This should never happen, as all methods which call this method
  // should check if the root is already set. Otherwise something
  // went really wrong.
  nassertv(_root != NULL);

  LUIVertexPool* pool = _root->get_vpool_by_texture(_tex);
  
  if (luiSprite_cat.is_spam()) {
    luiSprite_cat.spam() << "Got vertex pool location: " << pool << endl;
  }

  // This might occur sometimes (hopefully not), and means that get_vpool_by_texture
  // could not allocate a vertex pool for some reason. 
  nassertv(pool != NULL);

  // Delete old descriptor first
  if (_chunk_descriptor != NULL) {
    _chunk_descriptor->release();
    delete _chunk_descriptor;
    _chunk_descriptor = NULL;
  }

  _chunk_descriptor = pool->allocate_slot(this);
  if (luiSprite_cat.is_spam()) {
    luiSprite_cat.spam() << "Got chunk " << _chunk_descriptor->get_chunk() << ", slot = " << _chunk_descriptor->get_slot() << endl;
  }

  update_vertex_pool();

}

void LUISprite::update_vertex_pool() {
  if (_chunk_descriptor != NULL && _root != NULL && !_in_update_section) {
    
    // This should never happen, but it's good to check
    nassertv(_chunk_descriptor->get_chunk() != NULL);

    if (luiSprite_cat.is_spam()) {
      luiSprite_cat.spam() << "Updating vertex pool slot " << _chunk_descriptor->get_slot() << " in pool " << _chunk_descriptor->get_chunk() << endl;
    }

    void* write_pointer = _chunk_descriptor->get_write_ptr();

    // This also should never happen
    nassertv(write_pointer != NULL);

    memcpy(write_pointer, &_data, sizeof(LUIVertexData) * 4);
  }
}

void LUISprite::unassign_vertex_pool() {
  if (luiSprite_cat.is_spam()) {
    luiSprite_cat.spam() << "Unassign vertex pool" << endl;
  }

  if (_chunk_descriptor != NULL) {
    _chunk_descriptor->release();
    delete _chunk_descriptor;
    _chunk_descriptor = NULL;
  }
}




void LUISprite::recompute_vertices() {

  // Get current position
  float x1 = _pos_x;
  float y1 = _pos_y;
  float x2 = x1 + _size.get_x();
  float y2 = y1 + _size.get_y();

  // Get bounds
  float bnds_x1 = _abs_clip_bounds->get_x();
  float bnds_y1 = _abs_clip_bounds->get_y();
  float bnds_x2 = bnds_x1 + _abs_clip_bounds->get_w();
  float bnds_y2 = bnds_x2 + _abs_clip_bounds->get_h();

  // Clip position to bounds
  float nx1 = min(bnds_x2, max(bnds_x1, x1));
  float ny1 = min(bnds_y2, max(bnds_y1, y1));
  float nx2 = min(bnds_x2, max(bnds_x1, x2));
  float ny2 = min(bnds_y2, max(bnds_y1, y2));

  // Get current texcoord
  float u1 = _uv_begin.get_x();
  float v1 = _uv_begin.get_y();
  float u2 = _uv_end.get_x();
  float v2 = _uv_end.get_y();
  
  // Compute texcoord-per-pixel factor
  float upp = 0, vpp = 0;

  if (x2 - y1 != 0) {
    upp = (u2 - u1) / (x2 - x1);
  }

  if (y2 - y1 != 0) {
    vpp = (v2 - v1) / (y2 - y1);
  }


  // Adjust texcoord
  u1 += (nx1 - x1) * upp;
  u2 += (nx2 - x2) * upp;
  v1 += (ny1 - y1) * vpp;
  v2 += (ny2 - y2) * vpp;

  if (luiSprite_cat.is_spam()) {
    luiSprite_cat.spam() << "Recomputing, bounds = (" << _abs_clip_bounds->get_x() << ", " 
      << _abs_clip_bounds->get_y() << " / " << _abs_clip_bounds->get_w() << "x" << _abs_clip_bounds->get_h() 
      << "), pos = (" << nx1 << ", " << ny1 << ", " << nx2 << ", " << ny2 << ")"
      << endl;
  }

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
}