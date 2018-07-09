

#include "luiRegion.h"


#include "graphicsOutput.h"
#include "graphicsEngine.h"


TypeHandle LUIRegion::_type_handle;

LUIRegion::
  LUIRegion(GraphicsOutput* window, const LVecBase4& dr_dimensions,
  const string& context_name) :
  DisplayRegion(window, dr_dimensions),
  _input_handler(nullptr),
  _wireframe(false) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Constructing new LUIRegion .." << endl;
  }

  int pl, pr, pb, pt;
  get_pixels(pl, pr, pb, pt);
  _width = pr - pl;
  _height = pt - pb;

  _lens = new OrthographicLens();
  _lens->set_film_size(_width, -_height);
  _lens->set_film_offset(_width * 0.5, _height * 0.5);
  _lens->set_near_far(-1e6, 1e6);

  _lui_root = new LUIRoot(_width, _height);
  _empty_tex = new Texture();
  _object_shader = _lui_root->create_object_shader();
  set_camera(NodePath(new Camera(context_name, _lens)));
  set_clear_depth_active(false);
}

LUIRegion::~LUIRegion() {
}

void LUIRegion::
  do_cull(CullHandler* cull_handler, SceneSetup* scene_setup,
  GraphicsStateGuardian* gsg, Thread* current_thread) {
    PStatTimer timer(get_cull_region_pcollector(), current_thread);

    int pl, pr, pb, pt;
    get_pixels(pl, pr, pb, pt);
    int width = pr - pl;
    int height = pt - pb;

    if (width != _width || height != _height) {
      _width = width;
      _height = height;
      _lui_root->node()->set_size(_width, _height);
      _lens->set_film_size(_width, -_height);
      _lens->set_film_offset(_width * 0.5, _height * 0.5);
    }

    if (_input_handler != nullptr) {
      _input_handler->process(_lui_root);
    }

    CullTraverser* trav = get_cull_traverser();

    trav->set_cull_handler(cull_handler);
    trav->set_scene(scene_setup, gsg, get_incomplete_render());
    trav->set_view_frustum(nullptr);

    CPT(RenderAttrib) shaderAttrib = ShaderAttrib::make_default();

    for (int i = 0; i < 8; i++) {
      std::stringstream sstm;
      sstm << "lui_texture_" << i;
      if (i < _lui_root->get_num_textures()) {
          shaderAttrib = DCAST(ShaderAttrib, shaderAttrib)->set_shader_input(
            InternalName::make(sstm.str()), _lui_root->get_texture(i) );
      } else {
          shaderAttrib = DCAST(ShaderAttrib, shaderAttrib)->set_shader_input(
            InternalName::make(sstm.str()), _empty_tex);
      }

    }

    shaderAttrib = DCAST(ShaderAttrib, shaderAttrib)->set_shader(_object_shader);

    CPT(RenderState) state = RenderState::make(
      // CullBinAttrib::make("unsorted", 0),
      DepthTestAttrib::make(RenderAttrib::M_none),
      DepthWriteAttrib::make(DepthWriteAttrib::M_off),
      TransparencyAttrib::make(TransparencyAttrib::M_alpha),
      shaderAttrib
    );

    if (_wireframe) {
      state = state->set_attrib(RenderModeAttrib::make(RenderModeAttrib::M_wireframe));
    }

    CPT(TransformState) net_transform = trav->get_world_transform();
    CPT(TransformState) modelview_transform = trav->get_world_transform()->compose(net_transform);
    CPT(TransformState) internal_transform = trav->get_scene()->get_cs_transform()->compose(modelview_transform);

    _lui_root->prepare_render();

    Geom* geom = _lui_root->get_geom();

    CullableObject* object = new CullableObject(geom, state, internal_transform);
    trav->get_cull_handler()->record_object(object, trav);

    trav->end_traverse();
}

