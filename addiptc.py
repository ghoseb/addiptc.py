#!/usr/bin/env python
## addiptc.py -- Add IPTC Metadata to photos -*- Python -*-
## Time-stamp: "2008-10-29 15:24:35 ghoseb"

## Copyright (c) 2008, Baishampayan Ghose <b.ghose@gmail.com>
## All rights reserved.

## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are met:
##     * Redistributions of source code must retain the above copyright
##       notice, this list of conditions and the following disclaimer.
##     * Redistributions in binary form must reproduce the above copyright
##       notice, this list of conditions and the following disclaimer in the
##       documentation and/or other materials provided with the distribution.
##     * Neither the name of the <organization> nor the
##       names of its contributors may be used to endorse or promote products
##       derived from this software without specific prior written permission.

## THIS SOFTWARE IS PROVIDED BY BAISHAMPAYAN GHOSE ''AS IS'' AND ANY
## EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
## WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
## DISCLAIMED. IN NO EVENT SHALL BAISHAMPAYAN GHOSE BE LIABLE FOR ANY
## DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
## (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
## LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
## ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
from optparse import OptionParser, make_option

try:
    import pyexiv2
except ImportError:
    print "You need to install python-pyexiv2 first"
    sys.exit(1)

__APP_NAME__ = "addiptc.py by Baishampayan Ghose <b.ghose@gmail.com>"
__APP_VERSION__ = "0.1"

option_list = [
    make_option("-l", "--headline", default=None, dest="HEADLINE", help="Synopsis of the photo", metavar="HEADLINE"),
    make_option("-a", "--caption", default=None, dest="CAPTION", help="Photo caption", metavar="CAPTION"),
    make_option("-t", "--tags", default=None, dest="KEYWORDS", help="Comma separated tags", metavar="TAG,TAG2"),
    make_option("-c", "--city", default=None, dest="CITY", help="City where the photo was taken", metavar="CITY"),
    make_option("-o", "--country", default=None, dest="COUNTRY", help="Country code of origin", metavar="COUNTRY"),
    make_option("-r", "--credit", default=None, dest="CREDIT", help="Photo credit", metavar="CREDIT"),
    make_option("-p", "--copyright", default=None, dest="COPYRIGHT", help="Copyright notice", metavar="COPYRIGHT"),
    make_option("-n", "--contact", default=None, dest="CONTACT", help="Contact info", metavar="CONTACT"),
    make_option("-w", "--author", default=None, dest="AUTHOR", help="Author bio", metavar="AUTHOR_BIO"),
    make_option("-f", "--file", default=None, dest="FILE", help="File name", metavar="FILE"),
    ]

usage = "Usage: %prog -h HEADLINE -a CAPTION -t TAG1,TAG2 -c CITY -o COUNTRY_CODE -r CREDIT -p COPYRIGHT -n CONTACT -w AUTHOR_BIO -f FILE"    
parser = OptionParser(option_list=option_list, usage=usage)

def add_iptc_data(options, file_name):
    """Add IPTC metadata to a file
    
    Arguments:
    - `options`: The parsed options object
    - `file_name`: The image file name
    """
    try:
        image = pyexiv2.Image(file_name)
    except IOError:
        sys.exit(1)

    image.readMetadata()

    image['Iptc.Application2.Program'] = "%s v%s" % (__APP_NAME__, __APP_VERSION__) # Don't remove this
    
    if options.HEADLINE:
        image['Iptc.Application2.Headline'] = options.HEADLINE

    if options.CAPTION:
        image['Iptc.Application2.Caption'] = options.CAPTION

    if options.KEYWORDS:
        image['Iptc.Application2.Keywords'] = [tag for tag in options.KEYWORDS.split(',')]

    if options.CITY:
        image['Iptc.Application2.City'] = options.CITY

    if options.COUNTRY:
        image['Iptc.Application2.CountryCode'] = options.COUNTRY

    if options.CREDIT:
        image['Iptc.Application2.Credit'] = options.CREDIT

    if options.COPYRIGHT:
        image['Iptc.Application2.Copyright'] = options.COPYRIGHT

    if options.CONTACT:
        image['Iptc.Application2.Contact'] = options.CONTACT

    if options.AUTHOR:
        image['Iptc.Application2.Writer'] = options.AUTHOR
    
    image.writeMetadata()
    
    sys.exit(0)
    

if __name__ == '__main__':
    (options, args) = parser.parse_args()
    if options.FILE:
        add_iptc_data(options, options.FILE)
    else:
        parser.print_help()
