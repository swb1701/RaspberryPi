/*
use <PiZero.scad>;
translate([0,0,3+1]) union() {
    PiZeroBody();
    PiGPIO(true);
}
*/
led_space=33.33;
floor_thick=3;
height=led_space-floor_thick;
wall_thick=5;
inner_wall_thick=3;
tab_thick=2;
tab_height=4;
tab_tol=0.3;
outer=150;
inner=130;
ledw=6;
hook_depth=6;
hook_height=3;
hook_gap=3;
top_height=led_space*5+tab_height+4;
top_thick=3;
top_tol=0.6;
$fn=200;
base_height=15;

module bottom() {
    difference() {
        cylinder(h=base_height,d=outer+top_thick+top_tol);
        translate([0,0,-1+4]) cylinder(h=base_height+2,d=inner-top_tol-inner_wall_thick);
        translate([0,(outer+top_thick+top_tol)/2.0-11,8]) rotate([-90,0,0]) cylinder(h=11,d=10);
        color("red") translate([0,(outer+top_thick+top_tol)/2-22,7+2]) cube([15,23,14],center=true);
    }
     translate([0,0,-1]) 
     for(x=[0:9])
            rotate([0,0,x*18+9]) union() {
                translate([-outer/2+(outer-inner)*0.1,-1,height/2]) cube([(outer-inner)/2*0.75,tab_thick,tab_height]);
                translate([outer/2-(outer-inner)*0.1-((outer-inner)/2*0.75),-1,height/2]) cube([(outer-inner)/2*0.75,tab_thick,tab_height]);
            };                    
             
       
            
    translate([29,11.5,0]) cylinder(h=8,d=2.3);
    translate([-29,11.5,0]) cylinder(h=8,d=2.3);   
    translate([-29,-11.5,0]) cylinder(h=8,d=2.3);    
    translate([29,-11.5,0]) cylinder(h=8,d=2.3);  
}

module top() {
    difference() {
        cylinder(h=top_height,d=outer+top_thick+top_tol);
        translate([0,0,-4-tab_height]) cylinder(h=top_height,d=outer+top_tol);
        translate([0,0,-4]) cylinder(h=top_height,d=inner-top_tol-inner_wall_thick);
        translate([0,0,-0.1])
        for(x=[0:9])
            rotate([0,0,x*18]) translate([0,0,height/2+floor_thick+4*led_space]) union() {
                translate([-outer/2+(outer-inner)*0.1-tab_tol,-1,height/2]) cube([(outer-inner)/2*0.75+2*tab_tol,tab_thick+2*tab_tol,tab_height+4*tab_tol]);
                translate([outer/2-(outer-inner)*0.1-((outer-inner)/2*0.75)-tab_tol,-1,height/2]) cube([(outer-inner)/2*0.75+2*tab_tol,tab_thick+2*tab_tol,tab_height+4*tab_tol]);        
            }
        };
       
}

module retainer() {
    difference() {
        cylinder(h=3,d=inner-inner_wall_thick-3-0.15);
        translate([0,0,-0.1]) cylinder(h=4,d=inner-inner_wall_thick-3-3+0.15);
    };
}

module level() {
difference() {
    union() {
        cylinder(h=floor_thick,d=outer);
        for(x=[0:9])
            rotate([0,0,x*18]) translate([0,0,height/2+floor_thick]) union() {
                cube([outer,wall_thick,height],center=true);
                translate([-outer/2+(outer-inner)*0.1,-1,height/2]) cube([(outer-inner)/2*0.75,tab_thick,tab_height]);
                translate([outer/2-(outer-inner)*0.1-((outer-inner)/2*0.75),-1,height/2]) cube([(outer-inner)/2*0.75,tab_thick,tab_height]);
            };
        cylinder(h=floor_thick+height,d=inner);
        };
    translate([0,0,-1]) cylinder(h=height+floor_thick*2,d=inner-inner_wall_thick*2);
    for(x=[0:10])
        rotate([0,0,x*18+9]) translate([0,0,height/2+floor_thick]) cube([outer,ledw,ledw],center=true);
    translate([0,0,-height-floor_thick-tab_tol])
    for(x=[0:9])
            rotate([0,0,x*18]) translate([0,0,height/2+floor_thick]) union() {
                translate([-outer/2+(outer-inner)*0.1-tab_tol,-1,height/2]) cube([(outer-inner)/2*0.75+2*tab_tol,tab_thick+2*tab_tol,tab_height+4*tab_tol]);
                translate([outer/2-(outer-inner)*0.1-((outer-inner)/2*0.75)-tab_tol,-1,height/2]) cube([(outer-inner)/2*0.75+2*tab_tol,tab_thick+2*tab_tol,tab_height+4*tab_tol]);
            };
};
   for(x=[0:19])
            rotate([0,0,x*18]) translate([-inner/2,-inner_wall_thick/2,0]) difference() {
                cube([hook_depth,inner_wall_thick,10]);
                translate([-1,-1,7]) cube([hook_depth/2+2,inner_wall_thick+2,4]);
            };                
        
};

//retainer();
//level();
//color("white") translate([0,0,base_height]) top();
bottom();
//translate([0,0,7.1]) retainer();
//translate([0,0,height]) level();