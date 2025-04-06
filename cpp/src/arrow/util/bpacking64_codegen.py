#!/bin/python

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# This script is modified from its original version in GitHub. Original source:
# https://github.com/lemire/FrameOfReference/blob/146948b6058a976bc7767262ad3a2ce201486b93/scripts/turbopacking64.py

# Usage:
#   python bpacking64_codegen.py > bpacking64_default.h

def howmany(bit):
    """ how many values are we going to pack? """
    return 32


def howmanywords(bit):
    return (howmany(bit) * bit + 63)//64


def howmanybytes(bit):
    return (howmany(bit) * bit + 7)//8


print('''// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

// This file was generated by script which is modified from its original version in GitHub.
// Original source:
// https://github.com/lemire/FrameOfReference/blob/master/scripts/turbopacking64.py
// The original copyright notice follows.

// This code is released under the
// Apache License Version 2.0 http://www.apache.org/licenses/.
// (c) Daniel Lemire 2013

#pragma once

#include "arrow/util/bit_util.h"
#include "arrow/util/ubsan.h"

namespace arrow {
namespace internal {
''')


print("inline const uint8_t* unpack0_64(const uint8_t* in, uint64_t* out) {")
print(f"  for(int k = 0; k < {howmany(0)} ; k += 1) {{")
print("    out[k] = 0;")
print("  }")
print("  return in;")
print("}")

for bit in range(1, 65):
    print("")
    print(f"inline const uint8_t* unpack{bit}_64(const uint8_t* in, uint64_t* out) {{")

    if(bit < 64):
        print(f"  const uint64_t mask = {((1 << bit)-1)}ULL;")
    maskstr = " & mask"
    if (bit == 64):
        maskstr = ""  # no need

    for k in range(howmanywords(bit)-1):
        print(f"  uint64_t w{k} = util::SafeLoadAs<uint64_t>(in);")
        print(f"  w{k} = arrow::BitUtil::FromLittleEndian(w{k});")
        print(f"  in += 8;")
    k = howmanywords(bit) - 1
    if (bit % 2 == 0):
        print(f"  uint64_t w{k} = util::SafeLoadAs<uint64_t>(in);")
        print(f"  w{k} = arrow::BitUtil::FromLittleEndian(w{k});")
        print(f"  in += 8;")
    else:
        print(f"  uint64_t w{k} = util::SafeLoadAs<uint32_t>(in);")
        print(f"  w{k} = arrow::BitUtil::FromLittleEndian(w{k});")
        print(f"  in += 4;")

    for j in range(howmany(bit)):
        firstword = j * bit // 64
        secondword = (j * bit + bit - 1)//64
        firstshift = (j*bit) % 64
        firstshiftstr = f" >> {firstshift}"
        if(firstshift == 0):
            firstshiftstr = ""  # no need
        if(firstword == secondword):
            if(firstshift + bit == 64):
                print(f"  out[{j}] = w{firstword}{firstshiftstr};")
            else:
                print(f"  out[{j}] = (w{firstword}{firstshiftstr}){maskstr};")
        else:
            secondshift = (64-firstshift)
            print(f"  out[{j}] = ((w{firstword}{firstshiftstr}) | "
                  f"(w{firstword+1} << {secondshift})){maskstr};")
    print("")
    print("  return in;")
    print("}")

print('''
}  // namespace internal
}  // namespace arrow''')
