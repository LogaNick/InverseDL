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

            experimentRunner.fileName = saveTo + "/" +go.name + "/";

            experimentRunner.RunExperiments();
        }
    }
}
