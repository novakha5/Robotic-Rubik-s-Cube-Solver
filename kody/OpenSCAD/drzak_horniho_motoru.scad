rM3 = 1.65; //srouby velikosti M3
rHr = 2.7;  //hridel motoru
rMot = 11.2; //vystoupla cast motoru u hridele

skrz = 100; //delka veci na stoprocentni vysek
sroubMotPos = 15.5; //pozice sroubku na pripevneni motoru
sroubKolecPos = 15; //pozice sroubu na pripevneni kolecek

//promenne pro renderovací krok
$fa = 0.1;
$fs = 0.1;
$fn = 0;

//funkce pro umisteni sroubu
module transM3 (x, y, z)   { 
    translate ([x, y , z])
        cylinder(skrz, rM3, rM3, center = true);
    }
module placeM3 (i, j){
    transM3 (i*sroubKolecPos, j*sroubKolecPos, 0);
    rotate ([90, 0, 0])
         transM3 (i*sroubMotPos, j*sroubMotPos, 0);
    }
 
//samotne modelovani   
union(){
    //vytvoření vnější krychle s potřebnými dírami
    difference(){
        translate([0, -1.75, -11.25])
            cube ([40, 43.5, 61.5], center = true);
        translate ([-30 ,-20 ,-38.5])
            cube(60);  
        rotate ([90, 0, 0]){
            cylinder (44, rMot, rMot, center = true);
            cylinder (skrz, rHr, rHr, center =true);
        } 
        for (i = [-1:2:1]){
            for (j = [-1:2:1]){
                placeM3 (i, j);
            }
        }
        cube([25, 22.75, skrz], center = true);
    } 
        
    //vytvoření podstavce na motor
    difference(){
        translate([0 ,0 ,-31.2])
          cube([38, 5, 21.6], center = true);
    translate([19, -3, -17.4])
            rotate([0, 45, 0])
                cube([20, 15, 20], center = true);
        translate([-19, -3, -17.4])
            rotate([0, 45, 0])
                cube([20, 15, 20], center = true);
    }    
}