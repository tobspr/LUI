// Filename: config_lui.cxx
// Created by:  tobspr (28Aug14)
//
////////////////////////////////////////////////////////////////////

#include "config_lui.h"

#include "pandaSystem.h"
#include "dconfig.h"

#include "luiRegion.h"
#include "luiInputHandler.h"
#include "luiSprite.h"
#include "luiBaseElement.h"
#include "luiObject.h"
#include "luiText.h"
#include "luiEventData.h"
#include "luiBaseLayout.h"
#include "luiVerticalLayout.h"
#include "luiHorizontalLayout.h"

Configure(config_lui);
NotifyCategoryDef(lui, "");

ConfigureFn(config_lui) {
  init_lui();
}

void init_lui() {
  static bool initialized = false;
  if (initialized) {
    return;
  }
  initialized = true;

  LUIRegion::init_type();
  LUIInputHandler::init_type();
  LUIBaseElement::init_type();
  LUISprite::init_type();
  LUIObject::init_type();
  LUIText::init_type();
  LUIEventData::init_type();
  LUIBaseLayout::init_type();
  LUIVerticalLayout::init_type();
  LUIHorizontalLayout::init_type();
}
