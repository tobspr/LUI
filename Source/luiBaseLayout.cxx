

#include "luiBaseLayout.h"

#include <sstream>

TypeHandle LUIBaseLayout::_type_handle;
NotifyCategoryDef(luiBaseLayout, ":lui");

LUIBaseLayout::LUIBaseLayout(PyObject* self) : LUIObject(self)
{
}

void LUIBaseLayout::add(const string& cell_mode, PT(LUIBaseElement) object) {
    Cell cell = construct_cell(cell_mode);

    // Construct cell container object
    LUIObject* obj = new LUIObject(NULL);
    add_child(obj);
    cell.node = obj;
    _cells.push_back(cell);
}

bool check_int(const string& str) {
    for (auto it = str.begin(); it != str.end(); ++it) {
        if (*it < '0' || *it > '9')
            return false;
    }
    return true;
}

int parse_int(const string& str) {
    // Assumes valid int
    int result = 0;
    istringstream( str ) >> result;
    return result;
}

LUIBaseLayout::Cell LUIBaseLayout::construct_cell(const string& cell_mode) {
    Cell cell = { CM_fit, 0.0, NULL };

    // Fit
    if (cell_mode == "?") {
        cell.mode = CM_fit;
        return cell;
    }

    // Fill
    if (cell_mode == "*") {
        cell.mode = CM_fill;
        return cell;
    }

    // Percentage
    if (cell_mode.back() == '%') {
        cell.mode = CM_percentage;
        // TODO: parse payload
        return cell;
    }

    // Assume pixels otherwise
    if (check_int(cell_mode)) {
        cell.mode = CM_fixed;
        cell.payload = parse_int(cell_mode);
        return cell;
    }

    luiBaseLayout_cat.error() << "Invalid cell mode: '" << cell_mode << "'" << endl;
    return cell;
}
