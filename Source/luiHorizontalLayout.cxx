
#include "luiHorizontalLayout.h"

TypeHandle LUIHorizontalLayout::_type_handle;
NotifyCategoryDef(luiHorizontalLayout, ":lui");


LUIHorizontalLayout::LUIHorizontalLayout(PyObject* self, LUIObject* parent, float spacing)
: LUIBaseLayout(self) {
    set_spacing(spacing);
    set_parent(parent);
}

void LUIHorizontalLayout::init_container(LUIObject* container) {
}

float LUIHorizontalLayout::get_metric(LUIBaseElement* element) {
    return element->get_width();
}

void LUIHorizontalLayout::set_metric(LUIBaseElement* element, float metric) {
    element->set_width(metric);
}

void LUIHorizontalLayout::set_offset(LUIBaseElement* element, float offset) {
    element->set_left(offset);

    // Since we are in the downstream pass when performing this, our children
    // won't get the update right in time, so make sure they get it.
    // element->move_by(LVector2(offset, 0));
}

bool LUIHorizontalLayout::has_space(LUIBaseElement* element) {
  return element->has_height();
}

void LUIHorizontalLayout::set_full_metric(LUIBaseElement* element) {
  element->set_height("100%");
}

void LUIHorizontalLayout::clear_metric(LUIBaseElement* element) {
  element->clear_height();
}
