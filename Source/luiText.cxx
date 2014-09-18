
#include "luiText.h"

TypeHandle LUIText::_type_handle;

LUIText::LUIText(PyObject *self, LUIObject *parent, const string &text, const string &font_name, float font_size, float x, float y) 
  : 
  LUIObject(self, parent, x, y),
  _text(text),
  _font_size(font_size) {
  _snap_position = false;
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
  //lui_cat.spam() << "Allocating " << to_allocate << " Sprites" << endl;
  for (int i = 0; i < to_allocate; i++) {
    if (lui_cat.is_spam()) {
      lui_cat.spam() << "Allocating sprite .. " << endl;
    }
    PT(LUISprite) sprite = new LUISprite(NULL, this, (Texture*)NULL);

    // Required for text rendering
    sprite->set_snap_position(false);
  }



  // Pixels per unit, used to convert betweeen coordinate spaces
  float ppu = _font_size;

  // Unreference all current glyphs
  for (int i = 0; i < _glyphs.size(); i++) {
    _glyphs[i]->_geom_count --;
  }
  _glyphs.clear();

  // Iterate over the sprites
  int i = 0;
  float current_x_pos = 0.0;

  for (lui_element_iterator it = _children.begin(); it != _children.end(); ++it, i++)
  {
    LUIBaseElement* child = *it;

    LUISprite* sprite = DCAST(LUISprite, child);

    // A lui text should have only sprites contained
    nassertv(sprite != NULL);

    int char_code = (int)_text.at(i);

    const TextGlyph *const_glyph;
    if (!_font->get_glyph(char_code, const_glyph)) {
      sprite->set_texture((Texture*)NULL);
      lui_cat.error() << "Could not render character, skipping." << endl;
      continue;
    }

    TextGlyph *glyph = (TextGlyph*) const_glyph;

    PT(DynamicTextGlyph) dynamic_glyph = DCAST(DynamicTextGlyph, glyph);

    // If this gets executed, a non-dynamic font got loaded. 
    nassertv(dynamic_glyph != NULL);

    _glyphs.push_back(dynamic_glyph);
    dynamic_glyph->_geom_count ++;

    sprite->begin_update_section();

    // LUISprite has a check if the texture is the same, so if the atlas didn't
    // change, this is quite efficient.
    sprite->set_texture(dynamic_glyph->get_page());

    // Position the glyph. 
    sprite->set_pos(
      current_x_pos + dynamic_glyph->get_left() * ppu, 
      (_font->get_line_height() * 0.8 - dynamic_glyph->get_top()) * ppu);

    // The V coordinate is inverted, as panda stores the textures flipped
    sprite->set_uv_range(
      dynamic_glyph->get_uv_left(), 
      1-dynamic_glyph->get_uv_top(),
      dynamic_glyph->get_uv_right(), 
      1-dynamic_glyph->get_uv_bottom());

    // Determine size frm coordinates
    sprite->set_size( 
       (dynamic_glyph->get_right() - dynamic_glyph->get_left()) * ppu,
       (dynamic_glyph->get_top() - dynamic_glyph->get_bottom()) * ppu);
    
    sprite->end_update_section();

    // Move *cursor* by glyph length
    current_x_pos += dynamic_glyph->get_advance() * ppu;
  }

  // Finally, set the size
  set_size(current_x_pos, _font_size);

}

void LUIText::ls(int indent) {
  cout << string(indent, ' ')  << "[LUIText] pos = " << _pos_x << ", " << _pos_y << "; text = '" << _text << "'; z-index = " << _z_index << " (+ "<< _local_z_index << ")" << endl;

}