rM3 = 1.65; //srouby velikosti M3
rHr = 2.7;  //hridel motoru
rMot = 11.2; //vystoupla cast motoru u hridele

skrz = 6; //delka veci na stoprocentni vysek
sroubMotPos = 15.5; //pozice sroubku na pripevneni motoru

//promenne pro renderovací krok
$fa = 0.1;
$fs = 0.1;
$fn = 0;

//funkce pro umisteni sroubu
module transM3 (x, y, z)   { 
    translate ([x, y , z])
        cylinder(skrz, rM3, rM3, center = true);
}

difference(){
    cube([5, 43, 43], center = true);
    rotate ([0, 90, 0]){
        translate([0, 0, 3.5])
            cylinder (skrz, rMot, rMot, center =  true);
        cylinder (skrz, rHr, rHr, center = true);
        transM3(sroubMotPos, sroubMotPos, 0);
        transM3(-sroubMotPos, sroubMotPos, 0);
        transM3(sroubMotPos, -sroubMotPos, 0);
        transM3(-sroubMotPos, -sroubMotPos, 0);
    }
}
difference(){
    translate([14, 0, 24])
        rotate ([0, 90, 0])
            cube([5, 43, 33], center = true);
    translate([35, 40, 24])
        rotate([0, 0, 60])
            cube([60, 60, skrz], center = true );
    translate([35, -40, 24])
        rotate([0, 0, -60])
            cube([60, 60, skrz], center = true );
}
difference(){
    union(){
        translate([-2.5,-2.6, 26])
            cube([33, 5.2, 8]);
        translate([-2.5,-4.75, 31.2])
            cube([33, 9.5, 4.5]);
    } 
     translate([-2.6,-4.75, 32.7])
         rotate([45, 0, 0])
            cube([34, 9, 6.5]);
    translate([-2.6,4.75, 32.7])
         rotate([45, 0, 0])
            cube([34, 9, 6.5]);
}





