#ifndef CANARY_H_
#define CANARY_H_
#ifdef __cplusplus
extern "C" {
#endif

#if defined(__x86_64__) || defined (__i386__)
#include "arch/x86.h"
#else
#include "arch/noarch.h"
#endif

#define MAGMA_LOG(b,c) do{magma_log((b),(int)(c));}while(0)
#define MAGMA_LOG_V(b,c) (magma_log((b),(int)(c)))
#define MAGMA_AND(a,b) magma_and((a),(b))
#define MAGMA_OR(a,b) magma_or((a),(b))
#define ORACLE_HIT(a,b,c) do { oracle_hit((a), (b), (c)); } while (0)

extern void magma_log(const char *bug, int condition);

extern void oracle_hit(int bug_id, int oracle_id, int step_id);
#ifdef __cplusplus
}
#endif
#endif
