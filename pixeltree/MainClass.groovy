package com.swblabs.lasertree

class MainClass {

	static void main(String... args) {
		def mc=new MainClass()
		mc.buildTree()
	}

	double boxWidth=400
	double boxHeight=400

	def buildTree() {
		File file=new File("c:/lasertree/lasertree.svg")
		if (file.exists()) file.delete()
		file<<'<svg width="'+boxWidth+'mm" height="'+boxHeight+'mm" viewBox="0 0 '+boxWidth+' '+boxHeight+'">\n'
		file<<'<g id="layer">\n'
		file<<'<path d="'+tree(0,50,false)+'"\n'
		//file<<'      id="tree1" style="fill:#008000"/>\n'
		file<<'      id="tree1" style="fill:none;stroke:#008000"/>\n'
		file<<'<path d="'+tree(0,50,true)+'"\n'
		//file<<'      id="tree2" style="fill:#008000"/>\n'
		file<<'      id="tree2" style="fill:none;stroke:#008000"/>\n'
		file<<'</g>\n'
		file<<'</svg>\n'
	}

	double baseWidth=160
	double treeHeight=1.618*baseWidth //golden ratio
	double ringWidth=6 //was 8 (actual)
	double topRingWidth=12
	double thickness=3.175
	List<Double> rings=[16, 36, 56, 76, 96, baseWidth-ringWidth] //inner diameters in mm
	def pt(StringBuilder sb,x,y,boolean flip) {
		if (flip) {
			x=x+baseWidth*0.6
			y=treeHeight-(y-50)+50
		}
		println(x+","+y)
		sb.append(" "+x+","+y)
	}

	def tree(double ulx,double uly,boolean flip=false) {
		int treeparts=rings.size()
		double partHeight=treeHeight/treeparts
		double partWidth=baseWidth/2/treeparts
		StringBuilder sb=new StringBuilder()
		double x=ulx+baseWidth/2
		double y=uly
		println("x="+x+" y="+uly)
		sb.append("M")
		if (!flip) {
			pt(sb,x-thickness/2,y,flip)
			pt(sb,x-thickness/2,y+treeHeight/2,flip)
			pt(sb,x+thickness/2,y+treeHeight/2,flip)
			pt(sb,x+thickness/2,y,flip)
		} else {
			pt(sb,x,y,flip)
		}
		pt(sb,x+topRingWidth/2,y,flip)
		for(int i=0;i<treeparts;i++) {
			pt(sb,x+rings[i]/2,y+partHeight*(i+1),flip)
			if (i<(treeparts-1)) {
				pt(sb,x+rings[i]/2+ringWidth,y+partHeight*(i+1),flip)
			}
			if (i<(treeparts-2)) {
				pt(sb,x+rings[i]/2+ringWidth,y+partHeight*(i+1)+partHeight*0.2,flip)
				pt(sb,x+thickness*2*(i+1),y+partHeight*(i+1)+partHeight*0.1,flip)
			}
		}
		if (flip) {
			pt(sb,x+thickness/2,y+partHeight*treeparts,flip)
			pt(sb,x+thickness/2,y+treeHeight/2,flip)
			pt(sb,x-thickness/2,y+treeHeight/2,flip)
			pt(sb,x-thickness/2,y+partHeight*treeparts,flip)
		}
		for(int i=treeparts-1;i>=0;i--) {
			if (i<(treeparts-2)) {
				pt(sb,x-thickness*2*(i+1),y+partHeight*(i+1)+partHeight*0.1,flip)
				pt(sb,x-rings[i]/2-ringWidth,y+partHeight*(i+1)+partHeight*0.2,flip)
			}
			if (i<(treeparts-1)) {
				pt(sb,x-rings[i]/2-ringWidth,y+partHeight*(i+1),flip)
			}
			pt(sb,x-rings[i]/2,y+partHeight*(i+1),flip)
		}
		pt(sb,x-topRingWidth/2,y,flip)
		if (flip) {
		  pt(sb,x,y,flip)
		} else {
		  pt(sb,x-thickness/2,y,flip)
		}
		return(sb.toString())
	}
}