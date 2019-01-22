difference() {
    cube([40,26,15]);
    translate([4,10,-1]) cylinder(d=6.5,h=17,$fn=200);
    translate([26,6,-1]) cube([9,21,12]);
    translate([26,14,10.5]) cube([9,2,5]);
    translate([-2,17.3,-0.5]) rotate([0,0,-22]) cube([30.5,5,5]);
}