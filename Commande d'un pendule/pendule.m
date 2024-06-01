%Fonction de simulation du pendule du pendule inverse.

function [sys, x0] = pendule(t, x, u, flag)

    g = 9.81 ;
    l = 0.5 ;
    m = 0.1 ;
    M = 2 ;
    
    if flag == 0
        %Initialisation
        % sys=[nb etat cont; nb etat dis; nb de  sortie; nb d'entree; nb de comm direct; nb de periode d'ech]
        sys = [ 4, 0, 4, 1, 0, 1] ;
        %sys = [4, 0, 1, 1, 0, 1];
        x0 = [2; 5*pi/180; 0 ;0]; 
    end
    
    if flag == 1
        %Intégration
        f1 = x(3) ;
        f2 = x(4) ;
        f3 = (m*l*x(4)*x(4)*sin(x(2))-m*g*cos(x(2))*sin(x(2)))/(M+m*sin(x(2))*sin(x(2)))+(l*u(1))/(l*(M+m*sin(x(2))*sin(x(2)))) ;
        f4 = (-m*l*x(4)*x(4)*sin(x(2))*cos(x(2))+(M+m)*g*sin(x(2)))/(l*(M+m*sin(x(2))*sin(x(2))))+(-cos(x(2))*u(1))/(l*(M+m*sin(x(2))*sin(x(2)))) ;
        sys = [f1; f2; f3; f4];
    end
    
    if flag == 3 
        %Calcul des sorties
        sys = [ x(1); x(2); x(3); x(4)] ;
        %sys=x(1);
    end
end