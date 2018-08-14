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

    // If this is set above 0 (and below 3), will ignore lerping on a given axis
    // 0 is x, 1 is y, 2 is z
    public int ignoreAxis = -1;


    public override void PerformStep(float percentage, SceneRecorder sceneRecorder)
    {
        base.PerformStep(percentage, sceneRecorder);

        Vector3 originalPos = target.transform.position;

        float originalIgnoreAxisValue = 0f;

        if (UseIgnoreAxis())
        {
            originalIgnoreAxisValue = target.transform.position[ignoreAxis];
        }

        Vector3 newPosition = Vector3.Lerp(startPosition.transform.position,
            endPosition.transform.position, percentage);

        if(UseIgnoreAxis())
        {
            newPosition[ignoreAxis] = originalIgnoreAxisValue;
        }

        target.transform.position = newPosition;
    }

    /// <summary>
    /// Returns if the ignore axis is above -1 or below 3
    /// </summary>
    /// <returns></returns>
    private bool UseIgnoreAxis()
    {
        return ignoreAxis >= 0 && ignoreAxis < 3;
    }
}
