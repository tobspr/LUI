

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
  width = pr - pl;
  height = pt - pb;

  _lens = new OrthographicLens();
  _lens->set_film_size(width, -height);
  _lens->set_film_offset(width * 0.5, height * 0.5);
  _lens->set_near_far(-1, 1);

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
    return GraphicsEngine::do_cull(cull_handler, scene_setup, gsg, current_thread);

    /*
    //PStatTimer timer(get_cull_region_pcollector(), current_thread);

    int pl, pr, pb, pt;
    get_pixels(pl, pr, pb, pt);
    LVecBase2i dimensions = LVecBase2i(pr - pl, pt - pb);

    cout << "DO_CULL, with dimensions " << dimensions.get_x() << " x " << dimensions.get_y() << endl;

    if (_size != dimensions) {
      _size = dimensions;
      cout << "On resized!" << endl;
      _lens->set_film_size(_size.get_x(), -_size.get_y());
      _lens->set_film_offset(_size.get_x() * 0.5, _size.get_y() * 0.5);
    }

    if (_input_handler != NULL) {
      _input_handler->update_context(_context, pl, pb);
    } else {
      _context->Update();
    }

    CullTraverser *trav = get_cull_traverser();
    trav->set_cull_handler(cull_handler);
    trav->set_scene(scene_setup, gsg, get_incomplete_render());
    trav->set_view_frustum(NULL);

    //_interface.render(_context, trav);


    trav->end_traverse();
    */
}

