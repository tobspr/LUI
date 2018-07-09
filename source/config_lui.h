// Filename: config_lui.h
// Created by:  tobspr (28Aug14)
//

#ifndef CONFIG_LUI_H
#define CONFIG_LUI_H

#include "pandabase.h"
#include "notifyCategoryProxy.h"
#include "dconfig.h"

#define EXPCL_LUI EXPORT_CLASS
#define EXPTP_LUI EXPORT_TEMPL

ConfigureDecl(config_lui, EXPCL_LUI, EXPTP_LUI);
NotifyCategoryDecl(lui, EXPCL_LUI, EXPTP_LUI);

extern EXPCL_LUI void init_lui();

using namespace std;

#endif
