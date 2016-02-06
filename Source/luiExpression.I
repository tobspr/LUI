
INLINE bool LUIExpression::has_expression() const {
    return _type != ET_none;
}

INLINE bool LUIExpression::has_fixed_expression() const {
    return _type == ET_scalar;
}
