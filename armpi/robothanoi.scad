//Tower of Hanoi for Robot, Scott Bennett, 6/2019
num_disks=5;
min_diam=25;
diam_inc=5;
handle_thick=10;
disk_thick=15;
tol=1.0;
margin=5;
max_diam=min_diam+(num_disks-1)*diam_inc;
base_width=max_diam+2*margin;
base_length=3*max_diam+4*margin;
peg_diam=10;
$fn=200;
space=20;

module base() {
    difference() {
        minkowski() {
            cube([base_length,base_width,disk_thick],center=true);
            sphere(r=2);
        }
        translate([-margin/2-max_diam/2,0,-5]) cylinder(d=8.5,h=20);
        translate([margin/2+max_diam/2,0,-5]) cylinder(d=8.5,h=20); 
        translate([-margin/2-max_diam/2,0,-10]) cylinder(d=2.8,h=20);
        translate([margin/2+max_diam/2,0,-10]) cylinder(d=2.8,h=20);             
    }
    translate([0,0,disk_thick/2]) cylinder(d=peg_diam,h=handle_thick);
    translate([-margin-max_diam,0,disk_thick/2]) cylinder(d=peg_diam,h=handle_thick);
    translate([margin+max_diam,0,disk_thick/2]) cylinder(d=peg_diam,h=handle_thick);    
}

module disk(num) {
    difference() {
        cylinder(d=min_diam+diam_inc*(num-1),h=disk_thick);
        translate([0,0,-1]) cylinder(d1=peg_diam+tol+5,d2=peg_diam+tol,h=handle_thick+tol+1);
    }
    translate([0,0,disk_thick]) cylinder(d=peg_diam,h=handle_thick);
}

//base();
//for(d=[1:num_disks]) translate([0,0,disk_thick/2+space+(num_disks-d)*(disk_thick+space)]) disk(d);
for(d=[1:num_disks]) translate([max_diam*(d-1)-80,-max_diam-10,-disk_thick/2]) disk(d);

