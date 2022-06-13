function finalizeHRTFsimulation(varargin)
%  FINALIZEHRTFSIMULATION(varargin)
%  merge SOFA data from two separate Mesh2HRTF simulations for left & right ear.
%  For usage details, please check the documentation!
%
% A - no inputs = scan start folder for 2 projects to merge.
% B - 1 input  = scan given folder for 2 projects to merge.
% C - 2 inputs = Merge 2 projects that were given as input.
%
% mode A - no inputs = (recommended usage mode) scans start folder for 2 projects to merge,
%                       + usually executes "Output2HRTF.py" to run full pre-processing in one go.
%   1- run this .py file from a dedicated folder (for example use folder "Finalize_HRTF_simulation")
%   2- Move into the "Finalize_HRTF_simulation" folder exactly the 2 project folders that need to be merged.
%   3- "open/run" this "finalize_hrtf_simulation.py" with Python.
%   4- Merged SOFA files will be saved in a folder next to the project that was found.   DONE.
%
% mode B - Input1 only = scan Input1 folder for 2 projects to merge.
%   1- Move into any folder exactly the 2 project folders that need to be merged.
%   2- "run" this "finalize_HRTF_simulation.py" file & specify "input_1" folder that contains projects to merge.
%       This script searches and merges the SOFA files from the 2 projects it finds inside "input_1" path.
%   3- Merged SOFA files will be saved in a folder next to the project that was found.   DONE.
%
% mode C - 2 inputs = Merge the 2 projects that were given as input_1 and input_2.
%
% migrated from Python API from Sergejs Dombrovskis
% author(s): Katharina Pollack, June 2022

jj = 1;

% check input and input mode
switch numel(varargin)
    case 0 % mode 'no inputs' = scan working directory for 2 projects to merge.
        start_folder = dir;
        for ii = 3:numel(start_folder)
            % check for folder name
            [~, ~, fext] = fileparts(start_folder(ii).name);
            if isempty(fext)
                % save folder name to variable
                folder_names{jj} = fname;
                jj = jj+1;
            end
        end
        if numel(folder_names) ~= 2
            error('More than two folders were found, only two expected. Program aborted.');
        end
    case 1 % mode '1 input'   = scan given folder for 2 projects to merge.
        if ~ischar(varargin{1})
            error('Allowed input parameter is string.');
        elseif ~isfolder(varargin{1})
            error('Input parameter has to be valid folder name.');
        end
        start_folder = varargin{1};
        
        % pretty sure this can be solved in a more elegant way (than
        % copypasting the code from above ...)
        for ii = 3:numel(start_folder)
            % check for folder name
            [~, ~, fext] = fileparts(start_folder(ii).name);
            if isempty(fext)
                % save folder name to variable
                folder_names{jj} = fname;
                jj = jj+1;
            end
        end
        if numel(folder_names) ~= 2
            error('More than two folders were found, only two expected. Program aborted.');
        end
    case 2 % mode '2 inputs'  = Merge 2 projects that were given as input.
        if ~ischar(varargin{1}) || ~ischar(varargin{2})
            error('Allowed input parameter is string.');
        elseif ~isfolder(varargin{1}) || ~isfolder(varargin{2})
            error('Both input parameters have to be valid folder names.');
        end
        folder_names{1} = varargin{1};
        folder_names{2} = varargin{2};
    otherwise
        error(['Wrong number of inputs given. Valid number of input arguments are:\n', ...
            '%s\n%s\n%s'], ...
            'A - no inputs = scan start folder for 2 projects to merge.', ...
            'B - 1 input  = scan given folder for 2 projects to merge.', ...
            'C - 2 inputs = Merge 2 projects that were given as input.');
end

% def merge_write_sofa(sofa_left, sofa_right, basepath, filename, sofa_type='HRTF'):
% Write complex pressure or impulse responses as SOFA file.
%   adapted from "write_to_sofa()" in "Output2HRTF_Main.py"


% def scan_for_errors(project_path):  # find any broken data in this project
%     NOTE: made only to work with 1 source!!!

% def plot_hrir_pair(sofa_data_path, noise_floor=-70):
%     Plots both left and right ear HRIRs in an easy to diagnose format
% 
%     based on tutorial: https://sofar.readthedocs.io/en/latest/working_with_sofa_files.html#working-with-sofa
% 
%     Params:
%     sofa_data_path : full path to the sofa HRIR file to load and plot
% 
%     noise_floor : were to limit colormap to provide easy to read image
%         = -50  # noise floor value used in "SOFAplotHRTF.m" from SOFA Matlab API
%         = -70  # value that visually matches the look of "SOFAplotHRTF.m" from SOFA MatlabAPI



end
% EOF