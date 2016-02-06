
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

    // Since we are in the downstream pass when performing this, our children
    // won't get the update right in time, so make sure they get it.
    // element->move_by(LVector2(0, offset));
}
