
INLINE LUIRegion* LUIRegion::
  make(const string& context_name, GraphicsOutput *window) {
    return make(context_name, window, LVecBase4(0.0f, 1.0f, 0.0f, 1.0f));
}


INLINE LUIRegion* LUIRegion::
  make(const string& context_name, GraphicsOutput* window,
  const LVecBase4& dimensions) {
    return new LUIRegion(window, dimensions, context_name);
}

INLINE LUIObject* LUIRegion::get_root() const {
  return _lui_root->node();
}

INLINE void LUIRegion::set_input_handler(LUIInputHandler* handler) {
  _input_handler = handler;
}

INLINE LUIInputHandler* LUIRegion::get_input_handler() const {
  return _input_handler;
}


INLINE void LUIRegion::set_render_wireframe(bool wireframe) {
  _wireframe = wireframe;
}

INLINE void LUIRegion::toggle_render_wireframe() {
  set_render_wireframe(!_wireframe);
}
