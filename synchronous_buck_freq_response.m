%% Introduction to Modeling, Control and Simulations - Assignment
% This script analyzes the frequency response of a synchronous buck converter,
% including its plant transfer function, compensator, and output impedance.
% University of Colorado Boulder
close all;

%% Define Buck Converter Component Values
% Parameters are based on the LTspice model SyncBuck_switching_CL.asc
L = 1e-6;       % Inductor
Rs = 30e-3;     % Series resistance (Inductor DCR + MOSFET Rds_on)
C = 200e-6;     % Output filter capacitor
Resr = 0.8e-3;  % Capacitor Equivalent Series Resistance (ESR)
Vg = 5;         % Input voltage
R = 1;          % Load resistance (Updated from 1e3 to reflect a more typical load)
VM = 1;         % PWM modulator sawtooth amplitude
Vref = 1.8;     % Reference voltage
H = 1;          % Output voltage sensing gain

%% Calculate Key Features of the Plant Transfer Function Gvd(s)
% Gvd(s) is the duty-cycle-to-output-voltage transfer function.
wesr = 1/(C*Resr);      % Frequency of the zero caused by capacitor ESR
wo = 1/sqrt(C*L);       % Resonant frequency of the L-C output filter
Qload = R/sqrt(L/C);    % Q-factor component due to the load
Qloss = sqrt(L/C)/(Resr+Rs); % Q-factor component due to losses
Q = Qload*Qloss/(Qload+Qloss); % Total Q-factor of the complex poles

%% Define Plant and Compensator Transfer Functions
s = tf('s'); % Define the Laplace variable 's'

% Plant: Duty-cycle-to-output transfer function
Gvd = Vg*(1+s/wesr)/(1+(1/Q)*(s/wo)+(s/wo)^2);

% Compensator (Type II) component values
R1 = 3e3;
R2 = 16e3;
R4 = 360;
C4 = 1.5e-9;
C2 = 1.3e-9;

% Compensator pole and zero frequencies
wL = 1/(C2*R2);   % Low-frequency pole (integrator)
wz = 1/(C4*(R4+R1)); % Zero for phase boost
wp1 = 1/(C4*R4);  % High-frequency pole for noise attenuation

% Compensator transfer function Gc(s)
Gc = R1/R2*(1+wL/s)*(1+s/wz)/(1+s/wp1);

%% Plot Bode Response of the Compensator Gc(s)
fmin=10;    % Min frequency (Hz)
fmax=10e6;  % Max frequency (Hz)
BodeOptions = bodeoptions;
BodeOptions.FreqUnits = 'Hz';
BodeOptions.Title.String = 'PID Compensator Gc(s) Frequency Response';

figure(1);
bode(Gc, BodeOptions, 'b'); % Plot the Bode diagram
grid on;
set(findobj(gcf,'type','line'),'LineWidth',2); % Make line thicker

%% Calculate Compensator Gain and Phase at a Specific Frequency
fx = 100000; % Frequency of interest in Hz
magnitude_in_dB = 20*log10(abs(freqresp(Gc,fx,'Hz')));
phase_in_degrees = angle(freqresp(Gc,fx,'Hz'))*180/pi;
fprintf('Magnitude of Gc at %1.0f kHz is %1.2f dB\n', fx/1e3, magnitude_in_dB);
fprintf('Phase of Gc at %1.0f kHz is %1.2f degrees\n', fx/1e3, phase_in_degrees);

%% Define Loop Gain and Output Impedance
T = Gc * (1/VM) * Gvd * H; % Total loop gain T(s)

% Open-loop output impedance
Zout = (s*L+Rs)*Gvd/Vg;

% Closed-loop output impedance
Zo = Zout/(1+T);

%% Find the Maximum Value of Closed-Loop Output Impedance ||Zo||
frequencies = logspace(1,6,1000); % Define frequency range for analysis
Zo_values = squeeze(freqresp(Zo,frequencies,'Hz')); % Calculate Zo over frequency range
Zo_mag = abs(Zo_values); % Get magnitude in Ohms

% Find the maximum magnitude and the frequency at which it occurs
[Zo_mag_max, findex] = max(Zo_mag);
fz_max = frequencies(findex);
fprintf('||Zo||max = %1.2f mOhm occurs at %1.1f kHz\n\n', ...
  1000*Zo_mag_max, fz_max/1e3); % Display result in mOhms and kHz

%% Plot Open-Loop vs. Closed-Loop Output Impedance
BodeOptions2 = bodeoptions;
BodeOptions2.FreqUnits = 'Hz';
BodeOptions2.Title.String = 'Open-Loop Zout vs Closed-Loop Zo';
BodeOptions2.Grid = 'on';

figure(2);
bode(Zout, Zo, {fmin, fmax}, BodeOptions2); % Plot both impedances
legend('|Z_{out}| open-loop', '|Z_o| closed-loop', 'Location', 'best');
set(findobj(gcf,'type','line'),'LineWidth',2);
