// Filename: luiRegion.h
// Created by:  tobspr (02Sep14)
//

#ifndef LUI_REGION_H
#define LUI_REGION_H

#include "config_lui.h"
#include "displayRegion.h"
#include "pStatTimer.h"
#include "orthographicLens.h"

class EXPCL_PANDASKEL LUIRegion : public DisplayRegion {

protected:
  LUIRegion(GraphicsOutput *window, const LVecBase4 &dimensions,
               const string &context_name);

  virtual void do_cull(CullHandler *cull_handler, SceneSetup *scene_setup,
                       GraphicsStateGuardian *gsg, Thread *current_thread);

PUBLISHED:
  virtual ~LUIRegion();

  INLINE static LUIRegion* make(const string &context_name,
                                   GraphicsOutput *window);
  INLINE static LUIRegion* make(const string &context_name,
                                   GraphicsOutput *window,
                                   const LVecBase4 &dimensions);

  //INLINE void set_input_handler(LUIRegion *handler);
  //INLINE LUIRegion *get_input_handler() const;

private:

  PT(OrthographicLens) _lens;
  //PT(LUIInputHandler) _input_handler;
  LVecBase2i _size;

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