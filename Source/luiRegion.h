// Filename: luiRegion.h
// Created by:  tobspr (02Sep14)
//

#ifndef LUI_REGION_H
#define LUI_REGION_H


#include "pandabase.h"
#include "pandasymbols.h"
#include "config_lui.h"
#include "camera.h"
#include "displayRegion.h"
#include "nodePath.h"
#include "pStatTimer.h"
#include "luse.h"
#include "graphicsOutput.h"
#include "luiRoot.h"
#include "luiObject.h"
#include "cullableObject.h"
#include "cullTraverser.h"
#include "cullHandler.h"
#include "orthographicLens.h"
#include "cullBinAttrib.h"
#include "depthTestAttrib.h"
#include "depthWriteAttrib.h"
#include "luiInputHandler.h"

class EXPCL_LUI LUIRegion : public DisplayRegion {

protected:
  LUIRegion(GraphicsOutput* window, const LVecBase4& dimensions,
               const string& context_name);

  virtual void do_cull(CullHandler* cull_handler, SceneSetup* scene_setup,
                       GraphicsStateGuardian* gsg, Thread* current_thread);

PUBLISHED:
  virtual ~LUIRegion();

  INLINE static LUIRegion* make(const string& context_name,
                                   GraphicsOutput* window);
  INLINE static LUIRegion* make(const string& context_name,
                                   GraphicsOutput* window,
                                   const LVecBase4& dimensions);
  INLINE LUIObject* get_root() const;

  MAKE_PROPERTY(root, get_root);

  INLINE void set_input_handler(LUIInputHandler* handler);
  INLINE LUIInputHandler* get_input_handler() const;

  INLINE void set_render_wireframe(bool wireframe);
  INLINE void toggle_render_wireframe();

private:

  PT(OrthographicLens) _lens;
  PT(LUIRoot) _lui_root;
  PT(LUIInputHandler) _input_handler;
  int _width, _height;
  bool _wireframe;

  PT(Shader) _object_shader;
  PT(Texture) _empty_tex;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    DisplayRegion::init_type();
    register_type(_type_handle, "LUIRegion",
                  DisplayRegion::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;

};

#include "luiRegion.I"

#endif
