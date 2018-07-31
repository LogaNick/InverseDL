using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Runs the three experiments.
/// 
/// There were too many bugs in the original Experiment runner with the callbacks to create this kind
/// of for-loop in the inspector. If this was to be continued, this class should become RunNExperiments,
/// and the original ExperimentRunner experiments should be moved over to this
/// </summary>
public class TripleExperimentRunner : ExperimentRunner {

    // The experiments to run. For a refactor, make this a struct or class with steps
    public List<Experiment> firstExperiments;
    public List<Experiment> secondExperiments;
    public List<Experiment> thirdExperiments;

    // How many steps to run for each set of experiments
    public int firstExperimentSteps = 32;
    public int secondExperimentSteps = 32;
    public int thirdExperimentSteps = 8;

    public override void RunExperiments(SceneRecorder sceneRecorder, string baseFileName, bool recordScene)
    {
        // Giant for loop for each experiment type
        for(int i = 0; i <= firstExperimentSteps; i++)
        {
            string currentFileName = baseFileName + "_" + i;
            string currentImageFileName = currentFileName + "_img";

            RunExperimentStep(firstExperiments, sceneRecorder, currentImageFileName, currentImageFileName, firstExperimentSteps, false, null, i);

            for(int j = 0; j <= secondExperimentSteps; j++)
            {
                currentFileName = baseFileName + "_" + i + "_" + j;
                currentImageFileName = currentFileName + "_img";

                RunExperimentStep(secondExperiments, sceneRecorder, currentFileName, currentImageFileName, secondExperimentSteps, false, null, j);

                for (int k = 0; k <= thirdExperimentSteps; k++)
                {
                    currentFileName = baseFileName + "_" + i + "_" + j + "_" + k;
                    currentImageFileName = currentFileName + "_img";

                    RunExperimentStep(thirdExperiments, sceneRecorder, currentFileName, currentImageFileName, thirdExperimentSteps, recordScene, null, k);
                }
            }
        }
    }
}
