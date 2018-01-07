rM3 = 1.65; //srouby velikosti M3
skrz = 60; //delka veci na storpocentni vysek

//promenne pro renderovací krok
$fa = 0.02;
$fs = 0.02;
$fn = 0;

module transM3 (x, y, z)   { 
    translate ([x, y , z])
        cylinder(skrz, rM3, rM3, center = true);
    }
    
rotate([90, 0 , 0]){  
    difference(){ 
        union(){
            translate ([0, 0 , 80]){
                rotate([0, 90 , 0])
                    cylinder (3.5, 4, 4);
            }
            translate ([0, -4 , 0]){
                cube([62, 8 , 5.6]);
                cube([3.5, 8 , 80]);
            }
        }
        transM3 (26, 0 , 0);   
        transM3 (56, 0 , 0); 
        rotate([0, 90 , 0]){
            transM3 ( -77, 0 , 0);   
            transM3 (-50, 0 , 0);
        }
       
    }
}