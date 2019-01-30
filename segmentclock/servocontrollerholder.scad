ol=67;
ow=32;
oh=17.5+2.5;
wall=2;
lip=4;

module board() {
    translate([2.5,4,0]) cube([62.25,25.5,15.5]);
}

module holder() {
    difference() {
        cube([ol,ow,oh]);
        translate([2,-lip-wall,wall]) cube([ol-4,ow,oh-wall+1]);
        translate([-0.5,-lip-wall,wall+4]) cube([ol+1,ow,oh-wall+1]);        
        translate([wall,ow-lip-5,wall]) cube([ol-2*wall,7,oh-2*wall]);
        translate([ol-40+1.5,0,wall+5-3]) cube([10,40,7]);
    }
};

holder();
//board();