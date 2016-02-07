// Filename: luiHorizontalLayout.h
// Created by:  tobspr (31Jan16)
//

#ifndef LUI_HORIZONTAL_LAYOUT_H
#define LUI_HORIZONTAL_LAYOUT_H

#include "config_lui.h"
#include "luiBaseLayout.h"

#include "pandabase.h"
NotifyCategoryDecl(luiHorizontalLayout, EXPCL_LUI, EXPTP_LUI);

class EXPCL_LUI LUIHorizontalLayout : public LUIBaseLayout {

PUBLISHED:
  LUIHorizontalLayout(PyObject* self, LUIObject* parent, float spacing = 0.0);

protected:
  // Interfaces
  void init_container(LUIObject* container);
  float get_metric(LUIBaseElement* element);
  void set_metric(LUIBaseElement* element, float metric);
  void set_offset(LUIBaseElement* element, float offset);
  bool has_space(LUIBaseElement* element);
  void set_full_metric(LUIBaseElement* element);
  void clear_metric(LUIBaseElement* element);


public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    LUIBaseLayout::init_type();
    register_type(_type_handle, "LUIHorizontalLayout", LUIBaseLayout::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;

};

#endif // LUI_HORIZONTAL_LAYOUT_H
