close all;
N = width(clfdata)-2
figure(1)
M = [2,4,6,7,9,13,15,14,16,19,21,20,21];
subplot(2,1,1)
hold on
for i = 1:N
    if(i < 7)
        plot(A(:,i),'--')
    end
end
xlabel('Time (s)'); ylabel('Response Voltage (V)');
title('Pure CH4 Tests')
hold off

subplot(2,1,2)
hold on
for i = 1:N
    if(i > 7)
        plot(A(:,i),'.')
    end
end
xlabel('Time (s)'); ylabel('Response Voltage (V)');
title('Only Mixture Tests')
hold off

figure(2)
hold on
for i = 1:length(M)
    if(i < 7)
        plot(A(:,M(i)),'--')
    else
        plot(A(:,M(i)),'.')
    end
end
xlabel('Time (s)'); ylabel('Response Voltage (V)');
title('Varing 20% Mixture of CH4 to H2 Tests Comparison to Pure')
hold off

    
