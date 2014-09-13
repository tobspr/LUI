
#include "luiAtlasDescriptor.h"


int LUIAtlasDescriptor::_instance_count = 0;

LUIAtlasDescriptor::LUIAtlasDescriptor() {
  _instance_count ++;

  if (lui_cat.is_spam()) {
    cout << "Constructed a new atlas descriptor (active: " << _instance_count << ")" << endl;
  }
}

LUIAtlasDescriptor::~LUIAtlasDescriptor() {
  _instance_count --;

  if (lui_cat.is_spam()) {
    cout << "Destructed an atlas descriptor (left: " << _instance_count << ")" << endl;
  }
}

