

#include "luiSprite.h"
#include "luiRoot.h"

int LUISprite::_instance_count = 0;


LUISprite::LUISprite(LUIBaseElement* parent) : 
  LUIBaseElement(),
  _chunk_descriptor(NULL)
{  

  _instance_count ++;

  if (lui_cat.is_spam()) {
    cout << "Constructed new LUISprite, (active: " << _instance_count << ")" << endl;  
  }

  set_color(1.0, 1.0, 1.0, 1.0);
  set_parent(parent);
  set_top_left(0, 0); 
  set_uv_range(LVector2(0), LVector2(1));
  set_size(10, 10);
  recompute_z_index();
}

LUISprite::~LUISprite() {
  if (lui_cat.is_spam()) {
    _instance_count --;
    cout << "Destructing LUISprite, instances left: " << _instance_count << endl;
  }

  if (_chunk_descriptor != NULL) {
    lui_cat.spam() << "Released chunk descriptor, as sprite did not get detached" << endl;
    _chunk_descriptor->release();
    delete _chunk_descriptor;
    _chunk_descriptor = NULL;
  }
}

void LUISprite::on_bounds_changed() {
  _data[0].x = _pos_x;
  _data[0].z = _pos_y;
  recompute_vertices();
  update_vertex_pool();
}

void LUISprite::on_visibility_changed() {
  lui_cat.error() << "Todo: Implement hide() / show()" << endl;
}


void LUISprite::on_detached() {
  if (_tex != NULL) {
    unassign_vertex_pool();
  }
  _root = NULL;
  _parent = NULL;
}

void LUISprite::on_z_index_changed() {
  for (int i = 0; i < 4; i++) {
    _data[i].y = -_z_index;
  }
  update_vertex_pool();
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

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "LUISprite - root changed" << endl;
  }

  if (_root != NULL && _root != root) {
    lui_cat.warning() << "Unregistering from old LUIRoot" << endl;
    unassign_vertex_pool();
  }

  if (_root != root) {
    _root = root;

    if (_tex != NULL) {
      if (lui_cat.is_spam()) {
        cout << "Assigning vertex pool from set_root" << endl;
      }
      assign_vertex_pool();
    }

    if (lui_cat.is_spam()) {
      cout << "Root size is: " << _root->node()->get_size().get_x() << endl;
    }
  }
}


void LUISprite::assign_vertex_pool() {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "LUISprite:: Assign vertex pool" << endl;
  }

  // This should never happen, as all methods which call this method
  // should check if the root is already set. Otherwise something
  // went really wrong.
  nassertv(_root != NULL);

  LUIVertexPool* pool = _root->get_vpool_by_texture(_tex);
  
  if (lui_cat.is_spam()) {
    cout << "Vertex pool is at: " << pool << endl;
  }

  // This might occur sometimes (hopefully not), and means that get_vpool_by_texture
  // could not allocate a vertex pool for some reason. VERY BAD.
  nassertv(pool != NULL);

  // Delete old descriptor first
  if (_chunk_descriptor != NULL) {
    _chunk_descriptor->release();
    delete _chunk_descriptor;
    _chunk_descriptor = NULL;
  }

  _chunk_descriptor = pool->allocate_slot(this);
  if (lui_cat.is_spam()) {
    cout << "Got chunk pool " << _chunk_descriptor->get_chunk() << " with slot " << _chunk_descriptor->get_slot() << endl;
  }

  update_vertex_pool();

}

void LUISprite::update_vertex_pool() {
  if (_chunk_descriptor != NULL && _root != NULL) {
    
    // This should never happen, but it's good to check
    nassertv(_chunk_descriptor->get_chunk() != NULL);

    if (lui_cat.is_spam()) {
      cout << "Updating vertex pool , pool slot is " << _chunk_descriptor->get_slot() << " in pool " << _chunk_descriptor->get_chunk() << endl;
    }

    void* write_pointer = _chunk_descriptor->get_write_ptr();
    
    if (lui_cat.is_spam()) {
      cout << "Got vertex pool write pointer at " << write_pointer << endl;
    }

    if (write_pointer == NULL) {
      lui_cat.error() << "Got invalid vertex pool pointer. Ignoring .." << endl;
      return;
    }
    memcpy(write_pointer, &_data, sizeof(LUIVertexData) * 4);
  }
}

void LUISprite::unassign_vertex_pool() {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "LUISprite:: Unassign vertex pool" << endl;
  }

  if (_chunk_descriptor != NULL) {
    _chunk_descriptor->release();
    delete _chunk_descriptor;
    _chunk_descriptor = NULL;
  }
}
