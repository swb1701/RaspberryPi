//VARIABLES :)
height=80;
cuby_height=80;
width=320;
pi=3.14159265358979323846;
cubies_width=44;
cubies_height=11;
diam=(width+width/cubies_width)/pi; //was width/pi but one led too small
cuby_size=5;
top=10;
bottom=10;
thick=3;
$fn=200;
rotate=360/44;
cuby_space=cuby_height/cubies_height;
cuby_gap=cuby_space-cuby_size;
slide_tol=0.6;
diffuser_thick=2;

module cuby_cylinder() {
    difference(){
        cylinder(d=diam+thick,h=height+top+bottom);
        translate([0,0,-1])
            cylinder(d=diam,h=height+top+bottom+2);
        for (g=[0:10]){
            for (i = [0:21]){
                translate([0,0,height+bottom-cuby_gap*1.6-(g*cuby_space)])
                rotate(a=[0,0,rotate*i])                         
                    cube([cuby_size,diam+50,cuby_size],center=true);
            }
    
        }
    }
    //#translate([0,0,height+bottom]) cylinder(d=diam+thick,h=top);
    //#cylinder(d=diam+thick,h=bottom);
}

module diffuser() {
    outer=diam+thick+slide_tol+diffuser_thick;
    difference() {
        cylinder(d=outer,h=height+top+bottom);
        translate([0,0,-1]) cylinder(d=outer-diffuser_thick,h=height+top+bottom+2);
    }
}

module top() {
    outer=diam+thick;
    difference() {
        union() {
            cylinder(d=outer,h=3);
            translate([0,0,-6]) cylinder(d=outer-2.6-0.5,h=9);
        }
        translate([0,0,-7]) cylinder(d=outer-2.6-4,h=8);
    }
}

module bottom() {
    outer=diam+thick;
    difference() {
        union() {
            cylinder(d=outer,h=15);
            translate([0,0,-6]) cylinder(d=outer-2.6-1.0,h=18);
        }
        translate([0,0,-7]) cylinder(d=outer-2.6-4-16,h=19);
        translate([0,outer/2-11,7]) rotate([-90,0,0]) cylinder(h=11,d=10);
        color("red") translate([0,outer/2-22,6]) cube([15,23,14],center=true);
    }
    translate([29,11.5,5]) cylinder(h=8,d=2.3);
    translate([-29,11.5,5]) cylinder(h=8,d=2.3);   
    translate([-29,-11.5,5]) cylinder(h=8,d=2.3);    
    translate([29,-11.5,5]) cylinder(h=8,d=2.3);  
}

translate([0,0,100]) bottom();
color("red") cuby_cylinder();
///*translate([0,0,20])*/ diffuser();