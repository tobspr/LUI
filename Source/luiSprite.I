

void LUISprite::set_pos(const LPoint2 &pos) {
    _pos = pos;
}

LPoint2 &LUISprite::get_pos() const {
    return _pos;
}

void LUISprite::set_size(const LVector2 &size) {
    _size = size;
}

LVector2 &LUISprite::get_size() const {
    return _size;
}

void LUISprite::set_texcoord_start(const LVector2 &texcoord_start) {
    _texcoord_start = texcoord_start;
}

LVector2 &LUISprite::get_texcoord_start() const {
    return _texcoord_start;
}
		
void LUISprite::set_texcoord_end(const LVector2 &texcoord_end) {
    _texcoord_end = texcoord_end;
}

LVector2 &LUISprite::get_texcoord_end() const {
    return _texcoord_end;
}
		
void LUISprite::set_color(const LVecBase4f &color) {
    _color = color;
}

LVecBase4f &LUISprite::get_color() const {
    return _color;
}

void LUISprite::set_texture(Texture* tex) {
    _tex = tex;
}

Texture* LUISprite::get_texture() const {
    return _tex;
}

void LUISprite::set_z_index(float z_index) {
    _z_index = z_index;
}

float LUISprite::get_z_index() {
    return _z_index;
}
		
void LUISprite::set_visible(bool visible) {
    _visible = visible;
}
bool LUISprite::is_visible() {
    return _visible;
}

void LUISprite::hide() {
    set_visible(false);
}

void LUISprite::show() {
    set_visible(true);
}