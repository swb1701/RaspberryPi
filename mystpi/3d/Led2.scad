$fn=200;
thick=2;
led_width=10;
led_height=10;
per_row=23;
hole=6;

module base() {
difference() {
    import("c:/incoming/Myst_Lighthouse/files/Led-support.stl");
    translate([0,0,-1]) cylinder(d=90,h=130);
}
difference() {
    cylinder(d=92,h=1.0);
    translate([0,0,-1]) cylinder(d=60,h=4.0);
}
}

module cyl() {

difference() {
    cylinder(d=80,h=120);
    translate([0,0,-1]) cylinder(d=80-2*thick,h=122);
    
    for(i=[0:7]) {
        for(j=[0:per_row]) {
            translate([0,0,led_height*i+20]) rotate([0,0,j*(360/per_row*2)]) cube([hole,50,hole]);
        }
    }    
    translate([0,0,-1]) cylinder(d=80-2*thick,h=122);
};

}

module test() {

difference() {
    cylinder(d=80,h=23);
    translate([0,0,-1]) cylinder(d=80-2*thick,h=122);
    for(i=[0:1]) {
        for(j=[0:per_row]) {
            translate([0,0,led_height*i+3]) rotate([0,0,j*(360/per_row*2)]) cube([hole,50,hole]);
        }
    }
};

}

//test();
base();
cyl();
