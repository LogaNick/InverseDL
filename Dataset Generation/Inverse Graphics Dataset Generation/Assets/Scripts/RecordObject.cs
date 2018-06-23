using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Component for recording the label data about given objects (transformation matrices).
/// 
/// Put this on any object you want labels for.
/// </summary>
public class RecordObject : MonoBehaviour {

    // Mostly for testing, recording this transform's data and reverting to it later
    public ObjectRecord cachedRecord;

    /// <summary>
    /// Save the current ObjectRecord to cachedRecord
    /// </summary>
    [ContextMenu("Cache Current Transformation")]
    public void CacheCurrentTransformation()
    {
        cachedRecord = GetRecord();
    }

    /// <summary>
    /// Apply the transformation matrix in the cachedRecord to this transform
    /// </summary>
    [ContextMenu("Revert transformation to cached transformation")]
    public void RevertToCachedTransformation()
    {
        ApplyObjectRecord(cachedRecord);
    }

    /// <summary>
    /// Apply an objectRecord's transformationMatrix to this transform.
    /// </summary>
    /// <param name="objectRecord"></param>
    public void ApplyObjectRecord(ObjectRecord objectRecord)
    {
        transform.localScale = objectRecord.transformationMatrix.lossyScale;
        transform.rotation = objectRecord.transformationMatrix.rotation;
        transform.position = objectRecord.transformationMatrix.GetColumn(3); // Why doesn't Unity have this built in the Matrix4x4 class??

        name = objectRecord.name;
    }

    /// <summary>
    /// Create and return the current ObjectRecord that represents this transform's
    /// current transformation matrix.
    /// </summary>
    /// <returns>The current object record</returns>
	public ObjectRecord GetRecord()
    {
        ObjectRecord objectRecord = new ObjectRecord();

        objectRecord.name = name;
        objectRecord.translation = transform.position;
        objectRecord.eulerAngles = transform.eulerAngles;
        objectRecord.quaternion = transform.rotation;
        objectRecord.scale = transform.lossyScale; // Not accurate if we start doing parenting

        objectRecord.translationMatrix = Matrix4x4.Translate(objectRecord.translation);
        objectRecord.rotationMatrix = Matrix4x4.Rotate(objectRecord.quaternion);
        objectRecord.scaleMatrix = Matrix4x4.Scale(objectRecord.scale);
        objectRecord.transformationMatrix = Matrix4x4.TRS(objectRecord.translation, objectRecord.quaternion, objectRecord.scale);

        /* Test debug log
        Debug.Log("TRS: \n" + objectRecord.transformationMatrix + "\nMultiplied: \n" +
            (objectRecord.translationMatrix * objectRecord.rotationMatrix * objectRecord.scaleMatrix) + "\nWorld: \n" +
            transform.worldToLocalMatrix);
        */

        return objectRecord;
    }
}

/// <summary>
/// An object record stores all the data needed to be saved as a label
/// for this object.
/// </summary>
[System.Serializable]
public class ObjectRecord
{
    public string name;
    // Simplified
    public Vector3 translation;
    public Vector3 eulerAngles;
    public Quaternion quaternion;
    public Vector3 scale;

    // Matrix notation
    public Matrix4x4 translationMatrix;
    public Matrix4x4 rotationMatrix;
    public Matrix4x4 scaleMatrix;
    public Matrix4x4 transformationMatrix;
}
