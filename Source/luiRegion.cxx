

#include "luiRegion.h"


#include "graphicsOutput.h"

TypeHandle LUIRegion::_type_handle;

LUIRegion::
  LUIRegion(GraphicsOutput *window, const LVecBase4 &dr_dimensions,
  const string &context_name) :
DisplayRegion(window, dr_dimensions) {

  int pl, pr, pb, pt;
  get_pixels(pl, pr, pb, pt);
  _size = LVecBase2i(pr - pl, pt - pb);

  _lens = new OrthographicLens;
  _lens->set_film_size(_size.get_x(), -_size.get_y());
  _lens->set_film_offset(_size.get_x() * 0.5, _size.get_y() * 0.5);
  _lens->set_near_far(-1, 1);
  set_camera(new Camera(context_name, _lens));
}

LUIRegion::~LUIRegion() {

}

void LUIRegion::
  do_cull(CullHandler *cull_handler, SceneSetup *scene_setup,
  GraphicsStateGuardian *gsg, Thread *current_thread) {

    PStatTimer timer(get_cull_region_pcollector(), current_thread);

    int pl, pr, pb, pt;
    get_pixels(pl, pr, pb, pt);
    LVecBase2i dimensions = LVecBase2i(pr - pl, pt - pb);

    if (_size != dimensions) {
      _size = dimensions;
      lui_cat.debug() << "On resized!" << endl;
      _lens->set_film_size(_size.get_x(), -_size.get_y());
      _lens->set_film_offset(_size.get_x() * 0.5, _size.get_y() * 0.5);
    }

 /*   if (_input_handler != NULL) {
      _input_handler->update_context(_context, pl, pb);
    } else {
      _context->Update();
    }*/

    CullTraverser *trav = get_cull_traverser();
    trav->set_cull_handler(cull_handler);
    trav->set_scene(scene_setup, gsg, get_incomplete_render());
    trav->set_view_frustum(NULL);

    //_interface.render(_context, trav);


    trav->end_traverse();
}

