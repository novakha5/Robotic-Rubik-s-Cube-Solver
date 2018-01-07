//promenne pro renderovací krok
$fa = 0.05;
$fs = 0.05;
$fn = 0;

difference(){
    union(){
        translate([0,0,5.5]){
            cylinder(3.5,8,5.5);
        }
        cylinder(3.5,5.5,8);
        translate([0,0,3.5]){
            cylinder(2,8,8);
        }
    }
    cylinder(10, 3.9, 3.9);
    translate([0,0,-1]){
        cylinder(5, 4.6, 4.6);
    }
    translate([0,0,5]){
        cylinder(5, 4.6, 4.6);
    }    
}