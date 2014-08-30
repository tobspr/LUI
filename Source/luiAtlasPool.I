

INLINE bool LUIAtlasPool::has_atlas(const string &atlas_id) {
  return _atlases.count(atlas_id) == 1;
}


INLINE PT(LUIAtlas) LUIAtlasPool::get_atlas(const string &atlas_id) {
  if (has_atlas(atlas_id)) {
    return _atlases[atlas_id];
  }
  return NULL;
}

INLINE PT(LUIAtlasDescriptor) LUIAtlasPool::get_descriptor(const string &entry_id) {
  return get_descriptor("default", entry_id);
}

INLINE PT(LUIAtlasDescriptor) LUIAtlasPool::get_descriptor(const string &atlas_id, const string &entry_id) {
  if (!has_atlas(atlas_id)) {
    lui_cat.error() << "Atlas '" << atlas_id << "' not found!" << endl;
    return NULL;
  }

  LUIAtlas* atlas = get_atlas(atlas_id);
  LUIAtlasEntry * entry = atlas->get_entry(entry_id);

  if (entry != NULL) {
    PT(LUIAtlasDescriptor) descriptor = new LUIAtlasDescriptor();
    descriptor->set_size(entry->size);
    descriptor->set_uv_begin(entry->pos / float(atlas->get_size()) );
    descriptor->set_uv_end( (entry->pos + entry->size) / float(atlas->get_size()) );
    descriptor->set_texture(atlas->get_texture());
    return descriptor;
  } 
    
  lui_cat.error() << "Atlas entry '" << entry_id << "' not found!" << endl;
  return NULL;

}
