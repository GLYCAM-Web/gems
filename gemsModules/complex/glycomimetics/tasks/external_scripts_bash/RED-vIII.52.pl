#!/usr/bin/perl -w
# use warnings;
use Math::Round;
use Math::Trig;
use FileHandle;
use File::Basename;
use constant PI => 3.14159265358979;
                 #######################################################
                 ##               R.E.D. version III.52               ##
                 ##        http://q4md-forcefieldtools.org/RED/       ##
                 ##                                                   ##
                 ##                    UPJV - SBIMR                   ##
                 ##                                                   ##
                 ##      Authorship: See the program signature        ##
                 ##                                                   ##
                 ## Distributed under the GNU General Public License  ##
                 #######################################################
#-------------------------------------------------------------------------------------------------------
#------------------------------------------ VERIFICATIONS ----------------------------------------------
#-------------------------------------------------------------------------------------------------------
sub Verification{
	# system("clear");
#----------------------------------------------- X R.E.D. ----------------------------------------------
	$XRED =~ s/^\s*(.*?)\s*$/$1/;  $XRED = uc($XRED); 
	if(($XRED ne "ON") && ($XRED ne "OFF")){ $XRED = "OFF" }
	if($XRED eq "ON"){
		$i=0;
		if (-e "./RED.cfg"){
			open(CFG,"<RED.cfg");
			foreach (<CFG>){
				if(!/#/ig){
					if($i==0){ $QMSOFT=$_;      chomp($QMSOFT); }
					if($i==1){ $OPT_Calc=$_;    chomp($OPT_Calc); }
					if($i==2){ $MEPCHR_Calc=$_; chomp($MEPCHR_Calc); }
					if($i==3){ $Re_Fit=$_;      chomp($Re_Fit); }
					if($i==4){ $CHR_TYP=$_;     chomp($CHR_TYP); }
					if($i==5){ $DIR=$_;         chomp($DIR); }
					if($i==6){ $NP=$_;          chomp($NP); }
					if($i==7){ $COR_CHR=$_;     chomp($COR_CHR); }
					$i++;
				}
			}
			close(CFG);
		}
		XTerminal();
	}   
	print "\t\t      ---------------------------\n";
	print "\t\t     *  Welcome to R.E.D. III.52 *\n";
	print "\t\t         RESP ESP charge Derive  \n";
	print "\t\t  http://q4md-forcefieldtools.org/RED/ \n\n";
	print "\t\t         CHARGE TYPE = $CHR_TYP\n";
	if($CHR_TYP eq "DEBUG"){ print "   Job generated for debugging purposes - Charge values are rotten!\n"; }
	print "\t\t      ---------------------------\n";
	print "\t\tDistributed under the GNU General Public License\n";
	print "\t\t      ---------------------------\n";
	print "\t\t  Date: ";
	system ("date");
	chomp($hostname=`hostname`);
	print "\t\t  Machine: $hostname\n";
	print "\t\t      ---------------------------\n";
	print "\t\t  Number of cpu(s) used in the QM jobs(s): $NP\n";
	print "\t\t      ---------------------------\n";
	chomp($OS=`uname -a`);
	print "\n\t\t        * Operating system *\n$OS\n";
#---------------------------------------Verification of variables ---------------------------------------------
	if($<==0){
		print "\n\t\tERROR: DO NOT RUN THIS SCRIPT AS ROOT !\n\n"; $check=0; Information();
		if($XRED eq "ON"){ print "\t\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
	}
	$verif=1;
	$DIR =~ s/^\s*(.*?)\s*$/$1/;
	if($DIR eq ""){ $DIR = "Data-RED"; } 
	$Re_Fit =~ s/^\s*(.*?)\s*$/$1/; $Re_Fit=uc($Re_Fit);
	if(($Re_Fit ne "ON") && ($Re_Fit ne "OFF")){ print "\n\t\tERROR: Check the variable Re_Fit\n\n"; $verif=0; }
	if($Re_Fit eq "OFF"){
		$NP =~ s/^\s*(.*?)\s*$/$1/;
		if(($NP eq "") || ($NP =~ /[a-zA-Z]|\-|\+|\.|\,|\<|\>|\=|0/)){ print "\n\tERROR: Wrong number of processor(s) for QM calculation(s)\n\n"; $verif=0; }
		$OPT_Calc =~ s/^\s*(.*?)\s*$/$1/;  $OPT_Calc=uc($OPT_Calc);
		if(($OPT_Calc ne "ON") && ($OPT_Calc ne "OFF")){ print "\n\t\tERROR: Check the variable OPT_Calc\n\n"; $verif=0; }
		$MEPCHR_Calc =~ s/^\s*(.*?)\s*$/$1/;  $MEPCHR_Calc=uc($MEPCHR_Calc);
		if(($MEPCHR_Calc ne "ON") && ($MEPCHR_Calc ne "OFF")){ print "\n\t\tERROR: Check the variable MEPCHR_Calc\n\n"; $verif=0; }
		if(($OPT_Calc eq "OFF") && ($MEPCHR_Calc eq "OFF")){ print "\n\t\tWARNING: Nothing is done. Select a task!\n\n"; $verif=0; }
	}
	if(($MEPCHR_Calc eq "ON") || ($Re_Fit eq "ON")){
		$CHR_TYP =~ s/^\s*(.*?)\s*$/$1/; $CHR_TYP = uc($CHR_TYP);
		if(($CHR_TYP ne "DEBUG") and ($CHR_TYP ne "RESP-A1") and ($CHR_TYP ne "RESP-C1") and ($CHR_TYP ne "RESP-A2") and ($CHR_TYP ne "RESP-C2") and ($CHR_TYP ne "ESP-A1") and ($CHR_TYP ne "ESP-A2") and ($CHR_TYP ne "ESP-C1") and ($CHR_TYP ne "ESP-C2")){
			print "\n\t\tERROR: CHR_TYP must be RESP-A or C, 1 or 2 _or_ ESP-A or C, 1 or 2\n\n"; $verif=0; }
	}
	$QMSOFT =~ s/^\s*(.*?)\s*$/$1/; $QMSOFT=uc($QMSOFT);
	if($QMSOFT eq "GAMESS-US") { $QMSOFT = "GAMESS"; }
	if($QMSOFT eq "PC-GAMESS") { $QMSOFT = "FIREFLY"; }
	if(($QMSOFT ne "GAMESS") && ($QMSOFT ne "FIREFLY") && ($QMSOFT ne "GAUSSIAN")){
		print "\n\t\tERROR: Select GAMESS, Firefly or Gaussian\n\n"; $verif=0; }
	if($verif==0){
		$check=0; Information();
		if($XRED eq "ON"){ print "\t\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
	}
	if($Re_Fit eq "ON"){
		$OPT_Calc="OFF"; $MEPCHR_Calc="OFF"; 
		print "\n\nCharge re-fitting & force field library re-building from a previous R.E.D. run"; 
		if(!-e $DIR) { print "\n\n\tERROR: The directory containing the data of the previous R.E.D. run was not found."; $verif=0; }
		else{ print "\n\tThe \"$DIR\" directory is used as a previous R.E.D. run."; }
		print "\n\tSee the HowTo-III.x.pdf file for more information...\n\n";
	}
#----------------------- Verifications of files ---------------------------------------------
	#******************************RED-2012******************************
	@GLOBAL_intra_mcc=();
	#******************************RED-2012******************************
	$countmolimrs=$NM=1;
	if(!-e "Mol_red$NM.p2n"){
		print "\n\tERROR: The initial P2N file can not be found\n\n"; $check=0; Information();
		if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
	}
	while(-e "Mol_red$NM.p2n"){ $countmolimrs=$NM; $NM++; }
	$NM=1;
	if(($CHR_TYP eq "ESP-A2")||($CHR_TYP eq "ESP-C2")){
		print "\n\t\t\t         WARNING:\n\t\t \"ESP-A2\" \& \"ESP-C2\" charge models are outdated \n\tNowdays, they should _not_ be used in atomic charge derivation \n   These models are only available in R.E.D. for compatibility with the past\n";}
	if(($CHR_TYP eq "ESP-A2") && ($countmolimrs!=1) || ($CHR_TYP eq "ESP-C2") && ($countmolimrs!=1)){
		print "\n\t\t\t         WARNING:\n   \"ESP-A2\" \& \"ESP-C2\" charge models \& multi-molecule ESP charge derivation\n\t\t\t are not supported in R.E.D.-III.x\n    Job(s) will be performed as a batch; each molecule being independent\n ";}
	print "\nDID YOU PREPARE YOUR P2N INPUT FILES USING ANTE_R.E.D. 2.0/R.E.D SERVER?";
	print "\nWE STRONGLY RECOMMAND YOU TO USE ANTE_R.E.D. 2.0/R.E.D SERVER TO PREPARE YOUR P2N FILES...\n";
	if ($COR_CHR eq "1")    { print "\n\tCharge correction will be carried out at 1.10-1 e.\n"; }
	elsif ($COR_CHR eq "2") { print "\n\tCharge correction will be carried out at 1.10-2 e.\n"; }
	elsif ($COR_CHR eq "3") { print "\n\tCharge correction will be carried out at 1.10-3 e.\n"; }
	elsif ($COR_CHR eq "4") { print "\n\tCharge correction will be carried out at 1.10-4 e.\n"; }
	elsif ($COR_CHR eq "5") { print "\n\tCharge correction will be carried out at 1.10-5 e.\n"; }
	elsif ($COR_CHR eq "6") { print "\n\tCharge correction will be carried out at 1.10-6 e.\n"; }
	else { print "\n\tCharge correction will not be carried out.\n"; }
	#******************************RED-2012******************************
	#-----GEOM-OPT-CONSTRAINT-------------
	$mark_constraint=1;
	if(($QMSOFT eq "FIREFLY")||($QMSOFT eq "GAMESS") ){ $mark_constraint=0;	}
	@remarks_geom       = ();
	@remarks_geom_exist = ();	
	@remarks_geom_checked = ();
	#-----GEOM-OPT-CONSTRAINT-------------
	#******************************RED-2012******************************
	while(-e "Mol_red$NM.p2n"){
		# if($NM !=1 ){sleep(5);}

		#******************************RED-2012******************************
		#-----GEOM-OPT-CONSTRAINT-------------
		my $remarks_exist = 0;
		#-----GEOM-OPT-CONSTRAINT-------------
		#******************************RED-2012******************************
		
		$MOL_START="Mol_red$NM.p2n";
		$JOB_OPT="Mol_red$NM.log";
		$dfmol=$NM;
		$TITLE[$NM]=$CHR_VAL[$NM]=$MLT_VAL[$NM]="undefined";
		if($countmolimrs==1){
			print "\n  =========================================================================== ";
			print "\n  =======================     Single molecule     =========================== \n";
		}else{
			print "\n  =========================================================================== ";
			print "\n  =======================  Checking molecule $NM !  =========================== \n";
		}
		open (MOL_PDB, "<$MOL_START"); 
		$ter=$testchgmlt=0;
		foreach(<MOL_PDB>){
			
			#******************************RED-2012******************************
			#-----GEOM-OPT-CONSTRAINT-------------
			if ((/^REMARK GEOM-OPT-CONSTRAINT/ig)&($ter == 0)) {
				( my $geom ) = ( split(/GEOM-OPT-CONSTRAINT/) )[1];
				push( @remarks_geom, [ $NM, $geom ] );
				$remarks_exist = 1;
			}
			#-----GEOM-OPT-CONSTRAINT-------------
			#******************************RED-2012******************************
			
			if((/^REMARK TITLE/ig) && ($ter==0)){
				($TITLE[$NM]) = (split(' '))[2];
				if (defined ($TITLE[$NM])) { $TITLE[$NM] =~ s/^\s*(.*?)\s*$/$1/; }
				else { $TITLE[$NM]="undefined"; }
			}
			if((/^REMARK CHARGE-VALUE/ig) && ($ter==0)){
				($CHR_VAL[$NM]) = (split(' '))[2];
				if (defined($CHR_VAL[$NM])){
					$CHR_VAL[$NM] =~ s/^\s*(.*?)\s*$/$1/;
					if(($CHR_VAL[$NM] eq "")||($CHR_VAL[$NM] !~ /^[\+\-]?\d+$/)){ $testchgmlt=1; }
				}else { $CHR_VAL[$NM]="undefined"; }
			}
			if((/^REMARK MULTIPLICITY-VALUE/ig) && ($ter==0)){
				($MLT_VAL[$NM]) = (split(' '))[2];
				if (defined($MLT_VAL[$NM])) {
					$MLT_VAL[$NM] =~ s/^\s*(.*?)\s*$/$1/;
					if(($MLT_VAL[$NM] eq "") || (($MLT_VAL[$NM] !~ /^\d+$/) || ($MLT_VAL[$NM] =~ /^0$/))) { $testchgmlt=1; }
				}else { $MLT_VAL[$NM]="undefined"; }
			}
			if  (/^TER/ig) { $ter=1; }
		}
		close(MOL_PDB);
		
		#******************************RED-2012******************************
		#-----GEOM-OPT-CONSTRAINT-------------
		push( @remarks_geom_exist, $remarks_exist );
		#-----GEOM-OPT-CONSTRAINT-------------
		#******************************RED-2012******************************
		
		if($TITLE[$NM] eq "undefined"){ $TITLE[$NM]= "Molecule_$NM"; $titletest[$NM]=1;
		}else{ $titletest[$NM]=0; }
		if($CHR_VAL[$NM] eq "undefined"){ $CHR_VAL[$NM]= 0; $chrtest[$NM]=1
		}else{ $chrtest[$NM]=0; }
		if($MLT_VAL[$NM] eq "undefined"){ $MLT_VAL[$NM]= 1; $mlttest[$NM]=1;
		}else{ $mlttest[$NM]=0; }
		if($titletest[$NM]==0){ print "\t The molecule TITLE is \"$TITLE[$NM]\"\n";}
		if($titletest[$NM]==1){ print "\t  No molecule TITLE found: \"$TITLE[$NM]\" is automatially set\n"; }
		if($chrtest[$NM]==0){ print "\t\tThe TOTAL CHARGE value of the molecule is \"$CHR_VAL[$NM]\"\n"; }
		if($chrtest[$NM]==1){ print "\tNo TOTAL CHARGE value found: Value automatically set to \"0\"\n"; }
		if($mlttest[$NM]==0){ print "\t      The SPIN MULTIPLICITY value of the molecule is \"$MLT_VAL[$NM]\"\n"; }
		if($mlttest[$NM]==1){ print "      No spin MULTIPLICITY VALUE found: Value automatically set to \"1\"\n"; }
		print "  =========================================================================== \n";
		if($testchgmlt==1){
			print "\n\tERROR: Wrong charge and/or multiplicity value\n\tSee the $MOL_START file\n\n"; $check=0; Information();
			if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
		}
		Readpdb();
		$OUTP[$NM]=$QMSOFT;								# If the minimization is "on", then the output equals the selected software
		if((($OPT_Calc eq "OFF") && ($MEPCHR_Calc eq "ON")) || ($Re_Fit eq "ON")){	# If not, its type has to be determined
			$JOB_OPT =~ s/^\s*(.*?)\s*$/$1/;
			$_=$JOB_OPT;
			if (!-e $JOB_OPT){
				print "\n\tERROR: The optimization OUTPUT can not be found\n\n"; $check=0; Information();
				if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
			}
			$ok=0;
			open (LOGFILE1, "<$JOB_OPT");
			$OUTP[$NM]="null"; 								# Type of the output: "null" if the output is not recognized
			$testconf=$testconf2=$testconf3=0;
			foreach (<LOGFILE1>){
				if(/M.W.SCHMIDT, K.K.BALDRIDGE, J.A.BOATZ/ig) { $OUTP[$NM]="GAMESS"; }
				if(/gran\@classic.chem.msu.su/ig) { $OUTP[$NM]="FIREFLY"; }
				elsif(/M. J. Frisch, G. W. Trucks, H. B. Schlegel/ig) { $OUTP[$NM]="GAUSSIAN"; }
			}
			close(LOGFILE1);
			if($OUTP[$NM] eq "null"){ print "\n\t\t        Unknown output detected !";
			}elsif(($OUTP[$NM] eq "GAMESS") || ($OUTP[$NM] eq "FIREFLY")){			#------ GAMESS output ------
				print "\n\t\t    * Selected optimization output *\n\t\t\t\t$OUTP[$NM]";
				open (LOGFILE1, "<$JOB_OPT");
				foreach (<LOGFILE1>){ if(/TERMINATED NORMALLY/ig){ $ok=1; $testconf++;} }
				close(LOGFILE1);
				if($ok == 1){
					$ok=$testspf=0; $oksp=1;					# Test if this is a single point energy calc.
					open (LOGFILE1, "<$JOB_OPT");
					foreach (<LOGFILE1>){	if(/EQUILIBRIUM GEOMETRY LOCATED/ig){ $testspf++; $ok=1; $oksp=0; } }
					close(LOGFILE1);
					if ($testconf != $testspf) { $ok=0; $oksp=1; }
				}
				$i=$okr=$flag1=$flag2=$flag3=$nbatoms2[$NM]=0;
				if($ok==1){
					open(JOB1,"<$JOB_OPT");
					foreach (<JOB1>){
						if(/EQUILIBRIUM GEOMETRY LOCATED/ig){ $flag1=1; $testconf2++; }
						if(/TERMINATED NORMALLY/ig){ $flag2=1; }
						if(($flag1 == 1) && ($flag2 == 0)){
							if(/^\s\w+\s+\d+\.\d+\s+(\-\d+|\d+)\.\d+\s+(\-\d+|\d+)\.\d+\s+(\-\d+|\d+)\.\d+/){
								($numatomic)=(split(' '))[1];
								if(defined ($tab[3][$i][$NM])){
									if($tab[3][$i][$NM] != $numatomic){ $ok=0; $okr=1; }
									$i++;  $nbatoms2[$NM]++;
								}else{ $ok=0; }
							}
						}
						if(($flag1 == 1)&&($flag2 == 1)){ $flag1=$flag2=$i=0; }
					}
					close(JOB1);
					if (($testconf != $nbconf[$NM]) || ($testconf2 != $nbconf[$NM])) { $ok=0; }
				}
				$nbatoms2[$NM] = $nbatoms2[$NM]/$nbconf[$NM];
			}elsif($OUTP[$NM] eq "GAUSSIAN"){						#------ GAUSSIAN output------
				print "\n\t\t    * Selected optimization output *\n\t\t\t\t$OUTP[$NM]";
				open (LOGFILE1, "<$JOB_OPT");
				foreach (<LOGFILE1>){	if(/Normal termination of Gaussian/ig){ $ok=1; $testconf++;} }
				close(LOGFILE1);
				if($ok == 1){
					$ok=0; $oksp=1; $testspf=0;					# Test if this is a single point energy calc.
					open (LOGFILE1, "<$JOB_OPT");
					foreach (<LOGFILE1>){	if(/Stationary point found/ig){ $testspf++; $ok=1; $oksp=0; } }
					close(LOGFILE1);
					if ($testconf != $testspf) { $ok=0; $oksp=1; }
				}
				if($ok == 1){
					$okf0=$okf1=$okf2=$okf3=0;					# Test if optimization & frequency job in the same QM output
					open (LOGFILE1, "<$JOB_OPT");
					foreach (<LOGFILE1>){
						if(/Normal termination of Gaussian/ig){ $okf0=1; }
						if(($okf0==1) && (/Proceeding to internal job step number/ig)) { $okf1=1; $okf3=1; $okf0=0; } 
						if(($okf3==1) && (/APT atomic charges:/ig)) { $okf2=1; $okf3=0; }
					}
					close(LOGFILE1);
				}
				if($ok == 1){
					$ok=$ok2=$ok3=$verifconf=$count=0;				# If there is no "Standard orientation" between "Stationary point found"
					open (LOGFILE1, "<$JOB_OPT");					# & "Normal termination of Gaussia", then the output is not valid.
					foreach (<LOGFILE1>){							
						if(/Normal termination of Gaussian/ig){
							$count++;
							if ($count > $testconf3){ $verifconf=1; $ok3=1; }
						}								
						if(/Stationary point found/ig){ $ok2=1; $testconf2++; }
						if(($ok2==1)&&(/Standard orientation/ig)){ $ok=1; $ok2=0; $testconf3++; }
					}
					close(LOGFILE1);
				}
				$i=$okr=$flag0=$flag1=$flag2=$flag3=$nbatoms2[$NM]=0;
				if($ok == 1){
					open(JOB1,"<$JOB_OPT");
					foreach (<JOB1>){
						if(/Stationary point found/ig){ $flag0=1; }
						if((/Standard orientation:/ig) && ($flag0 == 1)){ $flag1=1; }
						if(($flag1 == 1) && ($flag2 <6)){ $flag2++; }
						if(($flag2 == 6) && ($flag3 == 0)){
							if(/\s+\d+\s+\d+\s+(\s|-|-\d+|\d+)\.\d+\s+(\s|-|-\d+|\d+)\.\d+\s+(\s|-|-\d+|\d+)\.\d+/){
								($numatomic)=(split(' '))[1];
								if(defined ($tab[3][$i][$NM])){
									if($tab[3][$i][$NM] != $numatomic){ $ok=0; $okr=1; }
									$i++;  $nbatoms2[$NM]++;
								}else{ $ok=0; }
							}else{ $flag3=1; }
						}
					}
					if( ($testconf != $nbconf[$NM]) || ($testconf2 != $nbconf[$NM]) || ($testconf3 != $nbconf[$NM]) || ($verifconf == 1) ) { $ok=0; }
					close(JOB1);
				}
			}else{ $ok=0; }
			if(($ok==1) && ($nbatoms[$NM] == $nbatoms2[$NM])){
				print "\n\t\t    Optimization OUTPUT looks nice ! \n";
			}else{
				print "\n\t\t      Invalid optimization OUTPUT ! \n\n";
				if ($oksp==1) {
					print "\tSingle point energy calculation detected in the QM output\n";
					print "\tYou need to provide a geometry optimization output\n\n";
				}else {
					if (($okf1==1) && ($okf2==1) && ($ok3==1)) {
						print "\tA frequency job is found after the geometry optimization\n";
						print "\tYou need to remove this frequency job from the Gaussian output\n\n";
					}
					if (($okf1!=1) && ($okf2!=1) && ($ok3==1)) {
						print "\tNo Standard orientation found after the Stationary point\n\n";
					}
					if ($okr==1) {
						print "\tThe atom order in the P2N file and QM output are not compatible\n\n";
					}
				}
				$check=0; Information();
				if($XRED eq "ON"){ print "\t\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
			}
		}
		print "\n\t\t     * $nbconf[$NM] conformation(s) selected *\n";
		if($atombrut[$NM]==1){
			print "\n\t\t\t       WARNING:\n\t\t  A 2nd column of atom names is detected";
			print "\n        This 2nd column will be used in the PDB (\& Tripos) file(s)\n";
		}elsif($atombrut[$NM]==2){
			print "\n\t\t\t       WARNING:\n\t\t  A unique atom name column is detected";
			print "\n        The atom names in the PDB (\& Tripos) file(s) will be incremented\n";
		}
		if((($nbconect[$NM]==0) && ($MEPCHR_Calc eq "ON")) || (($nbconect[$NM]==0) && ($Re_Fit eq "ON"))){
			print "\n\t\t\t       WARNING:\n\t     No connectivity information found in the P2N file";
			print "\n\t      The Tripos mol2 file(s) will NOT be generated !\n";
		}
		if(($nbrot[$NM]>0) || ($nbrot_rotate[$NM]>0) || ($nb_translate[$NM]>0)){ # Elodie - April 2010 - Beginning
			print "\n\t    * Selected three atom based re-orientation(s) *";
			if($nbrot[$NM]>0){ 
				print "\n\t                 $nbrot[$NM] re-orientation(s):\n";
				for($i=0;$i<$nbrot[$NM];$i++){	printf("\t\t\t  %3d    %3d    %3d \n",$rot[$i][0][$NM],$rot[$i][1][$NM],$rot[$i][2][$NM]); }
			}
			if($nbrot_rotate[$NM]>0){
				print "\n\t                 $nbrot_rotate[$NM] rotation(s):\n";
				for($i=0;$i<$nbrot_rotate[$NM];$i++){	printf("\t\t\t  %3d    %3d    %3d \n",$rot_rotate[$i][0][$NM],$rot_rotate[$i][1][$NM],$rot_rotate[$i][2][$NM]); }
			}
			if($nb_translate[$NM]>0 ){ 
				print "\n\t                 $nb_translate[$NM] translation(s):\n";
				for($i=0;$i<$nb_translate[$NM];$i++){	printf("\t\t\t  %3.2f    %3.2f    %3.2f \n",$trans[$i][0][$NM],$trans[$i][1][$NM],$trans[$i][2][$NM]); }
			}
			$nbmod[$NM]=$nbrot[$NM]+$nbrot_rotate[$NM]+$nb_translate[$NM];
			$reorient[$NM]=1;
		}else{
			$nbmod[$NM]=1;
			print "\n\t\t\t       WARNING:\n\t No three atom based re-orientation found in the P2N file\n";
			print "     Re-orientation will be done according to the $OUTP[$NM] Algorithm!\n";
		} # Elodie - April 2010 - End
		if($verifimr[$NM]==2){
			print "\n\t    * Selected intra-molecular charge constraint(s) *\n";
			$y=0;
			for($y=0; $y<$imrcount[$NM]; $y++){
				if($intramr[3][$y][$NM]=~/[K]/){ $flagimr="Keep"; }
				elsif($intramr[3][$y][$NM]=~/[R]/){ $flagimr="Remove"; }
				if($intramr[1][$y][$NM]=~/\-/){
					printf("\t\t  %3.4f | %3s | %3s \n",$intramr[1][$y][$NM],$intramr[2][$y][$NM],$flagimr);
				}else{	printf("\t\t   %3.4f | %3s | %3s \n",$intramr[1][$y][$NM],$intramr[2][$y][$NM],$flagimr); }
			}
		}
		
		#******************************RED-2012******************************
		#-----GEOM-OPT-CONSTRAINT-------------
		if($remarks_exist==1){
			if($mark_constraint==1){
				print "\n\t      * Constraint(s) in geometry optimization *\n";
				verif_constraint($NM);
				print "\n";
			}else{			
				print "\n\t      * Constraint(s) in geometry optimization *\n";
				print "\n   Geometry optimization constraints are only implemented for the Gaussian program!\n";
			}
		}
		#-----GEOM-OPT-CONSTRAINT-------------
		#******************************RED-2012******************************
		
		$NM++;
	}
	Read_imrs();
#------------- GAMESS - Gaussian - verifications -------------------
	$verif=1;
	if($Re_Fit eq "OFF"){ print "\n\t\t        * Selected QM Software *\n\t\t\t        $QMSOFT \n"; }
	print "\n\t\t         * Software checking *\n";
	if($Re_Fit eq "OFF"){
		$PCGVAR=0; $MPIVAR=1;
		if($QMSOFT eq "GAMESS"){							#------ GAMESS ------
			if($OS=~/CYGWIN/){							#--- WinGAMESS is used ---
				if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
				if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }		# To change stdout
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
				chomp($csh=`which csh.exe`);					#--- csh.exe ---
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
				if(($csh=~m/Command not found/ig) || ($csh=~m/not in/ig) || ($csh=~m/no csh.exe in/ig) || ($csh=~m/no csh in/ig) || ($csh eq "")){
					print "\t   csh.exe \t\t\t\t\t\t[ NOT FOUND ]\n"; $verif=0;
				}else{	print "\t   csh.exe \t\t\t\t\t\t\t[ OK ]\n"; }
				if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
				if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }		# To change stdout
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
				chomp($runscript=`which runscript.csh`);			#--- runscript.csh ---
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
				if(($runscript=~m/Command not found/ig) || ($runscript=~m/not in/ig) || ($runscript=~m/no runscript.csh in/ig) || ($runscript eq "")){
					print "\t   runscript.csh \t\t\t\t\t[ NOT FOUND ]\n"; $verif=0;
				}else{	print "\t   runscript.csh \t\t\t\t\t\t[ OK ]\n"; 
					$pathwingamess=dirname($runscript);
				}
				$gx=$hear=0;					# If several GAMESS binaries are available, the smallest number is used (gamess.0$n.exe)
				while(($gx<10) && ($hear==0)){
					if ($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
					if ($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
					if ($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
					chomp($gamessx=`which gamess.0$gx.exe`);
					if ($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
					if(($gamessx =~ m/Command not found/ig)||($gamessx =~ m/not in/ig)||($gamessx =~ m/no gamess.0/ig)||($gamessx eq "")){
					}else{ print"\t   gamess.0$gx.exe \t\t\t\t\t\t[ OK ]\n"; $hear=1; }
					$gx++;
				}
				$gx--;	$gx="0".$gx;
				if($hear==0){	print"\t   gamess.0n.exe  (n = 0->9)\t\t\t\t[ NOT FOUND ]\n";	
					print"\t   Rename \"gamess.version-nb.x\" into \"gamess.01.exe\" ?\n"; $verif=0;}
				if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
				if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
				chomp($ddikick=`which ddikick.exe`);			#--- ddikick.exe ---
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
				if(($ddikick =~ m/Command not found/ig)||($ddikick =~ m/not in/ig)||($ddikick =~ m/no ddikick.exe in/ig)||($ddikick =~ m/no ddikick in/ig)||($ddikick eq "")){
					print"\t   ddikick.exe \t\t\t\t\t\t[ NOT FOUND ]\n"; $verif=0;
				}else{	print"\t   ddikick.exe \t\t\t\t\t\t\t[ OK ]\n"; }
				
			}else{								#--- GAMESS compiled from sources is used ---
				$gx=$hear=0;						# If several GAMESS binaries are available, the smallest number is used (gamess.0$n.x)
				while(($gx<10) && ($hear==0)){
					if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
					if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
					if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
					chomp($gamessx=`which gamess.0$gx.x`);
					if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
					if(($gamessx =~ m/Command not found/ig)||($gamessx =~ m/not in/ig)||($gamessx =~ m/no gamess.0/ig)||($gamessx eq "")){}
					else{	print"\t   gamess.0$gx.x \t\t\t\t\t\t\t[ OK ]\n"; 
						$pathgamessus=dirname($gamessx); chomp($pathgamessus); $hear=1;
					}
					$gx++;
				}
				$gx--; $gx="0".$gx;
				if($hear == 0){	print"\t   gamess.0n.x  (n = 0->9)\t\t\t\t\t[ NOT FOUND ]\n";	
						print"\t   Rename \"gamess.version-nb.x\" into \"gamess.00.x\" ?\n"; $verif=0;
						$pathgamessus="unknown";
				}
				if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
				if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }	# To change stdout
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
                                # To use R.E.D./GAMESS on a UNIX cluster using a PBS script to handle multiple copies of the rungms$X script
                                if (-e "$pathgamessus/rungms.info"){
                                        open(INFO,"< $pathgamessus/rungms.info");
                                        foreach(<INFO>){ $temprungms=$_; }
                                        close(INFO);
                                        chomp($temprungms);
                                        chomp($rungms=`which $temprungms`);
                                }
                                else { chomp($rungms=`which rungms`); }
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
				# print "variable rungms = $rungms\n"; # Debugging...
				# Add "($rungms =~ m/printed message/ig)"
				if(($rungms =~ m/Command not found/ig)||($rungms =~ m/not in/ig)||($rungms =~ m/no rungms in/ig)||($rungms eq "")){
					print "\t   rungms \t\t\t\t\t\t\t[ NOT FOUND ]\n"; $verif=0;
				}else{	print "\t   rungms \t\t\t\t\t\t\t[ OK ]\n"; }
				if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
				if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
				chomp($ddikick=`which ddikick.x`);			#--- ddikick.x ---
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
				if(($ddikick=~m/Command not found/ig) || ($ddikick =~ m/not in/ig) || ($ddikick=~m/no ddikick.x in/ig) || ($ddikick eq "")){
						print"\t   ddikick.x \t\t\t\t\t\t\t[ NOT FOUND ]\n"; $verif=0;
				}else{	print"\t   ddikick.x \t\t\t\t\t\t\t[ OK ]\n"; }
			}
		}elsif($QMSOFT eq "FIREFLY"){
			if ($OS =~ /CYGWIN/) {
				if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
				if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
				chomp($cygpath=`which cygpath`);
				if(($cygpath =~ m/Command not found/ig)||($cygpath =~ m/not in/ig)||($cygpath =~ m/no cygpath in/ig)||($cygpath eq "")){
					if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
					print"\t   Utility cygpath \t\t\t\t\t[ NOT FOUND ]\n";
					print"\t   cygpath is required to define various paths for Firefly under Cygwin\n"; $verif=0;
				}else {
					if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
					print"\t   Utility cygpath \t\t\t\t\t\t[ OK ]\n";
				}
			}
			if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
			if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
			if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
			chomp($firefly=`which firefly`);			#--- Firefly
			if(($firefly =~ m/Command not found/ig)||($firefly =~ m/not in/ig)||($firefly =~ m/no firefly in/ig)||($firefly eq "")){
				chomp($firefly=`which firefly.exe`);
				if(($firefly =~ m/Command not found/ig)||($firefly =~ m/not in/ig)||($firefly =~ m/no firefly.exe in/ig)||($firefly eq "")){
					chomp($firefly=`which pcgamess`);
					if(($firefly =~ m/Command not found/ig)||($firefly =~ m/not in/ig)||($firefly =~ m/no pcgamess in/ig)||($firefly eq "")){
						chomp($firefly=`which pcgamess.exe`);
						if(($firefly =~ m/Command not found/ig)||($firefly =~ m/not in/ig)||($firefly =~ m/no pcgamess.exe in/ig)||($firefly eq "")){
							if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
							print"\t   PC-GAMESS/Firefly   \t\t\t\t\t[ NOT FOUND ]\n"; $verif=0;
						}else{
							if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
							print"\t   pcgamess.exe \t\t\t\t\t\t[ OK ]\n"; $PCGVAR=1;
							$pathfirefly=dirname($firefly);
						}
					}else{	
						if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
						print"\t   pcgamess \t\t\t\t\t\t\t[ OK ]\n"; $PCGVAR=1;
						$pathfirefly=dirname($firefly);
					}
				}else{
					if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
					print"\t   firefly.exe \t\t\t\t\t\t\t[ OK ]\n"; $PCGVAR=1;
					$pathfirefly=dirname($firefly);
				}
			}else{
				if ($CHR_TYP ne "DEBUG") { open(STDOUT,">&OLDSTDOUT"); }
				print"\t   firefly \t\t\t\t\t\t\t[ OK ]\n"; $PCGVAR=1;
				$pathfirefly=dirname($firefly);
			}
			chomp($OS=uc(`uname`));
			if(($OS ne "DARWIN") && ($OS !~ /CYGWIN/)){
				if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
				if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
				chomp($mpirun=`which mpirun`);				#--- mpirun for pc-gamess under UNIX
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
				if(($mpirun=~m/Command not found/ig) || ($mpirun=~m/not in/ig) || ($mpirun=~m/no mpirun in/ig) || ($mpirun eq "")){ $MPIVAR=0; }
				if(($NP!=1) && ($MPIVAR==1)) { print"\t   mpirun \t\t\t\t\t\t\t[ OK ]\n"; }
				elsif(($NP!=1) && ($MPIVAR==0)) { 
					print"\t   mpirun \t\t\t\t\t\t[ NOT FOUND ]\n";
					print"\t   Firefly will be executed using a single cpu/core\n";
				}
			}
			if($OS eq "DARWIN"){						#--- Wine for Mac OS/Darwin
				print "\t\t\t        WARNING:\n";
				print "\t\t Firefly & Wine for Mac OS X is executed by R.E.D.\n";
				print "   /Applications/Darwine/Wine.bundle/Contents/bin/wine is hard coded in R.E.D.\n";
				if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
				if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
				chomp($wine=`ls /Applications/Darwine/Wine.bundle/Contents/bin/wine`);
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
				if(($wine =~ m/No such file or directory/ig)||($wine eq "")){
					print "\t   Wine for Mac OS X \t\t\t\t\t\t[ NOT FOUND ]\n"; $verif=0;
				}else{	print "\t   Wine for Mac OS X \t\t\t\t\t\t[ OK ]\n"; }
			}
		}else {									#------ Gaussian ------
			if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
			if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
			if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
			chomp($gauss=`which g09`);
			if(($gauss =~ m/Command not found/ig)||($gauss =~ m/not in/ig)||($gauss =~ m/no g09 in/ig)||($gauss eq "")){
				chomp($gauss=`which g03`);
				if(($gauss =~ m/Command not found/ig)||($gauss =~ m/not in/ig)||($gauss =~ m/no g03 in/ig)||($gauss eq "")){
					chomp($gauss=`which g98`);
					if(($gauss =~ m/Command not found/ig)||($gauss =~ m/not in/ig)||($gauss =~ m/no g98 in/ig)||($gauss eq "")){
						chomp($gauss=`which g94`);
						if(($gauss =~ m/Command not found/ig)||($gauss =~ m/not in/ig)||($gauss =~ m/no g94 in/ig)||($gauss eq "")){
						      if ($CHR_TYP ne "DEBUG") { open(STDOUT,">&OLDSTDOUT"); }
						      print"\t   Gaussian \t\t\t\t\t\t[ NOT FOUND ]\n"; $verif=0;
						}else{	if ($CHR_TYP ne "DEBUG") { open(STDOUT,">&OLDSTDOUT"); }
						      print"\t   g94 \t\t\t\t\t\t\t\t[ OK ]\n";
						}
					}else{	if ($CHR_TYP ne "DEBUG") { open(STDOUT,">&OLDSTDOUT"); }
					      print"\t   g98 \t\t\t\t\t\t\t\t[ OK ]\n";
					}
				}else{	if ($CHR_TYP ne "DEBUG") { open(STDOUT,">&OLDSTDOUT"); }
				      print"\t   g03 \t\t\t\t\t\t\t\t[ OK ]\n";
				}
			}else{	if ($CHR_TYP ne "DEBUG") { open(STDOUT,">&OLDSTDOUT"); }
			      print"\t   g09 \t\t\t\t\t\t\t\t[ OK ]\n";
			}
		}
	}
	if(($MEPCHR_Calc eq "ON") || ($Re_Fit eq "ON")){				#--- RESP ---
		if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
		if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
		if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
		chomp($resp = `which resp`);
		if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
		if(($resp=~m/Command not found/ig) || ($resp =~ m/not in/ig) || ($resp =~ m/no resp in/ig) || ($resp =~ m/no resp.exe in/ig) || ($resp eq "")){
		     print"\t   resp \t\t\t\t\t\t[ NOT FOUND ]\n"; $verif=0;
		}else{ print"\t   resp \t\t\t\t\t\t\t[ OK ]\n"; }
	}
	if($verif==0){
		print "\n\n\t\tERROR: Some program(s) cannot be executed\n\n"; $check=0; Information();
		if($XRED eq "ON"){ print "\t\tPress Enter to exit.\n\n"; <STDIN>; } exit(0); 
	}
#--------------- GAMESS - Gaussian SCRATCH verification ------------
	$verif1=$verif11=$verif111=$verif2=$verif21=1;
	if($Re_Fit eq "OFF"){
	      if($QMSOFT eq "GAMESS"){
			if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
			if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
			if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
			if($OS =~ /CYGWIN/) {						#--- WinGAMESS is used ---
				system ('echo $GAMESSUS_SCRDIR > .scr');		# the scratch directory
				open(SCR,"<.scr");
				foreach(<SCR>){ $scrpath=$_; }
				close(SCR);
				system ("rm .scr");
				system ('echo $GAMESSUS_TMPDIR > .tmp');		# a temporary directory...
				open(TMP,"<.tmp");
				foreach(<TMP>){ $tmppath=$_; }
				close(TMP);
				chomp($scrpath); chomp($tmppath);
				system ("rm .tmp");
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }	
				if(($scrpath =~ m/Undefined variable/ig) || ($scrpath eq "")){
					print"\n\n\t   The Scratch directory for WinGAMESS/GAMESS is not defined!\n";
					print"\t   Define the \$GAMESSUS_SCRDIR variable in your SHELL.\n\n"; $verif11=0;
				}else{
					print"\n\n\t   The Scratch directory defined for WinGAMESS/GAMESS is \n\t\t $scrpath\n";
					if((!-e $scrpath) || ($scrpath ne "$pathwingamess/scratch")){
						print "\n\t   Scratch directory for WinGAMESS/GAMESS    \t\t[ NOT FOUND ]\n\n"; $verif11=0;
					}else{ print "\n\t   Scratch directory for WinGAMESS/GAMESS    \t\t\t[ OK ]\n\n"; }
				}
				if(($tmppath=~m/Undefined variable/ig) || ($tmppath eq "")){
					print"\n\n\t   The punch file directory for WinGAMESS/GAMESS is not defined!\n";
					print"\t   Define the \$GAMESSUS_TMPDIR variable in your SHELL.\n\n"; $verif21=0;
				}else{
					print"\n\n\t   The punch file directory defined for WinGAMESS/GAMESS is   \n\t\t $tmppath\n";
					if((!-e $tmppath) || ($tmppath ne "$pathwingamess/temp")){
						print "\n\t   Punch file directory for WinGAMESS/GAMESS    \t\t[ NOT FOUND ]\n\n"; $verif21=0;
					}else{ print "\n\t   Punch file directory for WinGAMESS/GAMESS    \t\t[ OK ]\n\n"; 
						$tmppath =~ s/\/$//;
					}
				}			
			}else {							#--- GAMESS-US compiled from sources is used ---
				if (-e "$pathgamessus/gms-files.csh") {         # New GAMESS installation procedure
					open (GMS_FILES,"< $pathgamessus/gms-files.csh");
					while (defined($line = <GMS_FILES>)){
						if ($line =~ /^setenv\s+PUNCH/){ ($punchfile) = (split (" ", $line))[2]; }
					}
					close(GMS_FILES);
				}
				else {
					open (SCR_FILE,"< $rungms");            # Former GAMESS installation procedure
						while (defined($line = <SCR_FILE>)){
							if ($line =~ /^setenv\s+PUNCH/){ ($punchfile) = (split (" ", $line))[2]; }
						}
					close(SCR_FILE);
				}
				open (SCR_FILE, "<$rungms");
				while (defined($line = <SCR_FILE>)){
					if ($line =~ /^set SCR=/){ ($scrpath) = (split (/=/, $line))[1]; }
					if ($line =~ /^set USERSCR=/){ ($scrpathuser) = (split (/=/, $line))[1]; } # New GAMESS installation procedure
				}
				close(SCR_FILE);
				chomp($scrpath); if (defined ($scrpathuser)) { chomp($scrpathuser); } chomp($punchfile);
				if ($CHR_TYP ne "DEBUG") { open(STDOUT,">&OLDSTDOUT"); }
				print"\n\t   The Scratch directory defined for GAMESS is $scrpath\n";
				if(!-e "$scrpath"){
					print "\n\t   Scratch directory for GAMESS    \t\t\t\t[ NOT FOUND ]\n\n"; $verif1=0;
				}else{
					if (!(-w $scrpath)) { print "\t   Bad permissions for the GAMESS Scratch directory \n\n"; $verif1=0; }
					else { print "\t   Scratch directory for GAMESS    \t\t\t\t[ OK ]\n\n"; }
				}
				if (defined ($scrpathuser)) { print"\t   The USER Scratch directory defined for GAMESS is $scrpathuser\n";
					if (!(-w $scrpathuser)) { print "\t   Bad permissions for the GAMESS Scratch directory \n\n"; $verif1=0; }
					else { print "\t   USER Scratch directory for GAMESS    \t\t\t[ OK ]\n\n"; }
				}
				print"\n\n\t   The punch file directory defined for GAMESS is $punchfile\n";
				if (-e "$pathgamessus/gms-files.csh") {
					if ($punchfile ne '$USERSCR/$JOB.dat') { $verif2=0; }
				}
				else {
					if ($punchfile ne '$SCR/$JOB.dat') { $verif2=0; }
				}
			}
		}elsif($QMSOFT eq "FIREFLY"){
			if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
			if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
			if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
			system ('echo $PCGAMESS_SCRDIR > .scr');
			open(SCR,"<.scr");
			foreach(<SCR>){ $scrpath=$_; }
			close(SCR);
			chomp ($scrpath);
			system ("rm .scr");
			if($CHR_TYP ne "DEBUG") { open(STDOUT,">&OLDSTDOUT"); }
			if(($scrpath =~ m/Undefined variable/ig)||($scrpath eq "")){
				print"\n\n\t   The Scratch directory for Firefly is not defined!\n";
				print"\t   Define the \$PCGAMESS_SCRDIR variable in your SHELL.\n\n"; $verif111=0;
			}else{
				print"\n\n\t   The Scratch directory defined for Firefly is $scrpath\n";
				if(!-e "$scrpath"){
					print "\n\t   Scratch directory for Firefly \t\t\t[ NOT FOUND ]\n\n"; $verif111=0;
				}else{
					if($OS !~ /CYGWIN/) {	# Do not check directory permissions under cygwin...
						if (!(-w $scrpath)) { print "\n\t   Bad permissions for the Firefly Scratch directory \n\n"; $verif111=0; }
						else { print "\n\t   Scratch directory for Firefly \t\t\t\t[ OK ]\n\n"; }
					} else{ print "\n\t   Scratch directory for Firefly \t\t\t\t[ OK ]\n\n"; }
				}
			}
	      }else{ 
			if($OS !~ /CYGWIN/) {
				if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
				if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
				system ('echo $GAUSS_SCRDIR > .scr');
				open(SCR,"<.scr");
				foreach(<SCR>){ $scrpath=$_; }
				close(SCR);
				chomp ($scrpath);
				system ("rm .scr");
				if ($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
				if(($scrpath =~ m/Undefined variable/ig)||($scrpath eq "")){
					print"\n\n\t   The Scratch directory for Gaussian is not defined!\n";
					print"\t   Define the \$GAUSS_SCRDIR variable in your SHELL.\n\n"; $verif1=0;
				}else {
					print"\n\n\t   The Scratch directory defined for Gaussian is $scrpath\n";
					if(!-e "$scrpath"){ 
						print "\n\t   Scratch directory for Gaussian \t\t\t\t[ NOT FOUND ]\n\n"; $verif1=0;
					}else {
						if (!(-w $scrpath)){ print "\n\t   Bad permissions for the Gaussian Scratch directory \n\n"; $verif1=0; }
						else{ print "\n\t   Scratch directory for Gaussian \t\t\t\t[ OK ]\n\n"; }
					}
				}
			}else { print "\n\t   The Scratch directory for Gaussian on CYGWIN is\n\t\tthe working directory.\n\n"; }
		}
		$scrpath =~ s/\/$//;
		if(($verif1==0) || ($verif11==0) || ($verif111==0) || ($verif2==0) || ($verif21==0)) {
			if($verif1==0){
				print "\n\t\tERROR: Problem with the QM Scratch directory."; 
				print "\n\t\tSee the R.E.D.-II manual, page 7.\n\n";
			}
			if($verif11==0){
				print "\n\t\tERROR: Problem with the QM Scratch directory"; 
				print "\n\t\tThe scratch directory has to be\n\t\t\t$pathwingamess/scratch.\n\n";
			}
			if($verif111==0){
				print "\n\t\tERROR: Problem with the QM Scratch directory.\n\n"; 
			}
			if($verif2==0){
				print "\n\t\tERROR: Problem with the punch file directory.";
				if (-e "$pathgamessus/gms-files.csh") {
					print "\n\t\tThe punch file directory has to be \$USERSCR/\$JOB.dat.";
				}
				else {
					print "\n\t\tThe punch file directory has to be \$SCR/\$JOB.dat."; 
					print "\n\t\tSee the R.E.D.-II manual, page 7.\n\n";
				}
			}
			if($verif21==0){
				print "\n\t\tERROR: Problem with the punch file directory";
				print "\n\t\tThe punch file directory has to be\n\t\t\t$pathwingamess/temp.\n\n";
			}
			$check=0; Information();
			if($XRED eq "ON"){ print "\t\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
		}
		if(($QMSOFT eq "GAMESS") || ($QMSOFT eq "GAUSSIAN") && ($OS !~ /CYGWIN/)){
			if(($QMSOFT eq "GAMESS") && ($OS =~ /CYGWIN/)){
				$tmppath =~ s/^\s*(.*?)\s*$/$1/;
				opendir(TMP,$tmppath);
				@filename = readdir(TMP);
				closedir(TMP);
			}else{
				$scrpath =~ s/^\s*(.*?)\s*$/$1/;
				opendir(SCR,$scrpath);
				@filename = readdir(SCR);
				closedir(SCR)
			}
			foreach(@filename){
				if($QMSOFT eq "GAMESS"){
					if((/dat/ig)||(/F05/ig)||(/irc/ig)){
						if ($OS !~ /CYGWIN/) { print "\n\t   ERROR: The Scratch directory is NOT empty\n\n"; }
						else { print "\n\t   ERROR: The punch file directory is NOT empty\n\n"; }
						$check=0; Information();
						if($XRED eq "ON"){ print "\t\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
					}
				}elsif($QMSOFT eq "GAUSSIAN") {
					if((/d2e/ig)||(/int/ig)||(/rwf/ig)||(/scr/ig)||(/inp/ig)){
						print "\n\t   ERROR: The Scratch directory is NOT empty\n\n";
						$check=0; Information();
						if($XRED eq "ON"){ print "\t\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
					}
				}
			}
		}
	}
}

#******************************RED-2012******************************
#-----GEOM-OPT-CONSTRAINT-------------
sub verif_constraint {
	my ($numero) = @_;
	my $nb_line = 0;
	foreach my $remark_geom (@remarks_geom) {
		if ( $remark_geom->[0] == $numero ) {
			$nb_line = $nb_line + 1;
			my @remarks_geom_right = ();
			my $string             = $remark_geom->[1];
			my @words              = split( /\s+/, $string );
			my $count_words        = scalar @words;
			for ( $i = 1 ; $i < $count_words ; $i++ ) {
				my $word = $words[$i];
				if ( $word =~ /^\d+$/ ) {
					if($word==0){
						print "\n\t\tERROR: Molecule $numero, GEOM-OPT-CONSTRAINT $nb_line: \n\tBad format for the constraint. 0 is not a number of atom!\n\n";
						$check = 0;
						Information();
						if ( $XRED eq "ON" ) { print "\t\tPress Enter to exit.\n\n"; <STDIN>; }
						exit(0);
					}elsif ( $word < $nbatoms[$numero] + 1) {
						push( @remarks_geom_right, $word );
					} else {
						if ( $i < $count_words - 1 ) {
							if ( $words[ $i + 1 ] =~ /^[-+]?\d+\.?\d*/ ) {
								my $max_nb_atom=$nbatoms[$numero] +1;
								print "\n\t\tERROR: Molecule $numero, GEOM-OPT-CONSTRAINT $nb_line: \n\tBad format for the constraint. The number of atom must be < $max_nb_atom!\n\n";
								$check = 0;
								Information();
								if ( $XRED eq "ON" ) { print "\t\tPress Enter to exit.\n\n"; <STDIN>; }
								exit(0);
							} else {
								push( @remarks_geom_right, $word );
								last;
							}
						} else {
							push( @remarks_geom_right, $word );
							last;
						}
					}
				} else {
					if ( $word =~ /^[-+]?\d+\.?\d*/ ) {
						if ( $i > 2 ) {
							push( @remarks_geom_right, $word );
							last;
						} else {
							last;
						}
					} else {
						last;
					}
				}
			}
			my $count_remarks_geom = scalar @remarks_geom_right;
			if ( $count_remarks_geom == 0 ) {
				print "\n\t\tERROR: Molecule $numero, GEOM-OPT-CONSTRAINT $nb_line: \n\tBad format for the constraint. No number of atom!\n\n";
				$check = 0;
				Information();
				if ( $XRED eq "ON" ) { print "\t\tPress Enter to exit.\n\n"; <STDIN>; }
				exit(0);
			} elsif ( $count_remarks_geom == 1 ) {
				print "\n\t                 X $remarks_geom_right[0] F";
				push( @remarks_geom_checked, [ $numero, \@remarks_geom_right ] );
			} elsif ( $count_remarks_geom == 2 ) {
				print "\n\t\tERROR: Molecule $numero, GEOM-OPT-CONSTRAINT $nb_line: \n\tBad format for the constraint. If this is a distance, provide a distance value!\n\n";
				$check = 0;
				Information();
				if ( $XRED eq "ON" ) { print "\t\tPress Enter to exit.\n\n"; <STDIN>; }
				exit(0);
			} elsif ( $count_remarks_geom == 3 ) {
				if($remarks_geom_right[0]==$remarks_geom_right[1]){
					print "\n\t\tERROR: Molecule $numero, GEOM-OPT-CONSTRAINT $nb_line: \n\tBad format for the constraint. Identical number of atom detected!\n\n";
					$check = 0;
					Information();
					if ( $XRED eq "ON" ) { print "\t\tPress Enter to exit.\n\n"; <STDIN>; }
					exit(0);
				}else{
					if ( $remarks_geom_right[2]>0&&($remarks_geom_right[2]<10||$remarks_geom_right[2]==10)) {
						my $string=$remarks_geom_right[2];
						$string=~s/\+//;
						print "\n\t                 B $remarks_geom_right[0] $remarks_geom_right[1] $string F";
						push( @remarks_geom_checked, [ $numero, \@remarks_geom_right ] );
					}else{
						print "\n\t\tERROR: Molecule $numero, GEOM-OPT-CONSTRAINT $nb_line: \n\tBad format for the constraint. A distance value is > 0 or < 11!\n\n";
						$check = 0;
						Information();
						if ( $XRED eq "ON" ) { print "\t\tPress Enter to exit.\n\n"; <STDIN>; }
						exit(0);
					}
				}
			} elsif ( $count_remarks_geom == 4 ) {
				my $meme=0;
				for (my $i=0;$i<3;$i++){
					for(my $j=0;$j<3;$j++){
						if($i!=$j){
							if($remarks_geom_right[$i]==$remarks_geom_right[$j]){
								$meme=1;
							}
						}
					}
				}
				if($meme==1){
					print "\n\t\tERROR: Molecule $numero, GEOM-OPT-CONSTRAINT $nb_line: \n\tBad format for the constraint. Identical numbers atom detected!\n\n";
					$check = 0;
					Information();
					if ( $XRED eq "ON" ) { print "\t\tPress Enter to exit.\n\n"; <STDIN>; }
					exit(0);
				}else{
					if ( $remarks_geom_right[3]>0&&($remarks_geom_right[3]<180||$remarks_geom_right[2]==180) ) {
						my $string=$remarks_geom_right[3];
						$string=~s/\+//;
						print "\n\t                 A $remarks_geom_right[0] $remarks_geom_right[1] $remarks_geom_right[2] $string F";
						push( @remarks_geom_checked, [ $numero, \@remarks_geom_right ] );
					} else {
						print "\n\t\tERROR: Molecule $numero, GEOM-OPT-CONSTRAINT $nb_line: \n\tBad format for the constraint. An angle value is > 0 or < 181!\n\n";
						$check = 0;
						Information();
						if ( $XRED eq "ON" ) { print "\t\tPress Enter to exit.\n\n"; <STDIN>; }
						exit(0);
					}
				}
			} elsif ( $count_remarks_geom == 5 ) {
				my $meme=0;
				for (my $i=0;$i<3;$i++){
					for(my $j=0;$j<3;$j++){
						if($i!=$j){
							if($remarks_geom_right[$i]==$remarks_geom_right[$j]){
								$meme=1;
							}
						}
					}
				}
				if($meme==1){
					print "\n\t\tERROR: Molecule $numero, GEOM-OPT-CONSTRAINT $nb_line: \n\tBad format for the constraint. Identical numbers atom detected!\n\n";
					$check = 0;
					Information();
					if ( $XRED eq "ON" ) { print "\t\tPress Enter to exit.\n\n"; <STDIN>; }
					exit(0);
				}else{
					my $string=$remarks_geom_right[4];
					$string=~s/\+//;
					print "\n\t                 D $remarks_geom_right[0] $remarks_geom_right[1] $remarks_geom_right[2] $remarks_geom_right[3] $string F";	
					push( @remarks_geom_checked, [ $numero, \@remarks_geom_right ] );
				}
			} else {
				print "\n\t\tERROR: Molecule $numero, GEOM-OPT-CONSTRAINT $nb_line: \n\t\tBad format for the constraint.\n\n";
				$check = 0;
				Information();
				if ( $XRED eq "ON" ) { print "\t\tPress Enter to exit.\n\n"; <STDIN>; }
				exit(0);
			}
		}
	}
}
#-----GEOM-OPT-CONSTRAINT-------------
#******************************RED-2012******************************

#-----------------------------------------------------------------------------------------------------
#------------------------ Read PDB: Extract information from the PDB file ----------------------------
#-----------------------------------------------------------------------------------------------------
sub Readpdb{
	%L4atoms = ('K'=>"19",'CA'=>"20",'SC'=>"21",'TI'=>"22",'V'=>"23",'CR'=>"24",'MN'=>"25",'FE'=>"26",'CO'=>"27",'NI'=>"28",'CU'=>"29",'ZN'=>"30",'GA'=>"31",'GE'=>"32",'AS'=>"33",'SE'=>"34",'BR'=>"35");			# 4th line of the periodic table
	%Tatoms = ('C'=>"6",'N'=>"7",'O'=>"8",'SI'=>"14",'P'=>"15",'S'=>"16");	# Atoms that can be written with a "T" 
	%Twoletterelt = ('LI'=>"LI",'BE'=>"BE",'NA'=>"NA",'MG'=>"MG",'AL'=>"AL",'SI'=>"SI",'CL'=>"CL",'CA'=>"CA",'SC'=>"SC",'TI'=>"TI",'CR'=>"CR",'MN'=>"MN",'FE'=>"FE",'CO'=>"CO",'NI'=>"NI",'CU'=>"CU",'ZN'=>"ZN",'GA'=>"GA",'GE'=>"GE",'AS'=>"AS",'SE'=>"SE",'BR'=>"BR");		# Elements which are composed of two letters
	$MOL_START =~ s/^\s*(.*?)\s*$/$1/;
	$_=$MOL_START;
	# if (!-e $MOL_START){
	# 	print "\n\tERROR: The initial P2N file is not in the working directory\n\n";
	# 	$check = 0; Information();
	# 	if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
	# }
	open (MOL_PDB, "<$MOL_START");
	$atomnb1=$nbconf[$NM]=0;
	foreach(<MOL_PDB>){		# Count the number of atoms in each conformation
		if( (/^ATOM/ig) || (/^HETATM/ig)){ $atomnb[$nbconf[$NM]][$NM]++; }
		# Atomnb1 is the number of atoms BEFORE the connections. Allows to check if "TER" has been misplaced
		if (/^CONECT/ig) { $atomnb1=$atomnb[0][$NM]; }
		if (/^TER/ig)	 { $nbconf[$NM]++; }
	}
	if($atomnb1==0){ $atomnb1=$atomnb[0][$NM]; }
	close(MOL_PDB);
	$nbconf[$NM]++;
	if($nbconf[$NM]>0){	   	# Compare the number of atoms in each conformation
		for ($i=0; $i<$nbconf[$NM]; $i++){
			if ((defined($atomnb[$i][$NM]) eq "") || ($atomnb1!=$atomnb[$i][$NM])){
				print "\n\tERROR: Each conformation must have the same number of atoms\n\tCheck for the presence or misplacement of the \"TER\" keyword\n\tSee the $MOL_START file\n\n";
				$check=0; Information();
				if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
			}
		}
	}
	open (MOL_PDB, "<$MOL_START");
	$nbconf[$NM]=$i=$testconf=$testconf2=$atombrut[$NM]=$atombrut2=0;
	foreach(<MOL_PDB>){
		if((/^ATOM/ig) || (/^HETATM/ig)){
			if(defined ($tab[0][$i][$NM]) eq ""){
				# CT1      MOL          1
				($type[$NM],$tab[4][$i][$NM],$tab[5][$i][$NM],$tab[10][$i][$NM])=(split(' '))[2,3,4,8]; 
				if(!(defined($tab[10][$i][$NM]))){ $tab[10][$i][$NM]=-1; } # If last column empty
				$tab[0][$i][$NM]=uc($type[$NM]);			# PDB atom name (ex: CT1)
				($type2[$NM],$ret)=($type[$NM]=~m/([a-zA-Z]+)/g);
				$tab[1][$i][$NM]=uc($type2[$NM]);			# Atom name without its number i.e. CT instead of CT1
				$tab[99][$i][$NM]=$tab[1][$i][$NM];  
				if($tab[99][$i][$NM]=~/T$/){ $tab[99][$i][$NM]=~s/T//; }	# Chemical symbol
				($numb2[$NM],$ret)=($type[$NM]=~m/([0-9]+)/g);  
				$tab[2][$i][$NM]=$numb2[$NM]; 				# Number of the PDB atom name i.e. 1 instead of CT1
				$tab[3][$i][$NM]=$Elements{uc($type2[$NM])};		# Atomic number Z
				if($tab[0][$i][$NM]!~/\d$/) { print "\n\tERROR: Missing Number in Atom name: $tab[0][$i][$NM] \n"; $testconf2=1; }
				if(($tab[0][$i][$NM]=~/^\d/) || ($tab[0][$i][$NM]=~/\W/) || (!exists $Elements{$tab[1][$i][$NM]})) {
					print "\n\tERROR: Invalid Atom name: $tab[0][$i][$NM] \n\t\t"; $testconf2=1; }
				$testlastcol=1;
				($testlastcol,$ret2)=($tab[10][$i][$NM] =~ m/[a-zA-Z]/g);
				($testlastcolbis,$ret2)=($tab[10][$i][$NM] =~m/\-?\d?\d?\d\.?\d?\d?\d?/g);
				if(defined($testlastcol) ne "") {			#Check if the last column contain atom names
					if($type2[$NM]=~/T$/ ){ $type2[$NM] =~ s/T//; }
					if(exists $Twoletterelt{uc($type2[$NM])}){
						($eltbrut,$ret2)=($tab[10][$i][$NM] =~ m/[a-zA-Z]+/g);
					}else{($eltbrut,$ret2)=($tab[10][$i][$NM] =~ m/[a-zA-Z]/g);}
					if (uc($type2[$NM]) eq uc($eltbrut)){ $atombrut[$NM]=1; #Check if the atoms names are the sames and display different messages for each possibility
					}elsif($type2[$NM] ne $eltbrut){
						print "\n\tERROR: Incompatible chemical elements: $type2[$NM] and $eltbrut\n"; $testconf2=1; }
				}elsif(defined($testlastcolbis) =~ /\d/){ $atombrut2=1; }
			}else{						# Check if the atoms names are the same in the other conformations
				$atomconf1=$tab[1][$i][$NM];
				if($atomconf1=~/T$/){ $atomconf1=~s/T//; }
				$tmpname=(split(' '))[2];
				($tmpname2,$ret)=($tmpname=~m/([a-zA-Z]+)/g);
				$atomconf2=uc($tmpname2);
				if($atomconf2=~/T$/) {$atomconf2=~s/T//; }
				if($atomconf1 ne $atomconf2){
					if($testconf==0){
						$nbconf[$NM]++;
						print "\n\tERROR: Invalid element in conformation $nbconf[$NM]:\n";
						$nbconf[$NM]--; $testconf=1; $testconf2=1;
					}
					print "\t\t\t$atomconf2 is $atomconf1 in first conformation\n";
				}
			} #		X	       Y         		Z
			($coord[0][$i][$nbconf[$NM]][$NM],$coord[1][$i][$nbconf[$NM]][$NM],$coord[2][$i][$nbconf[$NM]][$NM])=(split(' '))[5,6,7]; $i++;
		}
		if (/^TER/ig){ $nbconf[$NM]++; $i=0; $testconf=0; }
	}
	$nbconf[$NM]++;
	close(MOL_PDB);
	if($atombrut2==1){ $atombrut[$NM]=2; }
	$nbatoms[$NM]=$atomnb[0][$NM];
	$nbresi[$NM]=1; $residu[0][$NM]=1;		# Check if there are two different elements ending with a "T" and a same number
	for($i=0; $i<$nbatoms[$NM]; $i++){
	      if((defined($tab[5][$i+1][$NM])) && ($tab[5][$i][$NM] ne $tab[5][$i+1][$NM] )) { $nbresi[$NM]+=1; }
	      $residu[$i+1][$NM]=$nbresi[$NM];
	      for($j=0; $j<$i; $j++){
		      $atomname1=$tab[1][$i][$NM];	
		      if($atomname1=~/T$/) { $atomname1 =~ s/T//; }	# Name of the atom without the "T"
		      $atomname2=$tab[1][$j][$NM];
		      if($atomname2=~/T$/) { $atomname2 =~ s/T//; } 	# Name of the atom without the "T"
		      if((exists $Tatoms{$atomname1}) && (exists $Tatoms{$atomname2}) && ($tab[1][$i][$NM] ne $tab[1][$j][$NM])){
			      if(($tab[1][$i][$NM] =~ /T$/) && ($tab[1][$j][$NM] =~ /T$/)){
				      if($tab[2][$i][$NM]==$tab[2][$j][$NM]){
					      print "\n\tERROR: Redundant number in Atom name: $tab[0][$i][$NM] & $tab[0][$j][$NM]\n"; $testconf2=1;
				      }
			      }
		      }
	      }
	}
	$nbconect[$NM]=$reorient[$NM]=$nbrot[$NM]=$nbrot_rotate[$NM]=$nb_translate[$NM]=$n=0;
	open (MOL_PDB, "<$MOL_START"); 
	$ter=$imrcount[$NM]=$verifimr[$NM]=0; 	# Connection or re-orientation appearing after a "TER" will not be recorded
	foreach(<MOL_PDB>){
		if((/^CONECT/ig) && ($ter==0)){	# ter = 1 if the keyword "TER" has been seen
			s/[A-Z]//gi; $comp1=0;
			@tmp=(split(" "));
			foreach $arg (@tmp){
				if($comp1==0){ $comp1=$arg;
				}else{	$flagc1=$flagc2=0;
					for($i=0;$i<$nbconect[$NM];$i++){
						if($conections[$i][$NM] eq "$comp1-$arg") { $flagc1=1; }
					}
					for($i=0;$i<$nbconect[$NM];$i++){
						if($conections[$i][$NM] eq "$arg-$comp1") { $flagc2=1; }
					}
					if(($flagc1==0)&&($flagc2==0)){
						$conections[$nbconect[$NM]][$NM]="$comp1-$arg";
						$nbconect[$NM]++;
					}
				}
			}
		}
		if((/^REMARK REORIENT/ig) && ($ter==0)){
			s/[^\d\s|]//gi; # s/[A-Z]//gi;
			@rep = split("[|]"); # print $_ ;
			foreach (@rep){
				@rot2=(split(' '));
				$plan=$verif=0;
				foreach $arg (@rot2){
					$plan++;
					if($arg !~ /^\d+$/){
						print "\n\tERROR: Bad format in three atom based re-orientation!\n\n"; $check=0; Information();
						if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
					}
					if(($arg<1) || ($arg>$nbatoms[$NM])){ $verif=1; }
				}
				if(($plan!=3) && ($plan!=0)){ $verif=1; }
				$rot[$nbrot[$NM]][0][$NM]=$rot2[0];
				$rot[$nbrot[$NM]][1][$NM]=$rot2[1];
				$rot[$nbrot[$NM]][2][$NM]=$rot2[2];
				if((defined($rot2[0]) ne "") && (defined($rot2[1]) ne "") && (defined($rot2[2]) ne "")){
					if(($rot2[0]==$rot2[1]) || ($rot2[0]==$rot2[2]) || ($rot2[1]==$rot2[2])){ $verif=1; }
					else{ $nbrot[$NM]++; }
				}else{
					if((defined($rot2[0]) ne "") || (defined($rot2[1]) ne "") || (defined($rot2[2]) ne "")) { $verif=1; }
				}
				if($verif==1){ print "\n\tERROR: Bad format in three atom based re-orientation! \n"; $testconf2=1; }
			}
		}
		if((/^REMARK ROTATE/ig) && ($ter==0)){ # Elodie -April 2010 - Beginning
			s/[^\d\s|]//gi;
			@rep = split("[|]");
			foreach (@rep){
				@rot2=(split(' '));
				$plan=$verif=0;
				foreach $arg (@rot2){
					$plan++;
					if($arg !~ /^\d+$/){
						print "\n\tERROR: Bad format in three atom based rotation!\n\n"; $check=0; Information();
						if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
					}
					if(($arg<1) || ($arg>$nbatoms[$NM])){ $verif=1; }
				}
				if(($plan!=3) && ($plan!=0)){ $verif=1; }
				$rot_rotate[$nbrot_rotate[$NM]][0][$NM]=$rot2[0];
				$rot_rotate[$nbrot_rotate[$NM]][1][$NM]=$rot2[1];
				$rot_rotate[$nbrot_rotate[$NM]][2][$NM]=$rot2[2];
				if((defined($rot2[0]) ne "") && (defined($rot2[1]) ne "") && (defined($rot2[2]) ne "")){
					if(($rot2[0]==$rot2[1]) || ($rot2[0]==$rot2[2]) || ($rot2[1]==$rot2[2])){ $verif=1; }
					else{ $nbrot_rotate[$NM]++; }
				}else{
					if( (defined($rot2[0]) ne "") || (defined($rot2[1]) ne "") || (defined($rot2[2]) ne "")) { $verif=1; }
				}
				if($verif==1){ print "\n\tERROR: Bad format in three atom based rotation! \n"; $testconf2=1; }
			}
		}
		if((/^REMARK TRANSLATE/ig) && ($ter == 0)){
			s/[^-?\d+(?:\.\d+)?\s|]//gi; 
			@rep = split("[|]");
			foreach (@rep){
				@rot2=(split(' '));
				$plan=$verif=0;
				foreach $arg (@rot2){
					$plan++;
					if($arg !~ /^(?:\+|-)?\d+(?:\.\d+)?$/){
						print "\n\tERROR: Bad format in three integer based translation!\n\n"; $check=0; Information();
						if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
					}
				}
				if(($plan!=3) && ($plan!=0)){ $verif=1; }
				$trans[$nb_translate[$NM]][0][$NM]=$rot2[0];
				$trans[$nb_translate[$NM]][1][$NM]=$rot2[1];
				$trans[$nb_translate[$NM]][2][$NM]=$rot2[2];
				if((defined($rot2[0]) ne "") && (defined($rot2[1]) ne "") && (defined($rot2[2]) ne "")) { $nb_translate[$NM]++; 
				}else{
					if((defined($rot2[0]) ne "") || (defined($rot2[1]) ne "") || (defined($rot2[2]) ne "")) { $verif=1; }
				}
				if($verif == 1){ print "\n\tERROR: Bad format in three integer based translation! \n"; $testconf2=1; }
			}
		} # Elodie -April 2010 - End
		if((/^REMARK INTRA-MCC/ig) && ($ter==0)){
			$m=$verifimr[$NM]=0;
			($intramrval,$intramr[2][$n][$NM],$imrtype)=(split("[|]"))[0,1,2];
			$imrtype=~ s/\s*(\w).*/$1/gi;
			$intramrval=~ s/^REMARK INTRA-MCC\s*(.*?)\s*$/$1/gi;
			$intramr[1][$n][$NM]=$intramrval;
			if($intramrval !~ /^[\+\-]?(\d+(\.\d+)?|\.\d+)$/){ print "\n\tWrong charge value for the group of atoms\n"; $verifimr[$NM]=1; }
			
			#******************************RED-2012******************************
			my $mark_imrtype=$imrtype;
			chomp($mark_imrtype);
			$mark_imrtype=~ s/^\s+//;
			$mark_imrtype=~ s/\s+$//;
			my @intra_mcc=split(" ", $intramr[2][$n][$NM]);
			push(@GLOBAL_intra_mcc,[$NM,$intramrval,\@intra_mcc]);	
			#******************************RED-2012******************************
			
			($intramr[3][$n][$NM])=(uc($imrtype));
			if (defined($intramr[2][$n][$NM])=~/^\s*$/) { $verifimr[$NM]=1; }
			if (defined($intramr[2][$n][$NM])){
				foreach ($intramr[2][$n][$NM]){
					@nbimr2=(split (' '));
					$nbimr= (scalar @nbimr2);
					$intramr[4][$n][$NM]=$nbimr;
					for ($m=0; $m<$nbimr; $m++){
						($intratom[$m][$n][$NM])=(split(' '))[$m];
						if($intratom[$m][$n][$NM]!~ /^\d+$/) { print "\n\tAtom numbers must be integers\n"; $verifimr[$NM]=1; }
						if($verifimr[$NM] != 1){
							if(($intratom[$m][$n][$NM]>$nbatoms[$NM]) || ($intratom[$m][$n][$NM]==0)){ 
								print "\n\tThe atom numbers must be between 1 and $nbatoms[$NM]\n"; $verifimr[$NM]=1;
							}
						}
					}
					if( $nbimr>$nbatoms[$NM]){
						print "\n\tAtom numbers in intra-molecular charge constraint:\n\tThey cannot exceed the total number of atoms\n"; $verifimr[$NM]=1;
					}
				}
			}
			if($intramr[3][$n][$NM]=~/^\s*[KR]\s*$/i) {}
			else{
				print "\n\tBad flag in intra-molecular charge constraint:\n\tOnly \"K\" (for Keep) or \"R\" (for Remove) are allowed\n"; $verifimr[$NM]=1; }
			if($verifimr[$NM]==1){ print "\n\tERROR: Wrong intra-molecular charge constraint\n\t"; $testconf2=1; }
			if($verifimr[$NM]!=1){ $verifimr[$NM]=2; }
			$imrcount[$NM]++; $n++;
		}
		if  (/^TER/ig){ $ter=1; }
	}
	close(MOL_PDB);
	if($testconf2==1){
	      print "\n\tSee the $MOL_START file\n\n"; $check=0; Information();
	      if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; }	exit(0);
	}
	$TestL4a[$NM]=0;
	for ($i=0; $i<$nbatoms[$NM]; $i++){ 
		if (exists $L4atoms{$tab[1][$i][$NM]}){ $TestL4a[$NM]=1; last; }
	}
}
#----------------------------------------------------------------------------------------------------------
#------------------------------------Read inter molecular constraints and equivalencing---------------------
#----------------------------------------------------------------------------------------------------------
sub Read_imrs{
	$verifimrs2=$verifimeq2=$trodimrs=0; $nbref=999999999; $NM=$tyu=$tyu2=1;
	if(($dfmol != 1) && ($CHR_TYP ne "ESP-A2") && ($CHR_TYP ne "ESP-C2")){
		print "\n  =========================================================================== ";
		print "\n  = Checking inter-mol. charge constraint \& inter-mol. charge equivalencing = ";
		print "\n  =========================================================================== \n";
		
		#******************************RED-2012******************************
		@GLOBAL_inter_mcc=();
		@GLOBAL_inter_meqa=();
		#******************************RED-2012******************************
		
		for($NM=1; $NM<=$dfmol; $NM++){
			if(!defined($imrscount[$NM])){ $imrscount[$NM]=0; }
			$MOL_START="Mol_red$NM.p2n";
			open (MOL_PDB, "<$MOL_START");
			$v=$q=$ter=$verifimeq[$NM]=$verifimrs[$NM]=0;
			foreach(<MOL_PDB>){
				if((/^REMARK INTER-MCC/ig) && ($ter==0)){
					$verifimrs[$NM]=0;
					($interval,$intermr[2][$v][$NM],$intermr[3][$v][$NM],$intermr[4][$v][$NM])=(split("[|]"))[0,1,2,3];
					if(defined ($intermr[4][$v][$NM])){ $intermr[4][$v][$NM]=~s/[^\d\s]//gi;
					}else{ $verifimrs[$NM]=1; }
					$allright=0;
					if ((defined($intermr[2][$v][$NM])) && (defined($intermr[3][$v][$NM])) && (defined($intermr[4][$v][$NM]))) {
						if (($intermr[2][$v][$NM]!~ m/[0-9]/g) || ($intermr[3][$v][$NM]!~ m/[0-9]/g) || ($intermr[4][$v][$NM]!~ m/[0-9]/g) || ($intermr[2][$v][$NM]=~ /^\s*$/) || ($intermr[3][$v][$NM]=~/^\s*$/) || ($intermr[4][$v][$NM]=~/^\s*$/)){
							print "\n\t  Bad inter-molecular charge constraint:\n\t  Error in the list of molecules or atoms\n";
							$verifimrs[$NM]=1; $allright=-1;
						}
					}
					else {	print "\n\t  Bad format for at least one inter-molecular charge constraint\n";
						$verifimrs[$NM]=1; $allright=-1;
					}
					$interval=~s/^REMARK INTER-MCC\s*//gi;
					$interval=~s/\s*//gi;
					$intermr[1][$v][$NM]=$interval;
					if($interval !~ m/^[\+\-]?(\d+(\.\d+)?|\.\d+)$/){
						print "\n\t  Bad inter-molecular charge constraint:\n\t  Wrong constraint value for the group of atoms\n"; $verifimrs[$NM]=1;
					}
					
					#******************************RED-2012******************************
					my @inter_molcules = split( " ", $intermr[2][$v][$NM]);
					my @inter_atoms_1=split( " ", $intermr[3][$v][$NM]);
					my @inter_atoms_2=split( " ", $intermr[4][$v][$NM]);
					push(@inter_molcules,$interval);
					push(@inter_molcules,\@inter_atoms_1);
					push(@inter_molcules,\@inter_atoms_2);
					push(@GLOBAL_inter_mcc,\@inter_molcules);
					#******************************RED-2012******************************
					
					if($allright==0){
						foreach($intermr[2][$v][$NM]){
							@nbimrs2=(split (' '));
							$nbimrs1=(scalar @nbimrs2);
							if($nbimrs1!=2){
								print "\n\t  Bad inter-molecular charge constraint:\n\t  Wrong number of molecules (only 2 are allowed)\n"; $verifimrs[$NM]=1;
							}else {	($intertom1[0][$v][$NM])=(split(' '))[0];
								($intertom2[0][$v][$NM])=(split(' '))[1];
								$intertom1[0][$v][$NM]=~ s/^\s*(.*?)\s*$/$1/;
								$intertom2[0][$v][$NM]=~ s/^\s*(.*?)\s*$/$1/;
								if (($intertom1[0][$v][$NM]!~ /^\d+$/) || ($intertom2[0][$v][$NM]!~ /^\d+$/)) {
									print "\n\t  Bad inter-molecular charge constraint:\n\t  A molecule number must be an integer\n"; $verifimrs[$NM]=1;
								}
								else {
									if(($intertom1[0][$v][$NM]>$countmolimrs) || ($intertom1[0][$v][$NM]==0) || ($intertom2[0][$v][$NM]>$countmolimrs) || ($intertom2[0][$v][$NM]==0)) {
										print "\n\t  Bad inter-molecular charge constraint:\n\t  A molecule number must be between 1 and $countmolimrs\n"; $verifimrs[$NM]=1;
									}
									if(($intertom1[0][$v][$NM]==1)||($intertom2[0][$v][$NM]==1)){}
									else{
										print "\n\t  Bad inter-molecular charge constraint:\n\t  The molecule 1 must be involved \n"; $verifimrs[$NM]=1;
									}
									$imrsmol[0][$tyu]=$intertom1[0][$v][$NM]; 
									$imrsmol[1][$tyu]=$intertom2[0][$v][$NM]; 
									if(($tyu==2)&&($verifimrs2!=1)){
										if(($imrsmol[0][$tyu]!=$imrsmol[0][$tyu-1])||($imrsmol[1][$tyu]!=$imrsmol[1][$tyu-1])){
											print "\n\t  Bad inter-molecular charge constraint:\n\t  The same molecules must be used in each inter-mol. charge constraint\n"; 
											$verifimrs[$NM]=1;
										}
									}
								}
							}
						}
						foreach($intermr[3][$v][$NM]){
							@nbimrs18=(split (' '));
							$nbimrs15= (scalar @nbimrs18);
							$intermr[6][$v][$NM]=$nbimrs15;
							$imrstom[3][0][$tyu]=$intermr[6][$v][$NM];
							for ($m=1; $m<=$nbimrs15; $m++){
								($intertom1[$m][$v][$NM])=(split(' '))[$m-1];
								$imrstom[1][$m][$tyu]=$intertom1[$m][$v][$NM];
								if ($intertom1[$m][$v][$NM] !~ /^\d+$/) {
									print "\n\t  Bad inter-molecular charge constraint:\n\t  An atom number must be an integer \n"; $verifimrs[$NM]=1; 
								}
								if($verifimrs[$NM]!=1){
									if(($intertom1[$m][$v][$NM]>$nbatoms[$intertom1[0][$v][$NM]]) || ($intertom1[$m][$v][$NM]==0)) {
										print "\n\t  An atom number must be between 1 and $nbatoms[$intertom1[0][$v][$NM]] for the molecule $intertom1[0][$v][$NM]\n"; 
										$verifimrs[$NM]=1;
									}
								}
							}
							if($verifimrs[$NM]!=1){
								if($intermr[6][$v][$NM]>$nbatoms[$intertom1[0][$v][$NM]]){
									print "\n\t  Bad inter-molecular charge constraint:\n\t  The atom number cannot exceed the total number of atoms\n"; $verifimrs[$NM]=1;
								}
							}
						}
					}
					$f=0;
					if($verifimrs[$NM]!=1){
						for($b=0; $b<$nbatoms[$intertom1[0][$v][$NM]]+1; $b++){
							$testnon=0;
							for($x=1; $x<=$imrstom[3][0][$tyu]; $x++){
								if($b==$imrstom[1][$x][$tyu]){ $testnon=1; }
							}
							if($testnon!=1){ $nonimrs[1][$f][$tyu]=$b; $f++; }
						}
					}
					if ($allright==0) {
						foreach ($intermr[4][$v][$NM]){
							@nbimrs22=(split (' '));
							$nbimrs16= (scalar @nbimrs22);
							$intermr[7][$v][$NM]=$nbimrs16;
							$imrstom[4][0][$tyu]=$intermr[7][$v][$NM];
							for ($m=1; $m<=$nbimrs16; $m++){
								($intertom2[$m][$v][$NM])=(split(' '))[$m-1]; 
								$imrstom[2][$m][$tyu]=$intertom2[$m][$v][$NM];
								if($intertom2[$m][$v][$NM]!~/^\d+$/){
									print "\n\t  Bad inter-molecular charge constraint:\n\t  An atom number must be an integer \n"; $verifimrs[$NM]=1;
								}
								if($verifimrs[$NM]!=1){
									if(($intertom2[$m][$v][$NM]>$nbatoms[$intertom2[0][$v][$NM]]) || ($intertom2[$m][$v][$NM]==0)) {
										print "\n\t  Bad inter-molecular charge constraint:\n\t  An atom number must be between 1 and $nbatoms[$intertom2[0][$v][$NM]] for the molecule $intertom2[0][$v][$NM]\n";
										$verifimrs[$NM]=1;
									}
								}
							}
							if($verifimrs[$NM]!=1){
								if($intermr[7][$v][$NM]>$nbatoms[$intertom2[0][$v][$NM]]){
									print "\n\t  Bad inter-molecular charge constraint:\n\t  An atom number cannot exceed the total number of atoms\n"; $verifimrs[$NM]=1;
								}
							}
							if($verifimrs[$NM]!=1){
								if($intermr[7][$v][$NM]==$nbatoms[$intertom2[0][$v][$NM]]){ $flagp[$tyu]=2;
								}elsif($intermr[7][$v][$NM]==1){ $flagp[$tyu]=1; }
							}
						}
					}
					$f=0;
					if($verifimrs[$NM]!=1){
						for($b=0; $b<$nbatoms[$intertom2[0][$v][$NM]]; $b++){
							$testnon=0;
							for($x=1; $x<=$imrstom[4][0][$tyu]; $x++){
								if($b==$imrstom[2][$x][$tyu]){ $testnon=1; }
							}
							if($testnon!=1){ $nonimrs[2][$f][$tyu]=$b; $f++; }
						}
					}
					if($verifimrs[$NM]==1){ $verifimrs2=1; }
					if($verifimrs[$NM]!=1){ $verifimrs[$NM]=2; }
					$imrscount[$NM]++; $v++; $tyu++; $tyuaff=$tyu-1;
					if($tyu>3){ $trodimrs=1; }
				}
				if((/^REMARK INTER-MEQA/ig) && ($ter==0)){
					$m=$verifimeq[$NM]=0;
					($intermeqmol) = (split('INTER-MEQA'))[1];
					$intermeqmol=~ s/[^\d\s|]//gi;
					$_=$intermeqmol;
					($intermeq[0][$q][$NM],$intermeq[1][$q][$NM])=(split("[|]"))[0,1];
					
					#******************************RED-2012******************************					
					my @inter_molcules = split( " ", $intermeq[0][$q][$NM]);
					my @inter_atoms=split( " ", $intermeq[1][$q][$NM]);
					foreach my $inter_molcule (@inter_molcules){
						foreach my $inter_atom (@inter_atoms){
							push(@GLOBAL_inter_meqa,[$inter_molcule,$inter_atom]);	
						}
					}
					#******************************RED-2012******************************
					
					$allrights=0;
					if (!(defined($intermeq[1][$q][$NM])) || ($intermeq[1][$q][$NM]=~/^\s*$/)) { $allrights=-1; $verifimeq[$NM]=1; }
					foreach ($intermeq[0][$q][$NM]){
						@nbimrs28=(split (' '));
						$nbref=999999999;
						foreach $mol_temp (@nbimrs28) {
							if(!defined($nbatoms[$mol_temp])){ $nbatoms[$mol_temp]=0; }
							if ($nbatoms[$mol_temp]<$nbref) { $nbref=$nbatoms[$mol_temp]; }
						}
						$nbimrs19=(scalar @nbimrs28);
						$intermeq[2][$q][$NM]=$nbimrs19;
						if($intermeq[2][$q][$NM]<2){
							print "\n\t  Bad inter-molecular charge equivalencing: \n\t  A minimum of 2 molecules is required\n"; $verifimeq[$NM]=1; }
						for ($m=0; $m<$nbimrs19; $m++){
							($imeqtom1[$m][$q][$NM])=(split(' '))[$m]; 
							if ($imeqtom1[$m][$q][$NM]!~/^\d+$/) {
								print "\n\t  Bad inter-molecular charge equivalencing:\n\t  A molecule number must be an integer\n"; $verifimeq[$NM]=1;
							}
							if(($verifimeq[$NM]!=1) && ($tyu!=1)){
								if(($imeqtom1[$m][$q][$NM]>$countmolimrs) || ($imeqtom1[$m][$q][$NM]<2)) {
									print "\n\t  Bad inter-molecular charge equivalencing:\n\t  A molecule number must be between 2 and $countmolimrs\n"; $verifimeq[$NM]=1;
								}
							}
							if(($verifimeq[$NM]!=1) && ($tyu==1)){
								if(($imeqtom1[$m][$q][$NM]>$countmolimrs) || ($imeqtom1[$m][$q][$NM]==0)) {
									print "\n\t  Bad inter-molecular charge equivalencing:\n\t  A molecule number must be between 1 and $countmolimrs\n"; $verifimeq[$NM]=1;
								}
							}
							if($verifimeq[$NM]!=1){
								if($nbatoms[$imeqtom1[$m][$q][$NM]]<$nbref){ $nbref=$nbatoms[$imeqtom1[$m][$q][$NM]]; }
							}
						}
					}
					if($intermeq[2][$q][$NM]>$countmolimrs){
						print "\n\t  Bad inter-molecular charge equivalencing:\n\t  A molecule number cannot exceed the total number of molecules\n"; $verifimeq[$NM]=1;
					}
					if($allrights==0){
						foreach($intermeq[1][$q][$NM]){
							@nbimrs24=(split (' '));
							$nbimrs12=(scalar @nbimrs24);
							$intermeq[3][$q][$NM]=$nbimrs12;
							for($m=0; $m<$nbimrs12; $m++){
								($imeqtom2[$m][$q][$NM])=(split(' '))[$m];
								if($imeqtom2[$m][$q][$NM] !~ /^\d+$/){
									print "\n\t  Bad inter-molecular charge equivalencing:\n\t  An atom number must be an integer \n"; $verifimeq[$NM]=1;
								} 
								if($verifimeq[$NM]!=1){
									if(($imeqtom2[$m][$q][$NM]>$nbref) || ($imeqtom2[$m][$q][$NM]==0)) {
										print "\n\t  Bad inter-molecular charge equivalencing:\n\t  An atom number must be between 1 and $nbref\n"; $verifimeq[$NM]=1;
									}
								}
							}
							if($intermeq[3][$q][$NM]>$nbref){
								print "\n\t  Bad inter-molecular charge equivalencing:\n\t  The atom number cannot exceed the total number of atoms\n"; $verifimeq[$NM]=1;
							}
							for($g=0; $g<$intermeq[2][$q][$NM]-1; $g++){
								for($h=0; $h<$intermeq[3][$q][$NM]; $h++){
									if($verifimeq[$NM] != 1){
										if($tab[1][$imeqtom2[$h][$q][$NM]-1][$imeqtom1[$g][$q][$NM]] eq $tab[1][$imeqtom2[$h][$q][$NM]-1][$imeqtom1[$g+1][$q][$NM]]){}
										else{print "\n\t  Bad inter-molecular charge equivalencing:\n\t  $tab[1][$imeqtom2[$h][$q][$NM]-1][$imeqtom1[$g][$q][$NM]] and $tab[1][$imeqtom2[$h][$q][$NM]-1][$imeqtom1[$g+1][$q][$NM]] are incompatible\n"; $verifimeq[$NM]=1; }
									}
								}
							}
						}
					}
					if($verifimeq[$NM]==1){ $verifimeq2=1; }
					if($verifimeq[$NM]!=1){ $verifimeq[$NM]=2; }
					$imeqcount[$NM]++; $q++; $tyu2++;	
					if  (/^TER/ig){ $ter=1; }
				}
			}
			close(MOL_PDB);
		}
		if(($verifimrs2==1) || ($verifimeq2==1)){
			print "\n\t  ERROR: Wrong inter-molecular charge constraint or equivalencing\n\n"; $check=0; Information();
			if($XRED eq "ON"){ print "\t  Press Enter to exit.\n\n"; <STDIN>; } exit(0);
		}
		$t=0; $NM=1;
		for($NM=1; $NM<=$dfmol; $NM++){
			if($verifimrs[$NM]==2){
				if($t==0){ print "\n\t   * Selected inter-molecular charge constraint(s) *\n"; $t++; }
				$y=0;
				for($y=0; $y<$imrscount[$NM]; $y++){
					if($intermr[1][$y][$NM] =~ /\-/){
						printf("\t     %3.4f | %3s %3s | %3s | %3s", $intermr[1][$y][$NM],$intertom1[0][$y][$NM],$intertom2[0][$y][$NM],$intermr[3][$y][$NM],$intermr[4][$y][$NM]);
					}else{	printf("\t     %3.4f | %3s %3s | %3s | %3s", $intermr[1][$y][$NM],$intertom1[0][$y][$NM],$intertom2[0][$y][$NM],$intermr[3][$y][$NM],$intermr[4][$y][$NM]); }
				}
			}
		}
		$f=0;
		if($trodimrs==1){print "\n\t\t\t        WARNING:\n\t\t $tyuaff inter-molecular charge constraints detected!\n\t     The RESP derivation procedure will be carried out.\n   The Tripos file will NOT be generated since this procedure is unknown.\n";}
		for($NM=1; $NM<=$dfmol; $NM++){
			if($verifimeq[$NM]==2){
				if($f==0){
					print "\n\t\t\t        WARNING:\n\t    Atoms involved in inter-molecular charge equivalencing\n";
					print "\t      must be in the same order in each molecule!\n";
					print "\n\t       * Selected inter-molecular charge equivalencing *\n";
					$f++;
				}
				$y=0;
				for($y=0; $y<$imeqcount[$NM]; $y++){
					printf("\t  %3s | %3s ",$intermeq[0][$y][$NM],$intermeq[1][$y][$NM]); }
			}
		}
		if(($tyu==1) && ($tyu2!=1)) { print "\n\t       * No inter-molecular charge constraint detected *\n"; $t=1; }
		if(($tyu!=1) && ($tyu2==1)) { print "\n\t  * No inter-molecular charge equivalencing detected *\n"; $f=1; }
		if(($tyu==1) && ($tyu2==1)) { print "\n\t       * No inter-molecular charge constraint detected *\n\n\t     * No inter-molecular charge equivalencing detected * \n     Job(s) will be performed as a batch; each molecule being independent\n"; $t=1; $f=1; }
		if(($t==1) || ($f==1)){ print "\n  =========================================================================== \n"; }
	}
}
#----------------------------------------------------------------------------------------------------------
#-------------------------------------- SECTION FOR GEOMETRY OPTIMIZATION ---------------------------------
#----------------------------------------------------------------------------------------------------------
sub OPT_Calcul{
	if($OPT_Calc eq "ON"){
		$NM=1;
		for($NM=1; $NM<=$dfmol; $NM++){
			if($NM==1){ print "\n   Geometry optimization(s) is/are being computed for molecule $NM ..."; }
			else{ print "   Geometry optimization(s) is/are being computed for molecule $NM ..."; }
			for($NC=0; $NC<$nbconf[$NM]; $NC++){
				if($nbconf[$NM]>1){
					$NC++; print "\n\n\tConformation $NC ... \t\t\t\t"; $NC--;
				}
				if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
				if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
				for($i=0; $i<$nbatoms[$NM]; $i++){						# Preparation and conversion of input data
					$atom=$tab[1][$i][$NM];
					if($tab[1][$i][$NM]=~/T$/){ $atom=~s/T//; }				# If the atom's name ends with a "T", it needs to be removed
					$NC++;
					if(($QMSOFT eq "GAMESS") || ($QMSOFT eq "FIREFLY")){			#------ GAMESS ------
						$pdb2gam[0][$i][$NC][$NM]=$atom;
						$pdb2gam[1][$i][$NC][$NM]=$tab[3][$i][$NM];
						$pdb2gam[2][$i][$NC][$NM]=$coord[0][$i][$NC-1][$NM];
						$pdb2gam[3][$i][$NC][$NM]=$coord[1][$i][$NC-1][$NM];
						$pdb2gam[4][$i][$NC][$NM]=$coord[2][$i][$NC-1][$NM];
					}else{									#------ Gaussian ------
						$pdb2gau[0][$i][$NC][$NM]=$atom;
						$pdb2gau[1][$i][$NC][$NM]=$coord[0][$i][$NC-1][$NM];
						$pdb2gau[2][$i][$NC][$NM]=$coord[1][$i][$NC-1][$NM];
						$pdb2gau[3][$i][$NC][$NM]=$coord[2][$i][$NC-1][$NM];
					}
					$NC--;
				}
				$NC++;
				if(($QMSOFT eq "GAMESS") || ($QMSOFT eq "FIREFLY")){				#------ GAMESS ------
					$JOB="JOB1-gam_m$NM-$NC";
					open (JOB1_FILE, ">JOB1-gam_m$NM-$NC.inp");
					print JOB1_FILE "! Optimization - Input generated by R.E.D.-III.x\n!
 \$CONTRL  ICHARG=$CHR_VAL[$NM] MULT=$MLT_VAL[$NM] RUNTYP=OPTIMIZE\n          MAXIT=200 UNITS=ANGS MPLEVL=0 EXETYP=RUN\n";
					print JOB1_FILE "! INTTYP=HONDO QMTTOL=1.0E-08 ITOL=30 ICUT=20\n";
					if ($MLT_VAL[$NM]==1)	{ print JOB1_FILE "          SCFTYP=RHF \n"; }
					else        		{ print JOB1_FILE "          SCFTYP=UHF \n"; }
					if (($TestL4a[$NM]==1) && ($PCGVAR==0)) { print JOB1_FILE "          ISPHER=1 COORD=UNIQUE                        \$END\n"; }
					if (($TestL4a[$NM]==1) && ($PCGVAR==1)) { print JOB1_FILE "          D5=.T. COORD=UNIQUE                          \$END\n"; }
					else        		{ print JOB1_FILE "          COORD=UNIQUE                                 \$END\n"; }
					print JOB1_FILE " \$DFT     DFTTYP=NONE METHOD=GRID                      \$END\n";
					if ($PCGVAR==0)	{ print JOB1_FILE " \$SCF     DIRSCF=.T. CONV=1.0E-08 FDIFF=.F.            \$END\n"; }
					else			{ print JOB1_FILE " \$SCF     DIRSCF=.T. NCONV=8 FDIFF=.F.                 \$END\n"; }
					if ($PCGVAR==0)	{ print JOB1_FILE " \$SYSTEM  TIMLIM=50000 MWORDS=32 MEMDDI=0              \$END\n"; }
					else			{ print JOB1_FILE " \$SYSTEM  TIMLIM=50000 MWORDS=32                       \$END\n"; }
					if (($PCGVAR==1) && ($NP!=1))	{ print JOB1_FILE " \$P2P     P2P=.T. DLB=.T.                              \$END\n"; }
					if($CHR_TYP eq "DEBUG") 				{ 	print JOB1_FILE " \$BASIS   GBASIS=PM3                                   \$END\n"; }
					elsif(($CHR_TYP eq "ESP-A2")||($CHR_TYP eq "ESP-C2")) 	{ 	print JOB1_FILE " \$BASIS   GBASIS=STO NGAUSS=3                          \$END\n"; }
					else { 	print JOB1_FILE " \$BASIS   GBASIS=N31 NGAUSS=6 DIFFSP=.F. \n          NDFUNC=1 NPFUNC=0                            \$END\n"; }
					if($CHR_TYP eq "DEBUG") { 	print JOB1_FILE " \$STATPT  NSTEP=200 OPTTOL=5.0E-03                     \$END\n"; }
					else { 				print JOB1_FILE " \$STATPT  NSTEP=200 OPTTOL=1.0E-06 HESS=CALC IHREP=10  \$END\n"; }
					print JOB1_FILE " \$GUESS   GUESS=HUCKEL                                 \$END\n \$DATA\n $TITLE[$NM]\n C1\n";
format RESULTGAMESS=
@<<@##.#   @##.##### @##.##### @##.#####
$pdb2gam[0][$i][$NC][$NM],$pdb2gam[1][$i][$NC][$NM],$pdb2gam[2][$i][$NC][$NM],$pdb2gam[3][$i][$NC][$NM],$pdb2gam[4][$i][$NC][$NM]
.
					format_name JOB1_FILE "RESULTGAMESS";
					for($i=0; $i<$nbatoms[$NM]; $i++){ write JOB1_FILE; }
					print JOB1_FILE " \$END\n\n\n";
					close(JOB1_FILE);
					$currDir = `pwd`; chomp($currDir);
					if($CHR_TYP eq "DEBUG") { $NP2=$NP; $NP=1; }  						# Force to use a single cpu if PM3 is used.
					if(($PCGVAR==1) && ($OS eq "DARWIN")) {							# Firefly EXECUTION ON MAC OS/Darwin using Wine
						system ("$wine $firefly -osx -r -f -p -stdext -i $currDir/JOB1-gam_m$NM-$NC.inp -o $currDir/JOB1-gam_m$NM-$NC.log -t $scrpath/ -np $NP");
						if(-e "./PUNCH")   { system ("mv PUNCH JOB1-gam_m$NM-$NC.dat"); }
						if(-e "./input")   { system ("rm input"); }
						if(-e "./AOINTS")  { system ("rm AOINTS"); }
						if(-e "./DICTNRY") { system ("rm DICTNRY"); }
						# system ("rm -rf $scrpath/pcg.* $scrpath/* ");
					}
					elsif(($PCGVAR==1) && ($OS=~/CYGWIN/)){							# Firefly FOR WINDOWS EXECUTION UNDER CYGWIN
						$scrpathw = $scrpath; $scrpathw = `cygpath -w $scrpathw`; $scrpathw =~ s/\\/\\\\/g; chomp($scrpathw);
						$currDir = `cygpath -w $currDir`; $currDir =~ s/\\/\\\\/g; chomp($currDir);
						# system ("$firefly -r -f -p -stdext -i $currDir\\\\JOB1-gam_m$NM-$NC.inp -o $currDir\\\\JOB1-gam_m$NM-$NC.log -t $scrpathw\\\\ -np $NP ");
						# system ("$firefly -r -f -i $currDir\\\\JOB1-gam_m$NM-$NC.inp > JOB1-gam_m$NM-$NC.log -t $scrpathw\\\\ -np $NP ");
						system ("$firefly -r -f -i $currDir\\\\JOB1-gam_m$NM-$NC.inp -O $currDir\\\\JOB1-gam_m$NM-$NC.log -t $scrpathw\\\\ -np $NP ");
						if(-e "$scrpath/pcg.0/PUNCH")   { system ("mv $scrpath/pcg.0/PUNCH JOB1-gam_m$NM-$NC.dat"); }
						if(-e "./PUNCH")   { system ("mv PUNCH JOB1-gam_m$NM-$NC.dat"); }
						if(-e "./input")   { system ("rm input"); }
						if(-e "./AOINTS")  { system ("rm AOINTS"); }
						if(-e "./DICTNRY") { system ("rm DICTNRY"); }
					}
					elsif((($PCGVAR==1) && ($OS ne "DARWIN")) || (($PCGVAR==1) && ($OS!~/CYGWIN/))) {	# Firefly EXECUTION ON UNIX
						if(($NP==1) || ($MPIVAR==0)) {
							# After PC-GAMESS/Firefly v. 7.1.E, activate the following command:
							# system ("$firefly -r -f -p -stdext -i $currDir/JOB1-gam_m$NM-$NC.inp -o $currDir/JOB1-gam_m$NM-$NC.log -t $scrpath/ -ex $pathfirefly/");
							system ("$firefly -r -f -p -i $currDir/JOB1-gam_m$NM-$NC.inp -o $currDir/JOB1-gam_m$NM-$NC.log -t $scrpath/ -ex $pathfirefly/");
						}
						else{	# After PC-GAMESS/Firefly v. 7.1.E, activate the following command:
							# system ("mpirun -np $NP $firefly -r -f -p -stdext -i $currDir/JOB1-gam_m$NM-$NC.inp -o $currDir/JOB1-gam_m$NM-$NC.log -t $scrpath/ -ex $pathfirefly/");
							system ("mpirun -np $NP $firefly -r -f -p -i $currDir/JOB1-gam_m$NM-$NC.inp -o $currDir/JOB1-gam_m$NM-$NC.log -t $scrpath/ -ex $pathfirefly/");
						}
						if(-e "./PUNCH")   { system ("mv PUNCH JOB1-gam_m$NM-$NC.dat"); }
						if(-e "./input")   { system ("rm input"); }
						if(-e "./AOINTS")  { system ("rm AOINTS"); }
						if(-e "./DICTNRY") { system ("rm DICTNRY"); }
						# system ("rm -rf $scrpath/pcg.* $scrpath/* ");
					}
					elsif(($PCGVAR==0) && ($OS=~/CYGWIN/)){							# GAMESS EXECUTION ON CYGWIN
						system ("cp JOB1-gam_m$NM-$NC.inp $scrpath/JOB1-gam_m$NM-$NC.F05");
						system ("$csh -f $runscript JOB1-gam_m$NM-$NC $gx $NP $pathwingamess $hostname > $currDir/JOB1-gam_m$NM-$NC.log");
						system ("mv $tmppath/JOB1-gam_m$NM-$NC.dat .");
						if (-e "$tmppath/JOB1-gam_m$NM-$NC.irc") { system ("mv $tmppath/JOB1-gam_m$NM-$NC.irc ."); }			
					}else{ 											# GAMESS EXECUTION ON UNIX & DARWIN
						system ("$rungms JOB1-gam_m$NM-$NC $gx $NP > JOB1-gam_m$NM-$NC.log");
						if (defined ($scrpathuser)) {
							system ("mv $scrpathuser/JOB1-gam_m$NM-$NC.dat .");
							if (-e "$scrpathuser/JOB1-gam_m$NM-$NC.irc") { system ("mv $scrpathuser/JOB1-gam_m$NM-$NC.irc ."); }
						}
						else {
							system ("mv $scrpath/JOB1-gam_m$NM-$NC.dat .");
						}
						if (-e "$scrpath/JOB1-gam_m$NM-$NC.irc") { system ("mv $scrpath/JOB1-gam_m$NM-$NC.irc ."); }
					}			
					if($CHR_TYP eq "DEBUG") { $NP=$NP2; }
					$ok=$ok11=$ok12=$ok13=$ok14=0;
					open (LOGFILE1, "<JOB1-gam_m$NM-$NC.log");
					foreach (<LOGFILE1>){ 
						if(/TERMINATED NORMALLY/ig){ $ok=1; }
						elsif(/CHECK YOUR INPUT CHARGE AND MULTIPLICITY/ig){ $ok11=1; }
						elsif(/THERE ARE ATOMS LESS THAN/ig){ $ok12=1; }
						elsif((/ENERGY DID NOT CONVERGE/ig) || (/SCF DOES NOT CONVERGE/ig)) { $ok13=1; }
						if(/THE GEOMETRY SEARCH IS NOT CONVERGED/ig) { $ok14=1; }
					}
					close(LOGFILE1);
					if($ok == 1){
						$ok=0;
						open (LOGFILE1, "<JOB1-gam_m$NM-$NC.log");
						foreach (<LOGFILE1>){ if(/EQUILIBRIUM GEOMETRY LOCATED/ig){ $ok=1; }}
						close(LOGFILE1);
					}
				}else{										#------------ Gaussian ------------
					$JOB="JOB1-gau_m$NM-$NC";
					open (JOB1_FILE, ">JOB1-gau_m$NM-$NC.com");
					printf JOB1_FILE ("%%Chk=JOB1-gau_m$NM-$NC.chk \n");
					printf JOB1_FILE ("%%Mem=256MB \n");
					printf JOB1_FILE ("%%NProc=$NP \n\n");
					
					#******************************RED-2012******************************
					#-----GEOM-OPT-CONSTRAINT-------------
					my $opt_loose="Opt=(Loose)";
					my $opt_tight="Opt=(Tight)";
					if($remarks_geom_exist[$NM-1]==1){
						$opt_loose="Opt=(Loose,Modredundant)";
						$opt_tight="Opt=(Tight,Modredundant)";
					}
					#-----GEOM-OPT-CONSTRAINT-------------
					#******************************RED-2012******************************
					
					if($TestL4a[$NM] == 1) {
						if($CHR_TYP eq "DEBUG") { printf JOB1_FILE ("#P PM3 %s GFInput GFPrint SCF(Conver=8) Test \n\n",$opt_loose); }
						elsif(($CHR_TYP eq "ESP-A2")||($CHR_TYP eq "ESP-C2")) {	printf JOB1_FILE ("#P HF/STO-3G 5D %s GFInput GFPrint SCF(Conver=8) Test \n\n",$opt_tight); }
					#____#1 else { printf JOB1_FILE ("#P HF/6-31G** 5D %s GFInput GFPrint SCF(Conver=8) Test \n\n",$opt_tight); } # Modification for Duan et al. FF
						else { printf JOB1_FILE ("#P HF/6-31G*  5D %s GFInput GFPrint SCF(Conver=8) Test \n\n",$opt_tight); } ##__##1 
					}
					else {
						if($CHR_TYP eq "DEBUG") { printf JOB1_FILE ("#P PM3 %s GFInput GFPrint SCF(Conver=8) Test \n\n",$opt_loose); }
						elsif(($CHR_TYP eq "ESP-A2")||($CHR_TYP eq "ESP-A2")) {	printf JOB1_FILE ("#P HF/STO-3G %s GFInput GFPrint SCF(Conver=8) Test \n\n",$opt_tight); }
					#____#2 else { printf JOB1_FILE ("#P HF/6-31G** %s GFInput GFPrint SCF(Conver=8) Test \n\n",$opt_tight); } # Modification for Duan et al. FF
						else { printf JOB1_FILE ("#P HF/6-31G*  %s GFInput GFPrint SCF(Conver=8) Test \n\n",$opt_tight); } ##__##2 
					}
					printf JOB1_FILE (" Optimization - Input generated by R.E.D.-III.x %s \n\n%s %s \n", $TITLE[$NM],$CHR_VAL[$NM],$MLT_VAL[$NM]);
format RESULTGAUSSIAN=
@<<   @##.#####      @##.#####      @##.#####
$pdb2gau[0][$i][$NC][$NM],$pdb2gau[1][$i][$NC][$NM],$pdb2gau[2][$i][$NC][$NM],$pdb2gau[3][$i][$NC][$NM]
.
					format_name JOB1_FILE "RESULTGAUSSIAN";
					for($i=0;$i<$nbatoms[$NM];$i++){ write JOB1_FILE; }
					
					#******************************RED-2012******************************
					#-----GEOM-OPT-CONSTRAINT-------------
					printf JOB1_FILE "\n";
					foreach my $remark_geom(@remarks_geom_checked){
						if($remark_geom->[0]==$NM){					
							my @remarks_geom_right=@{$remark_geom->[1]};
							my $count_remarks_geom=scalar @remarks_geom_right;
							my $str="";
							if($count_remarks_geom==1){
								$str=$remarks_geom_right[0];
							}else{
								for(my $i=0;$i<$count_remarks_geom-1;$i++){
									$str=$str." ".$remarks_geom_right[$i];
								}
							}
							if($count_remarks_geom==1){
								printf JOB1_FILE (" X %s F",$str,);
								printf JOB1_FILE "\n";
							}elsif($count_remarks_geom==3){
								my $string=$remarks_geom_right[2];
								$string=~s/\+//;
								printf JOB1_FILE (" B%s %0.2f F",$str,$string);
								printf JOB1_FILE "\n";
							}elsif($count_remarks_geom==4){
								my $string=$remarks_geom_right[3];
								$string=~s/\+//;
								printf JOB1_FILE (" A%s %0.2f F",$str,$string);
								printf JOB1_FILE "\n";
							}elsif($count_remarks_geom==5){
								my $string=$remarks_geom_right[4];
								$string=~s/\+//;
								printf JOB1_FILE (" D%s %0.2f F",$str,$string);
								printf JOB1_FILE "\n";	
							}else{
									
							}								
						}
					}	
					#-----GEOM-OPT-CONSTRAINT-------------
					#******************************RED-2012******************************
					
					print JOB1_FILE " \n\n";
					close(JOB1_FILE);
					# system("$gauss < JOB1-gau_m$NM-$NC.com > JOB1-gau_m$NM-$NC.log"); 					# Gaussian EXECUTION ON UNIX
					system("$gauss JOB1-gau_m$NM-$NC.com");
					if(-e "JOB1-gau_m$NM-$NC.out"){ system("mv JOB1-gau_m$NM-$NC.out JOB1-gau_m$NM-$NC.log"); }		# Cygwin...

					$ok=$ok11=$ok12=$ok13=$ok14=$ok15=0;
					open (LOGFILE1, "<JOB1-gau_m$NM-$NC.log");
					foreach (<LOGFILE1>){ 
						if(/Normal termination of Gaussian/ig){ $ok=1; }
						elsif(/The combination of multiplicity/ig){ $ok11=1; }
						elsif((/Problem with the distance matrix/ig) || (/Error in internal coordinate system/ig)){ $ok12=1; }
						elsif((/The SCF is confused/ig) || (/Convergence failure/ig)) { $ok13=1; }
						elsif((/Optimization stopped/ig) || (/Number of steps exceeded/ig)) { $ok14=1; }
						elsif(/Error imposing constraints/ig) { $ok15=1; }
					}
					close(LOGFILE1);
					if($ok == 1){
						$ok=$ok2=0;
						open (LOGFILE1, "<JOB1-gau_m$NM-$NC.log");
						foreach (<LOGFILE1>){
							if(/Stationary point found/ig){ $ok2=1; }
							if(($ok2 == 1)&&(/Standard orientation/ig)){ $ok=1; }
						}
						close(LOGFILE1);
					}
				}
				if ($CHR_TYP ne "DEBUG") { open(STDOUT,">&OLDSTDOUT"); }
				if($ok == 1) {
					if($nbconf[$NM]==1) { print "\t[ OK ]\n\tSee the file(s) \"$JOB.log\""; }
					else{ print "\t\t[ OK ]\n\tSee the file(s) \"$JOB.log\""; }
				}else{
					if($nbconf[$NM]==1) {
						print "\t[ FAILED ]\n\tSee the file(s) \"$JOB.log\"\n\n";
						if($ok11==1) { print "\tCheck the total charge and spin multiplicity in your P2N file!\n\n"; }
						if($ok12==1) { print "\tBad input geometry: Check the input geometry in your P2N file!\n\n"; }
						if($ok13==1) { print "\tSCF convergence problem\nRe-run the job using a better input geometry\n\n"; }
						if($ok14==1) { print "\tGeometry optimization convergence problem\n\tRe-run the job using the best geometry obtained\n\n"; }
						if($ok15==1) { print "\tProblem with the constraint(s) defined\n\tRe-run the job using another constraint set up\n\n"; }
						$check=0; Information();
						if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
					}else{
						print "\t\t[ FAILED ]\n\tSee the file(s) \"$JOB.log\"\n\n";
						if($ok11==1) { print "\tCheck the total charge and spin multiplicity in your P2N file!\n\n"; }
						if($ok12==1) { print "\tBad input geometry: Check the input geometry in your P2N file!\n\n"; }
						if($ok13==1) { print "\tSCF convergence problem\nRe-run the job using a better input geometry\n\n"; }
						if($ok14==1) { print "\tGeometry optimization convergence problem\n\tRe-run the job using the best geometry obtained\n\n"; }
						if($ok15==1) { print "\tProblem with the constraint(s) defined\n\tRe-run the job using another constraint set up\n\n"; }
						$check=0; Information();
						if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
					}
				}
				$NC--;
			}
			print "\n\n";
			if(($QMSOFT eq "GAMESS") || ($QMSOFT eq "FIREFLY")){ open (LOGTOT, ">JOB1-gam_m$NM.log"); }
			else{	open (LOGTOT, ">JOB1-gau_m$NM.log"); }
			$/="";					# Instead of reading each file, we can read the whole file by changing that variable
			for ($NC=0; $NC<$nbconf[$NM]; $NC++){	# Copy all the different .log files into a single one
				$NC++;
				if(($QMSOFT eq "GAMESS") || ($QMSOFT eq "FIREFLY")){ open (LOGFILE1, "<JOB1-gam_m$NM-$NC.log"); }
				else{ open (LOGFILE1, "<JOB1-gau_m$NM-$NC.log"); }
				foreach $log (<LOGFILE1>){	# The entire Log file is written in that variable
					print LOGTOT "$log";
					close (LOGFILE1);
				}
				print LOGTOT "\n";
				$NC--;
			}
			close (LOGTOT);
			$/="\n";
		}
	}
}
#------------------------------------------------------------------------------------------------------------------
#----------------------------------------- LOG to PDB convertion --------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
sub Log2pdb{
	$NM=1;
	for($NM=1; $NM<=$dfmol; $NM++){
		if($dfmol!=1){
		      $JOB_OPT="Mol_red$NM.log";
		      $JOB_OPT =~ s/^\s*(.*?)\s*$/$1/;
		}
		if($atombrut[$NM]==1){
format RESULT1bis=
ATOM  @#### @<<< @<<< @###    @##.####@##.####@##.####
$flag3,$tab[10][$i-1][$NM],$tab[4][$i-1][$NM],$residu[$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM]
.
		}
		else{
format RESULT1=
ATOM  @#### @<<< @<<< @###    @##.####@##.####@##.####
$flag3,$atom,$tab[4][$i-1][$NM],$residu[$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM]
.
		}
		if(($MEPCHR_Calc eq "ON") || ($Re_Fit eq "ON")){
			for($NC=0; $NC<$nbconf[$NM]; $NC++){
				$flag1=$flag2=$i=0; $flag3=1; $nbc=-1;
				if(($OUTP[$NM] eq "GAMESS")||($OUTP[$NM] eq "FIREFLY")){				#------------ GAMESS ------------ 
					if($OPT_Calc eq "ON"){	open(JOB1,"<JOB1-gam_m$NM.log");
					}else{			open(JOB1,"<$JOB_OPT"); }
					foreach (<JOB1>){
						if(/EQUILIBRIUM GEOMETRY LOCATED/ig){ $flag1=1; $nbc++; }
						if(/TERMINATED NORMALLY/ig){ $flag2=1; }
						if(($flag1==1) && ($flag2==0) && ($nbc==$NC)){
							if(/^\s\w+\s+\d+\.\d+\s+(\-\d+|\d+)\.\d+\s+(\-\d+|\d+)\.\d+\s+(\-\d+|\d+)\.\d+/){
								($coord[0][$i][$NC][$NM],$coord[1][$i][$NC][$NM],$coord[2][$i][$NC][$NM])=(split(' '))[2,3,4];
								$i++;
							}
						}
						if(($flag1==1) && ($flag2==1)){ $flag1=$flag2=0; }
					}
					Reorient_Gam();		# Before writing the PDB file, the molecule is reoriented using the GAMESS algorithm
					if($atombrut[$NM] == 1){ format_name MOL_OPT1 "RESULT1bis"; }
					else{ format_name MOL_OPT1 "RESULT1"; }
					$NC++;
					if($Re_Fit eq "OFF") { open (MOL_OPT1, ">Mol_m$NM-o$NC-qmra.pdb"); }
					$NC--;
					if($Re_Fit eq "OFF") { printf MOL_OPT1 ("REMARK Mol. re-orientation as implemented in GAMESS/Firefly.\nREMARK Obtained Eigenvalues:\nREMARK Ixx: %8.3f\tIyy: %8.3f\tIzz: %8.3f\nREMARK\n", $eval[0], $eval[1], $eval[2]); }
					for($i=1; $i<=$nbatoms[$NM]; $i++){
						$atom=$tab[1][$i-1][$NM];		# If there is a "T" in the atom's name, it needs to be removed
						if(($tab[1][$i-1][$NM] =~ /T$/)){  $atom=~s/T//; }
						$atom="$atom"."$i";
						if($Re_Fit eq "OFF") { write MOL_OPT1; }
						$flag3++;
					}
					if($Re_Fit eq "OFF") { close(MOL_OPT1); }
				}else{						#------------ Gaussian ------------
					$NC++;		# The molecule is reoriented during the minimization; the PDB file can be written directly
					if($Re_Fit eq "OFF"){ open (MOL_OPT1, ">Mol_m$NM-o$NC-qmra.pdb"); }
					if($atombrut[$NM]==1){ format_name MOL_OPT1 "RESULT1bis"; }
					else{ format_name MOL_OPT1 "RESULT1"; }
					$flag0=0;
					if($OPT_Calc eq "ON"){	open(JOB1,"<JOB1-gau_m$NM.log");
					}else{			open(JOB1,"<$JOB_OPT"); }
					$NC--;
					foreach (<JOB1>){
						if(/Stationary point found/ig){ $flag0=1; $nbc++; }
						if((/Standard orientation/ig) && ($flag0==1) && ($nbc==$NC)){ $flag1=1; $flag0=0; }
						if(($flag1==1) && ($flag2<6)){ $flag2++; }
						if(($flag2==6) && ($flag3<=$nbatoms[$NM])){
							@tmp=(split(' '));
							$a=0; $tmp[$a]="";
							while ($tmp[$a] ne ""){ $a++; }
							$coord[0][$i][$NC][$NM]=$tmp[$a-3]; # The last 3 columns contain the Cart. coordinates
							$coord[1][$i][$NC][$NM]=$tmp[$a-2]; # (the number of columns depends on the version of gaussian)
							$coord[2][$i][$NC][$NM]=$tmp[$a-1];
							$atom=$tab[1][$i][$NM];
							if(($tab[1][$i][$NM]=~/T$/)){ $atom=~s/T//; }
							$i++; 
							$atom="$atom"."$i";
							if($Re_Fit eq "OFF"){ write MOL_OPT1; }
							$flag3++;
						}
					}
					close(JOB1);
					if($Re_Fit eq "OFF"){ close(MOL_OPT1); }
				}
			}
		}
	}
}
#------------------------------------------------------------------------------------------------------------------
#----------------------------------------- File generation for REDDB  ---------------------------------------------
#------------------------------------------------------------------------------------------------------------------
sub File4REDDB{
	$NM=1;
	for($NM=1; $NM<=$dfmol; $NM++){
		if($dfmol!=1){ $MOL_START="Mol_red$NM.p2n"; }
		$rereo=0;
		open (Mol_REDDB, ">File4REDDB_m$NM.pdb");
		printf Mol_REDDB ("REMARK\n");
		open (MOL_PDB2, "<$MOL_START");
		$ter=0;
		foreach(<MOL_PDB2>){
			if(((/^REMARK REORIENT/ig) && ($ter==0))||((/^REMARK ROTATE/ig) && ($ter==0))||((/^REMARK TRANSLATE/ig) && ($ter==0))){
				printf Mol_REDDB ("$_");
				$rereo=1;
			}
			if (/^TER/ig){ $ter=1; }
		}
		close (MOL_PDB2);
		if ($rereo==0){ printf Mol_REDDB ("REMARK QMRA\n"); }
		printf Mol_REDDB ("REMARK\n");
		for($NC=1; $NC<=$nbconf[$NM]; $NC++){
			if($NC!=1){printf Mol_REDDB ("TER\n");}
			open(File_qmra,"<Mol_m$NM-o$NC-qmra.pdb");
			print Mol_REDDB <File_qmra>;
			close(File_qmra);
		}
		print Mol_REDDB "END\n";
		close(Mol_REDDB);
	}
}
#------------------------------------------------------------------------------------------------------------------
#----------------------------------------- GAMESS Reorientation Algorithm -----------------------------------------
#------------------------------------------------------------------------------------------------------------------
sub Reorient_Gam{	# Inspired by GAMESS (inputc.src), PTRAJ (action.c) & http://mathworld.wolfram.com/JacobiMethod.html
	%Mass = ('H'=>"1.007825",'LI'=>"7.016",'BE'=>"9.01218",'B'=>"11.00931",'C'=>"12.0",'CT'=>"12.0",'N'=>"14.00307",'NT'=>"14.00307",'O'=>"15.99491",'OT'=>"15.99491",'F'=>"18.9984",'NA'=>"22.9898",'MG'=>"23.98504",'AL'=>"26.98153",'SI'=>"27.97693",'SIT'=>"27.97693",'P'=>"30.97376",'PT'=>"30.97376",'S'=>"31.97207",'ST'=>"31.97207",'CL'=>"34.96885",'K'=>"38.96371",'CA'=>"39.96259",'SC'=>"44.95592",'TI'=>"47.90",'V'=>"50.9440",'CR'=>"51.9405",'MN'=>"54.9381",'FE'=>"55.9349",'CO'=>"58.9332",'NI'=>"57.9353",'CU'=>"62.9298",'ZN'=>"63.9291",'GA'=>"68.9257",'GE'=>"73.9219",'AS'=>"74.9216",'SE'=>"79.9165",'BR'=>"78.9183"); # Mass of the atoms as defined in GAMESS
	$TotMass=$COM[0]=$COM[1]=$COM[2]=0.0;
	for($i=0; $i<$nbatoms[$NM]; $i++){   					# Center of mass calculation
		$tab[6][$i][$NM]=$coord[0][$i][$NC][$NM];
		$tab[7][$i][$NM]=$coord[1][$i][$NC][$NM];
		$tab[8][$i][$NM]=$coord[2][$i][$NC][$NM];
		$COM[0]+=$tab[6][$i][$NM]*$Mass{$tab[1][$i][$NM]};
		$COM[1]+=$tab[7][$i][$NM]*$Mass{$tab[1][$i][$NM]};
		$COM[2]+=$tab[8][$i][$NM]*$Mass{$tab[1][$i][$NM]};
		$TotMass+=$Mass{$tab[1][$i][$NM]};
	}
	$COM[0]=$COM[0]/$TotMass; # X						# Center of mass coordinates
	$COM[1]=$COM[1]/$TotMass; # Y
	$COM[2]=$COM[2]/$TotMass; # Z
	for($i=0; $i<3; $i++){
	      for ($j=0; $j<3; $j++){ $inertia[$i][$j]=0; }
	}
	for($i=0; $i<$nbatoms[$NM]; $i++){
		$tab[6][$i][$NM]=$tab[6][$i][$NM]-$COM[0]; #X
		$tab[7][$i][$NM]=$tab[7][$i][$NM]-$COM[1]; #Y
		$tab[8][$i][$NM]=$tab[8][$i][$NM]-$COM[2]; #Z
		$inertia[0][0]+=$Mass{$tab[1][$i][$NM]}*($tab[7][$i][$NM]*$tab[7][$i][$NM]+$tab[8][$i][$NM]*$tab[8][$i][$NM]); #$Ixx Moment of inertia tensor
		$inertia[1][1]+=$Mass{$tab[1][$i][$NM]}*($tab[6][$i][$NM]*$tab[6][$i][$NM]+$tab[8][$i][$NM]*$tab[8][$i][$NM]); #$Iyy
		$inertia[2][2]+=$Mass{$tab[1][$i][$NM]}*($tab[6][$i][$NM]*$tab[6][$i][$NM]+$tab[7][$i][$NM]*$tab[7][$i][$NM]); #$Izz
		$inertia[0][1]-=$Mass{$tab[1][$i][$NM]}*$tab[6][$i][$NM]*$tab[7][$i][$NM]; #$Ixy
		$inertia[0][2]-=$Mass{$tab[1][$i][$NM]}*$tab[6][$i][$NM]*$tab[8][$i][$NM]; #$Ixz
		$inertia[1][2]-=$Mass{$tab[1][$i][$NM]}*$tab[7][$i][$NM]*$tab[8][$i][$NM]; #$Iyz
	}
	for($ip=1; $ip<=3; $ip++){						# Diagonalization of the inertia tensor (jacobi)
		for($iq=1; $iq<=3; $iq++){ $evect[$ip-1][$iq-1]=0.0; }
		$evect[$ip-1][$ip-1]=1.0;
	}
	for($ip=1; $ip<=3; $ip++){ $b[$ip-1]=$eval[$ip-1]=$inertia[$ip-1][$ip-1]; $z[$ip-1]=0.0; }
	$nrot=$i=0; $sm=1.0;
	while (($sm!=0.0) && ($i<50)){
		$i++; $sm=0.0;
		for($ip=1; $ip<3; $ip++){
			for ($iq=$ip+1; $iq<=3; $iq++){ $sm+=abs($inertia[$ip-1][$iq-1]); }
		}
		if ($i<4){ $thresh=0.2*$sm/9;
		}else{ $thresh=0.0; }
		for($ip=1;$ip<3;$ip++){
			for ($iq=$ip+1; $iq<=3; $iq++){
				$g=100.0*abs($inertia[$ip-1][$iq-1]);
				if(($i>4) && ((abs($eval[$ip-1])+$g) == abs($eval[$ip-1])) && ((abs($eval[$iq-1])+$g) == abs($eval[$iq-1]))){
					$inertia[$ip-1][$iq-1]=0.0;
				}elsif(abs($inertia[$ip-1][$iq-1])>$thresh){
					$h=$eval[$iq-1]-$eval[$ip-1];
					if((abs($h)+$g) == abs($h)){ $t=($inertia[$ip-1][$iq-1])/$h;
					}else{
						$theta=0.5*$h/($inertia[$ip-1][$iq-1]);
						$t=1.0/(abs($theta)+sqrt(1.0+$theta*$theta));
						if ($theta<0.0){ $t=-$t; }
					}
					$c=1.0/sqrt(1+$t*$t);
					$s=$t*$c;
					$tau=$s/(1.0+$c);
					$h=$t*$inertia[$ip-1][$iq-1];
					$z[$ip-1]-=$h;
					$z[$iq-1]+=$h;
					$eval[$ip-1]-=$h;
					$eval[$iq-1]+=$h;
					$inertia[$ip-1][$iq-1]=0.0;
					for($j=1;$j<=$ip-1;$j++){
						$g=$inertia[$j-1][$ip-1];
						$h=$inertia[$j-1][$iq-1];
						$inertia[$j-1][$ip-1]=$g-$s*($h+$g*$tau);
						$inertia[$j-1][$iq-1]=$h+$s*($g-$h*$tau); }
					for($j=$ip+1;$j<=$iq-1;$j++){
						$g=$inertia[$ip-1][$j-1];
						$h=$inertia[$j-1][$iq-1];
						$inertia[$ip-1][$j-1]=$g-$s*($h+$g*$tau);
						$inertia[$j-1][$iq-1]=$h+$s*($g-$h*$tau); }
					for($j=$iq+1;$j<=3;$j++){
						$g=$inertia[$ip-1][$j-1];
						$h=$inertia[$iq-1][$j-1];
						$inertia[$ip-1][$j-1]=$g-$s*($h+$g*$tau);
						$inertia[$iq-1][$j-1]=$h+$s*($g-$h*$tau); }
					for($j=1;$j<=3;$j++){
						$g=$evect[$j-1][$ip-1];
						$h=$evect[$j-1][$iq-1];
						$evect[$j-1][$ip-1]=$g-$s*($h+$g*$tau);
						$evect[$j-1][$iq-1]=$h+$s*($g-$h*$tau); }
					$nrot++;
				}
			}
		}
		for ($ip=1; $ip<=3; $ip++){
			$b[$ip-1]+=$z[$ip-1];
			$eval[$ip-1]=$b[$ip-1];
			$z[$ip-1]=0.0;
		}
	}									# End of diagonalization swaping of the eigenvectors
	for($k1=0; $k1<3; $k1++){
		$jj=$k1;
		for ($k2=$k1; $k2<3; $k2++){
			if ($eval[$k2]<$eval[$jj]){ $jj=$k2; }
		}
		if($jj!=$k2){
			$t=$eval[$jj];
			$eval[$jj]=$eval[$k1];
			$eval[$k1]=$t;
			for ($k2=0;$k2<3;$k2++){
				$t=$evect[$k2][$jj];
				$evect[$k2][$jj]=$evect[$k2][$k1];
				$evect[$k2][$k1]=$t;
			}
		}
	}
	$coef1=$evect[1][1]*$evect[2][2]-$evect[1][2]*$evect[2][1];
	$coef2=$evect[1][0]*$evect[2][2]-$evect[1][2]*$evect[2][0];
	$coef3=$evect[1][0]*$evect[2][1]-$evect[1][1]*$evect[2][0];
	# if(!defined($evect[0][0])){ $evect[0][0]=0; }
	# if(!defined($evect[0][1])){ $evect[0][1]=0; }
	if(!defined($evect[0][3])){ $evect[0][3]=0; }    # March 2009 !!!
	$Det=$evect[0][0]*$coef1-$evect[0][1]*$coef2+$evect[0][3]*$coef3;
	if($Det<0){
		$evect[0][0]=-$evect[0][0];
		$evect[1][0]=-$evect[1][0];
		$evect[2][0]=-$evect[2][0];
	}
	for($i=0; $i<$nbatoms[$NM]; $i++){					# New coordinates
		$coord[0][$i][$NC][$NM]=$evect[0][0]*$tab[6][$i][$NM]+$evect[1][0]*$tab[7][$i][$NM]+$evect[2][0]*$tab[8][$i][$NM];
		$coord[1][$i][$NC][$NM]=$evect[0][1]*$tab[6][$i][$NM]+$evect[1][1]*$tab[7][$i][$NM]+$evect[2][1]*$tab[8][$i][$NM];
		$coord[2][$i][$NC][$NM]=$evect[0][2]*$tab[6][$i][$NM]+$evect[1][2]*$tab[7][$i][$NM]+$evect[2][2]*$tab[8][$i][$NM];
		$tab[6][$i][$NM]=$coord[0][$i][$NC][$NM];
		$tab[7][$i][$NM]=$coord[1][$i][$NC][$NM];
		$tab[8][$i][$NM]=$coord[2][$i][$NC][$NM];
	}
}
#------------------------------------------------------------------------------------------------------------------
#------------------------------------- Rigid-body reorientation ---------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
sub translation{ # Elodie - April 2010 - Beginning
	my ($xt, $yt, $zt, $sens, $inf, $sup) = @_;	
	if($sens==0){
		for($i=$inf; $i<$sup; $i++){
			$tab2[0][$i][$NM]=$tab2[0][$i][$NM]-$xt;	# X
			$tab2[1][$i][$NM]=$tab2[1][$i][$NM]-$yt;	# Y
			$tab2[2][$i][$NM]=$tab2[2][$i][$NM]-$zt;	# Z
		}
	}
	elsif($sens==1){
		for($i=$inf; $i<$sup; $i++){
			$tab2[0][$i][$NM]=$tab2[0][$i][$NM]+$xt;	# X
			$tab2[1][$i][$NM]=$tab2[1][$i][$NM]+$yt;	# Y
			$tab2[2][$i][$NM]=$tab2[2][$i][$NM]+$zt;	# Z
		}
	}
}
sub rotation_X{
	my ($x, $y, $z, $inf, $sup) = @_;
	if(($y==0) && ($z==0)){ $y=0.0000001; }
	$hyp=sqrt(($y)**2+($z)**2);	
	$adj=abs($y);
	$angle=acos($adj/$hyp);
	if($z>=0){  		  				# Z positive
		if($y>=0){ $angle=$angle; }		        # Y positive
		else{$angle=PI-$angle; }			# Y negative
	}else{  		 	  			# Z negative
		if($y >= 0){ $angle=2*PI-$angle; }		# Y positive
		else{ $angle=PI+$angle;} 	  		# Y negative
	} 	#--- Rotation  X Axis --> XY plane
	for($i=$inf;$i<$sup;$i++){
		$tz=$tab2[2][$i][$NM];
		$ty=$tab2[1][$i][$NM];
		$COS=cos($angle);
		$SIN=sin($angle);
		$tab2[1][$i][$NM] = $tz*$SIN+$ty*$COS;
		$tab2[2][$i][$NM] = $tz*$COS-$ty*$SIN;
	} 
}
sub rotation_Z{
	my ($x, $y, $z, $inf, $sup) = @_;
	if(($x==0) && ($y==0)){ $y=0.0000001; }
	$hyp=sqrt(($x)**2+($y)**2 );
	$adj=abs($x);
	$angle=acos($adj/$hyp);
	if($x >= 0){  		  				# X positive
		if($y >= 0){ $angle=$angle; }		        # Y positive
		else{ $angle=2*PI-$angle; }			# Y negative
	}else{  		 	  			# X negative
		if($y >= 0){ $angle=PI-$angle; }		# Y positive
		else{ $angle=PI+$angle; } 	  		# Y negative
	} 	#--- Rotation  Z Axis --> XZ plane
	for($i=$inf;$i<$sup;$i++){
		$tx=$tab2[0][$i][$NM];
		$ty=$tab2[1][$i][$NM];
		$COS=cos($angle);
		$SIN=sin($angle);
		$tab2[0][$i][$NM]=$tx*$COS+$ty*$SIN;
		$tab2[1][$i][$NM]=$ty*$COS-$tx*$SIN;
	} 
}
sub verif_align{
	my ($atom1, $atom2, $atom3) = @_;
	$d12[0]= sqrt(($coord[0][$atom1][$NC][$NM]-$coord[0][$atom2][$NC][$NM])**2 + ($coord[1][$atom1][$NC][$NM]-$coord[1][$atom2][$NC][$NM])**2 + ($coord[2][$atom1][$NC][$NM]-$coord[2][$atom2][$NC][$NM])**2); 
	$d23[0]= sqrt(($coord[0][$atom2][$NC][$NM]-$coord[0][$atom3][$NC][$NM])**2 + ($coord[1][$atom2][$NC][$NM]-$coord[1][$atom3][$NC][$NM])**2 + ($coord[2][$atom2][$NC][$NM]-$coord[2][$atom3][$NC][$NM])**2); 
	$d13[0]= sqrt(($coord[0][$atom1][$NC][$NM]-$coord[0][$atom3][$NC][$NM])**2 + ($coord[1][$atom1][$NC][$NM]-$coord[1][$atom3][$NC][$NM])**2 + ($coord[2][$atom1][$NC][$NM]-$coord[2][$atom3][$NC][$NM])**2); 
	$x[0]=int(rad2deg(acos(($d12[0]**2 + $d23[0]**2 - $d13[0]**2)/(2 * $d12[0] * $d23[0]))));
	if($d12[0]==0) { $d12[0]=0.000001; }
	if($d23[0]==0) { $d23[0]=0.000001; }
	if($d13[0]==0) { $d13[0]=0.000001; }
	$threshold=5;
	if (($x[0]>(0-$threshold) && $x[0]<(0+$threshold)) || ($x[0]>(180-$threshold) && $x[0]<(180+$threshold))) { $res=0; }
	else { $res=1; }
	return $res;
}
sub Reorientation_rbra{ 
	for($i=0;$i<$nbatoms[$NM];$i++){
		$tab2[0][$i][$NM]=$coord[0][$i][$NC][$NM];	# X
		$tab2[1][$i][$NM]=$coord[1][$i][$NC][$NM];	# Y
		$tab2[2][$i][$NM]=$coord[2][$i][$NC][$NM];	# Z
	}
	$atom1=$rot[$h][0][$NM]; 
	$atom2=$rot[$h][1][$NM]; 
	$atom3=$rot[$h][2][$NM];
	$atom1--; $atom2--; $atom3--; 
	$res=verif_align($atom1,$atom2,$atom3);
	if($res==0){
		if ($CHR_TYP ne "DEBUG") { open(STDOUT,">&OLDSTDOUT"); }
		$atom1++;$atom2++;$atom3++;
		printf ("\n   WARNING: In REMARK REORIENT, atoms %d %d %d are aligned",$atom1,$atom2,$atom3);
		$atom1--; $atom2--; $atom3--; 
	}
	$xt=$coord[0][$atom1][$NC][$NM];
	$yt=$coord[1][$atom1][$NC][$NM];
	$zt=$coord[2][$atom1][$NC][$NM];
	translation($xt,$yt,$zt,0,0,$nbatoms[$NM]);
	$x=$tab2[0][$atom2][$NM];
	$y=$tab2[1][$atom2][$NM];
	$z=$tab2[2][$atom2][$NM];
	rotation_X($x,$y,$z,0,$nbatoms[$NM]);	
	$x=$tab2[0][$atom2][$NM];
	$y=$tab2[1][$atom2][$NM];
	$z=$tab2[2][$atom2][$NM];
	rotation_Z($x,$y,$z,0,$nbatoms[$NM]);
	$x=$tab2[0][$atom3][$NM];
	$y=$tab2[1][$atom3][$NM];
	$z=$tab2[2][$atom3][$NM];
	rotation_X($x,$y,$z,0,$nbatoms[$NM]);
	if($atombrut[$NM] == 1){format_name MOL_OUTN "RESULTbis";}
	else{format_name MOL_OUTN "RESULT";}
	$h++; $NC++;
	open (MOL_OUTN, ">Mol_m$NM-o$NC-rbra$h.pdb");
	$h--; $NC--;
	for($i=0;$i<$nbatoms[$NM];$i++){
		$atom=$tab[1][$i][$NM];
		if(($tab[1][$i][$NM]=~/T$/)){ $atom=~s/T//; }
		$i++;
		$atom="$atom"."$i";
		$i--;
		write MOL_OUTN;
	}	
	close(MOL_OUTN);
}
sub Reorientation_rbra_rot(){
	for($i=0; $i<$nbatoms[$NM]; $i++){
		$tab2[0][$i][$NM]=$coord[0][$i][$NC][$NM];	# X
		$tab2[1][$i][$NM]=$coord[1][$i][$NC][$NM];	# Y
		$tab2[2][$i][$NM]=$coord[2][$i][$NC][$NM];	# Z
	}
	$atom1=$rot_rotate[$h][0][$NM]; 
	$atom2=$rot_rotate[$h][1][$NM]; 
	$atom3=$rot_rotate[$h][2][$NM];
	$atom1--; $atom2--; $atom3--; 
	$res=verif_align($atom1,$atom2,$atom3);
	if($res==0){
		if ($CHR_TYP ne "DEBUG") { open(STDOUT,">&OLDSTDOUT"); }
		$atom1++; $atom2++; $atom3++;
		printf ("\n   WARNING: In REMARK ROTATE, atoms %d %d %d are aligned",$atom1,$atom2,$atom3);
		$atom1--; $atom2--; $atom3--;
	}
	$xt=$coord[0][$atom1][$NC][$NM]; 
	$yt=$coord[1][$atom1][$NC][$NM]; 
	$zt=$coord[2][$atom1][$NC][$NM];
	translation($xt,$yt,$zt,0,0,$nbatoms[$NM]);
	$x=$tab2[0][$atom2][$NM];
	$y=$tab2[1][$atom2][$NM];
	$z=$tab2[2][$atom2][$NM];
	rotation_X($x,$y,$z,0,$nbatoms[$NM]);	
	$x=$tab2[0][$atom2][$NM];
	$y=$tab2[1][$atom2][$NM];
	$z=$tab2[2][$atom2][$NM];
	rotation_Z($x,$y,$z,0,$nbatoms[$NM]);
	$x=$tab2[0][$atom3][$NM];
	$y=$tab2[1][$atom3][$NM];
	$z=$tab2[2][$atom3][$NM];
	rotation_X($x,$y,$z,0,$nbatoms[$NM]);
	translation($xt,$yt,$zt,1,0,$nbatoms[$NM]);
	if($atombrut[$NM] == 1){format_name MOL_OUTN "RESULTbis";}
	else{format_name MOL_OUTN "RESULT";}
	$h++; $NC++;
	open(MOL_OUTN, ">Mol_m$NM-o$NC-rbra_rot$h.pdb");
	$h--; $NC--;
	for($i=0; $i<$nbatoms[$NM]; $i++){
		$atom=$tab[1][$i][$NM];
		if(($tab[1][$i][$NM]=~/T$/)){ $atom=~s/T//; }
		$i++;
		$atom="$atom"."$i";
		$i--;
		write MOL_OUTN;
	}	
	close(MOL_OUTN);
}
sub Reorientation_rbra_trans(){
	for($i=0; $i<$nbatoms[$NM]; $i++){
		$tab2[0][$i][$NM]=$coord[0][$i][$NC][$NM]; # X
		$tab2[1][$i][$NM]=$coord[1][$i][$NC][$NM]; # Y
		$tab2[2][$i][$NM]=$coord[2][$i][$NC][$NM]; # Z
	}
	$xt=$trans[$h][0][$NM]; 
	$yt=$trans[$h][1][$NM]; 
	$zt=$trans[$h][2][$NM];
	translation($xt,$yt,$zt,1,0,$nbatoms[$NM]);
	if($atombrut[$NM] == 1){ format_name MOL_OUTN "RESULTbis"; }
	else{ format_name MOL_OUTN "RESULT"; }
	$h++; $NC++;
	open (MOL_OUTN, ">Mol_m$NM-o$NC-rbra_trans$h.pdb");
	$h--; $NC--;
	for($i=0; $i<$nbatoms[$NM]; $i++){
		$atom=$tab[1][$i][$NM];
		if( ($tab[1][$i][$NM] =~ /T$/) ){ $atom=~s/T//; }
		$i++;
		$atom="$atom"."$i";
		$i--;
		write MOL_OUTN;
	}	
	close(MOL_OUTN);
} # Elodie -April 2010 - End
#------------------------------------------------------------------------------------------------------------------
#----------------------------------------- SECTION FOR MEP COMPUTATION --------------------------------------------
#------------------------------------------------------------------------------------------------------------------
sub MEP_Calcul{
	if($MEPCHR_Calc eq "ON"){
		Log2pdb(); File4REDDB();
		$NM=1; $okk=0; $okk2=0;
		for($NM=1; $NM<=$dfmol; $NM++){
			if($NM==1){ print "\n   MEP(s) is/are being computed for molecule $NM ..."; }
			else{ print "\n\n   MEP(s) is/are being computed for molecule $NM ..."; }
			for ($NC=0; $NC<$nbconf[$NM]; $NC++){
				if ($nbconf[$NM]>1){
					$NC++;
					print "\n\n\tConformation $NC ... \t\t";
					$NC--;
				}
				if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
				if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
				if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
				if(($QMSOFT eq "GAMESS") || ($QMSOFT eq "FIREFLY")){	 			#------------ GAMESS ------------
format INGAM=
 @<<       @## @##.######## @##.######## @##.########
$atom,$tab[3][$i][$NM],$tab2[0][$i][$NM],$tab2[1][$i][$NM],$tab2[2][$i][$NM]
.
					for($i=0;$i<$nbatoms[$NM];$i++){
						$tab2[0][$i][$NM]=$coord[0][$i][$NC][$NM]; # X
						$tab2[1][$i][$NM]=$coord[1][$i][$NC][$NM]; # Y
						$tab2[2][$i][$NM]=$coord[2][$i][$NC][$NM]; # Z
					}
					for($w=0; $w<$nbmod[$NM]; $w++){
						format_name JOB2_FILE "INGAM";
						$w++; $NC++;
						open (JOB2_FILE, ">JOB2-gam_m$NM-$NC-$w.inp");
						$w--; $NC--;
						print JOB2_FILE "! Single point to get MEP - Input generated by R.E.D.-III.x\n!
 \$CONTRL ICHARG=$CHR_VAL[$NM] MULT=$MLT_VAL[$NM] RUNTYP=ENERGY MOLPLT=.T.\n         MPLEVL=0 UNITS=ANGS MAXIT=200 EXETYP=RUN \n";
						if ($MLT_VAL[$NM] == 1)	{ print JOB2_FILE "         SCFTYP=RHF \n"; }
						else        		{ print JOB2_FILE "         SCFTYP=UHF \n"; }
						if (($TestL4a[$NM] == 1) && ($PCGVAR == 0)) { print JOB2_FILE "         ISPHER=1 COORD=UNIQUE                         \$END\n"; }
						if (($TestL4a[$NM] == 1) && ($PCGVAR == 1)) { print JOB2_FILE "         D5=.T. COORD=UNIQUE                           \$END\n"; }
						else        		{ print JOB2_FILE "         COORD=UNIQUE                                  \$END\n"; }
						if ($PCGVAR == 0)	{
							if ($CHR_TYP eq "DEBUG") { print JOB2_FILE " \$SCF    DIRSCF=.T. CONV=1.0E-01                       \$END\n"; }
							else {print JOB2_FILE " \$SCF    DIRSCF=.T. CONV=1.0E-06                       \$END\n"; }
						}
						else 			{
							if ($CHR_TYP eq "DEBUG") { print JOB2_FILE " \$SCF    DIRSCF=.T. NCONV=1                            \$END\n"; }
							else {print JOB2_FILE " \$SCF    DIRSCF=.T. NCONV=6                            \$END\n"; }
						}
						if ($PCGVAR == 0)	{ print JOB2_FILE " \$SYSTEM TIMLIM=5000 MWORDS=32 MEMDDI=0                \$END\n"; }
						else			{ print JOB2_FILE " \$SYSTEM TIMLIM=5000 MWORDS=32                         \$END\n"; }
						if (($PCGVAR == 1) && ($NP != 1))	{ print JOB2_FILE " \$P2P     P2P=.T. DLB=.T.                              \$END\n"; }
						if(($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")||($CHR_TYP eq "RESP-A2")||($CHR_TYP eq "RESP-C2")||($CHR_TYP eq "ESP-A1")||($CHR_TYP eq "ESP-C1"))	
							{ print JOB2_FILE " \$BASIS  GBASIS=N31 NGAUSS=6 NDFUNC=1                  \$END\n"; }
						elsif(($CHR_TYP eq "ESP-A2")||($CHR_TYP eq "ESP-C2"))
							{ print JOB2_FILE " \$BASIS  GBASIS=STO NGAUSS=3                           \$END\n"; }
						elsif($CHR_TYP eq "DEBUG")
							{ print JOB2_FILE " \$BASIS  GBASIS=STO NGAUSS=2                           \$END\n"; }
						print JOB2_FILE " \$GUESS  GUESS=HUCKEL                                  \$END
! CHELPG/CONNOLLY CHARGES\n \$ELPOT  IEPOT=1 WHERE=PDC OUTPUT=BOTH                 \$END";
						if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-A2")||($CHR_TYP eq "ESP-A1")||($CHR_TYP eq "ESP-A2"))	
							{ print JOB2_FILE " \n \$PDC    PTSEL=CONNOLLY CONSTR=NONE                    \$END";}
						elsif(($CHR_TYP eq "RESP-C1")||($CHR_TYP eq "RESP-C2")||($CHR_TYP eq "ESP-C1")||($CHR_TYP eq "ESP-C2"))
							{ print JOB2_FILE " \n \$PDC    PTSEL=CHELPG CONSTR=NONE                      \$END";}
						print JOB2_FILE "\n \$DATA\n $TITLE[$NM]\n C1\n";
						if($atombrut[$NM]==1){
format RESULTbis=
ATOM  @#### @<<< @<<< @###    @##.####@##.####@##.####
$i+1,$tab[10][$i][$NM],$tab[4][$i][$NM],$residu[$i][$NM],$tab2[0][$i][$NM],$tab2[1][$i][$NM],$tab2[2][$i][$NM]
.
						}else{
format RESULT=
ATOM  @#### @<<< @<<< @###    @##.####@##.####@##.####
$i+1,$atom,$tab[4][$i][$NM],$residu[$i][$NM],$tab2[0][$i][$NM],$tab2[1][$i][$NM],$tab2[2][$i][$NM]
.
						}
						if($reorient[$NM]==1){ # Elodie - April 2010 - Beginning
							if((0<=$w)&&($w<$nbrot[$NM])){
								$h=$w;
								Reorientation_rbra(); }
							if(($nbrot[$NM]<=$w)&&($w<$nbrot_rotate[$NM]+$nbrot[$NM])){
								$h=$w-$nbrot[$NM];
								Reorientation_rbra_rot();}
							if(($nbrot_rotate[$NM]+$nbrot[$NM]<=$w)&&($w<$nbmod[$NM])){
								$h=$w-$nbrot_rotate[$NM]-$nbrot[$NM];
								Reorientation_rbra_trans();}
						} # Elodie - April 2010 - End
						for($i=0; $i<$nbatoms[$NM]; $i++){
							$atom=$tab[1][$i][$NM];
							if(($tab[1][$i][$NM] =~ /T$/)){ $atom=~s/T//; }
							write JOB2_FILE;
						}
						print JOB2_FILE " \$END\n\n\n";
						close(JOB2_FILE);
						$w++; $NC++;
						$currDir=`pwd`; chomp($currDir);
						if (($PCGVAR==1) && ($OS eq "DARWIN")){							# Firefly EXECUTION ON MAC OS/Darwin
							system ("$wine $firefly -osx -r -f -p -stdext -i $currDir/JOB2-gam_m$NM-$NC-$w.inp -o $currDir/JOB2-gam_m$NM-$NC-$w.log -t $scrpath/ -np $NP");
							if (-e "./PUNCH")   { system ("mv PUNCH JOB2-gam_m$NM-$NC-$w.dat"); }
							if (-e "./input")   { system ("rm input"); }
							if (-e "./AOINTS")  { system ("rm AOINTS"); }
							if (-e "./DICTNRY") { system ("rm DICTNRY"); }
							# system ("rm -rf $scrpath/pcg.* $scrpath/*");
						}
						elsif (($PCGVAR==1) && ($OS =~ /CYGWIN/)){						# Firefly EXECUTION ON WINDOWS/CYGWIN
							$scrpathw=$scrpath; $scrpathw=`cygpath -w $scrpathw`; $scrpathw=~s/\\/\\\\/g; chomp($scrpathw);
							$currDir=`cygpath -w $currDir`; $currDir=~s/\\/\\\\/g; chomp($currDir);
							# system ("$firefly -r -f -p -stdext -i $currDir\\\\JOB2-gam_m$NM-$NC-$w.inp -o $currDir\\\\JOB2-gam_m$NM-$NC-$w.log -t $scrpathw\\\\ -np $NP ");
							# system ("$firefly -r -f -i $currDir\\\\JOB2-gam_m$NM-$NC-$w.inp > JOB2-gam_m$NM-$NC-$w.log -t $scrpathw\\\\ -np $NP ");
							system ("$firefly -r -f -i $currDir\\\\JOB2-gam_m$NM-$NC-$w.inp -O $currDir\\\\JOB2-gam_m$NM-$NC-$w.log -t $scrpathw\\\\ -np $NP ");
							if (-e "$scrpath/pcg.0/PUNCH")   { system ("mv $scrpath/pcg.0/PUNCH JOB2-gam_m$NM-$NC-$w.dat"); }
							if (-e "./PUNCH")   { system ("mv PUNCH JOB2-gam_m$NM-$NC-$w.dat"); }
							if (-e "./input")   { system ("rm input"); }
							if (-e "./AOINTS")  { system ("rm AOINTS"); }
							if (-e "./DICTNRY") { system ("rm DICTNRY"); }
						}
						elsif(($PCGVAR==1) && ($OS ne "DARWIN") || ($PCGVAR==1) && ($OS !~ /CYGWIN/)){		# Firefly EXECUTION ON UNIX
							if (($NP==1) || ($MPIVAR==0)){
								# After PC-GAMESS/Firefly v. 7.1.E, activate the following command:
								# system ("$firefly -r -f -p -stdext -i $currDir/JOB2-gam_m$NM-$NC-$w.inp -o $currDir/JOB2-gam_m$NM-$NC-$w.log -t $scrpath/ -ex $pathfirefly/");
								system ("$firefly -r -f -p -i $currDir/JOB2-gam_m$NM-$NC-$w.inp -o $currDir/JOB2-gam_m$NM-$NC-$w.log -t $scrpath/ -ex $pathfirefly/");
							}
							else {	# After PC-GAMESS/Firefly v. 7.1.E, activate the following command:
								# system ("mpirun -np $NP $firefly -r -f -p -stdext -i $currDir/JOB2-gam_m$NM-$NC-$w.inp -o $currDir/JOB2-gam_m$NM-$NC-$w.log -t $scrpath/ -ex $pathfirefly/");
								system ("mpirun -np $NP $firefly -r -f -p -i $currDir/JOB2-gam_m$NM-$NC-$w.inp -o $currDir/JOB2-gam_m$NM-$NC-$w.log -t $scrpath/ -ex $pathfirefly/");
							}
							if (-e "./PUNCH")   { system ("mv PUNCH JOB2-gam_m$NM-$NC-$w.dat"); }
							if (-e "./input")   { system ("rm input"); }
							if (-e "./AOINTS")  { system ("rm AOINTS"); }
							if (-e "./DICTNRY") { system ("rm DICTNRY"); }
							# system ("rm -rf $scrpath/pcg.* $scrpath/*");
						}
						elsif (($PCGVAR==0) && ($OS=~/CYGWIN/)){						# GAMESS EXECUTION ON CYGWIN
							system ("cp JOB2-gam_m$NM-$NC-$w.inp $scrpath/JOB2-gam_m$NM-$NC-$w.F05");
							system ("$csh -f $runscript JOB2-gam_m$NM-$NC-$w $gx $NP $pathwingamess $hostname > $currDir/JOB2-gam_m$NM-$NC-$w.log");
							system ("mv $tmppath/JOB2-gam_m$NM-$NC-$w.dat .");					
						}else {											# GAMESS EXECUTION ON UNIX & DARWIN
							system ("$rungms JOB2-gam_m$NM-$NC-$w $gx $NP > JOB2-gam_m$NM-$NC-$w.log");
							if (defined ($scrpathuser)) { system ("mv $scrpathuser/JOB2-gam_m$NM-$NC-$w.dat ."); }
							else { system ("mv $scrpath/JOB2-gam_m$NM-$NC-$w.dat ."); }
						}
						$ok=0;
						open(VERIF2,"JOB2-gam_m$NM-$NC-$w.log");
						foreach $arg (<VERIF2>){
							if($arg =~ /TERMINATED NORMALLY/ig) { $ok=1; }
							if(($arg =~ /TERMINATED -ABNORMALLY-/ig) || ($arg =~ /TERMINATED ABNORMALLY/ig)) { $okk=1; }
						}
						close(VERIF2);
						open(VERIFX,"JOB2-gam_m$NM-$NC-$w.dat");
						$w--; $NC--;
						foreach $arg (<VERIFX>){
							if($arg =~ /ELECTRIC POTENTIAL/ig) { $okk2=1; }
							if($arg =~ /TOTAL NUMBER OF GRID POINTS/ig) { $okk2=1; }
						}
						close(VERIFX);
						if($okk==1) { $ok=0; }
						if($okk2==0) { $ok=0; }
					}
					$NC++;
					$JOB="JOB2-gam_m$NM-$NC-(X)";
					$NC--;
				}else{											#------------ Gaussian ------------
format INGAU2=
  @<<    @##.########    @##.########    @##.########
$atom,$tab2[0][$i][$NM],$tab2[1][$i][$NM],$tab2[2][$i][$NM]
.
					for($i=0; $i<$nbatoms[$NM]; $i++){
						$tab2[0][$i][$NM]=$coord[0][$i][$NC][$NM];# X
						$tab2[1][$i][$NM]=$coord[1][$i][$NC][$NM];# Y
						$tab2[2][$i][$NM]=$coord[2][$i][$NC][$NM];# Z
					}
					for($w=0; $w<$nbmod[$NM]; $w++){
						$w++; $NC++;
						$JOB="JOB2-gau_m$NM-$NC-(X)";	
						open (JOB2_FILE, ">JOB2-gau_m$NM-$NC-$w.com");
						$w--; $NC--;
						format_name JOB2_FILE "INGAU2";
						printf JOB2_FILE ("%%Mem=256MB \n");
						printf JOB2_FILE ("%%NProc=$NP \n\n");
						if(($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")||($CHR_TYP eq "RESP-A2")||($CHR_TYP eq "RESP-C2")||($CHR_TYP eq "ESP-A1")||($CHR_TYP eq "ESP-C1"))
						#____#3 { printf JOB2_FILE ("#P b3lyp/cc-pVTZ SCRF(IEFPCM,Solvent=Ether) SCF(Conver=6) NoSymm Test \n"); }  # Modification for Duan et al. FF
							{ printf JOB2_FILE ("#P HF/6-31G* SCF(Conver=6) NoSymm Test \n"); } ##__##3 
						elsif(($CHR_TYP eq "ESP-A2")||($CHR_TYP eq "ESP-C2"))
							{ printf JOB2_FILE ("#P HF/STO-3G SCF(Conver=6) NoSymm Test \n"); }
						elsif($CHR_TYP eq "DEBUG")
							{ printf JOB2_FILE ("#P HF/STO-2G SCF(Conver=1) NoSymm Test \n"); }
						if ($TestL4a[$NM] == 1){ 
							if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-A2")||($CHR_TYP eq "ESP-A1")||($CHR_TYP eq "ESP-A2"))
								{printf JOB2_FILE "   5D Pop=(mk,ReadRadii) IOp(6/33=2) GFinput GFprint \n\n"; }
							elsif(($CHR_TYP eq "RESP-C1")||($CHR_TYP eq "RESP-C2")||($CHR_TYP eq "ESP-C1")||($CHR_TYP eq "ESP-C2"))
								{printf JOB2_FILE "   5D Pop=(chelpg,ReadRadii) IOp(6/33=2) GFinput GFprint \n\n"; }
						}else{ 
							if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-A2")||($CHR_TYP eq "ESP-A1")||($CHR_TYP eq "ESP-A2"))
								{printf JOB2_FILE "   Pop=mk IOp(6/33=2) GFInput GFPrint \n\n"; }
								# {printf JOB2_FILE "   Pop=mk GFInput GFPrint \n\n"; } # For debugging purpose: do not use!
							elsif(($CHR_TYP eq "RESP-C1")||($CHR_TYP eq "RESP-C2")||($CHR_TYP eq "ESP-C1")||($CHR_TYP eq "ESP-C2"))
								{printf JOB2_FILE "   Pop=chelpg IOp(6/33=2) GFInput GFPrint \n\n"; }
						}
						printf JOB2_FILE ("MEP - Input generated by R.E.D.-III.x %s \n\n%s %s \n",$TITLE[$NM],$CHR_VAL[$NM],$MLT_VAL[$NM]);
						if($reorient[$NM]==1){ # Elodie -April 2010 - Beginning
							if((0<=$w) && ($w<$nbrot[$NM])){
								$h=$w;
								Reorientation_rbra(); }
							if(($nbrot[$NM]<=$w) && ($w<$nbrot_rotate[$NM]+$nbrot[$NM])){
								$h=$w-$nbrot[$NM];
								Reorientation_rbra_rot();}
							if(($nbrot_rotate[$NM]+$nbrot[$NM]<=$w) && ($w<$nbmod[$NM])){
								$h=$w-$nbrot_rotate[$NM]-$nbrot[$NM];
								Reorientation_rbra_trans();}
						} # Elodie -April 2010 - End
						for($i=0; $i<$nbatoms[$NM]; $i++){
							$atom=$tab[1][$i][$NM];
							if(($tab[1][$i][$NM]=~/T$/)){ $atom=~s/T//; }
							write JOB2_FILE;
						}
						print JOB2_FILE "\n";
						$kvar=$cavar=$scvar=$tivar=$vvar=$crvar=$mnvar=$fevar=$covar=$nivar=$cuvar=$znvar=$gavar=$gevar=$asvar=$sevar=$brvar=0; # 4th lines of periodic table
						for($i=0; $i<$nbatoms[$NM]; $i++){
							if(($tab[99][$i][$NM] eq "K")  && ($kvar == 0))  { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $kvar = 1; } # 1.8 is the value implemented in GAMESS
							if(($tab[99][$i][$NM] eq "CA") && ($cavar == 0)) { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $cavar = 1; }
							if(($tab[99][$i][$NM] eq "SC") && ($scvar == 0)) { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $scvar = 1; }
							if(($tab[99][$i][$NM] eq "TI") && ($tivar == 0)) { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $tivar = 1; }
							if(($tab[99][$i][$NM] eq "V")  && ($vvar == 0))  { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $vvar = 1; }
							if(($tab[99][$i][$NM] eq "CR") && ($crvar == 0)) { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $crvar = 1; }
							if(($tab[99][$i][$NM] eq "MN") && ($mnvar == 0)) { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $mnvar = 1; }
							if(($tab[99][$i][$NM] eq "FE") && ($fevar == 0)) { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $fevar = 1; }
							if(($tab[99][$i][$NM] eq "CO") && ($covar == 0)) { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $covar = 1; }
							if(($tab[99][$i][$NM] eq "NI") && ($nivar == 0)) { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $nivar = 1; }
							if(($tab[99][$i][$NM] eq "CU") && ($cuvar == 0)) { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $cuvar = 1; }
							if(($tab[99][$i][$NM] eq "ZN") && ($znvar == 0)) { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $znvar = 1; }
							if(($tab[99][$i][$NM] eq "GA") && ($gavar == 0)) { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $gavar = 1; }
							if(($tab[99][$i][$NM] eq "GE") && ($gevar == 0)) { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $gevar = 1; }
							if(($tab[99][$i][$NM] eq "AS") && ($asvar == 0)) { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $asvar = 1; }
							if(($tab[99][$i][$NM] eq "SE") && ($sevar == 0)) { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $sevar = 1; }
							if(($tab[99][$i][$NM] eq "BR") && ($brvar == 0)) { printf JOB2_FILE (" $tab[99][$i][$NM]  1.8\n"); $brvar = 1; } # Gaussian uses 2.3 by default...
						}
						print JOB2_FILE "\n\n";
						close(JOB2_FILE);
						$w++; $NC++;	
						# system ("$gauss < JOB2-gau_m$NM-$NC-$w.com > JOB2-gau_m$NM-$NC-$w.log");		# GAUSSIAN EXECUTION !
						system ("$gauss JOB2-gau_m$NM-$NC-$w.com");
						if (-e "JOB2-gau_m$NM-$NC-$w.out") { system("mv JOB2-gau_m$NM-$NC-$w.out JOB2-gau_m$NM-$NC-$w.log"); } # Cygwin...
						$ok=0;
						open(VERIF2,"JOB2-gau_m$NM-$NC-$w.log");
						$w--; $NC--;
						foreach $arg (<VERIF2>){
							if($arg =~ /Normal termination of Gaussian/ig) { $ok=1; }
							if($arg =~ /Error termination via/ig) { $okk=1; }
							if($arg =~ / ESP Fit Center /ig) { $okk2=1; }
						}
						close(VERIF2);
						if($okk==1) { $ok=0; }
						if($okk2==0) { $ok=0; }
					}
				}
				if ($CHR_TYP ne "DEBUG") { open(STDOUT,">&OLDSTDOUT"); }
				if($ok==1){
					if($nbconf[$NM]==1) { print "\t\t\t[ OK ]\n\tSee the file(s) \"$JOB.log\""; }
					else		 { print "\t\t\t\t[ OK ]\n\tSee the file(s) \"$JOB.log\""; }
				}
				else{
					if($nbconf[$NM]==1) {
						if($okk2==0){
							print "\n\n\tNo electrostatic potential found!\n";
							if(($QMSOFT eq "GAMESS") || ($QMSOFT eq "FIREFLY")){
								print "\tDid you modified the R.E.D. source code? Re-download the program\n";
								print "\t  or contact the R.E.D. developers\t";
							}
							else {
								print "\tDid you modified the R.E.D. source code? Re-download the program.\n";
								print "\tIs Gaussian B.01 interfaced? Use another Gaussian version\n";
								print "\t  or contact the R.E.D. developers\t";
							}
						}
						print "\t\t\t[ FAILED ]\n\tSee the file(s) \"$JOB.log\"\n\n"; $check=0; Information();
						if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
					}
					else{
						if($okk2==0){
							print "\n\n\tNo electrostatic potential found!\n";
							if(($QMSOFT eq "GAMESS") || ($QMSOFT eq "FIREFLY")){
								print "\tDid you modified the R.E.D. source code? Re-download the program\n";
								print "\t  or contact the R.E.D. developers";
							}
							else {
								print "\tDid you modified the R.E.D. source code? Re-download the program.\n";
								print "\tIs Gaussian B.01 interfaced? Use another Gaussian version\n";
								print "\t  or contact the R.E.D. developers";
							}
						}
						print "\t\t\t\t[ FAILED ]\n\tSee the file(s) \"$JOB.log\"\n\n"; $check=0; Information();
						if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
					}
				}
			} 
		}
	} 
	elsif ($Re_Fit eq "ON") { Log2pdb(); }
}
#---------------------------------------------------------------------------------------------------------
#----------------------------------- MAKE ESPOT FILE -----------------------------------------------------
#---------------------------------------------------------------------------------------------------------
sub Makespot{
	$NM=1;
	for($NM=1; $NM<=$dfmol; $NM++){
format HEADER=
 @###@####  @##          @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 
$nbatoms[$NM], $nbpoint[$NM], $CHR_VAL[$NM], $TITLE[$NM]
.
		if(($QMSOFT eq "GAMESS") || ($QMSOFT eq "FIREFLY")){				#------------ GAMESS ------------
			for($NC=1; $NC<=$nbconf[$NM]; $NC++){
				for($w=1; $w<=$nbmod[$NM]; $w++){
					$flag1=0;
					open(JOB2DAT,"<JOB2-gam_m$NM-$NC-$w.dat");
					foreach (<JOB2DAT>){
						if(/ELECTRIC POTENTIAL/ig){ $flag1=1; }
						elsif(/TOTAL NUMBER OF GRID POINTS/ig){ $flag1=1; }
						if($flag1==1){
							if(/START OF -MOLPLT- INPUT FILE/ig){ $flag1=0; }
							if($flag1==1){ ($nbpoint[$NM])=(split(' '))[0]; }
						}
					}
					close(JOB2DAT);
					$flag1=$flag2=0;
					format_name ESPO "HEADER";
					open(ESPO,">espot_m$NM-$NC-$w");
					write ESPO;
					open(JOB2LOG,"<JOB2-gam_m$NM-$NC-$w.log");
					foreach(<JOB2LOG>){
						if((/ATOM/ig)&&(/ATOMIC/ig)&&(/COORDINATES/ig)){ $flag1=1; }
						if($flag1 == 1){				 $flag2++; }
						if(($flag2>2)&&($flag2<$nbatoms[$NM]+3)){	# Inspired by "Run.resp" (Hans De Winter -RIMR)
							($x,$y,$z)=(split(' '))[2,3,4];		# See http://amber.scripps.edu/Questions/resp2.txt
							printf ESPO ("                %16.7E%16.7E%16.7E\n",$x,$y,$z);
						}
					}
					close(JOB2LOG);
					$flag1=$flag2=0;
					open(JOB2DAT,"<JOB2-gam_m$NM-$NC-$w.dat");
					foreach (<JOB2DAT>){
						if(/ELECTRIC POTENTIAL/ig){		$flag1=1; }
						elsif(/TOTAL NUMBER OF GRID POINTS/ig){ $flag1=1; }
						if(/START OF -MOLPLT- INPUT FILE/ig){	$flag2=0; }
						if($flag2 == 1){
							($x,$y,$z,$charge)=(split(' '))[1,2,3,4];
							printf ESPO ("%16.7E%16.7E%16.7E%16.7E\n", $charge,$x,$y,$z);
						}
						if($flag1==1){ $flag2=1; $flag1=0; }
					}
					close(JOB2DAT);
					close(ESPO);
				}
			}
		}else{									#------------ Gaussian ------------
			for($NC=1; $NC<=$nbconf[$NM]; $NC++){
				for($w=1; $w<=$nbmod[$NM]; $w++){
					$nbpoint[$NM]=0;
					open(JOB2LOG,"<JOB2-gau_m$NM-$NC-$w.log");
					foreach (<JOB2LOG>){ if(/ESP FIT Center/ig){ $nbpoint[$NM]++;} }
					close(JOB2LOG);
					format_name ESPO "HEADER";
					open(ESPO,">espot_m$NM-$NC-$w");
					write ESPO;
					$flag1=$flag2=$i=0;
					open(JOB2LOG,"<JOB2-gau_m$NM-$NC-$w.log");
					foreach (<JOB2LOG>){
						if((/Electrostatic Properties /ig)&&(/Atomic Units/ig)){ $flag1=1; }
						if($flag1==1){ $flag2++; }
						if(($flag2>$nbatoms[$NM]+6) && ($flag2<$nbpoint[$NM]+$nbatoms[$NM]+7)){
							($charge[$i][$NM])=(split(' '))[2]; $i++;
						}
					}
					close(JOB2LOG);
					$i=0;
					open(JOB2LOG,"<JOB2-gau_m$NM-$NC-$w.log");
					foreach (<JOB2LOG>){
						if(/^       Atomic Center/ig){
							# ($x,$y,$z)=(split(' '))[5,6,7];		# FyD February 2009
							($x,$y,$z) = unpack("x32 A10 A10 A10",$_);
							$x=$x/0.529177249;		# Inspired by "readit.f" & "esp.sh" (J. Caldwell - UCSF)
							$y=$y/0.529177249;		# See http://amber.scripps.edu/Questions/resp.txt
							$z=$z/0.529177249;
							printf ESPO ("                %16.7E%16.7E%16.7E\n",$x,$y,$z); }
						if(/^      ESP Fit Center/ig){
							# ($x,$y,$z)=(split(' '))[6,7,8];               # FyD February 2009
							($x,$y,$z) = unpack("x32 A10 A10 A10",$_);
							$x=$x/0.529177249;
							$y=$y/0.529177249;
							$z=$z/0.529177249;
							printf ESPO ("%16.7E%16.7E%16.7E%16.7E\n",$charge[$i][$NM],$x,$y,$z);
							$i++; }
					}
					close(JOB2LOG);
					close(ESPO);
				}
			}
		}
		open(ESPOT,">espot_m$NM");
		for($NC=1; $NC<=$nbconf[$NM]; $NC++){
			for($w=1; $w<=$nbmod[$NM]; $w++){
				open(ESPO,"<espot_m$NM-$NC-$w");
				print ESPOT <ESPO>;
				close(ESPO);
			}
		}
		print ESPOT "\n\n";
		close(ESPOT);
		if(($nbmod[$NM]<=1) && (-e "./espot1")){ system ("rm espot1"); }
	}
}
#---------------------------------------------------------------------------------------------------------
#-------------------------------- ESP/RESP  input1 & input2 generator ------------------------------------
#---------------------------------------------------------------------------------------------------------
sub Inputgene{
	if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1"))	{ $qwt = 0.0005; }	# RESP/6-31G* (Connolly & chelpg) 2 stages
	elsif(($CHR_TYP eq "RESP-A2")||($CHR_TYP eq "RESP-C2"))				{ $qwt = 0.01; }	# RESP/6-31G* (Connolly & chelpg) 1 stage
	elsif(($CHR_TYP eq "ESP-A1")||($CHR_TYP eq "ESP-C1"))				{ $qwt = 0.0000; }	# ESP/6-31G*  (Connolly & chelpg) 1 stage
	else { $qwt = 0.0000; }											# ESP/STO-3G  (Connolly & chelpg) 1 stage
	$NM=1;
	for($NM=1; $NM<=$dfmol; $NM++){
		$i=$testaff=0;				#--------------------------- RESP INPUT 1 ----------------------------------------
format IN1=
  @## @###                      @###
$tab[3][$i][$NM],$temp1[$i][$NM],$i+1
.
format IN2=
  @## @###                      @###
$tab[3][$i][$NM],$temp2[$i][$NM],$i+1
.
format IN3=
  @## @###                      @###
$tab[3][$i][$NM],$temp3[$i][$NM],$i+1
.
format IN4=
  @## @###                      @###
$tab[3][$i][$NM],$temp4[$i][$NM],$i+1
.
		$nbtot[$NM]=$nbmod[$NM]*$nbconf[$NM];
		open(INP1,">input1_m$NM");
		printf INP1 (" %s project. RESP input generated by R.E.D.\n &cntrl\n  ioutopt=1, iqopt=1, nmol=$nbtot[$NM], ihfree=1, irstrnt=1, qwt= %1.4f \n &end \n  1.0\n %s \n%5s%5d          Column not used by RESP (Added by R.E.D. for information)\n",$CHR_TYP,$qwt,$TITLE[$NM],$CHR_VAL[$NM],$nbatoms[$NM]);
		format_name INP1 "IN1";
		for($i=0; $i<$nbatoms[$NM]; $i++){
			$temp1[$i][$NM]=$temp2[$i][$NM]=$temp3[$i][$NM]=$temp4[$i][$NM]=0;
			if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")){ 
				if ($tab[1][$i][$NM]=~/T$/) { 		# If the current atom ends with a T
					$temp1[$i][$NM]=0; write INP1;
				}else{
					$flag=0;
					for ($j=0; $j<$nbatoms[$NM]; $j++) {	# If both atoms have the same number in their name, and one of them ends with a T
						if(($tab[2][$j][$NM]==$tab[2][$i][$NM]) && ($tab[1][$j][$NM]=~/T$/) && ($flag==0)){
							$temp1[$i][$NM]=0; $flag=1; }
					}
					for ($j=0; $j<$i ;$j++) {		# If both atoms have the same name
						if(($tab[1][$j][$NM] eq $tab[1][$i][$NM]) && ($tab[2][$j][$NM]==$tab[2][$i][$NM]) && ($flag==0) ){
							$temp1[$i][$NM]=$j+1; $flag=1; }
					}
					write INP1;
				}
			}elsif(($CHR_TYP eq "ESP-A1")||($CHR_TYP eq "ESP-C1")||($CHR_TYP eq "RESP-A2")||($CHR_TYP eq "RESP-C2")){
				$temp1[$i][$NM]=$flag=0;
				for($z=0; $z<$nbatoms[$NM]; $z++){
					if(($tab[2][$i][$NM]==$tab[2][$z][$NM]) && ($flag==0)){ $flag=1; } #($tab[1][$z] =~ /T$/) &&
				}
				if($flag==1){
					$flag=$temp[$i][$NM]=0;
					for($z=0; $z<$i; $z++){
						if( ($tab[1][$z][$NM] eq $tab[1][$i][$NM]) && ($tab[2][$z][$NM]==$tab[2][$i][$NM]) && ($flag==0) ){
							$temp1[$i][$NM]=$z+1; $flag=1;
						}
					}
					write INP1;
				}else{
					$temp1[$i][$NM]=0;
					write INP1;
				}
			}else{    #--- ESP-A2 and ESP-C2 case
				write INP1; $temp1[$i][$NM]=0;
			}
		}
		if($nbtot[$NM] > 1){
			for($j=0; $j<$nbtot[$NM]-1; $j++){
				printf INP1 ("\n  1.0\n %s \n%5s%5d\n",$TITLE[$NM],$CHR_VAL[$NM],$nbatoms[$NM]);
				for($i=0; $i<$nbatoms[$NM]; $i++){ write INP1; }
			}
			for($i=1; $i<=$nbatoms[$NM]; $i++){
				if($temp1[$i-1][$NM]==0){ $testaff=1; }
			}	
			if ($testaff==1){ print INP1 "\n                    Inter-'molecular' charge equivalencing (i. e. for orientations, conformations or different molecules)\n"; }
			for($i=1; $i<=$nbatoms[$NM]; $i++){
				if($temp1[$i-1][$NM]==0){
					$nmol=$nbtot[$NM];
					printf INP1 ("  %3d\n",$nmol);
					$comp=0;
					for($j=1; $j<=$nbtot[$NM]; $j++){
						if($j==1){ printf INP1 ("  %3d  %3d",$j,$i); $comp++;
						}else{
							printf INP1 ("  %3d  %3d",$j,$i); $comp++;
							if(($comp==8) && ($j!=$nbtot[$NM])){ printf INP1 ("\n"); $comp=0;
							}
						}
					}
					print INP1 "\n";
				}
			}
		}
		print INP1 "\n\n\n\n\n\n";
		close(INP1);				    #--------------------------- RESP INPUT 2 ----------------------------------------
		if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")) {
			$testaff=0;
			open(INP2,">input2_m$NM");
			printf INP2 (" %s project. RESP input generated by R.E.D.\n &cntrl\n  ioutopt=1, iqopt=2, nmol=$nbtot[$NM], ihfree=1, irstrnt=1, qwt= 0.001 \n &end \n  1.0\n %s \n%5s%5d          Column not used by RESP (Added by R.E.D. for information)\n",$CHR_TYP,$TITLE[$NM],$CHR_VAL[$NM],$nbatoms[$NM]);
			format_name INP2 "IN2";
			for($i=0; $i<$nbatoms[$NM]; $i++){ 
				$flag=0;
				if($tab[1][$i][$NM]=~/T$/){			#------ If the current atom ends with a T 
					$temp2[$i][$NM]=$flag=0;
					for($z=0; $z<$i; $z++){
						if(($tab[1][$z][$NM] eq $tab[1][$i][$NM]) && ($tab[2][$z][$NM]==$tab[2][$i][$NM]) && ($flag==0)){ $temp2[$i][$NM]=$z+1; $flag=1; }
					}
					write INP2;
				}else{
					$temp2[$i][$NM]=$flag=0;
					for($z=0; $z<$nbatoms[$NM]; $z++){
						if(($tab[1][$z][$NM]=~/T$/) && ($tab[2][$i][$NM]==$tab[2][$z][$NM]) && ($flag==0)){ $flag=1; }
					}
					if($flag==1){
						$flag=$temp2[$i][$NM]=0;
						for($z=0; $z<$i; $z++){
							if(($tab[1][$z][$NM] eq $tab[1][$i][$NM]) && ($tab[2][$z][$NM]==$tab[2][$i][$NM]) && ($flag==0)){ $temp2[$i][$NM]=$z+1; $flag=1; }
						}
						write INP2;
					}else{ $temp2[$i][$NM]=-1; write INP2;
					}
				}
			}
			if($nbtot[$NM]>1){
				for($j=0; $j<$nbtot[$NM]-1; $j++){
					printf INP2 ("\n  1.0\n %s \n%5s%5d\n",$TITLE[$NM],$CHR_VAL[$NM],$nbatoms[$NM]);
					for($i=0; $i<$nbatoms[$NM]; $i++) { write INP2; }
				}
				for($i=1; $i<=$nbatoms[$NM]; $i++){
					if($temp2[$i-1][$NM]==0){ $testaff=1; }
				}	
				if($testaff==1){ print INP2 "\n                    Inter-'molecular' charge equivalencing (i. e. for orientations, conformations or different molecules)\n"; }
				for($i=1; $i<=$nbatoms[$NM]; $i++){
					if($temp2[$i-1][$NM]==0){
						$nmol=$nbtot[$NM];
						printf INP2 ("  %3d\n",$nmol); $comp=0;
						for($j=1; $j<=$nbtot[$NM]; $j++){
							if($j==1){
								printf INP2 ("  %3d  %3d",$j,$i); $comp++;
							}else{
								printf INP2 ("  %3d  %3d",$j,$i); $comp++;
								if(($comp == 8)&&($j != $nbtot[$NM])){
									printf INP2 ("\n"); $comp=0;
								}
							}
						}
						print INP2 "\n";
					}
				}
			}
			print INP2 "\n\n\n\n\n\n";
			close(INP2);
		}
		if($verifimr[$NM]==2){			#---------------------------- RESP INPUT 1.sm = single molecule ------------ -------------------------------------
			$i=$testaff=0;
			open(INP3,">input1_m$NM.sm");
			printf INP3 (" %s project. RESP input generated by R.E.D.\n &cntrl\n  ioutopt=1, iqopt=1, nmol=$nbtot[$NM], ihfree=1, irstrnt=1, qwt= %1.4f \n &end \n  1.0\n %s \n%5s%5d          Column not used by RESP (Added by R.E.D. for information)\n",$CHR_TYP,$qwt,$TITLE[$NM],$CHR_VAL[$NM],$nbatoms[$NM]);
			format_name INP3 "IN3";
			for($i=0; $i<$nbatoms[$NM]; $i++){
				if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")){
					if ($tab[1][$i][$NM]=~/T$/) { 		# If the current atom ends with a T
						$temp3[$i][$NM]=0; write INP3;
					}else{
						$flag=0;
						for ($j=0; $j<$nbatoms[$NM]; $j++) {	# If both atoms have the same number in their name, and one of them ends with a T
							if(($tab[2][$j][$NM]==$tab[2][$i][$NM]) && ($tab[1][$j][$NM]=~/T$/) && ($flag==0)){ $temp3[$i][$NM]=0; $flag=1; }
						}
						for ($j=0; $j<$i; $j++) {		# If both atoms have the same name
							if(($tab[1][$j][$NM] eq $tab[1][$i][$NM]) && ($tab[2][$j][$NM]==$tab[2][$i][$NM]) && ($flag==0)){ $temp3[$i][$NM]=$j+1; $flag=1; }
						}
						write INP3
					}
				}elsif(($CHR_TYP eq "ESP-A1")||($CHR_TYP eq "ESP-C1")||($CHR_TYP eq "RESP-A2")||($CHR_TYP eq "RESP-C2")){
					$temp3[$i][$NM]=$flag=0;
					for($z=0; $z<$nbatoms[$NM]; $z++){
						if(($tab[2][$i][$NM]==$tab[2][$z][$NM]) && ($flag==0)){ $flag=1; }
					}
					if($flag==1){
						$flag=$temp[$i][$NM]=0;
						for($z=0;$z<$i;$z++){
							if(($tab[1][$z][$NM] eq $tab[1][$i][$NM]) && ($tab[2][$z][$NM]==$tab[2][$i][$NM]) && ($flag==0) ){ $temp3[$i][$NM]=$z+1; $flag=1; }
						}
					write INP3;
					}else{ $temp3[$i][$NM]=0; write INP3;
					}	
				}else{    #--- ESP-A2 and ESP-C2 case
					$flag=$temp3[$i][$NM]=0;
					for($z=0;$z<$nbatoms[$NM];$z++){
						if(($tab[2][$i][$NM]==$tab[2][$z][$NM]) && ($flag==0)) { $flag=1; }
					}
					if($flag==1){
						$flag=$temp[$i][$NM]=0;
						for($z=0; $z<$i; $z++){
							$y=$w=$imrv=0;
							for($y=0; $y<$imrcount[$NM]; $y++){
								for($w=0; $w<$intramr[4][$y][$NM]; $w++){
									if($intratom[$w][$y][$NM]==$z+1){ $imrv=1; }
								}
							}
							if($imrv==1){
								if(($tab[1][$z][$NM] eq $tab[1][$i][$NM]) && ($tab[2][$z][$NM]==$tab[2][$i][$NM]) && ($flag==0)){
									$temp3[$i][$NM]=$z+1; $flag=1;
								}
							}
						}
					}
				write INP3;
				}
			}
			if($nbtot[$NM]>1){
				for($j=0; $j<$nbtot[$NM]-1; $j++){
					printf INP3 ("\n  1.0\n %s \n%5s%5d\n",$TITLE[$NM],$CHR_VAL[$NM],$nbatoms[$NM]);
					for($i=0; $i<$nbatoms[$NM]; $i++){ write INP3; }
				}
			}
			if($nbtot[$NM]>1){ printf INP3 ("                    Intra and/or inter-molecular charge constraints for atom or group of atoms\n"); }
			$rl=0;
			for($i=0; $i<$imrcount[$NM]; $i++){
				$nimr=$intramr[4][$i][$NM];
				if($intramr[1][$i][$NM] =~ /\-/){
					if($rl == 0){	printf INP3 ("  %3d %3f\n",$nimr,$intramr[1][$i][$NM]); }
					else{		printf INP3 ("\n  %3d %3f\n",$nimr,$intramr[1][$i][$NM]); }
				}else{	
					if($rl == 0){	printf INP3 ("  %3d  %3f\n",$nimr,$intramr[1][$i][$NM]); }
					else{		printf INP3 ("\n  %3d  %3f\n",$nimr,$intramr[1][$i][$NM]); }
				}
				$rl=1; $comp=0;
				for($j=1; $j<=$intramr[4][$i][$NM]; $j++){
					if($j==1){
						printf INP3 ("    1  %3d",$intratom[$j-1][$i][$NM]); $comp++;
					}else{
						printf INP3 ("    1  %3d",$intratom[$j-1][$i][$NM]); $comp++;
						if(($comp==8) && ($j!=$intramr[4][$i][$NM])){
							printf INP3 ("\n"); $comp=0;
						}
					}
				}
			}
			print INP3 "\n";
			if($nbtot[$NM]>1){
				for($i=1; $i<=$nbatoms[$NM]; $i++){ 
					if($temp3[$i-1][$NM]==0){ $testaff=1; }
				}
				if($testaff==1){ print INP3 "                    Inter-'molecular' charge equivalencing (i. e. for orientations, conformations or different molecules)\n"; }
				for($i=1; $i<=$nbatoms[$NM]; $i++){
					if($temp3[$i-1][$NM]==0){
						$nmol=$nbtot[$NM];
						printf INP3 ("  %3d\n",$nmol);
						$comp=0;
						for($j=1; $j<=$nbtot[$NM]; $j++){
							if($j==1){
								printf INP3 ("  %3d  %3d",$j,$i); $comp++;
							}else{
								printf INP3 ("  %3d  %3d",$j,$i); $comp++;
								if(($comp==8) && ($j!=$nbtot[$NM])){
									printf INP3 ("\n"); $comp=0;
								}
							}
						}
						print INP3 "\n";
					}
				}
			}
			print INP3 "\n\n\n\n\n\n";
			close(INP3);  				#---------------------------  RESP INPUT 2.sm -------------------------------------
			if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")){
				$testaff=0;
				open(INP4,">input2_m$NM.sm");
				printf INP4 (" %s project. RESP input generated by R.E.D.\n &cntrl\n  ioutopt=1, iqopt=2, nmol=$nbtot[$NM], ihfree=1, irstrnt=1, qwt= 0.001 \n &end \n  1.0\n %s \n%5s%5d          Column not used by RESP (Added by R.E.D. for information)\n",$CHR_TYP,$TITLE[$NM],$CHR_VAL[$NM],$nbatoms[$NM]);
				format_name INP4 "IN4";
				for($i=0; $i<$nbatoms[$NM]; $i++){
					$y=$w=$imrv=0;
					for($y=0; $y<$imrcount[$NM]; $y++){
						for($w=0; $w<$intramr[4][$y][$NM]; $w++){
							if($intratom[$w][$y][$NM]==$i+1){ $imrv=1; }
						}
					}
					$flag=$temp4[$i][$NM]=0;
					if(($tab[1][$i][$NM] =~ /T$/) && ($imrv != 1)){		#------ If the current atom ends with a T
						$temp4[$i][$NM]=$flag=0;
						for($z=0;$z<$i;$z++){
							if(($tab[1][$z][$NM] eq $tab[1][$i][$NM]) && ($tab[2][$z][$NM] == $tab[2][$i][$NM]) && ($flag == 0) ){
								$temp4[$i][$NM]=$z+1; $flag=1;
							}
						}
						write INP4;
					}elsif($imrv==1){ $temp4[$i][$NM]=-1; write INP4;
					}else{
						$temp4[$i][$NM]=$flag=0;
						for($z=0;$z<$nbatoms[$NM];$z++){
							if(($tab[1][$z][$NM]=~/T$/) && ($tab[2][$i][$NM]==$tab[2][$z][$NM]) && ($flag==0)){ $flag=1; }
						}
						if($flag==1){
							$flag=$temp4[$i][$NM]=0;
							for($z=0;$z<$i;$z++){
								if(($tab[1][$z][$NM] eq $tab[1][$i][$NM]) && ($tab[2][$z][$NM]==$tab[2][$i][$NM]) && ($flag==0)){ $temp4[$i][$NM]=$z+1; $flag=1; }
							}
							write INP4;
						}else{ $temp4[$i][$NM]=-1; write INP4;
						}
					}
				}
				if($nbtot[$NM]>1){
					for($j=0; $j<$nbtot[$NM]-1; $j++){
						printf INP4 ("\n  1.0\n %s \n%5s%5d\n",$TITLE[$NM],$CHR_VAL[$NM],$nbatoms[$NM]);
						for($i=0; $i<$nbatoms[$NM]; $i++){ write INP4; }
					}
					for($i=1; $i<=$nbatoms[$NM]; $i++){
						if($temp4[$i-1][$NM]==0){ $testaff=1; }
					}
					if($testaff==1){ print INP4 "\n                    Inter-'molecular' charge equivalencing (i. e. for orientations, conformations or different molecules)\n"; }
					for($i=1; $i<=$nbatoms[$NM]; $i++){
						if($temp4[$i-1][$NM] == 0){
							$nmol=$nbtot[$NM];
							printf INP4 ("  %3d\n",$nmol);	$comp=0;
							for($j=1;$j<=$nbtot[$NM];$j++){
								if($j==1){
									printf INP4 ("  %3d  %3d",$j,$i); $comp++;
								}else{
									printf INP4 ("  %3d  %3d",$j,$i); $comp++;
									if(($comp == 8)&&($j != $nbtot[$NM])){
										printf INP4 ("\n"); $comp=0;
									}
								}
							}
							print INP4 "\n";
						}
					}
				}
				print INP4 "\n\n\n\n\n\n";
				close(INP4);
			}
		}
	}
}
#---------------------------------------------------------------------------------------------------------
#----------------------------------- RESP or ESP charge Calculation ---------------------------------------
#---------------------------------------------------------------------------------------------------------
sub CHR_Calcul{
	if(($MEPCHR_Calc eq "ON") && ($Re_Fit eq "OFF")) { Makespot(); Inputgene(); }
	elsif($Re_Fit eq "ON"){
		for($NM=1; $NM<=$dfmol; $NM++){
			if ($countmolimrs==1) { 
				if (-e "$DIR/espot_m$NM") { system ("cp $DIR/espot_m$NM ."); }
				else { 	print "\n\t\tERROR: The espot file required in the re-fitting step is not found.\n\n"; $check=0; Information();
					if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0); }
			}
			elsif ($countmolimrs!=1) { 
				if (-e "$DIR/Mol_m$NM/espot_m$NM") { system ("cp -f $DIR/Mol_m$NM/espot_m$NM ."); }
				else { 	print "\n\t\tERROR: Some espot files required in the re-fitting step are not found.\n\n"; $check=0; Information();
					if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0); }
			}
		}
		Inputgene();
	}
	$NM=1;
	for($NM=1; $NM<=$dfmol; $NM++){
		print "\n\n   The $CHR_TYP charges are being derived for molecule $NM ...";
		if ($CHR_TYP ne "DEBUG") { open(STDERR,">/dev/null");  }
		if ($CHR_TYP ne "DEBUG") { open(OLDSTDOUT,">&STDOUT"); }
		if ($CHR_TYP ne "DEBUG") { open(STDOUT,">/dev/null");  }	#------ RESP input1 run ------
		system ("resp -O -i input1_m$NM -e espot_m$NM -o output1_m$NM -p punch1_m$NM -q qout_m$NM -t qout1_m$NM -w qwts_m$NM -s esout_m$NM");
		if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")){		#------ RESP input2 run ------
			system ("resp -O -i input2_m$NM -e espot_m$NM -o output2_m$NM -p punch2_m$NM -q qout1_m$NM -t qout2_m$NM -w qwts_m$NM -s esout_m$NM");
		}
		if($verifimr[$NM]==2){
			system ("resp -O -i input1_m$NM.sm -e espot_m$NM -o output1_m$NM.sm -p punch1_m$NM.sm -q qout_m$NM.sm -t qout1_m$NM.sm -w qwts_m$NM.sm -s esout_m$NM.sm");
			if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")){		#------ RESP input2 run ------
				system ("resp -O -i input2_m$NM.sm -e espot_m$NM -o output2_m$NM.sm -p punch2_m$NM.sm -q qout1_m$NM.sm -t qout2_m$NM.sm -w qwts_m$NM.sm -s esout_m$NM.sm");
			}
		}
		if ($CHR_TYP ne "DEBUG") { open(STDOUT,">&OLDSTDOUT"); }
		if(($CHR_TYP eq "ESP-A2")||($CHR_TYP eq "ESP-C2")){		#------ ESP Compute ------
			for($i=0; $i<$nbatoms[$NM]; $i++){
				$temp=$flag=$nbA=0;
				for($j=0; $j<$nbatoms[$NM]; $j++){
					if($tab[0][$i][$NM] eq $tab[0][$j][$NM]){
						if($flag==0){ $temp=$j+1; $flag++; }
						$nbA++;
					}
				}
				if($nbA>1){ $equiv[$i][$NM]=$temp;
				}else{ $equiv[$i][$NM]=$i+1; }
				if ($verifimr[$NM]==2){
					if($nbA>1){ $equivimr[$i][$NM]=$temp;
					}else{ $equivimr[$i][$NM]=$i+1; }
				}
			}
			if (-e "punch1_m$NM") {
				open (PUNCH1_FILE,"<punch1_m$NM");
				$i=0;
				while (defined($line=<PUNCH1_FILE>)){
					if($line=~/\s+\d+\s+\d+\s+(\-\d|\d)\.\d+\s+(\-\d|\d)\.\d+\s+/){
						$line=~s/\s+/:/ig;
						($qcharge[$i][$NM])=(split(/:/,$line))[4];
						$i++;
					}
				}
				close(PUNCH1_FILE);
				
#******************************RED-2012******************************						
format PUNCH2F_cc6 = 
@##     @##     @#.######	@#.######
$num,$num2,$average[$k][$NM],$average[$k][$NM]
.
				
format PUNCH2F_cc5 = 
@##     @##     @#.######	@#.#####
$num,$num2,$average[$k][$NM],$average[$k][$NM]
.
					
format PUNCH2F_cc3 = 
@##     @##     @#.######	@#.###
$num,$num2,$average[$k][$NM],$average[$k][$NM]
.
					
format PUNCH2F_cc2 = 
@##     @##     @#.######	@#.##
$num,$num2,$average[$k][$NM],$average[$k][$NM]
.
					
format PUNCH2F_cc1 = 
@##     @##     @#.######	@#.#
$num,$num2,$average[$k][$NM],$average[$k][$NM]
.
#******************************RED-2012******************************	
				
format PUNCH2F = 
@##     @##     @#.######	@#.####
$num,$num2,$average[$k][$NM],$average[$k][$NM]
.
				open(PUNCH2,">punch2_m$NM");
				printf PUNCH2 ("     Averaged ESP charges from punch1\n  Z     Equiv.    q(opt)	Rounding-Off\n");
				
				#******************************RED-2012******************************	
				if($COR_CHR==6){
					
					format_name PUNCH2 "PUNCH2F_cc6";
				
				}elsif($COR_CHR==5){
					
					format_name PUNCH2 "PUNCH2F_cc5";
					
				}elsif($COR_CHR==3){
					
					format_name PUNCH2 "PUNCH2F_cc3";
					
				}elsif($COR_CHR==2){
					
					format_name PUNCH2 "PUNCH2F_cc2";
					
				}elsif($COR_CHR==1){
					
					format_name PUNCH2 "PUNCH2F_cc1";
					
				}else{
				#******************************RED-2012******************************		
					
					format_name PUNCH2 "PUNCH2F";
					
				#******************************RED-2012******************************		
				}	
				#******************************RED-2012******************************	
				
				$k=$g=0;
				for($g=0; $g<$nbatoms[$NM]; $g++){
					$arg =$equiv[$g][$NM];
					$compt=$total=0;
					for($j=0;$j<=$i;$j++){
						if($arg==$equiv[$j][$NM]){ $compt++; $total+=$qcharge[$j][$NM]; }
					}
					if($equiv[$k][$NM]!=0){ $average[$k][$NM]=$total/$compt;
					}else{ $average[$k][$NM]=$qcharge[$k][$NM]; }
					$num=$tab[3][$k][$NM];
					$num2=$equiv[$k][$NM];
					write PUNCH2;
					$k++;
				}
				close(PUNCH2);
			}
			if($verifimr[$NM]==2){
				if (-e "punch1_m$NM.sm") {
					open (PUNCH1_FILE_IMR,"<punch1_m$NM.sm");
					$i=0;
					while (defined($line=<PUNCH1_FILE_IMR>)){
						if($line=~/\s+\d+\s+\d+\s+(\-\d|\d)\.\d+\s+(\-\d|\d)\.\d+\s+/){
							$line=~s/\s+/:/ig;
							($qchargeimr[$i][$NM])=(split(/:/,$line))[4];
							$i++;
						}
					}
					close(PUNCH1_FILE_IMR);
					
#******************************RED-2012******************************	

format PUNCH2FIMR_cc6 =
@##     @##     @#.######	@#.######
$num,$num2,$averageimr[$k][$NM],$averageimr[$k][$NM]
.

format PUNCH2FIMR_cc5 =
@##     @##     @#.######	@#.#####
$num,$num2,$averageimr[$k][$NM],$averageimr[$k][$NM]
.

format PUNCH2FIMR_cc3 =
@##     @##     @#.######	@#.###
$num,$num2,$averageimr[$k][$NM],$averageimr[$k][$NM]
.

format PUNCH2FIMR_cc2 =
@##     @##     @#.######	@#.##
$num,$num2,$averageimr[$k][$NM],$averageimr[$k][$NM]
.

format PUNCH2FIMR_cc1 =
@##     @##     @#.######	@#.#
$num,$num2,$averageimr[$k][$NM],$averageimr[$k][$NM]
.

#******************************RED-2012******************************
			
format PUNCH2FIMR =
@##     @##     @#.######	@#.####
$num,$num2,$averageimr[$k][$NM],$averageimr[$k][$NM]
.

					open(PUNCH2_IMR,">punch2_m$NM.sm");
					printf PUNCH2_IMR ("     Averaged ESP charges from punch1\n  Z     Equiv.    q(opt)	Rounding-Off\n");
					
					#******************************RED-2012******************************	
					if($COR_CHR==6){
						format_name PUNCH2_IMR "PUNCH2FIMR_cc6";
					}elsif($COR_CHR==5){
						format_name PUNCH2_IMR "PUNCH2FIMR_cc5";
					}elsif($COR_CHR==3){
						format_name PUNCH2_IMR "PUNCH2FIMR_cc3";
					}elsif($COR_CHR==2){
						format_name PUNCH2_IMR "PUNCH2FIMR_cc2";
					}elsif($COR_CHR==1){
						format_name PUNCH2_IMR "PUNCH2FIMR_cc1";
					}else{
					#******************************RED-2012******************************		
						
						format_name PUNCH2_IMR "PUNCH2FIMR";
						
					#******************************RED-2012******************************		
					}	
					#******************************RED-2012******************************	
					
					$k=$f=0;
					for($f=0; $f<$nbatoms[$NM]; $f++){
						$argimr =$equivimr[$f][$NM];
						$compt=$total=0;
						for($j=0; $j<=$i; $j++){
							$y=$w=$imrv=0;
							for($y=0; $y<$imrcount[$NM]; $y++){
								for($w=0;$w<$intramr[4][$y][$NM];$w++){
									if($intratom[$w][$y][$NM]==$j){ $imrv=1; }
								}
							}
							if(($argimr==$equivimr[$j][$NM])&&($imrv !=1)){ $compt++; $total+=$qchargeimr[$j][$NM]; }
						}
						if(($equivimr[$k][$NM] != 0)&& ($compt != 0)){ $averageimr[$k][$NM]=$total/$compt;
						}else{ $averageimr[$k][$NM]=$qchargeimr[$k][$NM]; }
						$num=$tab[3][$k][$NM];
						$num2=$equivimr[$k][$NM];
						write PUNCH2_IMR;
						$k++;
					}
					close(PUNCH2_IMR);
				}
			}
		}
		$ok=1;
		if (-e "punch1_m$NM") {
			open(PUNCH1,"<punch1_m$NM");
			foreach(<PUNCH1>){
				if(/\s+\d+\s+\d+\s+(\-\d+|\d+)\.\d+\s+/ig){
					($chr)=(split(' '))[3];
					if(($chr=~/\*+/) || ($chr=~"nan")) { $ok=0; } # FyD March 2009
					elsif(($chr==0) && ($ok!=0)){ $ok=2; }
				}
			}
			close(PUNCH1);
			if(($CHR_TYP eq "DEBUG") || ($CHR_TYP eq "RESP-A1") || ($CHR_TYP eq "RESP-C1")){
				if(($ok==1) || ($ok==2)){
					open(PUNCH2,"<punch2_m$NM");
					foreach(<PUNCH2>){
						if(/\s+\d+\s+\d+\s+(\-\d+|\d+)\.\d+\s+/ig){
							($chr)=(split(' '))[3];
							if(($chr =~ /\*+/) || ($chr =~ "nan")) { $ok=0; } # FyD March 2009
							elsif(($chr == 0) && ($ok!=0)){ $ok=2; }
						}
					}
					close(PUNCH2);
				}
			}
		}else { $ok=0 };
		if($verifimr[$NM] == 2){
			if (-e "punch1_m$NM.sm") {
				open(PUNCH1_IMR,"<punch1_m$NM.sm");
				foreach(<PUNCH1_IMR>){
					if(/\s+\d+\s+\d+\s+(\-\d+|\d+)\.\d+\s+/ig){
						($chr)=(split(' '))[3];
						if(($chr=~/\*+/) || ($chr=~"nan")) { $ok=0; } # FyD March 2009
						elsif(($chr == 0) && ($ok!=0)){ $ok=2; }
					}
				}
				close(PUNCH1_IMR);
				if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")){
					if(($ok==1) || ($ok==2)){
						open(PUNCH2_IMR,"<punch2_m$NM.sm");
						foreach(<PUNCH2_IMR>){
							if(/\s+\d+\s+\d+\s+(\-\d+|\d+)\.\d+\s+/ig){
								($chr)=(split(' '))[3];
								if(($chr=~/\*+/) || ($chr=~"nan")) { $ok=0; } # FyD March 2009
								elsif(($chr==0) && ($ok!=0)){ $ok=2; }
							}
						}
						close(PUNCH2_IMR);
					}
				}
			}else { $ok=0 };
		}
		if($ok==2){ # FyD March 2009
			if(($CHR_TYP eq "DEBUG") || ($CHR_TYP eq "RESP-A1") || ($CHR_TYP eq "RESP-C1") || ($CHR_TYP eq "ESP-A2") || ($CHR_TYP eq "ESP-C2")){
				print "\t\t[ WARNING ]\n\tAt least one charge value equals zero!\n\tSee the \"punch2_m$NM\" ";
				if($verifimr[$NM] == 2){ print "and the \"punch2_m$NM.sm\" "; }
			}else{	print "\t\t[ WARNING ]\n\tAt least one charge value equals zero!\n\tSee the \"punch1_m$NM\" ";
				if($verifimr[$NM] == 2){ print "and the \"punch1_m$NM.sm\" "; }
			}
			print "file(s)";
		}
		elsif($ok==1){
			if(($CHR_TYP eq "DEBUG") || ($CHR_TYP eq "RESP-A1") || ($CHR_TYP eq "RESP-C1") || ($CHR_TYP eq "ESP-A2") || ($CHR_TYP eq "ESP-C2")){
				print "\t\t[ OK ]\n\tSee the \"punch2_m$NM\" ";
				if($verifimr[$NM] == 2){ print "and the \"punch2_m$NM.sm\" "; }
			}else{	print "\t\t[ OK ]\n\tSee the \"punch1_m$NM\" ";
				if($verifimr[$NM] == 2){ print "and the \"punch1_m$NM.sm\" "; }
			}
			print "file(s)";
		}else {
			if(($CHR_TYP eq "DEBUG") || ($CHR_TYP eq "RESP-A1") || ($CHR_TYP eq "RESP-C1")){
				print "\t\t[ FAILED ]\n\tSee the \"output(1|2)_m$NM\" ";
				if($verifimr[$NM] == 2){ print "and the \"output(1|2)_m$NM.sm\" "; }
			}else{	print "\t\t[ FAILED ]\n\tSee the \"output1_m$NM\" ";
				if($verifimr[$NM] == 2){ print "and the \"output1_m$NM.sm\" "; }
			}
			print "file(s)\n\n"; $check=0; Information();
			if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
		}
		if($nbconect[$NM]>0){						#------ mol2 file is generated ------
			if($atombrut[$NM]==1){
format MOL2bis =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.#### ****
$i,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$residu[$i-1][$NM],$tab[4][$i-1][$NM],$potelect
.
			}else{
format MOL2 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.#### ****
$i,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$residu[$i-1][$NM],$tab[4][$i-1][$NM],$potelect
.
			}
			
#******************************RED-2012******************************	
				if($atombrut[$NM] == 1){	
format MOL2bis_cc6 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.###### ****
$i,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$residu[$i-1][$NM],$tab[4][$i-1][$NM],$potelect
.
				}else{
format MOL2_cc6 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.###### ****
$i,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$residu[$i-1][$NM],$tab[4][$i-1][$NM],$potelect
.
				}
				
				if($atombrut[$NM] == 1){	
format MOL2bis_cc5 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.##### ****
$i,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$residu[$i-1][$NM],$tab[4][$i-1][$NM],$potelect
.
				}else{
format MOL2_cc5 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.##### ****
$i,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$residu[$i-1][$NM],$tab[4][$i-1][$NM],$potelect
.
				}
								
				if($atombrut[$NM] == 1){	
format MOL2bis_cc3 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.### ****
$i,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$residu[$i-1][$NM],$tab[4][$i-1][$NM],$potelect
.
				}else{
format MOL2_cc3 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.### ****
$i,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$residu[$i-1][$NM],$tab[4][$i-1][$NM],$potelect
.
				}
				
				if($atombrut[$NM] == 1){	
format MOL2bis_cc2 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.## ****
$i,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$residu[$i-1][$NM],$tab[4][$i-1][$NM],$potelect
.
				}else{
format MOL2_cc2 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.## ****
$i,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$residu[$i-1][$NM],$tab[4][$i-1][$NM],$potelect
.
				}
				
				if($atombrut[$NM] == 1){	
format MOL2bis_cc1 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.# ****
$i,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$residu[$i-1][$NM],$tab[4][$i-1][$NM],$potelect
.
				}else{
format MOL2_cc1 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.# ****
$i,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$residu[$i-1][$NM],$tab[4][$i-1][$NM],$potelect
.
				}
#******************************RED-2012******************************
			
			$namecount=0;
			$molname=$tab[4][1][$NM];
			for($i=1; $i<$nbatoms[$NM]; $i++){
					if($residu[$i-1][$NM] != $residu[$i][$NM]){
						$nomtemp=$tab[4][$i][$NM];
						$molname=$molname."-".$nomtemp;
						$namecount++;
					}
				}
				
			#******************************RED-2012******************************	
			if($COR_CHR==6){
				if($atombrut[$NM] == 1){format_name MOL2_FILE "MOL2bis_cc6";}
				else{format_name MOL2_FILE "MOL2_cc6";}				
			}elsif($COR_CHR==5){
				if($atombrut[$NM] == 1){format_name MOL2_FILE "MOL2bis_cc5";}
				else{format_name MOL2_FILE "MOL2_cc5";}					
			}elsif($COR_CHR==3){
				if($atombrut[$NM] == 1){format_name MOL2_FILE "MOL2bis_cc3";}
				else{format_name MOL2_FILE "MOL2_cc3";}				
			}elsif($COR_CHR==2){
				if($atombrut[$NM] == 1){format_name MOL2_FILE "MOL2bis_cc2";}
				else{format_name MOL2_FILE "MOL2_cc2";}				
			}elsif($COR_CHR==1){
				if($atombrut[$NM] == 1){format_name MOL2_FILE "MOL2bis_cc1";}
				else{format_name MOL2_FILE "MOL2_cc1";}	
			}else{
			#******************************RED-2012******************************
				
				if($atombrut[$NM] == 1){format_name MOL2_FILE "MOL2bis";}
				else{format_name MOL2_FILE "MOL2";}	
			
			#******************************RED-2012******************************	
			}	
			#******************************RED-2012******************************
			
			for($NC=0; $NC<$nbconf[$NM]; $NC++){
				$NC++;
				open (MOL2_FILE, ">Mol_m$NM-o$NC.mol2");
				$NC--;
				if($namecount==0){ printf MOL2_FILE ("@<TRIPOS>MOLECULE\n%s\n",$tab[4][1][$NM]);
				}else{	printf MOL2_FILE ("@<TRIPOS>MOLECULE\n%s\n",$molname);}
				printf MOL2_FILE ("%5d %5d %5d     0     1\n",$nbatoms[$NM],$nbconect[$NM],$nbresi[$NM]);
				printf MOL2_FILE ("SMALL\nUSER_CHARGES\n@<TRIPOS>ATOM\n");
				$flag=$i=0;
				if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")){
					open (PCH_FILE, "<punch2_m$NM");
					foreach(<PCH_FILE>){
						if(/    NO   At\.No\.    q0           q\(opt\)   IVARY  d\(rstr\)\/dq/ig) { $flag=1; }
						if($flag==1){ $i++; }
						if(($i>=2) && ($i<=$nbatoms[$NM]+2)){
							$k=$i+($nbatoms[$NM]*$nbmod[$NM]*$NC);
							($average[$k-2][$NM])=(split(' '))[3];
						}
					}
					close(PCH_FILE);
				}
				if(($CHR_TYP eq "ESP-A1")||($CHR_TYP eq "ESP-C1")||($CHR_TYP eq "RESP-A2")||($CHR_TYP eq "RESP-C2")){
					open (PCH_FILE, "<punch1_m$NM");
					foreach(<PCH_FILE>){
						if(/    NO   At\.No\.    q0           q\(opt\)   IVARY  d\(rstr\)\/dq/ig){ $flag=1; }
						if($flag == 1){		$i++;	}
						if(($i>=2) && ($i<=$nbatoms[$NM]+2)){
							$k=$i+($nbatoms[$NM]*$nbmod[$NM]*$NC);
							($average[$k-2][$NM])=(split(' '))[3];
						}
					}
					close(PCH_FILE);
				}
				
				#******************************RED-2012******************************
				my $right_charge=0;
				if($COR_CHR==6||$COR_CHR==5||$COR_CHR==4||$COR_CHR==3||$COR_CHR==2||$COR_CHR==1){
					$right_charge=1;
				}
				if ( $right_charge == 1 ) {
					our @charges=();
					our @atoms_charge_edit=();
					my @charges_back=();
					my @charges_origin=();
					my $total_charge=0;
					my $i=0;	
					for(my $j=0; $j<$nbatoms[$NM]; $j++){
						my $charge=$average[$i][$NM];
						$i++;						
						my $charge_round=nearest( .0001, $charge);
						if($COR_CHR==6){
							$charge_round=nearest( .000001, $charge);
						}elsif($COR_CHR==5){
							$charge_round=nearest( .00001, $charge);
						}elsif($COR_CHR==4){
							$charge_round=nearest( .0001, $charge);
						}elsif($COR_CHR==3){
							$charge_round=nearest( .001, $charge);
						}elsif($COR_CHR==2){
							$charge_round=nearest( .01, $charge);
						}elsif($COR_CHR==1){
							$charge_round=nearest( .1, $charge);
						}							
						$total_charge=$total_charge+$charge_round;
						push(@charges,$charge_round);
						push(@charges_back,$charge_round);
						push(@charges_origin,$charge);						
					}
					my @name_atoms=();
					my @atoms_others=();
					for(my $i=0; $i<$nbatoms[$NM]; $i++){
						push(@atoms_others,$i);
						push(@name_atoms,$tab[0][$i][$NM]);
					}							
					my $errors=nearest( .0001,abs($CHR_VAL[$NM]-$total_charge))*10000;
					if($COR_CHR==6){
						$errors=nearest( .000001,abs($CHR_VAL[$NM]-$total_charge))*1000000;
					}elsif($COR_CHR==5){
						$errors=nearest( .00001,abs($CHR_VAL[$NM]-$total_charge))*100000;
					}elsif($COR_CHR==4){
						$errors=nearest( .0001,abs($CHR_VAL[$NM]-$total_charge))*10000;
					}elsif($COR_CHR==3){
						$errors=nearest( .001,abs($CHR_VAL[$NM]-$total_charge))*1000;
					}elsif($COR_CHR==2){
						$errors=nearest( .01,abs($CHR_VAL[$NM]-$total_charge))*100;
					}elsif($COR_CHR==1){
						$errors=nearest( .1,abs($CHR_VAL[$NM]-$total_charge))*10;
					}	
						
					our $GLOBAL_CHARGE_times         = 0;
					our $GLOBAL_CHARGE_exist_groupe  = 0;
					our @GLOBAL_CHARGE_result_branch = ();
					our @GLOBAL_CHARGE_results       = ();		
					our @GLOBAL_atoms         = ();
					our $GLOBAL_add_round=0;
					if($errors>0){					
						my $re_groupes = groupes(\@name_atoms,$errors);						
						my @valeur_groupes       = @{ $re_groupes->[0] };
						my @nb_groupes           = @{ $re_groupes->[1] };
						my @exist_groupe         = ();
						my $count_valeur_groupes = scalar @valeur_groupes;
						for ( my $i = 0 ; $i < $count_valeur_groupes ; $i++ ) {
							my @nb_groupe       = @{ $nb_groupes[$i] };
							my $count_nb_groupe = scalar @nb_groupe;
							push( @exist_groupe, [ $valeur_groupes[$i], $count_nb_groupe ] );
						}												
						exist_split( $errors, \@exist_groupe, 0, [] );
						my $count_result_branch = scalar @GLOBAL_CHARGE_result_branch;
						if ( $count_result_branch > 0 ) {
							get_result( \@GLOBAL_CHARGE_result_branch );
							if($GLOBAL_CHARGE_result_branch[0][0]!=0){
								unshift( @GLOBAL_CHARGE_results, $GLOBAL_CHARGE_result_branch[0][1] - $GLOBAL_CHARGE_result_branch[0][0] );
							}
						}						
						my @groupes_atom   = ();
						my @tmp_nb_groupes = @nb_groupes;
						foreach my $element (@GLOBAL_CHARGE_results) {
							for ( my $i = 0 ; $i < $count_valeur_groupes ; $i++ ) {
								if ( $element == $valeur_groupes[$i] ) {
									my @nb_groupe = @{ $tmp_nb_groupes[$i] };
									push( @groupes_atom, $nb_groupe[0] );
									shift(@nb_groupe);
									$tmp_nb_groupes[$i] = \@nb_groupe;
								}
							}
						}										
						my @atoms_groupes = @{ $re_groupes->[2] };						
						foreach my $element (@groupes_atom) {
							push( @GLOBAL_atoms, @{ $atoms_groupes[$element] } );
						}
						@GLOBAL_atoms = sort { $a <=> $b } @GLOBAL_atoms;	
						if($CHR_VAL[$NM]-$total_charge>0){
							$GLOBAL_add_round=0.0001;
							if($COR_CHR==6){
								$GLOBAL_add_round=0.000001;
							}elsif($COR_CHR==5){
								$GLOBAL_add_round=0.00001;
							}elsif($COR_CHR==4){
								$GLOBAL_add_round=0.0001;
							}elsif($COR_CHR==3){
								$GLOBAL_add_round=0.001;
							}elsif($COR_CHR==2){
								$GLOBAL_add_round=0.01;
							}elsif($COR_CHR==1){
								$GLOBAL_add_round=0.1;
							}	
						}else{
							$GLOBAL_add_round=-0.0001;
							if($COR_CHR==6){
								$GLOBAL_add_round=-0.000001;
							}elsif($COR_CHR==5){
								$GLOBAL_add_round=-0.00001;
							}elsif($COR_CHR==4){
								$GLOBAL_add_round=-0.0001;
							}elsif($COR_CHR==3){
								$GLOBAL_add_round=-0.001;
							}elsif($COR_CHR==2){
								$GLOBAL_add_round=-0.01;
							}elsif($COR_CHR==1){
								$GLOBAL_add_round=-0.1;
							}	
						}						
						foreach my $numero_atom (@GLOBAL_atoms){
							my $nb_atom=$atoms_others[$numero_atom];
							$charges[$nb_atom]=$charges[$nb_atom]+$GLOBAL_add_round;
							push(@atoms_charge_edit,$nb_atom);
						}	
						my $count_GLOBAL_atoms=scalar @GLOBAL_atoms;
						if($count_GLOBAL_atoms==0){							
							my $NC_1=$NC+1;print "\n\t\t\t         WARNING:\n\tMol_m$NM-o$NC_1.mol2 Charge correction not successful\n";	
						}
					}
					
					format CHARGESLOG_M_cc6 =
@## @<<<      @##.###### @##.###### @##.###### @< 
$icharge+1,$tab[0][$icharge][$NM],$charges_origin[$icharge],$charges_back[$icharge],$charges[$icharge],$mark_round
.
					format CHARGESLOG_M_cc5 =
@## @<<<      @##.###### @##.##### @##.##### @< 
$icharge+1,$tab[0][$icharge][$NM],$charges_origin[$icharge],$charges_back[$icharge],$charges[$icharge],$mark_round
.
					format CHARGESLOG_M_cc4 =
@## @<<<      @##.###### @##.#### @##.#### @< 
$icharge+1,$tab[0][$icharge][$NM],$charges_origin[$icharge],$charges_back[$icharge],$charges[$icharge],$mark_round
.
					format CHARGESLOG_M_cc3 =
@## @<<<      @##.###### @##.### @##.### @< 
$icharge+1,$tab[0][$icharge][$NM],$charges_origin[$icharge],$charges_back[$icharge],$charges[$icharge],$mark_round
.
					format CHARGESLOG_M_cc2 =
@## @<<<      @##.###### @##.## @##.## @< 
$icharge+1,$tab[0][$icharge][$NM],$charges_origin[$icharge],$charges_back[$icharge],$charges[$icharge],$mark_round
.
					format CHARGESLOG_M_cc1 =
@## @<<<      @##.###### @##.# @##.# @< 
$icharge+1,$tab[0][$icharge][$NM],$charges_origin[$icharge],$charges_back[$icharge],$charges[$icharge],$mark_round
.
									
					if($COR_CHR==6){
						format_name CHARGESLOG_M_FILE "CHARGESLOG_M_cc6";
					}elsif($COR_CHR==5){
						format_name CHARGESLOG_M_FILE "CHARGESLOG_M_cc5";
					}elsif($COR_CHR==4){
						format_name CHARGESLOG_M_FILE "CHARGESLOG_M_cc4";
					}elsif($COR_CHR==3){
						format_name CHARGESLOG_M_FILE "CHARGESLOG_M_cc3";
					}elsif($COR_CHR==2){
						format_name CHARGESLOG_M_FILE "CHARGESLOG_M_cc2";
					}elsif($COR_CHR==1){
						format_name CHARGESLOG_M_FILE "CHARGESLOG_M_cc1";
					}	
					open (CHARGESLOG_M_FILE, ">Mol_m$NM.CHARGES.log");
					printf CHARGESLOG_M_FILE "MOLECULE $NM - $TITLE[$NM]\n";
					for($icharge=0; $icharge<$nbatoms[$NM]; $icharge++){
						$mark_round="";
						if($charges_back[$icharge]!=$charges[$icharge]){
							$mark_round="!";
						}
						write CHARGESLOG_M_FILE;
					}
					close (CHARGESLOG_M_FILE);		
				
				}
				#******************************RED-2012******************************
				
				$i=0;
				for($j=0; $j<$nbatoms[$NM]; $j++){
					$atom=$tab[1][$i][$NM];
					if( ($tab[1][$i][$NM] =~ /T$/) ){ $atom=~s/T//; }
					$potelect=$average[$i][$NM];
					$i++;
					$element=$atom;
					$atom="$atom"."$i";
					
					#******************************RED-2012******************************
						if($right_charge==1){
							my $same=0;
							foreach my $numero_atom (@atoms_charge_edit){
								if($j==$numero_atom){
									$potelect=$charges[$numero_atom];
									$same=1;
								}							
							}
							if($same==0){
								my $potelect_round=nearest(.0001,$potelect);
								my $round=$potelect_round-$potelect;
								my $round_5=abs(abs($round)-0.00005);
								my $round_add=0.000001;
								if($COR_CHR==6){
									$potelect_round=nearest(.0001,$potelect);
									$round=$potelect_round-$potelect;
									$round_5=abs(abs($round)-0.00005);
									$round_add=0.000001;
								}elsif($COR_CHR==5){
									$potelect_round=nearest(.00001,$potelect);
									$round=$potelect_round-$potelect;
									$round_5=abs(abs($round)-0.000005);
									$round_add=0.0000001;
								}elsif($COR_CHR==4){
									$potelect_round=nearest(.0001,$potelect);
									$round=$potelect_round-$potelect;
									$round_5=abs(abs($round)-0.00005);
									$round_add=0.000001;
								}elsif($COR_CHR==3){
									$potelect_round=nearest(.001,$potelect);
									$round=$potelect_round-$potelect;
									$round_5=abs(abs($round)-0.0005);
									$round_add=0.00001;
								}elsif($COR_CHR==2){
									$potelect_round=nearest(.01,$potelect);
									$round=$potelect_round-$potelect;
									$round_5=abs(abs($round)-0.005);
									$round_add=0.0001;
								}elsif($COR_CHR==1){
									$potelect_round=nearest(.1,$potelect);
									$round=$potelect_round-$potelect;
									$round_5=abs(abs($round)-0.05);
									$round_add=0.001;
								}	
								if($round_5<0.00000000001){
									if($round>0){
										$potelect=$potelect+$round_add;
									}else{
										$potelect=$potelect-$round_add;
									}
								}
							}
						}
						#******************************RED-2012******************************
					
					write MOL2_FILE;	
				}
				printf MOL2_FILE ("@<TRIPOS>BOND\n");
				for($i=0; $i<$nbconect[$NM]; $i++){
					($at1,$at2)=(split(/\-/,$conections[$i][$NM]));  
					printf MOL2_FILE ("%5d %5d %5d 1\n",$i+1,$at1,$at2);
				}
				printf MOL2_FILE ("@<TRIPOS>SUBSTRUCTURE\n");
				printf MOL2_FILE (" %6d %4s         %6d ****               0 ****  ****  \n",1,$tab[4][0][$NM],1);
				for($i=1; $i<$nbatoms[$NM]; $i++){
					if(($residu[$i-1][$NM] != $residu[$i][$NM]) || ($tab[4][$i-1][$NM] ne $tab[4][$i][$NM])){
						printf MOL2_FILE (" %6d %4s         %6d ****               0 ****  ****  \n",$residu[$i][$NM],$tab[4][$i][$NM],$i+1);
					}
				}
				print MOL2_FILE "\n\n";
				close (MOL2_FILE);
			}
			print "\n\n\tThe following Tripos mol2 file(s) has/have been created.\n";
			for ($NC=1; $NC<=$nbconf[$NM]; $NC++){ print "\tMol_m$NM-o$NC.mol2"; }
			if(-e "input1_m$NM.sm"){ print "\n"; }
		}
		if(($nbconect[$NM]>0) && ($verifimr[$NM]==2)){
			if($atombrut[$NM] == 1){
format MOL2imrbis =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.#### ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
			}else{
format MOL2imr =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.#### ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
			}
			
			#******************************RED-2012******************************
			
			if($atombrut[$NM] == 1){
format MOL2imrbis_cc6 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.###### ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
			}else{
format MOL2imr_cc6 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.###### ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
			}
			if($atombrut[$NM] == 1){
format MOL2imrbis_cc5 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.##### ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
			}else{
format MOL2imr_cc5 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.##### ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
			}
			if($atombrut[$NM] == 1){
format MOL2imrbis_cc3 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.### ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
			}else{
format MOL2imr_cc3 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.### ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
			}
			if($atombrut[$NM] == 1){
format MOL2imrbis_cc2 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.## ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
			}else{
format MOL2imr_cc2 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.## ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
			}
			if($atombrut[$NM] == 1){
format MOL2imrbis_cc1 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.# ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
			}else{
format MOL2imr_cc1 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.# ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
			}
						
			
			if($COR_CHR==6){
				if($atombrut[$NM] == 1){ format_name MOL2_FILE_IMR "MOL2imrbis_cc6"; }
				else{ format_name MOL2_FILE_IMR "MOL2imr_cc6"; }
			}elsif($COR_CHR==5){
				if($atombrut[$NM] == 1){ format_name MOL2_FILE_IMR "MOL2imrbis_cc5"; }
				else{ format_name MOL2_FILE_IMR "MOL2imr_cc5"; }
			}elsif($COR_CHR==3){
				if($atombrut[$NM] == 1){ format_name MOL2_FILE_IMR "MOL2imrbis_cc3"; }
				else{ format_name MOL2_FILE_IMR "MOL2imr_cc3"; }
			}elsif($COR_CHR==2){
				if($atombrut[$NM] == 1){ format_name MOL2_FILE_IMR "MOL2imrbis_cc2"; }
				else{ format_name MOL2_FILE_IMR "MOL2imr_cc2"; }
			}elsif($COR_CHR==1){
				if($atombrut[$NM] == 1){ format_name MOL2_FILE_IMR "MOL2imrbis_cc1"; }
				else{ format_name MOL2_FILE_IMR "MOL2imr_cc1"; }
			}else{
			#******************************RED-2012******************************
			
				if($atombrut[$NM] == 1){ format_name MOL2_FILE_IMR "MOL2imrbis"; }
				else{ format_name MOL2_FILE_IMR "MOL2imr"; }
				
			#******************************RED-2012******************************	
			}
			#******************************RED-2012******************************
			
			for($NC=0; $NC<$nbconf[$NM]; $NC++){
				$NC++;
				open (MOL2_FILE_IMR, ">Mol_m$NM-o$NC-sm.mol2");
				$NC--;
				$cmptatoms=$il=$testnom=0;
				$rescpt=1;
				for($i=1; $i<=$nbatoms[$NM]; $i++){
					$testr=0;
					if($i==1){$rescpt=1;}
					for($y=0; $y<=$imrcount[$NM]; $y++){
						if(!defined($intramr[4][$y][$NM])){ $intramr[4][$y][$NM]=0; }
						if(!defined($intramr[3][$y][$NM])){ $intramr[3][$y][$NM]=""; }
						for($w=0;$w<=$intramr[4][$y][$NM];$w++){
							if(!defined($intratom[$w][$y][$NM])){ $intratom[$w][$y][$NM]=0; }
							if(($intratom[$w][$y][$NM]==$i) && ($intramr[3][$y][$NM]!~/[K]/)){ $testr=1; }
						}
					}
					if($testr==1){ $cmptatoms++; }
					if($testr==0){
						$saveres[2][$il][$NM]=$residu[$i-1][$NM];
						$saveres[5][$il][$NM]=$tab[4][$i-1][$NM];
						if($il==0){ $molname2=$saveres[5][$il][$NM]; }
						elsif($il!= 0){
							if($saveres[2][$il-1][$NM] != $saveres[2][$il][$NM]){
								$rescpt++; $testnom=1;
								$molname2=$molname2."-".$saveres[5][$il][$NM];
							}
						}
					$il++;
					}
				}
				$cmptatoms = $nbatoms[$NM]-$cmptatoms;
				$cmptconnect=0;
				for($i=0; $i<$nbconect[$NM]; $i++){
					($at1,$at2)=(split(/\-/,$conections[$i][$NM]));
					$testc2=0;
					for($y=0; $y<$imrcount[$NM]; $y++){
						for($w=0;$w<$intramr[4][$y][$NM];$w++){
							if((($intratom[$w][$y][$NM]==$at1) && ($intramr[3][$y][$NM]!~/[K]/)) || (($intratom[$w][$y][$NM]==$at2) && ($intramr[3][$y][$NM]!~/[K]/))){ $testc2=1; }
						}
					}
					if($testc2 == 1){ $cmptconnect++; }
				}
				$cmptconnect=$nbconect[$NM]-$cmptconnect;
				if($testnom==1){ printf MOL2_FILE_IMR ("@<TRIPOS>MOLECULE\n%s\n",$molname2);
				}else{ printf MOL2_FILE_IMR ("@<TRIPOS>MOLECULE\n%s\n",$saveres[5][0][$NM]); }
				printf MOL2_FILE_IMR ("%5d %5d %5d     0     1\n",$cmptatoms,$cmptconnect,$rescpt);
				printf MOL2_FILE_IMR ("SMALL\nUSER_CHARGES\n@<TRIPOS>ATOM\n");
				$flag=$i=0;
				if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1") || ($CHR_TYP eq "RESP-C1")){
					open (PCH_FILE, "<punch2_m$NM.sm");
					foreach(<PCH_FILE>){
						if(/    NO   At\.No\.    q0           q\(opt\)   IVARY  d\(rstr\)\/dq/ig) { $flag=1; }
						if($flag==1){ $i++; }
						if(($i>=2)&&($i<=$nbatoms[$NM]+2)){
							$k=$i+($nbatoms[$NM]*$nbmod[$NM]*$NC);
							($averageimr[$k-2][$NM])=(split(' '))[3];
						}
					}
					close(PCH_FILE);
				}
				if(($CHR_TYP eq "ESP-A1") || ($CHR_TYP eq "ESP-C1") || ($CHR_TYP eq "RESP-A2") || ($CHR_TYP eq "RESP-C2")){
					open (PCH_FILE, "<punch1_m$NM.sm");
					foreach(<PCH_FILE>){
						if(/    NO   At\.No\.    q0           q\(opt\)   IVARY  d\(rstr\)\/dq/ig){ $flag=1; }
						if($flag == 1){ $i++; }
						if(($i>=2) && ($i<=$nbatoms[$NM]+2)){
							$k=$i+($nbatoms[$NM]*$nbmod[$NM]*$NC);
							($averageimr[$k-2][$NM])=(split(' '))[3];
						}
					}
					close(PCH_FILE);
				}
				
				#******************************RED-2012******************************
				my $right_charge=0;
				if($COR_CHR==6||$COR_CHR==5||$COR_CHR==4||$COR_CHR==3||$COR_CHR==2||$COR_CHR==1){
					$right_charge=1;
				}
				if ( $right_charge == 1 ) {
					our @charges=();
					our @atoms_charge_edit=();
					my @charges_back=();
					my @charges_origin=();
					
					my $i=0;
					for(my $j=0;$j<$nbatoms[$NM];$j++){
						$potelect=$averageimr[$i][$NM];
						$i++;
						$y=$w=$molimr=0;
						for($y=0; $y<=$imrcount[$NM]; $y++){
							if(!defined($intramr[4][$y][$NM])){ $intramr[4][$y][$NM]=0; }
							if(!defined($intramr[3][$y][$NM])){ $intramr[3][$y][$NM]=""; }
							for($w=0;$w<=$intramr[4][$y][$NM];$w++){
								if(!defined($intratom[$w][$y][$NM])){ $intratom[$w][$y][$NM]=0; }
								if(($intratom[$w][$y][$NM]==$i) && ($intramr[3][$y][$NM]!~/[K]/)){ $molimr = 1; }
							}
						}												
						my $charge_round=nearest( .0001, $potelect);
						if($COR_CHR==6){
							$charge_round=nearest( .000001, $potelect);
						}elsif($COR_CHR==5){
							$charge_round=nearest( .00001, $potelect);
						}elsif($COR_CHR==4){
							$charge_round=nearest( .0001, $potelect);
						}elsif($COR_CHR==3){
							$charge_round=nearest( .001, $potelect);
						}elsif($COR_CHR==2){
							$charge_round=nearest( .01, $potelect);
						}elsif($COR_CHR==1){
							$charge_round=nearest( .1, $potelect);
						}	
						push(@charges,$charge_round);
						push(@charges_back,$charge_round);
						push(@charges_origin,$potelect);
						#intra mcc "keep" no 
						#if($molimr == 0){
							#$total_charge=$total_charge+$charge_round;
						#}	
					}								
					
					my @all_atoms_intra=();
					my $total_charge_intra=0;
					foreach my $intra_mcc(@GLOBAL_intra_mcc){
						my $mol=$intra_mcc->[0];
						if($mol==$NM){
							my $charge_intra=$intra_mcc->[1];
							$total_charge_intra=$total_charge_intra+$charge_intra;	
							my @atoms_intra=@{$intra_mcc->[2]};
							my $total_charges_intra=0;
							my $string_intra='';
							foreach my $atom (@atoms_intra){
								push(@all_atoms_intra,$atom);
								$total_charges_intra=$total_charges_intra+$charges[$atom-1];
								$string_intra=$string_intra." ".$atom;
							}
							my $errors=nearest( .0001,abs($charge_intra-$total_charges_intra))*10000;
														
							if($COR_CHR==6){
								$errors=nearest( .000001,abs($charge_intra-$total_charges_intra))*1000000;
							}elsif($COR_CHR==5){
								$errors=nearest( .00001,abs($charge_intra-$total_charges_intra))*100000;
							}elsif($COR_CHR==4){
								$errors=nearest( .0001,abs($charge_intra-$total_charges_intra))*10000;
							}elsif($COR_CHR==3){
								$errors=nearest( .001,abs($charge_intra-$total_charges_intra))*1000;
							}elsif($COR_CHR==2){
								$errors=nearest( .01,abs($charge_intra-$total_charges_intra))*100;
							}elsif($COR_CHR==1){
								$errors=nearest( .1,abs($charge_intra-$total_charges_intra))*10;
							}	
							
							our $GLOBAL_CHARGE_times         = 0;
							our $GLOBAL_CHARGE_exist_groupe  = 0;
							our @GLOBAL_CHARGE_result_branch = ();
							our @GLOBAL_CHARGE_results       = ();	
							our @GLOBAL_atoms         = ();
							our $GLOBAL_add_round=0;
							
							if($errors>0){									
								my @name_atoms=();
								foreach my $atom (@atoms_intra){
									push(@name_atoms,$tab[0][$atom-1][$mol]);	
								}		
											
								my $re_groupes = groupes(\@name_atoms,$errors);					
								my @valeur_groupes       = @{ $re_groupes->[0] };
								my @nb_groupes           = @{ $re_groupes->[1] };
								my @exist_groupe         = ();
								my $count_valeur_groupes = scalar @valeur_groupes;
								for ( my $i = 0 ; $i < $count_valeur_groupes ; $i++ ) {
									my @nb_groupe       = @{ $nb_groupes[$i] };
									my $count_nb_groupe = scalar @nb_groupe;
									push( @exist_groupe, [ $valeur_groupes[$i], $count_nb_groupe ] );
								}
								exist_split( $errors, \@exist_groupe, 0, [] );					
								my $count_result_branch = scalar @GLOBAL_CHARGE_result_branch;
								if ( $count_result_branch > 0 ) {
									get_result( \@GLOBAL_CHARGE_result_branch );
									if($GLOBAL_CHARGE_result_branch[0][0]!=0){
										unshift( @GLOBAL_CHARGE_results, $GLOBAL_CHARGE_result_branch[0][1] - $GLOBAL_CHARGE_result_branch[0][0] );
									}
								}					
								my @groupes_atom   = ();
								my @tmp_nb_groupes = @nb_groupes;
								foreach my $element (@GLOBAL_CHARGE_results) {
									for ( my $i = 0 ; $i < $count_valeur_groupes ; $i++ ) {
										if ( $element == $valeur_groupes[$i] ) {
											my @nb_groupe = @{ $tmp_nb_groupes[$i] };
											push( @groupes_atom, $nb_groupe[0] );
											shift(@nb_groupe);
											$tmp_nb_groupes[$i] = \@nb_groupe;
										}
									}
								}					
								my @atoms_groupes = @{ $re_groupes->[2] };
						
								foreach my $element (@groupes_atom) {
									push( @GLOBAL_atoms, @{ $atoms_groupes[$element] } );
								}		
								@GLOBAL_atoms = sort { $a <=> $b } @GLOBAL_atoms;				
						
								if($charge_intra-$total_charges_intra>0){
									$GLOBAL_add_round=0.0001;
									if($COR_CHR==6){
										$GLOBAL_add_round=0.000001;
									}elsif($COR_CHR==5){
										$GLOBAL_add_round=0.00001;
									}elsif($COR_CHR==4){
										$GLOBAL_add_round=0.0001;
									}elsif($COR_CHR==3){
										$GLOBAL_add_round=0.001;
									}elsif($COR_CHR==2){
										$GLOBAL_add_round=0.01;
									}elsif($COR_CHR==1){
										$GLOBAL_add_round=0.1;
									}	
								}else{
									$GLOBAL_add_round=-0.0001;
									if($COR_CHR==6){
										$GLOBAL_add_round=-0.000001;
									}elsif($COR_CHR==5){
										$GLOBAL_add_round=-0.00001;
									}elsif($COR_CHR==4){
										$GLOBAL_add_round=-0.0001;
									}elsif($COR_CHR==3){
										$GLOBAL_add_round=-0.001;
									}elsif($COR_CHR==2){
										$GLOBAL_add_round=-0.01;
									}elsif($COR_CHR==1){
										$GLOBAL_add_round=-0.1;
									}	
								}					
								foreach my $numero_atom (@GLOBAL_atoms){
									my $nb_atom=$atoms_intra[$numero_atom]-1;
									$charges[$nb_atom]=$charges[$nb_atom]+$GLOBAL_add_round;
									push(@atoms_charge_edit,$nb_atom);
								}
								my $count_GLOBAL_atoms=scalar @GLOBAL_atoms;
								if($count_GLOBAL_atoms==0){
									print "\n\t\t\t         WARNING:\n\tMolecule $mol INTRA-MCC $string_intra Charge correction not successful\n";	
								}					
							}
						}		
					}

					my $total_charge=0;
					for(my $i=0; $i<$nbatoms[$NM]; $i++){
							my $same=0;
							foreach my $atom_intra(@all_atoms_intra){
								if($i==$atom_intra-1){
									$same=1;
								}		
							}
							if($same==0){
								$total_charge=$total_charge+$charges[$i];
							}
						}						
					
					my $errors=nearest( .0001,abs($CHR_VAL[$NM]-$total_charge_intra-$total_charge))*10000;
					if($COR_CHR==6){
						$errors=nearest( .000001,abs($CHR_VAL[$NM]-$total_charge_intra-$total_charge))*1000000;
					}elsif($COR_CHR==5){
						$errors=nearest( .00001,abs($CHR_VAL[$NM]-$total_charge_intra-$total_charge))*100000;
					}elsif($COR_CHR==4){
						$errors=nearest( .0001,abs($CHR_VAL[$NM]-$total_charge_intra-$total_charge))*10000;
					}elsif($COR_CHR==3){
						$errors=nearest( .001,abs($CHR_VAL[$NM]-$total_charge_intra-$total_charge))*1000;
					}elsif($COR_CHR==2){
						$errors=nearest( .01,abs($CHR_VAL[$NM]-$total_charge_intra-$total_charge))*100;
					}elsif($COR_CHR==1){
						$errors=nearest( .1,abs($CHR_VAL[$NM]-$total_charge_intra-$total_charge))*10;
					}
						
					our $GLOBAL_CHARGE_times         = 0;
					our $GLOBAL_CHARGE_exist_groupe  = 0;
					our @GLOBAL_CHARGE_result_branch = ();
					our @GLOBAL_CHARGE_results       = ();		
					our @GLOBAL_atoms         = ();
					our $GLOBAL_add_round=0;
					
					if($errors>0){		
						my @name_atoms=();
						my @atoms_others=();
						for(my $i=0; $i<$nbatoms[$NM]; $i++){
							my $same=0;
							foreach my $atom_intra(@all_atoms_intra){
								if($i==$atom_intra-1){
									$same=1;
								}		
							}
							if($same==0){
								push(@atoms_others,$i);
								push(@name_atoms,$tab[0][$i][$NM]);
							}
						}			
						my $re_groupes = groupes(\@name_atoms,$errors);						
						my @valeur_groupes       = @{ $re_groupes->[0] };
						my @nb_groupes           = @{ $re_groupes->[1] };
						my @exist_groupe         = ();
						my $count_valeur_groupes = scalar @valeur_groupes;
						for ( my $i = 0 ; $i < $count_valeur_groupes ; $i++ ) {
							my @nb_groupe       = @{ $nb_groupes[$i] };
							my $count_nb_groupe = scalar @nb_groupe;
							push( @exist_groupe, [ $valeur_groupes[$i], $count_nb_groupe ] );
						}												
						exist_split( $errors, \@exist_groupe, 0, [] );
						my $count_result_branch = scalar @GLOBAL_CHARGE_result_branch;
						if ( $count_result_branch > 0 ) {
							get_result( \@GLOBAL_CHARGE_result_branch );
							if($GLOBAL_CHARGE_result_branch[0][0]!=0){
								unshift( @GLOBAL_CHARGE_results, $GLOBAL_CHARGE_result_branch[0][1] - $GLOBAL_CHARGE_result_branch[0][0] );
							}
						}						
						my @groupes_atom   = ();
						my @tmp_nb_groupes = @nb_groupes;
						foreach my $element (@GLOBAL_CHARGE_results) {
							for ( my $i = 0 ; $i < $count_valeur_groupes ; $i++ ) {
								if ( $element == $valeur_groupes[$i] ) {
									my @nb_groupe = @{ $tmp_nb_groupes[$i] };
									push( @groupes_atom, $nb_groupe[0] );
									shift(@nb_groupe);
									$tmp_nb_groupes[$i] = \@nb_groupe;
								}
							}
						}					
						my @atoms_groupes = @{ $re_groupes->[2] };					
						foreach my $element (@groupes_atom) {
							push( @GLOBAL_atoms, @{ $atoms_groupes[$element] } );
						}
						@GLOBAL_atoms = sort { $a <=> $b } @GLOBAL_atoms;	
						if($CHR_VAL[$NM]-$total_charge_intra-$total_charge>0){
							$GLOBAL_add_round=0.0001;
							if($COR_CHR==6){
								$GLOBAL_add_round=0.000001;
							}elsif($COR_CHR==5){
								$GLOBAL_add_round=0.00001;
							}elsif($COR_CHR==4){
								$GLOBAL_add_round=0.0001;
							}elsif($COR_CHR==3){
								$GLOBAL_add_round=0.001;
							}elsif($COR_CHR==2){
								$GLOBAL_add_round=0.01;
							}elsif($COR_CHR==1){
								$GLOBAL_add_round=0.1;
							}	
						}else{
							$GLOBAL_add_round=-0.0001;
							if($COR_CHR==6){
								$GLOBAL_add_round=-0.000001;
							}elsif($COR_CHR==5){
								$GLOBAL_add_round=-0.00001;
							}elsif($COR_CHR==4){
								$GLOBAL_add_round=-0.0001;
							}elsif($COR_CHR==3){
								$GLOBAL_add_round=-0.001;
							}elsif($COR_CHR==2){
								$GLOBAL_add_round=-0.01;
							}elsif($COR_CHR==1){
								$GLOBAL_add_round=-0.1;
							}	
						}						
						foreach my $numero_atom (@GLOBAL_atoms){
							my $nb_atom=$atoms_others[$numero_atom];
							$charges[$nb_atom]=$charges[$nb_atom]+$GLOBAL_add_round;
							push(@atoms_charge_edit,$nb_atom);
						}	
						my $count_GLOBAL_atoms=scalar @GLOBAL_atoms;
						if($count_GLOBAL_atoms==0){
							my $NC_1=$NC+1;print "\n\t\t\t         WARNING:\n\tMol_m$NM-o$NC_1-sm.mol2 Charge correction not successful\n";	
						}			
					}									
									
					format CHARGESLOG_SM_cc6 =
@## @<<<      @##.###### @##.###### @##.###### @<
$icharge+1,$tab[0][$icharge][$NM],$charges_origin[$icharge],$charges_back[$icharge],$charges[$icharge],$mark_round
.
					format CHARGESLOG_SM_cc5 =
@## @<<<      @##.###### @##.##### @##.##### @<
$icharge+1,$tab[0][$icharge][$NM],$charges_origin[$icharge],$charges_back[$icharge],$charges[$icharge],$mark_round
.
					format CHARGESLOG_SM_cc4 =
@## @<<<      @##.###### @##.#### @##.#### @<
$icharge+1,$tab[0][$icharge][$NM],$charges_origin[$icharge],$charges_back[$icharge],$charges[$icharge],$mark_round
.
					format CHARGESLOG_SM_cc3 =
@## @<<<      @##.###### @##.### @##.### @<
$icharge+1,$tab[0][$icharge][$NM],$charges_origin[$icharge],$charges_back[$icharge],$charges[$icharge],$mark_round
.
					format CHARGESLOG_SM_cc2 =
@## @<<<      @##.###### @##.## @##.## @<
$icharge+1,$tab[0][$icharge][$NM],$charges_origin[$icharge],$charges_back[$icharge],$charges[$icharge],$mark_round
.
					format CHARGESLOG_SM_cc1 =
@## @<<<      @##.###### @##.# @##.# @<
$icharge+1,$tab[0][$icharge][$NM],$charges_origin[$icharge],$charges_back[$icharge],$charges[$icharge],$mark_round
.
					if($COR_CHR==6){
						format_name CHARGESLOG_SM_FILE "CHARGESLOG_SM_cc6";
					}elsif($COR_CHR==5){
						format_name CHARGESLOG_SM_FILE "CHARGESLOG_SM_cc5";
					}elsif($COR_CHR==4){
						format_name CHARGESLOG_SM_FILE "CHARGESLOG_SM_cc4";
					}elsif($COR_CHR==3){
						format_name CHARGESLOG_SM_FILE "CHARGESLOG_SM_cc3";
					}elsif($COR_CHR==2){
						format_name CHARGESLOG_SM_FILE "CHARGESLOG_SM_cc2";
					}elsif($COR_CHR==1){
						format_name CHARGESLOG_SM_FILE "CHARGESLOG_SM_cc1";
					}	
					open (CHARGESLOG_SM_FILE, ">Mol_m$NM.sm.CHARGES.log");
					printf CHARGESLOG_SM_FILE "MOLECULE $NM - $TITLE[$NM]\n";
					for($icharge=0; $icharge<$nbatoms[$NM]; $icharge++){
						$mark_round="";
						if($charges_back[$icharge]!=$charges[$icharge]){
							$mark_round="!";
						}
						write CHARGESLOG_SM_FILE;
					}
					close (CHARGESLOG_SM_FILE);		
						
				}				
				#******************************RED-2012******************************
				
				$i=$in=0; $resmol=$ir=1;
				for($j=0; $j<$nbatoms[$NM]; $j++){
					$atom=$tab[1][$i][$NM];
					if(($tab[1][$i][$NM]=~/T$/) ){ $atom=~s/T//; }
					$potelect=$averageimr[$i][$NM];
					if($j==0){ $resmol=1; }
					$i++;
					$element=$atom;
					$atom="$atom"."$ir";
					$y=$w=$molimr=0;
					for($y=0; $y<=$imrcount[$NM]; $y++){
						if(!defined($intramr[4][$y][$NM])){ $intramr[4][$y][$NM]=0; }
						if(!defined($intramr[3][$y][$NM])){ $intramr[3][$y][$NM]=""; }
						for($w=0;$w<=$intramr[4][$y][$NM];$w++){
							if(!defined($intratom[$w][$y][$NM])){ $intratom[$w][$y][$NM]=0; }
							if(($intratom[$w][$y][$NM]==$i) && ($intramr[3][$y][$NM]!~/[K]/)){ $molimr = 1; }
						}
					}
					if($molimr==0){
						$saveres[1][$in][$NM]=$resmol;
						$saveres[2][$in][$NM]=$residu[$j][$NM];
						$saveres[3][$in][$NM]=$tab[4][$j][$NM];
						if($in!=0){
							if($saveres[2][$in-1][$NM]!=$saveres[2][$in][$NM]){ $resmol++; }
						}
						$ir++; $in++;
						$save[$i]=$in;
						
						#******************************RED-2012******************************
						if($right_charge==1){
							my $same=0;
							foreach my $numero_atom (@atoms_charge_edit){
								if($j==$numero_atom){
									$potelect=$charges[$numero_atom];
									$same=1;
								}							
							}	
							if($same==0){
								my $potelect_round=nearest(.0001,$potelect);
								my $round=$potelect_round-$potelect;
								my $round_5=abs(abs($round)-0.00005);
								my $round_add=0.000001;
								if($COR_CHR==6){
									$potelect_round=nearest(.0001,$potelect);
									$round=$potelect_round-$potelect;
									$round_5=abs(abs($round)-0.00005);
									$round_add=0.000001;
								}elsif($COR_CHR==5){
									$potelect_round=nearest(.00001,$potelect);
									$round=$potelect_round-$potelect;
									$round_5=abs(abs($round)-0.000005);
									$round_add=0.0000001;
								}elsif($COR_CHR==4){
									$potelect_round=nearest(.0001,$potelect);
									$round=$potelect_round-$potelect;
									$round_5=abs(abs($round)-0.00005);
									$round_add=0.000001;
								}elsif($COR_CHR==3){
									$potelect_round=nearest(.001,$potelect);
									$round=$potelect_round-$potelect;
									$round_5=abs(abs($round)-0.0005);
									$round_add=0.00001;
								}elsif($COR_CHR==2){
									$potelect_round=nearest(.01,$potelect);
									$round=$potelect_round-$potelect;
									$round_5=abs(abs($round)-0.005);
									$round_add=0.0001;
								}elsif($COR_CHR==1){
									$potelect_round=nearest(.1,$potelect);
									$round=$potelect_round-$potelect;
									$round_5=abs(abs($round)-0.05);
									$round_add=0.001;
								}	
								if($round_5<0.00000000001){
									if($round>0){
										$potelect=$potelect+$round_add;
									}else{
										$potelect=$potelect-$round_add;
									}
								}
							}
							
						}					
						#******************************RED-2012******************************
						
						write MOL2_FILE_IMR;
					}
				}
				$ic=$i=0;
				printf MOL2_FILE_IMR ("@<TRIPOS>BOND\n");
				for($i=0; $i<$nbconect[$NM]; $i++){
					($at1,$at2)=(split(/\-/,$conections[$i][$NM]));
					$y=$w=$testc=0;
					for($y=0; $y<=$imrcount[$NM]; $y++){
						for($w=0; $w<=$intramr[4][$y][$NM]; $w++){
							if((($intratom[$w][$y][$NM]==$at1) && ($intramr[3][$y][$NM]!~/[K]/)) || (($intratom[$w][$y][$NM]==$at2) && ($intramr[3][$y][$NM]!~/[K]/))){ $testc=1; }
						}
					}
					if($testc==0){ printf MOL2_FILE_IMR ("%5d %5d %5d 1\n",$ic+1,$save[$at1],$save[$at2]); $ic++; }
				}
				printf MOL2_FILE_IMR ("@<TRIPOS>SUBSTRUCTURE\n");
				$z=1;
				for($i=1; $i<$in; $i++){
					if($i==1){
						printf MOL2_FILE_IMR (" %6d %4s         %6d ****               0 ****  ****  \n",1,$saveres[3][$i][$NM],1);
					}elsif($saveres[2][$i-1][$NM]!=$saveres[2][$i][$NM]){
						$z++;
						printf MOL2_FILE_IMR (" %6d %4s         %6d ****               0 ****  ****  \n",$z,$saveres[3][$i][$NM],$i+1);
					}
				}	
				print MOL2_FILE_IMR "\n\n";
				close (MOL2_FILE_IMR);
			}
			print "\t";
			for ($NC=1; $NC<=$nbconf[$NM]; $NC++) { print "Mol_m$NM-o$NC-sm.mol2 "; }
		}
	}
}

#******************************RED-2012******************************
sub groupes {
	my ( $re_liste, $sum ) = @_;
	my @liste = @{$re_liste};

	my @diff_liste = ();
	foreach my $element (@liste) {
		my $same = 0;
		foreach my $diff_element (@diff_liste) {
			if ( $element eq $diff_element ) {
				$same = 1;
				last;
			}
		}
		if ( $same == 0 ) {
			push( @diff_liste, $element );
		}
	}

	my @groupes     = ();
	my $count_liste = scalar @liste;
	foreach my $diff_element (@diff_liste) {
		my @groupe = ();
		for ( my $i = 0 ; $i < $count_liste ; $i++ ) {
			if ( $diff_element eq $liste[$i] ) {
				push( @groupe, $i );
			}
		}
		push( @groupes, \@groupe );
	}

	my @count_groupes = ();
	foreach my $re_groupe (@groupes) {
		my @groupe       = @{$re_groupe};
		my $count_groupe = scalar @groupe;
		push( @count_groupes, $count_groupe );
	}

	my @diff_counts = ();
	foreach my $count_groupe (@count_groupes) {
		my $same = 0;
		foreach my $diff_count (@diff_counts) {
			if ( $count_groupe == $diff_count ) {
				$same = 1;
			}
		}
		if ( $same == 0 ) {
			if ( $count_groupe < $sum || $count_groupe == $sum ) {
				#如果原子团的原子数比误差数还大 就不用考虑了
				push( @diff_counts, $count_groupe );
			}
		}
	}

	@diff_counts = sort { $b <=> $a } @diff_counts;

	my @liste_counts     = ();
	my $nb_count_groupes = scalar @count_groupes;
	foreach my $diff_count (@diff_counts) {
		my @liste_count = ();
		for ( my $i = 0 ; $i < $nb_count_groupes ; $i++ ) {
			if ( $diff_count == $count_groupes[$i] ) {
				push( @liste_count, $i );
			}
		}
		push( @liste_counts, \@liste_count );
	}

	return [ \@diff_counts, \@liste_counts, \@groupes ];
}

sub get_result {
	my ($re_result)  = @_;
	my @result       = @{$re_result};
	my $count_result = scalar @result;
	if ( $count_result > 0 ) {
		if($result[0][0]==0){
			push(@GLOBAL_CHARGE_results, $result[0][1]);
		}else{
			push( @GLOBAL_CHARGE_results, $result[0][0] );
		}
		get_result( $result[0][2] );
	}
}

sub exist_split {
	my ( $re_x, $re_list, $last_x, $re_result ) = @_;
	my $x=int($re_x);
	$GLOBAL_CHARGE_times = $GLOBAL_CHARGE_times + 1;
	if ( $GLOBAL_CHARGE_times < 100 ) {
		if ( $GLOBAL_CHARGE_exist_groupe == 0 ) {
			my @list      = @{$re_list};
			my $long_list = scalar @list;
			my $exist_x   = 0;
			for ( my $i = 0 ; $i < $long_list ; $i++ ) {
				if ( $x == $list[$i][0] ) {
					if ( $list[$i][1] > 0 ) {
						$exist_x = 1;
						last;
					}
				}
			}
			if ( $exist_x == 1 ) {
				$GLOBAL_CHARGE_exist_groupe = 1;
				my @result = ();
				push( @result, [ 0, $x, $re_result ] );
				@GLOBAL_CHARGE_result_branch = @result;
			} else {
				for ( my $i = 1 ; $i < int( $x / 2 ) + 1 ; $i++ ) {
					if ( $GLOBAL_CHARGE_exist_groupe == 0 ) {
						my @result = ();
						push( @result, [ $i, $x+0, $re_result ] );
						my @list_i = ();
						foreach my $re_element (@list) {
							my @element  = @{$re_element};
							my @list_i_e = ();
							foreach my $element_e (@element) {
								push( @list_i_e, $element_e );
							}
							push( @list_i, \@list_i_e );
						}

						my $long_list_i = scalar @list_i;
						my $exist_i     = 0;
						for ( my $j = 0 ; $j < $long_list_i ; $j++ ) {
							if ( $i == $list_i[$j][0] ) {
								if ( $list_i[$j][1] > 0 ) {
									$list_i[$j][1] = $list_i[$j][1] - 1;
									$exist_i = 1;
									last;
								}
							}
						}

						if ( $exist_i == 1 ) {

							my $y      = $x - $i;
							my @list_y = ();
							foreach my $re_element (@list_i) {
								my @element  = @{$re_element};
								my @list_y_e = ();
								foreach my $element_e (@element) {
									push( @list_y_e, $element_e );
								}
								push( @list_y, \@list_y_e );
							}
							my $long_list_y = scalar @list_y;
							my $exist_y     = 0;
							for ( my $j = 0 ; $j < $long_list_y ; $j++ ) {
								if ( $y == $list_y[$j][0] ) {	
									if ( $list_y[$j][1] > 0 ) {
										$list_y[$j][1] = $list_y[$j][1] - 1;
										$exist_y = 1;
										last;
									}
								}
							}
							if ( $exist_y == 1 ) {
								@GLOBAL_CHARGE_result_branch = @result;
								$GLOBAL_CHARGE_exist_groupe  = 1;
								last;
							} else {
								if ( $y > $list_y[0][0] ) {
									exist_split( $y, \@list_y, $x, \@result );
								}
							}
						}
					}
				}
			}
		}
	}
}
#******************************RED-2012******************************

#---------------------------------------------------------------------------------------------------------
#---------------------------------------Inter-molecular calculations--------------------------------------
#---------------------------------------------------------------------------------------------------------
sub getindice{ # Elodie - April 2010 - Beggining permet de récupérer le nombre de connections d'un atome + les atomes connectés
	my ($indice)=@_;
	my @tab=[];
	$nbatome=0;
	$tab[1]=[];
	$tab[0]=0;
	for($i=0; $i<$nbconect[$imrsmol[0][$ri]]; $i++){
		($at1,$at2)=(split(/\-/,$conections[$i][$imrsmol[0][$ri]]));
		if($at1==$indice){ $tab[1][$nbatome]=$at2; $nbatome++; }
		elsif($at2==$indice){ $tab[1][$nbatome]=$at1; $nbatome++; }
	}
	$tab[0]=$nbatome;
	return(@tab);
}
sub travel{	# permet de récupérer une partie (celle qui contient $keepres3) de la molécule 1 / partie = liste d'atomes
	my ($indice)=@_;
	my $i=0;
	my @tab=[];
	if($vu[$indice]==0) {
		$tab3[1][$tab3[0]]=$indice;
		$vu[$indice]=1;
		$tab3[0]=$tab3[0]+1;
		@tab = getindice($indice);
		for($i=0;$i<$tab[0];$i++) {
			if(($tab[1][$i])!=$atome){ travel($tab[1][$i]); }
		}
	}
	return;
} # Elodie - April 2010 - End
sub INTER_Calcul{
	$nbinter=0;
	if(($CHR_TYP ne "ESP-A2") && ($countmolimrs!=1) && ($CHR_TYP ne "ESP-C2") && ($countmolimrs!=1)){
		if($Re_Fit eq "OFF") {
			$NM=1;
			open(ESPOT,">espot_mm");
			for($NM=1; $NM<=$dfmol; $NM++){
				for($NC=1; $NC<=$nbconf[$NM]; $NC++){
					for($w=1; $w<=$nbmod[$NM]; $w++){
						open(ESPO,"<espot_m$NM-$NC-$w");
						print ESPOT <ESPO>;
						close(ESPO);
					}
				}
			}
			print ESPOT "\n\n";
			close(ESPOT);
		}else{
		      if (-e "$DIR/Mol_MM/espot_mm") { system ("cp $DIR/Mol_MM/espot_mm ."); }
		      else {  print "\n\t\tERROR: The multiple molecule espot files required in the re-fitting step is not found.\n\n"; $check=0; Information();
			      if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0); }
		}
format IN=
  @## @###                   @###
$tab[3][$i][$NM],$tempimrs,$i+1
.
		for($i=1; $i<=$dfmol; $i++){ $nbinter=$nbinter+$nbtot[$i] }
		$NM=1;
		open(INPirms,">input1_mm");
		$flagequiv=0;
		printf INPirms (" %s project. RESP input generated by R.E.D.\n &cntrl\n  ioutopt=1, iqopt=1, nmol=$nbinter, ihfree=1, irstrnt=1, qwt= %1.4f \n &end \n  1.0\n %s \n%5s%5d          Column not used by RESP (Added by R.E.D. for information)\n",$CHR_TYP,$qwt,$TITLE[$NM],$CHR_VAL[$NM],$nbatoms[$NM]);
		format_name INPirms "IN";
		for($NM=1; $NM<=$dfmol; $NM++){
			$i=$j=$k=0;
			for($i=0; $i<$nbatoms[$NM]; $i++){
				if($verifimr[$NM]==2){ $tempimrs=$temp3[$i][$NM]; }
				else{ $tempimrs=$temp1[$i][$NM]; }
				write INPirms;
			}
			if($nbtot[$NM]>1){
				for($j=0; $j<$nbtot[$NM]-1; $j++){
					printf INPirms ("\n  1.0\n %s \n%5s%5d\n",$TITLE[$NM],$CHR_VAL[$NM],$nbatoms[$NM]);
					$i=0;
					for($i=0; $i<$nbatoms[$NM]; $i++){
						if($verifimr[$NM]==2){ $tempimrs = $temp3[$i][$NM]; }
						else{ $tempimrs=$temp1[$i][$NM]; }
						if($tempimrs ==0){ $testaff=1; }
						write INPirms;
					}
				}
			}
			if($NM!=$dfmol){ printf INPirms ("\n  1.0\n %s \n%5s%5d          Column not used by RESP (Added by R.E.D. for information)\n",$TITLE[$NM+1],$CHR_VAL[$NM+1],$nbatoms[$NM+1]); }
		}
		$testaff2=0;
		for($NM=1; $NM<=$dfmol; $NM++){ 
			if (($verifimr[$NM]==2) || ($verifimrs[$NM]==2)){ $testaff2=1; }
		}
		if($testaff2==1){ print INPirms "                     Intra and/or inter-molecular charge constraints for atom or group of atoms"; }
		$rl=0;
		for($NM=1; $NM<=$dfmol; $NM++){
			$natom=1;
			if($NM==1){ $natom=1 }
			else{
				for($h=1; $h<$NM;$h++){ $natom=$natom+$nbtot[$h]; }
			}
			if($verifimr[$NM]==2){
				for($i=0; $i<$imrcount[$NM]; $i++){
					$nimr=$intramr[4][$i][$NM];
					if($intramr[1][$i][$NM] =~ /\-/){ printf INPirms ("\n  %3d %3f\n",$nimr,$intramr[1][$i][$NM]);
					}else{ printf INPirms ("\n  %3d  %3f\n",$nimr,$intramr[1][$i][$NM]); }
					$rl=1; $comp=0;
					for($j=1; $j<=$intramr[4][$i][$NM]; $j++){
						printf INPirms ("  %3d  %3d",$natom,$intratom[$j-1][$i][$NM]); $comp++;
						if(($comp == 8) && ($j!=$intramr[4][$i][$NM])){
							printf INPirms ("\n"); $comp=0;
						}
					}
				}
			}
		}
		for($NM=1; $NM <= $dfmol; $NM++){
			if($verifimrs[$NM]==2){
				for($i=0; $i<$imrscount[$NM]; $i++){
					$comp=0;
					$nimr=$intermr[6][$i][$NM]+$intermr[7][$i][$NM];
					if($intermr[1][$i][$NM] =~ /\-/){ printf INPirms ("\n  %3d %3f\n",$nimr,$intermr[1][$i][$NM]);
					}else{ printf INPirms ("\n  %3d  %3f\n",$nimr,$intermr[1][$i][$NM]); }
					$rl=$natom=1;
					if($intertom1[0][$i][$NM]==1){ $natom=1 }
					else{
						for($h=1; $h<$intertom1[0][$i][$NM]; $h++){ $natom=$natom+$nbtot[$h]; }
					}
					for($j=1; $j<=$intermr[6][$i][$NM]; $j++){
						printf INPirms ("  %3d  %3d",$natom,$intertom1[$j][$i][$NM]); $comp++;
						if($comp==8){ printf INPirms ("\n"); $comp=0; }
					}
					$natom=1;
					if($intertom2[0][$i][$NM]==1){ $natom=1 }
					else{
						for($h=1; $h<$intertom2[0][$i][$NM]; $h++){ $natom=$natom+$nbtot[$h]; }
					}
					for($s=1;$s<=$intermr[7][$i][$NM];$s++){
						printf INPirms ("  %3d  %3d",$natom,$intertom2[$s][$i][$NM]); $comp++;
						if(($comp==8) && ($s!=$intermr[7][$i][$NM])){
							printf INPirms ("\n"); $comp=0;
						}
					}
				}
			}
		}
		if($testaff==1){ print INPirms "\n                    Inter-'molecular' charge equivalencing (i. e. for different orientations or conformations)\n";$flagequiv=1; }
		$NM=1;
		for($NM=1; $NM<=$dfmol; $NM++){
			$natom=1;
			if($NM==1){ $natom=1 }
			else{
				for($h=1; $h<$NM; $h++){ $natom=$natom+$nbtot[$h]; }
			}
			if($nbtot[$NM] > 1){
				$i=1;
				for($i=1; $i<=$nbatoms[$NM]; $i++){
					if($verifimr[$NM]==2){ $tempimrs=$temp3[$i-1][$NM]; }
					else{ $tempimrs=$temp1[$i-1][$NM]; }
					if($tempimrs==0){
						$nmol=$nbtot[$NM];
						printf INPirms ("  %3d\n",$nmol);
						$comp=0;
						$natom2=$natom;
						for($j=1;$j<=$nbtot[$NM];$j++){
							printf INPirms ("  %3d  %3d",$natom2,$i); $comp++; $natom2++;
							if(($comp == 8)&&($j != $nbtot[$NM])){
								printf INPirms ("\n"); $comp=0;
							}
						}
					print INPirms "\n";
					}
				}
			}
		}
		$t=0;
		for($NM=1; $NM<=$dfmol; $NM++){
			if($verifimeq[$NM]==2){
				for($i=0; $i<$imeqcount[$NM]; $i++){
					$nmol=$intermeq[2][$i][$NM];
					for($j=0; $j<$intermeq[3][$i][$NM]; $j++){
						$imeq=$imeqtom2[$j][$i][$NM];
						if($t==0){
							if ($flagequiv==0){print INPirms "\n\n";}
							printf INPirms ("  %3d               Inter-'molecular' charge equivalencing (i. e. for different molecules)\n",$nmol); $t++;
						}
						else{printf INPirms ("  %3d\n",$nmol);}
						$comp=0;
						for($s=0;$s<$intermeq[2][$i][$NM];$s++){
							$natom=1;
							if($imeqtom1[$s][$i][$NM]==1){$natom=1;
							}else{
								for($h=1; $h<$imeqtom1[$s][$i][$NM]; $h++){ $natom=$natom+$nbtot[$h]; }
							}
							printf INPirms ("  %3d  %3d",$natom,$imeq); $comp++;
							if(($comp==8) && ($s+1 != $intermeq[2][$i][$NM])){
								printf INPirms ("\n"); $comp=0;
							}
						}
						print INPirms "\n";
					}
				}
			}
		}
		print INPirms "\n\n\n\n\n\n";
		close(INPirms);
		if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")){
			$testaff=0; $NM=1;
			open(INPirms2,">input2_mm");
			$flagequiv2=0;
			printf INPirms2 (" %s project. RESP input generated by R.E.D.\n &cntrl\n  ioutopt=1, iqopt=2, nmol=$nbinter, ihfree=1, irstrnt=1, qwt=0.001\n &end \n  1.0\n %s \n%5s%5d          Column not used by RESP (Added by R.E.D. for information)\n",$CHR_TYP,$TITLE[$NM],$CHR_VAL[$NM],$nbatoms[$NM]);
			format_name INPirms2 "IN";
			for($NM=1; $NM<=$dfmol; $NM++){
				$i=$j=$k=0;
				for($i=0; $i<$nbatoms[$NM]; $i++){
					if($verifimr[$NM]==2){ $tempimrs=$temp4[$i][$NM]; }
					else{ $tempimrs=$temp2[$i][$NM]; }
					for($r=1; $r<=$dfmol; $r++){
						for($p=0; $p<$imrscount[$r]; $p++){
							if($intertom1[0][$p][$r]==$NM){
								for($o=1; $o<=$intermr[6][$p][$r]; $o++){
									if($intertom1[$o][$p][$r]==$i+1){ $tempimrs=-1; }
								}
							}
							elsif($intertom2[0][$p][$r]==$NM){
								for($u=1; $u<=$intermr[7][$p][$r]; $u++){
									if($intertom2[$u][$p][$r]==$i+1){ $tempimrs=-1; }
								}
							}
						}
					}
					$temp5[$i][$NM]=$tempimrs;
					write INPirms2;
				}
				if($nbtot[$NM]>1){
					for($j=0; $j<$nbtot[$NM]-1; $j++){
						printf INPirms2 ("\n  1.0\n %s \n%5s%5d\n",$TITLE[$NM],$CHR_VAL[$NM],$nbatoms[$NM]);
						$i=0;
						for($i=0; $i<$nbatoms[$NM]; $i++){
							$tempimrs=$temp5[$i][$NM];
							if($tempimrs==0){ $testaff=1; }
							write INPirms2;
						}
					}
				}
				if($NM!=$dfmol){ printf INPirms2 ("\n  1.0\n %s \n%5s%5d          Column not used by RESP (Added by R.E.D. for information)\n",$TITLE[$NM+1],$CHR_VAL[$NM+1],$nbatoms[$NM+1]);}
			}
			if($testaff==1){ print INPirms2 "\n                    Inter-'molecular' charge equivalencing (i. e. for different orientations or conformations)\n"; $flagequiv2=1;}
			$NM=1;
			for($NM=1; $NM<=$dfmol; $NM++){
				$natom=1;
				if($NM==1){$natom=1}
				else{
					for($h=1; $h<$NM;$h++){ $natom=$natom + $nbtot[$h]; }
				}
				if($nbtot[$NM]>1){
					$i=1;
					for($i=1;$i<=$nbatoms[$NM];$i++){
						$tempimrs=$temp5[$i-1][$NM];
						if($tempimrs==0){
							$nmol=$nbtot[$NM];
							printf INPirms2 ("  %3d\n",$nmol);
							$comp=0;
							$natom2=$natom;
							for($j=1; $j<=$nbtot[$NM]; $j++){
								printf INPirms2 ("  %3d  %3d",$natom2,$i); $comp++; $natom2++;
								if(($comp == 8) && ($j!=$nbtot[$NM])){
									printf INPirms2 ("\n"); $comp=0;
								}
							}
							print INPirms2 "\n";
						}
					}
				}
			}
			$o=$t=0;
			for($NM=1; $NM<=$dfmol; $NM++){
				if($verifimeq[$NM]==2){
					for($i=0; $i<$imeqcount[$NM]; $i++){
						$nmol=$intermeq[2][$i][$NM];
						for($j=0; $j<$intermeq[3][$i][$NM]; $j++){
							$imeq=$imeqtom2[$j][$i][$NM];
							$comp=0;
							for($s=0; $s<$intermeq[2][$i][$NM]; $s++){
								$tempimrs = $temp5[$imeq-1][$imeqtom1[$s][$i][$NM]];
								$natom=1;
								if($imeqtom1[$s][$i][$NM]==1){ $natom=1 }
								else{
									for($h=1; $h<$imeqtom1[$s][$i][$NM]; $h++){
									$natom=$natom + $nbtot[$h];
									}
								}
								if(($s==0) && ($tempimrs==0)){
									if(($t==0) && ($o==0)){
										if ($flagequiv2==0){ print INPirms2 "\n\n"; }
										printf INPirms2 ("  %3d               Inter-'molecular' charge equivalencing (i. e. for different molecules)",$nmol); $o++; $t++;
									}
									elsif($o==0){ printf INPirms2 ("\n  %3d",$nmol); $o++; }
									printf INPirms2 ("\n  %3d  %3d",$natom,$imeq); $comp++; $o=0;
								}elsif(($s!=0) && ($tempimrs==0)){
									printf INPirms2 ("  %3d  %3d",$natom,$imeq); $comp++; $o=0;
									if(($comp == 8)&&($s+1 != $intermeq[2][$i][$NM])){
										printf INPirms2 ("\n"); $comp=0;
									}
								}
							}
						}
					}
				}
			}
			print INPirms2 "\n\n\n\n\n\n";
			close(INPirms2);
		}
		print "\n\n\n   The $CHR_TYP charges are being derived for ALL molecules...";
		if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
		if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
		if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
		system ("resp -O -i input1_mm -e espot_mm -o output1_mm -p punch1_mm -q qout_mm -t qout1_mm -w qwts_mm -s esout_mm");
		if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")){		#------ RESP input2 run ------
			system ("resp -O -i input2_mm -e espot_mm -o output2_mm -p punch2_mm -q qout1_mm -t qout2_mm -w qwts_mm -s esout_mm");
		}
		if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
		$ok=1;
		if (-e "punch1_mm") {
			open(PUNCH1,"<punch1_mm");
			foreach(<PUNCH1>){
				if(/\s+\d+\s+\d+\s+(\-\d+|\d+)\.\d+\s+/ig){
					($chr)=(split(' '))[3];
					if(($chr =~ /\*+/) || ($chr =~ "nan")) { $ok=0; } # FyD March 2009
					elsif(($chr==0) && ($ok!=0)){ $ok=2; }
				}
			}
			close(PUNCH1);
			if(($CHR_TYP eq "DEBUG") || ($CHR_TYP eq "RESP-A1") || ($CHR_TYP eq "RESP-C1")){
				if(($ok==1) || ($ok==2)){
					open(PUNCH2,"<punch2_mm");
					foreach(<PUNCH2>){
						if(/\s+\d+\s+\d+\s+(\-\d+|\d+)\.\d+\s+/ig){
							($chr)=(split(' '))[3];
							if(($chr =~ /\*+/) || ($chr =~ "nan")) { $ok=0; } # FyD March 2009
							elsif(($chr == 0) && ($ok!=0)){ $ok=2; }
						}
					}
					close(PUNCH2);
				}
			}
		}else { $ok=0 };				
		if($ok==2){ # FyD March 2009
			if(($CHR_TYP eq "DEBUG") || ($CHR_TYP eq "RESP-A1") || ($CHR_TYP eq "RESP-C1")){
				print "\t\t[ WARNING ]\n\tAt least one charge value equals zero!\n\tSee the \"punch2_mm\" file\n\n"; }
			else {	print "\t\t[ WARNING ]\n\tAt least one charge value equals zero!\n\tSee the \"punch1_mm\" file\n\n"; }
		}
		elsif($ok==1){
			if(($CHR_TYP eq "DEBUG") || ($CHR_TYP eq "RESP-A1") || ($CHR_TYP eq "RESP-C1")){
				print "\t\t[ OK ]\n\tSee the \"punch2_mm\" file\n\n"; }
			else {	print "\t\t[ OK ]\n\tSee the \"punch1_mm\" file\n\n"; }
		}else{
			if(($CHR_TYP eq "DEBUG") || ($CHR_TYP eq "RESP-A1A") || ($CHR_TYP eq "RESP-C1")){
				  print "\t\t[ FAILED ]\n\tSee the \"output(1|2)_mm\" file\n\n"; $check=0; Information();
				  if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
			}
			else {	print "\t\t[ FAILED ]\n\tSee the \"output1_mm\" file\n\n"; $check=0; Information();
				  if($XRED eq "ON"){ print "\tPress Enter to exit.\n\n"; <STDIN>; } exit(0);
			}
		}
		if(($tyu==2) || ($tyu==3)){   # Fragment from 2 molecules
			$ri=1;
			
		#******************************RED-2012******************************
		my $right_charge=0;
		if($COR_CHR==6||$COR_CHR==5||$COR_CHR==4||$COR_CHR==3||$COR_CHR==2||$COR_CHR==1){
			$right_charge=1;
		}
		if ( $right_charge == 1 ) {						
			our @atoms_charge_edit=(); 
			our @mol_charges=();
			my $mol_total_charges=0;
			my @mol_charges_back=();
			my @mol_charges_origin=();
			my @mol_atoms_name=();
			for ( my $NM = 1 ; $NM <= $dfmol ; $NM++ ) {
				my $averageimrs;
				my $flag = 0;
				my $i    = 0;
				if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")){
				open (PCH_FILE, "<punch2_mm");
				foreach(<PCH_FILE>){
						if(/    NO   At\.No\.    q0           q\(opt\)   IVARY  d\(rstr\)\/dq/ig) { $flag=1; }
						if(/        Statistics of the fitting:/ig) { $flag=2; }
						if($flag==1){ $i++; }
						if(($i>=1) && ($flag == 1)){ ($averageimrs[$i-1])=(split(' '))[3]; }
					}
							close(PCH_FILE);
						}
						if(($CHR_TYP eq "ESP-A1")||($CHR_TYP eq "ESP-C1")||($CHR_TYP eq "RESP-A2")||($CHR_TYP eq "RESP-C2")){
							open (PCH_FILE, "<punch1_mm");
							foreach(<PCH_FILE>){
								if(/    NO   At\.No\.    q0           q\(opt\)   IVARY  d\(rstr\)\/dq/ig) { $flag=1; }
								if(/        Statistics of the fitting:/ig){ $flag=2; }
								if($flag==1){ $i++; }
								if(($i>=1) && ($flag==1)){ ($averageimrs[$i-1])=(split(' '))[3]; }
							}
							close(PCH_FILE);
						} 
			
				my $natom = 1;
				for ( my $h = 1 ; $h < $NM ; $h++ ) { $natom = $natom + ( $nbatoms[$h] * $nbconf[$h] * $nbmod[$h] ); }
			
				my @name_atomsA     = ();
				my @chargesA        = ();
				my @chargesA_back   = ();
				my @chargesA_origin   = ();
				my $total_chargeA   = 0;
				my $total_chargeA_6 = 0;
				my $iatom           = 0;
				my $iA              = 0;
				for ( my $j = 0 ; $j < $nbatoms[$NM] ; $j++ ) {
					my $potelectA = $averageimrs[ $iA + $natom ];
					$iA++;
					$iatom++;
					my $charge_round = nearest( .0001, $potelectA );
					if($COR_CHR==6){
						$charge_round=nearest( .000001, $potelectA);
					}elsif($COR_CHR==5){
						$charge_round=nearest( .00001, $potelectA);
					}elsif($COR_CHR==4){
						$charge_round=nearest( .0001, $potelectA);
					}elsif($COR_CHR==3){
						$charge_round=nearest( .001, $potelectA);
					}elsif($COR_CHR==2){
						$charge_round=nearest( .01, $potelectA);
					}elsif($COR_CHR==1){
						$charge_round=nearest( .1, $potelectA);
					}	
					
					$total_chargeA   = $total_chargeA + $charge_round;
					$total_chargeA_6 = $total_chargeA_6 + $potelectA;
					push( @name_atomsA, $tab[0][ $iatom - 1 ][$NM] );
					push( @chargesA,    $charge_round );
					push( @chargesA_back,    $charge_round);
					push( @chargesA_origin,    $potelectA);
				}			
				$mol_total_charges=$total_chargeA;
				push(@mol_charges,\@chargesA);
				push(@mol_charges_back,\@chargesA_back);
				push(@mol_charges_origin,\@chargesA_origin);
				push(@mol_atoms_name,\@name_atomsA);
			}					
			foreach my $intra_mcc(@GLOBAL_intra_mcc){
				my $mol=$intra_mcc->[0];
				my $charge_intra=$intra_mcc->[1];
				my @atoms_intra=@{$intra_mcc->[2]};
				my $total_charges_intra=0;
				my $string_intra='';
				foreach my $atom (@atoms_intra){
					$total_charges_intra=$total_charges_intra+$mol_charges[$mol-1][$atom-1];
					$string_intra=$string_intra." ".$atom;
				}
				my $errors=nearest( .0001,abs($charge_intra-$total_charges_intra))*10000;
				if($COR_CHR==6){
					$errors=nearest( .000001,abs($charge_intra-$total_charges_intra))*1000000;
				}elsif($COR_CHR==5){
					$errors=nearest( .00001,abs($charge_intra-$total_charges_intra))*100000;
				}elsif($COR_CHR==4){
					$errors=nearest( .0001,abs($charge_intra-$total_charges_intra))*10000;
				}elsif($COR_CHR==3){
					$errors=nearest( .001,abs($charge_intra-$total_charges_intra))*1000;
				}elsif($COR_CHR==2){
					$errors=nearest( .01,abs($charge_intra-$total_charges_intra))*100;
				}elsif($COR_CHR==1){
					$errors=nearest( .1,abs($charge_intra-$total_charges_intra))*10;
				}	
				our $GLOBAL_CHARGE_times         = 0;
				our $GLOBAL_CHARGE_exist_groupe  = 0;
				our @GLOBAL_CHARGE_result_branch = ();
				our @GLOBAL_CHARGE_results       = ();	
				our @GLOBAL_atoms         = ();
				our $GLOBAL_add_round=0;
				if($errors>0){										
					my @name_atoms=();
					foreach my $atom (@atoms_intra){
						$same=0;
						foreach my $meqa (@GLOBAL_inter_meqa){
							if($mol==$meqa->[0]&&$atom==$meqa->[1]){
								$same=1;
							}
						}						
						if($same==0){
							push(@name_atoms,$mol_atoms_name[$mol-1][$atom-1]);	
						}
					}					
					my $re_groupes = groupes(\@name_atoms,$errors);					
					my @valeur_groupes       = @{ $re_groupes->[0] };
					my @nb_groupes           = @{ $re_groupes->[1] };
					my @exist_groupe         = ();
					my $count_valeur_groupes = scalar @valeur_groupes;
					for ( my $i = 0 ; $i < $count_valeur_groupes ; $i++ ) {
						my @nb_groupe       = @{ $nb_groupes[$i] };
						my $count_nb_groupe = scalar @nb_groupe;
						push( @exist_groupe, [ $valeur_groupes[$i], $count_nb_groupe ] );
					}
					exist_split( $errors, \@exist_groupe, 0, [] );					
					my $count_result_branch = scalar @GLOBAL_CHARGE_result_branch;
					if ( $count_result_branch > 0 ) {
						get_result( \@GLOBAL_CHARGE_result_branch );
						if($GLOBAL_CHARGE_result_branch[0][0]!=0){
							unshift( @GLOBAL_CHARGE_results, $GLOBAL_CHARGE_result_branch[0][1] - $GLOBAL_CHARGE_result_branch[0][0] );
						}
					}					
					my @groupes_atom   = ();
					my @tmp_nb_groupes = @nb_groupes;
					foreach my $element (@GLOBAL_CHARGE_results) {
						for ( my $i = 0 ; $i < $count_valeur_groupes ; $i++ ) {
							if ( $element == $valeur_groupes[$i] ) {
								my @nb_groupe = @{ $tmp_nb_groupes[$i] };
								push( @groupes_atom, $nb_groupe[0] );
								shift(@nb_groupe);
								$tmp_nb_groupes[$i] = \@nb_groupe;
							}
						}
					}					
					my @atoms_groupes = @{ $re_groupes->[2] };
					
					foreach my $element (@groupes_atom) {
						push( @GLOBAL_atoms, @{ $atoms_groupes[$element] } );
					}		
					@GLOBAL_atoms = sort { $a <=> $b } @GLOBAL_atoms;				
					
					if($charge_intra-$total_charges_intra>0){
						$GLOBAL_add_round=0.0001;
						if($COR_CHR==6){
							$GLOBAL_add_round=0.000001;
						}elsif($COR_CHR==5){
							$GLOBAL_add_round=0.00001;
						}elsif($COR_CHR==4){
							$GLOBAL_add_round=0.0001;
						}elsif($COR_CHR==3){
							$GLOBAL_add_round=0.001;
						}elsif($COR_CHR==2){
							$GLOBAL_add_round=0.01;
						}elsif($COR_CHR==1){
							$GLOBAL_add_round=0.1;
						}	
					}else{
						$GLOBAL_add_round=-0.0001;
						if($COR_CHR==6){
							$GLOBAL_add_round=-0.000001;
						}elsif($COR_CHR==5){
							$GLOBAL_add_round=-0.00001;
						}elsif($COR_CHR==4){
							$GLOBAL_add_round=-0.0001;
						}elsif($COR_CHR==3){
							$GLOBAL_add_round=-0.001;
						}elsif($COR_CHR==2){
							$GLOBAL_add_round=-0.01;
						}elsif($COR_CHR==1){
							$GLOBAL_add_round=-0.1;
						}	
					}					
					foreach my $numero_atom (@GLOBAL_atoms){
						my $nb_atom=$atoms_intra[$numero_atom]-1;
						$mol_charges[$mol-1][$nb_atom]=$mol_charges[$mol-1][$nb_atom]+$GLOBAL_add_round;
						push(@atoms_charge_edit,[$mol,$nb_atom]);
					}
					my $count_GLOBAL_atoms=scalar @GLOBAL_atoms;
					if($count_GLOBAL_atoms==0){
						print "\n\t\t\t         WARNING:\n\tMolecule mm $mol INTRA-MCC $string_intra Charge correction not successful\n";	
					}					
				}
			}			
			my @atoms_inter_locked=();	
			foreach my $inter_mcc(@GLOBAL_inter_mcc){
				my $mol_1=$inter_mcc->[0];
				my $mol_2=$inter_mcc->[1];
				my $charge_inter=$inter_mcc->[2];
				my @atoms_inter_1=@{$inter_mcc->[3]};
				my @atoms_inter_2=@{$inter_mcc->[4]};
				my $total_charges_inter=0;
				my $string_inter_1='';
				my $string_inter_2='';
				foreach my $atom (@atoms_inter_1){
					$total_charges_inter=$total_charges_inter+$mol_charges[$mol_1-1][$atom-1];
					$string_inter_1=$string_inter_1." ".$atom;
				}
				foreach my $atom (@atoms_inter_2){
					$total_charges_inter=$total_charges_inter+$mol_charges[$mol_2-1][$atom-1];
					$string_inter_2=$string_inter_2." ".$atom;
				}
				my $errors=nearest( .0001,abs($charge_inter-$total_charges_inter))*10000;
				if($COR_CHR==6){
					$errors=nearest( .000001,abs($charge_inter-$total_charges_inter))*1000000;
				}elsif($COR_CHR==5){
					$errors=nearest( .00001,abs($charge_inter-$total_charges_inter))*100000;
				}elsif($COR_CHR==4){
					$errors=nearest( .0001,abs($charge_inter-$total_charges_inter))*10000;
				}elsif($COR_CHR==3){
					$errors=nearest( .001,abs($charge_inter-$total_charges_inter))*1000;
				}elsif($COR_CHR==2){
					$errors=nearest( .01,abs($charge_inter-$total_charges_inter))*100;
				}elsif($COR_CHR==1){
					$errors=nearest( .1,abs($charge_inter-$total_charges_inter))*10;
				}	
				our $GLOBAL_CHARGE_times         = 0;
				our $GLOBAL_CHARGE_exist_groupe  = 0;
				our @GLOBAL_CHARGE_result_branch = ();
				our @GLOBAL_CHARGE_results       = ();	
				our @GLOBAL_atoms_1         = ();
				our @GLOBAL_atoms_2         = ();
				our $GLOBAL_add_round=0;
				if($errors>0){										
					my @name_atoms_1=();
					foreach my $atom (@atoms_inter_1){
						my $same=0;
						foreach my $meqa (@GLOBAL_inter_meqa){
							if($mol_1==$meqa->[0]&&$atom==$meqa->[1]){
								$same=1;
							}
						}						
						foreach my $atom_inter_locked (@atoms_inter_locked){
							if($atom_inter_locked->[0]==$mol_1&&$atom_inter_locked->[1]==$atom){
								$same=1;
							}
						}
						if($same==0){
							push(@name_atoms_1,$mol_atoms_name[$mol_1-1][$atom-1]);	
							push(@atoms_inter_locked,[$mol_1,$atom]);
						}
					}
					my @name_atoms_2=();
					foreach my $atom (@atoms_inter_2){
						my $same=0;
						foreach my $meqa (@GLOBAL_inter_meqa){
							if($mol_2==$meqa->[0]&&$atom==$meqa->[1]){
								$same=1;
							}
						}						
						foreach my $atom_inter_locked (@atoms_inter_locked){
							if($atom_inter_locked->[0]==$mol_2&&$atom_inter_locked->[1]==$atom){
								$same=1;
							}
						}
						if($same==0){
							push(@name_atoms_2,$mol_atoms_name[$mol_2-1][$atom-1]);
							push(@atoms_inter_locked,[$mol_2,$atom]);
						}
					}					
					my $re_groupes_1 = groupes(\@name_atoms_1,$errors);
					my $re_groupes_2 = groupes(\@name_atoms_2,$errors);					
					my @valeur_groupes_1       = @{ $re_groupes_1->[0] };
					my @nb_groupes_1           = @{ $re_groupes_1->[1] };
					my @exist_groupe_1         = ();
					my $count_valeur_groupes_1 = scalar @valeur_groupes_1;
					for ( my $i = 0 ; $i < $count_valeur_groupes_1 ; $i++ ) {
						my @nb_groupe       = @{ $nb_groupes_1[$i] };
						my $count_nb_groupe = scalar @nb_groupe;
						push( @exist_groupe_1, [ $valeur_groupes_1[$i], $count_nb_groupe ] );
					}
					my @valeur_groupes_2       = @{ $re_groupes_2->[0] };
					my @nb_groupes_2           = @{ $re_groupes_2->[1] };
					my @exist_groupe_2         = ();
					my $count_valeur_groupes_2 = scalar @valeur_groupes_2;
					for ( my $i = 0 ; $i < $count_valeur_groupes_2 ; $i++ ) {
						my @nb_groupe       = @{ $nb_groupes_2[$i] };
						my $count_nb_groupe = scalar @nb_groupe;
						push( @exist_groupe_2, [ $valeur_groupes_2[$i], $count_nb_groupe ] );
					}
					my @exist_groupe         = ();
					foreach my $group_1 (@exist_groupe_1){
						my $same=0;
						my $note=0;
						foreach my $groupe (@exist_groupe){
							if($group_1->[0]==$groupe->[0]){
								$same=1;
								last;	
							}
							$note=$note+1;
						}
						if($same==1){
							$exist_groupe[$note][1]=$exist_groupe[$note][1]+$group_1->[1];
						}else{
							push(@exist_groupe,$group_1);	
						}
					}
					foreach my $group_2 (@exist_groupe_2){
						my $same=0;
						my $note=0;
						foreach my $groupe (@exist_groupe){
							if($group_2->[0]==$groupe->[0]){
								$same=1;
								last;	
							}
							$note=$note+1;
						}
						if($same==1){
							$exist_groupe[$note][1]=$exist_groupe[$note][1]+$group_2->[1];
						}else{
							push(@exist_groupe,$group_2);	
						}
					}
					exist_split( $errors, \@exist_groupe, 0, [] );					
					my $count_result_branch = scalar @GLOBAL_CHARGE_result_branch;
					if ( $count_result_branch > 0 ) {
						get_result( \@GLOBAL_CHARGE_result_branch );
						if($GLOBAL_CHARGE_result_branch[0][0]!=0){
							unshift( @GLOBAL_CHARGE_results, $GLOBAL_CHARGE_result_branch[0][1] - $GLOBAL_CHARGE_result_branch[0][0] );
						}
					}					
					my @groupes_atom_1   = ();
					my @tmp_nb_groupes_1 = @nb_groupes_1;
					my @groupes_atom_2   = ();
					my @tmp_nb_groupes_2 = @nb_groupes_2;
					foreach my $element (@GLOBAL_CHARGE_results) {
						for ( my $i = 0 ; $i < $count_valeur_groupes_1 ; $i++ ) {
							if ( $element == $valeur_groupes_1[$i] ) {
								my @nb_groupe_1 = @{ $tmp_nb_groupes_1[$i] };
								my $count_nb_groupe_1=scalar @nb_groupe_1;
								if($count_nb_groupe_1>0){
									push( @groupes_atom_1, $nb_groupe_1[0] );
									shift(@nb_groupe_1);
									$tmp_nb_groupes_1[$i] = \@nb_groupe_1;	
								}else{
									for ( my $j = 0 ; $j < $count_valeur_groupes_2 ; $j++ ) {
										if ( $element == $valeur_groupes_2[$j] ) {
											my @nb_groupe_2 = @{ $tmp_nb_groupes_2[$j] };
											my $count_nb_groupe_2=scalar @nb_groupe_2;
											push( @groupes_atom_2, $nb_groupe_2[0] );
											shift(@nb_groupe_2);
											$tmp_nb_groupes_2[$j] = \@nb_groupe_2;	
										}
									}
								}
							}else{
								for ( my $j = 0 ; $j < $count_valeur_groupes_2 ; $j++ ) {	
									if ( $element == $valeur_groupes_2[$j] ) {
										my @nb_groupe_2 = @{ $tmp_nb_groupes_2[$j] };
										my $count_nb_groupe_2=scalar @nb_groupe_2;
										push( @groupes_atom_2, $nb_groupe_2[0] );
										shift(@nb_groupe_2);
										$tmp_nb_groupes_2[$j] = \@nb_groupe_2;	
									}
								}
							}
						}
					}					
					my @atoms_groupes_1 = @{ $re_groupes_1->[2] };
					
					foreach my $element (@groupes_atom_1) {
						push( @GLOBAL_atoms_1, @{ $atoms_groupes_1[$element] } );
					}					
					@GLOBAL_atoms_1 = sort { $a <=> $b } @GLOBAL_atoms_1;					
					my @atoms_groupes_2 = @{ $re_groupes_2->[2] };
					
					foreach my $element (@groupes_atom_2) {
						push( @GLOBAL_atoms_2, @{ $atoms_groupes_2[$element] } );
					}					
					@GLOBAL_atoms_2 = sort { $a <=> $b } @GLOBAL_atoms_2;																	
					
					if($charge_inter-$total_charges_inter>0){
						$GLOBAL_add_round=0.0001;
						if($COR_CHR==6){
							$GLOBAL_add_round=0.000001;
						}elsif($COR_CHR==5){
							$GLOBAL_add_round=0.00001;
						}elsif($COR_CHR==4){
							$GLOBAL_add_round=0.0001;
						}elsif($COR_CHR==3){
							$GLOBAL_add_round=0.001;
						}elsif($COR_CHR==2){
							$GLOBAL_add_round=0.01;
						}elsif($COR_CHR==1){
							$GLOBAL_add_round=0.1;
						}	
					}else{
						$GLOBAL_add_round=-0.0001;
						if($COR_CHR==6){
							$GLOBAL_add_round=-0.000001;
						}elsif($COR_CHR==5){
							$GLOBAL_add_round=-0.00001;
						}elsif($COR_CHR==4){
							$GLOBAL_add_round=-0.0001;
						}elsif($COR_CHR==3){
							$GLOBAL_add_round=-0.001;
						}elsif($COR_CHR==2){
							$GLOBAL_add_round=-0.01;
						}elsif($COR_CHR==1){
							$GLOBAL_add_round=-0.1;
						}	
					}					
					foreach my $numero_atom (@GLOBAL_atoms_1){
						my $nb_atom=$atoms_inter_1[$numero_atom]-1;
						$mol_charges[$mol_1-1][$nb_atom]=$mol_charges[$mol_1-1][$nb_atom]+$GLOBAL_add_round;
						push(@atoms_charge_edit,[$mol_1,$nb_atom]);
					}
					foreach my $numero_atom (@GLOBAL_atoms_2){
						my $nb_atom=$atoms_inter_2[$numero_atom]-1;
						$mol_charges[$mol_2-1][$nb_atom]=$mol_charges[$mol_2-1][$nb_atom]+$GLOBAL_add_round;
						push(@atoms_charge_edit,[$mol_2,$nb_atom]);
					}	
					my $count_GLOBAL_atoms_1=scalar @GLOBAL_atoms_1;
					my $count_GLOBAL_atoms_2=scalar @GLOBAL_atoms_2;
					if($count_GLOBAL_atoms_1==0&&$count_GLOBAL_atoms_2==0){
							print "\n\t\t\t         WARNING:\n\tMolecule mm INTER-MCC $mol_1 $mol_2 | $string_inter_1 | $string_inter_2 Charge correction not successful\n";	
					}										
				}
			}					
			for ( my $NM = 1 ; $NM <= $dfmol ; $NM++ ) {
				my @intra_inter_mcc=();
				foreach my $intra_mcc(@GLOBAL_intra_mcc){
					if($intra_mcc->[0]==$NM){
						push(@intra_inter_mcc,@{$intra_mcc->[2]});
					}
				}
				foreach my $inter_mcc(@GLOBAL_inter_mcc){
					if($inter_mcc->[0]==$NM){
						push(@intra_inter_mcc,@{$inter_mcc->[3]});
					}
					if($inter_mcc->[1]==$NM){
						push(@intra_inter_mcc,@{$inter_mcc->[4]});
					}
				}
				my @atoms_others=();
				my @name_atoms=();
				my $total_charges=0;
					
				for(my $i=0; $i<$nbatoms[$NM]; $i++){
					my $same=0;
					foreach my $meqa (@GLOBAL_inter_meqa){
						if($NM==$meqa->[0]&&$i+1==$meqa->[1]){
							$same=1;
						}
					}					
					foreach my $intra_inter (@intra_inter_mcc){
						if($i==$intra_inter-1){
							$same=1;
						}
					}
					if($same==0){
						push(@atoms_others,$i);
						push(@name_atoms,$tab[0][$i][$NM]);
					}
					$total_charges=$total_charges+$mol_charges[$NM-1][$i];
				}
				my $total_charge=0;
				my $errors=nearest( .0001,abs($CHR_VAL[$NM]-$total_charges))*10000;
				if($COR_CHR==6){
					$errors=nearest( .000001,abs($CHR_VAL[$NM]-$total_charges))*1000000;
				}elsif($COR_CHR==5){
					$errors=nearest( .00001,abs($CHR_VAL[$NM]-$total_charges))*100000;
				}elsif($COR_CHR==4){
					$errors=nearest( .0001,abs($CHR_VAL[$NM]-$total_charges))*10000;
				}elsif($COR_CHR==3){
					$errors=nearest( .001,abs($CHR_VAL[$NM]-$total_charges))*1000;
				}elsif($COR_CHR==2){
					$errors=nearest( .01,abs($CHR_VAL[$NM]-$total_charges))*100;
				}elsif($COR_CHR==1){
					$errors=nearest( .1,abs($CHR_VAL[$NM]-$total_charges))*10;
				}	
				our $GLOBAL_CHARGE_times         = 0;
				our $GLOBAL_CHARGE_exist_groupe  = 0;
				our @GLOBAL_CHARGE_result_branch = ();
				our @GLOBAL_CHARGE_results       = ();			
				our @GLOBAL_atoms         = ();
				our $GLOBAL_add_round=0;
				if($errors>0){					
					my $re_groupes = groupes(\@name_atoms,$errors);						
					my @valeur_groupes       = @{ $re_groupes->[0] };
					my @nb_groupes           = @{ $re_groupes->[1] };
					my @exist_groupe         = ();
					my $count_valeur_groupes = scalar @valeur_groupes;
					for ( my $i = 0 ; $i < $count_valeur_groupes ; $i++ ) {
						my @nb_groupe       = @{ $nb_groupes[$i] };
						my $count_nb_groupe = scalar @nb_groupe;
						push( @exist_groupe, [ $valeur_groupes[$i], $count_nb_groupe ] );
					}						
					exist_split( $errors, \@exist_groupe, 0, [] );						
					my $count_result_branch = scalar @GLOBAL_CHARGE_result_branch;
					if ( $count_result_branch > 0 ) {
						get_result( \@GLOBAL_CHARGE_result_branch );
						if($GLOBAL_CHARGE_result_branch[0][0]!=0){
							unshift( @GLOBAL_CHARGE_results, $GLOBAL_CHARGE_result_branch[0][1] - $GLOBAL_CHARGE_result_branch[0][0] );
						}
					}					
					my @groupes_atom   = ();
					my @tmp_nb_groupes = @nb_groupes;
					foreach my $element (@GLOBAL_CHARGE_results) {
						for ( my $i = 0 ; $i < $count_valeur_groupes ; $i++ ) {
							if ( $element == $valeur_groupes[$i] ) {
								my @nb_groupe = @{ $tmp_nb_groupes[$i] };
								push( @groupes_atom, $nb_groupe[0] );
								shift(@nb_groupe);
								$tmp_nb_groupes[$i] = \@nb_groupe;
							}
						}
					}						
					my @atoms_groupes = @{ $re_groupes->[2] };
						
					foreach my $element (@groupes_atom) {
						push( @GLOBAL_atoms, @{ $atoms_groupes[$element] } );
					}
						
					@GLOBAL_atoms = sort { $a <=> $b } @GLOBAL_atoms;						
						
					if($CHR_VAL[$NM]-$total_charges>0){
						$GLOBAL_add_round=0.0001;
						if($COR_CHR==6){
							$GLOBAL_add_round=0.000001;
						}elsif($COR_CHR==5){
							$GLOBAL_add_round=0.00001;
						}elsif($COR_CHR==4){
							$GLOBAL_add_round=0.0001;
						}elsif($COR_CHR==3){
							$GLOBAL_add_round=0.001;
						}elsif($COR_CHR==2){
							$GLOBAL_add_round=0.01;
						}elsif($COR_CHR==1){
							$GLOBAL_add_round=0.1;
						}	
					}else{
						$GLOBAL_add_round=-0.0001;
						if($COR_CHR==6){
							$GLOBAL_add_round=-0.000001;
						}elsif($COR_CHR==5){
							$GLOBAL_add_round=-0.00001;
						}elsif($COR_CHR==4){
							$GLOBAL_add_round=-0.0001;
						}elsif($COR_CHR==3){
							$GLOBAL_add_round=-0.001;
						}elsif($COR_CHR==2){
							$GLOBAL_add_round=-0.01;
						}elsif($COR_CHR==1){
							$GLOBAL_add_round=-0.1;
						}	
					}						
					foreach my $numero_atom (@GLOBAL_atoms){
						my $nb_atom=$atoms_others[$numero_atom];
						$mol_charges[$NM-1][$nb_atom]=$mol_charges[$NM-1][$nb_atom]+$GLOBAL_add_round;
						push(@atoms_charge_edit,[$NM,$nb_atom]);
					}
					my $count_GLOBAL_atoms=scalar @GLOBAL_atoms;
					if($count_GLOBAL_atoms==0){
						print "\n\t\t\t         WARNING:\n\tMolecule mm $NM Charge correction not successful\n";	
					}								
				}				
			}		
				
			format CHARGESLOG_cc6 =
@## @<<<      @##.###### @##.###### @##.###### @<
$icharge+1,$tab[10][$icharge][$imol],$mol_charges_origin[$imol-1][$icharge],$mol_charges_back[$imol-1][$icharge],$mol_charges[$imol-1][$icharge],$mark_round
.
			format CHARGESLOG_cc5 =
@## @<<<      @##.###### @##.##### @##.##### @<
$icharge+1,$tab[10][$icharge][$imol],$mol_charges_origin[$imol-1][$icharge],$mol_charges_back[$imol-1][$icharge],$mol_charges[$imol-1][$icharge],$mark_round
.
			format CHARGESLOG_cc4 =
@## @<<<      @##.###### @##.#### @##.#### @<
$icharge+1,$tab[10][$icharge][$imol],$mol_charges_origin[$imol-1][$icharge],$mol_charges_back[$imol-1][$icharge],$mol_charges[$imol-1][$icharge],$mark_round
.
			format CHARGESLOG_cc3 =
@## @<<<      @##.###### @##.### @##.### @<
$icharge+1,$tab[10][$icharge][$imol],$mol_charges_origin[$imol-1][$icharge],$mol_charges_back[$imol-1][$icharge],$mol_charges[$imol-1][$icharge],$mark_round
.
			format CHARGESLOG_cc2 =
@## @<<<      @##.###### @##.## @##.## @<
$icharge+1,$tab[10][$icharge][$imol],$mol_charges_origin[$imol-1][$icharge],$mol_charges_back[$imol-1][$icharge],$mol_charges[$imol-1][$icharge],$mark_round
.
			format CHARGESLOG_cc1 =
@## @<<<      @##.###### @##.# @##.# @<
$icharge+1,$tab[10][$icharge][$imol],$mol_charges_origin[$imol-1][$icharge],$mol_charges_back[$imol-1][$icharge],$mol_charges[$imol-1][$icharge],$mark_round
.

			if($COR_CHR==6){
				format_name CHARGESLOG_FILE "CHARGESLOG_cc6";
			}elsif($COR_CHR==5){
				format_name CHARGESLOG_FILE "CHARGESLOG_cc5";
			}elsif($COR_CHR==4){
				format_name CHARGESLOG_FILE "CHARGESLOG_cc4";
			}elsif($COR_CHR==3){
				format_name CHARGESLOG_FILE "CHARGESLOG_cc3";
			}elsif($COR_CHR==2){
				format_name CHARGESLOG_FILE "CHARGESLOG_cc2";
			}elsif($COR_CHR==1){
				format_name CHARGESLOG_FILE "CHARGESLOG_cc1";
			}
			open (CHARGESLOG_FILE, ">mm.CHARGES.log");
			for ( $imol = 1 ; $imol <= $dfmol ; $imol++ ) {
				printf CHARGESLOG_FILE "MOLECULE $imol - $TITLE[$imol]\n";
				for($icharge=0; $icharge<$nbatoms[$imol]; $icharge++){
					$mark_round="";
					if($mol_charges_back[$imol-1][$icharge]!=$mol_charges[$imol-1][$icharge]){
						$mark_round="!";
					}
					write CHARGESLOG_FILE;
				}
				printf CHARGESLOG_FILE "\n";
			}
			close (CHARGESLOG_FILE);		
									
		}
		#******************************RED-2012******************************
			
			for($NM=2; $NM<=$dfmol; $NM++){
				if(($nbconect[$NM]!=0) && ($nbconect[1]!=0)){
format MOL2imrsbis =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.#### ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$resname,$potelect
.
format MOL2imrs =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.#### ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$resname,$potelect
.

#******************************RED-2012******************************

format MOL2imrsbis_cc6 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.###### ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$resname,$potelect
.
format MOL2imrs_cc6 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.###### ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$resname,$potelect
.
format MOL2imrsbis_cc5 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.##### ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$resname,$potelect
.
format MOL2imrs_cc5 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.##### ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$resname,$potelect
.
format MOL2imrsbis_cc3 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.### ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$resname,$potelect
.
format MOL2imrs_cc3 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.### ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$resname,$potelect
.
format MOL2imrsbis_cc2 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.## ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$resname,$potelect
.
format MOL2imrs_cc2 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.## ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$resname,$potelect
.
format MOL2imrsbis_cc1 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.# ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$resname,$potelect
.
format MOL2imrs_cc1 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.# ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$resname,$potelect
.

			if($COR_CHR==6){
				if(($atombrut[$NM]==1) && ($atombrut[$imrsmol[0][$ri]]==1)){ format_name MOL2_FILE_IMRS "MOL2imrsbis_cc6"; }
					else{ format_name MOL2_FILE_IMRS "MOL2imrs_cc6"; }
			}elsif($COR_CHR==5){
				if(($atombrut[$NM]==1) && ($atombrut[$imrsmol[0][$ri]]==1)){ format_name MOL2_FILE_IMRS "MOL2imrsbis_cc5"; }
					else{ format_name MOL2_FILE_IMRS "MOL2imrs_cc5"; }
			}elsif($COR_CHR==3){
				if(($atombrut[$NM]==1) && ($atombrut[$imrsmol[0][$ri]]==1)){ format_name MOL2_FILE_IMRS "MOL2imrsbis_cc3"; }
					else{ format_name MOL2_FILE_IMRS "MOL2imrs_cc3"; }
			}elsif($COR_CHR==2){
				if(($atombrut[$NM]==1) && ($atombrut[$imrsmol[0][$ri]]==1)){ format_name MOL2_FILE_IMRS "MOL2imrsbis_cc2"; }
					else{ format_name MOL2_FILE_IMRS "MOL2imrs_cc2"; }
			}elsif($COR_CHR==1){
				if(($atombrut[$NM]==1) && ($atombrut[$imrsmol[0][$ri]]==1)){ format_name MOL2_FILE_IMRS "MOL2imrsbis_cc1"; }
					else{ format_name MOL2_FILE_IMRS "MOL2imrs_cc1"; }
			}else{
			
			#******************************RED-2012******************************
				
				if(($atombrut[$NM]==1) && ($atombrut[$imrsmol[0][$ri]]==1)){ format_name MOL2_FILE_IMRS "MOL2imrsbis"; }
					else{ format_name MOL2_FILE_IMRS "MOL2imrs"; }
			
			#******************************RED-2012******************************
			}
			#******************************RED-2012******************************
					
					for($NC=0;$NC<$nbconf[$NM];$NC++){
						$NC++;
						open (MOL2_FILE_IMRS, ">Mol_m$NM-o$NC-mm1.mol2");
						$NC--;
						$cmptatoms=$il=$testnom=0; $rescpt=1;
						for($i=1; $i<=$nbatoms[$imrsmol[0][$ri]]; $i++){
							$testr=0;
							if($i==1){ $rescpt=1; }
							for($y=0; $y<=$imrcount[$imrsmol[0][$ri]]; $y++){
								if(!defined($intramr[4][$y][$imrsmol[0][$ri]])){ $intramr[4][$y][$imrsmol[0][$ri]]=0; }
								for($w=0; $w<=$intramr[4][$y][$imrsmol[0][$ri]]; $w++){
									if(!defined($intratom[$w][$y][$imrsmol[0][$ri]])){ $intratom[$w][$y][$imrsmol[0][$ri]]=0; }
									if(($intratom[$w][$y][$imrsmol[0][$ri]]==$i) && ($intramr[3][$y][$imrsmol[0][$ri]]!~/[K]/)){ $testr=1; }
								}
							}
							for($x=1; $x<=$imrstom[3][0][$ri]; $x++){
								if($imrstom[1][$x][$ri]==$i){ $testr=1; }
							}
							if($tyu==3){
								for($x=1;$x<=$imrstom[3][0][2];$x++){
									if($imrstom[1][$x][2]==$i){ $testr=1; }
								}
							}
							if($testr==1){ $cmptatoms++; }
						}
						$cmptconnect=0;
						for($i=0; $i<$nbconect[$imrsmol[0][$ri]]; $i++){
							($at1,$at2)=(split(/\-/,$conections[$i][$imrsmol[0][$ri]]));
							$testc2=$testc3=$testc4=0;
							for($y=0; $y<$imrcount[$imrsmol[0][$ri]]; $y++){
								for($w=0;$w<$intramr[4][$y][$imrsmol[0][$ri]];$w++){
									if((($intratom[$w][$y][$imrsmol[0][$ri]]==$at1) && ($intramr[3][$y][$imrsmol[0][$ri]]!~/[K]/)) || (($intratom[$w][$y][$imrsmol[0][$ri]]==$at2) && ($intramr[3][$y][$imrsmol[0][$ri]]!~/[K]/))){ $testc2=1; }
								}
							}
							for($x=1; $x<=$imrstom[3][0][$ri]; $x++){
								if($imrstom[1][$x][$ri]==$at1){
									$testc2=1;
									for($b=1; $b<=$nbatoms[$imrsmol[0][$ri]]-$imrstom[3][0][$ri]; $b++){
										if($nonimrs[1][$b][$ri] == $at2){ $keepres1=$at2; $keepres1bis=$at1; }
									}
								}elsif($imrstom[1][$x][$ri] == $at2){
									$testc2=1;
									for($b=1; $b<=$nbatoms[$imrsmol[0][$ri]]-$imrstom[3][0][$ri]; $b++){
										if($nonimrs[1][$b][$ri] == $at1){ $keepres1=$at1; $keepres1bis=$at2; }
									}
								}
							}
							if($tyu==3){
								for($x=1; $x<=$imrstom[3][0][2]; $x++){
									if($imrstom[1][$x][2]==$at1){
										$testc2=1;
										for($b=1;$b<=$nbatoms[$imrsmol[0][2]]-$imrstom[3][0][2];$b++){
											if($nonimrs[1][$b][2]==$at2){ $keepres3=$at2; $keepres3bis=$at1; }
										}
									}elsif($imrstom[1][$x][2]==$at2){
										$testc2=1;
										for($b=1;$b<=$nbatoms[$imrsmol[0][2]]-$imrstom[3][0][2];$b++){
											if($nonimrs[1][$b][2]==$at1){ $keepres3=$at1; $keepres3bis=$at2; }
										}
									}
								}
							}
							if($testc2==1){ $cmptconnect++; }
						}
						$il=0;
						for($i=1; $i<=$nbatoms[$NM]; $i++){
							$testr=0;
							for($y=0; $y<=$imrcount[$NM]; $y++){
								if(!defined($intramr[4][$y][$NM])){ $intramr[4][$y][$NM]=0; }
								if(!defined($intramr[3][$y][$NM])){ $intramr[3][$y][$NM]=""; }
								for($w=0; $w<=$intramr[4][$y][$NM]; $w++){
									if(!defined($intratom[$w][$y][$NM])){ $intratom[$w][$y][$NM]=0; }
									if(($intratom[$w][$y][$NM]==$i) && ($intramr[3][$y][$NM]!~/[K]/)){ $testr=1; }
								}
							}
							for($x=1; $x<=$imrstom[4][0][$ri]; $x++){
								if($imrstom[2][$x][$ri] == $i){ $testr=1; }
							}
							if($tyu==3){
								for($x=1; $x<=$imrstom[4][0][2]; $x++){
									if($imrstom[2][$x][2] == $i){ $testr=1; }
								}
							}
							if($testr==1){ $cmptatoms++;
							}else{
								$saveres[2][$il][$NM]=$residu[$i-1][$NM];
								$saveres[5][$il][$NM]=$tab[4][$i-1][$NM];
								if($il==0){ $molname2=$saveres[5][$il][$NM]; }
								elsif($il!=0){
									if($saveres[2][$il-1][$NM]!=$saveres[2][$il][$NM]){
										$rescpt++; $molname2=$molname2."-".$saveres[5][$il][$NM];
									}
								}
							$il++;
							}
						}
						$cmptatoms=$nbatoms[$imrsmol[0][$ri]]+$nbatoms[$NM]-$cmptatoms;
						for($i=0;$i<$nbconect[$NM];$i++){
							($at1,$at2)=(split(/\-/,$conections[$i][$NM])); 
							$testc2=$testc3=$testc4=0;
							for($y=0; $y<$imrcount[$NM]; $y++){
								for($w=0; $w<$intramr[4][$y][$NM]; $w++){
									if((($intratom[$w][$y][$NM]==$at1) && ($intramr[3][$y][$NM]!~/[K]/)) || (($intratom[$w][$y][$NM]==$at2) && ($intramr[3][$y][$NM]!~/[K]/))){ $testc2=1; }
								}
							}
							$testc3=0;
							for($x=1; $x<=$imrstom[4][0][$ri]; $x++){
								if($imrstom[2][$x][$ri]==$at1){
									$testc2=1;
									for($b=1;$b<=$nbatoms[$NM]-$imrstom[4][0][$ri];$b++){ 
										if(!defined($nonimrs[2][$b][$ri])){ $nonimrs[2][$b][$ri]=0; }
										if($nonimrs[2][$b][$ri]==$at2){ $keepres2=$at2; $keepres2bis=$at1; }
									}
								}elsif($imrstom[2][$x][$ri]==$at2){
									$testc2=1;
									for($b=1;$b<=$nbatoms[$NM]-$imrstom[4][0][$ri];$b++){
										if(!defined($nonimrs[2][$b][$ri])){$nonimrs[2][$b][$ri]=0;}
										if($nonimrs[2][$b][$ri]==$at1){ $keepres2=$at1; $keepres2bis=$at2; }
									}
								}
							}
							if(!defined($keepres2)){ $keepres2=0; }
							if($tyu==3){
								for($x=1;$x<=$imrstom[4][0][2];$x++){
									if($imrstom[2][$x][2] == $at1){
										$testc2=1;
										for($b=1; $b<=$nbatoms[$NM]-$imrstom[4][0][2]; $b++){
											if(!defined($nonimrs[2][$b][2])){ $nonimrs[2][$b][2]=0; }
											if($nonimrs[2][$b][2]==$at2){ $keepres4=$at2; $keepres4bis=$at1; }
										}
									}elsif($imrstom[2][$x][2] == $at2){
										$testc2=1;
										for($b=1; $b<=$nbatoms[$NM]-$imrstom[4][0][2]; $b++){
											if(!defined($nonimrs[2][$b][2])){ $nonimrs[2][$b][2]=0; }
											if($nonimrs[2][$b][2]==$at1){ $keepres4=$at1; $keepres4bis=$at2; }
										}
									}
								}
							}
							if(!defined($keepres4)){ $keepres4=0; }
							if($testc2==1){ $cmptconnect++; }
						}
						$cmptconnect=$nbconect[$imrsmol[0][$ri]]+$nbconect[$NM]-$cmptconnect+1;
						printf MOL2_FILE_IMRS ("@<TRIPOS>MOLECULE\n%s\n",$molname2);
						printf MOL2_FILE_IMRS ("%5d %5d %5d     0     1\n",$cmptatoms,$cmptconnect,$rescpt);
						printf MOL2_FILE_IMRS ("SMALL\nUSER_CHARGES\n@<TRIPOS>ATOM\n");
						$flag=$i=0;
						if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")){
							open (PCH_FILE, "<punch2_mm");
							foreach(<PCH_FILE>){
								if(/    NO   At\.No\.    q0           q\(opt\)   IVARY  d\(rstr\)\/dq/ig) { $flag=1; }
								if(/        Statistics of the fitting:/ig) { $flag=2; }
								if($flag==1){ $i++; }
								if(($i>=1) && ($flag == 1)){ ($averageimrs[$i-1])=(split(' '))[3]; }
							}
							close(PCH_FILE);
						}
						if(($CHR_TYP eq "ESP-A1")||($CHR_TYP eq "ESP-C1")||($CHR_TYP eq "RESP-A2")||($CHR_TYP eq "RESP-C2")){
							open (PCH_FILE, "<punch1_mm");
							foreach(<PCH_FILE>){
								if(/    NO   At\.No\.    q0           q\(opt\)   IVARY  d\(rstr\)\/dq/ig) { $flag=1; }
								if(/        Statistics of the fitting:/ig){ $flag=2; }
								if($flag==1){ $i++; }
								if(($i>=1) && ($flag==1)){ ($averageimrs[$i-1])=(split(' '))[3]; }
							}
							close(PCH_FILE);
						} # Elodie -April 2010 - Beginning
						$oldnm=$NM; $oldnc=$NC; $NM=$imrsmol[0][$ri]; $NC=0;
						$nb_at[1]=0;$nb_at[2]=0;
						$RESTC = "OFF"; $res1terval=3; # Trick Elodie-FyD If $res1terval=2; this means atom no 2 of part1 of mol1, of part2 of mol1 and of whole mol2
						if($tyu==3){
							for($i=0; $i<$nbconect[$imrsmol[0][$ri]]; $i++){
								($at1,$at2)=(split(/\-/,$conections[$i][$imrsmol[0][$ri]]));
								$test2=0;
								for($b=1; $b<=$nbatoms[$imrsmol[0][2]]-$imrstom[3][0][2]; $b++){
									if($nonimrs[1][$b][2]==$at2){
										for($d=1; $d<=$nbatoms[$imrsmol[0][2]]-$imrstom[3][0][2]; $d++){
											if($nonimrs[1][$d][2]==$at1){ $test2=1; }
										}
									}
								}
								if($test2==1){
									if($keepres3==$at1){
										if ($tab[3][$at2-1][$imrsmol[0][2]]!=1){ $atome=$at2; }
									}
									elsif($keepres3==$at2){
										if ($tab[3][$at1-1][$imrsmol[0][2]]!=1){ $atome=$at1; }
									}
								}
							}
							for($i=1; $i<=$nbatoms[$NM]; $i++) { $vu[$i]=0; }
							$tab3[1]=[];
							$tab3[0]=0;
							travel($keepres3,0);
							$nb_at[1]=$tab3[0];
							$part_mol1[1]=$tab3[1];
							$nb_at[2]=$nbatoms[$NM]-$nb_at[1];
							$nb=0;
							for($i=1; $i<=$nbatoms[$NM]; $i++) {
								$ok=0;
								for($j=0; $j<$nb_at[1]; $j++) {
									if($part_mol1[1][$j]==$i){ $ok=1; }
								}
								if($ok==0){ $part_mol1[2][$nb]=$i; $nb++; }
							}
						}
						if($tyu==2){	
							$nb_at[2]=$nbatoms[$NM];
							for($j=0; $j<$nb_at[2]; $j++){ $part_mol1[2][$j]=$j+1; }
						}
						for($n=0;$n<$nb_at[2];$n++){ #molecule 1 partie2
							$tab2[0][$n][$NM]=$coord[0][$part_mol1[2][$n]-1][$NC][$NM];
							$tab2[1][$n][$NM]=$coord[1][$part_mol1[2][$n]-1][$NC][$NM];
							$tab2[2][$n][$NM]=$coord[2][$part_mol1[2][$n]-1][$NC][$NM];
							if (($part_mol1[2][$n])==$keepres1) { $res1=$n+1; }
							if (($part_mol1[2][$n])==$keepres1bis) { $res1bis=$n+1; }
						}
						$xt=$tab2[0][$res1-1][$NM];
						$yt=$tab2[1][$res1-1][$NM];
						$zt=$tab2[2][$res1-1][$NM];
						translation($xt,$yt,$zt,0,0,$nb_at[2]);
						$x=$tab2[0][$res1bis-1][$NM];
						$y=$tab2[1][$res1bis-1][$NM];
						$z=$tab2[2][$res1bis-1][$NM];	
						rotation_X($x,$y,$z,0,$nb_at[2]);
						$x=$tab2[0][$res1bis-1][$NM];
						$y=$tab2[1][$res1bis-1][$NM];
						$z=$tab2[2][$res1bis-1][$NM];	
						rotation_Z($x,$y,$z,0,$nb_at[2]);
						$res1ter=1;
						while((defined($part_mol1[2][$res1ter-1])) && (($res1==$res1ter)||($res1bis==$res1ter)||(verif_align($keepres1-1,$keepres1bis-1,$part_mol1[2][$res1ter-1]-1)==0))){
							$res1ter++;
						} if ($RESTC eq "ON") { $res1ter=$res1terval; }     #pour choisir directement le 3ème atome à réorienter
						if($res1ter<=$nb_at[2]){
							$x=$tab2[0][$res1ter-1][$NM];
							$y=$tab2[1][$res1ter-1][$NM];
							$z=$tab2[2][$res1ter-1][$NM];
							rotation_X($x,$y,$z,0,$nb_at[2]);
						}
						for($n=0;$n<$nb_at[2];$n++){
							$coord[0][$part_mol1[2][$n]-1][$NC][$NM]=$tab2[0][$n][$NM];
							$coord[1][$part_mol1[2][$n]-1][$NC][$NM]=$tab2[1][$n][$NM];
							$coord[2][$part_mol1[2][$n]-1][$NC][$NM]=$tab2[2][$n][$NM];
						}
						if($tyu==3){
							for($n=0;$n<$nb_at[1];$n++){ # molecule 1 partie 1
								$tab2[0][$n][$NM]=$coord[0][$part_mol1[1][$n]-1][$NC][$NM];
								$tab2[1][$n][$NM]=$coord[1][$part_mol1[1][$n]-1][$NC][$NM];
								$tab2[2][$n][$NM]=$coord[2][$part_mol1[1][$n]-1][$NC][$NM];
								if (($part_mol1[1][$n])==$keepres3) { $res3=$n+1; }
								if (($part_mol1[1][$n])==$keepres3bis) { $res3bis=$n+1; }
							}	
							$xt=$tab2[0][$res3-1][$NM];
							$yt=$tab2[1][$res3-1][$NM];
							$zt=$tab2[2][$res3-1][$NM];
							translation($xt,$yt,$zt,0,0,$nb_at[1]);	
							$x=$tab2[0][$res3bis-1][$NM];
							$y=$tab2[1][$res3bis-1][$NM];
							$z=$tab2[2][$res3bis-1][$NM];
							rotation_X($x,$y,$z,0,$nb_at[1]);
							$x=$tab2[0][$res3bis-1][$NM];
							$y=$tab2[1][$res3bis-1][$NM];
							$z=$tab2[2][$res3bis-1][$NM];
							rotation_Z($x,$y,$z,0,$nb_at[1]);
							$res3ter=1;
							while((defined($part_mol1[1][$res3ter-1])) && (($res3==$res3ter)||($res3bis==$res3ter)||(verif_align($keepres3-1,$keepres3bis-1,$part_mol1[1][$res3ter-1]-1)==0))) {
								$res3ter++;
							} if ($RESTC eq "ON") { $res3ter=$res1terval; }     #pour choisir directement le 3ème atome à réorienter
							if($res3ter<=$nb_at[1]){
								$x=$tab2[0][$res3ter-1][$NM];
								$y=$tab2[1][$res3ter-1][$NM];
								$z=$tab2[2][$res3ter-1][$NM];
								rotation_X($x,$y,$z,0,$nb_at[1]);
							}
							for($n=0; $n<$nb_at[1]; $n++){
								$coord[0][$part_mol1[1][$n]-1][$NC][$NM]=$tab2[0][$n][$NM];
								$coord[1][$part_mol1[1][$n]-1][$NC][$NM]=$tab2[1][$n][$NM];
								$coord[2][$part_mol1[1][$n]-1][$NC][$NM]=$tab2[2][$n][$NM];
							}
						}
						$NM=$oldnm; $NC=$oldnc; $oldnc=0; #molécule 2
						for($n=0; $n<$nbatoms[$NM]; $n++){  
							$tab2[0][$n][$NM]=$coord[0][$n][$NC][$NM];
							$tab2[1][$n][$NM]=$coord[1][$n][$NC][$NM];
							$tab2[2][$n][$NM]=$coord[2][$n][$NC][$NM];
						}
						$xt=$tab2[0][$keepres2bis-1][$NM];
						$yt=$tab2[1][$keepres2bis-1][$NM];
						$zt=$tab2[2][$keepres2bis-1][$NM];
						translation($xt,$yt,$zt,0,0,$nbatoms[$NM]);
						$x=$tab2[0][$keepres2-1][$NM];
						$y=$tab2[1][$keepres2-1][$NM];
						$z=$tab2[2][$keepres2-1][$NM];
						rotation_X($x,$y,$z,0,$nbatoms[$NM]);
						$x=$tab2[0][$keepres2-1][$NM];
						$y=$tab2[1][$keepres2-1][$NM];
						$z=$tab2[2][$keepres2-1][$NM];
						rotation_Z($x,$y,$z,0,$nbatoms[$NM]);
						$res2ter=1;
						while(($keepres2==$res2ter)||($keepres2bis==$res2ter)||(verif_align($keepres2-1,$keepres2bis-1,$res2ter-1)==0)){
							$res2ter++;
						} if ($RESTC eq "ON") { $res2ter=$res1terval; }
						if($res2ter<=$nbatoms[$NM]){
							$x=$tab2[0][$res2ter-1][$NM];
							$y=$tab2[1][$res2ter-1][$NM];
							$z=$tab2[2][$res2ter-1][$NM];
							rotation_X($x,$y,$z,0,$nbatoms[$NM]);
						}
						for($n=0;$n<$nbatoms[$NM];$n++){
							$coord[0][$n][$NC][$NM]=$tab2[0][$n][$NM];
							$coord[1][$n][$NC][$NM]=$tab2[1][$n][$NM];
							$coord[2][$n][$NC][$NM]=$tab2[2][$n][$NM];
						}
						if($tyu==3){
							for($n=0;$n<$nbatoms[$NM];$n++){
								$tab2[0][$n][$NM]=$coord[0][$n][$NC][$NM];
								$tab2[1][$n][$NM]=$coord[1][$n][$NC][$NM];
								$tab2[2][$n][$NM]=$coord[2][$n][$NC][$NM];
							}
							$xt=$tab2[0][$keepres4bis-1][$NM];
							$yt=$tab2[1][$keepres4bis-1][$NM];
							$zt=$tab2[2][$keepres4bis-1][$NM];
							translation($xt,$yt,$zt,0,0,$nbatoms[$NM]);
							$x=$tab2[0][$keepres4-1][$NM];
							$y=$tab2[1][$keepres4-1][$NM];
							$z=$tab2[2][$keepres4-1][$NM];
							rotation_X($x,$y,$z,0,$nbatoms[$NM]);
							$x2=$tab2[0][$keepres4-1][$NM];
							$y2=$tab2[1][$keepres4-1][$NM];
							$z2=$tab2[2][$keepres4-1][$NM];	
							rotation_Z($x2,$y2,$z2,0,$nbatoms[$NM]);
							$res4ter=1;
							while(($keepres4==$res4ter)||($keepres4bis==$res4ter)||(verif_align($keepres4-1,$keepres4bis-1,$res4ter-1)==0)){
								$res4ter++;
							} if ($RESTC eq "ON") { $res4ter=$res1terval; }
							if($res4ter<=$nbatoms[$NM]){
								$x1=$tab2[0][$res4ter-1][$NM];
								$y1=$tab2[1][$res4ter-1][$NM];
								$z1=$tab2[2][$res4ter-1][$NM];
								rotation_X($x1,$y1,$z1,0,$nbatoms[$NM]);
							}
							for($n=0;$n<$nbatoms[$NM];$n++){
								$coord[0][$n][$NC][$NM]=$tab2[0][$n][$NM];
								$coord[1][$n][$NC][$NM]=$tab2[1][$n][$NM];
								$coord[2][$n][$NC][$NM]=$tab2[2][$n][$NM];
							} 
							for($n=0;$n<$nb_at[2];$n++){ #molécule 1 - partie 2
								$tab2[0][$n][$NM]=$coord[0][$part_mol1[2][$n]-1][$oldnc][$imrsmol[0][$ri]];
								$tab2[1][$n][$NM]=$coord[1][$part_mol1[2][$n]-1][$oldnc][$imrsmol[0][$ri]];
								$tab2[2][$n][$NM]=$coord[2][$part_mol1[2][$n]-1][$oldnc][$imrsmol[0][$ri]];
							}
							translation($xt,$yt,$zt,0,0,$nb_at[2]);
							rotation_X($x,$y,$z,0,$nb_at[2]);
							rotation_Z($x2,$y2,$z2,0,$nb_at[2]);
							if($res4ter<=$nbatoms[$NM]){ rotation_X($x1,$y1,$z1,0,$nb_at[2]); }
							for($n=0;$n<$nb_at[2];$n++){
								$coord[0][$part_mol1[2][$n]-1][$oldnc][$imrsmol[0][$ri]]=$tab2[0][$n][$NM];
								$coord[1][$part_mol1[2][$n]-1][$oldnc][$imrsmol[0][$ri]]=$tab2[1][$n][$NM];
								$coord[2][$part_mol1[2][$n]-1][$oldnc][$imrsmol[0][$ri]]=$tab2[2][$n][$NM];
							} 
						} # Elodie April 2010 - end
						$i=0;$in=0; $resmol=$ir=1; $oldnm=$NM; $oldnc=$NC; $NM=$imrsmol[0][$ri]; $NC=0;
						for($j=0;$j<$nbatoms[$imrsmol[0][$ri]];$j++){
							$atom=$tab[1][$i][$imrsmol[0][$ri]]; 
							$resname=$tab[4][$keepres2+1][$oldnm];
							if( ($tab[1][$i][$imrsmol[0][$ri]] =~ /T$/) ) { $atom=~s/T//; }
							$potelect=$averageimrs[$i+1];
							if($j==0){ $resmol=1; }
							$i++;
							$element=$atom;
							$atom="$atom"."$ir";
							$y=$w=$molimr=0;
							for($y=0; $y<=$imrcount[$imrsmol[0][$ri]]; $y++){
								for($w=0;$w<=$intramr[4][$y][$imrsmol[0][$ri]];$w++){
									if(($intratom[$w][$y][$imrsmol[0][$ri]]==$i) && ($intramr[3][$y][$imrsmol[0][$ri]]!~/[K]/)){ $molimr=1; }
								}
							}
							for($x=1;$x<=$imrstom[3][0][$ri];$x++){
								if($imrstom[1][$x][$ri] == $i){ $molimr=1; }
							}
							if($tyu==3){
								for($x=1;$x<=$imrstom[3][0][2];$x++){
									if($imrstom[1][$x][2] == $i){ $molimr=1; }
								}
							}
							if($molimr==0){
								$saveres[1][$in]=1;
								$saveres[2][$in]=$saveres[2][0][$oldnm];
								$saveres[3][$in]=$resname;
								$ir++; $in++;
								$save[$i][$imrsmol[0][$ri]]=$in;
								
								#******************************RED-2012******************************
								if($right_charge==1){
									my $same=0;
									foreach my $atom_charge_edit(@atoms_charge_edit){
									if($NM==$atom_charge_edit->[0]&&$j==$atom_charge_edit->[1]){
											$potelect=$mol_charges[$NM-1][$j];
											$same=1;
										}
									}	
									if($same==0){
										my $potelect_round=nearest(.0001,$potelect);
										my $round=$potelect_round-$potelect;
										my $round_5=abs(abs($round)-0.00005);
										my $round_add=0.000001;
										if($COR_CHR==6){
											$potelect_round=nearest(.0001,$potelect);
											$round=$potelect_round-$potelect;
											$round_5=abs(abs($round)-0.00005);
											$round_add=0.000001;
										}elsif($COR_CHR==5){
											$potelect_round=nearest(.00001,$potelect);
											$round=$potelect_round-$potelect;
											$round_5=abs(abs($round)-0.000005);
											$round_add=0.0000001;
										}elsif($COR_CHR==4){
											$potelect_round=nearest(.0001,$potelect);
											$round=$potelect_round-$potelect;
											$round_5=abs(abs($round)-0.00005);
											$round_add=0.000001;
										}elsif($COR_CHR==3){
											$potelect_round=nearest(.001,$potelect);
											$round=$potelect_round-$potelect;
											$round_5=abs(abs($round)-0.0005);
											$round_add=0.00001;
										}elsif($COR_CHR==2){
											$potelect_round=nearest(.01,$potelect);
											$round=$potelect_round-$potelect;
											$round_5=abs(abs($round)-0.005);
											$round_add=0.0001;
										}elsif($COR_CHR==1){
											$potelect_round=nearest(.1,$potelect);
											$round=$potelect_round-$potelect;
											$round_5=abs(abs($round)-0.05);
											$round_add=0.001;
										}	
										if($round_5<0.00000000001){
											if($round>0){
												$potelect=$potelect+$round_add;
											}else{
												$potelect=$potelect-$round_add;
											}
										}
									}
												
								}					
								#******************************RED-2012******************************
								
								write MOL2_FILE_IMRS;
							}
							if(!defined($save[$i][$imrsmol[0][$ri]])){ $save[$i][$imrsmol[0][$ri]]=0; }
						}
						$i=0;$test=0; $NM=$oldnm; $NC=$oldnc; $natom=1;
						# for($h=1; $h<$NM; $h++){ $natom=$natom+($nbatoms[$h]*$nbconf[$h]*$nbrot[$h]); } # FyD July 2010
						for($h=1; $h<$NM; $h++){ $natom=$natom+($nbatoms[$h]*$nbconf[$h]*$nbmod[$h]); }
						for($j=0; $j<$nbatoms[$NM]; $j++){
							$atom=$tab[1][$i][$NM];
							if(($tab[1][$i][$NM] =~ /T$/)){ $atom=~s/T//; }
							$potelect=$averageimrs[$i+$natom];
							if($j==0){ $resmol++; }
							$i++;
							$element=$atom;
							$atom="$atom"."$ir";
							$y=$w=$molimr=0;
							for($y=0; $y<=$imrcount[$NM]; $y++){
								if(!defined($intramr[4][$y][$NM])){ $intramr[4][$y][$NM]=0; }
								if(!defined($intramr[3][$y][$NM])){ $intramr[3][$y][$NM]=""; }
								for($w=0;$w<=$intramr[4][$y][$NM];$w++){
									if(!defined($intratom[$w][$y][$NM])){ $intratom[$w][$y][$NM]=0; }
									if(($intratom[$w][$y][$NM]==$i) && ($intramr[3][$y][$NM]!~/[K]/)){ $molimr=1; }
								}
							}
							for($x=1; $x<=$imrstom[4][0][$ri]; $x++){
								if($imrstom[2][$x][$ri]==$i){ $molimr=1; }
							}
							if($tyu==3){
								for($x=1; $x<=$imrstom[4][0][2]; $x++){
									if($imrstom[2][$x][2]==$i){ $molimr=1; }
								}
							}
							if($molimr==0){
								$saveres[1][$in]=$resmol;
								$saveres[2][$in]=$residu[$j][$NM];
								$saveres[3][$in]=$tab[4][$j][$NM];
								$resname=$tab[4][$j][$NM];
								if ($test==0){
									$resmol=1;
									for($l=0;$l<$in;$l++){ $saveres[2][$l]=$saveres[2][$in]; }
								}else{
									if($saveres[2][$in-1]!=$saveres[2][$in]){ $resmol++; }
								}
								$test++; $ir++; $in++;
								$save[$i][$NM]=$in;
								
								#******************************RED-2012******************************
								if($right_charge==1){
									my $same=0;
									foreach my $atom_charge_edit(@atoms_charge_edit){
									if($NM==$atom_charge_edit->[0]&&$j==$atom_charge_edit->[1]){
											$potelect=$mol_charges[$NM-1][$j];
											$same=1;
										}
									}	
									if($same==0){
										my $potelect_round=nearest(.0001,$potelect);
										my $round=$potelect_round-$potelect;
										my $round_5=abs(abs($round)-0.00005);
										my $round_add=0.000001;
										if($COR_CHR==6){
											$potelect_round=nearest(.0001,$potelect);
											$round=$potelect_round-$potelect;
											$round_5=abs(abs($round)-0.00005);
											$round_add=0.000001;
										}elsif($COR_CHR==5){
											$potelect_round=nearest(.00001,$potelect);
											$round=$potelect_round-$potelect;
											$round_5=abs(abs($round)-0.000005);
											$round_add=0.0000001;
										}elsif($COR_CHR==4){
											$potelect_round=nearest(.0001,$potelect);
											$round=$potelect_round-$potelect;
											$round_5=abs(abs($round)-0.00005);
											$round_add=0.000001;
										}elsif($COR_CHR==3){
											$potelect_round=nearest(.001,$potelect);
											$round=$potelect_round-$potelect;
											$round_5=abs(abs($round)-0.0005);
											$round_add=0.00001;
										}elsif($COR_CHR==2){
											$potelect_round=nearest(.01,$potelect);
											$round=$potelect_round-$potelect;
											$round_5=abs(abs($round)-0.005);
											$round_add=0.0001;
										}elsif($COR_CHR==1){
											$potelect_round=nearest(.1,$potelect);
											$round=$potelect_round-$potelect;
											$round_5=abs(abs($round)-0.05);
											$round_add=0.001;
										}	
										if($round_5<0.00000000001){
											if($round>0){
												$potelect=$potelect+$round_add;
											}else{
												$potelect=$potelect-$round_add;
											}
										}
									}			
								}					
								#******************************RED-2012******************************
								
								write MOL2_FILE_IMRS;
							}
						}
						$ic=$i=0;
						printf MOL2_FILE_IMRS ("@<TRIPOS>BOND\n");
						for($i=0; $i<$nbconect[$imrsmol[0][$ri]]; $i++){
							($at1,$at2)=(split(/\-/,$conections[$i][$imrsmol[0][$ri]]));
							$y=$w=$testc=$test2=0;
							for($y=0; $y<=$imrcount[$imrsmol[0][$ri]]; $y++){
								for($w=0;$w<=$intramr[4][$y][$imrsmol[0][$ri]];$w++){
									if((($intratom[$w][$y][$imrsmol[0][$ri]]==$at1) && ($intramr[3][$y][$imrsmol[0][$ri]]!~/[K]/)) || (($intratom[$w][$y][$imrsmol[0][$ri]]==$at2) && ($intramr[3][$y][$imrsmol[0][$ri]]!~/[K]/))) { $testc=1; } 
									for($x=1;$x<=$imrstom[3][0][$ri];$x++){
										if(($imrstom[1][$x][$ri] == $at1)||($imrstom[1][$x][$ri] == $at2)) { $testc=1; } 
									}
									if($tyu==3){
										for($b=1; $b<=$nbatoms[$imrsmol[0][2]]-$imrstom[3][0][2]; $b++){
											if($nonimrs[1][$b][2]==$at2){
												for($d=1; $d<=$nbatoms[$imrsmol[0][2]]-$imrstom[3][0][2]; $d++){
													if($nonimrs[1][$d][2]==$at1){ $test2=1; }
												}
											}
										}
										if($test2==1){
											if($keepres3==$at1){
												if ($tab[3][$at2-1][$imrsmol[0][2]]!=1){ $testc=1; }
											}
											if($keepres3==$at2){
												if ($tab[3][$at1-1][$imrsmol[0][2]]!=1){ $testc=1; }
											}
										}
										for($x=1;$x<=$imrstom[3][0][2];$x++){
											if(($imrstom[1][$x][2] == $at1)||($imrstom[1][$x][2] == $at2)) { $testc=1; }
										}
									}
								}
							}
							if($testc==0){ printf MOL2_FILE_IMRS ("%5d %5d %5d 1\n",$ic+1,$save[$at1][$imrsmol[0][$ri]],$save[$at2][$imrsmol[0][$ri]]); $ic++; }
						}
						for($i=0; $i<$nbconect[$NM]; $i++){
							($at1,$at2)=(split(/\-/,$conections[$i][$NM]));   
							$y=$w=$testc=0;
							for($y=0; $y<=$imrcount[$NM]; $y++){
								for($w=0;$w<=$intramr[4][$y][$NM];$w++){
									if((($intratom[$w][$y][$NM]==$at1) && ($intramr[3][$y][$NM]!~/[K]/)) || (($intratom[$w][$y][$NM]==$at2) && ($intramr[3][$y][$NM]!~/[K]/))){ $testc=1; }
									for($x=1;$x<=$imrstom[4][0][$ri];$x++){
										if(($imrstom[2][$x][$ri]==$at1) || ($imrstom[2][$x][$ri]==$at2)) { $testc=1; }
									}
									if($tyu==3){
										for($x=1;$x<=$imrstom[4][0][2];$x++){
											if(($imrstom[2][$x][2]==$at1) || ($imrstom[2][$x][2]==$at2)) { $testc=1; }
										}
									}
								}
							}
							if($testc==0){ printf MOL2_FILE_IMRS ("%5d %5d %5d 1\n",$ic+1,$save[$at1][$NM],$save[$at2][$NM]);$ic++; }
						}
						if(!defined($save[$keepres2][$NM])){ $save[$keepres2][$NM]=0; }
						if(!defined($save[$keepres4][$NM])){ $save[$keepres4][$NM]=0; }
						printf MOL2_FILE_IMRS ("%5d %5d %5d 1\n",$ic+1,$save[$keepres1][$imrsmol[0][$ri]],$save[$keepres2][$NM]);$ic++;
						if($tyu==3){ printf MOL2_FILE_IMRS ("%5d %5d %5d 1\n",$ic+1,$save[$keepres3][$imrsmol[0][$ri]],$save[$keepres4][$NM]); }
						printf MOL2_FILE_IMRS ("@<TRIPOS>SUBSTRUCTURE\n");
						$z=1;
						for($i=1;$i<$in;$i++){
							if($i==1){
								printf MOL2_FILE_IMRS (" %6d %4s         %6d ****               0 ****  ****  \n",1,$saveres[3][$i],1);
							}elsif($saveres[2][$i-1] != $saveres[2][$i]){
								$z++;
								printf MOL2_FILE_IMRS (" %6d %4s         %6d ****               0 ****  ****  \n",$z,$saveres[3][$i],$i+1);
							}
						}
						print MOL2_FILE_IMRS "\n\n";
						close (MOL2_FILE_IMRS);
					}
				}
			}
			$rg=0;
			for($NM=2; $NM<=$dfmol; $NM++){
				if(($nbconect[$NM]!=0) && ($nbconect[1]!=0)){
					if($rg==0){ print "\n\n\tThe following Tripos mol2 file(s) has/have been created."; $rg++ }
					print "\n\t";
					for ($NC=1;$NC<=$nbconf[$imrsmol[1][$ri]];$NC++){ print "Mol_m$NM-o$NC-mm1.mol2 "; }  # Fragment from 2 molecules
					if($NM==$dfmol){ print "\n"; }
				}
			}
		}
		elsif($tyu==1){  # Whole molecules
		
		#******************************RED-2012******************************
		my $right_charge=0;
		if($COR_CHR==6||$COR_CHR==5||$COR_CHR==4||$COR_CHR==3||$COR_CHR==2||$COR_CHR==1){
			$right_charge=1;
		}
		if ( $right_charge == 1 ) {						
			our @atoms_charge_edit=(); 
			our @mol_charges=();
			my $mol_total_charges=0;
			my @mol_charges_back=();
			my @mol_charges_origin=();
			my @mol_atoms_name=();
			for ( my $NM = 1 ; $NM <= $dfmol ; $NM++ ) {
				my $averageimrs;
				my $flag = 0;
				my $i    = 0;
				if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")){
				open (PCH_FILE, "<punch2_mm");
				foreach(<PCH_FILE>){
						if(/    NO   At\.No\.    q0           q\(opt\)   IVARY  d\(rstr\)\/dq/ig) { $flag=1; }
						if(/        Statistics of the fitting:/ig) { $flag=2; }
						if($flag==1){ $i++; }
						if(($i>=1) && ($flag == 1)){ ($averageimrs[$i-1])=(split(' '))[3]; }
					}
							close(PCH_FILE);
						}
						if(($CHR_TYP eq "ESP-A1")||($CHR_TYP eq "ESP-C1")||($CHR_TYP eq "RESP-A2")||($CHR_TYP eq "RESP-C2")){
							open (PCH_FILE, "<punch1_mm");
							foreach(<PCH_FILE>){
								if(/    NO   At\.No\.    q0           q\(opt\)   IVARY  d\(rstr\)\/dq/ig) { $flag=1; }
								if(/        Statistics of the fitting:/ig){ $flag=2; }
								if($flag==1){ $i++; }
								if(($i>=1) && ($flag==1)){ ($averageimrs[$i-1])=(split(' '))[3]; }
							}
							close(PCH_FILE);
						} 
			
				my $natom = 1;
				for ( my $h = 1 ; $h < $NM ; $h++ ) { $natom = $natom + ( $nbatoms[$h] * $nbconf[$h] * $nbmod[$h] ); }
			
				my @name_atomsA     = ();
				my @chargesA        = ();
				my @chargesA_back   = ();
				my @chargesA_origin   = ();
				my $total_chargeA   = 0;
				my $total_chargeA_6 = 0;
				my $iatom           = 0;
				my $iA              = 0;
				for ( my $j = 0 ; $j < $nbatoms[$NM] ; $j++ ) {
					my $potelectA = $averageimrs[ $iA + $natom ];
					$iA++;
					$iatom++;
					my $charge_round = nearest( .0001, $potelectA );
					if($COR_CHR==6){
						$charge_round=nearest( .000001, $potelectA);
					}elsif($COR_CHR==5){
						$charge_round=nearest( .00001, $potelectA);
					}elsif($COR_CHR==4){
						$charge_round=nearest( .0001, $potelectA);
					}elsif($COR_CHR==3){
						$charge_round=nearest( .001, $potelectA);
					}elsif($COR_CHR==2){
						$charge_round=nearest( .01, $potelectA);
					}elsif($COR_CHR==1){
						$charge_round=nearest( .1, $potelectA);
					}	
					
					$total_chargeA   = $total_chargeA + $charge_round;
					$total_chargeA_6 = $total_chargeA_6 + $potelectA;
					push( @name_atomsA, $tab[0][ $iatom - 1 ][$NM] );
					push( @chargesA,    $charge_round );
					push( @chargesA_back,    $charge_round);
					push( @chargesA_origin,    $potelectA);
				}			
				$mol_total_charges=$total_chargeA;
				push(@mol_charges,\@chargesA);
				push(@mol_charges_back,\@chargesA_back);
				push(@mol_charges_origin,\@chargesA_origin);
				push(@mol_atoms_name,\@name_atomsA);
			}					
			foreach my $intra_mcc(@GLOBAL_intra_mcc){
				my $mol=$intra_mcc->[0];
				my $charge_intra=$intra_mcc->[1];
				my @atoms_intra=@{$intra_mcc->[2]};
				my $total_charges_intra=0;
				my $string_intra='';
				foreach my $atom (@atoms_intra){
					$total_charges_intra=$total_charges_intra+$mol_charges[$mol-1][$atom-1];
					$string_intra=$string_intra." ".$atom;
				}
				my $errors=nearest( .0001,abs($charge_intra-$total_charges_intra))*10000;
				if($COR_CHR==6){
					$errors=nearest( .000001,abs($charge_intra-$total_charges_intra))*1000000;
				}elsif($COR_CHR==5){
					$errors=nearest( .00001,abs($charge_intra-$total_charges_intra))*100000;
				}elsif($COR_CHR==4){
					$errors=nearest( .0001,abs($charge_intra-$total_charges_intra))*10000;
				}elsif($COR_CHR==3){
					$errors=nearest( .001,abs($charge_intra-$total_charges_intra))*1000;
				}elsif($COR_CHR==2){
					$errors=nearest( .01,abs($charge_intra-$total_charges_intra))*100;
				}elsif($COR_CHR==1){
					$errors=nearest( .1,abs($charge_intra-$total_charges_intra))*10;
				}	
				our $GLOBAL_CHARGE_times         = 0;
				our $GLOBAL_CHARGE_exist_groupe  = 0;
				our @GLOBAL_CHARGE_result_branch = ();
				our @GLOBAL_CHARGE_results       = ();	
				our @GLOBAL_atoms         = ();
				our $GLOBAL_add_round=0;
				if($errors>0){										
					my @name_atoms=();
					foreach my $atom (@atoms_intra){
						$same=0;
						foreach my $meqa (@GLOBAL_inter_meqa){
							if($mol==$meqa->[0]&&$atom==$meqa->[1]){
								$same=1;
							}
						}						
						if($same==0){
							push(@name_atoms,$mol_atoms_name[$mol-1][$atom-1]);	
						}
					}					
					my $re_groupes = groupes(\@name_atoms,$errors);					
					my @valeur_groupes       = @{ $re_groupes->[0] };
					my @nb_groupes           = @{ $re_groupes->[1] };
					my @exist_groupe         = ();
					my $count_valeur_groupes = scalar @valeur_groupes;
					for ( my $i = 0 ; $i < $count_valeur_groupes ; $i++ ) {
						my @nb_groupe       = @{ $nb_groupes[$i] };
						my $count_nb_groupe = scalar @nb_groupe;
						push( @exist_groupe, [ $valeur_groupes[$i], $count_nb_groupe ] );
					}
					exist_split( $errors, \@exist_groupe, 0, [] );					
					my $count_result_branch = scalar @GLOBAL_CHARGE_result_branch;
					if ( $count_result_branch > 0 ) {
						get_result( \@GLOBAL_CHARGE_result_branch );
						if($GLOBAL_CHARGE_result_branch[0][0]!=0){
							unshift( @GLOBAL_CHARGE_results, $GLOBAL_CHARGE_result_branch[0][1] - $GLOBAL_CHARGE_result_branch[0][0] );
						}
					}					
					my @groupes_atom   = ();
					my @tmp_nb_groupes = @nb_groupes;
					foreach my $element (@GLOBAL_CHARGE_results) {
						for ( my $i = 0 ; $i < $count_valeur_groupes ; $i++ ) {
							if ( $element == $valeur_groupes[$i] ) {
								my @nb_groupe = @{ $tmp_nb_groupes[$i] };
								push( @groupes_atom, $nb_groupe[0] );
								shift(@nb_groupe);
								$tmp_nb_groupes[$i] = \@nb_groupe;
							}
						}
					}					
					my @atoms_groupes = @{ $re_groupes->[2] };
					
					foreach my $element (@groupes_atom) {
						push( @GLOBAL_atoms, @{ $atoms_groupes[$element] } );
					}		
					@GLOBAL_atoms = sort { $a <=> $b } @GLOBAL_atoms;				
					
					if($charge_intra-$total_charges_intra>0){
						$GLOBAL_add_round=0.0001;
						if($COR_CHR==6){
							$GLOBAL_add_round=0.000001;
						}elsif($COR_CHR==5){
							$GLOBAL_add_round=0.00001;
						}elsif($COR_CHR==4){
							$GLOBAL_add_round=0.0001;
						}elsif($COR_CHR==3){
							$GLOBAL_add_round=0.001;
						}elsif($COR_CHR==2){
							$GLOBAL_add_round=0.01;
						}elsif($COR_CHR==1){
							$GLOBAL_add_round=0.1;
						}	
					}else{
						$GLOBAL_add_round=-0.0001;
						if($COR_CHR==6){
							$GLOBAL_add_round=-0.000001;
						}elsif($COR_CHR==5){
							$GLOBAL_add_round=-0.00001;
						}elsif($COR_CHR==4){
							$GLOBAL_add_round=-0.0001;
						}elsif($COR_CHR==3){
							$GLOBAL_add_round=-0.001;
						}elsif($COR_CHR==2){
							$GLOBAL_add_round=-0.01;
						}elsif($COR_CHR==1){
							$GLOBAL_add_round=-0.1;
						}	
					}					
					foreach my $numero_atom (@GLOBAL_atoms){
						my $nb_atom=$atoms_intra[$numero_atom]-1;
						$mol_charges[$mol-1][$nb_atom]=$mol_charges[$mol-1][$nb_atom]+$GLOBAL_add_round;
						push(@atoms_charge_edit,[$mol,$nb_atom]);
					}
					my $count_GLOBAL_atoms=scalar @GLOBAL_atoms;
					if($count_GLOBAL_atoms==0){
						print "\n\t\t\t         WARNING:\n\tMolecule mm $mol INTRA-MCC $string_intra Charge correction not successful\n";	
					}					
				}
			}			
			my @atoms_inter_locked=();	
			foreach my $inter_mcc(@GLOBAL_inter_mcc){
				my $mol_1=$inter_mcc->[0];
				my $mol_2=$inter_mcc->[1];
				my $charge_inter=$inter_mcc->[2];
				my @atoms_inter_1=@{$inter_mcc->[3]};
				my @atoms_inter_2=@{$inter_mcc->[4]};
				my $total_charges_inter=0;
				my $string_inter_1='';
				my $string_inter_2='';
				foreach my $atom (@atoms_inter_1){
					$total_charges_inter=$total_charges_inter+$mol_charges[$mol_1-1][$atom-1];
					$string_inter_1=$string_inter_1." ".$atom;
				}
				foreach my $atom (@atoms_inter_2){
					$total_charges_inter=$total_charges_inter+$mol_charges[$mol_2-1][$atom-1];
					$string_inter_2=$string_inter_2." ".$atom;
				}
				my $errors=nearest( .0001,abs($charge_inter-$total_charges_inter))*10000;
				if($COR_CHR==6){
					$errors=nearest( .000001,abs($charge_inter-$total_charges_inter))*1000000;
				}elsif($COR_CHR==5){
					$errors=nearest( .00001,abs($charge_inter-$total_charges_inter))*100000;
				}elsif($COR_CHR==4){
					$errors=nearest( .0001,abs($charge_inter-$total_charges_inter))*10000;
				}elsif($COR_CHR==3){
					$errors=nearest( .001,abs($charge_inter-$total_charges_inter))*1000;
				}elsif($COR_CHR==2){
					$errors=nearest( .01,abs($charge_inter-$total_charges_inter))*100;
				}elsif($COR_CHR==1){
					$errors=nearest( .1,abs($charge_inter-$total_charges_inter))*10;
				}	
				our $GLOBAL_CHARGE_times         = 0;
				our $GLOBAL_CHARGE_exist_groupe  = 0;
				our @GLOBAL_CHARGE_result_branch = ();
				our @GLOBAL_CHARGE_results       = ();	
				our @GLOBAL_atoms_1         = ();
				our @GLOBAL_atoms_2         = ();
				our $GLOBAL_add_round=0;
				if($errors>0){										
					my @name_atoms_1=();
					foreach my $atom (@atoms_inter_1){
						my $same=0;
						foreach my $meqa (@GLOBAL_inter_meqa){
							if($mol_1==$meqa->[0]&&$atom==$meqa->[1]){
								$same=1;
							}
						}						
						foreach my $atom_inter_locked (@atoms_inter_locked){
							if($atom_inter_locked->[0]==$mol_1&&$atom_inter_locked->[1]==$atom){
								$same=1;
							}
						}
						if($same==0){
							push(@name_atoms_1,$mol_atoms_name[$mol_1-1][$atom-1]);	
							push(@atoms_inter_locked,[$mol_1,$atom]);
						}
					}
					my @name_atoms_2=();
					foreach my $atom (@atoms_inter_2){
						my $same=0;
						foreach my $meqa (@GLOBAL_inter_meqa){
							if($mol_2==$meqa->[0]&&$atom==$meqa->[1]){
								$same=1;
							}
						}						
						foreach my $atom_inter_locked (@atoms_inter_locked){
							if($atom_inter_locked->[0]==$mol_2&&$atom_inter_locked->[1]==$atom){
								$same=1;
							}
						}
						if($same==0){
							push(@name_atoms_2,$mol_atoms_name[$mol_2-1][$atom-1]);
							push(@atoms_inter_locked,[$mol_2,$atom]);
						}
					}					
					my $re_groupes_1 = groupes(\@name_atoms_1,$errors);
					my $re_groupes_2 = groupes(\@name_atoms_2,$errors);					
					my @valeur_groupes_1       = @{ $re_groupes_1->[0] };
					my @nb_groupes_1           = @{ $re_groupes_1->[1] };
					my @exist_groupe_1         = ();
					my $count_valeur_groupes_1 = scalar @valeur_groupes_1;
					for ( my $i = 0 ; $i < $count_valeur_groupes_1 ; $i++ ) {
						my @nb_groupe       = @{ $nb_groupes_1[$i] };
						my $count_nb_groupe = scalar @nb_groupe;
						push( @exist_groupe_1, [ $valeur_groupes_1[$i], $count_nb_groupe ] );
					}
					my @valeur_groupes_2       = @{ $re_groupes_2->[0] };
					my @nb_groupes_2           = @{ $re_groupes_2->[1] };
					my @exist_groupe_2         = ();
					my $count_valeur_groupes_2 = scalar @valeur_groupes_2;
					for ( my $i = 0 ; $i < $count_valeur_groupes_2 ; $i++ ) {
						my @nb_groupe       = @{ $nb_groupes_2[$i] };
						my $count_nb_groupe = scalar @nb_groupe;
						push( @exist_groupe_2, [ $valeur_groupes_2[$i], $count_nb_groupe ] );
					}
					my @exist_groupe         = ();
					foreach my $group_1 (@exist_groupe_1){
						my $same=0;
						my $note=0;
						foreach my $groupe (@exist_groupe){
							if($group_1->[0]==$groupe->[0]){
								$same=1;
								last;	
							}
							$note=$note+1;
						}
						if($same==1){
							$exist_groupe[$note][1]=$exist_groupe[$note][1]+$group_1->[1];
						}else{
							push(@exist_groupe,$group_1);	
						}
					}
					foreach my $group_2 (@exist_groupe_2){
						my $same=0;
						my $note=0;
						foreach my $groupe (@exist_groupe){
							if($group_2->[0]==$groupe->[0]){
								$same=1;
								last;	
							}
							$note=$note+1;
						}
						if($same==1){
							$exist_groupe[$note][1]=$exist_groupe[$note][1]+$group_2->[1];
						}else{
							push(@exist_groupe,$group_2);	
						}
					}
					exist_split( $errors, \@exist_groupe, 0, [] );					
					my $count_result_branch = scalar @GLOBAL_CHARGE_result_branch;
					if ( $count_result_branch > 0 ) {
						get_result( \@GLOBAL_CHARGE_result_branch );
						if($GLOBAL_CHARGE_result_branch[0][0]!=0){
							unshift( @GLOBAL_CHARGE_results, $GLOBAL_CHARGE_result_branch[0][1] - $GLOBAL_CHARGE_result_branch[0][0] );
						}
					}					
					my @groupes_atom_1   = ();
					my @tmp_nb_groupes_1 = @nb_groupes_1;
					my @groupes_atom_2   = ();
					my @tmp_nb_groupes_2 = @nb_groupes_2;
					foreach my $element (@GLOBAL_CHARGE_results) {
						for ( my $i = 0 ; $i < $count_valeur_groupes_1 ; $i++ ) {
							if ( $element == $valeur_groupes_1[$i] ) {
								my @nb_groupe_1 = @{ $tmp_nb_groupes_1[$i] };
								my $count_nb_groupe_1=scalar @nb_groupe_1;
								if($count_nb_groupe_1>0){
									push( @groupes_atom_1, $nb_groupe_1[0] );
									shift(@nb_groupe_1);
									$tmp_nb_groupes_1[$i] = \@nb_groupe_1;	
								}else{
									for ( my $j = 0 ; $j < $count_valeur_groupes_2 ; $j++ ) {
										if ( $element == $valeur_groupes_2[$j] ) {
											my @nb_groupe_2 = @{ $tmp_nb_groupes_2[$j] };
											my $count_nb_groupe_2=scalar @nb_groupe_2;
											push( @groupes_atom_2, $nb_groupe_2[0] );
											shift(@nb_groupe_2);
											$tmp_nb_groupes_2[$j] = \@nb_groupe_2;	
										}
									}
								}
							}else{
								for ( my $j = 0 ; $j < $count_valeur_groupes_2 ; $j++ ) {	
									if ( $element == $valeur_groupes_2[$j] ) {
										my @nb_groupe_2 = @{ $tmp_nb_groupes_2[$j] };
										my $count_nb_groupe_2=scalar @nb_groupe_2;
										push( @groupes_atom_2, $nb_groupe_2[0] );
										shift(@nb_groupe_2);
										$tmp_nb_groupes_2[$j] = \@nb_groupe_2;	
									}
								}
							}
						}
					}					
					my @atoms_groupes_1 = @{ $re_groupes_1->[2] };
					
					foreach my $element (@groupes_atom_1) {
						push( @GLOBAL_atoms_1, @{ $atoms_groupes_1[$element] } );
					}					
					@GLOBAL_atoms_1 = sort { $a <=> $b } @GLOBAL_atoms_1;					
					my @atoms_groupes_2 = @{ $re_groupes_2->[2] };
					
					foreach my $element (@groupes_atom_2) {
						push( @GLOBAL_atoms_2, @{ $atoms_groupes_2[$element] } );
					}					
					@GLOBAL_atoms_2 = sort { $a <=> $b } @GLOBAL_atoms_2;																	
					
					if($charge_inter-$total_charges_inter>0){
						$GLOBAL_add_round=0.0001;
						if($COR_CHR==6){
							$GLOBAL_add_round=0.000001;
						}elsif($COR_CHR==5){
							$GLOBAL_add_round=0.00001;
						}elsif($COR_CHR==4){
							$GLOBAL_add_round=0.0001;
						}elsif($COR_CHR==3){
							$GLOBAL_add_round=0.001;
						}elsif($COR_CHR==2){
							$GLOBAL_add_round=0.01;
						}elsif($COR_CHR==1){
							$GLOBAL_add_round=0.1;
						}	
					}else{
						$GLOBAL_add_round=-0.0001;
						if($COR_CHR==6){
							$GLOBAL_add_round=-0.000001;
						}elsif($COR_CHR==5){
							$GLOBAL_add_round=-0.00001;
						}elsif($COR_CHR==4){
							$GLOBAL_add_round=-0.0001;
						}elsif($COR_CHR==3){
							$GLOBAL_add_round=-0.001;
						}elsif($COR_CHR==2){
							$GLOBAL_add_round=-0.01;
						}elsif($COR_CHR==1){
							$GLOBAL_add_round=-0.1;
						}	
					}					
					foreach my $numero_atom (@GLOBAL_atoms_1){
						my $nb_atom=$atoms_inter_1[$numero_atom]-1;
						$mol_charges[$mol_1-1][$nb_atom]=$mol_charges[$mol_1-1][$nb_atom]+$GLOBAL_add_round;
						push(@atoms_charge_edit,[$mol_1,$nb_atom]);
					}
					foreach my $numero_atom (@GLOBAL_atoms_2){
						my $nb_atom=$atoms_inter_2[$numero_atom]-1;
						$mol_charges[$mol_2-1][$nb_atom]=$mol_charges[$mol_2-1][$nb_atom]+$GLOBAL_add_round;
						push(@atoms_charge_edit,[$mol_2,$nb_atom]);
					}	
					my $count_GLOBAL_atoms_1=scalar @GLOBAL_atoms_1;
					my $count_GLOBAL_atoms_2=scalar @GLOBAL_atoms_2;
					if($count_GLOBAL_atoms_1==0&&$count_GLOBAL_atoms_2==0){
						print "\n\t\t\t         WARNING:\n\tMolecule mm INTER-MCC $mol_1 $mol_2 | $string_inter_1 | $string_inter_2 Charge correction not successful\n";	
					}										
				}
			}					
			for ( my $NM = 1 ; $NM <= $dfmol ; $NM++ ) {
				my @intra_inter_mcc=();
				foreach my $intra_mcc(@GLOBAL_intra_mcc){
					if($intra_mcc->[0]==$NM){
						push(@intra_inter_mcc,@{$intra_mcc->[2]});
					}
				}
				foreach my $inter_mcc(@GLOBAL_inter_mcc){
					if($inter_mcc->[0]==$NM){
						push(@intra_inter_mcc,@{$inter_mcc->[3]});
					}
					if($inter_mcc->[1]==$NM){
						push(@intra_inter_mcc,@{$inter_mcc->[4]});
					}
				}
				my @atoms_others=();
				my @name_atoms=();
				my $total_charges=0;
					
				for(my $i=0; $i<$nbatoms[$NM]; $i++){
					my $same=0;
					foreach my $meqa (@GLOBAL_inter_meqa){
						if($NM==$meqa->[0]&&$i+1==$meqa->[1]){
							$same=1;
						}
					}					
					foreach my $intra_inter (@intra_inter_mcc){
						if($i==$intra_inter-1){
							$same=1;
						}
					}
					if($same==0){
						push(@atoms_others,$i);
						push(@name_atoms,$tab[0][$i][$NM]);
					}
					$total_charges=$total_charges+$mol_charges[$NM-1][$i];
				}
				my $total_charge=0;
				my $errors=nearest( .0001,abs($CHR_VAL[$NM]-$total_charges))*10000;
				if($COR_CHR==6){
					$errors=nearest( .000001,abs($CHR_VAL[$NM]-$total_charges))*1000000;
				}elsif($COR_CHR==5){
					$errors=nearest( .00001,abs($CHR_VAL[$NM]-$total_charges))*100000;
				}elsif($COR_CHR==4){
					$errors=nearest( .0001,abs($CHR_VAL[$NM]-$total_charges))*10000;
				}elsif($COR_CHR==3){
					$errors=nearest( .001,abs($CHR_VAL[$NM]-$total_charges))*1000;
				}elsif($COR_CHR==2){
					$errors=nearest( .01,abs($CHR_VAL[$NM]-$total_charges))*100;
				}elsif($COR_CHR==1){
					$errors=nearest( .1,abs($CHR_VAL[$NM]-$total_charges))*10;
				}	
				our $GLOBAL_CHARGE_times         = 0;
				our $GLOBAL_CHARGE_exist_groupe  = 0;
				our @GLOBAL_CHARGE_result_branch = ();
				our @GLOBAL_CHARGE_results       = ();			
				our @GLOBAL_atoms         = ();
				our $GLOBAL_add_round=0;
				if($errors>0){					
					my $re_groupes = groupes(\@name_atoms,$errors);						
					my @valeur_groupes       = @{ $re_groupes->[0] };
					my @nb_groupes           = @{ $re_groupes->[1] };
					my @exist_groupe         = ();
					my $count_valeur_groupes = scalar @valeur_groupes;
					for ( my $i = 0 ; $i < $count_valeur_groupes ; $i++ ) {
						my @nb_groupe       = @{ $nb_groupes[$i] };
						my $count_nb_groupe = scalar @nb_groupe;
						push( @exist_groupe, [ $valeur_groupes[$i], $count_nb_groupe ] );
					}						
					exist_split( $errors, \@exist_groupe, 0, [] );						
					my $count_result_branch = scalar @GLOBAL_CHARGE_result_branch;
					if ( $count_result_branch > 0 ) {
						get_result( \@GLOBAL_CHARGE_result_branch );
						if($GLOBAL_CHARGE_result_branch[0][0]!=0){
							unshift( @GLOBAL_CHARGE_results, $GLOBAL_CHARGE_result_branch[0][1] - $GLOBAL_CHARGE_result_branch[0][0] );
						}
					}					
					my @groupes_atom   = ();
					my @tmp_nb_groupes = @nb_groupes;
					foreach my $element (@GLOBAL_CHARGE_results) {
						for ( my $i = 0 ; $i < $count_valeur_groupes ; $i++ ) {
							if ( $element == $valeur_groupes[$i] ) {
								my @nb_groupe = @{ $tmp_nb_groupes[$i] };
								push( @groupes_atom, $nb_groupe[0] );
								shift(@nb_groupe);
								$tmp_nb_groupes[$i] = \@nb_groupe;
							}
						}
					}						
					my @atoms_groupes = @{ $re_groupes->[2] };
						
					foreach my $element (@groupes_atom) {
						push( @GLOBAL_atoms, @{ $atoms_groupes[$element] } );
					}
						
					@GLOBAL_atoms = sort { $a <=> $b } @GLOBAL_atoms;						
						
					if($CHR_VAL[$NM]-$total_charges>0){
						$GLOBAL_add_round=0.0001;
						if($COR_CHR==6){
							$GLOBAL_add_round=0.000001;
						}elsif($COR_CHR==5){
							$GLOBAL_add_round=0.00001;
						}elsif($COR_CHR==4){
							$GLOBAL_add_round=0.0001;
						}elsif($COR_CHR==3){
							$GLOBAL_add_round=0.001;
						}elsif($COR_CHR==2){
							$GLOBAL_add_round=0.01;
						}elsif($COR_CHR==1){
							$GLOBAL_add_round=0.1;
						}	
					}else{
						$GLOBAL_add_round=-0.0001;
						if($COR_CHR==6){
							$GLOBAL_add_round=-0.000001;
						}elsif($COR_CHR==5){
							$GLOBAL_add_round=-0.00001;
						}elsif($COR_CHR==4){
							$GLOBAL_add_round=-0.0001;
						}elsif($COR_CHR==3){
							$GLOBAL_add_round=-0.001;
						}elsif($COR_CHR==2){
							$GLOBAL_add_round=-0.01;
						}elsif($COR_CHR==1){
							$GLOBAL_add_round=-0.1;
						}	
					}						
					foreach my $numero_atom (@GLOBAL_atoms){
						my $nb_atom=$atoms_others[$numero_atom];
						$mol_charges[$NM-1][$nb_atom]=$mol_charges[$NM-1][$nb_atom]+$GLOBAL_add_round;
						push(@atoms_charge_edit,[$NM,$nb_atom]);
					}
					my $count_GLOBAL_atoms=scalar @GLOBAL_atoms;
					if($count_GLOBAL_atoms==0){
						print "\n\t\t\t         WARNING:\n\tMolecule mm $NM Charge correction not successful\n";	
					}								
				}				
			}		
			
							
			format CHARGESLOG_cc6_1 =
@## @<<<      @##.###### @##.###### @##.###### @<
$icharge+1,$tab[10][$icharge][$imol],$mol_charges_origin[$imol-1][$icharge],$mol_charges_back[$imol-1][$icharge],$mol_charges[$imol-1][$icharge],$mark_round
.
			format CHARGESLOG_cc5_1 =
@## @<<<      @##.###### @##.##### @##.##### @<
$icharge+1,$tab[10][$icharge][$imol],$mol_charges_origin[$imol-1][$icharge],$mol_charges_back[$imol-1][$icharge],$mol_charges[$imol-1][$icharge],$mark_round
.
			format CHARGESLOG_cc4_1 =
@## @<<<      @##.###### @##.#### @##.#### @<
$icharge+1,$tab[10][$icharge][$imol],$mol_charges_origin[$imol-1][$icharge],$mol_charges_back[$imol-1][$icharge],$mol_charges[$imol-1][$icharge],$mark_round
.
			format CHARGESLOG_cc3_1 =
@## @<<<      @##.###### @##.### @##.### @<
$icharge+1,$tab[10][$icharge][$imol],$mol_charges_origin[$imol-1][$icharge],$mol_charges_back[$imol-1][$icharge],$mol_charges[$imol-1][$icharge],$mark_round
.
			format CHARGESLOG_cc2_1 =
@## @<<<      @##.###### @##.## @##.## @<
$icharge+1,$tab[10][$icharge][$imol],$mol_charges_origin[$imol-1][$icharge],$mol_charges_back[$imol-1][$icharge],$mol_charges[$imol-1][$icharge],$mark_round
.
			format CHARGESLOG_cc1_1 =
@## @<<<      @##.###### @##.# @##.# @<
$icharge+1,$tab[10][$icharge][$imol],$mol_charges_origin[$imol-1][$icharge],$mol_charges_back[$imol-1][$icharge],$mol_charges[$imol-1][$icharge],$mark_round
.
			
					
			if($COR_CHR==6){
				format_name CHARGESLOG_FILE "CHARGESLOG_cc6_1";
			}elsif($COR_CHR==5){
				format_name CHARGESLOG_FILE "CHARGESLOG_cc5_1";
			}elsif($COR_CHR==4){
				format_name CHARGESLOG_FILE "CHARGESLOG_cc4_1";
			}elsif($COR_CHR==3){
				format_name CHARGESLOG_FILE "CHARGESLOG_cc3_1";
			}elsif($COR_CHR==2){
				format_name CHARGESLOG_FILE "CHARGESLOG_cc2_1";
			}elsif($COR_CHR==1){
				format_name CHARGESLOG_FILE "CHARGESLOG_cc1_1";
			}
			open (CHARGESLOG_FILE, ">mm.CHARGES.log");
			for ( $imol = 1 ; $imol <= $dfmol ; $imol++ ) {
				printf CHARGESLOG_FILE "MOLECULE $imol - $TITLE[$imol]\n";
				for($icharge=0; $icharge<$nbatoms[$imol]; $icharge++){
					$mark_round="";
					if($mol_charges_back[$imol-1][$icharge]!=$mol_charges[$imol-1][$icharge]){
						$mark_round="!";
					}
					write CHARGESLOG_FILE;
				}
				printf CHARGESLOG_FILE "\n";
			}
			close (CHARGESLOG_FILE);		
									
		}
		#******************************RED-2012******************************
		
			for($NM=1; $NM<=$dfmol; $NM++){
				if($nbconect[$NM]!=0){
format MOL2imeqbis =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.#### ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
format MOL2imeq =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.#### ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.

#******************************RED-2012******************************
format MOL2imeqbis_cc6 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.###### ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
format MOL2imeq_cc6 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.###### ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
format MOL2imeqbis_cc5 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.##### ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
format MOL2imeq_cc5 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.##### ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
format MOL2imeqbis_cc3 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.### ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
format MOL2imeq_cc3 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.### ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
format MOL2imeqbis_cc2 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.## ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
format MOL2imeq_cc2 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.## ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
format MOL2imeqbis_cc1 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.# ****
$in,$tab[10][$i-1][$NM],$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.
format MOL2imeq_cc1 =
@## @<<<      @##.######  @##.######  @##.###### @<<<     @> @<<<<    @##.# ****
$in,$atom,$coord[0][$i-1][$NC][$NM],$coord[1][$i-1][$NC][$NM],$coord[2][$i-1][$NC][$NM],$element,$resmol,$tab[4][$i-1][$NM],$potelect
.

					#******************************RED-2012******************************
					if($COR_CHR==6){
						if($atombrut[$NM]==1){ format_name MOL2_FILE_IMEQ "MOL2imeqbis_cc6"; }
							else{ format_name MOL2_FILE_IMEQ "MOL2imeq_cc6"; }
					}elsif($COR_CHR==5){
						if($atombrut[$NM]==1){ format_name MOL2_FILE_IMEQ "MOL2imeqbis_cc5"; }
							else{ format_name MOL2_FILE_IMEQ "MOL2imeq_cc5"; }
					}elsif($COR_CHR==3){
						if($atombrut[$NM]==1){ format_name MOL2_FILE_IMEQ "MOL2imeqbis_cc3"; }
							else{ format_name MOL2_FILE_IMEQ "MOL2imeq_cc3"; }
					}elsif($COR_CHR==2){
						if($atombrut[$NM]==1){ format_name MOL2_FILE_IMEQ "MOL2imeqbis_cc2"; }
							else{ format_name MOL2_FILE_IMEQ "MOL2imeq_cc2"; }
					}elsif($COR_CHR==1){
						if($atombrut[$NM]==1){ format_name MOL2_FILE_IMEQ "MOL2imeqbis_cc1"; }
							else{ format_name MOL2_FILE_IMEQ "MOL2imeq_cc1"; }
					}else{
					#******************************RED-2012******************************
						
						if($atombrut[$NM]==1){ format_name MOL2_FILE_IMEQ "MOL2imeqbis"; }
							else{ format_name MOL2_FILE_IMEQ "MOL2imeq"; }
					#******************************RED-2012******************************
					}
					#******************************RED-2012******************************
					
					for($NC=0; $NC<$nbconf[$NM]; $NC++){
						$NC++;
						open (MOL2_FILE_IMEQ, ">Mol_m$NM-o$NC-mm2.mol2");
						$NC--;
						$cmptatoms=$il=$testnom=0;
						$rescpt=1;
						for($i=1; $i<=$nbatoms[$NM]; $i++){
							$testr=0;
							if($i==1){ $rescpt=1; }
							for($y=0; $y<=$imrcount[$NM]; $y++){
								if(!defined($intramr[4][$y][$NM])){ $intramr[4][$y][$NM]=0; }
								if(!defined($intramr[3][$y][$NM])){ $intramr[3][$y][$NM]=""; }
								for($w=0;$w<=$intramr[4][$y][$NM];$w++){
									if(!defined($intratom[$w][$y][$NM])){ $intratom[$w][$y][$NM]=0; }
									if(($intratom[$w][$y][$NM]==$i) && ($intramr[3][$y][$NM]!~/[K]/)){ $testr=1; }
								}
							}
							if($testr==1){ $cmptatoms++; }
							if($testr==0){
								$saveres[2][$il][$NM]=$residu[$i-1][$NM];
								$saveres[5][$il][$NM]=$tab[4][$i-1][$NM];
								if($il == 0){ $molname2=$saveres[5][$il][$NM]; }
								elsif($il != 0){
									if($saveres[2][$il-1][$NM]!=$saveres[2][$il][$NM]){
										$rescpt++; $testnom=1;
										$molname2=$molname2."-".$saveres[5][$il][$NM];
									}
								}
								$il++;
							}
						}
						$cmptatoms=$nbatoms[$NM]-$cmptatoms;
						$cmptconnect=0;
						for($i=0; $i<$nbconect[$NM]; $i++){
							($at1,$at2)=(split(/\-/,$conections[$i][$NM])); 
							$testc2=0;
							for($y=0; $y<$imrcount[$NM]; $y++){
								for($w=0; $w<$intramr[4][$y][$NM]; $w++){
									if((($intratom[$w][$y][$NM]==$at1) && ($intramr[3][$y][$NM]!~/[K]/)) || (($intratom[$w][$y][$NM]==$at2) && ($intramr[3][$y][$NM]!~/[K]/))) { $testc2=1; }
								}
							}
							if($testc2==1){ $cmptconnect++; }
						}
						$cmptconnect=$nbconect[$NM]-$cmptconnect;
						if($testnom==1){ printf MOL2_FILE_IMEQ ("@<TRIPOS>MOLECULE\n%s\n",$molname2);
						}else{ printf MOL2_FILE_IMEQ ("@<TRIPOS>MOLECULE\n%s\n",$saveres[5][0][$NM]); }
						printf MOL2_FILE_IMEQ ("%5d %5d %5d     0     1\n",$cmptatoms,$cmptconnect,$rescpt);
						printf MOL2_FILE_IMEQ ("SMALL\nUSER_CHARGES\n@<TRIPOS>ATOM\n");
						$flag=$i=0;
						if(($CHR_TYP eq "DEBUG")||($CHR_TYP eq "RESP-A1")||($CHR_TYP eq "RESP-C1")){
							open (PCH_FILE, "<punch2_mm");
							foreach(<PCH_FILE>){
								if(/    NO   At\.No\.    q0           q\(opt\)   IVARY  d\(rstr\)\/dq/ig){ $flag=1; }
								if(/        Statistics of the fitting:/ig){ $flag=2; }
								if($flag==1){	$i++;}
								if(($i>=1)&&($flag == 1)){ ($averageimeq[$i-1])=(split(' '))[3]; }
							}
							close(PCH_FILE);
						}
						if(($CHR_TYP eq "ESP-A1")||($CHR_TYP eq "ESP-C1")||($CHR_TYP eq "RESP-A2")||($CHR_TYP eq "RESP-C2")){
							open (PCH_FILE, "<punch1_mm");
							foreach(<PCH_FILE>){
								if(/    NO   At\.No\.    q0           q\(opt\)   IVARY  d\(rstr\)\/dq/ig) { $flag=1; }
								if(/        Statistics of the fitting:/ig) { $flag=2; }
								if($flag==1){ $i++; }
								if(($i>=1) && ($flag == 1)){ ($averageimeq[$i-1])=(split(' '))[3]; }
							}
							close(PCH_FILE);
						}
						$i=$in=0; $resmol=1; $ir=1; $natom=1;
						if($NM==1){ $natom=1; }
						else{
							for($h=1; $h<$NM; $h++){ $natom=$natom+($nbatoms[$h]*$nbconf[$h]*$nbmod[$h]); }
						}
						for($j=0; $j<$nbatoms[$NM]; $j++){
							$atom=$tab[1][$i][$NM];
							if( ($tab[1][$i][$NM] =~ /T$/) ){ $atom=~s/T//; }
							$potelect=$averageimeq[$i+$natom];
							if($j==0){ $resmol=1; }
							$i++;
							$element=$atom;
							$atom="$atom"."$ir";
							$y=$w=$molimr=0;
							for($y=0; $y<=$imrcount[$NM]; $y++){
								if(!defined($intramr[4][$y][$NM])){ $intramr[4][$y][$NM]=0; }
								if(!defined($intramr[3][$y][$NM])){ $intramr[3][$y][$NM]=""; }
								for($w=0; $w<=$intramr[4][$y][$NM]; $w++){
									if(!defined($intratom[$w][$y][$NM])){ $intratom[$w][$y][$NM]=0; }
									if(($intratom[$w][$y][$NM]==$i) && ($intramr[3][$y][$NM]!~/[K]/)) { $molimr=1; }
								}
							}
							if($molimr==0){
								$saveres[1][$in][$NM]=$resmol;
								$saveres[2][$in][$NM]=$residu[$j][$NM];
								$saveres[3][$in][$NM]=$tab[4][$j][$NM];
								if ($in != 0){
									if($saveres[2][$in-1][$NM] != $saveres[2][$in][$NM]){ $resmol++; }
								}
								$ir++; $in++;
								$save[$i]=$in;
								
								#******************************RED-2012******************************
								if ( $right_charge == 1 ) {
									my $same = 0;
									foreach my $atom_charge_edit (@atoms_charge_edit) {
										if ( $NM == $atom_charge_edit->[0] && $j == $atom_charge_edit->[1] ) {
											$potelect = $mol_charges[ $NM - 1 ][$j];
											$same     = 1;
										}
									}
									if ( $same == 0 ) {
										my $potelect_round = nearest( .0001, $potelect );
										my $round          = $potelect_round - $potelect;
										my $round_5        = abs( abs($round) - 0.00005 );
										my $round_add      = 0.000001;
										if ( $COR_CHR == 6 ) {
											$potelect_round = nearest( .0001, $potelect );
											$round          = $potelect_round - $potelect;
											$round_5        = abs( abs($round) - 0.00005 );
											$round_add      = 0.000001;
										} elsif ( $COR_CHR == 5 ) {
											$potelect_round = nearest( .00001, $potelect );
											$round          = $potelect_round - $potelect;
											$round_5        = abs( abs($round) - 0.000005 );
											$round_add      = 0.0000001;
										} elsif ( $COR_CHR == 4 ) {
											$potelect_round = nearest( .0001, $potelect );
											$round          = $potelect_round - $potelect;
											$round_5        = abs( abs($round) - 0.00005 );
											$round_add      = 0.000001;
										} elsif ( $COR_CHR == 3 ) {
											$potelect_round = nearest( .001, $potelect );
											$round          = $potelect_round - $potelect;
											$round_5        = abs( abs($round) - 0.0005 );
											$round_add      = 0.00001;
										} elsif ( $COR_CHR == 2 ) {
											$potelect_round = nearest( .01, $potelect );
											$round          = $potelect_round - $potelect;
											$round_5        = abs( abs($round) - 0.005 );
											$round_add      = 0.0001;
										} elsif ( $COR_CHR == 1 ) {
											$potelect_round = nearest( .1, $potelect );
											$round          = $potelect_round - $potelect;
											$round_5        = abs( abs($round) - 0.05 );
											$round_add      = 0.001;
										}
										if ( $round_5 < 0.00000000001 ) {
											if ( $round > 0 ) {
												$potelect = $potelect + $round_add;
											} else {
												$potelect = $potelect - $round_add;
											}
										}
									}
							
								}			
								#******************************RED-2012******************************
								
								write MOL2_FILE_IMEQ;
							}
						}
						$ic=$i=0;
						printf MOL2_FILE_IMEQ ("@<TRIPOS>BOND\n");
						for($i=0; $i<$nbconect[$NM]; $i++){
							($at1,$at2)=(split(/\-/,$conections[$i][$NM]));
							$y=$w=$testc=0;
							for($y=0; $y<=$imrcount[$NM]; $y++){
								for($w=0; $w<=$intramr[4][$y][$NM]; $w++){
									if((($intratom[$w][$y][$NM]==$at1) && ($intramr[3][$y][$NM]!~/[K]/)) || (($intratom[$w][$y][$NM]==$at2) && ($intramr[3][$y][$NM]!~/[K]/))) { $testc=1; }
								}
							}
							if($testc==0){ printf MOL2_FILE_IMEQ ("%5d %5d %5d 1\n",$ic+1,$save[$at1],$save[$at2]); $ic++; }
						}
						printf MOL2_FILE_IMEQ ("@<TRIPOS>SUBSTRUCTURE\n");
						$z=1;
						for($i=1; $i<$in; $i++){
							if($i==1){
								printf MOL2_FILE_IMEQ (" %6d %4s         %6d ****               0 ****  ****  \n",1,$saveres[3][$i][$NM],1);
							}elsif($saveres[2][$i-1][$NM] != $saveres[2][$i][$NM]){
								$z++;
								printf MOL2_FILE_IMEQ (" %6d %4s         %6d ****               0 ****  ****  \n",$z,$saveres[3][$i][$NM],$i+1);
							}
						}
						print MOL2_FILE_IMEQ "\n\n";
						close (MOL2_FILE_IMEQ);
					}
				}
			}
			$rg=0;
			for($NM=1; $NM<=$dfmol; $NM++){
				if($nbconect[$NM]!=0){
					if($rg==0){ print "\n\n\tThe following Tripos mol2 file(s) has/have been created."; $rg++ }
					print "\n\t";
					for ($NC=1; $NC<=$nbconf[$NM]; $NC++){ print "Mol_m$NM-o$NC-mm2.mol2 "; }  # Whole molecules
					if($NM==$dfmol){ print "\n"; }
				}
			}
		}
	}
}
#---------------------------------------------------------------------------------------------------------
#------------------------------------------- Directory ---------------------------------------------------
#---------------------------------------------------------------------------------------------------------
sub Directory{
	if($OPT_Calc eq "ON") {
		$zip=0;
		if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
		if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
		if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
		chomp($bzip2=`which bzip2`);
		if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
		if(($bzip2 =~ m/Command not found/ig)||($bzip2 =~ m/not in/ig)||($bzip2 =~ m/no bzip2 in/ig)||($bzip2 eq "")) { $zip=1; }
		elsif (($QMSOFT eq "GAMESS") || ($QMSOFT eq "FIREFLY")) { system ("bzip2 JOB1*.dat "); }
		elsif ($QMSOFT eq "GAUSSIAN") { system ("bzip2 JOB1*.chk "); }
		if ($zip==1){
			if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
			if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
			if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
			chomp($gzip=`which gzip`);
			if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
			if(($gzip =~ m/Command not found/ig)||($gzip =~ m/not in/ig)||($gzip =~ m/no gzip in/ig)||($gzip eq "")) { $zip=2; }
			elsif (($QMSOFT eq "GAMESS") || ($QMSOFT eq "FIREFLY")) { system ("gzip -9 JOB1*.dat "); }
			elsif ($QMSOFT eq "GAUSSIAN") { system ("gzip -9 JOB1*.chk "); }
		}
		if ($zip==2){
			if($CHR_TYP ne "DEBUG"){ open(STDERR,">/dev/null");  }
			if($CHR_TYP ne "DEBUG"){ open(OLDSTDOUT,">&STDOUT"); }
			if($CHR_TYP ne "DEBUG"){ open(STDOUT,">/dev/null");  }
			chomp($comp=`which compress`);
			if($CHR_TYP ne "DEBUG"){ open(STDOUT,">&OLDSTDOUT"); }
			if(($comp =~ m/Command not found/ig)||($comp =~ m/not in/ig)||($comp =~ m/no compress in/ig)||($comp eq "")) {}
			elsif (($QMSOFT eq "GAMESS") || ($QMSOFT eq "FIREFLY")) { system ("compress JOB1*.dat "); }
			elsif ($QMSOFT eq "GAUSSIAN") { system ("compress JOB1*.chk "); }
		}
	}
	if (!-e "$DIR"){ system ("mkdir $DIR"); }
	else{
		$X = 1;
		while (-e "$DIR-".$X){ $X++; }
		rename ("$DIR","$DIR-".$X);
		system ("mkdir $DIR");
	}
	if($dfmol == 1){ system ("mv *_m1* $DIR"); }
	if($dfmol != 1){
		if (($CHR_TYP ne "ESP-A2") && ($CHR_TYP ne "ESP-C2")) {
			if (!-e "./Mol_MM") { system ("mkdir Mol_MM"); }
			system ("mv *mm* Mol_MM");
			system ("mv Mol_MM $DIR");
		}
		for($NM=1; $NM<=$dfmol; $NM++) {
			if (!-e "./Mol_m$NM") { system ("mkdir Mol_m$NM"); }
			system ("mv Mol_m$NM $DIR");
			# if ($Re_Fit eq "ON") {	system ("mv es*_m$NM *1_m$NM *2_m$NM *_m$NM-* *_m$NM.* $DIR/Mol_m$NM"); }
			# else { 			system ("mv es*_m$NM *1_m$NM *2_m$NM *_m$NM-* *_m$NM.* $DIR/Mol_m$NM"); }
			system ("mv es*_m$NM *1_m$NM *2_m$NM *_m$NM-* *_m$NM.* $DIR/Mol_m$NM");
		}
	}
	print "\n\n\tCharge values & force field libraries are available in\n\t\tthe \"$DIR\" directory.\n";
}
#---------------------------------------------------------------------------------------------------------
#----------------------------------------- Information ---------------------------------------------------
#---------------------------------------------------------------------------------------------------------
sub Information{
	if ($check==1) { Directory(); }
	$finish = time();
	$during = $finish-$start;
	$hours = int($during/3600);
	$minutes = int(($during/60)-($hours*60));
	$secondes = int($during-($hours*3600+$minutes*60));
	print "\n\t\tExecution time: $hours h $minutes m $secondes s\n\n";
	print " *************************************************************************
  R.E.D. I was developed \@ the \"Faculte de Pharmacie\" in Amiens by:
           A.Pigache,(1) P.Cieplak(2) & F.-Y.Dupradeau(1)\n
  R.E.D. II was developed in D.A.Case's laboratory at \"TSRI\" by:
         T.Zaffran,(1,3) P.Cieplak(2) & F.-Y.Dupradeau(1,3)\n
  R.E.D. III.x developments were initiated in D.A.Case's laboratory \@ TSRI
        & are now carried out \@ the \"UFR de Pharmacie\" in Amiens by:
  F.Wang,(5) E.Garcia,(5) N.Grivel,(1,3) P.Cieplak(4) & F.-Y.Dupradeau(1,3,5)\n
  R.E.D. IV is developed \@ the \"UFR de Pharmacie\" in Amiens by:
       F.Wang,(5) W.Rozanski,(5) E.Garcia,(5) D.Lelong,(5) P.Cieplak(4) 
                       & F.-Y.Dupradeau(5)\n
  (1) DMAG EA 3901 & Faculte de Pharmacie, Amiens, France
  (2) Accelrys Inc., San Diego, USA
  (3) D.A.Case's lab., The Scripps Research Institute, La Jolla, CA, USA
  (4) Sanford|Burnham Institute for Medical Research, La Jolla, CA, USA
  (5) CNRS UMR 6219 & UFR de Pharmacie, Amiens, France
 *************************************************************************
     R.E.D. III.5 is distributed under the GNU General Public License
 *************************************************************************
  Do you need a new feature which is not yet implemented in R.E.D.-III.5?
                contact the q4md force field tools team \@
                   contact\@q4md-forcefieldtools.org

           Regularly look for bug fixes at the R.E.D. home page

                 To use R.E.D. IV, see R.E.D. Server \@
                  http://q4md-forcefieldtools.org/REDS/
                                ----
       Please, submit your force field library(ies) to R.E.DD.B. \@
                http://q4md-forcefieldtools.org/REDDB/
   to freely review & share your results within the scientific community
                                ----
           Do you need help about the q4md force field tools?
        Please, use the q4md-forcefieldtools.org mailing list \@
                http://lists.q4md-forcefieldtools.org/
 *************************************************************************\n\n";
}
#---------------------------------------------------------------------------------------------------------
#------------------------------------------ X Terminal ---------------------------------------------------
#---------------------------------------------------------------------------------------------------------
sub XTerminal{
	chomp($OS=uc(`uname`));
	if (!($#ARGV==0 and $ARGV[0] eq "--term")){
		# If perl_4.x & perl_5.x are in the system, binary "perl" = perl_4.x and "perl5" = perl_5.x, replace "perl" by "perl5" as below:
		if ($OS =~ /IRIX/)     { system ("winterm -fg white -bg black -geometry 95x60+300+400 -title R.E.D.-III.5 -e perl $0 --term &");}
		# system ("winterm -fg white -bg black -geometry 71x30+329+400 -title R.E.D. -e perl5 $0 --term &"); 
		#                                                                            85 x 50 (height x width) +X+Y (X,Y related to the top-left corner)
		elsif ($OS =~ /LINUX/) { system ("xterm  -b 10 -sb -ms black -fg white -bg black -geometry 95x60+250+30  -title R.E.D.-III.5 -e perl $0 --term &"); }
		elsif ($OS =~ /DARWIN/){ system ("xterm  -b 10 -sb -ms black -fg white -bg black -geometry 95x60+250+30  -title R.E.D.-III.5 -e perl $0 --term &"); } # Mac OS
		elsif ($OS =~ /CYGWIN/){ system ("xterm  -b 10 -sb -ms black -fg white -bg black -geometry 95x60+250+30  -title R.E.D.-III.5 -e perl $0 --term &"); } # Windows
		elsif ($OS =~ /AIX/)   { system ("dtterm -b 10 -sb -ms black -fg white -bg black -geometry 95x60+300+400 -title R.E.D.-III.5 -e perl $0 --term &"); }
		elsif ($OS =~ /HP-UX/) { system ("dtterm -b 10 -sb -ms black -fg white -bg black -geometry 95x60+300+400 -title R.E.D.-III.5 -e perl $0 --term &"); }
		elsif ($OS =~ /SUNOS/) { system ("dtterm -b 10 -sb -ms black -fg white -bg black -geometry 95x60+300+400 -title R.E.D.-III.5 -e perl $0 --term &"); }
		# Replace "xterm" by another X-window terminal like "dtterm" ?
		else		       { system ("xterm  -b 10 -sb -ms black -fg white -bg black -geometry 95x60+300+400 -title R.E.D.-III.5 -e perl $0 --term &"); }
		exit(0);
	}
}
#*********************************************************************************************************
#						MAIN PROGRAM
#*********************************************************************************************************
#----------- Variables that can be modified in R.E.D.: See HowTo.pdf as well ------------

$XRED   = "OFF";	  # If XRED="ON", R.E.D. will be executed using the XRED graphical interface.
$NP     = "1";		  # Number of cpu(s)/core(s) used in parallel in QM calculations.
$QMSOFT = "GAMESS";	  # "GAMESS" (GAMESS-US or WinGAMESS), "Firefly" (PC-GAMESS), or "GAUSSIAN" (g09, g03, g98 or g94) is used in QM calculations.

$DIR     = "Data-RED"; 	  # Directory name where the final data will be stored.

$OPT_Calc    = "Off";	  # Geometry optimization will be carried out only if $OPT_Calc = "ON".
$MEPCHR_Calc = "On";	  # MEP computation & charge fitting will be carried out if $MEPCHR_Calc = "ON".
$Re_Fit  = "Off";	  # Charges are re-fitted & force field libraries re-built from a previous R.E.D. job.

$CHR_TYP = "RESP-A1";	  # Charge derivation models: "RESP-A1, RESP-A2, RESP-C1, RESP-C2, ESP-A1, ESP-A2, ESP-C1, ESP-C2".
			  # -1- RESP-A1: HF/6-31G* Connolly surface algo., 2 stage RESP fit qwt=.0005/.001
			  # -2- RESP-A2: HF/6-31G* Connolly surface algo., 1 stage RESP fit qwt=.01
			  # -3- RESP-C1: HF/6-31G* CHELPG algo., 2 stage RESP fit qwt=.0005/.001
			  # -4- RESP-C2: HF/6-31G* CHELPG algo., 1 stage RESP fit qwt=.01
			  # -5- ESP-A1: HF/6-31G* Connolly surface algo., 1 stage RESP fit qwt=.0000
			  # -6- ESP-A2: HF/STO-3G Connolly surface algo., 1 stage RESP fit qwt=.0000
			  # -7- ESP-C1: HF/6-31G* CHELPG algo., 1 stage RESP fit qwt=.0000
			  # -8- ESP-C2: HF/STO-3G CHELPG algo., 1 stage RESP fit qwt=.0000
			  # -9- DEBUG: Do not use the DEBUG mode for generating correct charge values !!!
			  
$COR_CHR = "4"; 	  # Correct charge value rounding off errors at an accuracy defined by the user
			  # 0 : no correction is performed
			  # 6 : correction at ± 1.10-6 e			# 3 : correction at ± 1.10-3 e (pay attention)
			  # 5 : correction at ± 1.10-5 e			# 2 : correction at ± 1.10-2 e (pay attention)
			  # 4 : correction at ± 1.10-4 e (default)		# 1 : correction at ± 1.10-1 e (pay attention)

%Elements = ('H' =>"1",'LI' =>"3",'BE' =>"4",'B' =>"5",'C' =>"6",'CT' =>"6",'N' =>"7",'NT' =>"7",'O' =>"8",'OT' =>"8",'F' =>"9",'NA' =>"11",'MG' =>"12",'AL' =>"13",'SI' =>"14",'SIT' => "14",'P' =>"15",'PT' =>"15",'S' =>"16",'ST' =>"16",'CL' =>"17",'K' =>"19",'CA' =>"20",'SC'=>"21",'TI' => "22",'V'=>"23",'CR' =>"24",'MN'=>"25",'FE' =>"26",'CO' =>"27",'NI' =>"28",'CU' =>"29",'ZN' =>"30",'GA' =>"31",'GE' =>"32",'AS' =>"33",'SE' =>"34",'BR' =>"35");
#---------------------- Beginning of the prog. -------------------
# system("sleep 10");
$check=1;
$start=time();
Verification();
OPT_Calcul();
MEP_Calcul();
CHR_Calcul();
INTER_Calcul();
Information();
if ($XRED eq "ON") { print "\n\t\tDone, press Enter to exit.\n"; <STDIN>; }
