#define OTHER_LIBS p3interrogatedb:c p3dconfig:c p3dtoolconfig:m \
                   p3dtoolutil:c p3dtoolbase:c p3dtool:m p3prc:c

#define USE_PACKAGES 
#define BUILDING_DLL BUILDING_PANDASKEL

#begin lib_target
  #define TARGET p3lui
  #define LOCAL_LIBS \
    p3display p3text p3pgraph p3gobj p3linmath p3putil
    
  #define COMBINED_SOURCES $[TARGET]_composite1.cxx 

  #define SOURCES \
    config_lui.h \
    luiAtlas.I luiAtlas.h \
    luiAtlasDescriptor.I luiAtlasDescriptor.h \
    luiAtlasPacker.h \
    luiAtlasPool.I luiAtlasPool.h \
    luiBaseElement.I luiBaseElement.h \
    luiChunkDescriptor.I luiChunkDescriptor.h \
    luiIterators.h \
    luiObject.I luiObject.h \
    luiRegion.I luiRegion.h \
    luiRoot.I luiRoot.h \
    luiSprite.I luiSprite.h \
    luiVertexChunk.I luiVertexChunk.h \
    luiVertexData.h \
    luiVertexPool.I luiVertexPool.h
    
  #define INCLUDED_SOURCES \
    config_lui.cxx \
    luiAtlas.cxx \
    luiAtlasDescriptor.cxx
    luiAtlasPacker.cxx
    luiAtlasPool.cxx
    luiBaseElement.cxx
    luiChunkDescriptor.cxx
    luiObject.cxx
    luiRegion.cxx
    luiRoot.cxx
    luiSprite.cxx
    luiVertexChunk.cxx
    luiVertexPool.cxx

  #define INSTALL_HEADERS \
    luiAtlas.I luiAtlas.h \
    luiAtlasDescriptor.I luiAtlasDescriptor.h \
    luiAtlasPacker.h \
    luiAtlasPool.I luiAtlasPool.h \
    luiBaseElement.I luiBaseElement.h \
    luiChunkDescriptor.I luiChunkDescriptor.h \
    luiIterators.h \
    luiObject.I luiObject.h \
    luiRegion.I luiRegion.h \
    luiRoot.I luiRoot.h \
    luiSprite.I luiSprite.h \
    luiVertexChunk.I luiVertexChunk.h \
    luiVertexData.h \
    luiVertexPool.I luiVertexPool.h

  #define IGATESCAN all

#end lib_target

