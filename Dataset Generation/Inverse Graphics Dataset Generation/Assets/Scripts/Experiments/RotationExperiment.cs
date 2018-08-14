using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Experiment for performing linear translations. Linearly translates
/// the target gameobject between startPosition and endPosition during
/// its step
/// </summary>
public class RotationExperiment : Experiment {

    public Vector3 axis = Vector3.up;
    public float startAngle = -180f;
    public float endAngle = 180f;

    public Transform target;

    public override void PerformStep(float percentage, SceneRecorder sceneRecorder)
    {
        base.PerformStep(percentage, sceneRecorder);

        target.rotation = Quaternion.Euler(axis * (startAngle + percentage * (endAngle - startAngle)));
    }

}
