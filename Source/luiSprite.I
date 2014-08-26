

void LUISprite::set_pos(const LPoint2 &pos) {
    _pos = pos;
}

const LPoint2 &LUISprite::get_pos() {
    return _pos;
}

void LUISprite::set_size(const LVector2 &size) {
    _size = size;
}

const LVector2 &LUISprite::get_size() {
    return _size;
}

void LUISprite::set_texcoord_start(const LVector2 &texcoord_start) {
    _texcoord_start = texcoord_start;
}

const LVector2 &LUISprite::get_texcoord_start() {
    return _texcoord_start;
}
		
void LUISprite::set_texcoord_end(const LVector2 &texcoord_end) {
    _texcoord_end = texcoord_end;
}

const LVector2 &LUISprite::get_texcoord_end() {
    return _texcoord_end;
}
		
void LUISprite::set_color(const LVecBase4f &color) {
    _color = color;
}
const LVecBase4f &LUISprite::get_color() {
    return _color;
}

void LUISprite::set_texture(Texture* tex) {
    _tex = tex;
}

Texture* LUISprite::get_texture() {
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