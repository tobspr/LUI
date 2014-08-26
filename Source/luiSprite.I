

INLINE void LUISprite::set_pos(const LPoint2 &pos) {
    _pos = pos;
}

INLINE const LPoint2 &LUISprite::get_pos() const {
    return _pos;
}

INLINE void LUISprite::set_size(const LVector2 &size) {
    _size = size;
}

INLINE const LVector2 &LUISprite::get_size() const {
    return _size;
}

INLINE void LUISprite::set_texcoord_start(const LVector2 &texcoord_start) {
    _texcoord_start = texcoord_start;
}

INLINE const LVector2 &LUISprite::get_texcoord_start() const {
    return _texcoord_start;
}
		
INLINE void LUISprite::set_texcoord_end(const LVector2 &texcoord_end) {
    _texcoord_end = texcoord_end;
}

INLINE const LVector2 &LUISprite::get_texcoord_end() const {
    return _texcoord_end;
}
		
INLINE void LUISprite::set_color(const LColor &color) {
    _color = color;
}

INLINE const LColor &LUISprite::get_color() const {
    return _color;
}

INLINE void LUISprite::set_texture(Texture* tex) {
    _tex = tex;
}

INLINE Texture* LUISprite::get_texture() const {
    return _tex;
}

INLINE void LUISprite::set_z_index(float z_index) {
    _z_index = z_index;
}

INLINE float LUISprite::get_z_index() {
    return _z_index;
}
		
INLINE void LUISprite::set_visible(bool visible) {
    _visible = visible;
}

INLINE bool LUISprite::is_visible() {
    return _visible;
}

INLINE void LUISprite::hide() {
    set_visible(false);
}

INLINE void LUISprite::show() {
    set_visible(true);
}