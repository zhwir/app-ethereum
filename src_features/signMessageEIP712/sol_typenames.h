#ifndef SOL_TYPENAMES_H_
#define SOL_TYPENAMES_H_

#include <stdbool.h>
#include <stdint.h>

bool sol_typenames_init(void);

const char *get_struct_field_sol_typename(const uint8_t *ptr,
                                          uint8_t *const length);

#endif // SOL_TYPENAMES_H_
