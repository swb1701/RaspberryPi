//Robot Console by Scott Bennett, 6/2019
w=80;
h=112;
sh=50;
pz_hole=1.6;
pc_hole=1.6;
pz_length=58;
pz_width=23;
pc_length=55.66;
pc_width=18.975;
base=16;
$fn=200;

/*
use <PiZero.scad>;
rotate([45,0,0]) translate([39,34.5,-4]) union() {
    PiZeroBody();
    PiGPIO(true);
}
*/

module sc_cutout() {
    cube([65,27,6]);
    translate([-10,7/2,0]) cube([20,20,6]);
    translate([4,4,-5]) union() {
            translate([0,0,-1]) cylinder(d=pc_hole,h=7);
            translate([pc_length,0,-1]) cylinder(d=pc_hole,h=7);
            translate([pc_length,pc_width,-1]) cylinder(d=pc_hole,h=7);
            translate([0,pc_width,-1]) cylinder(d=pc_hole,h=7);        
    };    
}

module pi_cutout() {
    cube([70,45,16]);
    translate([-10,11,0]) cube([20,15,8]);
    translate([5,5,-5]) union() {
        translate([0,0,-1]) cylinder(d=pz_hole,h=7);
        translate([pz_length,0,-1]) cylinder(d=pz_hole,h=7);
        translate([pz_length,pz_width,-1]) cylinder(d=pz_hole,h=7);
        translate([0,pz_width,-1]) cylinder(d=pz_hole,h=7);
    }; 
}

module power_cutout() {
    translate([0,0,0]) rotate([-90,0,0]) cylinder(h=11,d=10);
    translate([-1-1,-11-15/2,0]) cube([15,23+15,15],center=true);
}

difference() {
    //minkowski() {
    union() {
        cube([w,h,base]);
        translate([0,0,base])
        polyhedron(
        points=[
        [0,0,0],[0,sh,sh],[w,sh,sh],[w,0,0],
        [w,0,0],[w,sh,sh],[w,sh,0],
        [0,0,0],[0,sh,0],[0,sh,sh],
        [w,sh,sh],[0,sh,sh],[0,sh,0],[w,sh,0],
        [w,0,0],[w,sh,0],[0,sh,0],[0,0,0]
        ],
        faces=[
        [0,1,2,3],
        [4,5,6],
        [7,8,9],
        [10,11,12,13],
        [14,15,16,17]
        ]);
    };
    //sphere(r=2);
//};
    translate([(w-65)/2,(h-sh-27)/2+sh,base-5]) sc_cutout();
    rotate([45,0,0]) translate([(w-70)/2,18,-4]) pi_cutout();
    translate([w-10,58,8]) rotate([90,90,0]) power_cutout();
    translate([10,10,4]) cylinder(d=8.5,h=20);
    translate([10,10,-1]) cylinder(d=2.8,h=20);
    translate([w-10,10,4]) cylinder(d=8.5,h=20);
    translate([w-10,10,-1]) cylinder(d=2.8,h=20);  
    translate([10,104,4]) cylinder(d=8.5,h=20);
    translate([10,104,-1]) cylinder(d=2.8,h=20);
    translate([w-10,104,4]) cylinder(d=8.5,h=20);
    translate([w-10,104,-1]) cylinder(d=2.8,h=20);    
};