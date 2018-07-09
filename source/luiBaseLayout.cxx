

#include "luiBaseLayout.h"

#include "pstrtod.h"
#include <sstream>

TypeHandle LUIBaseLayout::_type_handle;
NotifyCategoryDef(luiBaseLayout, ":lui");

LUIBaseLayout::LUIBaseLayout(PyObject* self) : LUIObject(self), _spacing(0.0f)
{
}

void LUIBaseLayout::add(PT(LUIBaseElement) object, const string& cell_mode) {
  if (object->has_parent()) {
    luiBaseLayout_cat.error() << "Cannot call add() with an object which already has a parent! Tried to add "
      << object->get_debug_name() << " to " << get_debug_name() << ", current parent is " << object->get_parent()->get_debug_name() << endl;
    return;
  }

  add_cell(object, construct_cell(cell_mode));
}

void LUIBaseLayout::add(PT(LUIBaseElement) object, float cell_height) {
  Cell cell = { CM_fixed, cell_height, nullptr };
  add_cell(object, cell);
}

LUIObject* LUIBaseLayout::add_cell(PT(LUIBaseElement) object, Cell cell) {
  // Construct cell container object
  LUIObject* container = new LUIObject(nullptr);
  add_child(container);
  if (object)
    container->add_child(object);
  container->set_debug_name("LUILayoutCell");
  cell.node = container;
  init_container(container);
  _cells.push_back(cell);
  return container;
}


PT(LUIObject) LUIBaseLayout::cell(const string& cell_mode) {
  return add_cell(nullptr, construct_cell(cell_mode));
}

PT(LUIObject) LUIBaseLayout::cell(float cell_height) {
  Cell cell = { CM_fixed, cell_height, nullptr };
  return add_cell(nullptr, cell);
}

PT(LUIObject) LUIBaseLayout::cell() {
  Cell cell = { CM_fit, 0.0f, nullptr };
  return add_cell(nullptr, cell);
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
  Cell cell = { CM_fit, 0.0f, nullptr };

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

    // Parse payload
    string val = cell_mode.substr(0, cell_mode.size() - 1);
    char* endptr;
    double d_val = pstrtod(val.c_str(), &endptr);

    if (*endptr != 0) {
      luiBaseLayout_cat.error() << "Could not parse float: '" << val << "'" << endl;
      d_val = 0.0;
    }
    cell.payload = (float)(d_val / 100.0);
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


void LUIBaseLayout::update_layout() {
  // First, get available space
  float available = get_metric(this);
  size_t num_fill_cells = 0;
  for (auto it = _cells.begin(); it != _cells.end(); ++it) {
    if ((*it).mode == CM_fill)
      ++num_fill_cells;
    else
      available -= get_metric((*it).node);
  }

  // Take spacing into account
  available -= max(size_t(0), _cells.size() - 1) * _spacing;

  if (available < 0.0f) {
    // luiBaseLayout_cat.warning() << "Not enough space available! (Missing " << -available << " pixels)" << endl;
    available = 0.0;
  }

  // Divide available space by amount of containers that specify the '*' flag
  available /= max(size_t(1), num_fill_cells);
  available = ceil(available);

  // cout << "Available metrics = " << ava%ilable << " (for " << num_fill_cells << " cells)" << endl;

  float this_metric = get_metric(this);
  float offset = 0.0;

  // Iterate over all cells and distribute them
  for (auto it = _cells.begin(); it != _cells.end(); ++it) {
    const Cell& cell = *it;
    set_offset(cell.node, offset);
    switch (cell.mode) {

      // Fixed metric
      case CM_fixed: {
        set_metric(cell.node, cell.payload);
        offset += cell.payload;
        break;
      }

      // Filler cell
      case CM_fill: {
        set_metric(cell.node, available);
        offset += available;
        break;
      }

      // Percentage
      case CM_percentage: {
        float pct_metric = this_metric * cell.payload;
        set_metric(cell.node, pct_metric);
        offset += pct_metric;
        break;
      }

      // Fit
      case CM_fit: {
        float cell_metric = get_metric(cell.node);
        offset += cell_metric;
        break;
      }

      default: {
        // Unkown metric type
        nassertv(false);
      }
    };
    offset += _spacing;
  }
}

void LUIBaseLayout::update_dimensions_upstream() {
  for (auto it = _children.begin(); it!= _children.end(); ++it) {
    (*it)->update_dimensions_upstream();
  }

  update_dimensions();
  update_layout();
  fit_dimensions();
}

void LUIBaseLayout::reset() {
  _cells.clear();
  remove_all_children();
}


void LUIBaseLayout::update_downstream() {

  update_layout();

  bool fill_children = has_space(this);

  for (auto it = _children.begin(); it != _children.end(); ++it) {
    if (fill_children)
      // Layout has either fixed width/height assigned, make all containers resize
      set_full_metric(*it);
    else
      // Layout has no fixed size, fit the children
      clear_metric(*it);
  }

  LUIObject::update_downstream();
}

void LUIBaseLayout::remove_cell(size_t index) {
  nassertv(index < _cells.size());
  PT(LUIBaseElement) cell = _cells[index].node;
  remove_child(cell);
  _cells.erase(_cells.begin() + index);
}
