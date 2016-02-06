// Filename: luiBaseLayout.h
// Created by:  tobspr (06Feb16)
//

#ifndef LUI_BASE_LAYOUT_H
#define LUI_BASE_LAYOUT_H

#include "config_lui.h"
#include "luiBaseElement.h"
#include "luiObject.h"
#include "pandabase.h"

NotifyCategoryDecl(luiBaseLayout, EXPCL_LUI, EXPTP_LUI);

class EXPCL_LUI LUIBaseLayout : public LUIObject {

public:

    enum CellMode {
        CM_fit,             // Key: '?'
        CM_percentage,      // Key: "xxx%", e.g. "23%"
        CM_fill,            // Key: '*'
        CM_fixed,           // Key: '10' (absolute value)
    };

    LUIBaseLayout(PyObject* self);

    void add(const string& cell_mode, PT(LUIBaseElement) object);

protected:

    struct Cell {
        // Cell mode, determines the cell size
        CellMode mode;

        // Stores stuff like percentage, pixels, content depends on mode
        double payload;

        // Container node
        PT(LUIBaseElement) node;
    };


    Cell construct_cell(const string& cell_mode);
    pvector<Cell> _cells;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    LUIObject::init_type();
    register_type(_type_handle, "LUIBaseLayout", LUIObject::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};



#endif // LUI_BASE_LAYOUT_H
