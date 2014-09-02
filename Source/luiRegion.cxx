

#include "luiRegion.h"


#include "graphicsOutput.h"
#include "graphicsEngine.h"


TypeHandle LUIRegion::_type_handle;

LUIRegion::
  LUIRegion(GraphicsOutput *window, const LVecBase4 &dr_dimensions,
  const string &context_name) :
DisplayRegion(window, dr_dimensions) {

  cout << "Constructor called for context '" << context_name << "' .." << endl;
  int pl, pr, pb, pt;
  get_pixels(pl, pr, pb, pt);
  _width = pr - pl;
  _height = pt - pb;

  _lens = new OrthographicLens();
  _lens->set_film_size(_width, -_height);
  _lens->set_film_offset(_width * 0.5, _height * 0.5);
  _lens->set_near_far(-1, 1);


  _lui_root = new LUIRoot(_width, _height);
  //_cam = new Camera(context_name, _lens);

  //NodePath _cam_np(_cam);
  set_camera(new Camera(context_name, _lens));

  cout << "Constructor done!" << endl;
}

LUIRegion::~LUIRegion() {
  cout << "Destructor called" << endl;
}

void LUIRegion::
  do_cull(CullHandler *cull_handler, SceneSetup *scene_setup,
  GraphicsStateGuardian *gsg, Thread *current_thread) {

    cout << "do_cull called" << endl;

    //PStatTimer timer(get_cull_region_pcollector(), current_thread);

    int pl, pr, pb, pt;
    get_pixels(pl, pr, pb, pt);
    int width = pr - pl;
    int height = pt - pb;

    cout << "DO_CULL, with dimensions " << width << "x" << height << endl;

    if (width != _width || height != height) {
      cout << "On resized" << endl;
      _width = width;
      _height = height;
      _lui_root->node()->set_size(_width, _height);
      _lens->set_film_size(_width, -_height);
      _lens->set_film_offset(_width * 0.5, _height * 0.5);
    }

    //if (_input_handler != NULL) {
    //  _input_handler->update_context(_context, pl, pb);
    //} else {
    //  _context->Update();
    //}

    CullTraverser *trav = get_cull_traverser();

    // References!
    for (int i = 0; i < 100; i++) {
      trav->ref();
    }

    trav->set_cull_handler(cull_handler);
    trav->set_scene(scene_setup, gsg, get_incomplete_render());
    trav->set_view_frustum(NULL);

    CPT(RenderState) state = RenderState::make(
      CullBinAttrib::make("unsorted", 0),
      DepthTestAttrib::make(RenderAttrib::M_none),
      DepthWriteAttrib::make(DepthWriteAttrib::M_off)
    );
    CPT(TransformState) net_transform = trav->get_world_transform();


    //CPT(TransformState) modelview_transform = TransformState::make_pos_hpr_scale(LVecBase3(0), LVecBase3(0), LVecBase3(0.01));
    
    CPT(TransformState) modelview_transform = trav->get_world_transform()->compose(net_transform);
    CPT(TransformState) internal_transform = trav->get_scene()->get_cs_transform()->compose(modelview_transform);

    //CPT(TransformState) net_transform = data.get_net_transform(trav);
    //CPT(TransformState) modelview_transform = trav->get_world_transform()->compose(_net_transform);
    //CPT(TransformState) internal_transform = trav->get_scene()->get_cs_transform()->compose(modelview_transform);

    // Iterate all vertex pools
    LUIVertexPoolMap::iterator iter = _lui_root->get_iter_pool_begin();
    LUIVertexPoolMap::iterator end = _lui_root->get_iter_pool_end();
    for (;iter != end; ++iter) {

      LUIVertexPool *current = iter->second;
      Texture *currentTex = iter->first;

      CPT(RenderState) texture_state = state->set_attrib(TextureAttrib::make(currentTex));

      for (int i = 0; i < current->get_num_chunks(); i++) {
        Geom* geom = current->get_chunk(i)->get_geom();

        CullableObject *object = 
          new CullableObject(geom, texture_state, net_transform, 
          modelview_transform, _trav->get_scene());
        trav->get_cull_handler()->record_object(object, trav);
        cout << "Adding geom .." << endl;

      }
    }
    trav->end_traverse();
}

