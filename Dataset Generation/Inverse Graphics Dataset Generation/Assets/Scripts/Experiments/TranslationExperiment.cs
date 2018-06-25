using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Experiment for performing linear translations. Linearly translates
/// the target gameobject between startPosition and endPosition during
/// its step
/// </summary>
public class TranslationExperiment : Experiment {

    public GameObject startPosition;
    public GameObject endPosition;

    public GameObject target;


    public override void PerformStep(float percentage, SceneRecorder sceneRecorder)
    {
        base.PerformStep(percentage, sceneRecorder);

        target.transform.position = Vector3.Lerp(startPosition.transform.position,
            endPosition.transform.position, percentage);
    }

}
