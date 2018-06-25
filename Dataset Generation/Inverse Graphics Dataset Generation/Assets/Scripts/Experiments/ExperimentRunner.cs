using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Runs a list of experiments
/// 
/// Inherits from Experiment, so we can run nested experiments
/// </summary>
public class ExperimentRunner : Experiment {

    // The experiments to run
    public List<Experiment> experiments;

    // Number of steps in an experiment
    public int steps = 10;

    // When using the context menu, we'll save the experiment to this filename
    [SerializeField]
    protected string fileName = "data_generation/experiment_0/datum";

    [ContextMenu("Run Experiments")]
    public void RunExperiments()
    {
        SceneRecorder sceneRecorder = FindObjectOfType<SceneRecorder>();

        RunExperiments(sceneRecorder, fileName, true);
    }

    public void RunExperiments(SceneRecorder sceneRecorder, string baseFileName, bool recordScene)
    {
        RunExperiments(experiments, sceneRecorder, baseFileName, steps, recordScene);
    }

    public static void RunExperiments(List<Experiment> experiments, SceneRecorder sceneRecorder, string baseFileName, int steps,
        bool recordScene)
    {
        int currentStep = 0;
        while(currentStep <= steps)
        {
            string currentFileName = baseFileName + "_" + currentStep;
            string currentImageFileName = baseFileName + "_img_" + currentStep;
            float percent = currentStep / (float)steps;
            foreach (Experiment experiment in experiments)
            {
                experiment.PerformStep(percent, sceneRecorder);
            }

            // Sometimes we don't want to record after an experiment (for example, if an experiment
            // is nested and the parent is simply setting up the children experiments).
            if (recordScene)
            {
                sceneRecorder.SaveCurrentSceneRecord(currentFileName, currentImageFileName);
            }

            currentStep++;
        }
    }
}
