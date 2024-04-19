        program resp
C
C       RESP   version 2.2     January 2011 - q4md-forcefieldtools.org
C       RESP   version 2.1     October 1994 Jim Caldwell
C       RESP   version 2.0     September 1992
C          Author: Christopher Bayly
C
C       ESPFIT version 1.0 modified by Ian Gould to run in conjunction
C              with gaussian 90.
C
C       ESPFIT version 1.0 (G80UCSF):
C
C                 U.CHANDRA SINGH AND P.A.KOLLMAN
C
C       All authors:
C
C                 DEPARTMENT OF PHARMACEUTICAL CHEMISTRY
C                 SCHOOL OF PHARMACY
C                 UNIVERSITY OF CALIFORNIA
C                 SAN FRANCISCO   CA 94143
C
C---------------------------------------------------------------------
C
C       Make the standalone version of the resp program,
C              independent of the AmberTools.
C       Increase the numbers maxq   (maximal number of charges),
C                            maxlgr (max. no of Lagrangian constraints) &
C                            maxmol (max. no of molecules)
C              to handle complex charge derivation.
C       Decrease the convergence criteria qtol to 0.1d-5
C              to increase charge accuracy.
C       Extend RESP and ESP charge derivation using the RESP program 
C              to all the elements of the periodic table.
C
C       Authors: F.-Y. Dupradeau & P. Cieplak
C                http://q4md-forcefieldtools.org/
C
C---------------------------------------------------------------------
C
C     THIS PROGRAM FITS THE QUANTUM MECHANICALLY CALCULATED
C     POTENTIAL AT MOLECULAR SURFACES USING AN ATOM-CENTERED
C     POINT CHARGE MODEL. THE MOLECULAR SURFACES ARE GENERATED
C     BEYOND VANDER WAAL SURFACE IN ORDER TO MINIMISE OTHER
C     CONTRIBUTIONS SUCH AS EXCHANGE REPULSION AND CHARGE TRANSFER
C
C---------------------------------------------------------------------
C
C     -1st-   TITLE       FORMAT(10A8)
C
C---------------------------------------------------------------------
C
c     -2nd-
C
C           OPTIONS FOR THE JOB begin with " &cntrl"
c                               end with   " &end"
c           note leading blanks !!!!!!!!!!
C
C
C        INOPT   =  0  ... NORMAL RUN
C                =  1  ... CYCLE THROUGH A LIST OF DIFFERENT qwt
c                                read from -w unit 
c
C       IOUTOPT  =  0   NORMAL RUN
C                =  1   write restart info of new esp etc to 
c                              unit -e (esout unit)  
C
C         IQOPT  =  0  ... use the q's which are read the -i unit 
C                =  1  ... RESET ALL INITIAL CHARGES TO ZERO
C                =  2  ... READ IN NEW INITIAL CHARGES FROM -q (qwt) 
C                =  3  ... READ IN NEW INITIAL CHARGES FROM  -q (qwt)
C                                  AND PERFORM AVERAGING OF THOSE NEW 
C                                  INITIAL CHARGES ACCORDING TO IVARY VALUES
C
C         ihfree =  0  ... ALL ATOMS ARE RESTRAINED
C                =  1  ... HYDROGENS NOT RESTRAINED
C
C      irstrnt   =  0  ... HARMONIC RESTRAINTS (old style)
C                =  1  ... HYPERBOLIC RESTRAINT TO CHARGE OF ZERO (default)
C                =  2  ... ONLY ANALYSIS OF INPUT CHARGES; NO
C                          CHARGE FITTING IS CARRIED OUT
c
c      iunits    =  0  ... atom coordinates in angstroms
c                =  1       "     "          "  bohrs
c 
c 
c          qwt   =  restraint weight if irstrnt = 1
c
c NOTE: ESP coordinates must always be in Bohrs
C
C--------------------------------------------------------------------------
C
C     -3rd- wtmol .... relative weight for the molecule if 
c                    multiple molecule fit (1.0 otherwise) 
C
C             FORMAT(F10.5)
C
C--------------------------------------------------------------------------
c
c     -4th- subtitle for molecule
c
C------------------------------------------------------
C--------------------------------------------------------------------------
C
c     -5th- CHARGE,IUNIQ ( THE NUMBER OF UNIQUE CENTERS for this molecule)
c
C           FORMAT(2I5)
C
C--------------------------------------------------------------------------
C     -6th-  ONE CARD FOR EACH UNIQUE CENTER
C
C     FORMAT(I5,i5)
C
C      Name, IVARY
C
C             NAME = ATOMIC number  
C
C             IVARY = CONTROL OF CHARGE VARIATION OF THIS CENTER
C                   =  0 CHARGE VARIED INDEPENDENTLY OF PREVIOUS CENTERS
C                   = -n CHARGE FROZEN AT "INITIAL CHARGE" VALUE
C                   =  n CHARGE FITTED TOGETHER WITH CENTER n
C
C-------------------------------------------------------------------------
C
C     -7th-  intra molecule charge constraints...  blank line if no constr
C
C             FORMAT(I5,F10.5)
C
C     ngrp = number of centers in the group associated with this
C            constraint (i.e. the number of centers to be read in)
C
C    grpchg(i) = charge to which the associated group of atoms
C               (given on the next card) is to be constrained
C
C
C     -7.1-  
C       imol,iatom (16I5) (repeat if more than 8  centers
C
C    the list (ngrp long) of the atom indices of those atoms to be
C    constrained to the charge specified on the previous card.
C
c          blank to end
C
C------------------------------------------------------------------------
c  -8th-
c       intermolecular charge constraints  (atoms must sum to the 
c                                           specified value)
c       same format as indvidual molecule constraints
c       blank to end
c
C------------------------------------------------------------------------
c
c -9th- 
c      Multiple molecule constraints....constrain atoms on i to be
c                                            the same as on j
c      NGRP (I5) number of constaints 
C      (imol,iatom) (16I5) (repeat card if more than 8 groups)
c
c      blank to end
c
C------------------------------------------------------------------------
c
c
C  Unit 3 (qin) input of replacement charges if requested 
c  iqopt = 2,3
c
c       (8f10.6)  (i = 1,iuniq)
c
c-------------------------------------------------------------
c  Unit 4 input if new weight factors if requested
c
c    (i5)  nqwt  number of new weights to cycle thru
c    (f10.5)  new weights (nqwt lines)
c
c--------------------------------------------------------------
C
C Unit 10 input of ESP's  (mandatory)
C
C      natoms,nesp (2i5)
C              X , Y , Z  .   FORMAT (17X,3E16.7)
C      QUPOT , X , Y , Z  .   FORMAT (1X,4E16.7)
C
C          QUPOT = THE QUANTUM MECHANICAL ELECTROSTATIC
C                  POTENTIAL ( A.U )
C
C          X,Y,Z = THE COORDINATE AT WHICH THE POTENTIAL
C                  IS CALCULATED ( A.U )
C
C      NOTE : THE PROGRAM G80UCSF WRITES IN THIS FORMAT BUT THE
C             OUTPUT OF G90 MUST BE TRANSLATED (PROGRAM BOHR).
C
C--------------------------------------------------------------
C
c
c    usage: resp -i input -o output -p punch -q qin -t qout \
c                -e espot -w qwts -s esout 
c
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      integer icycle
      character*8   TITLE,    keywd
      parameter (maxq   = 8000)
      parameter (maxlgr = 900)
      parameter (maxmol = 400)
      COMMON/IOSTUF/inopt,ioutopt,IQOPT,iunits
      common /files/ input,output,qin,qout,punch,espot,qwts,esout,
     .               owrite
      character*80 input,output,qin,qout,punch,espot,qwts,esout
      character owrite
      COMMON/INFOA/NAT, IUNIQ,NESP,natpl1, ihfree,irstrnt
      COMMON/RUNLAB/TITLE(10), keywd( 4,4)
      COMMON/ESPCOM/apot(maxq,maxq), bpot(maxq), grad(maxq),
     &               awt(maxq,maxq), bwt(maxq), ssvpot,chipot,vavrg
      COMMON/CALCUL/ QCAL(maxq),a(maxq,maxq),b(maxq),
     & qwtval(maxq),iwttyp(maxq),iqcntr(maxq)
      common/LAGRNG/ grpchg(maxlgr), lgrcnt(maxlgr,maxq), nlgrng
      COMMON/ORIG/q0(maxq),CRD(3,maxq),IVARY(maxq),IZAN(maxq),qwt,q0tot
      COMMON/worker/awork(maxq,maxq),bwork(maxq),scr1(maxq),iscr1(maxq)
      COMMON/propty/ CO(3,maxq), CMAS(3), DIPOL(3), dipmom, QUAD(6)
      COMMON/mltmol/ wtmol(maxmol), moleqv(4,maxmol), ibeg(maxmol),
     &               iend(maxmol), nmol
C
C
c get the file names
c
      do jn = 1,maxq
         q0(jn) = 0.0d0
      enddo
      call filein
      call amopen(5,input,'O','F','R')
C
c read the atomic centers and q0's (readin), then read the potential inf
c
      call readin
c
c if its a multiple molecule run (nmol>0), do mult. mol. input
c
      if( nmol .gt. 1 )call mult_mol
c
c center & reorient molecule once in preparation for dipole & quadrupole
c
      if( nmol .eq. 1 ) call reornt
c
c read in the qm esp, forming the matrices apot(awt) and bpot(bwt)
c
      call matpot
c
c process the input (freezing, equivalencing charges)
c
      call data_prep
c
c set up cycle control structure: if icycle .gt. 0, come back to stmt 10
c subroutine cycle and read new "qwt"
c
c  icycle is initially set in readin 
c  subsequently decremented in cycle
c
      icycle= 0
c
c call cycle to see if we are supposed to cycle. reset icycle as needed
c
   10 continue
      call cycle(icycle)
c
      if( irstrnt .eq. 2 ) then
c
c if irstrnt= 2 then we just want to compare esp's to q0's
c
        do k= 1, iuniq
           qcal(k) = q0(k)
        enddo
        qwt= 0.0d0
      else
c 
c do the charge fitting
c
        call charge_opt
      endif
c
c calculate residuals sum-of-squares (chi-square) for the esp's
c
      call evlchi( ssvpot, bpot, apot, qcal, iuniq, maxq, chipot)
c
c now calculate and print dipole and quadrupole moments
c
      if(nmol .eq. 1) call elec_mom
c
c now punch short summary of charges & important evaluation criteria
c
      call pun_sum
c
      if( icycle .ne. 0 ) go to 10
c
c now calculate and print sum-of-squares, sigma, and rms
c
      call pot_out
c
      if( ioutopt .eq. 1 ) then
c 
c write the coords, old esps, new esps and residuals
c
         call wrt_pot
      endif
c
      END
C-----------------------------------------------------------------------
      SUBROUTINE readin
c
C-----------------------------------------------------------------------
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      parameter (maxq   = 8000)
      parameter (maxlgr = 900)
      parameter (maxmol = 400)
      character *80 card
      COMMON/IOSTUF/inopt,ioutopt,IQOPT,iunits
      COMMON/INFOA/NAT, IUNIQ,NESP,natpl1, ihfree,irstrnt
      COMMON/RUNLAB/TITLE(10),keywd( 4,4)
      character*8   TITLE,    keywd
      COMMON/ESPCOM/apot(maxq,maxq), bpot(maxq), grad(maxq),
     &               awt(maxq,maxq), bwt(maxq), ssvpot,chipot,vavrg
      COMMON/CALCUL/ QCAL(maxq), a(maxq,maxq), b(maxq),
     & qwtval(maxq), iwttyp(maxq), iqcntr(maxq)
      common/LAGRNG/ grpchg(maxlgr), lgrcnt(maxlgr,maxq), nlgrng
      COMMON/ORIG/q0(maxq),CRD(3,maxq),IVARY(maxq),IZAN(maxq),qwt,q0tot
      COMMON/worker/awork(maxq,maxq),bwork(maxq),scr1(maxq),iscr1(maxq)
      COMMON/propty/ CO(3,maxq), CMAS(3), DIPOL(3), dipmom, QUAD(6)
      COMMON/mltmol/ wtmol(maxmol), moleqv(4,maxmol), ibeg(maxmol),
     &               iend(maxmol), nmol
C-----------------------------------------------------------------------
      common /files/ input,output,qin,qout,punch,espot,qwts,esout,
     .               owrite
      character*80 input,output,qin,qout,punch,espot,qwts,esout
      character owrite
c
      namelist /cntrl/
     &  ich, INOPT, ioutopt, iuniq, nmol ,IQOPT, ihfree,  qwt,
     &  irstrnt,iunits
C
      UNITS = 1.D0/0.529177249d0
c
      do i= 1,maxlgr
        do j= 1,maxq
           lgrcnt(i,j)= 0
        enddo
      enddo
c
      nlgrng= 0
c
c
c start of molecule input
c
      READ(5,1000) (TITLE(I),I=1,10)
 1000 FORMAT(10A8)
      WRITE(6,1010) (TITLE(I),I=1,10)
 1010 FORMAT(/,t2,'-----------------------------------------------',
     $       /,t2,'     Restrained ESP Fit 2.3  Amber 4.1',
     $       /,t2,'-----------------------------------------------',
     $       /,t2,10A8, 
     $       /,t2,'-----------------------------------------------'/) 
c 
c read in charge, number of charge centers, and control parameters 
c
      ich = 0
      iuniq = 0
      nmol = 1
      IQOPT = 0
      irstrnt = 1
      ihfree = 1
      qwt = 0.0005d0
      iunits = 0
c
      do 7 icard=1,1000
        read(5,'(a80)',end=10) card
        if (card(3:7).eq.'cntrl') go to 9
    7 continue
    9 backspace (5)
      read(5,cntrl,end=10)
      go to 20
   10 continue
         write(6,'(''Sorry, you must use namelist input'')')
         stop
   20 continue
      WRITE(6,1030) INOPT,ioutopt,nmol,IQOPT,
     $ ihfree,irstrnt,iunits,qwt
 1030 FORMAT(
     $       /t2,'inopt       = ',I5,'   ioutopt     = ',I5,
     $       /t2,'nmol        = ',I5,'   iqopt       = ',I5,
     $       /t2,'ihfree      = ',I5,'   irstrnt     = ',I5,
     $       /t2,'iunits      = ',i5,'   qwt         = ',f12.8)
c
c if nmol > 1, this is a multiple molecule run
c
c and so we should leave this routine now because routine mult_mol
c is responsible for the rest of the multiple-molecule reading in.
c
      if( nmol .gt. 1 ) then
        return
      endif
c
c read in fitting weight for q0 and esp point weighting
c
      READ(5,'(f10.0)') wtmol(1) 
      write(6,'(t2,''wtmol(1) = '',f12.6)')wtmol(1)
      READ(5,1000) (TITLE(I),I=1,10)
      write(6,'(t2,''subtitle:'',/ /,10a8)')(TITLE(I),I=1,10)
      read(5,'(2i5)')ich,iuniq
      write(6,'(''ich = '',i3,''  iuniq = '',i3)')ich,iuniq
      ibeg(1) = 1
      iend(1) = iuniq
      wtmol(1) = 1.d0
c
c
c readin  this is a single-molecule run 
c  
c readin  read in nuclear positions crd(i), initial charges q0(i)
c readin  convert angstroms to bohrs
c
      DO 12 I=1,iuniq
        READ(5,'(2i5)') IZAN(I),IVARY(I)
        write(6,'(3i5)') i,IZAN(I),IVARY(I)
   12 CONTINUE
 9708 FORMAT(2I5)
 9709 FORMAT(2I5)
c 
c
c read in lagrange (charge) constraints
c
      call lagrange( ICH, ibeg(1),iend(1), nmol)
c
c
c replacement initial charges q0 from unit IUNTQ0 if IQOPT=2
c
      if( IQOPT .gt. 1) then
        call amopen(3,qin,'O','F','R')
        WRITE(6,'(t2,''new q0 values to be read'' ,i4)') iuniq
c
c
        READ(3,'(8f10.6)',end=55,err=55) (Q0(I),i=1,iuniq)
        CLOSE(3)
        go to 59
c
c now is a simple trap for when not enough replacement q0 are given.
c tactic: just keep going with old q0 (assume IQOPT=2 was not intended)
c
   55 WRITE(6,'(t2,a,/,t2,a)')
     .   ' not enough (possibly none) q0 are given in file',
     .   ' ESP.Q0, so the remaining old ones will be used.'
   59 continue
      endif
c
c end of "replacement initial charge" section.
c
c set initial charges to 0; done if IQOPT=1
c
      if( IQOPT .eq. 1 ) then
        WRITE(6,'(t2,''IQOPT=1, all q0 values will be set to 0''/)')
        DO I=1,iuniq
           Q0(I)= 0.0d0
        enddo
      endif
c
      WRITE (6,9088)
 9088 FORMAT(/,2X,38(2H--),/,2X,'   ATOM   ',20X,  'COORDINATES',25X,
     $                             'CHARGE',/,23X,'X',13X, 'Y',
     $                            16X,'Z',/,2X,38(2H--))
      WRITE(6,9128)
 9128 FORMAT(2X,38(2H--),/)
      WRITE (6,9168) ICH,iuniq,qwt
 9168 FORMAT(/t2,'Charge on the molecule(ich) =',I5,
     $       /t2,'Total number of atoms (iuniq)     =',I5,
     $       /t2,'Weight factor on initial charge restraints(qwt)='
     $           ,d16.5,/)
c
c charge constraint info
c
      write(6,'(/t2,'' there are'',i3,'' charge constraints:'')')nlgrng
      write(6,'(/)')
      do 165 i= 1, iuniq
        write(6,'(t2,i5,5x,6(20i3,/,10x),20i3)')
     $   i,(lgrcnt(j,i), j= 1,nlgrng)
  165 continue
c     write(6,'(/t2'' charge: '',7f10.3)') (grpchg(i), i=1,nlgrng)
c
      IF (iuniq .LE. maxq ) RETURN
      WRITE (6,'(t2,''Number of atoms exceeds program dimensions'')')
      stop
      END
C------------------------------------------------------------------------
      SUBROUTINE mult_mol 
C-----------------------------------------------------------------------
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      parameter (maxq   = 8000)
      parameter (maxlgr = 900)
      parameter (maxmol = 400)
      COMMON/IOSTUF/inopt,ioutopt,IQOPT,iunits
      COMMON/INFOA/NAT, IUNIQ,NESP,natpl1, ihfree,irstrnt
      COMMON/RUNLAB/TITLE(10), keywd( 4,4)
      character*8   TITLE,     keywd
      COMMON/ESPCOM/apot(maxq,maxq), bpot(maxq), grad(maxq),
     &               awt(maxq,maxq), bwt(maxq), ssvpot,chipot,vavrg
      COMMON/CALCUL/ QCAL(maxq), a(maxq,maxq), b(maxq),
     & qwtval(maxq), iwttyp(maxq), iqcntr(maxq)
      common/LAGRNG/ grpchg(maxlgr), lgrcnt(maxlgr,maxq), nlgrng
      COMMON/ORIG/q0(maxq),CRD(3,maxq),IVARY(maxq),IZAN(maxq),qwt,q0tot
      COMMON/worker/awork(maxq,maxq),bwork(maxq),scr1(maxq),iscr1(maxq)
      COMMON/propty/ CO(3,maxq), CMAS(3), DIPOL(3), dipmom, QUAD(6)
      COMMON/mltmol/ wtmol(maxmol), moleqv(4,maxmol), ibeg(maxmol),
     &               iend(maxmol), nmol
C-----------------------------------------------------------------------
      integer itmp(maxq),imoll(maxq)
      common /files/ input,output,qin,qout,punch,espot,qwts,esout,
     .               owrite
      character*80 input,output,qin,qout,punch,espot,qwts,esout
      character owrite
      DATA ONE,ZERO/1.0D0,0.0D0/
c
c this routine reads in multiple molecule input.  In routine readin
c it has already read the control variable input for the run, namely:
c ICH,IUNIQ,INOPT,IQOPT,ihfree, irstrnt, nlgrng, nmol
c where nmol > 0 caused this routine to be called.
c The input form for the other molecules is that their entire control
c decks are appended to the initial 2 control lines just read in,
c each control deck separated by a blank line, and then comes the
c multiple-molecule specific input, which is
c  - equivalencing of centers between molecules in the series
c  - the lagrange constraints to be applied between molecules
c
c the control characters read in the individual job decks are ignored
c except for ICH, and icntrs.  The lagrange (charge) constraints
c contained in the individual-molecule inputs ARE included.
c
c NOTE: the following are NOT implemented:
c       - output QM/calculated esp's (ioutOPT=1)
c
 1000 FORMAT(10A8)
 1010 FORMAT(10A8)
 1030 FORMAT(/,t2,'Total charge (ich):',I3,
     *       /,t2,'Number of centers:',I3)
 9708 FORMAT(I5,6x,4F12.6,i5,i5,f10.5)
      UNITS = 1.D0/0.529177249d0
      imol  = 0
      iuniq = 0
      mmlgr= nlgrng
      nlgrng= 0
c
      WRITE(6,'(/,t2,a,i3,a)')
     .   '%RESP-I-MULT_MOL,  multiple-molecule run of ', 
     .   nmol, ' molecules'
c
      do imol= 1, nmol
c
c read in the molecule weight and control variables
c  - the lagrange constraints to be applied between molecules
c
         READ(5,'(f10.5)') wtmol(imol)
         WRITE(6,'(/,t2,a,i3,a,f10.3)')
     .      'Reading input for molecule ', imol,
     .      ' weight:', wtmol(imol)
c
         READ(5,1000) (TITLE(I),I=1,10)
         WRITE(6,1010) (TITLE(I),I=1,10)
c
c read in charge, number of charge centers, and control parameters
c
         READ(5,'(2i5)') ICH,icntrs
         WRITE(6,1030) ICH, icntrs
c
c read in fitting weight for q0 and esp point weighting
c
c now some book-keeping: IUNIQ is the global variable for the total
c number of centers over all molecules.  The first center of this
c mol therefore starts in IUNIQ+1 and goes to IUNIQ+icntrs.
c
         ibeg(imol)= iuniq+1
         iend(imol)= iuniq+icntrs
c
c trap for having too many centers
c
         if( iend(imol) .gt. maxq ) then
           write (6,'(t2,''ERROR: more than '',i5,'' centers'')') maxq
           stop
         endif
c
c Read in nuclear positions crd(i), initial charges q0(i), and ivary(i)
c Since IVARY(i) is supposed to correspond to a center-number in the
c same molecule, this has to be adjusted to IVARY(i)+ibeg(imol)-1
c convert angstroms to bohrs if necessary
C
         DO I= ibeg(imol),iend(imol)
            READ(5,'(2i5)') IZAN(I), IVARY(I)
            write(6,'(3i5)') i,IZAN(I), IVARY(I)
            if (IVARY(i) .gt. 0) IVARY(i)= IVARY(i)+ibeg(imol)-1
         enddo
c
c now reset IUNIQ to IUNIQ+icntrs
c
         iuniq= iend(imol)
c
c now read in the lagrange (charge) restraints for this molecule
c
         call lagrange(ICH, ibeg(imol), iend(imol), imol)
      enddo
c
c end of molecule input, now do other preparation stuff
c
c read past a blank line after the final molecule job deck and then
c read in inter-molecule lagrange (charge) constraints (mmlgr).
c The "-99" for the total charge tells lgrange to drop the total charge
c constraint
c
      call lagrange( -99, 1, iuniq, imol)
c
c  this is for different types of charge resetting according to IQOPT :
c
c  replacement initial charges q0 from unit 3 if IQOPT=1
c
      if( IQOPT .gt. 1 ) then
        call amopen(3,qin,'O','F','R')
        WRITE(6,'(t2,'' since IQOPT=1,'',i4,'' new q0 values'')') iuniq
        WRITE(6,'(t2,'' will be read in from file ESP.Q0 (unit 3)'')')
c
c now read in replacement charges
c
        READ(3,'(8f10.6)',end=55,err=55) (Q0(I),i=1,iuniq)
        CLOSE(3)
        goto 59
c
c now is a simple trap for when not enough replacement q0 are given.
c tactic: just keep going with old q0 (assume IQOPT=2 was not intended)
c
   55   WRITE(6,'(t2,a,/,t2,a)')
     .     'not enough (possibly none) q0 are given in file',
     .     'ESP.Q0 (unit 3), so the remaining old ones will be used.'
   59   continue
      endif
c 
c end of "replacement initial charge" section.
c begin section: setting initial charges to 0; done if IQOPT=1
c
      if( IQOPT .eq. 1 ) then
        WRITE(6,'(/t2,''Iqopt =1: all q0 values will be set to 0'')')
        DO I=1,iuniq
           Q0(I)= 0.0
        enddo
      endif
c
c now carry out the inter-molecule equivalencing.  This is done by
c
c First : read the cards saying how many centers will be read in in the
c         next card. a zero means we have finished input
c
c Second: read the first-occurrence-in-each-molecule of the centers to
c        be equivalenced.  
c
c        The specifcations MUST be in ascending order.
c
c        The expanding of the centers within each
c        molecule is based on the IVARY values for the individual mol.
c
c        if ivary for mol 2+ is zero it is replaced with the atom number
c        of mol 1.  
c
      write(6,'(t2,''--------------------------------'')')
      write(6,'(t2,''reading mult_mol constraint info'')')
      write(6,'(t2,''--------------------------------'')')
  600 read(5,'(i5)') ntmp1
      if( ntmp1 .gt. 0 ) then
c
        read(5,'(16i5)') (imoll(j),itmp( j), j= 1,ntmp1)
        write(6,'(16i5)') (imoll(j),itmp( j), j= 1,ntmp1)
        do i = 1,ntmp1
           icntrs = ibeg(imoll(i)) - 1
           itmp(i) = icntrs + itmp(i)
        enddo
        do i= 2,ntmp1
           IVARY( itmp(i))= itmp(1)
        enddo
        go to 600
      endif
      do i= 1,iuniq
        ntmp1= IVARY(i)
        if( ntmp1 .gt. 0 ) then
          ntmp2= IVARY(ntmp1)
          if( ntmp2 .gt. 0 ) then 
             IVARY(i)= ntmp2
          endif
        endif
      enddo
c
      WRITE (6,9088)
 9088 FORMAT(/,2X,10(2H--),/,5x,'Atom   Ivary',/,2X,10(2H--))
      icnt = 1
      jcnt = 1
      DO 1100 IAT = 1,iuniq
        WRITE (6,'(2i5)')IZAN(IAT),ivary(iat)
      jcnt = jcnt + 1
      if (jcnt.gt.iend(icnt))then
         write(6,'( )') 
         icnt = icnt + 1
      endif
 1100 CONTINUE
      WRITE(6,9128)
 9128 FORMAT(2X,38(2H--),/)
      WRITE (6,9168) iuniq,qwt
 9168 FORMAT(/t2,'Total number of atoms      =',I5,
     *       /t2,'Weight factor on initial charge restraints=',f10.6,/)

c charge constraint info
 
      write(6,'(/,t2,''There are'',i3,'' charge constraints'')')nlgrng
      return
      end
C-------------------------------------------------------------------
      SUBROUTINE lagrange( ncharge, ifirst, ilast, imol)
c
c read in and assign lagrange constraint pointers
c
c called from "readin" and "mult_mol"
c
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      parameter (maxq   = 8000)
      parameter (maxlgr = 900)
      parameter (maxmol = 400)
      COMMON/IOSTUF/inopt,ioutopt,IQOPT,iunits
      COMMON/INFOA/NAT, IUNIQ,NESP,natpl1, ihfree,irstrnt
      COMMON/RUNLAB/TITLE(10),keywd( 4,4)
      character*8   TITLE,    keywd
      COMMON/ESPCOM/apot(maxq,maxq), bpot(maxq), grad(maxq),
     &               awt(maxq,maxq), bwt(maxq), ssvpot,chipot,vavrg
      COMMON/CALCUL/ QCAL(maxq), a(maxq,maxq), b(maxq),
     & qwtval(maxq), iwttyp(maxq), iqcntr(maxq)
      common/LAGRNG/ grpchg(maxlgr), lgrcnt(maxlgr,maxq), nlgrng
      COMMON/ORIG/q0(maxq),CRD(3,maxq),IVARY(maxq),IZAN(maxq),qwt,q0tot
      COMMON/worker/awork(maxq,maxq),bwork(maxq),scr1(maxq),iscr1(maxq)
      COMMON/propty/ CO(3,maxq), CMAS(3), DIPOL(3), dipmom, QUAD(6)
      COMMON/mltmol/ wtmol(maxmol), moleqv(4,maxmol), ibeg(maxmol),
     &               iend(maxmol), nmol
C-----------------------------------------------------------------------
      integer itmp(maxq),imoll(maxq)
c
c
c section: read in explicit Lagrange constraints on charge groups
c 
c 
c read in constraints: charge, center to which it applies
c
  10    continue
          read(5,'(i5,f10.5)') ntmp, gtemp
          if(ntmp.eq.0) go to 20
          nlgrng= nlgrng + 1
          if( (nlgrng) .gt. maxlgr) then
             write(6,'(t2,a,i3,/,t2,a,i3)')
     .          ' Too many charge-group constraints', nlgrng,
     .          ' Maximum allowed: ', maxlgr
             stop
          endif
          grpchg(nlgrng) = gtemp 
          read(5,'(16i5)') (imoll(j),itmp( j), j= 1,ntmp)
          write(6,'(16i5)') (imoll(j),itmp( j), j= 1,ntmp)
c
          do ii = 1,ntmp
             jmol = imoll(ii)
             icntrs = ibeg(jmol) - 1
             itmp(ii) = icntrs + itmp(ii)
          enddo
          do j= 1, ntmp
            if( itmp(j) .gt. 0 ) then
              itmp(j)= itmp(j) + ifirst -1
              lgrcnt(nlgrng, itmp(j))= 1
            elseif( itmp(j) .lt. 0 ) then
              itmp(j)= itmp(j) - ifirst +1
              lgrcnt(nlgrng, itmp(j))= -1
            endif
          enddo
        go to 10
   20 continue
c
c as long as ncharge is not -99, implement the "total charge" constraint
c
      if( ncharge .gt. -99 ) then
        nlgrng= nlgrng + 1
c
        if( nlgrng .gt. maxlgr) then
           write(6,'(t2,a,i3,/,t2,a,i3)')
     .          ' Too many charge-group constraints', nlgrng,
     .          ' Maximum allowed: ', maxlgr
           stop
        endif
        grpchg(nlgrng)= float( ncharge)
        do  j= ifirst, ilast
            lgrcnt(nlgrng,j)= 1
        enddo
      endif
      return
      end
c-----------------------------------------------------------------------
      SUBROUTINE matpot
c
c read in the electrostatic potential points used in the fitting,
c building up as we go the matrices for LU decomposition
c
c called from Main
c
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      parameter (maxq   = 8000)
      parameter (maxlgr = 900)
      parameter (maxmol = 400)
      COMMON/IOSTUF/inopt,ioutopt,IQOPT,iunits
      COMMON/INFOA/NAT, IUNIQ,NESP,natpl1, ihfree,irstrnt
      COMMON/RUNLAB/TITLE(10), keywd( 4,4)
      character*8   TITLE,         keywd
      COMMON/ESPCOM/apot(maxq,maxq), bpot(maxq), grad(maxq),
     &               awt(maxq,maxq), bwt(maxq), ssvpot,chipot,vavrg
      COMMON/CALCUL/ QCAL(maxq), a(maxq,maxq), b(maxq),
     & qwtval(maxq), iwttyp(maxq), iqcntr(maxq)
      common/LAGRNG/ grpchg(maxlgr), lgrcnt(maxlgr,maxq), nlgrng
      COMMON/ORIG/q0(maxq),CRD(3,maxq),IVARY(maxq),IZAN(maxq),qwt,q0tot
      COMMON/worker/awork(maxq,maxq),bwork(maxq),scr1(maxq),iscr1(maxq)
      COMMON/propty/ CO(3,maxq), CMAS(3), DIPOL(3), dipmom, QUAD(6)
      COMMON/mltmol/ wtmol(maxmol), moleqv(4,maxmol), ibeg(maxmol),
     &               iend(maxmol), nmol
      common /files/ input,output,qin,qout,punch,espot,qwts,esout,
     .               owrite
      character*80 input,output,qin,qout,punch,espot,qwts,esout
      character owrite
c
      DO k=1,iuniq
        bpot(k)= 0.0d0
        bwt(k) = 0.0d0
        DO j=1,iuniq
           apot(j,k)= 0.0d0
           awt(j,k) = 0.0d0
        enddo
      enddo
c
      call amopen(10,espot,'O','F','R')
c
      ssvpot= 0.0d0
      vavrg = 0.0d0
      vavtmp = 0.0d0
      ioff = 1
c
      if( nmol .gt. 0 ) then
        inmol= nmol
      else
        inmol= 1
        ibeg(1)= 1
        iend(1)= iuniq
        wtmol(1)= 1.0d0
      endif
c
      do imol= 1, inmol
        read(10,'(2i5)') inat,nesp
        WRITE(6,'(/,t2,a,i3,/,t2,a,i5,/,t2,a,i5)')
     .     'Reading esp"s for molecule ',imol,
     .     'total number of atoms      = ',inat,
     .     'total number of esp points = ',NESP
        WRITE(6,'(/ /,a)')
     .     ' center     X       Y       Z '
        do i = 1,inat
            read(10,52)crd(1,ioff),crd(2,ioff),crd(3,ioff)
            write(6,152)i,crd(1,ioff),crd(2,ioff),crd(3,ioff)
            ioff = ioff + 1
        enddo
   52      format(17X,3e16.7) 
  152      format(1X,i4,3e16.7) 
c
c build up matrix elements Ajk according to (SUMi 1/Rik SUMj 1/Rij)
c
        DO i= 1,nesp
           read(10, 53, err=940, end=930) espi, xi, yi, zi
   53      format(1X,4e16.7) 
           wt= wtmol(imol)
           wt2= wt*wt
           vavtmp = vavtmp + wt*espi
           ssvpot = ssvpot + wt2*espi*espi
           vavrg  = vavrg  + vavtmp/float(NESP)
           DO k= ibeg(imol),iend(imol)
              rik = sqrt( (xi - CRD(1,k))**2 + (yi - CRD(2,k))**2 +
     $                                      (zi - CRD(3,k))**2)
              rik = 1.d0/rik
              bpot(k)  = bpot(k) +     espi*rik
              bwt(k)   = bwt(k)  + wt2*espi*rik
              apot(k,k)= apot(k,k) +     rik*rik 
              awt(k,k) = awt(k,k)  + wt2*rik*rik 
              DO j= k+1, iend(imol)
                 rij = sqrt((xi - CRD(1,j))**2+(yi - CRD(2,j))**2+
     $                                         (zi - CRD(3,j))**2)
                 rij = 1.d0/rij
                 apot(j,k)= apot(j,k) +     rij*rik
                 awt(j,k) = awt(j,k)  + wt2*rij*rik
              enddo
           enddo
        enddo
      enddo
c
c symmetrize the potenitial and weighted potential matrices
c
      DO k=1,iuniq
         DO j= k+1,iuniq
            awt(k,j)= awt(j,k)
            apot(k,j)= apot(j,k)
         enddo
      enddo
      close(10)
      write(6,900)ssvpot
  900 format(t2,'Initial ssvpot =',f10.3/)
      return
c
  930 write(6,'(5X,''premature end of potential file'')')
      stop
  940 write(6,'(5X,a)') 
     .    'Error in reading potential input file (1X,4e16.7)'
      stop
      end
c-----------------------------------------------------------------------
      SUBROUTINE data_prep
c
c  setup pointers for groups of charges  based on "ivary" info
c
c  called from Main
C
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      parameter (maxq   = 8000)
      parameter (maxlgr = 900)
      parameter (maxmol = 400)
      COMMON/IOSTUF/inopt,ioutopt,IQOPT,iunits
      COMMON/INFOA/NAT, IUNIQ,NESP,natpl1, ihfree,irstrnt
      COMMON/RUNLAB/TITLE(10), keywd( 4,4)
      character*8   TITLE,     keywd
      COMMON/ESPCOM/apot(maxq,maxq), bpot(maxq), grad(maxq),
     &               awt(maxq,maxq), bwt(maxq), ssvpot,chipot,vavrg
      COMMON/CALCUL/ QCAL(maxq), a(maxq,maxq), b(maxq),
     & qwtval(maxq), iwttyp(maxq), iqcntr(maxq)
      common/LAGRNG/ grpchg(maxlgr), lgrcnt(maxlgr,maxq), nlgrng
      COMMON/ORIG/q0(maxq),CRD(3,maxq),IVARY(maxq),IZAN(maxq),qwt,q0tot
      COMMON/worker/awork(maxq,maxq),bwork(maxq),scr1(maxq),iscr1(maxq)
      COMMON/propty/ CO(3,maxq), CMAS(3), DIPOL(3), dipmom, QUAD(6)
      COMMON/mltmol/ wtmol(maxmol), moleqv(4,maxmol), ibeg(maxmol),
     &               iend(maxmol), nmol
C***********************************************************************
c
c
c begin section: set lists for combined and frozen charges
c
c IVARY(i) = 0, it is a new charge center to be fitted
c IVARY(i) =+n, it is a charge center to be fitted with center n
c                    (center n must be a previous center entered with 
c                    IVARY(n) = 0
c IVARY(i) =-n, it is a frozen charge center to be kept at q0(i)
c
c************************************************************************
      NAT = 0
      do i= 1,iuniq
        if(IVARY(i) .eq. 0) then
           NAT= NAT + 1
           iqcntr( i)= NAT
        elseif(IVARY(i) .gt. 0) then
           iqcntr(i)= iqcntr(IVARY(i))
c
           if( iqcntr( IVARY(i)) .gt. NAT ) then
              write(6,'(t2,''data_prep: charge vary input is screwy'')')
              stop
           endif
        else
           iqcntr( i)= -1
        endif
      enddo
c
      WRITE (6,'(/t2,''Number of unique UNfrozen centers='',i5)') NAT
      if( NAT .eq. 0 ) then 
            write(6,'(t2,''ALL charges are frozen!!!'')')
      endif
c
c finish off list with Lagrange constraints
c
      do 150 i= 1,nlgrng
        iqcntr(iuniq+i)= nat + i
  150 continue
c
c set NATPL1 to the total number of row elements 
c (charges to be independantly fit + constraints )
c in fitting matrix
c
      natpl1= nat + nlgrng
c
c     write(6,'(t2,''iqcntr: '')')
c     write(6,'(20i3)')(iqcntr(jn),jn=1,iuniq+nlgrng)
c
c done adding Lagrange constraints to elements list
c
c red in charges must now be averaged 
c a posteriori averaging of replacement charges according
c              to current IVARY charge-combining pointers
c
      if( IQOPT .eq. 3 ) then
        do i= 1,iuniq-1
          qcntrs= q0(i)
          tmpctr= 1.0d0
          do j= i+1,iuniq
            if( IVARY(j) .eq. i ) then
              qcntrs= qcntrs + q0(j)
              tmpctr= tmpctr + 1.0d0
            endif
          enddo
          if(tmpctr .gt. 0.99d0 )then
             qcntrs= qcntrs/tmpctr
             q0(i)= qcntrs
             do j= i+1,iuniq
                if( IVARY(j) .eq. i ) q0(j)= qcntrs
             enddo
          endif
        enddo
      endif
      RETURN
      END
C-------------------------------------------------------------------
      SUBROUTINE matbld
c
c called from "chgopt"
c 
c build up matrices for LU decomposition:
c
c   stage 1: copy weighted matrices awt and bwt to work arrays awork and bwork
c            (which are destroyed in the LU decomp & back subst)
c
c   stage 2: if charge restraints are to be included,
c            then modify awork and bwork appropriately
c
c
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      parameter (maxq   = 8000)
      parameter (maxlgr = 900)
      parameter (maxmol = 400)
      COMMON/IOSTUF/inopt,ioutopt,IQOPT,iunits
      COMMON/INFOA/NAT, IUNIQ,NESP,natpl1, ihfree,irstrnt
      COMMON/RUNLAB/TITLE(10), keywd( 4,4)
      character*8   TITLE,           keywd
      COMMON/ESPCOM/apot(maxq,maxq), bpot(maxq), grad(maxq),
     &               awt(maxq,maxq), bwt(maxq), ssvpot,chipot,vavrg
      COMMON/CALCUL/ QCAL(maxq), a(maxq,maxq), b(maxq),
     & qwtval(maxq), iwttyp(maxq), iqcntr(maxq)
      common/LAGRNG/ grpchg(maxlgr), lgrcnt(maxlgr,maxq), nlgrng
      COMMON/ORIG/q0(maxq),CRD(3,maxq),IVARY(maxq),IZAN(maxq),qwt,q0tot
      COMMON/worker/awork(maxq,maxq),bwork(maxq),scr1(maxq),iscr1(maxq)
      COMMON/propty/ CO(3,maxq), CMAS(3), DIPOL(3), dipmom, QUAD(6)
      COMMON/mltmol/ wtmol(maxmol), moleqv(4,maxmol), ibeg(maxmol),
     &               iend(maxmol), nmol
C
      do k=1,iuniq
        b(k) = bwt(k)
        do J=1,iuniq
           a(j,k) = awt(j,k)
        enddo
      enddo
c
c fill in the final columns & rows of A with the Lagrange
c constraints which keep the charge on groups of atoms to a 
c constant 
c
c note index counters!
c
      do i=1,nlgrng
        b(iuniq+i)  = grpchg(i)
        do j= 1,iuniq+nlgrng
          a(iuniq+i,j)= float(lgrcnt(i,j))
          a(j,iuniq+i)= float(lgrcnt(i,j))
        enddo
      enddo
  450 continue
c
c add restraint to initial charge q0(i):
c
      call rstran
c
c build awork and bwork based on "combined and frozen centers" info:
c
c 1) frozen centers do not appear in the matrix of fitted charges
c 2) combined centers appear as one single charge center for fitting
c
c first, since we accumulate values, zero out awork & bwork up to natpl1
c (the independant + contraint number):
c
      do i= 1,natpl1
        bwork( i)   = 0.0d0
        awork( i, i)= 0.0d0
        do j= i+1,natpl1
          awork( j, i)= 0.0d0
          awork( i, j)= 0.0d0
        enddo
      enddo
c
c loop over all centers, building awork & bwork from A and
c B based on iqcntr: for each center, iqcntr(i) dictates which of
c the fitted charges it is and therefore where it goes in the matrices.
c If iqcntr(j) < 1, this center is a frozen charge and it is skipped as
c far as forming a row in awork, and its esp contribution is subtracted
c from bwork to take care of it's awork jth column-element for each i.
c
      do i= 1,iuniq+nlgrng
        icntr= iqcntr(i)
        if(icntr .ge. 1) then
c i is "active" 
          bwork(icntr)= bwork(icntr) + b(i)
          do j = 1,iuniq+nlgrng
            jcntr = iqcntr( j)
            if( jcntr .ge. 1 ) then
c j i "active"
              awork(icntr,jcntr)= awork(icntr,jcntr) + a(i,j)
            else
c j is  a frozen charge
              bwork(icntr)= bwork(icntr)       - q0(j)*a(i,j)
            endif
          enddo
        endif
      enddo
c
      RETURN
      END
c-----------------------------------------------------------------------
      SUBROUTINE rstran
c 
c routine to assign the retraint weights 
c to the diagonal of A and to B
c 
c called from "matbld"
c
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      parameter (maxq   = 8000)
      parameter (maxlgr = 900)
      parameter (maxmol = 400)
      COMMON/IOSTUF/inopt,ioutopt,IQOPT,iunits
      COMMON/INFOA/NAT, IUNIQ,NESP,natpl1, ihfree,irstrnt
      COMMON/RUNLAB/TITLE(10),keywd( 4,4)
      character*8   TITLE,    keywd
      COMMON/ESPCOM/apot(maxq,maxq), bpot(maxq), grad(maxq),
     &               awt(maxq,maxq), bwt(maxq), ssvpot,chipot,vavrg
      COMMON/CALCUL/ QCAL(maxq), a(maxq,maxq), b(maxq),
     & qwtval(maxq), iwttyp(maxq), iqcntr(maxq)
      common/LAGRNG/ grpchg(maxlgr), lgrcnt(maxlgr,maxq), nlgrng
      COMMON/ORIG/q0(maxq),CRD(3,maxq),IVARY(maxq),IZAN(maxq),qwt,q0tot
      COMMON/worker/awork(maxq,maxq),bwork(maxq),scr1(maxq),iscr1(maxq)
      COMMON/propty/ CO(3,maxq), CMAS(3), DIPOL(3), dipmom, QUAD(6)
      COMMON/mltmol/ wtmol(maxmol), moleqv(4,maxmol), ibeg(maxmol),
     &               iend(maxmol), nmol
C----------------------------------------------------------------------
c two kinds of restraint are available:
c
c a) a harmonic restraint to the initial charge.  Fine as long as there
c  aren't any large charges that SHOULD be large... these really feel a
c  strong force if they are restrained to a low value.
c
c b) a hyperbolic restraint to a charge of 0.  This gets asymptotic at
c  "large" values, so "large" charges aren't pulled down any stronger
c  than some (reasonable) limiting force.  This is a non-linear
c  weighting function, so the fit procedure is iterative.
c
c other options for restraints to initial charge q0(i):
c if requested, restrain the charges by modifying the sum-of-squares
c cost function derivative.  The scheme for doing this is as follows:
c
c if control variable ihfree > 0, let hydrogen charges float free
c                                   (i.e. reset their qwtval to 0.0).
c
c-----------------------------------------------------------------------
c
      do i = 1,iuniq
        qwtval(i)= qwt
        if(ihfree.gt.0.and. IZAN(i).eq.1) then
           qwtval(i)= 0.0D0
        endif
c
        if(irstrnt .eq. 0) then
          a(i,i)= a(i,i) + qwtval(i)
c
c q0 has the initial and/or frozen  charge
c
          b(i)  = b(i)   + qwtval(i)*q0(i)
        elseif (irstrnt .gt. 0 .and. qwtval(i) .gt. 0.1d-10) then
c
c use analytic gradient of the hyperbola 
c
c qcal has the current (calculated) charge
c
          qwtval(i) = qwt/sqrt(qcal(i)*qcal(i) + 0.01d0)
          a(i,i)= a(i,i) + qwtval(i)
        endif
      enddo
c
c  if all qwtval(i) are 0.0, no restraints so set irstrnt= -1
c
      ihit = 0
      do i= 1,iuniq
         if(qwtval(i) .gt. 0.1d-10 ) ihit = 1
      enddo
      if(ihit .eq. 0) irstrnt = -1
      return
      end
c------------------------------------------------------------------------
      SUBROUTINE cycle( icycle)
c
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      parameter (maxq   = 8000)
      parameter (maxlgr = 900)
      parameter (maxmol = 400)
      integer icycle, nqwt
      character*8   TITLE,    keywd
      COMMON/IOSTUF/inopt,ioutopt,IQOPT,iunits
      COMMON/INFOA/  NAT,IUNIQ,NESP,natpl1, ihfree,irstrnt
      COMMON/RUNLAB/ TITLE(10),keywd( 4,4)
      COMMON/ESPCOM/ apot(maxq,maxq), bpot(maxq), grad(maxq),
     &               awt(maxq,maxq), bwt(maxq), ssvpot,chipot,vavrg
      COMMON/CALCUL/ QCAL(maxq), a(maxq,maxq), b(maxq),
     &               qwtval(maxq), iwttyp(maxq), iqcntr(maxq)
      common/LAGRNG/ grpchg(maxlgr), lgrcnt(maxlgr,maxq), nlgrng
      COMMON/ORIG/   q0(maxq),CRD(3,maxq),IVARY(maxq),IZAN(maxq),qwt,q0tot
      COMMON/worker/ awork(maxq,maxq),bwork(maxq),scr1(maxq),iscr1(maxq)
      COMMON/propty/ CO(3,maxq), CMAS(3), DIPOL(3), dipmom, QUAD(6)
      COMMON/mltmol/ wtmol(maxmol), moleqv(4,maxmol), ibeg(maxmol),
     &               iend(maxmol), nmol
C-----------------------------------------------------------------------
      save nqwt
      common /files/ input,output,qin,qout,punch,espot,qwts,esout,
     .               owrite
      character*80 input,output,qin,qout,punch,espot,qwts,esout
      character owrite
c
      DATA ZERO/0.0D0/
c
c
c if INOPT=1, reads values new of qwt from unit 4 and 
c writes a summary of the resulting fit, 
c as well as a list of the fit charges.
c
      if( INOPT .lt. 1 ) return
      if( icycle .eq. 0 ) then
         nqwt= 0
c
c first pass
c
         call amopen(4,qwts,'O','F','R')
         read(4,'(i5)') nqwt
         if(nqwt.eq.0) then
            write(6,'('' subroutine icycle: INPUT ERROR...'')')
            write(6,'(a,a)')
     .         ' INOPT=1 so qwt cycling expected, but',
     .         ' reading non-zero nqwt failed'
            return
         endif
   37    READ(4,'(f10.5)') qwt
         icycle= 1
         write(6,'(t2,''cycle   1: weighting factor= '',f10.4)')qwt
      else
c
c rest of the time
c
         READ(4,'(f10.5)') qwt
         icycle= icycle + 1
         write(6,'(/t2,''cycle'',i4,'': weighting factor= '',f10.4)')
     &             icycle,qwt
         if( icycle .ge. nqwt ) icycle= 0
      endif
      return
      end
c-----------------------------------------------------------------------------
      SUBROUTINE reornt
c
c translates molecule to center of mass and 
c reorients it along principal axes
c in preparation for dipole and quadrupole
c  moment calculation.
C
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      parameter (maxq   = 8000)
      parameter (maxlgr = 900)
      parameter (maxmol = 400)
      COMMON/IOSTUF/inopt,ioutopt,IQOPT,iunits
      COMMON/INFOA/NAT, IUNIQ,NESP,natpl1, ihfree,irstrnt
      COMMON/RUNLAB/TITLE(10), keywd( 4,4)
      character*8   TITLE,     keywd
      COMMON/ESPCOM/apot(maxq,maxq), bpot(maxq), grad(maxq),
     &               awt(maxq,maxq), bwt(maxq), ssvpot,chipot,vavrg
      COMMON/CALCUL/ QCAL(maxq), a(maxq,maxq), b(maxq),
     & qwtval(maxq), iwttyp(maxq), iqcntr(maxq)
      common/LAGRNG/ grpchg(maxlgr), lgrcnt(maxlgr,maxq), nlgrng
      COMMON/ORIG/q0(maxq),CRD(3,maxq),IVARY(maxq),IZAN(maxq),qwt,q0tot
      COMMON/worker/awork(maxq,maxq),bwork(maxq),scr1(maxq),iscr1(maxq)
      COMMON/propty/ CO(3,maxq), CMAS(3), DIPOL(3), dipmom, QUAD(6)
      COMMON/mltmol/ wtmol(maxmol), moleqv(4,maxmol), ibeg(maxmol),
     &               iend(maxmol), nmol
C-----------------------------------------------------------------------
      DIMENSION IATOM(maxq),WT(110)
C
C     ---- ATOMIC WEIGHT ARRAY FOR CENTER OF MASS ----
C
C      20 elements were originally handled: H(1) - Ca(20)
C     103 elements are now considered:      H(1) - Lr(103)
C
C     Atomic weight from The Merck Index - Thirteeth edition
C     Merck & Co., INC., Whitehouse Station, NJ, 2001
C
C     F.-Y. Dupradeau & P. Cieplak
C     http://q4md-forcefieldtools.org/
C
      DATA ZERO/0.0D0/,BOHR/0.52917725D0/
      DATA (WT(I),I=1,104) /
     *                     0.0000D0,1.0079D0,4.0026D0,
     *                     6.9410D0,9.0122D0,10.8110D0,12.0107D0,
     *                    14.0067D0,15.9994D0,18.9984D0,20.1797D0,
     *                    22.9898D0,24.3050D0,26.9815D0,28.0855D0,
     *                    30.9738D0,32.0650D0,35.4530D0,39.9480D0,
     *                    39.0983D0,40.0780D0,44.9559D0,47.8670D0,
     *                    50.9415D0,51.9961D0,54.9380D0,55.8450D0,
     *                    58.9332D0,58.6934D0,63.5460D0,65.3900D0,
     *                    69.7230D0,72.6400D0,74.9216D0,78.9600D0,
     *                    79.9040D0,83.8000D0,85.4678D0,87.6200D0,
     *                    88.9058D0,91.2240D0,92.9064D0,95.9400D0,
     *                    97.9072D0,101.0700D0,102.9055D0,106.4200D0,
     *                    107.8682D0,112.4110D0,114.8180D0,118.7100D0,
     *                    121.7600D0,127.6000D0,126.9045D0,131.2930D0,
     *                    132.9054D0,137.3270D0,138.9055D0,140.1160D0,
     *                    140.9076D0,144.2400D0,144.9127D0,150.3600D0,
     *                    151.9640D0,157.2500D0,158.9253D0,162.5000D0,
     *                    164.9303D0,167.2590D0,168.9342D0,173.0400D0,
     *                    174.9670D0,178.4900D0,180.9479D0,183.8400D0,
     *                    186.2070D0,190.2300D0,192.2170D0,195.0780D0,
     *                    196.9665D0,200.5900D0,204.3833D0,207.2000D0,
     *                    208.9804D0,208.9824D0,209.9871D0,222.0176D0,
     *                    223.0197D0,226.0254D0,227.0277D0,232.0381D0,
     *                    231.0359D0,238.0289D0,237.0482D0,244.0642D0,
     *                    243.0614D0,247.0704D0,247.0703D0,251.0796D0,
     *                    252.0830D0,257.0951D0,258.0984D0,259.1010D0,
     *                    262.1097D0 /
C
C     ----- INITIALISE SOME VARIABLES -----
C
      XC = ZERO
      YC = ZERO
      ZC = ZERO
      DO 10 I = 1,iuniq
         IATOM(I) = IZAN(I)+1
   10 CONTINUE
C
C     ----- CALCULATE THE CENTER OF MASS -----
C
      CALL CMASS(XC,YC,ZC,CRD,IATOM,iuniq,WT,maxq)
      CMAS(1)= XC
      CMAS(2)= YC
      CMAS(3)= ZC
c convert center of mass from bohr to angstroms
      DO I = 1,3
         CMAS(I) = CMAS(I)*BOHR
      enddo
C
C     ----- MOVE THE ORIGIN TO CENTER OF MASS AND
C           FORM NEW COORDINATE -----
C
      CALL CMOVE(XC,YC,ZC,CRD,iuniq,CO,maxq)
C
C     ----- CALCULATE THE MOMENT OF INERTIA -----
C
      CALL MOMIN(CO,IATOM,iuniq,WT,maxq)
C
      RETURN
      END
C-----------------------------------------------------------------------
      SUBROUTINE elec_mom
c
C ROUTINE TO CALCULATE THE DIPOLE AND QUADRUPOLE MOMENTS 
C-----------------------------------------------------------------------
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      parameter (maxq   = 8000)
      parameter (maxlgr = 900)
      parameter (maxmol = 400)
      COMMON/IOSTUF/inopt,ioutopt,IQOPT,iunits
      COMMON/INFOA/NAT, IUNIQ,NESP,natpl1, ihfree,irstrnt
      COMMON/RUNLAB/TITLE(10), keywd( 4,4)
      character*8   TITLE,     keywd
      COMMON/ESPCOM/apot(maxq,maxq), bpot(maxq), grad(maxq),
     &               awt(maxq,maxq), bwt(maxq), ssvpot,chipot,vavrg
      COMMON/CALCUL/ QCAL(maxq), a(maxq,maxq), b(maxq),
     & qwtval(maxq), iwttyp(maxq), iqcntr(maxq)
      common/LAGRNG/ grpchg(maxlgr), lgrcnt(maxlgr,maxq), nlgrng
      COMMON/ORIG/q0(maxq),CRD(3,maxq),IVARY(maxq),IZAN(maxq),qwt,q0tot
      COMMON/worker/awork(maxq,maxq),bwork(maxq),scr1(maxq),iscr1(maxq)
      COMMON/propty/ CO(3,maxq), CMAS(3), DIPOL(3), dipmom, QUAD(6)
      COMMON/mltmol/ wtmol(maxmol), moleqv(4,maxmol), ibeg(maxmol),
     &               iend(maxmol), nmol
C***********************************************************************
      ZERO=0.0D0
      BOHR=0.52917725D0
      debye=2.541765d0
C
C calculate dipole moment
C
      DIPOL(1) =ZERO
      DIPOL(2) =ZERO
      DIPOL(3) =ZERO
      DO I =1,iuniq
        DIPOL(1) =DIPOL(1) +QCAL(I)*CRD(1,I)
        DIPOL(2) =DIPOL(2) +QCAL(I)*CRD(2,I)
        DIPOL(3) =DIPOL(3) +QCAL(I)*CRD(3,I)
      enddo
      CONTINUE
      dipmom= dsqrt( DIPOL(1)*DIPOL(1) + DIPOL(2)*DIPOL(2) +
     *                                               DIPOL(3)*DIPOL(3))
 
C     ----- CALCULATE THE QUADRUPOLE MOMENT -----
 
      CALL QUADM(CRD,QCAL,iuniq,QUAD,maxq)
 
C convert dipoles from a.u. to debyes, and quadrupoles to debye*angstroms
 
      DO I = 1,3
         DIPOL(I) = DIPOL(I)*debye
         QUAD(I) = QUAD(I)*debye*BOHR
         QUAD(I+3) = QUAD(I+3)*debye*BOHR
      enddo
      dipmom= dipmom*debye
 
      RETURN
      END
C***********************************************************************
      SUBROUTINE CMASS(XC,YC,ZC,C,IATOM,NATOM,WT,maxq)
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
 
c  called from "reornt"
 
C      THIS SUBROUTINE CALCULATES THE CENTER OF MASS OF THE
C      MOLECULE.
 
      DIMENSION C(3,maxq),IATOM(maxq),WT(2)
 
      DATA ZERO/0.0D0/
 
      SUMX = ZERO
      SUMY = ZERO
      SUMZ = ZERO
      SUM  = ZERO
      DO 3 I =1,NATOM
        INDEX=IATOM(I)
        SUMX = SUMX + C(1,I) * WT(INDEX)
        SUMY = SUMY + C(2,I) * WT(INDEX)
        SUMZ = SUMZ + C(3,I) * WT(INDEX)
    3 SUM = SUM + WT(INDEX)
      XC = SUMX/SUM
      YC = SUMY/SUM
      ZC = SUMZ/SUM
      RETURN
      END
C***********************************************************************
      SUBROUTINE CMOVE(XC,YC,ZC,C,NATOM,CO,maxq)
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
  
c called from "reornt"
 
C     THIS SUBROUTINE MOVES THE ORIGIN TO THE CENTER OF MASS.
 
      DIMENSION C(3,maxq),CO(3,maxq)
C
      DO 5 I=1,NATOM
      CO(1,I) = C(1,I) - XC
      CO(2,I) = C(2,I) - YC
      CO(3,I) = C(3,I) - ZC
    5 CONTINUE
      RETURN
      END
C***********************************************************************
      SUBROUTINE MOMIN(CO,IATOM,NATOM,WT,maxq)
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
C
c 
c called from  "reornt"
c
C     THIS SUBROUTINE CALCULATES THE MOMENTS OF INERTIA AND
C     THE PRINCIPAL AXES OF ROTATION OF THE MOLECULE.  IT THEN
C     REORIENTS THE MOLECULE ALONG THE PRINCIPAL AXES OF
C     ROTATION (WITH THE ORIGIN AT THE CENTER OF MASS) IN
C     PREPARATION FOR CALCULATION OF QUADRAPOLE MOMENT
C     COMPONENTS.
C
C
      DIMENSION D(3),AIN(3,3),S(3,3)
      DIMENSION CO(3,maxq),IATOM(maxq),WT(2)
C
      DATA ZERO /0.0D0/
C
      SXX=ZERO
      SYY=ZERO
      SZZ=ZERO
      SXY=ZERO
      SXZ=ZERO
      SYZ=ZERO
      DO 10 I=1,NATOM
        INDEX=IATOM(I)
        XX=CO(1,I)*CO(1,I)
        YY=CO(2,I)*CO(2,I)
        ZZ=CO(3,I)*CO(3,I)
        SXX=SXX + (WT(INDEX)*(YY + ZZ))
        SYY=SYY + (WT(INDEX)*(XX + ZZ))
        SZZ=SZZ + (WT(INDEX)*(XX + YY))
        SXY=SXY + (WT(INDEX)*CO(1,I)*CO(2,I))
        SXZ=SXZ + (WT(INDEX)*CO(1,I)*CO(3,I))
   10 SYZ=SYZ + (WT(INDEX)*CO(2,I)*CO(3,I))
      AIN(1,1)=SXX
      AIN(1,2)=-SXY
      AIN(1,3)=-SXZ
      AIN(2,1)=AIN(1,2)
      AIN(2,2)=SYY
      AIN(2,3)=-SYZ
      AIN(3,1)=AIN(1,3)
      AIN(3,2)=AIN(2,3)
      AIN(3,3)=SZZ
C
C     ----- CALCULATE PRINCIPAL AXES OF INERTIA -----
C     ----- EV ARE PRINCIPLE MOMENTS OF INERTIA -----
C
      CALL DIAGM(AIN,S)
C
C      ----- ARRANGE SMALLEST TO LARGEST -----
C
      DO 30 I=1,2
        I1=I + 1
        DO 30 K=I1,3
          IF(AIN(I,I)-AIN(K,K))30,30,20
   20     RET=AIN(I,I)
          AIN(I,I)=AIN(K,K)
          AIN(K,K)=RET
          DO 25 L=1,3
            D(L)=S(L,I)
            S(L,I)=S(L,K)
   25     S(L,K)=D(L)
   30 CONTINUE
      DO 35 I=1,NATOM
        XT=S(1,1)*CO(1,I) + S(2,1)*CO(2,I) + S(3,1)*CO(3,I)
        YT=S(1,2)*CO(1,I) + S(2,2)*CO(2,I) + S(3,2)*CO(3,I)
        ZT=S(1,3)*CO(1,I) + S(2,3)*CO(2,I) + S(3,3)*CO(3,I)
        CO(1,I)=XT
        CO(2,I)=YT
   35 CO(3,I)=ZT
C
C MOMENT OF INERTIA WITH THE PRINCIPAL AXES
C
      XPI=AIN(1,1)
      YPI=AIN(2,2)
      ZPI=AIN(3,3)
      RETURN
      END
C***********************************************************************
      SUBROUTINE DIAGM(AIN,S)
c
c  called from "momin"
c
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
C
C     THIS SUBROUTINE PERFORMS DIAGONALIZATION OF A ROTATION
C     MATRIX BY JACOBI ROTATION METHOD.  IT IS NECESSARY TO
C     OBTAIN THE MOMENTS OF INERTIA AND COORDINATES OF THE
C     PRINCIPAL ROTATIONAL AXES.  THIS SUBROUTINE IS FROM THE
C     DIAGONALIZATION SUBROUTINE IN MM2 WRITTEN BY M. MILLER.
C
      DIMENSION AIN(3,3),S(3,3)
C
      DATA ZERO,ONE,TWO/0.0D0,1.0D0,2.0D0/
      DATA THREE,PT5,TENP8/3.0D0,0.5D0,1.0D+08/
C
      I=1
      K=1
      VI=ZERO
   10 BD=ZERO
   20 DO 80 I=1,3
   30    DO 70 K=1,3
   40       IF(I-K)60,50,60
   50       S(I,K)=ONE
            GO TO 70
   60       S(I,K)=ZERO
            VI=VI + (AIN(I,K)*AIN(I,K))
   70    CONTINUE
   80 CONTINUE
      VI=DSQRT(VI)
      VF=VI/TENP8
      SGM=THREE
      V=VI
      IF(VI)280,280,90
   90 V=V/SGM
  100 M=2
  110 L=1
  120 IF(DABS(AIN(L,M))-V)210,130,130
  130 BD=ONE
      ALM=-AIN(L,M)
      UM=PT5*(AIN(L,L)-AIN(M,M))
      OMG=ALM/(DSQRT((ALM*ALM)+(UM*UM)))
      IF(UM)140,150,150
  140 OMG=-OMG
  150 SN=OMG/(DSQRT(TWO*(ONE+(DSQRT(ONE-OMG*OMG)))))
      CS=DSQRT(ONE-SN*SN)
      I=1
  160 C1=AIN(I,L)
      C2=AIN(I,M)
      AIN(I,L)=C1*CS-C2*SN
      AIN(I,M)=C1*SN+C2*CS
      C1=S(I,L)
      C2=S(I,M)
      S(I,L)=C1*CS-C2*SN
      S(I,M)=C1*SN+C2*CS
      IF(I-3)170,180,170
  170 I=I+1
      GO TO 160
  180 C1=AIN(L,L)
      C2=AIN(M,M)
      C3=AIN(L,M)
      C4=AIN(M,L)
      AIN(L,L)=C1*CS-C4*SN
      AIN(M,M)=C2*CS+C3*SN
      AIN(L,M)=C3*CS-C2*SN
      AIN(M,L)=AIN(L,M)
      I=1
  190 AIN(L,I)=AIN(I,L)
      AIN(M,I)=AIN(I,M)
      IF(I-3)200,210,200
  200 I=I+1
      GO TO 190
  210 IF(L-M+1)220,230,220
  220 L=L+1
      GO TO 120
  230 IF(M-3)240,250,240
  240    M=M+1
         GO TO 110
  250    IF(BD-ONE)260,270,260
  260       IF(V-VF)280,280,90
  270          BD=ZERO
               GO TO 100
  280 CONTINUE
      RETURN
      END
C------------------------------------------------------------------------
      SUBROUTINE QUADM( C, q, NATOM, QUAD, maxq)
 
c  called from "elec_mom"
 
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
 
C   THIS SUBROUTINE CALCULATES THE COMPONENTS OF THE QUADROPOLE MOMENT 
 
      DIMENSION C(3,maxq), q(maxq), QUAD(6)
 
      QXX=0.0d0
      QYY=0.0d0
      QZZ=0.0d0
      QXY=0.0d0
      QXZ=0.0d0
      QYZ=0.0d0

      DO 7 I=1,NATOM
         X2 = C(1,I)*C(1,I)
         Y2 = C(2,I)*C(2,I)
         Z2 = C(3,I)*C(3,I)
         RQ = X2 + Y2 + Z2
            QXX = QXX + Q(I)*( 3.d0* (C(1,I)*C(1,I)) - RQ )
            QYY = QYY + Q(I)*( 3.d0* (C(2,I)*C(2,I)) - RQ )
            QZZ = QZZ + Q(I)*( 3.d0* (C(3,I)*C(3,I)) - RQ )
            QXY = QXY + Q(I)*( 3.d0* (C(1,I)*C(2,I)) - RQ )
            QXZ = QXZ + Q(I)*( 3.d0* (C(1,I)*C(3,I)) - RQ )
            QYZ = QYZ + Q(I)*( 3.d0* (C(2,I)*C(3,I)) - RQ )
    7 CONTINUE
C
C STORE IN QUAD
C
      QUAD(1) = QXX
      QUAD(2) = QYY
      QUAD(3) = QZZ
      QUAD(4) = QXY
      QUAD(5) = QXZ
      QUAD(6) = QYZ
C
      RETURN
      END
C***********************************************************************
      subroutine filein
c
      implicit double precision (a-h,o-z)
c
c     OUTPUT: (to common)
c
      common /files/ input,output,qin,qout,punch,espot,qwts,esout,
     .               owrite
      character*80 input,output,qin,qout,punch,espot,qwts,esout
      character owrite
c
      character *80 arg
c
      integer iarg, narg
      input = 'input'       ! -i
      output = 'output'     ! -o
      punch = 'punch'       ! -p
      qin= 'qin'            ! -q
      qout= 'qout'          ! -t 
      espot = 'espot'       ! -e
      qwts = 'qwts'         ! -w
      esout = 'esout'       ! -s
c
c     --- default for output files: 'N'ew
c
      owrite = 'N'
c
c     --- get com line arguments ---
c
      indx = iargc()
      iarg = 0
      if (indx.eq.iarg) goto 20
   10 continue
           iarg = iarg + 1
           call getarg(iarg,arg)
           if (arg .eq. '-O') then
                owrite = 'U'
           elseif (arg .eq. '-i') then
                iarg = iarg + 1
                call getarg(iarg,input)
           elseif (arg .eq. '-o') then
                iarg = iarg + 1
                call getarg(iarg,output)
           elseif (arg .eq. '-p') then
                iarg = iarg + 1
                call getarg(iarg,punch)
           elseif (arg .eq. '-q') then
                iarg = iarg + 1
                call getarg(iarg,qin)
           elseif (arg .eq. '-t') then
                iarg = iarg + 1
                call getarg(iarg,qout)
           elseif (arg .eq. '-e') then
                iarg = iarg + 1
                call getarg(iarg,espot)
           elseif (arg .eq. '-s') then
                iarg = iarg + 1
                call getarg(iarg,esout)
           elseif (arg .eq. '-w') then
                iarg = iarg + 1
                call getarg(iarg,qwts)
           else
                if (arg .eq. ' ') go to 20
                write(6,'(/,5x,a,a)') 'unknown flag: ',arg
                write(6,9000)
                stop
           endif
      if (iarg .lt. indx) go to 10
c
   20 continue
      narg = iarg - 1
      if (narg .lt. 2) then
           write(6,9000)
           stop
      endif
c
      if(output .ne. 'screen') then
          call amopen(6,output,owrite,'F','W')
      endif
      return
 9000 format(/,t2,
     $'usage: resp [-O] -i input -o output -p punch -q qin -t qout','
     $   -e espot -w qwts -s esout ')
      end
c------------------------------------------------------------------------
      subroutine evlchi(ssvpot,bpot,apot,qcal,iuniq,maxq,chipot)

      implicit double precision (a-h,o-z)
      dimension bpot(maxq), apot(maxq,maxq), 
     $         qcal(maxq)
c
c called from Main
c
c Evaluate chi-square for linear function  yclci= sum-j(paramj*termij),
c where j= number of terms, paramj is the coefficient to termij, and
c chi-square is the merit function: chi-square= sum-i((yi-yclci)**2),
c where i is the number of data points for which y is known.
c
c To avoid going through all i data points every time, the chi-square
c function is expanded into: chi-square= sum-i(yi**2 - 2*yi*yclci + yclci**2),
c and re-expressed as sum-i(yi**2) - 2*sum-i(yi*yclci) + sum-i(yclci**2).
c The first term is calculated once as the data is read in (sum-i(yi**2)== ssy).
c The second and third term depend upon the parameters: for each parameter
c paramj, sum-i(yi*termij) is the jth element in xprod, and sum-i(yclci**2) is
c a row in apot where element ajk= sum-i(termij*termik).  These elements
c are also built up once as the (possibly large) set of data is read in.
c
      cross= 0.0d0
      ssyclc= 0.0d0
      do j= 1,iuniq
        cross= cross + qcal(j)*bpot(j)
        do k= 1,iuniq
          ssyclc= ssyclc + qcal(j)*qcal(k)*apot(j,k)
        enddo
      enddo
c
      chipot = ssvpot - 2.0d0*cross + ssyclc
c
      return
      end
c------------------------------------------------------------------------
      subroutine pun_sum
C************************************************************************
C                              AMBER                                   **
C                                                                      **
C                  Copyright (c) 1986, 1991, 1995,1997                 **
C             Regents of the University of California                  **
C                       All Rights Reserved.                           ** 
C                                                                      **
C  This software provided pursuant to a license agreement containing   **
C  restrictions on its disclosure, duplication, and use. This software **
C  contains confidential and proprietary information, and may not be   **
C  extracted or distributed, in whole or in part, for any purpose      **
C  whatsoever, without the express written permission of the authors.  **
C  This notice, and the associated author list, must be attached to    **
C  all copies, or extracts, of this software. Any additional           **
C  restrictions set forth in the license agreement also apply to this  **
C  software.                                                           **
C************************************************************************
c
c  called from Main
c
C***********************************************************************
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      parameter (maxq   = 8000)
      parameter (maxlgr = 900)
      parameter (maxmol = 400)
      COMMON/IOSTUF/inopt,ioutopt,IQOPT,iunits
      COMMON/INFOA/NAT, IUNIQ,NESP,natpl1, ihfree,irstrnt
      COMMON/RUNLAB/TITLE(10),keywd( 4,4)
      character*8   TITLE,    keywd
      COMMON/ESPCOM/apot(maxq,maxq), bpot(maxq), grad(maxq),
     &               awt(maxq,maxq), bwt(maxq), ssvpot,chipot,vavrg
      COMMON/CALCUL/ QCAL(maxq), a(maxq,maxq), b(maxq),
     & qwtval(maxq), iwttyp(maxq), iqcntr(maxq)
      common/LAGRNG/ grpchg(maxlgr), lgrcnt(maxlgr,maxq), nlgrng
      COMMON/ORIG/q0(maxq),CRD(3,maxq),IVARY(maxq),IZAN(maxq),qwt,q0tot
      COMMON/worker/awork(maxq,maxq),bwork(maxq),scr1(maxq),iscr1(maxq)
      COMMON/propty/ CO(3,maxq), CMAS(3), DIPOL(3), dipmom, QUAD(6)
      COMMON/mltmol/ wtmol(maxmol), moleqv(4,maxmol), ibeg(maxmol),
     &               iend(maxmol), nmol
C***********************************************************************
      common /files/ input,output,qin,qout,punch,espot,qwts,esout,
     .               owrite
      character*80 input,output,qin,qout,punch,espot,qwts,esout
      character owrite
c
c
      QCRTRN= SQRT(chipot/ssvpot)
      ssvtot = ssvpot
c
c calculate standard error of estimate and correlation coefficients
c
      SIGMA = SQRT(chipot/FLOAT(NESP))
c
c punch name, one-line summary, and charges:
c
      call amopen(7,punch,owrite,'F','W')
      WRITE(7,1110) (TITLE(I),I=1,10)
 1110 FORMAT(/,10A8)
      write(7, 1230) IQOPT, irstrnt, ihfree,qwt
 1230 format(/,'iqopt   irstrnt  ihfree     qwt'/,3(i3,4x),f12.6)
      write(7,1235)  QCRTRN, dipmom, (QUAD(I), I=1,3)
 1235 format(/t2,'rel.rms   dipole mom       Qxx      Qyy      Qzz',/
     $ t2,5f10.5)
      WRITE(7,1200)
 1200 FORMAT(/,10X,'Point charges before & after optimization',/,4X,
     .  'NO',3X,'At.No.',4x,'q0',11X,'q(opt)   IVARY  d(rstr)/dq ')
      icnt = 1
      jcnt = 1
      DO j=1,iuniq
      WRITE(7,1210) j,izan(j),q0(j), qcal(j), IVARY(j), qwtval(j)
      jcnt = jcnt + 1
      if (jcnt.gt.iend(icnt))then
         write(6,'( )') 
         icnt = icnt + 1
      endif
      enddo
 1210 format(2x,i4,2x,i4,1x,f10.6,5x,f10.6, i5, f12.6, f12.3)
c
      call amopen(19,qout,owrite,'F','W')
      write(19,'(8f10.6)') (Qcal(I),i=1,iuniq)
      close(unit=19)
c
      RETURN
      END
C---------------------------------------------------------------------
      SUBROUTINE POT_OUT
C************************************************************************
C                              AMBER                                   **
C                                                                      **
C                  Copyright (c) 1986, 1991, 1995,1997                 **
C             Regents of the University of California                  **
C                       All Rights Reserved.                           ** 
C                                                                      **
C  This software provided pursuant to a license agreement containing   **
C  restrictions on its disclosure, duplication, and use. This software **
C  contains confidential and proprietary information, and may not be   **
C  extracted or distributed, in whole or in part, for any purpose      **
C  whatsoever, without the express written permission of the authors.  **
C  This notice, and the associated author list, must be attached to    **
C  all copies, or extracts, of this software. Any additional           **
C  restrictions set forth in the license agreement also apply to this  **
C  software.                                                           **
C************************************************************************
c
c  called from Main
C
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      parameter (maxq   = 8000)
      parameter (maxlgr = 900)
      parameter (maxmol = 400)
      COMMON/IOSTUF/inopt,ioutopt,IQOPT,iunits
      COMMON/INFOA/NAT, iuniq,NESP,natpl1, ihfree,irstrnt
      COMMON/RUNLAB/TITLE(10),keywd( 4,4)
      character*8   TITLE,    keywd
      COMMON/ESPCOM/apot(maxq,maxq), bpot(maxq), grad(maxq),
     &               awt(maxq,maxq), bwt(maxq), ssvpot,chipot,vavrg
      COMMON/CALCUL/ QCAL(maxq), a(maxq,maxq), b(maxq),
     & qwtval(maxq), iwttyp(maxq), iqcntr(maxq)
      common/LAGRNG/ grpchg(maxlgr), lgrcnt(maxlgr,maxq), nlgrng
      COMMON/ORIG/q0(maxq),CRD(3,maxq),IVARY(maxq),IZAN(maxq),qwt,q0tot
      COMMON/worker/awork(maxq,maxq),bwork(maxq),scr1(maxq),iscr1(maxq)
      COMMON/propty/ CO(3,maxq), CMAS(3), DIPOL(3), dipmom, QUAD(6)
      COMMON/mltmol/ wtmol(maxmol), moleqv(4,maxmol), ibeg(maxmol),
     &               iend(maxmol), nmol
      DATA ZERO/0.0D0/,AU2CAL/627.5095D0/
C
C
C     ---- PRINT THE OPTIMIZED CHARGES AND COORDINATES ----
C
      WRITE(6,1110) (TITLE(I),I=1,10)
c
c print the charges
c
      WRITE(6,1200)
      icnt = 1
      jcnt = 1
      chge = 0.0
      DO j=1,iuniq
         WRITE(6,1210) j,izan(j),q0(j), qcal(j), IVARY(j), qwtval(j)
         chge = chge + qcal(j)
         jcnt = jcnt + 1
         if (jcnt.gt.iend(icnt))then
            write(6,'( )') 
            icnt = icnt + 1
         endif
      enddo
      write(6,'(t2,''Sum over the calculated charges: '',f10.3)')chge
c
c
      QCRTRN= SQRT(chipot/ssvpot)
c
c calculate standard error of estimate
c
      SIGMA = SQRT(chipot/FLOAT(NESP))
c
c now write all this stuff out
c
      WRITE(6,1040) ssvpot
      WRITE(7,1040) ssvpot
      WRITE(6,1050) chipot 
      WRITE(7,1050) chipot 
      WRITE(6,1080) SIGMA
      WRITE(7,1080) SIGMA
      WRITE(6,1090) QCRTRN
      WRITE(7,1090) QCRTRN
C
C     ----- PRINT THE DIPOLE , QUADRUPOLE AND CENTER OF MASS ----
C
      if(nmol.eq.1) then
         WRITE(6,1340)
         write(6,1350) ( CMAS(I), I=1,3)
         WRITE(6,1360)
         write(6,1370) ( DIPOL(I), I=1,3)
         write(6,1375) dipmom
         write(7,1375) dipmom
         WRITE(6,1380)
         write(6,1390) ( QUAD(I), I=1,3)
         write(6,1395) ( QUAD(I), I=4,6)
      endif
c
 1000 FORMAT(/ /,10X,'Point charges after optimization',/ /,4X,
     *'NO',15X,'X',15X,'Y',15X,'Z',10X, 'Qoptim',/)
 1010 FORMAT(2X,I4,2X,4(5X,F10.6))
 1040 FORMAT(/,8X,'Statistics of the fitting:',
     *       /,2x,'The initial sum of squares (ssvpot)',t50,f15.3)
 1050 FORMAT(2x,'The residual sum of squares (chipot)',t50,f15.3)
 1080 FORMAT(2x,
     *'The std err of estimate (sqrt(chipot/N))',t50,f15.5)
 1090 FORMAT(2x, 'ESP relative RMS (SQRT(chipot/ssvpot))',t50,f15.5)
 1110 FORMAT(/,10A8)
 1130 FORMAT(/,t2,'Net charge on the system =',F10.7)
 1200 FORMAT(/,10X,
     *    'Point Charges Before & After Optimization',/ /,4X,'no.',
     *    2x,'At.no.',4x,'q(init)',7X,'q(opt)     ivary    d(rstr)/dq')
 1210 format(t2,2i4, 2(5x,f10.6), i7, f15.6, f12.3)
 1340 FORMAT(/,t2,'Center of Mass (Angst.):',/)
 1350 FORMAT(t2,'X  =',F10.5,5X,' Y  =',F10.5,5X,' Z  =',F10.5)
 1360 FORMAT(/,t2,'Dipole (Debye):',/)
 1370 FORMAT(t2,'X  =',F10.5,5X,' Y  =',F10.5,5X,' Z  =',F10.5)
 1375 FORMAT(/,t2,'Dipole Moment (Debye)=',F10.5)
 1380 FORMAT(/,t2,'Quadrupole (Debye*Angst.):',/)
 1390 FORMAT(t2,'Qxx =',F10.5,5X,'QYY =',F10.5,5X,'QZZ =',F10.5)
 1395 FORMAT(t2,'Qxy =',F10.5,5X,'QXZ =',F10.5,5X,'QYZ =',F10.5)
c
      return
      end
c-------------------------------------------------------------------------
      SUBROUTINE wrt_pot
C************************************************************************
C                              AMBER                                   **
C                                                                      **
C                  Copyright (c) 1986, 1991, 1995,1997                 **
C             Regents of the University of California                  **
C                       All Rights Reserved.                           ** 
C                                                                      **
C  This software provided pursuant to a license agreement containing   **
C  restrictions on its disclosure, duplication, and use. This software **
C  contains confidential and proprietary information, and may not be   **
C  extracted or distributed, in whole or in part, for any purpose      **
C  whatsoever, without the express written permission of the authors.  **
C  This notice, and the associated author list, must be attached to    **
C  all copies, or extracts, of this software. Any additional           **
C  restrictions set forth in the license agreement also apply to this  **
C  software.                                                           **
C************************************************************************
c
c called from Main
c
c read in the electrostatic potential points used in the fitting,
c calculate esp using existing charges, and write out both esp's & residual
c
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      parameter (maxq   = 8000)
      parameter (maxlgr = 900)
      parameter (maxmol = 400)
      COMMON/IOSTUF/inopt,ioutopt,IQOPT,iunits
      COMMON/INFOA/NAT, iuniq,NESP,natpl1, Ihfree,irstrnt
      COMMON/RUNLAB/TITLE(10), keywd( 4,4)
      character*8   TITLE,     keywd
      COMMON/ESPCOM/apot(maxq,maxq), bpot(maxq), grad(maxq),
     &               awt(maxq,maxq), bwt(maxq), ssvpot,chipot,vavrg
      COMMON/CALCUL/ QCAL(maxq), a(maxq,maxq), b(maxq),
     & qwtval(maxq), iwttyp(maxq), iqcntr(maxq)
      common/LAGRNG/ grpchg(maxlgr), lgrcnt(maxlgr,maxq), nlgrng
      COMMON/ORIG/q0(maxq),CRD(3,maxq),IVARY(maxq),IZAN(maxq),qwt,q0tot
      COMMON/worker/awork(maxq,maxq),bwork(maxq),scr1(maxq),iscr1(maxq)
      COMMON/propty/ CO(3,maxq), CMAS(3), DIPOL(3), dipmom, QUAD(6)
      COMMON/mltmol/ wtmol(maxmol), moleqv(4,maxmol), ibeg(maxmol),
     &               iend(maxmol), nmol
      common /files/ input,output,qin,qout,punch,espot,qwts,esout,
     .               owrite
      character*80 input,output,qin,qout,punch,espot,qwts,esout
      character owrite
c
      DATA AU2CAL/627.5095d0/,BOHR/0.52917725d0/
c
c open the file containing the qm esp points & read in the no. of points
c
      call amopen(10, ESPOT,'O','F','R')
      rewind(10)
      call amopen(20, ESOUT,owrite,'F','W')
      read(10,'(2i5)') idum,nesp
      ssvkcl= ssvpot*au2cal*au2cal
      chikcl= chipot*au2cal*au2cal
      write( 20, '(i5,i6,4x,2f20.10)') nesp, izan(1), ssvkcl, chikcl
c
c build up matrix elements Ajk according to (SUMi 1/Rik SUMj 1/Rij)
c
      do i = 1,idum
         read(10,100, end=930)  xi, yi, zi
 100     format(17x,3e16.7)
      enddo
      do i= 1,nesp
         read(10,101, end=930) espqmi, xi, yi, zi
 101     format(1x,4e16.7)
         espclc= 0.0d0
         do k=1,iuniq
           Xik    = xi - CRD(1,k)
           Yik    = yi - CRD(2,k)
           Zik    = zi - CRD(3,k)
           espclc= espclc + qcal(k)/ SQRT( Xik*Xik + Yik*Yik + Zik*Zik)
         enddo
         vresid= espqmi - espclc
         xa= xi*BOHR
         ya= yi*BOHR
         za= zi*BOHR
         espclc= espclc*AU2CAL
         espqmi= espqmi*AU2CAL
         vresid= vresid*AU2CAL
         write( 20, '(3f10.5, 3f12.5)') xa,ya,za, espqmi,espclc,vresid
      enddo
c
      close(10)
      close(20)
c
      return
  930 write (6, *) ' unexpected eof in ', espot
      stop
      end
C-------------------------------------------------------------------
      SUBROUTINE charge_opt
c
c  driver for the charge determinization/optimizaton
c
c  called from Main
c
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
      parameter (maxq   = 8000)
      parameter (maxlgr = 900)
      parameter (maxmol = 400)
c
      COMMON/IOSTUF/inopt,ioutopt,IQOPT,iunits
      COMMON/INFOA/NAT, IUNIQ,NESP,natpl1, ihfree,irstrnt
      COMMON/RUNLAB/TITLE(10),keywd( 4,4)
      character*8   TITLE,    keywd
      COMMON/ESPCOM/apot(maxq,maxq), bpot(maxq), grad(maxq),
     &               awt(maxq,maxq), bwt(maxq), ssvpot,chipot,vavrg
      COMMON/CALCUL/ QCAL(maxq), a(maxq,maxq), b(maxq),
     & qwtval(maxq), iwttyp(maxq), iqcntr(maxq)
      common/LAGRNG/ grpchg(maxlgr), lgrcnt(maxlgr,maxq), nlgrng
      COMMON/ORIG/q0(maxq),CRD(3,maxq),IVARY(maxq),IZAN(maxq),qwt,q0tot
      COMMON/worker/awork(maxq,maxq),bwork(maxq),scr1(maxq),iscr1(maxq)
      COMMON/propty/ CO(3,maxq), CMAS(3), DIPOL(3), dipmom, QUAD(6)
      COMMON/mltmol/ wtmol(maxmol), moleqv(4,maxmol), ibeg(maxmol),
     &               iend(maxmol), nmol
      dimension qold(maxq)
      integer istat
c
      gs= 0.0d0
      irsave= 0
      nitern= 0
      do i= 1,maxq
         qold(i)= 0.0d0
      enddo
c
c qtol & maxit are criteria for convergence & maximum iterations for
c the non-linear optimizations.
c
c     qtol= 0.1d-4
      qtol= 0.1d-5
      maxit=  24
c
c only on first pass through this subroutine (indicated by nitern= 0),
c if irstrnt > 0, transfer irstrnt to irsave and reset irstrnt to 0,
c in order to get an initial guess using a harmonic constraint.  This is
c done so restraint subroutine (rstran) will use a harmonic restraint.
c
      if( irstrnt .gt. 0 ) then
        irsave= irstrnt
        irstrnt= 0
        WRITE(6, '(/,t2,a)')'Non-linear optimization requested.'
      endif
c
c now go do a "harmonic restraint" run, restraint= qwt(qcal(i)-q0(i))**2
c -- loop to convergence
c
  100 continue
         call matbld
c
c        solve (Ax = b) where A and b are input, x is solution
c                     awork x = bwork
c
c        the solution "x" is returned in "b" (bwork)
c
c        -- condition the matrix diagonal to avoid DGETRF() detecting
c           singularity
c
         do jn = 1,natpl1
           if (abs(awork(jn,jn)).lt. 1.d-10) awork(jn,jn) = 1.d-10
         enddo
c
         call DGETRF( NATPL1,NATPL1,awork,maxq,iscr1,istat)
         if(istat.lt. 0) then
           write(6,'('' chgopt: LU decomp has an illegal value'')')
           stop
         elseif(istat.gt. 0) then
           write(6,'('' chgopt: LU decomp gave almost-singular U'')')
           stop
         endif
c
         call DGETRS( 'N',NATPL1,1,awork,maxq,iscr1,bwork,NATPL1,istat)
         if(istat.ne. 0) then
           write(6,'('' chgopt: LU backsubst has an illegal value'')')
           stop
         endif
c
c        -- copy solution vector "bwork" to 'calculated charges' vector 
c           qcal
c
         do k= 1, iuniq
           icntr= iqcntr(k)
           if( icntr .ge. 1 ) then
c
c            -- new charge
c
             qcal(k) = bwork( icntr)
           else
c
c            -- frozen charge
c
             qcal(k) = q0(k)
           endif
         enddo
c
c        -- a quick check from rstrn: if irstrnt is now negative, 
c           there are no restraints because no qwtval(i) > 0.1e-10, 
c           so reset irsave= 0
c
         if (irstrnt .lt. 0) then
           irsave=0
           WRITE(6,'(/,t2,a,/,t2,a)')
     .        'WARNING: Restraints were requested, but',
     .        '         the restraint weights were all zero'
         endif
c
c        -- we're finished if it's only a "harmonic restraint" run, 
c           but if it's a non-linear optimization (irsave>0)... 
c           we've only just begun (i.e. we have our initial guess)
c
         if( irsave .le. 0 ) then
           return
         else
c
c          -- it's a non-linear optimization: reset irstrnt (to now 
c             calculate the proper non-linear restraint derivatives 
c             in routine rstran)
c
           irstrnt= irsave
         endif
c
c        -- begin iterative optimization loop with comparison of 
c           old & new charges; calculate the convergence and replace 
c           the old charges with the new
c
         qchnge= 0.0d0
         xuniq = dble(iuniq)
         do i= 1,iuniq
            qdiff = qcal(i) - qold(i)
            qchnge = qchnge + (qdiff*qdiff)
            qold(i) = qcal(i)
         enddo
c
c        -- hp compiler bug requires that xuniq be calcd
c           before loop 11/94
c
         qchnge = sqrt(qchnge) / xuniq
         write(6,'(t2,''qchnge ='',g20.10)')qchnge
c
c        -- if this is less than qtol then we're done
c
         if (qchnge .lt. qtol .and. nitern .gt. 1) then
           write(6,'(/t2,''Convergence in'',i5,'' iterations'')')nitern
           return
         elseif( nitern .ge. maxit ) then
c
           write(6, 
     $        '(t2,''after '',i5,'' iterations, no convergence!'')') 
     $        maxit
           return
         endif
c
c loop again
c
         nitern= nitern + 1
      go to 100
      end
C-----------------------------------------------------------------------
      subroutine amopen(lun,fname,fstat,fform,facc)

c     INPUT:
c
      integer lun
c        ... logical unit number
      character*(*) fname
c        ... file name (not used in VAX/VMS implementation)
      character*1 fstat
c        ... status code: "N", "O", or "U" = new, old, unk.
      character*1 fform
c        ... format code: "U", "F" = unform., form.
      character*1 facc
c        ... access code: "R", "W", "A" = read, read/write, append
c
c     THIS IS UNIX VERSION
c     Author: George Seibel
c     Rev 13-Jun-90:  add rewind after open.
 
c     INTERNAL:
 
      character*7 stat
c        ... status keyword
      character*11 kform
c        ... form keyword
      integer ios
c        ... i/o status variable
 
      if (fstat .eq. 'N') then
           stat = 'NEW'
      elseif (fstat .eq. 'O') then
           stat = 'OLD'
      elseif (fstat .eq. 'U') then
           stat = 'UNKNOWN'
      else
           write(6,'(/,2x,a,i4)')
     $           'amopen: bogus fstat, unit ', lun
           stop
      endif
c
      if (fform .eq. 'U') then
           kform = 'UNFORMATTED'
      elseif (fform .eq. 'F') then
           kform = 'FORMATTED'
      else
           write(6,'(/,2x,a,i4)')
     $           'amopen: bogus fform, unit', lun
           stop
      endif
c
      open(unit=lun,file=fname,status=stat,form=kform,iostat=ios)
c
      if (ios .ne. 0) then
           if (lun .eq. 6) then
                write(0,'(/,2x,a,i4,a,a)') 'Unit ', lun, 
     $                                    ' Error on OPEN: ',fname
                close(unit=0)
           else
                write(6,'(/,2x,a,i4,a,a)') 'Unit ', lun, 
     $                                    ' Error on OPEN: ',fname
                close(unit=6)
                write(0,'(/,2x,a,i4,a,a)') 'Unit ', lun, 
     $                                    ' Error on OPEN: ',fname
                close(unit=0)
           endif
           stop
      endif
      rewind(lun)
      return
      end
c----------------------------------------------------------------------
      SUBROUTINE DGETRF( M, N, A, LDA, IPIV, INFO )
c
c  -- LAPACK routine (version 2.0) --
c     Univ. of Tennessee, Univ. of California Berkeley, NAG Ltd.,
c     Courant Institute, Argonne National Lab, and Rice University
c     March 31, 1993
c
c     .. Scalar Arguments ..
      INTEGER            INFO, LDA, M, N
c     ..
c     .. Array Arguments ..
      INTEGER            IPIV( * )
      DOUBLE PRECISION   A( LDA, * )
c     ..
c
c  Purpose
c  =======
c
c  DGETRF computes an LU factorization of a general M-by-N matrix A
c  using partial pivoting with row interchanges.
c
c  The factorization has the form
c     A = P * L * U
c  where P is a permutation matrix, L is lower triangular with unit
c  diagonal elements (lower trapezoidal if m > n), and U is upper
c  triangular (upper trapezoidal if m < n).
c
c  This is the right-looking Level 3 BLAS version of the algorithm.
c
c  Arguments
c  =========
c
c  M       (input) INTEGER
c          The number of rows of the matrix A.  M >= 0.
c
c  N       (input) INTEGER
c          The number of columns of the matrix A.  N >= 0.
c
c  A       (input/output) DOUBLE PRECISION array, dimension (LDA,N)
c          On entry, the M-by-N matrix to be factored.
c          On exit, the factors L and U from the factorization
c          A = P*L*U; the unit diagonal elements of L are not stored.
c
c  LDA     (input) INTEGER
c          The leading dimension of the array A.  LDA >= max(1,M).
c
c  IPIV    (output) INTEGER array, dimension (min(M,N))
c          The pivot indices; for 1 <= i <= min(M,N), row i of the
c          matrix was interchanged with row IPIV(i).
c
c  INFO    (output) INTEGER
c          = 0:  successful exit
c          < 0:  if INFO = -i, the i-th argument had an illegal value
c          > 0:  if INFO = i, U(i,i) is exactly zero. The factorization
c                has been completed, but the factor U is exactly
c                singular, and division by zero will occur if it is used
c                to solve a system of equations.
c
c  =====================================================================
c
c     .. Parameters ..
      DOUBLE PRECISION   ONE
      PARAMETER          ( ONE = 1.0D+0 )
c     ..
c     .. Local Scalars ..
      INTEGER            I, IINFO, J, JB, NB
c     ..
c     .. External Subroutines ..
      EXTERNAL           DGEMM, DGETF2, DLASWP, DTRSM, XERBLA
c     ..
c     .. External Functions ..
      INTEGER            ILAENV
      EXTERNAL           ILAENV
c     ..
c     .. Intrinsic Functions ..
      INTRINSIC          MAX, MIN
c     ..
c     .. Executable Statements ..
c
c     Test the input parameters.
c
      INFO = 0
      IF( M.LT.0 ) THEN
         INFO = -1
      ELSE IF( N.LT.0 ) THEN
         INFO = -2
      ELSE IF( LDA.LT.MAX( 1, M ) ) THEN
         INFO = -4
      END IF
      IF( INFO.NE.0 ) THEN
         CALL XERBLA( 'DGETRF', -INFO )
         RETURN
      END IF
c
c     Quick return if possible
c
      IF( M.EQ.0 .OR. N.EQ.0 )
     $   RETURN
c
c     Determine the block size for this environment.
c
      NB = ILAENV( 1, 'DGETRF', ' ', M, N, -1, -1 )
      IF( NB.LE.1 .OR. NB.GE.MIN( M, N ) ) THEN
c
c        Use unblocked code.
c
         CALL DGETF2( M, N, A, LDA, IPIV, INFO )
      ELSE
c
c        Use blocked code.
c
         DO 20 J = 1, MIN( M, N ), NB
            JB = MIN( MIN( M, N )-J+1, NB )
c
c           Factor diagonal and subdiagonal blocks and test for exact
c           singularity.
c
            CALL DGETF2( M-J+1, JB, A( J, J ), LDA, IPIV( J ), IINFO )
c
c           Adjust INFO and the pivot indices.
c
            IF( INFO.EQ.0 .AND. IINFO.GT.0 )
     $         INFO = IINFO + J - 1
            DO 10 I = J, MIN( M, J+JB-1 )
               IPIV( I ) = J - 1 + IPIV( I )
   10       CONTINUE
c
c           Apply interchanges to columns 1:J-1.
c
            CALL DLASWP( J-1, A, LDA, J, J+JB-1, IPIV, 1 )
c
            IF( J+JB.LE.N ) THEN
c
c              Apply interchanges to columns J+JB:N.
c
               CALL DLASWP( N-J-JB+1, A( 1, J+JB ), LDA, J, J+JB-1,
     $                      IPIV, 1 )
c
c              Compute block row of U.
c
               CALL DTRSM( 'Left', 'Lower', 'No transpose', 'Unit', JB,
     $                     N-J-JB+1, ONE, A( J, J ), LDA, A( J, J+JB ),
     $                     LDA )
               IF( J+JB.LE.M ) THEN
c
c                 Update trailing submatrix.
c
                  CALL DGEMM( 'No transpose', 'No transpose', M-J-JB+1,
     $                        N-J-JB+1, JB, -ONE, A( J+JB, J ), LDA,
     $                        A( J, J+JB ), LDA, ONE, A( J+JB, J+JB ),
     $                        LDA )
               END IF
            END IF
   20    CONTINUE
      END IF
      RETURN
c
c     End of DGETRF
c
      END
c***********************************************************************
      SUBROUTINE DGETRS( TRANS, N, NRHS, A, LDA, IPIV, B, LDB, INFO )
c
c  -- LAPACK routine (version 2.0) --
c     Univ. of Tennessee, Univ. of California Berkeley, NAG Ltd.,
c     Courant Institute, Argonne National Lab, and Rice University
c     March 31, 1993
c
c     .. Scalar Arguments ..
      CHARACTER          TRANS
      INTEGER            INFO, LDA, LDB, N, NRHS
c     ..
c     .. Array Arguments ..
      INTEGER            IPIV( * )
      DOUBLE PRECISION   A( LDA, * ), B( LDB, * )
c     ..
c
c  Purpose
c  =======
c
c  DGETRS solves a system of linear equations
c     A * X = B  or  A_prime * X = B
c  with a general N-by-N matrix A using the LU factorization computed
c  by DGETRF.
c
c  Arguments
c  =========
c
c  TRANS   (input) CHARACTER*1
c          Specifies the form of the system of equations:
c          = "N":        A * X = B  (No transpose)
c          = "T":  A_prime * X = B  (Transpose)
c          = "C":  A_prime * X = B  (Conjugate transpose = Transpose)
c
c  N       (input) INTEGER
c          The order of the matrix A.  N >= 0.
c
c  NRHS    (input) INTEGER
c          The number of right hand sides, i.e., the number of columns
c          of the matrix B.  NRHS >= 0.
c
c  A       (input) DOUBLE PRECISION array, dimension (LDA,N)
c          The factors L and U from the factorization A = P*L*U
c          as computed by DGETRF.
c
c  LDA     (input) INTEGER
c          The leading dimension of the array A.  LDA >= max(1,N).
c
c  IPIV    (input) INTEGER array, dimension (N)
c          The pivot indices from DGETRF; for 1<=i<=N, row i of the
c          matrix was interchanged with row IPIV(i).
c
c  B       (input/output) DOUBLE PRECISION array, dimension (LDB,NRHS)
c          On entry, the right hand side matrix B.
c          On exit, the solution matrix X.
c
c  LDB     (input) INTEGER
c          The leading dimension of the array B.  LDB >= max(1,N).
c
c  INFO    (output) INTEGER
c          = 0:  successful exit
c          < 0:  if INFO = -i, the i-th argument had an illegal value
c
c  =====================================================================
c
c     .. Parameters ..
      DOUBLE PRECISION   ONE
      PARAMETER          ( ONE = 1.0D+0 )
c     ..
c     .. Local Scalars ..
      LOGICAL            NOTRAN
c     ..
c     .. External Functions ..
      LOGICAL            LSAME
      EXTERNAL           LSAME
c     ..
c     .. External Subroutines ..
      EXTERNAL           DLASWP, DTRSM, XERBLA
c     ..
c     .. Intrinsic Functions ..
      INTRINSIC          MAX
c     ..
c     .. Executable Statements ..
c
c     Test the input parameters.
c
      INFO = 0
      NOTRAN = LSAME( TRANS, 'N' )
      IF( .NOT.NOTRAN .AND. .NOT.LSAME( TRANS, 'T' ) .AND. .NOT.
     $    LSAME( TRANS, 'C' ) ) THEN
         INFO = -1
      ELSE IF( N.LT.0 ) THEN
         INFO = -2
      ELSE IF( NRHS.LT.0 ) THEN
         INFO = -3
      ELSE IF( LDA.LT.MAX( 1, N ) ) THEN
         INFO = -5
      ELSE IF( LDB.LT.MAX( 1, N ) ) THEN
         INFO = -8
      END IF
      IF( INFO.NE.0 ) THEN
         CALL XERBLA( 'DGETRS', -INFO )
         RETURN
      END IF
c
c     Quick return if possible
c
      IF( N.EQ.0 .OR. NRHS.EQ.0 )
     $   RETURN
c
      IF( NOTRAN ) THEN
c
c        Solve A * X = B.
c
c        Apply row interchanges to the right hand sides.
c
         CALL DLASWP( NRHS, B, LDB, 1, N, IPIV, 1 )
c
c        Solve L*X = B, overwriting B with X.
c
         CALL DTRSM( 'Left', 'Lower', 'No transpose', 'Unit', N, NRHS,
     $               ONE, A, LDA, B, LDB )
c
c        Solve U*X = B, overwriting B with X.
c
         CALL DTRSM( 'Left', 'Upper', 'No transpose', 'Non-unit', N,
     $               NRHS, ONE, A, LDA, B, LDB )
      ELSE
c
c        Solve A_prime * X = B.
c
c        Solve U_prime * X = B, overwriting B with X.
c
         CALL DTRSM( 'Left', 'Upper', 'Transpose', 'Non-unit', N, NRHS,
     $               ONE, A, LDA, B, LDB )
c
c        Solve L_prime * X = B, overwriting B with X.
c
         CALL DTRSM( 'Left', 'Lower', 'Transpose', 'Unit', N, NRHS, ONE,
     $               A, LDA, B, LDB )
c
c        Apply row interchanges to the solution vectors.
c
         CALL DLASWP( NRHS, B, LDB, 1, N, IPIV, -1 )
      END IF
c
      RETURN
c
c     End of DGETRS
c
      END
c***********************************************************************
      SUBROUTINE DGETF2( M, N, A, LDA, IPIV, INFO )
c
c  -- LAPACK routine (version 2.0) --
c     Univ. of Tennessee, Univ. of California Berkeley, NAG Ltd.,
c     Courant Institute, Argonne National Lab, and Rice University
c     June 30, 1992
c
c     .. Scalar Arguments ..
      INTEGER            INFO, LDA, M, N
c     ..
c     .. Array Arguments ..
      INTEGER            IPIV( * )
      DOUBLE PRECISION   A( LDA, * )
c     ..
c
c  Purpose
c  =======
c
c  DGETF2 computes an LU factorization of a general m-by-n matrix A
c  using partial pivoting with row interchanges.
c
c  The factorization has the form
c     A = P * L * U
c  where P is a permutation matrix, L is lower triangular with unit
c  diagonal elements (lower trapezoidal if m > n), and U is upper
c  triangular (upper trapezoidal if m < n).
c
c  This is the right-looking Level 2 BLAS version of the algorithm.
c
c  Arguments
c  =========
c
c  M       (input) INTEGER
c          The number of rows of the matrix A.  M >= 0.
c
c  N       (input) INTEGER
c          The number of columns of the matrix A.  N >= 0.
c
c  A       (input/output) DOUBLE PRECISION array, dimension (LDA,N)
c          On entry, the m by n matrix to be factored.
c          On exit, the factors L and U from the factorization
c          A = P*L*U; the unit diagonal elements of L are not stored.
c
c  LDA     (input) INTEGER
c          The leading dimension of the array A.  LDA >= max(1,M).
c
c  IPIV    (output) INTEGER array, dimension (min(M,N))
c          The pivot indices; for 1 <= i <= min(M,N), row i of the
c          matrix was interchanged with row IPIV(i).
c
c  INFO    (output) INTEGER
c          = 0: successful exit
c          < 0: if INFO = -k, the k-th argument had an illegal value
c          > 0: if INFO = k, U(k,k) is exactly zero. The factorization
c               has been completed, but the factor U is exactly
c               singular, and division by zero will occur if it is used
c               to solve a system of equations.
c
c  =====================================================================
c
c     .. Parameters ..
      DOUBLE PRECISION   ONE, ZERO
      PARAMETER          ( ONE = 1.0D+0, ZERO = 0.0D+0 )
c     ..
c     .. Local Scalars ..
      INTEGER            J, JP
c     ..
c     .. External Functions ..
      INTEGER            IDAMAX
      EXTERNAL           IDAMAX
c     ..
c     .. External Subroutines ..
      EXTERNAL           DGER, DSCAL, DSWAP, XERBLA
c     ..
c     .. Intrinsic Functions ..
      INTRINSIC          MAX, MIN
c     ..
c     .. Executable Statements ..
c
c     Test the input parameters.
c
      INFO = 0
      IF( M.LT.0 ) THEN
         INFO = -1
      ELSE IF( N.LT.0 ) THEN
         INFO = -2
      ELSE IF( LDA.LT.MAX( 1, M ) ) THEN
         INFO = -4
      END IF
      IF( INFO.NE.0 ) THEN
         CALL XERBLA( 'DGETF2', -INFO )
         RETURN
      END IF
c
c     Quick return if possible
c
      IF( M.EQ.0 .OR. N.EQ.0 )
     $   RETURN
c
      DO 10 J = 1, MIN( M, N )
c
c        Find pivot and test for singularity.
c
         JP = J - 1 + IDAMAX( M-J+1, A( J, J ), 1 )
         IPIV( J ) = JP
         IF( A( JP, J ).NE.ZERO ) THEN
c
c           Apply the interchange to columns 1:N.
c
            IF( JP.NE.J )
     $         CALL DSWAP( N, A( J, 1 ), LDA, A( JP, 1 ), LDA )
c
c           Compute elements J+1:M of J-th column.
c
            IF( J.LT.M )
     $         CALL DSCAL( M-J, ONE / A( J, J ), A( J+1, J ), 1 )
c
         ELSE IF( INFO.EQ.0 ) THEN
c
            INFO = J
         END IF
c
         IF( J.LT.MIN( M, N ) ) THEN
c
c           Update trailing submatrix.
c
            CALL DGER( M-J, N-J, -ONE, A( J+1, J ), 1, A( J, J+1 ), LDA,
     $                 A( J+1, J+1 ), LDA )
         END IF
   10 CONTINUE
      RETURN
c
c     End of DGETF2
c
      END
c***********************************************************************
      SUBROUTINE DLASWP( N, A, LDA, K1, K2, IPIV, INCX )
c
c  -- LAPACK auxiliary routine (version 2.0) --
c     Univ. of Tennessee, Univ. of California Berkeley, NAG Ltd.,
c     Courant Institute, Argonne National Lab, and Rice University
c     October 31, 1992
c
c     .. Scalar Arguments ..
      INTEGER            INCX, K1, K2, LDA, N
c     ..
c     .. Array Arguments ..
      INTEGER            IPIV( * )
      DOUBLE PRECISION   A( LDA, * )
c     ..
c
c  Purpose
c  =======
c
c  DLASWP performs a series of row interchanges on the matrix A.
c  One row interchange is initiated for each of rows K1 through K2 of A.
c
c  Arguments
c  =========
c
c  N       (input) INTEGER
c          The number of columns of the matrix A.
c
c  A       (input/output) DOUBLE PRECISION array, dimension (LDA,N)
c          On entry, the matrix of column dimension N to which the row
c          interchanges will be applied.
c          On exit, the permuted matrix.
c
c  LDA     (input) INTEGER
c          The leading dimension of the array A.
c
c  K1      (input) INTEGER
c          The first element of IPIV for which a row interchange will
c          be done.
c
c  K2      (input) INTEGER
c          The last element of IPIV for which a row interchange will
c          be done.
c
c  IPIV    (input) INTEGER array, dimension (M*abs(INCX))
c          The vector of pivot indices.  Only the elements in positions
c          K1 through K2 of IPIV are accessed.
c          IPIV(K) = L implies rows K and L are to be interchanged.
c
c  INCX    (input) INTEGER
c          The increment between successive values of IPIV.  If IPIV
c          is negative, the pivots are applied in reverse order.
c
c =====================================================================
c
c     .. Local Scalars ..
      INTEGER            I, IP, IX
c     ..
c     .. External Subroutines ..
      EXTERNAL           DSWAP
c     ..
c     .. Executable Statements ..
c
c     Interchange row I with row IPIV(I) for each of rows K1 through K2.
c
      IF( INCX.EQ.0 )
     $   RETURN
      IF( INCX.GT.0 ) THEN
         IX = K1
      ELSE
         IX = 1 + ( 1-K2 )*INCX
      END IF
      IF( INCX.EQ.1 ) THEN
         DO 10 I = K1, K2
            IP = IPIV( I )
            IF( IP.NE.I )
     $         CALL DSWAP( N, A( I, 1 ), LDA, A( IP, 1 ), LDA )
   10    CONTINUE
      ELSE IF( INCX.GT.1 ) THEN
         DO 20 I = K1, K2
            IP = IPIV( IX )
            IF( IP.NE.I )
     $         CALL DSWAP( N, A( I, 1 ), LDA, A( IP, 1 ), LDA )
            IX = IX + INCX
   20    CONTINUE
      ELSE IF( INCX.LT.0 ) THEN
         DO 30 I = K2, K1, -1
            IP = IPIV( IX )
            IF( IP.NE.I )
     $         CALL DSWAP( N, A( I, 1 ), LDA, A( IP, 1 ), LDA )
            IX = IX + INCX
   30    CONTINUE
      END IF
c
      RETURN
c
c     End of DLASWP
c
      END
c***********************************************************************
      INTEGER          FUNCTION ILAENV( ISPEC, NAME, OPTS, N1, N2, N3,
     $                 N4 )
c
c  -- LAPACK auxiliary routine (version 2.0) --
c     Univ. of Tennessee, Univ. of California Berkeley, NAG Ltd.,
c     Courant Institute, Argonne National Lab, and Rice University
c     September 30, 1994
c
c     .. Scalar Arguments ..
      CHARACTER*( * )    NAME, OPTS
      INTEGER            ISPEC, N1, N2, N3, N4
c     ..
c
c  Purpose
c  =======
c
c  ILAENV is called from the LAPACK routines to choose problem-dependent
c  parameters for the local environment.  See ISPEC for a description of
c  the parameters.
c
c  This version provides a set of parameters which should give good,
c  but not optimal, performance on many of the currently available
c  computers.  Users are encouraged to modify this subroutine to set
c  the tuning parameters for their particular machine using the option
c  and problem size information in the arguments.
c
c  This routine will not function correctly if it is converted to all
c  lower case.  Converting it to all upper case is allowed.
c
c  Arguments
c  =========
c
c  ISPEC   (input) INTEGER
c          Specifies the parameter to be returned as the value of
c          ILAENV.
c          = 1: the optimal blocksize; if this value is 1, an unblocked
c               algorithm will give the best performance.
c          = 2: the minimum block size for which the block routine
c               should be used; if the usable block size is less than
c               this value, an unblocked routine should be used.
c          = 3: the crossover point (in a block routine, for N less
c               than this value, an unblocked routine should be used)
c          = 4: the number of shifts, used in the nonsymmetric
c               eigenvalue routines
c          = 5: the minimum column dimension for blocking to be used;
c               rectangular blocks must have dimension at least k by m,
c               where k is given by ILAENV(2,...) and m by ILAENV(5,...)
c          = 6: the crossover point for the SVD (when reducing an m by n
c               matrix to bidiagonal form, if max(m,n)/min(m,n) exceeds
c               this value, a QR factorization is used first to reduce
c               the matrix to a triangular form.)
c          = 7: the number of processors
c          = 8: the crossover point for the multishift QR and QZ methods
c               for nonsymmetric eigenvalue problems.
c
c  NAME    (input) CHARACTER*(*)
c          The name of the calling subroutine, in either upper case or
c          lower case.
c
c  OPTS    (input) CHARACTER*(*)
c          The character options to the subroutine NAME, concatenated
c          into a single character string.  For example, UPLO = "U",
c          TRANS = "T", and DIAG = "N" for a triangular routine would
c          be specified as OPTS = "UTN".
c
c  N1      (input) INTEGER
c  N2      (input) INTEGER
c  N3      (input) INTEGER
c  N4      (input) INTEGER
c          Problem dimensions for the subroutine NAME; these may not all
c          be required.
c
c (ILAENV) (output) INTEGER
c          >= 0: the value of the parameter specified by ISPEC
c          < 0:  if ILAENV = -k, the k-th argument had an illegal value.
c
c  Further Details
c  ===============
c
c  The following conventions have been used when calling ILAENV from the
c  LAPACK routines:
c  1)  OPTS is a concatenation of all of the character options to
c      subroutine NAME, in the same order that they appear in the
c      argument list for NAME, even if they are not used in determining
c      the value of the parameter specified by ISPEC.
c  2)  The problem dimensions N1, N2, N3, N4 are specified in the order
c      that they appear in the argument list for NAME.  N1 is used
c      first, N2 second, and so on, and unused problem dimensions are
c      passed a value of -1.
c  3)  The parameter value returned by ILAENV is checked for validity in
c      the calling subroutine.  For example, ILAENV is used to retrieve
c      the optimal blocksize for STRTRI as follows:
c
c      NB = ILAENV( 1, "STRTRI", UPLO // DIAG, N, -1, -1, -1 )
c      IF( NB.LE.1 ) NB = MAX( 1, N )
c
c  =====================================================================
c
c     .. Local Scalars ..
      LOGICAL            CNAME, SNAME
      CHARACTER*1        C1
      CHARACTER*2        C2, C4
      CHARACTER*3        C3
      CHARACTER*6        SUBNAM
      INTEGER            I, IC, IZ, NB, NBMIN, NX
c     ..
c     .. Intrinsic Functions ..
      INTRINSIC          CHAR, ICHAR, INT, MIN, REAL
c     ..
c     .. Executable Statements ..
c
      GO TO ( 100, 100, 100, 400, 500, 600, 700, 800 ) ISPEC
c
c     Invalid value for ISPEC
c
      ILAENV = -1
      RETURN
c
  100 CONTINUE
c
c     Convert NAME to upper case if the first character is lower case.
c
      ILAENV = 1
      SUBNAM = NAME
      IC = ICHAR( SUBNAM( 1:1 ) )
      IZ = ICHAR( 'Z' )
      IF( IZ.EQ.90 .OR. IZ.EQ.122 ) THEN
c
c        ASCII character set
c
         IF( IC.GE.97 .AND. IC.LE.122 ) THEN
            SUBNAM( 1:1 ) = CHAR( IC-32 )
            DO 10 I = 2, 6
               IC = ICHAR( SUBNAM( I:I ) )
               IF( IC.GE.97 .AND. IC.LE.122 )
     $            SUBNAM( I:I ) = CHAR( IC-32 )
   10       CONTINUE
         END IF
c
      ELSE IF( IZ.EQ.233 .OR. IZ.EQ.169 ) THEN
c
c        EBCDIC character set
c
         IF( ( IC.GE.129 .AND. IC.LE.137 ) .OR.
     $       ( IC.GE.145 .AND. IC.LE.153 ) .OR.
     $       ( IC.GE.162 .AND. IC.LE.169 ) ) THEN
            SUBNAM( 1:1 ) = CHAR( IC+64 )
            DO 20 I = 2, 6
               IC = ICHAR( SUBNAM( I:I ) )
               IF( ( IC.GE.129 .AND. IC.LE.137 ) .OR.
     $             ( IC.GE.145 .AND. IC.LE.153 ) .OR.
     $             ( IC.GE.162 .AND. IC.LE.169 ) )
     $            SUBNAM( I:I ) = CHAR( IC+64 )
   20       CONTINUE
         END IF
c
      ELSE IF( IZ.EQ.218 .OR. IZ.EQ.250 ) THEN
c
c        Prime machines:  ASCII+128
c
         IF( IC.GE.225 .AND. IC.LE.250 ) THEN
            SUBNAM( 1:1 ) = CHAR( IC-32 )
            DO 30 I = 2, 6
               IC = ICHAR( SUBNAM( I:I ) )
               IF( IC.GE.225 .AND. IC.LE.250 )
     $            SUBNAM( I:I ) = CHAR( IC-32 )
   30       CONTINUE
         END IF
      END IF
c
      C1 = SUBNAM( 1:1 )
      SNAME = C1.EQ.'S' .OR. C1.EQ.'D'
      CNAME = C1.EQ.'C' .OR. C1.EQ.'Z'
      IF( .NOT.( CNAME .OR. SNAME ) )
     $   RETURN
      C2 = SUBNAM( 2:3 )
      C3 = SUBNAM( 4:6 )
      C4 = C3( 2:3 )
c
      GO TO ( 110, 200, 300 ) ISPEC
c
  110 CONTINUE
c
c     ISPEC = 1:  block size
c
c     In these examples, separate code is provided for setting NB for
c     real and complex.  We assume that NB will take the same value in
c     single or double precision.
c
      NB = 1
c
      IF( C2.EQ.'GE' ) THEN
         IF( C3.EQ.'TRF' ) THEN
            IF( SNAME ) THEN
               NB = 64
            ELSE
               NB = 64
            END IF
         ELSE IF( C3.EQ.'QRF' .OR. C3.EQ.'RQF' .OR. C3.EQ.'LQF' .OR.
     $            C3.EQ.'QLF' ) THEN
            IF( SNAME ) THEN
               NB = 32
            ELSE
               NB = 32
            END IF
         ELSE IF( C3.EQ.'HRD' ) THEN
            IF( SNAME ) THEN
               NB = 32
            ELSE
               NB = 32
            END IF
         ELSE IF( C3.EQ.'BRD' ) THEN
            IF( SNAME ) THEN
               NB = 32
            ELSE
               NB = 32
            END IF
         ELSE IF( C3.EQ.'TRI' ) THEN
            IF( SNAME ) THEN
               NB = 64
            ELSE
               NB = 64
            END IF
         END IF
      ELSE IF( C2.EQ.'PO' ) THEN
         IF( C3.EQ.'TRF' ) THEN
            IF( SNAME ) THEN
               NB = 64
            ELSE
               NB = 64
            END IF
         END IF
      ELSE IF( C2.EQ.'SY' ) THEN
         IF( C3.EQ.'TRF' ) THEN
            IF( SNAME ) THEN
               NB = 64
            ELSE
               NB = 64
            END IF
         ELSE IF( SNAME .AND. C3.EQ.'TRD' ) THEN
            NB = 1
         ELSE IF( SNAME .AND. C3.EQ.'GST' ) THEN
            NB = 64
         END IF
      ELSE IF( CNAME .AND. C2.EQ.'HE' ) THEN
         IF( C3.EQ.'TRF' ) THEN
            NB = 64
         ELSE IF( C3.EQ.'TRD' ) THEN
            NB = 1
         ELSE IF( C3.EQ.'GST' ) THEN
            NB = 64
         END IF
      ELSE IF( SNAME .AND. C2.EQ.'OR' ) THEN
         IF( C3( 1:1 ).EQ.'G' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR.
     $          C4.EQ.'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR.
     $          C4.EQ.'BR' ) THEN
               NB = 32
            END IF
         ELSE IF( C3( 1:1 ).EQ.'M' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR.
     $          C4.EQ.'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR.
     $          C4.EQ.'BR' ) THEN
               NB = 32
            END IF
         END IF
      ELSE IF( CNAME .AND. C2.EQ.'UN' ) THEN
         IF( C3( 1:1 ).EQ.'G' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR.
     $          C4.EQ.'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR.
     $          C4.EQ.'BR' ) THEN
               NB = 32
            END IF
         ELSE IF( C3( 1:1 ).EQ.'M' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR.
     $          C4.EQ.'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR.
     $          C4.EQ.'BR' ) THEN
               NB = 32
            END IF
         END IF
      ELSE IF( C2.EQ.'GB' ) THEN
         IF( C3.EQ.'TRF' ) THEN
            IF( SNAME ) THEN
               IF( N4.LE.64 ) THEN
                  NB = 1
               ELSE
                  NB = 32
               END IF
            ELSE
               IF( N4.LE.64 ) THEN
                  NB = 1
               ELSE
                  NB = 32
               END IF
            END IF
         END IF
      ELSE IF( C2.EQ.'PB' ) THEN
         IF( C3.EQ.'TRF' ) THEN
            IF( SNAME ) THEN
               IF( N2.LE.64 ) THEN
                  NB = 1
               ELSE
                  NB = 32
               END IF
            ELSE
               IF( N2.LE.64 ) THEN
                  NB = 1
               ELSE
                  NB = 32
               END IF
            END IF
         END IF
      ELSE IF( C2.EQ.'TR' ) THEN
         IF( C3.EQ.'TRI' ) THEN
            IF( SNAME ) THEN
               NB = 64
            ELSE
               NB = 64
            END IF
         END IF
      ELSE IF( C2.EQ.'LA' ) THEN
         IF( C3.EQ.'UUM' ) THEN
            IF( SNAME ) THEN
               NB = 64
            ELSE
               NB = 64
            END IF
         END IF
      ELSE IF( SNAME .AND. C2.EQ.'ST' ) THEN
         IF( C3.EQ.'EBZ' ) THEN
            NB = 1
         END IF
      END IF
      ILAENV = NB
      RETURN
c
  200 CONTINUE
c
c     ISPEC = 2:  minimum block size
c
      NBMIN = 2
      IF( C2.EQ.'GE' ) THEN
         IF( C3.EQ.'QRF' .OR. C3.EQ.'RQF' .OR. C3.EQ.'LQF' .OR.
     $       C3.EQ.'QLF' ) THEN
            IF( SNAME ) THEN
               NBMIN = 2
            ELSE
               NBMIN = 2
            END IF
         ELSE IF( C3.EQ.'HRD' ) THEN
            IF( SNAME ) THEN
               NBMIN = 2
            ELSE
               NBMIN = 2
            END IF
         ELSE IF( C3.EQ.'BRD' ) THEN
            IF( SNAME ) THEN
               NBMIN = 2
            ELSE
               NBMIN = 2
            END IF
         ELSE IF( C3.EQ.'TRI' ) THEN
            IF( SNAME ) THEN
               NBMIN = 2
            ELSE
               NBMIN = 2
            END IF
         END IF
      ELSE IF( C2.EQ.'SY' ) THEN
         IF( C3.EQ.'TRF' ) THEN
            IF( SNAME ) THEN
               NBMIN = 8
            ELSE
               NBMIN = 8
            END IF
         ELSE IF( SNAME .AND. C3.EQ.'TRD' ) THEN
            NBMIN = 2
         END IF
      ELSE IF( CNAME .AND. C2.EQ.'HE' ) THEN
         IF( C3.EQ.'TRD' ) THEN
            NBMIN = 2
         END IF
      ELSE IF( SNAME .AND. C2.EQ.'OR' ) THEN
         IF( C3( 1:1 ).EQ.'G' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR.
     $          C4.EQ.'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR.
     $          C4.EQ.'BR' ) THEN
               NBMIN = 2
            END IF
         ELSE IF( C3( 1:1 ).EQ.'M' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR.
     $          C4.EQ.'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR.
     $          C4.EQ.'BR' ) THEN
               NBMIN = 2
            END IF
         END IF
      ELSE IF( CNAME .AND. C2.EQ.'UN' ) THEN
         IF( C3( 1:1 ).EQ.'G' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR.
     $          C4.EQ.'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR.
     $          C4.EQ.'BR' ) THEN
               NBMIN = 2
            END IF
         ELSE IF( C3( 1:1 ).EQ.'M' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR.
     $          C4.EQ.'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR.
     $          C4.EQ.'BR' ) THEN
               NBMIN = 2
            END IF
         END IF
      END IF
      ILAENV = NBMIN
      RETURN
c
  300 CONTINUE
c
c     ISPEC = 3:  crossover point
c
      NX = 0
      IF( C2.EQ.'GE' ) THEN
         IF( C3.EQ.'QRF' .OR. C3.EQ.'RQF' .OR. C3.EQ.'LQF' .OR.
     $       C3.EQ.'QLF' ) THEN
            IF( SNAME ) THEN
               NX = 128
            ELSE
               NX = 128
            END IF
         ELSE IF( C3.EQ.'HRD' ) THEN
            IF( SNAME ) THEN
               NX = 128
            ELSE
               NX = 128
            END IF
         ELSE IF( C3.EQ.'BRD' ) THEN
            IF( SNAME ) THEN
               NX = 128
            ELSE
               NX = 128
            END IF
         END IF
      ELSE IF( C2.EQ.'SY' ) THEN
         IF( SNAME .AND. C3.EQ.'TRD' ) THEN
            NX = 1
         END IF
      ELSE IF( CNAME .AND. C2.EQ.'HE' ) THEN
         IF( C3.EQ.'TRD' ) THEN
            NX = 1
         END IF
      ELSE IF( SNAME .AND. C2.EQ.'OR' ) THEN
         IF( C3( 1:1 ).EQ.'G' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR.
     $          C4.EQ.'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR.
     $          C4.EQ.'BR' ) THEN
               NX = 128
            END IF
         END IF
      ELSE IF( CNAME .AND. C2.EQ.'UN' ) THEN
         IF( C3( 1:1 ).EQ.'G' ) THEN
            IF( C4.EQ.'QR' .OR. C4.EQ.'RQ' .OR. C4.EQ.'LQ' .OR.
     $          C4.EQ.'QL' .OR. C4.EQ.'HR' .OR. C4.EQ.'TR' .OR.
     $          C4.EQ.'BR' ) THEN
               NX = 128
            END IF
         END IF
      END IF
      ILAENV = NX
      RETURN
c
  400 CONTINUE
c
c     ISPEC = 4:  number of shifts (used by xHSEQR)
c
      ILAENV = 6
      RETURN
c
  500 CONTINUE
c
c     ISPEC = 5:  minimum column dimension (not used)
c
      ILAENV = 2
      RETURN
c
  600 CONTINUE 
c
c     ISPEC = 6:  crossover point for SVD (used by xGELSS and xGESVD)
c
      ILAENV = INT( REAL( MIN( N1, N2 ) )*1.6E0 )
      RETURN
c
  700 CONTINUE
c
c     ISPEC = 7:  number of processors (not used)
c
      ILAENV = 1
      RETURN
c
  800 CONTINUE
c
c     ISPEC = 8:  crossover point for multishift (used by xHSEQR)
c
      ILAENV = 50
      RETURN
c
c     End of ILAENV
c
      END
c***********************************************************************
      LOGICAL          FUNCTION LSAME( CA, CB )
c
c  -- LAPACK auxiliary routine (version 2.0) --
c     Univ. of Tennessee, Univ. of California Berkeley, NAG Ltd.,
c     Courant Institute, Argonne National Lab, and Rice University
c     September 30, 1994
c
c     .. Scalar Arguments ..
      CHARACTER          CA, CB
c     ..
c
c  Purpose
c  =======
c
c  LSAME returns .TRUE. if CA is the same letter as CB regardless of
c  case.
c
c  Arguments
c  =========
c
c  CA      (input) CHARACTER*1
c  CB      (input) CHARACTER*1
c          CA and CB specify the single characters to be compared.
c
c =====================================================================
c
c     .. Intrinsic Functions ..
      INTRINSIC          ICHAR
c     ..
c     .. Local Scalars ..
      INTEGER            INTA, INTB, ZCODE
c     ..
c     .. Executable Statements ..
c
c     Test if the characters are equal
c
      LSAME = CA.EQ.CB
      IF( LSAME )
     $   RETURN
c
c     Now test for equivalence if both characters are alphabetic.
c
      ZCODE = ICHAR( 'Z' )
c
c     Use "Z" rather than "A" so that ASCII can be detected on Prime
c     machines, on which ICHAR returns a value with bit 8 set.
c
      INTA = ICHAR( CA )
      INTB = ICHAR( CB )
c
      IF( ZCODE.EQ.90 .OR. ZCODE.EQ.122 ) THEN
c
c        ASCII is assumed - ZCODE is the ASCII code of either lower or
c        upper case "Z".
c
         IF( INTA.GE.97 .AND. INTA.LE.122 ) INTA = INTA - 32
         IF( INTB.GE.97 .AND. INTB.LE.122 ) INTB = INTB - 32
c
      ELSE IF( ZCODE.EQ.233 .OR. ZCODE.EQ.169 ) THEN
c
c        EBCDIC is assumed - ZCODE is the EBCDIC code of either lower or
c        upper case "Z".
c
         IF( INTA.GE.129 .AND. INTA.LE.137 .OR.
     $       INTA.GE.145 .AND. INTA.LE.153 .OR.
     $       INTA.GE.162 .AND. INTA.LE.169 ) INTA = INTA + 64
         IF( INTB.GE.129 .AND. INTB.LE.137 .OR.
     $       INTB.GE.145 .AND. INTB.LE.153 .OR.
     $       INTB.GE.162 .AND. INTB.LE.169 ) INTB = INTB + 64
c
      ELSE IF( ZCODE.EQ.218 .OR. ZCODE.EQ.250 ) THEN
c
c        ASCII is assumed, on Prime machines - ZCODE is the ASCII code
c        plus 128 of either lower or upper case "Z".
c
         IF( INTA.GE.225 .AND. INTA.LE.250 ) INTA = INTA - 32
         IF( INTB.GE.225 .AND. INTB.LE.250 ) INTB = INTB - 32
      END IF
      LSAME = INTA.EQ.INTB
c
c     RETURN
c
c     End of LSAME
c
      END
c***********************************************************************
      SUBROUTINE XERBLA( SRNAME, INFO )
c
c  -- LAPACK auxiliary routine (version 2.0) --
c     Univ. of Tennessee, Univ. of California Berkeley, NAG Ltd.,
c     Courant Institute, Argonne National Lab, and Rice University
c     September 30, 1994
c
c     .. Scalar Arguments ..
      CHARACTER*6        SRNAME
      INTEGER            INFO
c     ..
c
c  Purpose
c  =======
c
c  XERBLA  is an error handler for the LAPACK routines.
c  It is called by an LAPACK routine if an input parameter has an
c  invalid value.  A message is printed and execution stops.
c
c  Installers may consider modifying the STOP statement in order to
c  call system-specific exception-handling facilities. 
c
c  Arguments
c  =========
c
c  SRNAME  (input) CHARACTER*6
c          The name of the routine which called XERBLA.
c
c  INFO    (input) INTEGER
c          The position of the invalid parameter in the parameter list
c          of the calling routine.
c
c =====================================================================
c
c     .. Executable Statements ..
c
      WRITE( *, FMT = 9999 )SRNAME, INFO
c
      stop
c
 9999 FORMAT( ' ** On entry to ', A6, ' parameter number ', I2, ' had ',
     $      'an illegal value' )
c
c     End of XERBLA
c
      END
c***********************************************************************
      SUBROUTINE DGEMM ( TRANSA, TRANSB, M, N, K, ALPHA, A, LDA, B, LDB,
     $                   BETA, C, LDC )
c     .. Scalar Arguments ..
      CHARACTER*1        TRANSA, TRANSB
      INTEGER            M, N, K, LDA, LDB, LDC
      DOUBLE PRECISION   ALPHA, BETA
c     .. Array Arguments ..
      DOUBLE PRECISION   A( LDA, * ), B( LDB, * ), C( LDC, * )
c     ..
c
c  Purpose
c  =======
c
c  DGEMM  performs one of the matrix-matrix operations
c
c     C := alpha*op( A )*op( B ) + beta*C,
c
c  where  op( X ) is one of
c
c     op( X ) = X   or   op( X ) = X_prime,
c
c  alpha and beta are scalars, and A, B and C are matrices, with op( A )
c  an m by k matrix,  op( B )  a  k by n matrix and  C an m by n matrix.
c
c  Parameters
c  ==========
c
c  TRANSA - CHARACTER*1.
c           On entry, TRANSA specifies the form of op( A ) to be used in
c           the matrix multiplication as follows:
c
c              TRANSA = "N" or "n",  op( A ) = A.
c
c              TRANSA = "T" or "t",  op( A ) = A_prime.
c
c              TRANSA = "C" or "c",  op( A ) = A_prime.
c
c           Unchanged on exit.
c
c  TRANSB - CHARACTER*1.
c           On entry, TRANSB specifies the form of op( B ) to be used in
c           the matrix multiplication as follows:
c
c              TRANSB = "N" or "n",  op( B ) = B.
c
c              TRANSB = "T" or "t",  op( B ) = B_prime.
c
c              TRANSB = "C" or "c",  op( B ) = B_prime.
c
c           Unchanged on exit.
c
c  M      - INTEGER.
c           On entry,  M  specifies  the number  of rows  of the  matrix
c           op( A )  and of the  matrix  C.  M  must  be at least  zero.
c           Unchanged on exit.
c
c  N      - INTEGER.
c           On entry,  N  specifies the number  of columns of the matrix
c           op( B ) and the number of columns of the matrix C. N must be
c           at least zero.
c           Unchanged on exit.
c
c  K      - INTEGER.
c           On entry,  K  specifies  the number of columns of the matrix
c           op( A ) and the number of rows of the matrix op( B ). K must
c           be at least  zero.
c           Unchanged on exit.
c
c  ALPHA  - DOUBLE PRECISION.
c           On entry, ALPHA specifies the scalar alpha.
c           Unchanged on exit.
c
c  A      - DOUBLE PRECISION array of DIMENSION ( LDA, ka ), where ka is
c           k  when  TRANSA = "N" or "n",  and is  m  otherwise.
c           Before entry with  TRANSA = "N" or "n",  the leading  m by k
c           part of the array  A  must contain the matrix  A,  otherwise
c           the leading  k by m  part of the array  A  must contain  the
c           matrix A.
c           Unchanged on exit.
c
c  LDA    - INTEGER.
c           On entry, LDA specifies the first dimension of A as declared
c           in the calling (sub) program. When  TRANSA = "N" or "n" then
c           LDA must be at least  max( 1, m ), otherwise  LDA must be at
c           least  max( 1, k ).
c           Unchanged on exit.
c
c  B      - DOUBLE PRECISION array of DIMENSION ( LDB, kb ), where kb is
c           n  when  TRANSB = "N" or "n",  and is  k  otherwise.
c           Before entry with  TRANSB = "N" or "n",  the leading  k by n
c           part of the array  B  must contain the matrix  B,  otherwise
c           the leading  n by k  part of the array  B  must contain  the
c           matrix B.
c           Unchanged on exit.
c
c  LDB    - INTEGER.
c           On entry, LDB specifies the first dimension of B as declared
c           in the calling (sub) program. When  TRANSB = "N" or "n" then
c           LDB must be at least  max( 1, k ), otherwise  LDB must be at
c           least  max( 1, n ).
c           Unchanged on exit.
c
c  BETA   - DOUBLE PRECISION.
c           On entry,  BETA  specifies the scalar  beta.  When  BETA  is
c           supplied as zero then C need not be set on input.
c           Unchanged on exit.
c
c  C      - DOUBLE PRECISION array of DIMENSION ( LDC, n ).
c           Before entry, the leading  m by n  part of the array  C must
c           contain the matrix  C,  except when  beta  is zero, in which
c           case C need not be set on entry.
c           On exit, the array  C  is overwritten by the  m by n  matrix
c           ( alpha*op( A )*op( B ) + beta*C ).
c
c  LDC    - INTEGER.
c           On entry, LDC specifies the first dimension of C as declared
c           in  the  calling  (sub)  program.   LDC  must  be  at  least
c           max( 1, m ).
c           Unchanged on exit.
c
c
c  Level 3 Blas routine.
c
c  -- Written on 8-February-1989.
c     Jack Dongarra, Argonne National Laboratory.
c     Iain Duff, AERE Harwell.
c     Jeremy Du Croz, Numerical Algorithms Group Ltd.
c     Sven Hammarling, Numerical Algorithms Group Ltd.
c
c
c     .. External Functions ..
      LOGICAL            LSAME
      EXTERNAL           LSAME
c     .. External Subroutines ..
      EXTERNAL           XERBLA
c     .. Intrinsic Functions ..
      INTRINSIC          MAX
c     .. Local Scalars ..
      LOGICAL            NOTA, NOTB
      INTEGER            I, INFO, J, L, NCOLA, NROWA, NROWB
      DOUBLE PRECISION   TEMP
c     .. Parameters ..
      DOUBLE PRECISION   ONE         , ZERO
      PARAMETER        ( ONE = 1.0D+0, ZERO = 0.0D+0 )
c     ..
c     .. Executable Statements ..
c
c     Set  NOTA  and  NOTB  as  true if  A  and  B  respectively are not
c     transposed and set  NROWA, NCOLA and  NROWB  as the number of rows
c     and  columns of  A  and the  number of  rows  of  B  respectively.
c
      NOTA  = LSAME( TRANSA, 'N' )
      NOTB  = LSAME( TRANSB, 'N' )
      IF( NOTA )THEN
         NROWA = M
         NCOLA = K
      ELSE
         NROWA = K
         NCOLA = M
      END IF
      IF( NOTB )THEN
         NROWB = K
      ELSE
         NROWB = N
      END IF
c
c     Test the input parameters.
c
      INFO = 0
      IF(      ( .NOT.NOTA                 ).AND.
     $         ( .NOT.LSAME( TRANSA, 'C' ) ).AND.
     $         ( .NOT.LSAME( TRANSA, 'T' ) )      )THEN
         INFO = 1
      ELSE IF( ( .NOT.NOTB                 ).AND.
     $         ( .NOT.LSAME( TRANSB, 'C' ) ).AND.
     $         ( .NOT.LSAME( TRANSB, 'T' ) )      )THEN
         INFO = 2
      ELSE IF( M  .LT.0               )THEN
         INFO = 3
      ELSE IF( N  .LT.0               )THEN
         INFO = 4
      ELSE IF( K  .LT.0               )THEN
         INFO = 5
      ELSE IF( LDA.LT.MAX( 1, NROWA ) )THEN
         INFO = 8
      ELSE IF( LDB.LT.MAX( 1, NROWB ) )THEN
         INFO = 10
      ELSE IF( LDC.LT.MAX( 1, M     ) )THEN
         INFO = 13
      END IF
      IF( INFO.NE.0 )THEN
         CALL XERBLA( 'DGEMM ', INFO )
         RETURN
      END IF
c
c     Quick return if possible.
c
      IF( ( M.EQ.0 ).OR.( N.EQ.0 ).OR.
     $    ( ( ( ALPHA.EQ.ZERO ).OR.( K.EQ.0 ) ).AND.( BETA.EQ.ONE ) ) )
     $   RETURN
c
c     And if  alpha.eq.zero.
c
      IF( ALPHA.EQ.ZERO )THEN
         IF( BETA.EQ.ZERO )THEN
            DO 20, J = 1, N
               DO 10, I = 1, M
                  C( I, J ) = ZERO
   10          CONTINUE
   20       CONTINUE
         ELSE
            DO 40, J = 1, N
               DO 30, I = 1, M
                  C( I, J ) = BETA*C( I, J )
   30          CONTINUE
   40       CONTINUE
         END IF
         RETURN
      END IF
c
c     Start the operations.
c
      IF( NOTB )THEN
         IF( NOTA )THEN
c
c           Form  C := alpha*A*B + beta*C.
c
            DO 90, J = 1, N
               IF( BETA.EQ.ZERO )THEN
                  DO 50, I = 1, M
                     C( I, J ) = ZERO
   50             CONTINUE
               ELSE IF( BETA.NE.ONE )THEN
                  DO 60, I = 1, M
                     C( I, J ) = BETA*C( I, J )
   60             CONTINUE
               END IF
               DO 80, L = 1, K
                  IF( B( L, J ).NE.ZERO )THEN
                     TEMP = ALPHA*B( L, J )
                     DO 70, I = 1, M
                        C( I, J ) = C( I, J ) + TEMP*A( I, L )
   70                CONTINUE
                  END IF
   80          CONTINUE
   90       CONTINUE
         ELSE
c
c           Form  C := alpha*A_prime*B + beta*C
c
            DO 120, J = 1, N
               DO 110, I = 1, M
                  TEMP = ZERO
                  DO 100, L = 1, K
                     TEMP = TEMP + A( L, I )*B( L, J )
  100             CONTINUE
                  IF( BETA.EQ.ZERO )THEN
                     C( I, J ) = ALPHA*TEMP
                  ELSE
                     C( I, J ) = ALPHA*TEMP + BETA*C( I, J )
                  END IF
  110          CONTINUE
  120       CONTINUE
         END IF
      ELSE
         IF( NOTA )THEN
c
c           Form  C := alpha*A*B_prime + beta*C
c
            DO 170, J = 1, N
               IF( BETA.EQ.ZERO )THEN
                  DO 130, I = 1, M
                     C( I, J ) = ZERO
  130             CONTINUE
               ELSE IF( BETA.NE.ONE )THEN
                  DO 140, I = 1, M
                     C( I, J ) = BETA*C( I, J )
  140             CONTINUE
               END IF
               DO 160, L = 1, K
                  IF( B( J, L ).NE.ZERO )THEN
                     TEMP = ALPHA*B( J, L )
                     DO 150, I = 1, M
                        C( I, J ) = C( I, J ) + TEMP*A( I, L )
  150                CONTINUE
                  END IF
  160          CONTINUE
  170       CONTINUE
         ELSE
c
c           Form  C := alpha*A_prime*B_prime + beta*C
c
            DO 200, J = 1, N
               DO 190, I = 1, M
                  TEMP = ZERO
                  DO 180, L = 1, K
                     TEMP = TEMP + A( L, I )*B( J, L )
  180             CONTINUE
                  IF( BETA.EQ.ZERO )THEN
                     C( I, J ) = ALPHA*TEMP
                  ELSE
                     C( I, J ) = ALPHA*TEMP + BETA*C( I, J )
                  END IF
  190          CONTINUE
  200       CONTINUE
         END IF
      END IF
c
      RETURN
c
c     End of DGEMM .
c
      END
c***********************************************************************
      SUBROUTINE DGER  ( M, N, ALPHA, X, INCX, Y, INCY, A, LDA )
c     .. Scalar Arguments ..
      DOUBLE PRECISION   ALPHA
      INTEGER            INCX, INCY, LDA, M, N
c     .. Array Arguments ..
      DOUBLE PRECISION   A( LDA, * ), X( * ), Y( * )
c     ..
c
c  Purpose
c  =======
c
c  DGER   performs the rank 1 operation
c
c     A := alpha*x*y_prime + A,
c
c  where alpha is a scalar, x is an m element vector, y is an n element
c  vector and A is an m by n matrix.
c
c  Parameters
c  ==========
c
c  M      - INTEGER.
c           On entry, M specifies the number of rows of the matrix A.
c           M must be at least zero.
c           Unchanged on exit.
c
c  N      - INTEGER.
c           On entry, N specifies the number of columns of the matrix A.
c           N must be at least zero.
c           Unchanged on exit.
c
c  ALPHA  - DOUBLE PRECISION.
c           On entry, ALPHA specifies the scalar alpha.
c           Unchanged on exit.
c
c  X      - DOUBLE PRECISION array of dimension at least
c           ( 1 + ( m - 1 )*abs( INCX ) ).
c           Before entry, the incremented array X must contain the m
c           element vector x.
c           Unchanged on exit.
c
c  INCX   - INTEGER.
c           On entry, INCX specifies the increment for the elements of
c           X. INCX must not be zero.
c           Unchanged on exit.
c
c  Y      - DOUBLE PRECISION array of dimension at least
c           ( 1 + ( n - 1 )*abs( INCY ) ).
c           Before entry, the incremented array Y must contain the n
c           element vector y.
c           Unchanged on exit.
c
c  INCY   - INTEGER.
c           On entry, INCY specifies the increment for the elements of
c           Y. INCY must not be zero.
c           Unchanged on exit.
c
c  A      - DOUBLE PRECISION array of DIMENSION ( LDA, n ).
c           Before entry, the leading m by n part of the array A must
c           contain the matrix of coefficients. On exit, A is
c           overwritten by the updated matrix.
c
c  LDA    - INTEGER.
c           On entry, LDA specifies the first dimension of A as declared
c           in the calling (sub) program. LDA must be at least
c           max( 1, m ).
c           Unchanged on exit.
c
c
c  Level 2 Blas routine.
c
c  -- Written on 22-October-1986.
c     Jack Dongarra, Argonne National Lab.
c     Jeremy Du Croz, Nag Central Office.
c     Sven Hammarling, Nag Central Office.
c     Richard Hanson, Sandia National Labs.
c
c
c     .. Parameters ..
      DOUBLE PRECISION   ZERO
      PARAMETER        ( ZERO = 0.0D+0 )
c     .. Local Scalars ..
      DOUBLE PRECISION   TEMP
      INTEGER            I, INFO, IX, J, JY, KX
c     .. External Subroutines ..
      EXTERNAL           XERBLA
c     .. Intrinsic Functions ..
      INTRINSIC          MAX
c     ..
c     .. Executable Statements ..
c
c     Test the input parameters.
c
      INFO = 0
      IF     ( M.LT.0 )THEN
         INFO = 1
      ELSE IF( N.LT.0 )THEN
         INFO = 2
      ELSE IF( INCX.EQ.0 )THEN
         INFO = 5
      ELSE IF( INCY.EQ.0 )THEN
         INFO = 7
      ELSE IF( LDA.LT.MAX( 1, M ) )THEN
         INFO = 9
      END IF
      IF( INFO.NE.0 )THEN
         CALL XERBLA( 'DGER  ', INFO )
         RETURN
      END IF
c
c     Quick return if possible.
c
      IF( ( M.EQ.0 ).OR.( N.EQ.0 ).OR.( ALPHA.EQ.ZERO ) )
     $   RETURN
c
c     Start the operations. In this version the elements of A are
c     accessed sequentially with one pass through A.
c
      IF( INCY.GT.0 )THEN
         JY = 1
      ELSE
         JY = 1 - ( N - 1 )*INCY
      END IF
      IF( INCX.EQ.1 )THEN
         DO 20, J = 1, N
            IF( Y( JY ).NE.ZERO )THEN
               TEMP = ALPHA*Y( JY )
               DO 10, I = 1, M
                  A( I, J ) = A( I, J ) + X( I )*TEMP
   10          CONTINUE
            END IF
            JY = JY + INCY
   20    CONTINUE
      ELSE
         IF( INCX.GT.0 )THEN
            KX = 1
         ELSE
            KX = 1 - ( M - 1 )*INCX
         END IF
         DO 40, J = 1, N
            IF( Y( JY ).NE.ZERO )THEN
               TEMP = ALPHA*Y( JY )
               IX   = KX
               DO 30, I = 1, M
                  A( I, J ) = A( I, J ) + X( IX )*TEMP
                  IX        = IX        + INCX
   30          CONTINUE
            END IF
            JY = JY + INCY
   40    CONTINUE
      END IF
c
      RETURN
c
c     End of DGER  .
c
      END
c***********************************************************************
      subroutine  dscal(n,da,dx,incx)
c
c     scales a vector by a constant.
c     uses unrolled loops for increment equal to one.
c     jack dongarra, linpack, 3/11/78.
c     modified 3/93 to return if incx .le. 0.
c     modified 12/3/93, array(1) declarations changed to array(*)
c
      double precision da,dx(*)
      integer i,incx,m,mp1,n,nincx
c
      if( n.le.0 .or. incx.le.0 )return
      if(incx.eq.1)go to 20
c
c        code for increment not equal to 1
c
      nincx = n*incx
      do 10 i = 1,nincx,incx
        dx(i) = da*dx(i)
   10 continue
      return
c
c        code for increment equal to 1
c
c
c        clean-up loop
c
   20 m = mod(n,5)
      if( m .eq. 0 ) go to 40
      do 30 i = 1,m
        dx(i) = da*dx(i)
   30 continue
      if( n .lt. 5 ) return
   40 mp1 = m + 1
      do 50 i = mp1,n,5
        dx(i) = da*dx(i)
        dx(i + 1) = da*dx(i + 1)
        dx(i + 2) = da*dx(i + 2)
        dx(i + 3) = da*dx(i + 3)
        dx(i + 4) = da*dx(i + 4)
   50 continue
      return
      end
      subroutine  dswap (n,dx,incx,dy,incy)
c
c     interchanges two vectors.
c     uses unrolled loops for increments equal one.
c     jack dongarra, linpack, 3/11/78.
c     modified 12/3/93, array(1) declarations changed to array(*)
c
      double precision dx(*),dy(*),dtemp
      integer i,incx,incy,ix,iy,m,mp1,n
c
      if(n.le.0)return
      if(incx.eq.1.and.incy.eq.1)go to 20
c
c       code for unequal increments or equal increments not equal
c         to 1
c
      ix = 1
      iy = 1
      if(incx.lt.0)ix = (-n+1)*incx + 1
      if(incy.lt.0)iy = (-n+1)*incy + 1
      do 10 i = 1,n
        dtemp = dx(ix)
        dx(ix) = dy(iy)
        dy(iy) = dtemp
        ix = ix + incx
        iy = iy + incy
   10 continue
      return
c
c       code for both increments equal to 1
c
c
c       clean-up loop
c
   20 m = mod(n,3)
      if( m .eq. 0 ) go to 40
      do 30 i = 1,m
        dtemp = dx(i)
        dx(i) = dy(i)
        dy(i) = dtemp
   30 continue
      if( n .lt. 3 ) return
   40 mp1 = m + 1
      do 50 i = mp1,n,3
        dtemp = dx(i)
        dx(i) = dy(i)
        dy(i) = dtemp
        dtemp = dx(i + 1)
        dx(i + 1) = dy(i + 1)
        dy(i + 1) = dtemp
        dtemp = dx(i + 2)
        dx(i + 2) = dy(i + 2)
        dy(i + 2) = dtemp
   50 continue
      return
      end
      SUBROUTINE DTRSM ( SIDE, UPLO, TRANSA, DIAG, M, N, ALPHA, A, LDA,
     $                   B, LDB )
c     .. Scalar Arguments ..
      CHARACTER*1        SIDE, UPLO, TRANSA, DIAG
      INTEGER            M, N, LDA, LDB
      DOUBLE PRECISION   ALPHA
c     .. Array Arguments ..
      DOUBLE PRECISION   A( LDA, * ), B( LDB, * )
c     ..
c
c  Purpose
c  =======
c
c  DTRSM  solves one of the matrix equations
c
c     op( A )*X = alpha*B,   or   X*op( A ) = alpha*B,
c
c  where alpha is a scalar, X and B are m by n matrices, A is a unit, or
c  non-unit,  upper or lower triangular matrix  and  op( A )  is one  of
c
c     op( A ) = A   or   op( A ) = A_prime.
c
c  The matrix X is overwritten on B.
c
c  Parameters
c  ==========
c
c  SIDE   - CHARACTER*1.
c           On entry, SIDE specifies whether op( A ) appears on the left
c           or right of X as follows:
c
c              SIDE = "L" or "l"   op( A )*X = alpha*B.
c
c              SIDE = "R" or "r"   X*op( A ) = alpha*B.
c
c           Unchanged on exit.
c
c  UPLO   - CHARACTER*1.
c           On entry, UPLO specifies whether the matrix A is an upper or
c           lower triangular matrix as follows:
c
c              UPLO = "U" or "u"   A is an upper triangular matrix.
c
c              UPLO = "L" or "l"   A is a lower triangular matrix.
c
c           Unchanged on exit.
c
c  TRANSA - CHARACTER*1.
c           On entry, TRANSA specifies the form of op( A ) to be used in
c           the matrix multiplication as follows:
c
c              TRANSA = "N" or "n"   op( A ) = A.
c
c              TRANSA = "T" or "t"   op( A ) = A_prime.
c
c              TRANSA = "C" or "c"   op( A ) = A_prime.
c
c           Unchanged on exit.
c
c  DIAG   - CHARACTER*1.
c           On entry, DIAG specifies whether or not A is unit triangular
c           as follows:
c
c              DIAG = "U" or "u"   A is assumed to be unit triangular.
c
c              DIAG = "N" or "n"   A is not assumed to be unit
c                                  triangular.
c
c           Unchanged on exit.
c
c  M      - INTEGER.
c           On entry, M specifies the number of rows of B. M must be at
c           least zero.
c           Unchanged on exit.
c
c  N      - INTEGER.
c           On entry, N specifies the number of columns of B.  N must be
c           at least zero.
c           Unchanged on exit.
c
c  ALPHA  - DOUBLE PRECISION.
c           On entry,  ALPHA specifies the scalar  alpha. When  alpha is
c           zero then  A is not referenced and  B need not be set before
c           entry.
c           Unchanged on exit.
c
c  A      - DOUBLE PRECISION array of DIMENSION ( LDA, k ), where k is m
c           when  SIDE = "L" or "l"  and is  n  when  SIDE = "R" or "r".
c           Before entry  with  UPLO = "U" or "u",  the  leading  k by k
c           upper triangular part of the array  A must contain the upper
c           triangular matrix  and the strictly lower triangular part of
c           A is not referenced.
c           Before entry  with  UPLO = "L" or "l",  the  leading  k by k
c           lower triangular part of the array  A must contain the lower
c           triangular matrix  and the strictly upper triangular part of
c           A is not referenced.
c           Note that when  DIAG = "U" or "u",  the diagonal elements of
c           A  are not referenced either,  but are assumed to be  unity.
c           Unchanged on exit.
c
c  LDA    - INTEGER.
c           On entry, LDA specifies the first dimension of A as declared
c           in the calling (sub) program.  When  SIDE = "L" or "l"  then
c           LDA  must be at least  max( 1, m ),  when  SIDE = "R" or "r"
c           then LDA must be at least max( 1, n ).
c           Unchanged on exit.
c
c  B      - DOUBLE PRECISION array of DIMENSION ( LDB, n ).
c           Before entry,  the leading  m by n part of the array  B must
c           contain  the  right-hand  side  matrix  B,  and  on exit  is
c           overwritten by the solution matrix  X.
c
c  LDB    - INTEGER.
c           On entry, LDB specifies the first dimension of B as declared
c           in  the  calling  (sub)  program.   LDB  must  be  at  least
c           max( 1, m ).
c           Unchanged on exit.
c
c
c  Level 3 Blas routine.
c
c
c  -- Written on 8-February-1989.
c     Jack Dongarra, Argonne National Laboratory.
c     Iain Duff, AERE Harwell.
c     Jeremy Du Croz, Numerical Algorithms Group Ltd.
c     Sven Hammarling, Numerical Algorithms Group Ltd.
c
c
c     .. External Functions ..
      LOGICAL            LSAME
      EXTERNAL           LSAME
c     .. External Subroutines ..
      EXTERNAL           XERBLA
c     .. Intrinsic Functions ..
      INTRINSIC          MAX
c     .. Local Scalars ..
      LOGICAL            LSIDE, NOUNIT, UPPER
      INTEGER            I, INFO, J, K, NROWA
      DOUBLE PRECISION   TEMP
c     .. Parameters ..
      DOUBLE PRECISION   ONE         , ZERO
      PARAMETER        ( ONE = 1.0D+0, ZERO = 0.0D+0 )
c     ..
c     .. Executable Statements ..
c
c     Test the input parameters.
c
      LSIDE  = LSAME( SIDE  , 'L' )
      IF( LSIDE )THEN
         NROWA = M
      ELSE
         NROWA = N
      END IF
      NOUNIT = LSAME( DIAG  , 'N' )
      UPPER  = LSAME( UPLO  , 'U' )
c
      INFO   = 0
      IF(      ( .NOT.LSIDE                ).AND.
     $         ( .NOT.LSAME( SIDE  , 'R' ) )      )THEN
         INFO = 1
      ELSE IF( ( .NOT.UPPER                ).AND.
     $         ( .NOT.LSAME( UPLO  , 'L' ) )      )THEN
         INFO = 2
      ELSE IF( ( .NOT.LSAME( TRANSA, 'N' ) ).AND.
     $         ( .NOT.LSAME( TRANSA, 'T' ) ).AND.
     $         ( .NOT.LSAME( TRANSA, 'C' ) )      )THEN
         INFO = 3
      ELSE IF( ( .NOT.LSAME( DIAG  , 'U' ) ).AND.
     $         ( .NOT.LSAME( DIAG  , 'N' ) )      )THEN
         INFO = 4
      ELSE IF( M  .LT.0               )THEN
         INFO = 5
      ELSE IF( N  .LT.0               )THEN
         INFO = 6
      ELSE IF( LDA.LT.MAX( 1, NROWA ) )THEN
         INFO = 9
      ELSE IF( LDB.LT.MAX( 1, M     ) )THEN
         INFO = 11
      END IF
      IF( INFO.NE.0 )THEN
         CALL XERBLA( 'DTRSM ', INFO )
         RETURN
      END IF
c
c     Quick return if possible.
c
      IF( N.EQ.0 )
     $   RETURN
c
c     And when  alpha.eq.zero.
c
      IF( ALPHA.EQ.ZERO )THEN
         DO 20, J = 1, N
            DO 10, I = 1, M
               B( I, J ) = ZERO
   10       CONTINUE
   20    CONTINUE
         RETURN
      END IF
c
c     Start the operations.
c
      IF( LSIDE )THEN
         IF( LSAME( TRANSA, 'N' ) )THEN
c
c           Form  B := alpha*inv( A )*B.
c
            IF( UPPER )THEN
               DO 60, J = 1, N
                  IF( ALPHA.NE.ONE )THEN
                     DO 30, I = 1, M
                        B( I, J ) = ALPHA*B( I, J )
   30                CONTINUE
                  END IF
                  DO 50, K = M, 1, -1
                     IF( B( K, J ).NE.ZERO )THEN
                        IF( NOUNIT )
     $                     B( K, J ) = B( K, J )/A( K, K )
                        DO 40, I = 1, K - 1
                           B( I, J ) = B( I, J ) - B( K, J )*A( I, K )
   40                   CONTINUE
                     END IF
   50             CONTINUE
   60          CONTINUE
            ELSE
               DO 100, J = 1, N
                  IF( ALPHA.NE.ONE )THEN
                     DO 70, I = 1, M
                        B( I, J ) = ALPHA*B( I, J )
   70                CONTINUE
                  END IF
                  DO 90 K = 1, M
                     IF( B( K, J ).NE.ZERO )THEN
                        IF( NOUNIT )
     $                     B( K, J ) = B( K, J )/A( K, K )
                        DO 80, I = K + 1, M
                           B( I, J ) = B( I, J ) - B( K, J )*A( I, K )
   80                   CONTINUE
                     END IF
   90             CONTINUE
  100          CONTINUE
            END IF
         ELSE
c
c           Form  B := alpha*inv( A_prime )*B.
c
            IF( UPPER )THEN
               DO 130, J = 1, N
                  DO 120, I = 1, M
                     TEMP = ALPHA*B( I, J )
                     DO 110, K = 1, I - 1
                        TEMP = TEMP - A( K, I )*B( K, J )
  110                CONTINUE
                     IF( NOUNIT )
     $                  TEMP = TEMP/A( I, I )
                     B( I, J ) = TEMP
  120             CONTINUE
  130          CONTINUE
            ELSE
               DO 160, J = 1, N
                  DO 150, I = M, 1, -1
                     TEMP = ALPHA*B( I, J )
                     DO 140, K = I + 1, M
                        TEMP = TEMP - A( K, I )*B( K, J )
  140                CONTINUE
                     IF( NOUNIT )
     $                  TEMP = TEMP/A( I, I )
                     B( I, J ) = TEMP
  150             CONTINUE
  160          CONTINUE
            END IF
         END IF
      ELSE
         IF( LSAME( TRANSA, 'N' ) )THEN
c
c           Form  B := alpha*B*inv( A ).
c
            IF( UPPER )THEN
               DO 210, J = 1, N
                  IF( ALPHA.NE.ONE )THEN
                     DO 170, I = 1, M
                        B( I, J ) = ALPHA*B( I, J )
  170                CONTINUE
                  END IF
                  DO 190, K = 1, J - 1
                     IF( A( K, J ).NE.ZERO )THEN
                        DO 180, I = 1, M
                           B( I, J ) = B( I, J ) - A( K, J )*B( I, K )
  180                   CONTINUE
                     END IF
  190             CONTINUE
                  IF( NOUNIT )THEN
                     TEMP = ONE/A( J, J )
                     DO 200, I = 1, M
                        B( I, J ) = TEMP*B( I, J )
  200                CONTINUE
                  END IF
  210          CONTINUE
            ELSE
               DO 260, J = N, 1, -1
                  IF( ALPHA.NE.ONE )THEN
                     DO 220, I = 1, M
                        B( I, J ) = ALPHA*B( I, J )
  220                CONTINUE
                  END IF
                  DO 240, K = J + 1, N
                     IF( A( K, J ).NE.ZERO )THEN
                        DO 230, I = 1, M
                           B( I, J ) = B( I, J ) - A( K, J )*B( I, K )
  230                   CONTINUE
                     END IF
  240             CONTINUE
                  IF( NOUNIT )THEN
                     TEMP = ONE/A( J, J )
                     DO 250, I = 1, M
                       B( I, J ) = TEMP*B( I, J )
  250                CONTINUE
                  END IF
  260          CONTINUE
            END IF
         ELSE
c
c           Form  B := alpha*B*inv( A_prime ).
c
            IF( UPPER )THEN
               DO 310, K = N, 1, -1
                  IF( NOUNIT )THEN
                     TEMP = ONE/A( K, K )
                     DO 270, I = 1, M
                        B( I, K ) = TEMP*B( I, K )
  270                CONTINUE
                  END IF
                  DO 290, J = 1, K - 1
                     IF( A( J, K ).NE.ZERO )THEN
                        TEMP = A( J, K )
                        DO 280, I = 1, M
                           B( I, J ) = B( I, J ) - TEMP*B( I, K )
  280                   CONTINUE
                     END IF
  290             CONTINUE
                  IF( ALPHA.NE.ONE )THEN
                     DO 300, I = 1, M
                        B( I, K ) = ALPHA*B( I, K )
  300                CONTINUE
                  END IF
  310          CONTINUE
            ELSE
               DO 360, K = 1, N
                  IF( NOUNIT )THEN
                     TEMP = ONE/A( K, K )
                     DO 320, I = 1, M
                        B( I, K ) = TEMP*B( I, K )
  320                CONTINUE
                  END IF
                  DO 340, J = K + 1, N
                     IF( A( J, K ).NE.ZERO )THEN
                        TEMP = A( J, K )
                        DO 330, I = 1, M
                           B( I, J ) = B( I, J ) - TEMP*B( I, K )
  330                   CONTINUE
                     END IF
  340             CONTINUE
                  IF( ALPHA.NE.ONE )THEN
                     DO 350, I = 1, M
                        B( I, K ) = ALPHA*B( I, K )
  350                CONTINUE
                  END IF
  360          CONTINUE
            END IF
         END IF
      END IF
c
      RETURN
c
c     End of DTRSM .
c
      END
c***********************************************************************
      integer function idamax(n,dx,incx)
c
c     finds the index of element having max. absolute value.
c     jack dongarra, linpack, 3/11/78.
c     modified 3/93 to return if incx .le. 0.
c     modified 12/3/93, array(1) declarations changed to array(*)
c
      double precision dx(*),dmax
      integer i,incx,ix,n
c
      idamax = 0
      if( n.lt.1 .or. incx.le.0 ) return
      idamax = 1
      if(n.eq.1)return
      if(incx.eq.1)go to 20
c
c        code for increment not equal to 1
c
      ix = 1
      dmax = dabs(dx(1))
      ix = ix + incx
      do 10 i = 2,n
         if(dabs(dx(ix)).le.dmax) go to 5
         idamax = i
         dmax = dabs(dx(ix))
    5    ix = ix + incx
   10 continue
      return
c
c        code for increment equal to 1
c
   20 dmax = dabs(dx(1))
      do 30 i = 2,n
         if(dabs(dx(i)).le.dmax) go to 30
         idamax = i
         dmax = dabs(dx(i))
   30 continue
      return
      end
c***********************************************************************
