span=103;
leg_width=8;
leg_inside=6;
leg_inside2=6.5;
base_height=10;

intersection() {
    translate([0,-40,-4]) cube([200,80,50]);
union() {
translate([(3+76)/2,5,38.75]) import("ArduCam_Base.stl");
cube([span+2*leg_inside,leg_inside2,base_height]);
translate([leg_inside,0,-4]) cube([span,leg_inside2,4]);
}
}