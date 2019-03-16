public class Quaternion {
  
public float x, y, z, w;
public Quaternion() {
    x = y = z = 0;
    w = 1;
}

public Quaternion(float _x, float _y, float _z, float _w) {
    x = _x;
    y = _y;
    z = _z;
    w = _w;
}

public Quaternion(float angle, PVector axis) {
    setAngleAxis(angle, axis);
}

public Quaternion get() {
    return new Quaternion(x, y, z, w);
}

public Boolean equal(Quaternion q) {
    return x == q.x && y == q.y && z == q.z && w == q.w;
}

public float[][] getDCM() {
    float[][] dcm = new float[3][3];
    float q0 = w;
    float q1 = x;
    float q2 = y;
    float q3 = z;
    
    float q00 = q0*q0;
    float q11 = q1*q1;
    float q22 = q2*q2;
    float q33 = q3*q3;
    float q01 = q0*q1;
    float q02 = q0*q2;
    float q03 = q0*q3;
    float q12 = q1*q2;
    float q13 = q1*q3;
    float q23 = q2*q3;
    
    dcm[0][0] = q00+q11-q22-q33;
    dcm[0][1] = 2*(q12+q03);
    dcm[0][2] = 2*(q13-q02);
    dcm[1][0] = 2*(q12-q03);
    dcm[1][1] = q00-q11+q22-q33;
    dcm[1][2] = 2*(q23+q01);
    dcm[2][0] = 2*(q13+q02);
    dcm[2][1] = 2*(q23-q01);
    dcm[2][2] = q00-q11-q22+q33;
        
    
    return dcm;
}

public float[] getEA() {
    float[] ea = new float[3];
    float[][] dcm = new float[3][3];
    dcm = getDCM();
    ea[0] = atan(dcm[0][1]/dcm[0][0]);
    ea[1] = -asin(dcm[0][2]);
    ea[2] = atan(dcm[1][2]/dcm[2][2]);
    return ea;  
}

public void set(float _x, float _y, float _z, float _w) {
    x = _x;
    y = _y;
    z = _z;
    w = _w;
}

public void setAngleAxis(float angle, PVector axis) {
    axis.normalize();
    float hcos = cos(angle / 2);
    float hsin = sin(angle / 2);
    w = hcos;
    x = axis.x * hsin;
    y = axis.y * hsin;
    z = axis.z * hsin;
}

public Quaternion conj() {
    Quaternion ret = new Quaternion();
    ret.x = -x;
    ret.y = -y;
    ret.z = -z;
    ret.w = w;
    return ret;
}

public Quaternion mult(float r) {
    Quaternion ret = new Quaternion();
    ret.x = x * r;
    ret.y = y * r;
    ret.z = z * r;
    ret.w = w * w;
    return ret;
}

public Quaternion mult(Quaternion q) {
    Quaternion ret = new Quaternion();
    ret.x = q.w*x + q.x*w + q.y*z - q.z*y;
    ret.y = q.w*y - q.x*z + q.y*w + q.z*x;
    ret.z = q.w*z + q.x*y - q.y*x + q.z*w;
    ret.w = q.w*w - q.x*x - q.y*y - q.z*z;
    return ret;
}


public PVector mult(PVector v) {
  float px = (1 - 2 * y * y - 2 * z * z) * v.x +
             (2 * x * y - 2 * z * w) * v.y +
             (2 * x * z + 2 * y * w) * v.z;
             
  float py = (2 * x * y + 2 * z * w) * v.x +
             (1 - 2 * x * x - 2 * z * z) * v.y +
             (2 * y * z - 2 * x * w) * v.z;
             
  float pz = (2 * x * z - 2 * y * w) * v.x +
             (2 * y * z + 2 * x * w) * v.y +
             (1 - 2 * x * x - 2 * y * y) * v.z;

  return new PVector(px, py, pz);
}

public void normalize(){
  float len = w*w + x*x + y*y + z*z;
  float factor = 1.0f / sqrt(len);
  x *= factor;
  y *= factor;
  z *= factor;
  w *= factor;
}

}
