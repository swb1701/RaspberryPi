//building facade
height=200;
width=100;
thick=3;
windows_across=4;
window_space=width/windows_across;
window_width=15;
floors=4;
room_depth=60;
led_tube_diam=13;
led_tube_len=20;
back_depth=40;

floor_heights=[60,50,50,30];
floor_window_frac=[0.6,0.6,0.6,0.6];
floor_window_offset=[8,8,8,8];

module window_sub(floor,from,to,n) {
    translate([n*window_space+(window_space-window_width)/2,from+floor_window_offset[floor],-1]) union() {
        if (floor>0) {
            cube([window_width,(to-from)*floor_window_frac[floor],thick+4]); //window hole
        }
        if (floor==0) {
            if (n==2) {
          translate([0,-6,0]) cube([window_width,(to-from)*floor_window_frac[floor],thick+4]); //bottom window hole
            translate([window_width/2,30,0]) linear_extrude(height=thick+4) circle(d=window_width,$fn=100); //bottom window oval                
            } else {
            cube([window_width,(to-from)*floor_window_frac[floor]-5,thick+4]); //bottom window hole
            translate([window_width/2,30,0]) linear_extrude(height=thick+4) circle(d=window_width,$fn=100); //bottom window oval
            }
        }
    }
}

module window_add(floor,from,to,n) {
    window_height=(to-from)*floor_window_frac[floor];
   if (floor>0 || n!=2) {    
    translate([n*window_space+(window_space-window_width)/2+1,from+4,thick]) cube([window_width-2,3,thick]); //window boxes
 
    translate([n*window_space+(window_space-window_width)/2,from+7,thick]) cube([window_width,1,thick+1]);  //window sill  
    }
    if (floor==3) {
        translate([n*window_space+(window_space-window_width)/2,from+floor_window_offset[floor]+(to-from)*0.3-0.5,0]) cube([window_width,1,thick-1]); //top window horizontal
        translate([n*window_space+(window_space-window_width)/2+window_width/2-0.5,from+floor_window_offset[floor],0]) cube([1,(to-from)*floor_window_frac[floor],thick-1]); //top window vertical   
    } else {
     translate([n*window_space+(window_space-window_width)/2,from+floor_window_offset[floor]+(to-from)*floor_window_frac[floor]/3-0.5,0]) cube([window_width,1,thick-1]); //window bottom horizontal
     if (floor==0 && n==2) {
    translate([n*window_space+(window_space-window_width)/2,from+floor_window_offset[floor]+(to-from)*0-0.5,0]) cube([window_width,1,thick-1]); //window bottom horizontal         
     }
    translate([n*window_space+(window_space-window_width)/2,from+floor_window_offset[floor]+(to-from)*floor_window_frac[floor]/3*2-0.5,0]) cube([window_width,1,thick-1]); //window top horizontal       
        translate([n*window_space+(window_space-window_width)/2+window_width/2-0.5,from+floor_window_offset[floor]-8,0]) cube([1,(to-from)*floor_window_frac[floor]+20,thick-1]);//window bottom vertical            
    }
    if (floor>0) {
        translate([0,2,0])
        difference() {
            translate([n*window_space+(window_space-window_width)/2-2,from+window_height+4,thick]) union() {
                if (floor==3) {
                     translate([0,0.51,0]) cube([window_width+4,0.2*window_height,thick]); //top window cover
                } else {
                cube([window_width+4,0.2*window_height-2,thick]); //window cover
                translate([window_width/2+2,4,0]) linear_extrude(height=thick) resize([window_width+4,10]) circle(d=window_width+4,$fn=100); //window cover oval
                }
            };
            translate([0,-2,1]) window_sub(floor,from,to,n);
        }
    }
    
}

function get_from(floor) = (floor==0 ? 0 : floor_heights[floor-1]+get_from(floor-1));

function get_to(floor) = (floor==0 ? floor_heights[0] : floor_heights[floor]+get_to(floor-1));

module floor_add(n,from,to) {
        if (from>0) translate([0,from,thick]) cube([width,3,thick]);
        for(i=[0:windows_across-1]) {
            window_add(n,from,to,i); //add window parts
        }
}

module floor_sub(n,from,to) {
        for(i=[0:windows_across-1]) {  
            window_sub(n,from,to,i); //subtract window parts
        }
}

module facade() {
    difference() {
        cube([width,height,thick]); //make the floor
        for(i=[0:floors-1]) {
            floor_sub(i,get_from(i),get_to(i)); //perform the subtracts
        } 
    }
    for(i=[0:floors-1]) {
        floor_add(i,get_from(i),get_to(i));  //perform the adds
    }      
}

module rooms() {
    room_width=(width-5*thick)/windows_across;
    difference() {
        union() {
    difference() {
        cube([width,height,room_depth]);
        for(i=[0:floors-1]) {
            for(j=[0:windows_across-1]) {
                translate([thick+j*(room_width+thick),thick+get_from(i),thick]) 
                if (i==3) {
                    cube([room_width,get_to(i)-get_from(i)-1.5*thick+8,room_depth-thick+1]);    
                } else {
                    cube([room_width,get_to(i)-get_from(i)-1.5*thick,room_depth-thick+1]);
                }
            }
        }
    }
    for(i=[0:floors-1]) {
            for(j=[0:windows_across-1]) {  
                  if (i==3) {
   translate([thick+j*(room_width+thick)+room_width/2,thick+get_from(i)+(get_to(i)-get_from(i)-1.5*thick+8)/2,thick])
       cylinder(d=led_tube_diam+3,h=led_tube_len,$fn=100);                      
      
   
                  } else {
                  translate([thick+j*(room_width+thick)+room_width/2,thick+get_from(i)+(get_to(i)-get_from(i)-1.5*thick)/2,thick]) 
                      cylinder(d=led_tube_diam+3,h=led_tube_len,$fn=100);
                     
                 
                  }
            }
    }
}
  for(i=[0:floors-1]) {
            for(j=[0:windows_across-1]) {  
                  if (i==3) {
   translate([thick+j*(room_width+thick)+room_width/2,thick+get_from(i)+(get_to(i)-get_from(i)-1.5*thick+8)/2,thick])                    
       translate([0,0,-thick-5]) cylinder(d=led_tube_diam,h=led_tube_len+thick+10,$fn=100);
   
                  } else {
                  translate([thick+j*(room_width+thick)+room_width/2,thick+get_from(i)+(get_to(i)-get_from(i)-1.5*thick)/2,thick]) 
                      translate([0,0,-thick-5]) cylinder(d=led_tube_diam,h=led_tube_len+thick+10,$fn=100);
                  
                  }
            }
    }
}
}

module test_cylinder() {
    difference() {
         cylinder(d=led_tube_diam+3,h=led_tube_len,$fn=100);
         translate([0,0,-thick-5]) cylinder(d=led_tube_diam,h=led_tube_len+thick+10,$fn=100);        
    }
}

module back_cover() {
       border=2;
       overlap=10;
       translate([-border,0,0]) difference() {
        cube([width+2*border,height+border,back_depth+overlap+border+thick]);
        translate([thick,thick,thick]) cube([width+2*border-thick*2,height+border-thick*2,back_depth+overlap+border+1]);  
        translate([border-1,-1,back_depth+border+thick]) cube([width+2,height+2,overlap+1]);
        translate([thick,thick,-1]) cube([15,10,10]);
       }
}

//translate([0,0,room_depth+50]) facade();
//facade();
//translate([0,0,46]) rooms();
//test_cylinder();
back_cover();