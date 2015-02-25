// Filename: config_lui.h
// Created by:  tobspr (28Aug14)
//

#ifndef CONFIG_LUI_H
#define CONFIG_LUI_H

#include "pandabase.h"
#include "notifyCategoryProxy.h"
#include "dconfig.h"

// It is convenient to put these here for now.
#if (defined(WIN32_VC) || defined(WIN64_VC)) && !defined(CPPPARSER) && !defined(LINK_ALL_STATIC)
#ifdef BUILDING_LUI
  #define EXPCL_LUI __declspec(dllexport)
  #define EXPTP_LUI
#else
  #define EXPCL_LUI __declspec(dllimport)
  #define EXPTP_LUI extern
#endif
#else
#define EXPCL_LUI
#define EXPTP_LUI
#endif

ConfigureDecl(config_lui, EXPCL_LUI, EXPTP_LUI);
NotifyCategoryDecl(lui, EXPCL_LUI, EXPTP_LUI);

extern EXPCL_LUI void init_lui();

#endif
