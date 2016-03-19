#include "luiExpression.h"

#include "pstrtod.h"


NotifyCategoryDef(luiExpression, ":lui");


LUIExpression::LUIExpression() : _type(ET_none), _value(0.0f) {
}

void LUIExpression::load_expression(float scalar) {
  if (scalar < 0.0f) {
    _type = ET_none;
    _value = 0.0f;
  } else {
    _type = ET_scalar;
    _value = scalar;
  }
}

void LUIExpression::load_expression(const string& str) {
  if (str.size() < 2) {
    luiExpression_cat.error() << "String '" << str << "' is no valid expression!" << endl;
    return;
  }

  if (str.back() != '%') {
    luiExpression_cat.error() << "String '" << str << "' is not a valid percentage!" << endl;
    return;
  }

  string val = str.substr(0, str.size() - 1);

  char* endptr;
  double d_val = pstrtod(val.c_str(), &endptr);

  if (*endptr != 0) {
    luiExpression_cat.error() << "Could not parse float '" << val << "'" << endl;
    return;
  }
  _value = (float)(d_val / 100.0f);
  _type = ET_percentage;
}

float LUIExpression::evaluate(float max_constraint) const {
    // cout << "Evaluating expression, max constraint = " << max_constraint << ", value = " << _value << ", type = " << _type << endl;
  switch(_type) {
    case ET_none:
      return 0;
    case ET_scalar:
      return _value;
    case ET_percentage:
      return _value * max_constraint;
  }
  nassertr(false, 0.0f); // Should never happen
  return -1;
}
