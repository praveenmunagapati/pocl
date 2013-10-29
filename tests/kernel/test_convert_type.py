#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Victor Oliveira <victormatheus@gmail.com>
# Copyright (c) 2013 Jesse Towner <jessetowner@lavabit.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

all_types = ['char', 'uchar', 'short', 'ushort', 'int', 'uint', 'long', 'ulong', 'float', 'double']
int_types = ['char', 'uchar', 'short', 'ushort', 'int', 'uint', 'long', 'ulong']
signed_types = ['char', 'short', 'int', 'long', 'float', 'double']
unsigned_types = ['uchar', 'ushort', 'uint', 'ulong']
int32_types = ['char', 'uchar', 'short', 'ushort', 'int', 'uint']
int64_types = ['long', 'ulong']
float_types = ['float', 'double']
vector_sizes = ['', '2', '4', '8', '16']
rounding_modes = ['','_rte','_rtz','_rtp','_rtn']

limit_max = {'char'  : 'CHAR_MAX',
             'uchar' : 'UCHAR_MAX',
             'short' : 'SHRT_MAX',
             'ushort': 'USHRT_MAX',
             'int'   : 'INT_MAX',
             'uint'  : 'UINT_MAX',
             'long'  : 'LONG_MAX',
             'ulong' : 'ULONG_MAX',
             'float' : 'FLT_MAX',
             'double': 'DBL_MAX'}

limit_min = {'char'  : 'CHAR_MIN',
             'uchar' : '0',
             'short' : 'SHRT_MIN',
             'ushort': '0',
             'int'   : 'INT_MIN',
             'uint'  : '0',
             'long'  : 'LONG_MIN',
             'ulong' : '0',
             'float' : '-FLT_MAX',
             'double': '-DBL_MAX'}

float_suffix = {'float': 'f', 'double': ''}
float_int_type = {'float': 'int', 'double': 'long'}

printf_format_type = {
             'char'  : '%#.2hhx',
             'uchar' : '%#.2hhx',
             'short' : '%#.4hx',
             'ushort': '%#.4hx',
             'int'   : '%#.8x',
             'uint'  : '%#.8x',
             'long'  : '%#.16llx',
             'ulong' : '%#.16llx',
             'float' : '%.8g',
             'double': '%.17g'}

def generate_conversions(src_types, dst_types):
  for src in src_types:
    for dst in dst_types:
      for size in vector_sizes:
        yield (src, dst, size)

#
# file header
#

print("""/* !!!! AUTOGENERATED FILE generated by test_convert_type.py !!!!!

   DO NOT CHANGE THIS FILE. MAKE YOUR CHANGES TO test_convert_type.py AND RUN:
   $ python3 test_convert_type.py > test_convert_type.cl
*/
""")

#
# integer value tables
#

for types in [int32_types, int64_types]:
  if types == int64_types:
    print("\n#ifdef cl_khr_int64")
  for t in types:
    values = ["0", "1", limit_min[t], limit_max[t], limit_min[t] + " / 2", limit_max[t] + " / 2"]
    print("constant {0} {0}_values[{1}] = {{ ".format(t, len(values)), end="")
    print(*values, sep=", ", end=" };\n")
  print()
  for t in types:
    print("constant size_t {0}_values_length = sizeof({0}_values) / sizeof({0}_values[0]);".format(t))
  if types == int64_types:
    print("\n#endif")

#
# floating-point value tables
#

for f in float_types:
  if f == 'double':
    print("\n#ifdef cl_khr_fp64")
  print("""
#ifdef cl_khr_fp64
constant {F} {F}_sat_offsets[16] =
{{
   0.0{S}, ({F})CHAR_MAX, ({F})CHAR_MIN, ({F})UCHAR_MAX, ({F})SHRT_MIN, ({F})SHRT_MAX, ({F})USHRT_MAX, ({F})INT_MAX,
   ({F})INT_MIN, ({F})UINT_MAX, ({F})LONG_MAX, ({F})LONG_MIN, ({F})ULONG_MAX, 0.0{S}, 1.0e15{S}, -1.0e15{S}
}};
#else
constant {F} {F}_sat_offsets[13] =
{{
   0.0{S}, ({F})CHAR_MAX, ({F})CHAR_MIN, ({F})UCHAR_MAX, ({F})SHRT_MIN, ({F})SHRT_MAX, ({F})USHRT_MAX, ({F})INT_MAX,
   ({F})INT_MIN, ({F})UINT_MAX, 0.0{S}, 1.0e15{S}, -1.0e15{S}
}};
#endif

constant {F} {F}_values            [17] = {{ -2.0{S}, -1.75{S}, -1.5{S}, -1.25{S}, -1.0{S}, -0.75{S}, -0.5{S}, -0.25{S}, 0.0{S}, 0.25{S}, 0.5{S}, 0.75{S}, 1.0{S}, 1.25{S}, 1.5{S}, 1.75{S}, 2.0{S} }};
constant {I} {F}_rounded_values    [17] = {{ -2     , -1      , -1     , -1      , -1     ,  0      ,  0     ,  0      , 0     , 0      , 0     , 0      , 1     , 1      , 1     , 1      , 2      }};
constant {I} {F}_rounded_values_rtz[17] = {{ -2     , -1      , -1     , -1      , -1     ,  0      ,  0     ,  0      , 0     , 0      , 0     , 0      , 1     , 1      , 1     , 1      , 2      }};
constant {I} {F}_rounded_values_rte[17] = {{ -2     , -2      , -2     , -1      , -1     , -1      ,  0     ,  0      , 0     , 0      , 0     , 1      , 1     , 1      , 2     , 2      , 2      }};
constant {I} {F}_rounded_values_rtp[17] = {{ -2     , -1      , -1     , -1      , -1     ,  0      ,  0     ,  0      , 0     , 1      , 1     , 1      , 1     , 2      , 2     , 2      , 2      }};
constant {I} {F}_rounded_values_rtn[17] = {{ -2     , -2      , -2     , -2      , -1     , -1      , -1     , -1      , 0     , 0      , 0     , 0      , 1     , 1      , 1     , 1      , 2      }};

constant size_t {F}_values_length = sizeof({F}_values) / sizeof({F}_values[0]);
""".format(F=f, S=float_suffix[f], I=float_int_type[f]))
  if f == 'double':
    print("\n#endif")

#
# comparison functions
#

for t in all_types:
  for ot in all_types:
    if t == 'double' or ot == 'double':
      print("\n#ifdef cl_khr_fp64")
    if t in int64_types or ot in int64_types:
      print("\n#ifdef cl_khr_int64")
    print("""
_CL_NOINLINE
void compare_{Type}_elements_{OrigType}(char const* name, size_t sample, constant {OrigType}* original1, const {OrigType}* original2, const {Type}* expected, const {Type}* actual, size_t n)
{{
  for (size_t i = 0; i < n; ++i) {{
    if (expected[i] != actual[i]) {{
      printf("FAIL: %s - sample#: %u element#: %u original: {OrigTypeFormat} expected: {TypeFormat} actual: {TypeFormat}\\n",
        name, (uint)sample, (uint)i, ({OrigType})(original1 ? *original1 : *original2), expected[i], actual[i]);
    }}
  }}
}}""".format(Type=t, TypeFormat=printf_format_type[t], OrigType=ot, OrigTypeFormat=printf_format_type[ot]))
    if t == 'double' or ot == 'double':
      print("\n#endif")
    if t in int64_types or ot in int64_types:
      print("\n#endif")

#
# conversion tests
#

print("\nkernel void test_convert_type()\n{", end="")

#
# integer to integer conversions, with and without saturation
#

for (src, dst, size) in generate_conversions(int_types, int_types):
  if (src in int64_types) or (dst in int64_types):
    print("\n#ifdef cl_khr_int64")
  print("""
  for (size_t i = 0; i < {S}_values_length; ++i) {{
    const {S} min_expected = ({DMIN} > {SMIN}) ? ({S}){DMIN} : {SMIN};
    const {S} max_expected = ({DMAX} < {SMAX}) ? ({S}){DMAX} : {SMAX};
    union {{ {D}{N} value; {D} raw[{M}]; }} expected, actual;
    expected.value = (({D}{N})(({D}){S}_values[i]));
    actual.value = convert_{D}{N}(({S}{N}){S}_values[i]);
    compare_{D}_elements_{S}("convert_{D}{N}({S}{N})", i, &{S}_values[i], 0, expected.raw, actual.raw, {M});
    if ({S}_values[i] < min_expected) {{
       expected.value = ({D}{N})min_expected;
    }}
    else if ({S}_values[i] > max_expected) {{
       expected.value = ({D}{N})max_expected;
    }}
    actual.value = convert_{D}{N}_sat(({S}{N}){S}_values[i]);
    compare_{D}_elements_{S}("convert_{D}{N}_sat({S}{N})", i, &{S}_values[i], 0, expected.raw, actual.raw, {M});
  }}""".format(
      S=src, SMIN=limit_min[src], SMAX=limit_max[src],
      D=dst, DMIN=limit_min[dst], DMAX=limit_max[dst],
      N=size, M=size if len(size) > 0 else "1"))
  if (src in int64_types) or (dst in int64_types):
    print("\n#endif")

#
# floating-point to integer conversions, with and without saturation
#

for (src, dst, size) in generate_conversions(float_types, int_types):
  if (dst in int64_types):
    print("\n#ifdef cl_khr_int64")
  if (src == 'double'):
    print("\n#ifdef cl_khr_fp64")
  print("""
  for (size_t i = 0; i < {S}_values_length; ++i) {{
    const {S} sat_input = ({S}_values[i] + {S}_sat_offsets[i]);
    const {S} min_expected = ({DMIN} > {SMIN}) ? ({S}){DMIN} : {SMIN};
    const {S} max_expected = ({DMAX} < {SMAX}) ? ({S}){DMAX} : {SMAX};
    union {{ {D}{N} value; {D} raw[{M}]; }} expected, actual;"""
      .format(
        S=src, SMIN=limit_min[src], SMAX=limit_max[src],
        D=dst, DMIN=limit_min[dst], DMAX=limit_max[dst],
        N=size, M=size if len(size) > 0 else "1"))
  for mode in rounding_modes:
    print("""    expected.value = (({D}{N})(({D}){S}_rounded_values{R}[i]));
    actual.value = convert_{D}{N}{R}(({S}{N}){S}_values[i]);
    for (size_t n=0; n<{M}; ++n) {{
      bool type_is_unsigned = ({D})(({D})0 - ({D})1) >= ({D})0;
      bool origin_is_negative = {S}_values[i] < ({S})0;
      bool result_is_nonzero = actual.raw[n] != ({D})0;
      if (type_is_unsigned && origin_is_negative && result_is_nonzero) {{
        expected.raw[n] = 0;
        actual.raw[n] = 0;
      }}
    }}
    compare_{D}_elements_{S}("convert_{D}{N}{R}({S}{N})", i, &{S}_values[i], 0, expected.raw, actual.raw, {M});
    expected.value = ({D}{N})convert_{D}{R}(sat_input);
    if (sat_input < min_expected) {{
       expected.value = ({D}{N})min_expected;
    }}
    else if (sat_input > max_expected) {{
       expected.value = ({D}{N})max_expected;
    }}
    actual.value = convert_{D}{N}_sat{R}(({S}{N})sat_input);
    compare_{D}_elements_{S}("convert_{D}{N}_sat{R}({S}{N})", i, 0, &sat_input, expected.raw, actual.raw, {M});"""
      .format(S=src, D=dst, R=mode, N=size, M=size if len(size) > 0 else "1"))
  print("  }");
  if (src == 'double'):
    print("\n#endif")
  if (dst in int64_types):
    print("\n#endif")

#
# other random tests
#

print("""
union { int8 value; int raw[8]; } qe, qa;
union { float8 value; float raw[8]; } qo;

qo.value = (float8)(-23.67f, -23.50f, -23.35f, -23.0f, 23.0f, 23.35f, 23.50f, 23.67f);
qa.value = convert_int8_rtz(qo.value);
qe.value = (int8)(-23, -23, -23, -23, 23, 23, 23, 23);
compare_int_elements_float("convert_int8_rtz(float8)", 0, 0, qo.raw, qe.raw, qa.raw, 8);

qo.value = (float8)(-23.67f, -23.50f, -23.35f, -23.0f, 23.0f, 23.35f, 23.50f, 23.67f);
qa.value = convert_int8_rtp(qo.value);
qe.value = (int8)(-23, -23, -23, -23, 23, 24, 24, 24);
compare_int_elements_float("convert_int8_rtp(float8)", 0, 0, qo.raw, qe.raw, qa.raw, 8);

qo.value = (float8)(-23.67f, -23.50f, -23.35f, -23.0f, 23.0f, 23.35f, 23.50f, 23.67f);
qa.value = convert_int8_rtn(qo.value);
qe.value = (int8)(-24, -24, -24, -23, 23, 23, 23, 23);
compare_int_elements_float("convert_int8_rtn(float8)", 0, 0, qo.raw, qe.raw, qa.raw, 8);

qo.value = (float8)(-23.67f, -23.50f, -23.35f, -23.0f, 23.0f, 23.35f, 23.50f, 23.67f);
qa.value = convert_int8_rte(qo.value);
qe.value = (int8)(-24, -24, -23, -23, 23, 23, 24, 24);
compare_int_elements_float("convert_int8_rte(float8)", 0, 0, qo.raw, qe.raw, qa.raw, 8);

qo.value = (float8)(-23.67f, -23.50f, -23.35f, -23.0f, 23.0f, 23.35f, 23.50f, 23.67f);
qa.value = convert_int8(qo.value);
qe.value = (int8)(-23, -23, -23, -23, 23, 23, 23, 23);
compare_int_elements_float("convert_int8(float8)", 0, 0, qo.raw, qe.raw, qa.raw, 8);
""")

#
# end conversion tests
#

print("}")

