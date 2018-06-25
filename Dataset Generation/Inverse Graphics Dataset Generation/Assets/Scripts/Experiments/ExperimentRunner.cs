using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Runs a list of experiments
/// 
/// Inherits from Experiment, so we can run nested experiments
/// </summary>
public class ExperimentRunner : Experiment {

    public delegate void ExperimentCallback(int step, string fileName, string imageFileName);

    // The experiments to run
    public List<Experiment> experiments;

    // These experiments are run one step at a time without recording, and at
    // at each step all experiments are run (with recording)
    public List<Experiment> preRunExperiments;

    // Number of steps in an experiment
    public int steps = 10;

    // When using the context menu, we'll save the experiment to this filename
    [SerializeField]
    protected string fileName = "data_generation/experiment_0/datum";

    [SerializeField]
    protected bool recordSceneDuringMyExperiments = true;

    [ContextMenu("Run Experiments")]
    public void RunExperiments()
    {
        SceneRecorder sceneRecorder = FindObjectOfType<SceneRecorder>();

        RunExperiments(sceneRecorder, fileName, recordSceneDuringMyExperiments);
    }

    public void RunExperiments(SceneRecorder sceneRecorder, string baseFileName, bool recordScene)
    {
        RunExperiments(experiments, sceneRecorder, baseFileName, baseFileName + "_img", steps, recordScene);
    }

    public static void RunExperiments(List<Experiment> experiments, SceneRecorder sceneRecorder, string baseFileName,
        string baseImageFileName, int steps, bool recordScene, ExperimentCallback callback = null)
    {
        int currentStep = 0;
        while(currentStep <= steps)
        {
            string currentFileName = baseFileName + "_" + currentStep;
            string currentImageFileName = baseImageFileName + "_" + currentStep;
            float percent = currentStep / (float)steps;
            foreach (Experiment experiment in experiments)
            {
                experiment.PerformStep(percent, sceneRecorder);
            }

            // Sometimes we don't want to record after an experiment (for example, if an experiment
            // is nested and the parent is simply setting up the children experiments).
            if (recordScene)
            {
                Debug.Log("Saving " + currentFileName);
                sceneRecorder.SaveCurrentSceneRecord(currentFileName, currentImageFileName);
            }

            if(callback != null)
            {
                callback(currentStep, currentFileName, currentImageFileName);
            }

            currentStep++;
        }
    }

    public override void PerformStep(float percentage, SceneRecorder sceneRecorder)
    {
        base.PerformStep(percentage, sceneRecorder);

        RunExperiments(preRunExperiments, sceneRecorder, fileName, fileName + "_img", steps, false,
            delegate (int step, string experimentFileName, string experimentImageFileName)
            {
                RunExperiments(experiments, sceneRecorder, experimentFileName, experimentImageFileName + "_" + step, steps, true);
            });
    }
}
