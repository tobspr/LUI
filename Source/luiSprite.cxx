

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
    luiSprite_cat.spam() <<  _debug_name << "Constructed new LUISprite, (active: " << _instance_count << ")" << endl;  
  }

  // Prevent recomputation of the position while we initialize the sprite
  begin_update_section();

  set_color(color);
  set_uv_range(LVector2(0), LVector2(1));
  set_size(1, 1);
  set_pos(x, y); 
  set_z_offset(0);
  end_update_section();

  parent->add_child(this);

}

LUISprite::~LUISprite() {
  if (luiSprite_cat.is_spam()) {
    _instance_count --;
    luiSprite_cat.spam() <<  _debug_name << "Destructing LUISprite, instances left: " << _instance_count << endl;
  }

  if (_chunk_descriptor != NULL) {
    luiSprite_cat.spam() <<  _debug_name << "Released chunk descriptor, as sprite did not get detached" << endl;
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
    luiSprite_cat.spam() <<  _debug_name << "Root changed .." << endl;
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
    luiSprite_cat.spam() <<  _debug_name << "Got vertex pool location: " << pool << endl;
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
    luiSprite_cat.spam() <<  _debug_name << "Got chunk " << _chunk_descriptor->get_chunk() << ", slot = " << _chunk_descriptor->get_slot() << endl;
  }

  update_vertex_pool();

}

void LUISprite::update_vertex_pool() {
  if (_chunk_descriptor != NULL && _root != NULL && !_in_update_section) {
    
    // This should never happen, but it's good to check
    nassertv(_chunk_descriptor->get_chunk() != NULL);

    if (luiSprite_cat.is_spam()) {
      luiSprite_cat.spam() <<  _debug_name << "Updating vertex pool slot " << _chunk_descriptor->get_slot() << " in pool " << _chunk_descriptor->get_chunk() << endl;
    }

    void* write_pointer = _chunk_descriptor->get_write_ptr();

    // This also should never happen
    nassertv(write_pointer != NULL);

    memcpy(write_pointer, &_data, sizeof(LUIVertexData) * 4);
  }
}

void LUISprite::unassign_vertex_pool() {
  if (luiSprite_cat.is_spam()) {
    luiSprite_cat.spam() <<  _debug_name << "Unassign vertex pool" << endl;
  }

  if (_chunk_descriptor != NULL) {
    _chunk_descriptor->release();
    delete _chunk_descriptor;
    _chunk_descriptor = NULL;
  }
}
