/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                               keyboard.c
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                                                    jin, 2019
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

#include "type.h"
#include "const.h"
#include "protect.h"
#include "proto.h"
#include "string.h"
#include "proc.h"
#include "global.h"
/*======================================================================*
                           keyboard_handler
 *======================================================================*/
PUBLIC void keyboard_handler(int irq)
{	in_byte(0x60);
	if(p_proc_ready->pid == 0){		
		p_proc_ready=proc_table+1;
	}else{		
	}
}



