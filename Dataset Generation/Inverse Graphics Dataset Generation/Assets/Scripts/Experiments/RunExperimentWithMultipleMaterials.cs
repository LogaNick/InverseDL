using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Runs an experiment runner with a different material multiple times
/// </summary>
public class RunExperimentWithMultipleMaterials : MonoBehaviour {

    public List<Material> materials;

    public string saveTo = "data_generation/experiment_3/datum";
    public ExperimentRunner experimentRunner;

    public Renderer rendererToChange;



	[ContextMenu("Run Experiment Runnder")]
    public void RunExperiment()
    {
        int index = 0;
        foreach(Material mat in materials)
        {
            rendererToChange.material = mat;

            experimentRunner.fileName = saveTo + "_" + index;

            experimentRunner.RunExperiments();

            index++;
        }
    }
}
