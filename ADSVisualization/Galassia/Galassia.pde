//Z axis data should multiply -1
//X Y rotation should multiply -1
import processing.serial.*;
Serial port; 
import peasy.*;
PeasyCam cam;

PFont xText, yText, zText, sText;

float sqx=0, sqy=0, sqz=0, sqw = 1;

float qx=0, qy=0, qz=0, qw = 1;

int ang = 0;
String myString = "";

void setup() {
  size(1000, 1000, P3D);
  cam = new PeasyCam(this, 600);
  port= new Serial(this, "COM3", 38400);  
}

void draw() {
  
  String[] sunLoc = new String[4];
  String[] qLoc = new String[4];
  String info = "";
  String msg = "";
  myString = "";
  try{
    if(port.available() > 0) {
      msg = port.readString();
      for(int i =0;i<msg.length();i++){
        if(msg.charAt(i) == '\n'){
          //print(myString);
          if(myString.startsWith("KalQ:")){
            println(myString);
            info = myString.substring(6, myString.length()-1); 
            if(info != null){
              //sunLoc = info.split(" ");    
              //sunX = Float.parseFloat(sunLoc[0]);
              //sunY = Float.parseFloat(sunLoc[1]);
              //sunZ = -1*Float.parseFloat(sunLoc[2]);
              qLoc = info.split(" ");    
              qw = Float.parseFloat(qLoc[0]);
              qx = Float.parseFloat(qLoc[1]);
              qy = Float.parseFloat(qLoc[2]);
              qz = -Float.parseFloat(qLoc[3]);
            }
          }
          else if(myString.startsWith("Desired_Quat:")){
            println(myString);
            info = myString.substring(14, myString.length()-1); 
            if(info != null){
              sunLoc = info.split(" ");    
              sqw = Float.parseFloat(sunLoc[0]);
              sqx = Float.parseFloat(sunLoc[1]);
              sqy = Float.parseFloat(sunLoc[2]);
              sqz = -Float.parseFloat(sunLoc[3]);
            }
          }
          myString = "";
        }
        else
          myString += msg.charAt(i);
      }
    }
  }catch(Exception e)
  {
    println("Something Error");
  }
  
  background(175);
  
  stroke(0);
  fill(255);
  
  //Quaternion rot = new Quaternion();
  Quaternion rot = new Quaternion(qx, qy, qz, qw);
  Quaternion sunrot = new Quaternion(sqx, sqy, sqz, sqw);
  //rot.setAngleAxis(radians(ang), new PVector(0.5, 1, 2));
  ang += 1;
  if(ang == 361)
    ang = 0;
  
  //Satellite coordinate
  showAxis(rot, "x", 255, "y", 255, "z", 255);
  
  //+Z Bottom
  showLine(-50, 50, -150, 50, 50, -150, rot);
  showLine(50, 50, -150, 50, -50, -150, rot);
  showLine(50, -50, -150, -50, -50, -150, rot);
  showLine(-50, -50, -150, -50, 50, -150, rot);
  
  //-Z Bottom
  showLine(-50, 50, 150, 50, 50, 150, rot);
  showLine(50, 50, 150, 50, -50, 150, rot);
  showLine(50, -50, 150, -50, -50, 150, rot);
  showLine(-50, -50, 150, -50, 50, 150, rot);
  
  //Side
  showLine(-50, 50, 150, -50, 50, -150, rot);
  showLine(50, 50, 150, 50, 50, -150, rot);
  showLine(50, -50, 150, 50, -50, -150, rot);
  showLine(-50, -50, 150, -50, -50, -150, rot);
  
  //Left Wing
  showLine(-50, 50, -150, -50, 150, -150, rot);
  showLine(-50, 150, -150, -50, 150, 150, rot);
  showLine(-50, 150, 150, -50, 50, 150, rot);
  
  //Right Wing
  showLine(-50, -50, -150, -50, -150, -150, rot);
  showLine(-50, -150, -150, -50, -150, 150, rot);
  showLine(-50, -150, 150, -50, -50, 150, rot);
  
  //Inertial coordinate
  rot.set(0,0,0,1);
  showAxis(rot, "X", 0, "Y", 0, "Z", 0);
  
  //Sun
  PVector sun = new PVector();
  sun.set(250, 0, 0);
  sun = sunrot.mult(sun);
  //println(sqw, sqx, sqy, sqz);
  sText = createFont("Arial", 20, true);
  textFont(sText, 20);
  fill(255, 255, 0);
  text("Sun", sun.x, sun.y, sun.z);
  noStroke();
  fill(255, 0, 0, 100);
  translate(sun.x, sun.y, sun.z);
  sphere(30);
  
}

void showAxis(Quaternion q, 
              String nameX, int colorX,
              String nameY, int colorY,
              String nameZ, int colorZ){
  PVector axis = new PVector();
  PVector axname = new PVector();
  
  xText = createFont("Arial", 20, true);
  stroke(colorX, 0, 0);
  textFont(xText, 20);
  fill(colorX, 0, 0);
  axis.set(200, 0, 0);
  axname.set(220, 0, 0);
  axis = q.mult(axis);
  axname = q.mult(axname);
  line(0, 0, 0, axis.x, axis.y, axis.z); 
  text(nameX, axname.x,axname.y,axname.z);
  
  yText = createFont("Arial", 20, true);
  stroke(0, colorY, 0);
  textFont(yText, 20);
  fill(0, colorY, 0);
  axis.set(0, 200, 0);
  axname.set(0, 200, 0);
  axis = q.mult(axis);
  axname = q.mult(axname);
  line(0, 0, 0, axis.x, axis.y, axis.z); 
  text(nameY, axname.x,axname.y,axname.z);
  
  zText = createFont("Arial", 20, true);
  stroke(0, 0, colorZ);
  textFont(zText, 20);
  fill(0, 0, colorZ);
  axis.set(0, 0, -200);
  axname.set(0, 0, -200);
  axis = q.mult(axis);
  axname = q.mult(axname);
  line(0, 0, 0, axis.x, axis.y, axis.z); 
  text(nameZ, axname.x,axname.y,axname.z);
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
