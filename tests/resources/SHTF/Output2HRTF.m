% Collect the data simulated by NumCalc and save to project folder.
close all; clear

Mesh2HRTF_version = '1.0.0';

% source information
sourceType = 'Both ears';
numSources = 2;
sourceCenter(1,1:3) = [-0.002530 0.087218 0.000632];
sourceArea(1,1) = 3.26585e-05;
sourceCenter(2,1:3) = [0.004010 -0.087165 -0.000470];
sourceArea(2,1) = 3.68826e-05;

% Reference to a point source in the origin
% accoring to the classical HRTF definition
% (https://doi.org/10.1016/0003-682X(92)90046-U)
reference = true;

% Compute HRIRs via the inverse Fourier transfrom.
% This will add data at 0 Hz, mirror the single sided spectrum, and
% shift the HRIRs in time. Requires reference = true.
computeHRIRs = true;

% Constants
speedOfSound = 343; % [m/s]
densityOfAir = 1.1839; % [kg/m^3]

% Collect the data simulated by NumCalc
Output2HRTF_Main(Mesh2HRTF_version, ...
                 sourceType, numSources, sourceCenter, sourceArea, ...
                 reference, computeHRIRs, ...
                 speedOfSound, densityOfAir);
