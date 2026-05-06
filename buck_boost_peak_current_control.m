%% Peak current mode controlled buck-boost converter
% Power Electronics, University of Colorado Boulder 

% Converter parameters
Vg = 5;
D = 0.3;
Dp = 1-D;
Vout = Vg*D/Dp;
L = 33e-6;
C = 220e-6;
R = 5;
fs = 1e6;
Rf = 1;

% Peak current mode control: simple model
Gc0simple = Dp*R/((1+D)*Rf);
wz = Dp^2*R/(D*L);
wp1simple = (1+D)/(R*C);

s = tf('s');

% 1. Plant Transfer Function (Control-to-Output)
Gvc = Gc0simple * (1 - s/wz) / (1 + s/wp1simple);

% 2. Controller Transfer Function (PI)
Gcm = 7.8;
fzv = 500;
Gv = Gcm * (1 + 2*pi*fzv/s);

% 3. Sensor/Feedback Gain
H = 0.5;

% 4. Loop Gain
T = H * Gv * Gvc;

%% Plotting

% Figure 1: Plant Bode Plot
figure(1);
bode(Gvc);
grid on;
title('Bode Plot of the Plant G_{vc}(s)');

% Figure 2: Controller Bode Plot
figure(2);
bode(Gv);
grid on;
title('Bode Plot of the Controller G_v(s)');

% Figure 3: Loop Gain, Crossover Frequency, and Phase Margin
figure(3);
margin(T); % This automatically calculates and displays Fc and PM
grid on;
title('Loop Gain T(s) = H \cdot G_v(s) \cdot G_{vc}(s)');

% Display margins in the command window for quick reference
[gm, pm, wcg, wcp] = margin(T);
fprintf('Crossover Frequency: %.2f Hz\n', wcp/(2*pi));
fprintf('Phase Margin: %.2f degrees\n', pm);