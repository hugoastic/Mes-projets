#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>


/*Déclaration des variables globales et des structures*/

/* Nom des registres*/
typedef struct{
    int nom ;
    int64_t valeur; 
}registre ; /*structure pour la valeur finale*/


/* Structure d'une instruction */
typedef struct{
  char *opcode;
  int rs1; /*on récupère l'indice du registre*/
  int rs2;
  int rd;
  int val_imm;
  }instruction_structure;

/*Déclaration tableau pour les valeurs des registres et du PC*/
registre registres_tab[33]={{0,0}, {1,0}, {2,16384},  {3,0},  {4,0}, {5,0}, {6,0}, {7,0},
                                  {8,0},   {9,0}, {10,0},  {11,0},  {12,0}, {13,0}, {14,0}, {15,0},
                                  {16,0},   {17,0}, {18,0},  {19,0},  {20,0}, {21,0}, {22,0}, {23,0},
                                  {24,0},   {25,0}, {26,0}, {27,0}, {28,0}, {29,0}, {30,0}, {31,0},{32,0}}; 





/* Déclaration des fonctions secondaires à notre programme principal*/

int extension_de_signe(int nombre_binaire, int nombre_de_bit){
    int nombre_res;
    if ((nombre_binaire & (1 << (nombre_de_bit - 1))) != 0){ /*on gérer les valeurs immédiates négatives et positives*/
        nombre_res = ~nombre_binaire + 1;
        return -(nombre_res & ((1 << nombre_de_bit) - 1));
    }
    else {
        return nombre_binaire  ;
    }
}



instruction_structure decoder (int instruction_hex){
  instruction_structure inst;
  int opcode=0x0000007f;
  int inst_opcode= opcode & instruction_hex;
  int funct3=0x7000;
  int inst_funct3= (funct3 & instruction_hex)>>12;
  int funct7=0xfe000000;
  int inst_funct7= (funct7 & instruction_hex)>>25;
  
  /*add*/
  if ( (inst_opcode== 0x33) && (inst_funct3==0x0) && (inst_funct7==0x00)){
    inst.opcode="add";
    inst.rs1=(0xf8000 & instruction_hex)>>15; /* on décale vers la droite pour supprimer tous les 0 après l'opération & bit à bit car sinon on a xx00 au lieu de xx */
    inst.rs2=(0x1f00000 & instruction_hex)>>20;
    inst.rd=(0xf80 & instruction_hex)>>7;
    inst.val_imm=0;
  }
  /*sub*/
  if ( (inst_opcode== 0x33) && (inst_funct3==0x0) && (inst_funct7==0x20)){
    inst.opcode="sub";
    inst.rs1=(0xf8000 & instruction_hex)>>15;
    inst.rs2=(0x1f00000 & instruction_hex)>>20;
    inst.rd=(0xf80 & instruction_hex)>>7;
    inst.val_imm=0;
  }
  /*addi*/
  if ( (inst_opcode== 0x13) && (inst_funct3==0x0)){
    inst.opcode="addi";
    inst.rs1=(0xf8000 & instruction_hex)>>15; 
    inst.rd=(0xf80 & instruction_hex)>>7;
    inst.val_imm=(0xfff00000 & instruction_hex)>>20;
    inst.rs2=0;
  }
  /*ld*/
  if ( (inst_opcode== 0x3) && (inst_funct3==0x3)){
    inst.opcode="ld";
    inst.rs1=(0xf8000 & instruction_hex)>>15; 
    inst.rd=(0xf80 & instruction_hex)>>7;
    inst.val_imm=(0xfff00000 & instruction_hex)>>20;
    inst.rs2=0;
  }
  /*sd*/
  if ( (inst_opcode== 0x23) && (inst_funct3==0x3) ){
    inst.opcode="sd";
    inst.rs1=(0xf8000 & instruction_hex)>>15;
    inst.rs2=(0x1f00000 & instruction_hex)>>20;
    inst.rd=0;
    int val_imm_fin =(0xfe000000 & instruction_hex)>>20;
    int val_imm_deb = (0xf80 & instruction_hex)>>7 ;
    inst.val_imm = val_imm_fin | val_imm_deb ;
  }
  /*beq*/
  if ( (inst_opcode== 0x63) && (inst_funct3==0x0)){
    inst.opcode="beq";
    inst.rs1=(0xf8000 & instruction_hex)>>15;
    inst.rs2=(0x1f00000 & instruction_hex)>>20;
    inst.rd=0;
    int val_imm_fin = (0x7e000000 & instruction_hex)>> 19 ;
    int val_imm_deb = (0xf80 & instruction_hex) >> 7;
    int bin1 = (0x1 & val_imm_deb)<<10 ; /*11*/
    int bin2 = 0x1e & val_imm_deb ; /*4:1*/
    int bin3 =  (0x7c0 & val_imm_fin)>>1;/*10:5*/
    int bin4 = 0x800 & val_imm_fin;/*12*/
    inst.val_imm = (bin4 | bin1 | bin3 | bin2) ;
  }
  /*bne*/
  if ( (inst_opcode== 0x63) && (inst_funct3==0x1) ){
    inst.opcode="bne";
    inst.rs1=(0xf8000 & instruction_hex)>>15;
    inst.rs2=(0x1f00000 & instruction_hex)>>20;
    inst.rd=0;
    int val_imm_fin = (0x7e000000 & instruction_hex)>> 19 ;
    int val_imm_deb = (0xf80 & instruction_hex) >> 7;
    int bin1 = (0x1 & val_imm_deb)<<10 ; /*11*/
    int bin2 = 0x1e & val_imm_deb ; /*4:1*/
    int bin3 =  (0x7c0 & val_imm_fin)>>1;/*10:5*/
    int bin4 = 0x800 & val_imm_fin;/*12*/
    inst.val_imm = (bin4 | bin1 | bin3 | bin2) ;
  }
  /*blt*/
  if ( (inst_opcode== 0x63) && (inst_funct3==0x4) ){
    inst.opcode="blt";
    inst.rs1=(0xf8000 & instruction_hex)>>15;
    inst.rs2=(0x1f00000 & instruction_hex)>>20;
    inst.rd=0;
    int val_imm_fin = (0x7e000000 & instruction_hex)>> 19 ;
    int val_imm_deb = (0xf80 & instruction_hex) >> 7;
    int bin1 = (0x1 & val_imm_deb)<<10 ; /*11*/
    int bin2 = 0x1e & val_imm_deb ; /*4:1*/
    int bin3 =  (0x7c0 & val_imm_fin)>>1;/*10:5*/
    int bin4 = 0x800 & val_imm_fin;/*12*/
    inst.val_imm = (bin4 | bin1 | bin3 | bin2) ;
  }
  /*bge*/
  if ( (inst_opcode== 0x63) && (inst_funct3==0x5) ){
    inst.opcode="bge";
    inst.rs1=(0xf8000 & instruction_hex)>>15;
    inst.rs2=(0x1f00000 & instruction_hex)>>20;
    inst.rd=0;
    int val_imm_fin = (0x7e000000 & instruction_hex)>> 19 ;
    int val_imm_deb = (0xf80 & instruction_hex) >> 7;
    int bin1 = (0x1 & val_imm_deb)<<10 ; /*11*/
    int bin2 = 0x1e & val_imm_deb ; /*4:1*/
    int bin3 =  (0x7c0 & val_imm_fin)>>1;/*10:5*/
    int bin4 = 0x800 & val_imm_fin;/*12*/
    inst.val_imm = (bin4 | bin1 | bin3 | bin2) ;
  }
  /*jal*/
  if (inst_opcode== 0x6f){
    inst.opcode="jal";
    inst.rs1 = 0 ;
    inst.rs2 = 0 ;
    inst.rd=(0xf80 & instruction_hex)>>7;
    int val_imm=(0xfffff000 & instruction_hex)>>12;
    int bin1 = (0x100 & val_imm)<<2 ; /*11*/
    int bin2 = (0xff & val_imm) << 11 ; /*19:12*/
    int bin3 =  (0x80000 & val_imm);/*20*/
    int bin4 = (0x7fe00 & val_imm)>>8 ;/*10:1 9 car 0eme bit a prendre en compte*/
    inst.val_imm = bin3 | bin2 |bin1 | bin4 ;
  }
  
  return (inst);
  
}   
 
  
  

void execute_ligne ( instruction_structure sequence, int memoire[]){ /* en fonction du type d'instruction, des registres et des valeurs immédiates on émule la ligne souhaitée*/

  if ( strcmp(sequence.opcode,"add")==0){
    int rs1=sequence.rs1;
    int rs2= sequence.rs2;
    int rd=sequence.rd;
    if (rd!=0){  /* on ne modifie la valeur des registres que si il ne s'agit pas de x0*/
      registres_tab[rd].valeur=registres_tab[rs1].valeur+registres_tab[rs2].valeur;
    }
    registres_tab[32].valeur=registres_tab[32].valeur+1; /*on incrémente PC à 1*/
  }
  
  if ( strcmp(sequence.opcode,"sub")==0){
    int rs1=sequence.rs1;
    int rs2= sequence.rs2;
    int rd=sequence.rd;
    if (rd!=0){
      registres_tab[rd].valeur=registres_tab[rs1].valeur-registres_tab[rs2].valeur;
    }
    registres_tab[32].valeur=registres_tab[32].valeur+1; 
  }
  
  if ( strcmp(sequence.opcode,"addi")==0){
    int rs1=sequence.rs1;
    int v_imm= extension_de_signe(sequence.val_imm,12);
    int rd=sequence.rd;
    if (rd!=0){
      registres_tab[rd].valeur=registres_tab[rs1].valeur+v_imm;
    }
    registres_tab[32].valeur=registres_tab[32].valeur+1; 
  }
  
  if ( strcmp(sequence.opcode,"beq")==0){
    int rs1=sequence.rs1;
    int v_imm= extension_de_signe(sequence.val_imm,12);
    int rs2=sequence.rs2;
    if (registres_tab[rs1].valeur==registres_tab[rs2].valeur){
      registres_tab[32].valeur=registres_tab[32].valeur+(v_imm/4); /* on saute à la ligne suivante en fonction de la valeur immédiates. On divise v_imm par 4 car une ligne en mémoire correspond à 4 octets */
    }
    else{
      registres_tab[32].valeur=registres_tab[32].valeur+1; 
    }
  }
  
  if ( strcmp(sequence.opcode,"bne")==0){
    int rs1=sequence.rs1;
    int v_imm= extension_de_signe(sequence.val_imm,12);
    int rs2=sequence.rs2;
    if (registres_tab[rs1].valeur!=registres_tab[rs2].valeur){
      registres_tab[32].valeur=registres_tab[32].valeur+(v_imm/4); 
    }
    else{
      registres_tab[32].valeur=registres_tab[32].valeur+1; 
    }
  }
  
  if ( strcmp(sequence.opcode,"blt")==0){
    int rs1=sequence.rs1;
    int v_imm= extension_de_signe(sequence.val_imm,12);
    int rs2=sequence.rs2;
    if (registres_tab[rs1].valeur<registres_tab[rs2].valeur){
      registres_tab[32].valeur=registres_tab[32].valeur+(v_imm/4); 
    }
    else{
      registres_tab[32].valeur=registres_tab[32].valeur+1; 
    }
  }
  
  if ( strcmp(sequence.opcode,"bge")==0){
    int rs1=sequence.rs1;
    int v_imm= extension_de_signe(sequence.val_imm,12);
    int rs2=sequence.rs2;
    if (registres_tab[rs1].valeur>=registres_tab[rs2].valeur){
      registres_tab[32].valeur=registres_tab[32].valeur+(v_imm/4); 
    }
    else{
      registres_tab[32].valeur=registres_tab[32].valeur+1; 
    }
  }
  
  if ( strcmp(sequence.opcode,"jal")==0){
    int v_imm= extension_de_signe(sequence.val_imm,20);
    int rd=sequence.rd;
    if (rd!=0){
      registres_tab[rd].valeur=1+registres_tab[32].valeur; /*rd=PC+4 or ici une ligne de mémoire fait 4 octets donc on effetcue: rd=PC+1 pour stocker l'adresse de retour de l'instruction suivante */
    }
    registres_tab[32].valeur=registres_tab[32].valeur+(v_imm/4); 
  }
  
  if ( strcmp(sequence.opcode,"ld")==0){
    int rs1=sequence.rs1;
    int v_imm= extension_de_signe(sequence.val_imm,12);
    int rd=sequence.rd;
    /*Assemblage valeur/registre*/
    int val_rs1=registres_tab[rs1].valeur;
    int v1 = memoire[(v_imm+val_rs1)/4];
    int64_t v1_64 = (0x00000000ffffffff & v1); /*on a des lignes mémoire de 32 bits il faut donc stocker notre valeur de 64 bits sur deux lignes*/
    int v2 = memoire[((v_imm+val_rs1)/4)+1];
    int64_t v2_64 = (0xffffffff00000000 & v2)<<32;
    int64_t val_final= v1_64 | v2_64;
    val_final= extension_de_signe(val_final,31); /* on prend en compte le fait que des valeurs de registres puissent etre négatives*/
    if (rd!=0){
      registres_tab[rd].valeur=val_final;
    }
    registres_tab[32].valeur=registres_tab[32].valeur+1; 
    
  }
  
  if ( strcmp(sequence.opcode,"sd")==0){
    int rs1=sequence.rs1;
    int v_imm= extension_de_signe(sequence.val_imm,12);
    int rs2=sequence.rs2;
    /*Assemblage valeur/registre*/
    int val_rs1=registres_tab[rs1].valeur; /*on procède de la même facon que pour le ld sauf que on stocke en mémoire, sur deux lignes, une valeurs de 64 bits au lieu de la récupérer*/
    int val_rs2=registres_tab[rs2].valeur;
    memoire[(v_imm+val_rs1)/4] = (val_rs2 &  0x00000000ffffffff);
    memoire[((v_imm+val_rs1)/4)-1] =( val_rs2 & 0xffffffff00000000);
    registres_tab[32].valeur=registres_tab[32].valeur+1; 
    
  }

}
  
  
  
  

/*Programme principal*/

int main(int argc, char **argv)
{
    /* ./riscv-emulator <HEX INPUT> <EMULATION OUTPUT> */
    if(argc != 3) {
        printf("Usage: ./riscv-emulator <HEX INPUT> <EMULATION OUTPUT>\n");
        printf("error: invalid command\n");
        return 1;
    }

    char *hex_input_file = argv[1];
    char *emu_output_file = argv[2];
    FILE *fichier_hex = fopen(hex_input_file,"r");
    FILE *fichier_emu = fopen(emu_output_file,"w");
    

    if (fichier_emu == NULL){/* gestion d'erreur si le fichier est mal renseigné*/
        printf("Files provided unavailable or wrong directory\n");
        exit(EXIT_FAILURE);
    }
    

    
    int taille_memoire=4096;/* initialisation de la mémoire*/
    int memoire[taille_memoire];
    for (int i=0 ; i<taille_memoire ; ++i){
      memoire[i]=0;
    }
    
    /*Lecture fichier ligne par ligne du fichier hexadécimal*/
    int indice_tab_instruction_memoire=0;
    while ( !feof(fichier_hex)){ 
      fscanf(fichier_hex,"%08x",&memoire[indice_tab_instruction_memoire]);
      ++indice_tab_instruction_memoire;
    }
    
    
    int PC= registres_tab[32].valeur;
    while( memoire[PC] !=0){ /*on parcourt notre tableau contenant toute les instructions en fonction du PC*/
        PC= registres_tab[32].valeur;
        instruction_structure instruction_decod = decoder(memoire[PC]);
        execute_ligne(instruction_decod, memoire);
        
    }
    /*pour afficher les valeurs finales des 32 registres*/ 
    for ( int nb_reg=0 ; nb_reg<32 ; ++nb_reg){
      printf("x%d : %ld\n",registres_tab[nb_reg].nom,registres_tab[nb_reg].valeur);
      fprintf(fichier_emu,"x%d : %ld\n",registres_tab[nb_reg].nom,registres_tab[nb_reg].valeur);
    }
    
    fclose(fichier_hex);
    fclose(fichier_emu);
     
    return 0;
}

