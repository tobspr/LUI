// Filename: luiExpression.h
// Created by:  tobspr (31Jan16)
//

#ifndef LUI_EXPRESSION_H
#define LUI_EXPRESSION_H

#include "config_lui.h"
#include "pandabase.h"

NotifyCategoryDecl(luiExpression, EXPCL_LUI, EXPTP_LUI);

class EXPCL_LUI LUIExpression {
public:
  enum ExpressionType {
      ET_none, // No type
      ET_scalar, // Simple scalar, like 10, in pixels
      ET_percentage, // Percentage value, like 20%
  };

  LUIExpression();
  void load_expression(float scalar);
  void load_expression(const string& str);
  void clear();
  float evaluate(float max_constraint) const;

  INLINE bool has_expression() const;
  INLINE bool has_fixed_expression() const;
  INLINE bool has_parent_dependent_expression() const;

private:
  ExpressionType _type;
  float _value;
};

inline ostream& operator<<(ostream& stream, LUIExpression::ExpressionType ty) {
  switch(ty) {
    case LUIExpression::ET_none:        return stream << "ET_none";
    case LUIExpression::ET_scalar:      return stream << "ET_scalar";
    case LUIExpression::ET_percentage:  return stream << "ET_percentage";
  }
  return stream << "(Invalid Expression Type)";
}

#include "luiExpression.I"

#endif
