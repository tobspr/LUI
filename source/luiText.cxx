
#include "luiText.h"
#include "pandaVersion.h"

TypeHandle LUIText::_type_handle;

LUIText::LUIText(PyObject* self, LUIObject* parent, const wstring& text,
                 const string& font_name, float font_size, float x, float y, bool wordwrap)
  :
  LUIObject(self, parent, x, y),
  _text(text),
  _font_size(font_size),
  _wordwrap(wordwrap) {
  set_font(font_name);
}

LUIText::~LUIText() {

}

void LUIText::update_text() {
  int len = _text.size();

  nassertv(_font != NULL);

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Current text is '" << _text.c_str() << "'" << endl;
  }

  // Remove all sprites which aren't required
  while (_children.size() > len) {
    if (lui_cat.is_spam()) {
      lui_cat.spam() << "Removing sprite .. " << endl;
    }
    remove_child(*_children.begin());
  }

  // Allocate as many sprites as required
  int to_allocate  = len - _children.size();
  for (int i = 0; i < to_allocate; ++i) {
    if (lui_cat.is_spam()) {
      lui_cat.spam() << "Allocating sprite .. " << endl;
    }
    PT(LUISprite) sprite = new LUISprite(this);

    // Required for smooth text rendering
    sprite->set_snap_position(false);
  }

  // Pixels per unit, used to convert betweeen coordinate spaces
  float ppu = _font_size;
  float line_height = _font->get_line_height();

  // Unreference all current glyphs
  _glyphs.clear();

  // Iterate over the sprites
  int char_idx = 0;
  float current_x_pos = 0.0f;

  for (auto it = _children.begin(); it != _children.end(); ++it, ++char_idx)
  {
    LUIBaseElement* child = *it;
    LUISprite* sprite = DCAST(LUISprite, child);

    // A lui text should have only sprites contained, otherwise something went wrong
    nassertv(sprite != NULL);

    int char_code = (int)_text.at(char_idx);

#if PANDA_MAJOR_VERSION > 1 || PANDA_MINOR_VERSION >= 10
    CPT(TextGlyph) const_glyph;
#else
    const TextGlyph* const_glyph;
#endif
    if (!_font->get_glyph(char_code, const_glyph)) {
      sprite->set_texture((Texture*)NULL);
      lui_cat.error() << "Font does not support character with char code " << char_code << ", ignoring .. target = " << _debug_name << endl;
      continue;
    }

    CPT(DynamicTextGlyph) dynamic_glyph = DCAST(DynamicTextGlyph, const_glyph);

    // If this gets executed, a non-dynamic font got loaded.
    nassertv(dynamic_glyph != NULL);

    _glyphs.push_back(dynamic_glyph);

    // Some characters have no texture (like space)
    if (dynamic_glyph->get_page() == NULL) {
      lui_cat.debug() << "Character '" << (char)char_code << "' (Code: " << char_code << ") has no texture page!" << endl;
      sprite->hide();

    } else {
      sprite->show();

      // LUISprite has a check if the texture is the same, so if the atlas didn't
      // change, this is quite efficient.
      sprite->set_texture(dynamic_glyph->get_page());

      // Position the glyph.
      sprite->set_pos(
        current_x_pos + dynamic_glyph->get_left() * ppu,
        (0.85 - dynamic_glyph->get_top()) * ppu + 1);

      // The V coordinate is inverted, as panda stores the textures flipped
      sprite->set_uv_range(
        dynamic_glyph->get_uv_left(),
        1 - dynamic_glyph->get_uv_top(),
        dynamic_glyph->get_uv_right(),
        1 - dynamic_glyph->get_uv_bottom());

      // Determine size from coordinates
      sprite->set_size(
         (dynamic_glyph->get_right() - dynamic_glyph->get_left()) * ppu,
         (dynamic_glyph->get_top() - dynamic_glyph->get_bottom()) * ppu);

      sprite->set_color(_color);
    }

    // Move *cursor* by glyph length
    current_x_pos += dynamic_glyph->get_advance() * ppu;
  }

  set_size( floor(current_x_pos), floor(line_height * ppu));
}

void LUIText::ls(int indent) {
  cout << string(indent, ' ')  << "[" << _debug_name << "] pos = " << get_abs_pos().get_x() << ", " << get_abs_pos().get_y()
       << "; size = " << get_width() << " x " << get_height() << "; text = u'" << _text << "'; color = "
       << _color << " / " << _composed_color << "; z = " << _z_offset << endl;
}

int LUIText::get_char_index(float pos) const {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Trying to resolve " << pos << " into a character index .." << endl;
  }
  nassertr(_font != NULL, 0);

  float cursor = 0.0f;

  for (int i = 0; i < _text.size(); ++i) {
    int char_code = (int)_text.at(i);

#if PANDA_MAJOR_VERSION > 1 || PANDA_MINOR_VERSION >= 10
    CPT(TextGlyph) glyph;
#else
    const TextGlyph* glyph;
#endif
    if (!_font->get_glyph(char_code, glyph)) {
      lui_cat.error() << "Font does not support character with char code " << char_code << ", ignoring .. target = " << _debug_name << endl;
      continue;
    }

    nassertr(glyph != NULL, 0);
    cursor += glyph->get_advance() * _font_size;

    if (cursor > pos) {
      return i;
    }
  }
  return _text.size();
}

float LUIText::get_char_pos(int char_index) const {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Trying to resolve " << char_index << " into a character position .." << endl;
  }
  nassertr(_font != NULL, 0);

  // Make sure we don't iterate over the text bounds
  int iterate_max = min(char_index, (int)_text.size());

  float cursor = 0.0f;

  for (int i = 0; i < iterate_max; i++) {
    int char_code = (int)_text.at(i);

#if PANDA_MAJOR_VERSION > 1 || PANDA_MINOR_VERSION >= 10
    CPT(TextGlyph) glyph;
#else
    const TextGlyph* glyph;
#endif
    if (!_font->get_glyph(char_code, glyph)) {
      lui_cat.error() << "Font does not support character with char code " << char_code << ", ignoring .. target = " << _debug_name << endl;
      continue;
    }
    nassertr(glyph != NULL, 0);
    cursor += glyph->get_advance() * _font_size;
  }

  return cursor;
}
