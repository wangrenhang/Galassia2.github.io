import peasy.*;
PeasyCam cam;

PFont xText, yText,zText;

int ang = 0;

void setup() {
  size(640, 640, P3D);
  cam = new PeasyCam(this, 600);
}

void draw() {
  background(150);
  
  stroke(0);
  fill(255);
  lights();
  
  Quaternion xRot = new Quaternion();
  //Quaternion xRot = new Quaternion(x, y, z, w);
  xRot.setAngleAxis(radians(ang), new PVector(-2, 0.6, 1));
  ang += 1;
  float[] ea = new float[3];
  ea = xRot.getEA();
  
  rotateZ(ea[0]);
  rotateY(ea[1]);
  rotateX(ea[2]);
  box(80, 150, 80);
  
  showAxis();
  
}

void showAxis(){
  xText = createFont("Arial", 20, true);
  stroke(255, 0, 0);
  line(0, 0, 0, 200, 0, 0);
  textFont(xText, 20);
  fill(255, 0, 0);
  text("X", 220,0,0);
  yText = createFont("Arial", 20, true);
  stroke(0, 255, 0);
  line(0, 0, 0, 0, 200, 0);
  textFont(yText, 20);
  fill(0, 255, 0);
  text("Y", 0,220,0);
  zText = createFont("Arial", 20, true);
  stroke(0, 0, 255);
  line(0, 0, 0, 0, 0, 200);
  textFont(zText, 20);
  fill(0, 0, 255);
  text("Z", 0,0,220);
}
