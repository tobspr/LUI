
#include "luiText.h"


LUIText::LUIText(float x, float y) : LUIObject(x, y) {
  _text = "";
  _font_size = 100.0;
  set_font("default");
}

LUIText::LUIText(LUIObject *parent, float x, float y) : LUIObject(parent, x, y) {
  _text = "";
  _font_size = 100.0;
  set_font("default");
}

LUIText::LUIText(LUIObject *parent, const string &text, const string &font_name, float x, float y) 
  : LUIObject(parent, x, y)  {
  _text = text;
  _font_size = 100.0;
  set_font(font_name);
}


LUIText::~LUIText() {

}


void LUIText::update_text() {
  int len = _text.size();

  nassertv(_font != NULL);

  if (lui_cat.is_spam()) {
    cout << "Current text is '" << _text.c_str() << "'" << endl; 
  }

  // Remove all sprites which aren't required
  while (_sprites.size() > len) {
    if (lui_cat.is_spam()) {
      cout << "Removing sprite .. " << endl;
    }
    remove_sprite(*_sprites.begin());
  }

  // Allocate as many sprites as required
  int to_allocate  = len - _sprites.size();
  //cout << "Allocating " << to_allocate << " Sprites" << endl;
  for (int i = 0; i < to_allocate; i++) {
    attach_sprite((Texture*)NULL);
  }

  // Pixels per unit, used to convert betweeen coordinate spaces
  float ppu = _font_size;

  // Unreference all current glyphs
  for (int i = 0; i < _glyphs.size(); i++) {
    _glyphs[i]->_geom_count --;
  }
  _glyphs.clear();

  // Iterate over the sprites
  pset<PT(LUISprite)>::iterator it;
  int i = 0;
  float current_x_pos = 0.0;

  for (it = _sprites.begin(); it != _sprites.end(); ++it, i++)
  {
    LUISprite* sprite = *it;
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
    
    // Move *cursor* by glyph length
    current_x_pos += dynamic_glyph->get_advance() * ppu;
  }

  // Finally, set the size
  set_size(current_x_pos, _font_size);

}