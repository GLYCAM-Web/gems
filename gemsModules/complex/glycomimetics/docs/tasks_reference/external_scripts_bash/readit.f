      program readit
C***********************************************************************
C                                                                      #
C                Copyright (c) 1986, 1991, 1995                        #
C           Regents of the University of California                    #
C                                                                      #
C                    All Rights Reserved                               #
C                                                                      #
C  Permission to use, copy, modify, and distribute this software and   #
C  its documentation for any purpose and without fee is hereby         #
C  granted, provided that the above copyright notice appear in all     #
C  copies and that both that copyright notice and this permission      #
C  notice appear in supporting documentation, and that the name of     #
C  the University of California not be used in advertising or          #
C  publicity pertaining to distribution of the software without        #
C  specific, written prior permission.                                 #
C                                                                      #
C  THE REGENTS OF THE UNIVERSITY OF CALIFORNIA DISCLAIM ALL            #
C  WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED      #
C  WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL THE    #
C  UNIVERSITY OF CALIFORNIA BE LIABLE FOR ANY SPECIAL, INDIRECT OR     #
C  CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM      #
C  LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,     #
C  NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN           #
C  CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.            #
C                                                                      #
C***********************************************************************
C
      implicit double precision (a-h,o-z)
c
c   routine to output "esp.dat" files of coordinates
c   and electrostatic potential values for use in
c   "RESP".  Output values are in atomic units (the
c   default for resp).
c
c   version 1.0
c   james caldwell-ucsf February,1996
c
      open(unit=7,file="a",status="old",form="formatted")
      open(unit=8,file="b",status="old",form="formatted")
      open(unit=9,file="c",status="old",form="formatted")
      open(unit=10,file="esp.dat",status="new",form="formatted")
      open(unit=11,file="count",status="old",form="formatted")
      unit=0.529177249d0
      read (11,'(i6)')j
      read (11,'(i6)')i
c      write(6,'(t2,''enter natom,nesp: '',$)')
c      read (5,*)i,j
      write(6,'(''# atoms: '',i6,'' # esp: ''i6)')i,j
      write(10,'(2i6)')i,j
      do jn = 1,i
         read ( 7,'(32x,3f10.0)')a,b,c
         write(10,'(16x,3e16.6)')a/unit,b/unit,c/unit
      enddo
      do jn = 1,j
         read ( 8,'(32x3f10.0)')a,b,c
         read ( 9,'(14x,f10.0)')esp
         write(10,'(4e16.6)')esp,a/unit,b/unit,c/unit
      enddo
      rewind(7)
      rewind(8)
      rewind(9)
      rewind(10)
      rewind(11)
      call exit
      end
