
#include "luiVerticalLayout.h"

TypeHandle LUIVerticalLayout::_type_handle;
NotifyCategoryDef(luiVerticalLayout, ":lui");


LUIVerticalLayout::LUIVerticalLayout(PyObject* self, LUIObject* parent, float spacing)
: LUIBaseLayout(self) {
    set_spacing(spacing);
    set_parent(parent);
}

void LUIVerticalLayout::init_container(LUIObject* container) {
}

float LUIVerticalLayout::get_metric(LUIBaseElement* element) {
    return element->get_height();
}

void LUIVerticalLayout::set_metric(LUIBaseElement* element, float metric) {
    element->set_height(metric);
}

void LUIVerticalLayout::set_offset(LUIBaseElement* element, float offset) {
    element->set_top(offset);
}

bool LUIVerticalLayout::has_space(LUIBaseElement* element) {
  return element->has_width();
}

void LUIVerticalLayout::set_full_metric(LUIBaseElement* element) {
  element->set_width("100%");
}

void LUIVerticalLayout::clear_metric(LUIBaseElement* element) {
  element->clear_width();
}
