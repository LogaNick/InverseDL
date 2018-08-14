using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Runs an experiment runner with a different game object multiple times
/// </summary>
public class SwitchGameObjectsRunExperiment : MonoBehaviour {

    public List<GameObject> gameObjects;

    public string saveTo = "data_generation/experiment_7/";
    public ExperimentRunner experimentRunner;



	[ContextMenu("Run Experiment Runnder")]
    public void RunExperiment()
    {
        foreach(GameObject go in gameObjects)
        {
            foreach(GameObject subGo in gameObjects)
            {
                subGo.SetActive(false);
            }

            go.SetActive(true);

            // Set the name of the parent object so we can get different classes
            if(go.transform.parent)
            {
                go.transform.parent.name = go.name;
            }

            SetExperimentsFileNameRecursively(experimentRunner,  saveTo + "/" +go.name + "/");

            experimentRunner.RunExperiments();
        }
    }

    /// <summary>
    /// Sets all experiment runners in the given experiment runner contains to the given filename.
    /// Recursive
    /// </summary>
    /// <param name="experimentRunner"></param>
    /// <param name="fileName"></param>
    public void SetExperimentsFileNameRecursively(ExperimentRunner experimentRunner, string fileName)
    {
        foreach(Experiment experiment in experimentRunner.experiments)
        {  
            ExperimentRunner containedExperimentRunner = experiment as ExperimentRunner;
            if (containedExperimentRunner != null)
            {
                SetExperimentsFileNameRecursively(containedExperimentRunner, fileName);
            }
        }

        experimentRunner.fileName = fileName;
    }
}
