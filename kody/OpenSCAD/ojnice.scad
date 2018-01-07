rM3 = 1.65; //srouby velikosti M3
delka = 68;
skrz = 5;

//promenne pro renderovací krok
$fa = 0.02;
$fs = 0.02;
$fn = 0;

module transM3 (x, y, z){ 
    translate ([x, y , z])
        cylinder(skrz, rM3, rM3, center = true);
}

difference(){
    union(){
        cube([delka, 6, 3.5], center = true);
        translate([delka/2, 0, 0]){
           cylinder(3.5, 4.5, 4.5, center = true);     
        }
        translate([-delka/2, 0, 0]){
           cylinder(3.5, 4.5, 4.5, center = true);     
        }
    }
    transM3(delka/2,0,0);
    transM3(-delka/2,0,0);
}
