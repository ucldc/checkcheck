import math


class EntropyCounter(object):
    """ calculate entropy of a file
    """

    # based on [ActiveState Code » Recipes » Shannon Entropy Calculation (Python recipe)](
    # http://code.activestate.com/recipes/577476-shannon-entropy-calculation/#c9)
    # Created by FB36 on Mon, 29 Nov 2010 (MIT)
    def __init__(self, default=None):
        self.byte_freq = [0] * 256
        self.byte_total = 0

    def update(self, data):
        for b in bytearray(data):
            self.byte_freq[b] += 1
            self.byte_total += 1

    def entropy(self):
        """bits per byte symbol (shannon entropy)"""
        ent = 0.0
        for f in self.byte_freq:
            if f > 0:
                freq = float(f) / self.byte_total
                ent = ent + freq * math.log(freq, 2)
        return -ent

    def __str__(self):
        """"""
        return '{}(bits/byte symbol) * {} (bytes storage) = {} (bytes info)'.format(
            self.entropy(), self.byte_total,
            self.entropy() * self.byte_total / 8)


"""
Copyright © 2016, Regents of the University of California
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
- Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the University of California nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""
