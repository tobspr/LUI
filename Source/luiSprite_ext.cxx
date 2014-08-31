

#include "luiSprite.h"
#include "luiRoot.h"

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
    cout << "Got vertex pool handle: " << pool << endl;
  }

  // This might occur sometimes (hopefully not), and means that get_vpool_by_texture
  // could not allocate a vertex pool for some reason. VERY BAD.
  nassertv(pool != NULL);

  _vertex_pool = pool;
}

void LUISprite::unassign_vertex_pool() {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "LUISprite:: Unassign vertex pool" << endl;
  }

  if (_vertex_pool != NULL) {
    
  }

}