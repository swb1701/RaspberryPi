    h=10;
d1=200; //turntable diameter
d2=20*25.4; //platform diameter
wh=6;
th=50;
$fn=200;

module turntable() {
    color("white") cylinder(d=d1,h=th,center=true);
}

module wood() {
    color("#c39b77") cylinder(d=d2,h=wh,center=true);
}

module arc(radius, thick, angle){
	intersection(){
		union(){
			rights = floor(angle/90);
			remain = angle-rights*90;
			if(angle > 90){
				for(i = [0:rights-1]){
					rotate(i*90-(rights-1)*90/2){
						polygon([[0, 0], [radius+thick, (radius+thick)*tan(90/2)], [radius+thick, -(radius+thick)*tan(90/2)]]);
					}
				}
				rotate(-(rights)*90/2)
					polygon([[0, 0], [radius+thick, 0], [radius+thick, -(radius+thick)*tan(remain/2)]]);
				rotate((rights)*90/2)
					polygon([[0, 0], [radius+thick, (radius+thick)*tan(remain/2)], [radius+thick, 0]]);
			}else{
				polygon([[0, 0], [radius+thick, (radius+thick)*tan(angle/2)], [radius+thick, -(radius+thick)*tan(angle/2)]]);
			}
		}
		difference(){
			circle(radius+thick);
			circle(radius);
		}
	}
}

module align() {
    linear_extrude(height=h) {
        arc(d1/2+0.4,10,45);
    }
    translate([-10,0,0]) linear_extrude(height=h) {
        arc(d2/2,10,20);
    } 
    translate([178,0,5]) cube([140,10,10],center=true);
  
}

module trace() {
    difference() {
      translate([-10,0,0]) linear_extrude(height=h) {
        arc(d2/2,20,20);
    }
   translate([258,0,5]) cylinder(h=15,d=8,center=true); 
      rotate([0,0,3]) translate([258,0,5]) cube([1,8,15],center=true);
      rotate([0,0,-3]) translate([258,0,5]) cube([1,8,15],center=true);    
}
}

module trace2() {
    difference() {
      translate([-10,0,0]) linear_extrude(height=h) {
        arc(d2/2,12,20);
    }
   translate([250,0,5]) cylinder(h=15,d=8,center=true); 
      rotate([0,0,3]) translate([248,0,5]) cube([1,8,15],center=true);
      rotate([0,0,-3]) translate([248,0,5]) cube([1,8,15],center=true);    
}
}

module clamp() {
    difference() {
     linear_extrude(height=8) {
        arc(d1/2+0.4,10,88);
    }
    translate([105,0,6.75-2.75]) rotate([0,90,0]) cylinder(h=20,d=2.5,center=true);
    rotate([0,0,30]) translate([105,0,6.75-2.75]) rotate([0,90,0]) cylinder(h=20,d=2.5,center=true);
    rotate([0,0,-30]) translate([105,0,6.75-2.75]) rotate([0,90,0]) cylinder(h=20,d=2.5,center=true);
    }
}

translate([0,0,-25]) union() {
    for(a=[0:90:270]) rotate([0,0,a]) clamp();
}
translate([0,0,-25]) clamp();
translate([20,0,-25]) align();
rotate([0,0,45]) trace2();
translate([0,0,-th/2-wh/2]) wood();
turntable();

