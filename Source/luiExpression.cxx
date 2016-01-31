#include "luiExpression.h"

#include <stdexcept>

NotifyCategoryDef(luiExpression, ":lui");


LUIExpression::LUIExpression() : _type(ET_none), _value(0.0f) {
}

void LUIExpression::load_expression(float scalar) {
    if (scalar < 0.0) {
        _type = ET_none;
        _value = 0.0;
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
    float float_val = 0.0;

    try {
        float_val = std::stof(val);
    } catch (const std::invalid_argument &e) {
        luiExpression_cat.error() << "Could not parse float '" << val << "': " << e.what() << endl;
        return;
    }

    _value = float_val;
    _type = ET_percentage;
}

float LUIExpression::evaluate(float max_constraint) {
    // cout << "Evaluating expression, max constraint = " << max_constraint << ", value = " << _value << ", type = " << _type << endl;
    switch(_type) {
        case ET_none:
            return 0;
        case ET_scalar:
            return _value;
        case ET_percentage:
            return _value * max_constraint;
    }
    nassertr(false, 0.0); // Should never happen
    return -1;
}

bool LUIExpression::has_expression() const {
    return _type != ET_none;
}
