
INLINE LUIRegion *LUIRegion::
  make(const string &context_name, GraphicsOutput *window) {
    return make(context_name, window, LVecBase4(0.0f, 1.0f, 0.0f, 1.0f));
}


INLINE LUIRegion *LUIRegion::
  make(const string &context_name, GraphicsOutput *window,
  const LVecBase4 &dimensions) {
    cout << "Constructing new LUI Region .." << endl;
    return new LUIRegion(window, dimensions, context_name);
}

INLINE LUIObject *LUIRegion::root() {
  return _lui_root->node();
}