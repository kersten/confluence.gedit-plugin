confluence.gedit-plugin
=======================

### Dependencies ###
This package has the following dependecies:

* [confluencerpclib](https://github.com/kersten/confluencerpclib)

### Installation ###
To install the plugins for personal use (in your home directory), run the
following commands from a terminal:

./autogen.sh  
./configure  
make  
make install

To install the plugin in another location use:

./autogen.sh  
./configure --without-home --prefix=</path/to/location>  
make  
make install

To install the plugins in the same location as the standard gedit plugins, set
the prefix path to the same as gedit (usually /usr).

### Donations ###

Please feel free to donate if you like this software. Click on the following
link to donate:

[![Flattr this](http://api.flattr.com/button/flattr-badge-large.png)](http://flattr.com/thing/112499/confluence-gedit-plugin)

[![Donate](http://pledgie.com/campaigns/14263.png)](http://pledgie.com/campaigns/14263)

### License ###

	Copyright (c) 2010, Kersten Burkhardt
	All rights reserved.

	Redistribution and use in source and binary forms, with or without
	modification, are permitted provided that the following conditions are met:
	1. Redistributions of source code must retain the above copyright
	   notice, this list of conditions and the following disclaimer.
	2. Redistributions in binary form must reproduce the above copyright
	   notice, this list of conditions and the following disclaimer in the
	   documentation and/or other materials provided with the distribution.
	3. All advertising materials mentioning features or use of this software
	   must display the following acknowledgement:
	   This product includes software developed by Kersten Burkhardt
	   (kerstenk@gmail.com).
	4. The names of its contributors may be used to endorse or promote products
	   derived from this software without specific prior written permission.

	THIS SOFTWARE IS PROVIDED BY KERSTEN BURKHARDT ''AS IS'' AND ANY
	EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
	WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
	DISCLAIMED. IN NO EVENT SHALL KERSTEN BURKHARDT BE LIABLE FOR ANY
	DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
	(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
	LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
	ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
	(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
	SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
