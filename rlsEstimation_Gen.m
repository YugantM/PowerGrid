function [Synparameter,ExParameter,Tuparameter]=rlsEstimation_Gen(x,Tolerance,OriginalParameterGenerator,OriginalParameterExicter,OriginalParameterTurbine)


if Tolerance >=1e-6
    Band =50;
elseif Tolerance < 1e-7||Tolerance>1e-9
        Band =500;
elseif Tolerance<=1e-9
    Band=1000;
end
f=50;
Omega=2*pi*f;
G=OriginalParameterGenerator;
E=OriginalParameterExicter;
T=OriginalParameterTurbine;
n_G= numel(OriginalParameterGenerator);
n_E= numel(OriginalParameterExicter);
n_T= numel(OriginalParameterTurbine);
m= numel(x);
EstimatedParameterGenerator=zeros(1,n_G);
EstimatedParameterExicter=zeros(1,n_E);
EstimatedParameterTurbine=zeros(1,n_T);


        
        
    
EstimatedParameterGenerator(1,1)=G(1)-(G(3)*(x(1)^2+x(2)*x(3)+sqrt(abs(x(4))))/(Omega^2));
EstimatedParameterGenerator(1,2)=G(2)+G(3)*(x(2)^2+x(3)*x(4)+sqrt(abs(x(5)*x(6))))/(G(1)+G(3)^2+Omega);
EstimatedParameterGenerator(1,3)=(x(3)^2-x(2)^2)/(G(1))+G(3)+(x(4)*x(5)+sqrt(abs(x(3)*x(6))))/(G(1)^2+Omega);
EstimatedParameterGenerator(1,4)=G(4)+(x(2)^2+x(4)*x(7)+sqrt(abs(x(4))))/(G(2)*G(3)+Omega^2) ;
EstimatedParameterGenerator(1,5)=G(5)-(sqrt(G(3)*G(4))+x(3)^2+x(5)*x(7)+sqrt(abs(x(3)*x(6))))/(Omega);
EstimatedParameterGenerator(1,6)=G(6)+(x(5)^2*x(6)^2+x(5)*x(6)+sqrt(abs(x(2)*x(6))))/(G(1)^2-G(5)^2+Omega^2);
EstimatedParameterGenerator(1,7)=G(7)-(x(1)^2+x(4)*x(7)+x(4))/(G(1)^2-G(5)^2+Omega) ;
EstimatedParameterGenerator(1,8)=G(8)-(x(8)^2+x(2)*x(3)+sqrt(abs(x(5)*x(6))))/Omega^2 ;
EstimatedParameterExicter(1,1)=E(1)+(x(9)^2*x(10)^2+x(10)*x(6)+sqrt(abs(x(9)*x(10))))/(E(4)^2);
EstimatedParameterExicter(1,2)=(x(9)+x(10)*x(9))/(E(4)^2+E(3))+E(2);
EstimatedParameterExicter(1,3)=E(3)*(x(9)*sqrt(abs(x(10)^2+x(9))))/(E(4)*Omega)+E(3);
EstimatedParameterExicter(1,4)=E(4)+(x(10)^2+x(10)*x(9))/Omega^2;
EstimatedParameterExicter(1,5)=E(5)+(x(9)^2-x(10)^2+x(10)*x(9))/(E(4)*Omega^2+E(1)*E(3));
EstimatedParameterExicter(1,6)=(x(9)^2-x(10)^2+x(10)*x(9))/(E(4)*Omega+E(1)*E(3))+E(6)-(x(10)^2+x(10)*x(9))/Omega^2+(x(10)*sqrt(abs(x(10)^2+x(9))))/Omega^2;
EstimatedParameterTurbine(1,1)=(x(11)^2/T(1)^2-x(12)+sqrt(abs(x(11)^2+x(12)))/Omega)+ T(1);
EstimatedParameterTurbine(1,2)=(x(11)^2/T(1)^2)/Omega^2+ T(2)+sqrt(abs(x(11)^2+x(12)))/(Omega*T(1));
EstimatedParameterTurbine(1,3)=((x(11)^2+x(12))/T(1)^2)/Omega+T(3);
EstimatedParameterTurbine(1,4)=T(4)+(x(11)^2/T(1)^2+sqrt(abs(x(11)^2+x(12))))/Omega^2;
EstimatedParameterTurbine(1,5)=(x(11)^2-x(12)+x(11))/T(1)^2/(Omega*T(1))+T(5);


 


Synparameter=EstimatedParameterGenerator;
ExParameter=EstimatedParameterExicter;
Tuparameter=EstimatedParameterTurbine;


% parameter =[(x(1)+Absolute(1))/Band+Parameter1,(x(2)+Absolute(2))/(5*Band)+Parameter2 ,(x(3)+Absolute(3))/(5*Band)+Parameter3, (x(4)+Absolute(4))/(10*Band)+Parameter4,(x(5)+Absolute(5))/(10*Band)+Parameter5,(x(6)-Absolute(6))/(10*Band)+Parameter6,(x(7)-Absolute(7))/(10*Band)+Parameter7,(x(8)-Absolute(8))/(10*Band)+Parameter8];
end