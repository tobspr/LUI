
INLINE bool LUIExpression::has_expression() const {
  return _type != ET_none;
}

INLINE bool LUIExpression::has_fixed_expression() const {
  return _type == ET_scalar;
}

INLINE bool LUIExpression::has_parent_dependent_expression() const {
  return _type == ET_percentage;
}

INLINE void LUIExpression::clear() {
  _type = ET_none;
  _value = 0.0f;
}
