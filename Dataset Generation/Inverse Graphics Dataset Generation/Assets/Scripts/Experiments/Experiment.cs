using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Base class for experiments (not using an interface so we can more easily
/// view these in lists in the inspector).
/// </summary>
public class Experiment : MonoBehaviour {

    // Usually we want the experiment to go from 0 to 1 inclusively (like for translation).
    // However there's other times when we want to exclude 1 (like in rotation so we don't
    // see the first 0 degree angle and the final 360 degree angle (the same rotation) twice)
    public bool doFinalStep = true;

    /// <summary>
    /// Performs an experiment's step. Percentage is from 0 to 1.0, denotes
    /// how far along in the experiment this step is.
    /// </summary>
    /// <param name="percentage">0 is the start of the experiment, 1.0 is the end</param>
    public virtual void PerformStep(float percentage, SceneRecorder sceneRecorder) { }
}
