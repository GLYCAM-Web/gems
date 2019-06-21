#include <glylib.h>
#include <AMBER/amber.h>

#define USAGE "\n\
\tdetect_shape input.top input.crd config_file \n\
	or \n\
\tdetect_shape input.pdb configgg_file \n"

plane get_plane_test(int n,coord_3D **r);
//double get_signed_distance_from_point_to_plane(plane p, coord_3D pt );

int main(int argc,char *argv[]){

if(argc<3){mywhineusage("Insufficient number of arguments on command line.",USAGE);}
if(argc>4){mywhineusage("Too many arguments on command line.",USAGE);}

assembly A;
assembly *B;
fileset Tset,Cset,Pset,Oset,Caset;
fileslurp Pslurp;
int i=0,j=0,k=0,no=4,timestep=1,mi,ri,ai,test=0,a_size=6,temp_size,dum,tempresno,resno,hcheck=0,cut_check=0;
char *atom;
atom=(char*)calloc(4,sizeof(char));
char *path;
path=(char*)calloc(1000,sizeof(char));
double *maximum;
maximum = (double*)calloc(15,sizeof(double));
double *d;
d=(double*)calloc(6,sizeof(double));
double dihedral;
double *fifteen_dihedrals;
fifteen_dihedrals=(double*)calloc(16,sizeof(double));
plane *fifteen_planes;
fifteen_planes=(plane*)calloc(16,sizeof(plane));
coord_3D **four;
four=(coord_3D**)calloc(60,sizeof(coord_3D*));
char **names;
names = (char**)calloc(6,sizeof(char*));
coord_3D **ring;
ring=(coord_3D**)calloc(6,sizeof(coord_3D*));

/* creating output files conformations.txt,ranks.txt and opening them for writing*/
char *output = NULL;
output=(char*)calloc(23,sizeof(char));
sprintf(output,"ring_conformations.txt");
Oset.N=strdup(output);
Oset.F=myfopen(Oset.N,"w");

/* opening and reading all the input files*/
if(argc==4){
Tset.N=strdup(argv[1]);//topology file
Tset.F=myfopen(Tset.N,"r");
A=load_amber_prmtop(Tset);
Cset.N=strdup(argv[2]);//coordinate file
Cset.F=myfopen(Cset.N,"r");
Pset.N=strdup(argv[3]);//input file
Pset.F=myfopen(Pset.N,"r");
Pslurp = slurp_file(Pset);
}

if(argc==3){
Tset.N=strdup(argv[1]);
Tset.F=myfopen(Tset.N,"r");
B=load_pdb(Tset.N);

printf("just loaded the pdb\n");

Pset.N=strdup(argv[2]);//input file
Pset.F=myfopen(Pset.N,"r");
Pslurp = slurp_file(Pset);
}


/* reading the input file with atom names and residue numbers*/
int cut_off=0,cut_off1=0;
while(i<Pslurp.n){
	/*if(strstr(Pslurp.L[i],"Number") != NULL){
		i++;
		sscanf(Pslurp.L[i],"%d",&dum);
		a_size=dum;
		//printf("a_size is %d allocating space to names\n",a_size);
		names=(char**)calloc(a_size,sizeof(char*));
		}*/
	if(strstr(Pslurp.L[i],"Atom") != NULL){
		i++;
		while(strstr(Pslurp.L[i],"Residue") == NULL){
			//if(j>0) printf("1.  names[%d] is >>>%s<<<\n",j-1,names[j-1]);
			sscanf(Pslurp.L[i],"%s",atom);
			//names[j]=(char*)calloc(strlen(atom),sizeof(char));
			names[j]=strdup(atom);
			//printf("2.  names[%d] is >>>%s<<<\n",j,names[j]);
			i++;
			j++;
		}
	}
	if(strstr(Pslurp.L[i],"Residue") != NULL){
		i++;
		sscanf(Pslurp.L[i],"%d",&dum);
		resno=dum;
		}	
	if(strstr(Pslurp.L[i],"Cutoff") != NULL){
		i++;
		sscanf(Pslurp.L[i],"%d",&dum);
		cut_off=dum;
		cut_off1= 0-dum;
		cut_check=1;
	}
	if(strstr(Pslurp.L[i],"Path") != NULL){
		i++;
		sscanf(Pslurp.L[i],"%s",path);
	}	
	
	i++;
}

printf("path is %s\n",path);
if(cut_check==0){
	cut_off=10;
	cut_off1=0-cut_off;
}
//printf("resno is %d\n",resno);
//printf("a_size is %d\n",a_size);
//printf("first atom name is %s\n",names[0]);
printf("cut-off is %d\n",cut_off);

i=0;
j=0;
k=0;

/*** determining if the input file is a trajectory or a restart file ***/
char ctype;
if(argc==4){
char line[2000];
fgets(line,2000,Cset.F); /* get line 1 */
fgets(line,2000,Cset.F); /* get line 2 */
if(line[4]=='.'){ /* is the entry an integer or a float? */
ctype='c';
}
else{
ctype='r';
}
//printf("ctype is %c\n",ctype);
rewind(Cset.F);
test=fgetc(Cset.F);
}

if(argc==3){
test=fgetc(Tset.F);
}


temp_size=0;
tempresno=1;
//printf("test is %d\n",test);

fprintf(Oset.F,"Timestep\tStandard Nomenclature\tRing conformation\n");
//printf("Timestep\tRingstate\t\n");



/*extracting the coordinates of the ring and storing them in an array named ring*/
/*at every time step we are calculating all possible planes, best plane, and then detecting the best conformation based on the planes*/
while(test != EOF){
	if(argc==4){
		ungetc(test,Cset.F);
		//printf("test 2 is %d\n",test);
		add_trajcrds_to_prmtop_assembly(Cset,&A,ctype,0);
		//printf("adding coordinates to trajectory\n");
		fprintf(Oset.F,"\n");
		//printf("\n");
		//printf("%d\t",timestep);
		fprintf(Oset.F,"%d\t\t",timestep);
		timestep++;
		if(timestep>1){
			k=0;
			j=0;
			tempresno =1;
			temp_size=0;
		}
	}
	else{
		fprintf(Oset.F,"%d\t\t",timestep);
	}
	//printf("The number of molecules found are %d\n",A.nm);
	//printf("a_size is %d\t",a_size);
	if(argc==4){
	for(mi=0;mi<A.nm;mi++){
		//printf("The number of residues in molecule %d are %d\n",mi+1,A.m[mi][0].nr);
		for(ri=0;ri<A.m[mi][0].nr;ri++){
			//printf("The residue number is %d\n",A.m[mi][0].r[ri].n);
			//res_num = tempresno;
			//tempresno++;
			if(A.m[mi][0].r[ri].n ==resno){
				while(temp_size<a_size){
					ai=0;
					while(ai<A.m[mi][0].r[ri].na){
						if(strstr(A.m[mi][0].r[ri].a[ai].N,names[temp_size]) != NULL){
							ring[temp_size]=&A.m[mi][0].r[ri].a[ai].xa[0];
							ai=A.m[mi][0].r[ri].na;
						}
					ai++;
					}
				temp_size++;
				}


			}
	
		}
	}
	}

	if(argc==3){	
		for(mi=0;mi<B[0].nm;mi++){
                //printf("The number of residues in molecule %d are %d\n",mi+1,A[0].m[mi][0].nr);
                	for(ri=0;ri<B[0].m[mi][0].nr;ri++){
				//printf("The residue number is %d\n",B[0].m[mi][0].r[ri].n);
                        	//res_num = tempresno;
                        	//tempresno++;
                        	if(B[0].m[mi][0].r[ri].n ==resno){
                                	//printf("resnum is %d and a_size is %d\n",res_num,a_size);
                                	while(temp_size<a_size){
                                        	ai=0;
                                        	while(ai<B[0].m[mi][0].r[ri].na){
                                                	if(strstr(B[0].m[mi][0].r[ri].a[ai].N,names[temp_size]) != NULL){
                                                        	//dprint_coord_3D(&A[0].m[mi][0].r[ri].a[ai].x);
                                                        	ring[temp_size]=&B[0].m[mi][0].r[ri].a[ai].x;
                                                        	ai=B[0].m[mi][0].r[ri].na;
                                                	}
                                        	ai++;
                                        	}
                                	temp_size++;
                                	}

			
                        	}

                	}
        	}
	}



	//printf("six ring coordinates\n");
	//dprint_coord_3D(&ring[0][0]);
	//dprint_coord_3D(&ring[1][0]);
	//dprint_coord_3D(&ring[2][0]);
	//dprint_coord_3D(&ring[3][0]);
	//dprint_coord_3D(&ring[4][0]);
	//dprint_coord_3D(&ring[5][0]);

	//int list[60] = {1,2,3,4,1,2,3,5,1,2,3,6,1,2,4,5,1,2,4,6,1,2,5,6,1,3,4,5,1,3,4,6,1,3,5,6,1,4,5,6,2,3,4,5,2,3,4,6,2,3,5,6,2,4,5,6,3,4,5,6};
	int list[60] =   {0,1,2,3,0,1,2,4,0,1,2,5,0,1,3,4,0,1,3,5,0,1,4,5,0,2,3,4,0,2,3,5,0,2,4,5,0,3,4,5,1,2,3,4,1,2,3,5,1,2,4,5,1,3,4,5,2,3,4,5};
	//int secondlist[30] = {5,6,4,6,4,5,3,6,3,5,3,4,2,6,2,5,2,4,2,3,1,6,1,5,1,4,1,3,1,2};
	int secondlist[30] =   {4,5,3,5,3,4,2,5,2,4,2,3,1,5,1,4,1,3,1,2,0,5,0,4,0,3,0,2,0,1};

	char *conformers[16] = {"q","t","q","d","t","q","t","d","t","q","q","t","d","t","q"};
	//printf(" list is %d\n",list[3]);
	/*calculating the dihedral angles and planes*/
	
	double temp_dihedral,temp_dihedral1,temp_dihedral2,temp_dihedral3;
	j=0;
	for(i=0;i<15;i++){
			
		temp_dihedral=get_dihedral_ABCD_points(ring[list[j]][0],ring[list[j+1]][0],ring[list[j+2]][0],ring[list[j+3]][0]);	
		temp_dihedral1=get_dihedral_ABCD_points(ring[list[j+1]][0],ring[list[j+2]][0],ring[list[j+3]][0],ring[list[j]][0]);
		temp_dihedral2=get_dihedral_ABCD_points(ring[list[j+2]][0],ring[list[j+3]][0],ring[list[j]][0],ring[list[j+1]][0]);
		temp_dihedral3=	get_dihedral_ABCD_points(ring[list[j+3]][0],ring[list[j]][0],ring[list[j+1]][0],ring[list[j+2]][0]);	
		fifteen_dihedrals[i]=(fabs(temp_dihedral)+fabs(temp_dihedral1)+fabs(temp_dihedral2)+fabs(temp_dihedral3))/4*(180/PI);
		//printf("average_dihedrals are %lf\n",fifteen_dihedrals[i]);

		j=j+4;
		
	}
	i=0;
	j=0;



	for(i=0;i<15;i++){
		//printf("Plane %d dihedral atoms are %d %d %d %d\n",i+1,list[j],list[j+1],list[j+2],list[j+3]);
		dihedral=get_dihedral_ABCD_points(ring[list[j]][0],ring[list[j+1]][0],ring[list[j+2]][0],ring[list[j+3]][0]);
		four[0]=&ring[list[j]][0];
		four[1]=&ring[list[j+1]][0];
		four[2]=&ring[list[j+2]][0];
		four[3]=&ring[list[j+3]][0];
		fifteen_planes[i]=get_plane_for_ring(no,four);
		//dprint_plane(&fifteen_planes[i]);
		//dprint_coord_3D(&ring[list[j]][0]);
		//dprint_coord_3D(&ring[list[j+1]][0]);
		//dprint_coord_3D(&ring[list[j+2]][0]);
		//dprint_coord_3D(&ring[list[j+3]][0]);
		//fifteen_dihedrals[i]=dihedral*(180/PI);
		//printf("%lf\n",fifteen_dihedrals[i]);
		j=j+4;
		//printf("plane %d\n",i+1);
	}


	

	/*filtering all the planes with dihedral angles less than 10*/
	int no_planes=0;
	int bpsize=0;
	int sdsize=0;
	int *bestplanes;
	bestplanes=(int*)calloc(0,sizeof(int));
	int *sortedplanes;
	sortedplanes=(int*)calloc(0,sizeof(int));
	double *tendihedrals;
	tendihedrals=(double*)calloc(0,sizeof(double));
	double *sortdihedrals;
	sortdihedrals=(double*)calloc(0,sizeof(double));
	double *threedihedrals;
	threedihedrals=(double*)calloc(3,sizeof(double));		

	
	for(i=0;i<15;i++){
		if(fifteen_dihedrals[i]<=cut_off && fifteen_dihedrals[i]>=cut_off1){
			bpsize++;
			bestplanes=(int*)realloc(bestplanes,(bpsize*sizeof(int)));
			bestplanes[bpsize-1]=i;
			tendihedrals=(double*)realloc(tendihedrals,(bpsize*sizeof(double)));
			tendihedrals[bpsize-1]=fifteen_dihedrals[i];
			sortdihedrals=(double*)realloc(sortdihedrals,(bpsize*sizeof(double)));
			sortdihedrals[bpsize-1]=fifteen_dihedrals[i];
			//printf("%f\n",fabs(tendihedrals[bpsize-1]));
			no_planes++;
			//printf("the planes are %d\n",i+1);
		}
	}			
	
	double temp;
	for(i=0;i<bpsize;i++){
		for(j=i;j<bpsize;j++){
			if(fabs(sortdihedrals[i]) > fabs(sortdihedrals[j])){
				temp=sortdihedrals[i];
				sortdihedrals[i]=sortdihedrals[j];
				sortdihedrals[j]=temp;
			}
		}
	}
	
	for(i=0;i<bpsize;i++){
		for(j=0;j<bpsize;j++){
			if(sortdihedrals[i]==tendihedrals[j]){
				sdsize++;
				sortedplanes=(int*)realloc(sortedplanes,(sdsize*sizeof(int)));
				sortedplanes[sdsize-1]=bestplanes[j];
				//printf("the sorted dihedrals are %f and planes are %d\n",sortdihedrals[i],bestplanes[j]);
			}
		}
	}


	//printf("sdsize is %d\n",sdsize);	
		
	for(i=0;i<sdsize;i++){
		//printf("sortedplanes are %d\n",sortedplanes[i]);
	}


		

	/*calculating the six dihedrals around the ring to check if it is a flat ring or an envelope*/
	j=0;
	//int six_list[25]= {1,2,3,4,2,3,4,5,3,4,5,6,4,5,6,1,5,6,1,2,6,1,2,3}
	int six_list[25]= {0,1,2,3,1,2,3,4,2,3,4,5,3,4,5,0,4,5,0,1,5,0,1,2};
	double *six_dihedrals;
	int sixcheck=0;
	six_dihedrals=(double*)calloc(7,sizeof(double));
	for(i=0;i<6;i++){
		//dprint_coord_3D(&ring[six_list[j]][0]);
                //dprint_coord_3D(&ring[six_list[j+1]][0]);
                //dprint_coord_3D(&ring[six_list[j+2]][0]);
                //dprint_coord_3D(&ring[six_list[j+3]][0]);
		dihedral=get_dihedral_ABCD_points(ring[six_list[j]][0],ring[six_list[j+1]][0],ring[six_list[j+2]][0],ring[six_list[j+3]][0]);
		six_dihedrals[i]=dihedral*(180/PI);
		if(six_dihedrals[i]<=5 && six_dihedrals[i]>=-5){
			sixcheck++;
		}
		j=j+4;
	}

	if(sixcheck==6){
		fprintf(Oset.F,"F\t");
		//printf("This is a flat ring\n");
	}


	for(i=0;i<6;i++){
		//printf("%lf\t",six_dihedrals[i]);
	}


int envelope_check=0;
int pre_e_check=0;
	//printf("%lf\t",fabs(fabs(six_dihedrals[0])-fabs(six_dihedrals[5])));		
	if(fabs(fabs(six_dihedrals[0])-fabs(six_dihedrals[3])) <= 6.0){
		pre_e_check++;
	}
	//printf("%lf\t",fabs(fabs(six_dihedrals[1])-fabs(six_dihedrals[4])));
	 if(fabs(fabs(six_dihedrals[1])-fabs(six_dihedrals[2])) <= 5.0){
                pre_e_check++;
        }
	//printf("%lf\t",fabs(fabs(six_dihedrals[2])-fabs(six_dihedrals[3])));
	 if(fabs(fabs(six_dihedrals[4])-fabs(six_dihedrals[5])) <= 9.0){
                pre_e_check++;
        }
//printf("pre check is %d\n",pre_e_check);

if(pre_e_check<3){
	pre_e_check=0;
	if(fabs(fabs(six_dihedrals[1])-fabs(six_dihedrals[4])) <= 6.0){
                pre_e_check++;
        }
         if(fabs(fabs(six_dihedrals[2])-fabs(six_dihedrals[3])) <= 5.0){
                pre_e_check++;
        }
         if(fabs(fabs(six_dihedrals[5])-fabs(six_dihedrals[0])) <= 9.0){
                pre_e_check++;
        }
}

if(pre_e_check<3){
        pre_e_check=0;
        if(fabs(fabs(six_dihedrals[2])-fabs(six_dihedrals[5])) <= 6.0){
                pre_e_check++;
        }
         if(fabs(fabs(six_dihedrals[3])-fabs(six_dihedrals[4])) <= 5.0){
                pre_e_check++;
        }
         if(fabs(fabs(six_dihedrals[0])-fabs(six_dihedrals[1])) <= 9.0){
                pre_e_check++;
        }
}


if(pre_e_check<3){
        pre_e_check=0;
        if(fabs(fabs(six_dihedrals[0])-fabs(six_dihedrals[3])) <= 6.0){
                pre_e_check++;
        }
         if(fabs(fabs(six_dihedrals[4])-fabs(six_dihedrals[5])) <= 5.0){
                pre_e_check++;
        }
         if(fabs(fabs(six_dihedrals[1])-fabs(six_dihedrals[2])) <= 9.0){
                pre_e_check++;
        }
}

if(pre_e_check<3){
        pre_e_check=0;
        if(fabs(fabs(six_dihedrals[1])-fabs(six_dihedrals[4])) <= 6.0){
                pre_e_check++;
        }
         if(fabs(fabs(six_dihedrals[5])-fabs(six_dihedrals[0])) <= 5.0){
                pre_e_check++;
        }
         if(fabs(fabs(six_dihedrals[2])-fabs(six_dihedrals[3])) <= 9.0){
                pre_e_check++;
        }
}

if(pre_e_check<3){
        pre_e_check=0;
        if(fabs(fabs(six_dihedrals[2])-fabs(six_dihedrals[5])) <= 6.0){
                pre_e_check++;
        }
         if(fabs(fabs(six_dihedrals[0])-fabs(six_dihedrals[1])) <= 5.0){
                pre_e_check++;
        }
         if(fabs(fabs(six_dihedrals[3])-fabs(six_dihedrals[4])) <= 9.0){
                pre_e_check++;
        }
}


if(pre_e_check==3){
        envelope_check=1;
}

/*checking if there are two consecutive bad torsion angles in a row*/
	int *envelope_planes;
	envelope_planes=(int*)calloc(0,sizeof(int));
	int ssize;
	int esize=0;
	/*int *forty_planes;
	forty_planes=(int*)calloc(0,sizeof(int));
	int fosize=0;
	int esize=0;
	int ssize;
	int k=0;
	int fivecheck=0;
	if(sixcheck !=6 ){	
		for(i=0;i<1;i++){
			//printf("%lf and %lf\n",six_dihedrals[0],six_dihedrals[1]);
			if((six_dihedrals[0] >=36.0 || six_dihedrals[0] <=-36.0) && (six_dihedrals[1]>=36.0 || six_dihedrals[1]<=-36.0)){
				fivecheck++;
				for(i=0;i<2;i++){
					fosize++;
					forty_planes=(int*)realloc(forty_planes,(fosize*sizeof(int)));
					forty_planes[fosize-1]=i;
				}
			}
			//printf("%lf and %lf\n",six_dihedrals[1],six_dihedrals[2]);
			if((six_dihedrals[1] >=36.0 || six_dihedrals[1] <=-36.0) && (six_dihedrals[2]>=36.0 || six_dihedrals[2]<=-36.0)){
                 	       	fivecheck++;
				for(i=1;i<3;i++){
					fosize++;
					forty_planes=(int*)realloc(forty_planes,(fosize*sizeof(int)));
					forty_planes[fosize-1]=i;
				}
					
                	}
			//printf("%lf and %lf\n",six_dihedrals[2],six_dihedrals[3]);
			if((six_dihedrals[2] >=36.0 || six_dihedrals[2] <=-36.0) && (six_dihedrals[3]>=36.0 || six_dihedrals[3]<=-36.0)){
                		fivecheck++;
				for(i=2;i<4;i++){
					fosize++;
					forty_planes=(int*)realloc(forty_planes,(fosize*sizeof(int)));
					forty_planes[fosize-1]=i;
				}
                	}
			//printf("%lf and %lf\n",six_dihedrals[3],six_dihedrals[4]);
			if((six_dihedrals[3] >=36.0 || six_dihedrals[3] <=-36.0) && (six_dihedrals[4]>=36.0 || six_dihedrals[4]<=-36.0)){
                        	fivecheck++;
				for(i=3;i<5;i++){
					fosize++;
					forty_planes=(int*)realloc(forty_planes,(fosize*sizeof(int)));
					forty_planes[fosize-1]=i;
				}
			
                	}
			//printf("%lf and %lf\n",six_dihedrals[4],six_dihedrals[5]);
			if((six_dihedrals[4] >=36.0 || six_dihedrals[4] <=-36.0) && (six_dihedrals[5]>=36.0 || six_dihedrals[5]<=-36.0)){
                        	fivecheck++;
				for(i=4;i<6;i++){
					fosize++;
					forty_planes=(int*)realloc(forty_planes,(fosize*sizeof(int)));
					forty_planes[fosize-1]=i;
				}
                	}
			//printf("%lf and %lf\n",six_dihedrals[5],six_dihedrals[0]);
			if((six_dihedrals[5] >=36.0 || six_dihedrals[5] <=-36.0) && (six_dihedrals[0]>=36.0 || six_dihedrals[0]<=-36.0)){
                        	fivecheck++;
				fosize++;
                                forty_planes=(int*)realloc(forty_planes,(fosize*sizeof(int)));
                                forty_planes[fosize-1]=5;
				fosize++;
                                forty_planes=(int*)realloc(forty_planes,(fosize*sizeof(int)));
                                forty_planes[fosize-1]=0;
				
                	}
		}
	}
//printf("fivecheck is %d\n",fivecheck);

if(fivecheck==1){
	//printf("This is an envelope\n");
}

for(i=0;i<fosize;i++){
	//printf("The dihedrals are %d\n",forty_planes[i]);
}

int *thirty_planes;
thirty_planes=(int*)calloc(0,sizeof(int));
int tsize=0;
int focheck=0;
if(fivecheck==1){
	for(i=0;i<6;i++){
		//printf("forty_planes[0] is %d and forty_planes[1] is %d\n",forty_planes[0],forty_planes[1]);
		if(i!= forty_planes[0] && i!= forty_planes[1]){
			//printf("inside if %d\n",i);
			if(six_dihedrals[i]>30.0 || six_dihedrals[i]<-30.0){
				tsize++;
				thirty_planes=(int*)realloc(thirty_planes,(tsize*sizeof(int)));
				thirty_planes[tsize-1]=i;
				focheck++;
				
			}
		}	
	}
}
	
//printf("thirty planes are %d\n",thirty_planes[0]);

//printf("focheck is %d\n",focheck);
int thcheck=0;

if(focheck ==1){
	//printf("inside focheck\n");
	for(i=0;i<6;i++){
		if(i != forty_planes[0] && i!= forty_planes[1]){
			if(i!=thirty_planes[0]){
				//printf("inside if\n");
				if((six_dihedrals[i]>=20.0 && six_dihedrals[i]<=30.0) || (six_dihedrals[i]<=-20.0 && six_dihedrals[i]>=-30.0)){
					thcheck=1;
				}
			}
		}
	}
} 

//printf("thcheck is %d\n",thcheck);*/
/*checking if the opposite angles are less than zero*/
int fiveplanes=0;
int fivecheck2=0;
if(envelope_check==1){
	 for(i=0;i<1;i++){
                        //printf("%lf and %lf\n",six_dihedrals[0],six_dihedrals[1]);
                        if((six_dihedrals[0] <=12.0 && six_dihedrals[0] >=-12.0) && (six_dihedrals[1]<=12.0 && six_dihedrals[1]>=-12.0)){
                                fivecheck2=1;
				ssize=0;
				for(j=ssize;j<ssize+8;j++){
					esize++;
					envelope_planes=(int*)realloc(envelope_planes,(esize*sizeof(int)));
					envelope_planes[esize-1]=six_list[j];
	
				}
				//printf("yes\n");
				fiveplanes++;
                        }
                        //printf("%lf and %lf\n",six_dihedrals[1],six_dihedrals[2]);
                        if((six_dihedrals[1] <=12.0 && six_dihedrals[1] >=-12.0) && (six_dihedrals[2]<=12.0 && six_dihedrals[2]>=-12.0)){
                                fivecheck2=1;
				ssize=4;
				for(j=ssize;j<ssize+8;j++){
                                        esize++;
                                        envelope_planes=(int*)realloc(envelope_planes,(esize*sizeof(int)));
                                        envelope_planes[esize-1]=six_list[j];

                                }
				//printf("yes\n");
				fiveplanes++;
                        }
                        //printf("%lf and %lf\n",six_dihedrals[2],six_dihedrals[3]);
                        if((six_dihedrals[2] <=12.0 && six_dihedrals[2] >=-12.0) && (six_dihedrals[3]<=12.0 && six_dihedrals[3]>=-12.0)){
                                fivecheck2=1;
				ssize=8;
                                for(j=ssize;j<ssize+8;j++){
                                        esize++;
                                        envelope_planes=(int*)realloc(envelope_planes,(esize*sizeof(int)));
                                        envelope_planes[esize-1]=six_list[j];

                                }
				//printf("yes\n");
				fiveplanes++;
                        }
                        //printf("%lf and %lf\n",six_dihedrals[3],six_dihedrals[4]);
                        if((six_dihedrals[3] <=12.0 && six_dihedrals[3] >=-12.0) && (six_dihedrals[4]<=12.0 && six_dihedrals[4]>=-12.0)){
                                fivecheck2=1;
				ssize=12;
                                for(j=ssize;j<ssize+8;j++){
                                        esize++;
                                        envelope_planes=(int*)realloc(envelope_planes,(esize*sizeof(int)));
                                        envelope_planes[esize-1]=six_list[j];

                                }
				//printf("yes\n");
				fiveplanes++;
                        }
                        //printf("%lf and %lf\n",six_dihedrals[4],six_dihedrals[5]);
                        if((six_dihedrals[4] <=12.0 && six_dihedrals[4] >=-12.0) && (six_dihedrals[5]<=12.0 && six_dihedrals[5]>=-12.0)){
                                fivecheck2=1;
				ssize=16;
                                for(j=ssize;j<ssize+8;j++){
                                        esize++;
                                        envelope_planes=(int*)realloc(envelope_planes,(esize*sizeof(int)));
                                        envelope_planes[esize-1]=six_list[j];

                                }
				//printf("yes\n");
				fiveplanes++;
                        }
                        //printf("%lf and %lf\n",six_dihedrals[5],six_dihedrals[0]);
                        if((six_dihedrals[5] <=12.0 && six_dihedrals[5] >=-12.0) && (six_dihedrals[0]<=12.0 && six_dihedrals[0]>=-12.0)){
                                fivecheck2=1;
				ssize=20;
                                for(j=ssize;j<ssize+4;j++){
                                        esize++;
                                        envelope_planes=(int*)realloc(envelope_planes,(esize*sizeof(int)));
                                        envelope_planes[esize-1]=six_list[j];

                                }
				ssize=0;
				for(j=ssize;j<ssize+4;j++){
                                        esize++;
                                        envelope_planes=(int*)realloc(envelope_planes,(esize*sizeof(int)));
                                        envelope_planes[esize-1]=six_list[j];

                                }
				//printf("yes\n");
				fiveplanes++;
                        }
                }

}
		

//printf("five planes is %d\n",fiveplanes*2);

/*for(i=0;i<esize;i++){
	printf("%d\n",envelope_planes[i]);
}*/


/*determining the conformation of the envelope*/
i=0;
j=0;
int echeck=0;
int fsize=0;
int *fiveatom_planes;
fiveatom_planes=(int*)calloc(0,sizeof(int));

if(envelope_check==1 && fivecheck2==1){
	//printf("fiveatomplane\n");
	while(i<fiveplanes*2*4){
		j=i;
		while(j<i+4){
			echeck=0;
			for(k=i+4;k<i+8;k++){
				if(envelope_planes[j] == envelope_planes[k]){
					//printf("%d\n",envelope_planes[k]);
					echeck=1;
				}
			}
			if(echeck==0){
				fsize++;
				fiveatom_planes=(int*)realloc(fiveatom_planes,(fsize*sizeof(fiveatom_planes)));
				fiveatom_planes[fsize-1]=envelope_planes[j];
				for(k=i+4;k<i+8;k++){
					fsize++;
					fiveatom_planes=(int*)realloc(fiveatom_planes,(fsize*sizeof(fiveatom_planes)));
                        		fiveatom_planes[fsize-1]=envelope_planes[k];
				}
				j=i+4;
			//printf("%d\n",envelope_planes[j]);
			}
		
			j++;
		}

		i=i+8;
	}//while(i<fiveplanes*2*4)
				

	for(i=0;i<fsize;i++){
		//printf("%d\n",fiveatom_planes[i]);
	}

	int ringatoms[6]= {0,1,2,3,4,5};
	ssize=0;
	int *sixth_atom;
	sixth_atom=(int*)calloc(0,sizeof(sixth_atom));
	i=0;
	while(i<fiveplanes*5){
		j=i;
		k=0;
		while(k<6){
			echeck=0;
			for(j=i;j<i+5;j++){
				if(fiveatom_planes[j]==ringatoms[k]){
					echeck=1;
				}
			}
		
			if(echeck==0){
				//printf("%d\n",ringatoms[k]);
				ssize++;
				sixth_atom=(int*)realloc(sixth_atom,(ssize*sizeof*(sixth_atom)));
				sixth_atom[ssize-1]=ringatoms[k];

			}
			k++;
		}

		i=i+5;
	}//while (i<fiveplanes*5)

	coord_3D **five;
	five=(coord_3D**)calloc(6,sizeof(coord_3D*));
	plane *fiveatomplane;
	fiveatomplane=(plane*)calloc(1,sizeof(plane)); 
	int n=5;

	for(i=0;i<fiveplanes;i++){
		five[0]=&ring[fiveatom_planes[i]][0];
		five[1]=&ring[fiveatom_planes[i+1]][0];
		five[2]=&ring[fiveatom_planes[i+2]][0];
        	five[3]=&ring[fiveatom_planes[i+3]][0];
        	five[4]=&ring[fiveatom_planes[i+4]][0];
		fiveatomplane[0]=get_plane_for_ring(n,five);
		d[i]=get_signed_distance_from_point_to_plane(fiveatomplane[0],ring[sixth_atom[i]][0]);
		//printf("distances are %f\n",d[i]);

	}

	double min=0.0;
	int min_atom=0;
	min=d[0];
	min_atom=sixth_atom[0];
	for(i=0;i<fiveplanes;i++){
		if(d[i]<min){
			min=d[i];
			min_atom=sixth_atom[i];
		}
	}


	if(min<0.0){
		fprintf(Oset.F,"\tE%d\t",min_atom+1);
		fprintf(Oset.F,"\tp%d\t",min_atom+1);
	}	
	else{
		fprintf(Oset.F,"\t%dE\t",min_atom+1);
		fprintf(Oset.F,"\t%dp\t",min_atom+1);
	}
//	printf("The min distance is %f and the atom is %d\n",min,min_atom+1);

}



//printf("%d and %d \n",fivecheck,fivecheck2);

if(fivecheck2==0){
	//printf("The number of good planes are %d\n",no_planes);
}

/*char *canonicals;
canonicals=(char*)calloc(87,sizeof(char));
sprintf(canonicals,"/home/spandana/programs/ring_torsions/shapeid_working/shapeid_dihedrals/canonicals.txt");*/
/*if(argc==5){
Caset.N=strdup(argv[4]);
}
//printf("here\n");
if(argc==4){
Caset.N=strdup(argv[3]);
//printf("done\n");
}*/

if(fivecheck2==0 && no_planes==0){
	fprintf(Oset.F,"\t-\t\t\tm\t");
}


//Cset.N=strdup(canonicals);
Caset.N=strdup(path);
fileslurp Cslurp;
Cslurp=slurp_file(Caset);
char cname[6];
int dum1,dum2,dum3,dum4,dum5,dum6,dum7,dum8,dum9,dum10,dum11,dum12;
int *atoms;
atoms=(int*)calloc(13,sizeof(int));
int j=0;k=0;
int match=0,match1=0,ccheck=0,bcheck=0;

if(fivecheck2==0 && no_planes>0){
	
	if(sdsize>=3){
	for(i=0;i<Cslurp.n;i++){
		sscanf(Cslurp.L[i],"%s",cname);
		//printf("%s\n",cname);	
		if(strstr(cname,"chair") != NULL){
			sscanf(Cslurp.L[i],"%s%d%d%d%d%d%d%d%d%d%d%d%d",cname,&dum1,&dum2,&dum3,&dum4,&dum5,&dum6,&dum7,&dum8,&dum9,&dum10,&dum11,&dum12);
			atoms[0]=dum1;atoms[1]=dum2;atoms[2]=dum3;atoms[3]=dum4;atoms[4]=dum5;atoms[5]=dum6;atoms[6]=dum7;atoms[7]=dum8;atoms[8]=dum9;atoms[9]=dum10;atoms[10]=dum11;atoms[11]=dum12;	
		}		
	}//for	
	}
	while(j<3){
		k=0;
		while(k<12){
			match=0;
			if(list[sortedplanes[j]*4] == atoms[k]){
				match++;
			}
			if(list[sortedplanes[j]*4+1]== atoms[k+1]){
				match++;
                        } 
			if(list[sortedplanes[j]*4+2] == atoms[k+2]){
				match++;
                        }
			if(list[sortedplanes[j]*4+3] == atoms[k+3]){
				match++;
                        } 
			if(match==4){
				k=12;
			}
			k=k+4;
				
		}//while k
		//printf("match is %d\n",match);
		if(match==4){
			match1++;
		}
		j++;
	}//while no_planes
		
	//printf("match1 is %d\n",match1);
	if(match1==3){
		d[0]=get_signed_distance_from_point_to_plane(fifteen_planes[12],ring[3][0]);
		d[1]=get_signed_distance_from_point_to_plane(fifteen_planes[12],ring[0][0]);
		//printf("the distances are %f and %f\n",d[0],d[1]);
		if(d[0]<0.0 && d[1] > 0.0){
			fprintf(Oset.F,"\t1C4\t");
		}
		if(d[0]>0.0 && d[1] <0.0){
			fprintf(Oset.F,"\t4C1\t");
		}	
					
		ccheck=1;
		//printf("This is a chair\n");
		}//match1==3	

	//printf("ccheck is %d\n",ccheck);
	if(ccheck==0 && sdsize >=3){
		match=0;
		match1=0;
		int bnum=1;
		j=0;k=0;
		for(i=0;i<Cslurp.n;i++){
			char conf_name[6];	
			sprintf(conf_name,"boat%d",bnum);
			sscanf(Cslurp.L[i],"%s",cname);
			//printf("%s and conf_name %s\n",cname,conf_name);
			if(strstr(cname,conf_name) != NULL){
				sscanf(Cslurp.L[i],"%s%d%d%d%d%d%d%d%d%d%d%d%d",cname,&dum1,&dum2,&dum3,&dum4,&dum5,&dum6,&dum7,&dum8,&dum9,&dum10,&dum11,&dum12);
				atoms[0]=dum1;atoms[1]=dum2;atoms[2]=dum3;atoms[3]=dum4;atoms[4]=dum5;atoms[5]=dum6;atoms[6]=dum7;atoms[7]=dum8;atoms[8]=dum9;atoms[9]=dum10;atoms[10]=dum11;atoms[11]=dum12;		
				//printf("%s\n",conf_name);
				bnum++;
				j=0;
				match1=0;
				while(j<sdsize){
					k=0;
					match=0;
					while(k<12){
						match=0;
						if(list[sortedplanes[j]*4] == atoms[k]){
							match++;
						}
						if(list[sortedplanes[j]*4+1] == atoms[k+1]){
							match++;
                                                }
						if(list[sortedplanes[j]*4+2] == atoms[k+2]){
							match++;
                                                }
						if(list[sortedplanes[j]*4+3] == atoms[k+3]){
							match++;
                                                }
						if(match==4){
							k=12;
						}	
						k=k+4;
						}
						j++;
						//printf("match is %d\n",match);
						if(match==4){
							match1++;
						}							

				}//j<no_planes	
			}
					
					//printf("match1 is %d\n",match1);
					
			if(match1==3){
				//printf("cname is %s\n",cname);
				//bcheck=1;
				if(strstr(cname,"boat1") != NULL){
					d[0]=get_signed_distance_from_point_to_plane(fifteen_planes[12],ring[3][0]);
					d[1]=get_signed_distance_from_point_to_plane(fifteen_planes[12],ring[0][0]);
					if(d[0]>0.0 && d[1]>0.0){
						bcheck=1;
						fprintf(Oset.F,"\t14B\t");	
					}
					if(d[0]<0.0 && d[1]<0.0){
						bcheck=1;
						fprintf(Oset.F,"\tB14\t");
					}
							
				}
				if(strstr(cname,"boat2") != NULL){
					d[0]=get_signed_distance_from_point_to_plane(fifteen_planes[3],ring[2][0]);
                                        d[1]=get_signed_distance_from_point_to_plane(fifteen_planes[3],ring[5][0]);
                                        if(d[0]>0.0 && d[1]>0.0){
                                        	fprintf(Oset.F,"\tO3B\t");
						bcheck=1;
                                        }
                                        if(d[0]<0.0 && d[1]<0.0){
                                        	fprintf(Oset.F,"\tBO3\t");
						bcheck=1;
                                        }

				}
				if(strstr(cname,"boat3") != NULL){
					d[0]=get_signed_distance_from_point_to_plane(fifteen_planes[7],ring[1][0]);
                                        d[1]=get_signed_distance_from_point_to_plane(fifteen_planes[7],ring[4][0]);
                                        if(d[0]>0.0 && d[1]>0.0){
                                        	fprintf(Oset.F,"\t25B\t");
						bcheck=1;
                                        }
                                        if(d[0]<0.0 && d[1]<0.0){
                                        	fprintf(Oset.F,"\tB25\t");
						bcheck=1;
                                        }
				}
					//printf("This is a boat\n");
					i=Cslurp.n;
			}
					
		}//for				
				
	
	}//if ccheck=0;

	//printf("ccheck and bcheck are %d and %d\n",bcheck,ccheck);


	int scheck=0;
	int snum=1;
	int nsize=0;
	match1=0;
	match=0;
	if(ccheck==0 && bcheck==0){
	for(i=0;i<Cslurp.n;i++){
		char conf_name[6];
                sprintf(conf_name,"Skew%d",snum);
                sscanf(Cslurp.L[i],"%s",cname);
                //printf("%s and conf_name %s\n",cname,conf_name);
                if(strstr(cname,conf_name) != NULL){
			sscanf(Cslurp.L[i],"%s%d%d%d%d%d%d%d%d",cname,&dum1,&dum2,&dum3,&dum4,&dum5,&dum6,&dum7,&dum8);
			atoms[0]=dum1;atoms[1]=dum2;atoms[2]=dum3;atoms[3]=dum4;atoms[4]=dum5;atoms[5]=dum6;atoms[6]=dum7;atoms[7]=dum8;
			//printf("%s\n",conf_name);
                        snum++;
                        j=0;
                        match1=0;
			if(sdsize>=3){
				nsize=3;
			}
			else{
				nsize=sdsize;
			}
			//printf("nsize is %d\n",nsize);
                        while(j<nsize){
				//printf("j is %d\n",j);
                        	k=0;
                                match=0;
                                while(k<8){
                                	match=0;
                                        if(list[sortedplanes[j]*4] == atoms[k]){
                                        	match++;
                                        }
                                        if(list[sortedplanes[j]*4+1] == atoms[k+1]){
                                        	match++;
                                        }
                                        if(list[sortedplanes[j]*4+2] == atoms[k+2]){
                                         	match++;
                                        }
                                        if(list[sortedplanes[j]*4+3] == atoms[k+3]){
                                        	match++;
                                        }
                                        if(match==4){
                                        	k=8;
                                        }
					k=k+4;
                                 }
                                 j++;
				 //printf("match is %d\n",match);
                                 if(match==4){
                                 	match1++;
                                 }

                          }//j<no_planes  
                  }

                  //printf("match1 is %d\n",match1);

                  if(match1==2){
			if(strstr(cname,"Skew1") != NULL){
				d[0]=get_signed_distance_from_point_to_plane(fifteen_planes[11],ring[0][0]);
				d[1]=get_signed_distance_from_point_to_plane(fifteen_planes[11],ring[4][0]);
				if(d[0]<0.0 && d[1]>0.0){
					scheck=1;
					fprintf(Oset.F,"\t5S1\t");
				}
				if(d[0]>0.0 && d[1]<0.0){
					scheck=1;
					fprintf(Oset.F,"\t1S5\t");
				}	
							
			}
			if(strstr(cname,"Skew2") != NULL){
				d[0]=get_signed_distance_from_point_to_plane(fifteen_planes[6],ring[5][0]);
                                d[1]=get_signed_distance_from_point_to_plane(fifteen_planes[6],ring[1][0]);
				if(d[0]<0.0 && d[1]>0.0){
					scheck=1;
                                        fprintf(Oset.F,"\t2SO\t");
                                }
                                if(d[0]>0.0 && d[1]<0.0){
                                        fprintf(Oset.F,"\tOS2\t");
                                }
			}
			if(strstr(cname,"Skew3") != NULL){
				d[0]=get_signed_distance_from_point_to_plane(fifteen_planes[13],ring[2][0]);
                                d[1]=get_signed_distance_from_point_to_plane(fifteen_planes[13],ring[0][0]);
				if(d[0]<0.0 && d[1]>0.0){
					scheck=1;
                                        fprintf(Oset.F,"\t1S3\t");
                                }
                                if(d[0]>0.0 && d[1]<0.0){
					scheck=1;
                                        fprintf(Oset.F,"\t3S1\t");
                                }	
			}
                        //printf("This is a skewboat\n");
                        i=Cslurp.n;
			//scheck=1;
                   }

         }//for                    

	}   


	//printf("bcheck,ccheck and scheck are %d,%d and %d\n",bcheck,ccheck,scheck);
	hcheck=0;
	int hnum=1;
	nsize=0;
	match1=0;
	match=0;
	if(ccheck==0 && bcheck==0 && scheck==0){ 
        for(i=0;i<Cslurp.n;i++){
        	char conf_name[6];
                sprintf(conf_name,"Half%d",hnum);
                sscanf(Cslurp.L[i],"%s",cname);
                //printf("%s and conf_name %s\n",cname,conf_name);
                if(strstr(cname,conf_name) != NULL){
                	sscanf(Cslurp.L[i],"%s%d%d%d%d",cname,&dum1,&dum2,&dum3,&dum4);
                        atoms[0]=dum1;atoms[1]=dum2;atoms[2]=dum3;atoms[3]=dum4;
                        //printf("%s\n",conf_name);
                        hnum++;
                        j=0;
                        match1=0;
                        nsize=sdsize;
			while(j<1){
                        	k=0;
                                match=0;
                        	while(k<4){
                                	match=0;
                                	if(list[sortedplanes[j]*4] == atoms[k]){
                                        	match++;
                                        }
                                       	if(list[sortedplanes[j]*4+1] == atoms[k+1]){
                                        	match++;
                                        }
                                        if(list[sortedplanes[j]*4+2] == atoms[k+2]){
                                        	match++;
                                        }
                                        if(list[sortedplanes[j]*4+3] == atoms[k+3]){
                                        	match++;
                                        }
                                        if(match==4){
                                        	k=4;
                                        }
					k=k+4;
                                }
                                j++;
                                //printf("match is %d\n",match);
                                if(match==4){
                                	match1++;
                                }

                        }//j<no_planes  
              }

               //printf("match1 is %d\n",match1);
		if(match1==1){
			//printf("cname is %s\n",cname);
                        if(strstr(cname,"Half1") != NULL){
                        	d[0]=get_signed_distance_from_point_to_plane(fifteen_planes[14],ring[0][0]);
                                d[1]=get_signed_distance_from_point_to_plane(fifteen_planes[14],ring[1][0]);
                                if(d[0]<0.0 && d[1]>0.0){
                                	i=Cslurp.n;
                                        hcheck=1;
                                        fprintf(Oset.F,"\t2H1\t");
                                }
                                if(d[0]>0.0 && d[1]<0.0){
                                        i=Cslurp.n;
                                        hcheck=1;
                                        fprintf(Oset.F,"\t1H2\t");
                                }
                        }
                        if(strstr(cname,"Half2") != NULL){
                                 //printf("inside Half2\n");
                                 d[0]=get_signed_distance_from_point_to_plane(fifteen_planes[9],ring[2][0]);
                                 d[1]=get_signed_distance_from_point_to_plane(fifteen_planes[9],ring[1][0]);
                                 //printf("%f and %f\n",d[0],d[1]);
                                 if(d[0]<0.0 && d[1]>0.0){
                                 	i=Cslurp.n;
                                        hcheck=1;
                                        fprintf(Oset.F,"\t2H3\t");
                                 }
                                 if(d[0]>0.0 && d[1]<0.0){
                                 	i=Cslurp.n;
                                        hcheck=1;
                                        fprintf(Oset.F,"\t3H2\t");
                                  }
                        }
                        if(strstr(cname,"Half3") != NULL){
                        	d[0]=get_signed_distance_from_point_to_plane(fifteen_planes[5],ring[2][0]);
                                d[1]=get_signed_distance_from_point_to_plane(fifteen_planes[5],ring[3][0]);
                                if(d[0]<0.0 && d[1]>0.0){
                                	i=Cslurp.n;
                                        hcheck=1;
                                        fprintf(Oset.F,"\t4H3\t");
                                }
                                if(d[0]>0.0 && d[1]<0.0){
                                	i=Cslurp.n;
                                        hcheck=1;
                                	fprintf(Oset.F,"\t3H4\t");
                                }
                       }
		       if(strstr(cname,"Half4") != NULL){
                                d[0]=get_signed_distance_from_point_to_plane(fifteen_planes[2],ring[4][0]);
                                d[1]=get_signed_distance_from_point_to_plane(fifteen_planes[2],ring[3][0]);
                                if(d[0]<0.0 && d[1]>0.0){
                                          i=Cslurp.n;
                                          hcheck=1;
                                          fprintf(Oset.F,"\t4H5\t");
                                }
                                if(d[0]>0.0 && d[1]<0.0){
                                          i=Cslurp.n;
                                          hcheck=1;
                                          fprintf(Oset.F,"\t5H4\t");
                                }
                       }
                       if(strstr(cname,"Half5") != NULL){
                                 d[0]=get_signed_distance_from_point_to_plane(fifteen_planes[0],ring[4][0]);
                                 d[1]=get_signed_distance_from_point_to_plane(fifteen_planes[0],ring[5][0]);
                                 if(d[0]<0.0 && d[1]>0.0){
                                            i=Cslurp.n;
                                            hcheck=1;
                                            fprintf(Oset.F,"\tOh5\t");
                                 }
                                 if(d[0]>0.0 && d[1]<0.0){
                                            i=Cslurp.n;
                                            hcheck=1;
                                            fprintf(Oset.F,"\t5HO\t");
                                 }
                        }
                        if(strstr(cname,"Half6") != NULL){
                                  d[0]=get_signed_distance_from_point_to_plane(fifteen_planes[10],ring[0][0]);
                                  d[1]=get_signed_distance_from_point_to_plane(fifteen_planes[10],ring[5][0]);
                                  if(d[0]<0.0 && d[1]>0.0){
                                             i=Cslurp.n;
                                             hcheck=1;
                                             fprintf(Oset.F,"\tOH1\t");
                                  }
                                  if(d[0]>0.0 && d[1]<0.0){
                                             i=Cslurp.n;
                                             hcheck=1;
                                             fprintf(Oset.F,"\t1HO\t");
                                  }
                        }
                  }//if match==1


  	}//for                       
	}
		
		if(ccheck==0 && bcheck==0 && scheck==0 && hcheck==0){
				fprintf(Oset.F,"\t-\t");
		}



		for(i=0;i<no_planes;i++){
			
			//printf("sortedplanes are %d\n",sortedplanes[i]);
			//printf("conformers are %s\n",conformers[sortedplanes[i]]);
			//printf("secondlistatoms are %d && %d\n",secondlist[sortedplanes[i]*2],secondlist[sortedplanes[i]*2+1]);
			d[0]=get_signed_distance_from_point_to_plane(fifteen_planes[sortedplanes[i]],ring[secondlist[sortedplanes[i]*2]][0]);
			d[1]=get_signed_distance_from_point_to_plane(fifteen_planes[sortedplanes[i]],ring[secondlist[sortedplanes[i]*2+1]][0]);
			//printf("%f and %f\n",d[0],d[1]);
			if(d[0]<0.0 && d[1]>0.0){
				fprintf(Oset.F,"\t%d%s%d(%f)\t",secondlist[sortedplanes[i]*2+1]+1,conformers[sortedplanes[i]],secondlist[sortedplanes[i]*2]+1,fifteen_dihedrals[sortedplanes[i]]);
			}
			if(d[0]>0.0 && d[1]<0.0){
				fprintf(Oset.F,"\t%d%s%d(%f)\t",secondlist[sortedplanes[i]*2]+1,conformers[sortedplanes[i]],secondlist[sortedplanes[i]*2+1]+1,fifteen_dihedrals[sortedplanes[i]]);
			}
			if(d[0]>0.0 && d[1] >0.0){
				fprintf(Oset.F,"\t%d%d%s(%f)\t",secondlist[sortedplanes[i]*2]+1,secondlist[sortedplanes[i]*2+1]+1,conformers[sortedplanes[i]],fifteen_dihedrals[sortedplanes[i]]);
			}
			if(d[0]<0.0 && d[1]<0.0){
				fprintf(Oset.F,"\t%s%d%d(%f)\t",conformers[sortedplanes[i]],secondlist[sortedplanes[i]*2]+1,secondlist[sortedplanes[i]*2+1]+1,fifteen_dihedrals[sortedplanes[i]]); 
			}

		}


	
	
}//fivecheck2==0


if(argc==3){
test=EOF;
}

if(argc==4){
test=fgetc(Cset.F);
for(mi=0;mi<A.nm;mi++){
        for(ri=0;ri<A.m[mi][0].nr;ri++){
                for(ai=0;ai<A.m[mi][0].r[ri].na;ai++){
                                A.m[mi][0].r[ri].a[ai].nalt=0;
                                free(A.m[mi][0].r[ri].a[ai].xa);

                        } // close atom loop
                } // close residue loop

        }// close mole
}



}//fgetc loop


fprintf(Oset.F,"\n");
printf("\n");
printf("OUTPUT FILE:ring_conformations.txt\n");


return 0;
}
