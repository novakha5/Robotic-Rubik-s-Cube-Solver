//promenne pro renderovací krok
$fa = 0.05;
$fs = 0.05;
$fn = 0;

sirKostky = 57.5;
rM3 = 1.65;

difference(){
    union(){
        difference(){
            cube([(sirKostky+10), (sirKostky/3)+5, 8]);
            translate([5,5,-0.5])
                cube([sirKostky, sirKostky, 9]);
            translate([0,(sirKostky/3),-1]){
                difference(){
                    cube(10);
                    cylinder (20, 5, 5, center = true);
                }
            }
            translate([(sirKostky+10),(sirKostky/3),-1]){
                difference(){
                    translate([-10,0,0])
                        cube(10);
                    cylinder (20, 5, 5, center = true);
                }
            }   
        }
        translate([(sirKostky/2)+5, -5, 4]){
            cube([20, 10, 8], center = true);
            }
        }
    translate([(sirKostky/2)+5, 7, 4]){    
        difference(){   
            rotate ([90, 0, 0]){
                cylinder (20, 2.53, 2.53); 
            }
            translate([2.1,-21, -5]){ 
                cube(22);
            }
        }
    }
    translate([(sirKostky/2)+5,-5,4]){   
        rotate ([90, 0, 90]){
            cylinder (25, rM3, rM3, center =  true); 
        }
    }
    translate([(sirKostky/2)+0.5, -5, 1]){  
        cube ([2.7, 6.5, 12.5], center = true);
    }
    
    translate([(sirKostky/2)+9.5, -5, 1]){  
        cube ([2.7, 6.5, 12.5], center = true);
    }
}

