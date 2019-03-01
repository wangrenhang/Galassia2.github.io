clear
N=100; %number of samples
T=0.25; %sampling interval
sw=1; % sigma_w
sv=0.1; % sigma_v

A=[1 T; 0 1]; %process matrix
C=[1 0;0 1]; %process matrix
R1=sw^2*[T^4/4 T^3/2; T^3/2 T^2]; %covariance of process noise
R2=[sv^2 sv^2;sv^2 sv^2]; %covariance of measurement noise
Pm(:,:,1)=1e3.*eye(2); %P(0|-1)
xhm(:,1)=[0 0]'; %xhm(:,1)=x(0|-1)
x(:,1)=[0 0]'; %x(:,1)=x(0)
y(:,1)=[0 0]';
w=random('normal',0,sw,1,N); %process noise
v=random('normal',0,sv,1,N); %measurement noise

%To plot and calculate
x1k=zeros(1,N);
x1hatk=zeros(1,N);
x2k=zeros(1,N);
x2hatk=zeros(1,N);
p11kk=zeros(1,N);
p22kk=zeros(1,N);
kf1k=zeros(1,N);
kf2k=zeros(1,N);
bias1=0;
bias2=0;
variance1=0;
variance2=0;

for k=1:N
    Kf(:,:,k)=Pm(:,:,k)*C'*(C*Pm(:,:,k)*C'+R2)^(-1); %Kf(:,k)=Kf(k)
    K(:,:,k)=(A*Pm(:,:,k)*C')*(C*Pm(:,:,k)*C'+R2)^(-1); %K(:,k)=K(k)
    P(:,:,k)=Pm(:,:,k)-(Pm(:,:,k)*C')*(C*Pm(:,:,k)*C'+R2)^(-1)*C*Pm(:,:,k); %P(:,:,k)=P(N|N)
    Pm(:,:,k+1)=A*Pm(:,:,k)*A'+R1-K(:,:,k)*(C*Pm(:,:,k)*C'+R2)*K(:,:,k)'; %Pm(:,:,k+1)=P(N+1|N)
    x(:,k+1)=A*x(:,k)+[T^2/2 T]'*w(k); %x(:,k+1)=x(k+1)
    y(:,k)=C*x(:,k)+[v(k);v(k)]; %y(k)=y(k)
    xh(:,k)=xhm(:,k)+Kf(:,:,k)*(y(:,k)-C*xhm(:,k)); %xh(:,k)=x^hat(k|k)
    xhm(:,k+1)=A*xhm(:,k)+K(:,:,k)*(y(:,k)-C*xhm(:,k)); %xhm(:,k+1)=x^hat(k+1|k)
    
    % Variables related to x1
    x1k(k)=x(1,k);
    x1hatk(k)=xh(1,k);
    p11kk(k)=P(1,1,k);
    kf1k(k)=Kf(1,k);
    bias1=bias1+(x1k(k)-x1hatk(k));
    variance1=variance1+(x1k(k)-x1hatk(k))^2;
    
    % Variables related to x2
    x2k(k)=x(2,k);
    x2hatk(k)=xh(2,k);
    p22kk(k)=P(2,2,k);
    kf2k(k)=Kf(2,k);
    bias2=bias2+(x2k(k)-x2hatk(k));
    variance2=variance2+(x2k(k)-x2hatk(k))^2;
end

figure(1)
plot(x1k,'k-')
hold on 
plot(x1hatk,'k:')
legend('theta(k)','theta(k|k)')
grid %draw grid on the plot
xlabel('Data points') %x-axis label
ylabel('theta / rad')
hold off
title('Real theta vs. estimated theta')

figure(2)
plot(x2k,'k-')
hold on 
plot(x2hatk,'k:')
legend('w(k)','w(k|k)')
grid %draw grid on the plot
xlabel('Data points') %x-axis label
ylabel('w / rad/s')
hold off
title('Real w vs. estimated w')