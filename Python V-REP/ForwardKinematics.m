s1 = [0 -1 0 0; 1 0 0 0; 0 0 0 0; 0 0 0 0];
s2 = [0 0 1 -.2305; 0 0 0 0; -1 0 0 0; 0 0 0 0];
s3 = [0 -1 0 .1315; 1 0 0 0; 0 0 0 0; 0 0 0 0];
s4 = [0 0 -1 .2755; 0 0 0 0; 1 0 0 0; 0 0 0 0];
s5 = [0 -1 0 -.1210; 1 0 0 0; 0 0 0 0; 0 0 0 0];
s6 = [0 0 1 -.2869; 0 0 0 0; -1 0 0 0; 0 0 0 0];
s7 = [0 -1 0 .0958; 1 0 0 0; 0 0 0 0; 0 0 0 0];
M = [1 0 0 0; 0 1 0 .1603; 0 0 1 1.1045; 0 0 0 1];
conv = pi/180;
theta = [-150*conv, -90*conv, 0, 50*conv, 0, 110*conv, 0]; 
%theta = [-160*conv, -90*conv, 28*conv, 65.45*conv, 0, 112.4*conv, 0]; 
%theta = [-160*conv, -90*conv, 28*conv, 65.45*conv, 0, 112.4*conv, 270]; 
T = expm(s1*theta(1))*expm(s2*theta(2))*expm(s3*theta(3))*expm(s4*theta(4))*expm(s5*theta(5))*expm(s6*theta(6))*expm(s7*theta(7))*M