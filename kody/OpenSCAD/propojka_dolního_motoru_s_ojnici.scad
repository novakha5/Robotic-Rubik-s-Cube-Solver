rM3 = 1.7; //srouby velikosti M3
skrz = 10;

//promenne pro renderovací krok
$fa = 0.1;
$fs = 0.1;
$fn = 0;

//funkce pro umisteni sroubu
module transM3 (x, y, z)   { 
    translate ([x, y , z])
        rotate ([90, 0, 0])
            cylinder(skrz, rM3, rM3, center = true);
    }

difference(){
    union(){
        translate([0, -5, 4]){
            cube([20, 10, 8], center = true);
        }
        translate([-20,0,0]){
            cube([40, 3.5, 8]);
        }
        translate ([20, 3.5, 4])
            rotate ([90, 0, 0])
                cylinder(3.5, 4, 4);
        translate ([-20, 3.5, 4])
            rotate ([90, 0, 0])
                cylinder(3.5, 4, 4);
    }
    translate([0, 7, 4]){    
        difference(){   
            rotate ([90, 0, 0]){
                cylinder (20, 2.53, 2.53); 
            }
            translate([2.1,-21, -5]){ 
                cube(22);
            }
        }
    }
    translate([0,-5,4]){   
        rotate ([90, 0, 90]){
            cylinder (25, rM3, rM3, center =  true); 
        }
    }
    translate([-4.5, -5, 1]){  
        cube ([2.7, 6., 12.5], center = true);
    }
    translate([4.5, -5, 1]){  
        cube ([2.7, 6.5, 12.5], center = true);
    }
    
    transM3(20, 0, 4);
    transM3(-20, 0, 4);
}

