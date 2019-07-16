close all
figure(1)
subplot(3,2,1);
hold on;
plot(Z(:,1),'--')
plot(Z(:,2),'.')
legend('Pure Sample: 120 PPM CH4','Mix Sample:120 PPM CH4 30 PPM H2')
xlabel('Time (s)'); ylabel('Response Voltage (V)');
hold off;

subplot(3,2,2);
hold on;
plot(Z(:,3),'--')
plot(Z(:,4),'.')
legend('Pure Sample: 240 PPM CH4','Mix Sample:240 PPM CH4 60 PPM H2')
xlabel('Time (s)'); ylabel('Response Voltage (V)');
hold off;
subplot(3,2,3);
hold on;
plot(Z(:,5),'--')
plot(Z(:,6),'.')
legend('Pure Sample: 360 PPM CH4','Mix Sample:360 PPM CH4 90 PPM H2')
xlabel('Time (s)'); ylabel('Response Voltage (V)');
hold off;
subplot(3,2,4);
hold on;
plot(Z(:,7),'--')
plot(Z(:,8),'.')
legend('Pure Sample: 480 PPM CH4','Mix Sample:120 PPM CH4 120 PPM H2')
xlabel('Time (s)'); ylabel('Response Voltage (V)');
hold off;
subplot(3,2,5);
hold on;
plot(Z(:,9),'--')
plot(Z(:,10),'.')
legend('Pure Sample: 600 PPM CH4','Mix Sample:120 PPM CH4 150 PPM H2')
xlabel('Time (s)'); ylabel('Response Voltage (V)');
hold off;
subplot(3,2,6);
hold on;
plot(Z(:,11),'--')
plot(Z(:,12),'.')
legend('Pure Sample: 720 PPM CH4','Mix Sample:120 PPM CH4 180 PPM H2')
xlabel('Time (s)'); ylabel('Response Voltage (V)');
hold off;