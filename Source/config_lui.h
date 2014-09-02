// Filename: config_lui.h
// Created by:  tobspr (28Aug14)
//

#ifndef CONFIG_LUI_H
#define CONFIG_LUI_H

#include "pandabase.h"
#include "notifyCategoryProxy.h"
#include "dconfig.h"

//ConfigureDecl(config_lui, EXPCL_PANDASKEL, EXPTP_PANDASKEL);
NotifyCategoryDecl(lui, EXPCL_PANDASKEL, EXPTP_PANDASKEL);


extern EXPCL_PANDASKEL void init_lui();

#endif
