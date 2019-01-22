hole_diam=9.25;
hole_space=98;
margin=1;
length=hole_space+hole_diam+2;
width=18;
pizero_diam=2.5;
pizero_space=58;
zero_offset=1;

difference() {
    union () {
        cube([length,width,3]);
        translate([(length-80)/2,-5+zero_offset,0]) cube([80,5,3]);
        translate([(length-80)/2,-5+zero_offset,2]) cube([80,13,3]);
    };
    translate([hole_diam/2+margin,width-hole_diam/2-margin,-1]) cylinder(d=hole_diam,h=6,$fn=200);
    translate([length-hole_diam/2-margin,width-hole_diam/2-margin,-1]) cylinder(d=hole_diam,h=6,$fn=200);
    translate([length/2-pizero_space/2,zero_offset+9+pizero_diam/2,-1]) cylinder(d=pizero_diam,h=6,$fn=200);
    translate([length/2+pizero_space/2,zero_offset+9+pizero_diam/2,-1]) cylinder(d=pizero_diam,h=6,$fn=200);    
}    

