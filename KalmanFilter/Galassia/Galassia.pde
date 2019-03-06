//Z axis data should multiply -1
//X Y rotation should multiply -1
import processing.serial.*;
Serial port; 
import peasy.*;
PeasyCam cam;

PFont xText, yText,zText;

int ang = 0;

void setup() {
  size(640, 640, P3D);
  cam = new PeasyCam(this, 600);
  port= new Serial(this, "COM3", 38400);  
}

void draw() {
  
  //println(port.read());
  
  background(150);
  
  stroke(0);
  fill(255);
  lights();
  
  Quaternion rot = new Quaternion();
  //Quaternion xRot = new Quaternion(x, y, z, w);
  rot.setAngleAxis(radians(ang), new PVector(0.5, 1, 2));
  ang += 1;
  
  //Satellite coordinate
  showAxis(rot);
  
  //+Z Bottom
  showLine(-50, 50, -150, 50, 50, -150, rot);
  showLine(50, 50, -150, 50, -50, -150, rot);
  showLine(50, -50, -150, -50, -50, -150, rot);
  showLine(-50, -50, -150, -50, 50, -150, rot);
  
  //-Z Bpttom
  showLine(-50, 50, 150, 50, 50, 150, rot);
  showLine(50, 50, 150, 50, -50, 150, rot);
  showLine(50, -50, 150, -50, -50, 150, rot);
  showLine(-50, -50, 150, -50, 50, 150, rot);
  
  //Side
  showLine(-50, 50, 150, -50, 50, -150, rot);
  showLine(50, 50, 150, 50, 50, -150, rot);
  showLine(50, -50, 150, 50, -50, -150, rot);
  showLine(-50, -50, 150, -50, -50, -150, rot);
  
  //Inertial coordinate
  rot.set(0,0,0,1);
  showAxis(rot);
  
}

void showAxis(Quaternion q){
  PVector axis = new PVector();
  PVector axname = new PVector();
  
  xText = createFont("Arial", 20, true);
  stroke(255, 0, 0);
  textFont(xText, 20);
  fill(255, 0, 0);
  axis.set(200, 0, 0);
  axname.set(220, 0, 0);
  axis = q.mult(axis);
  axname = q.mult(axname);
  line(0, 0, 0, axis.x, axis.y, axis.z); 
  text("X", axname.x,axname.y,axname.z);
  
  yText = createFont("Arial", 20, true);
  stroke(0, 255, 0);
  textFont(yText, 20);
  fill(0, 255, 0);
  axis.set(0, 200, 0);
  axname.set(0, 200, 0);
  axis = q.mult(axis);
  axname = q.mult(axname);
  line(0, 0, 0, axis.x, axis.y, axis.z); 
  text("Y", axname.x,axname.y,axname.z);
  
  zText = createFont("Arial", 20, true);
  stroke(0, 0, 255);
  textFont(yText, 20);
  fill(0, 0, 255);
  axis.set(0, 0, -200);
  axname.set(0, 0, -200);
  axis = q.mult(axis);
  axname = q.mult(axname);
  line(0, 0, 0, axis.x, axis.y, axis.z); 
  text("Z", axname.x,axname.y,axname.z);
}

void showLine(int ax, int ay, int az, int bx, int by, int bz, Quaternion q){
  PVector axA = new PVector();
  PVector axB = new PVector();
  
  fill(0);
  stroke(0);
  axA.set(ax, ay, az);
  axA = q.mult(axA);
  axB.set(bx, by, bz);
  axB = q.mult(axB);
  line(axA.x, axA.y, axA.z, axB.x, axB.y, axB.z); 
}
