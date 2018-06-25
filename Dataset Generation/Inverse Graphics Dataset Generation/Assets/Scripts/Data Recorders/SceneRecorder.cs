using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

/// <summary>
/// Create examples/labels of the current state of the scene. 
/// Saves out the camera views as well as records any RecordObjects
/// in the scene. Saves to a json file.
/// 
/// In other words, creates "scene snapshots"
/// </summary>
public class SceneRecorder : MonoBehaviour {

    // Resolution of our images to save
    public int resolutionWidth = 32;
    public int resolutionHeight = 32;

    /// <summary>
    /// Test function to save out the current scene snapshot
    /// </summary>
    [ContextMenu("Save Current Scene Record Snapshot")]
    public void SaveCurrentSnapshot()
    {
        SaveCurrentSceneRecord("../scene_record", "../view");
    }

    /// <summary>
    /// Save the current scene snapshot to a json file
    /// </summary>
    /// <param name="fileName">JSON file to create and save to</param>
    /// <param name="imageFileName">The prefix to the pngs to output.</param>
    public void SaveCurrentSceneRecord(string fileName, string imageFileName)
    {
        string sceneRecordString = JsonUtility.ToJson(RecordSceneSnapshot(imageFileName));
        FileExtensions.SaveStringToFile(fileName + ".json", sceneRecordString);
    }

    /// <summary>
    /// Gathers all the CameraPNGSavers and RecordObjects. Saves out pngs of the CameraPNGSavers,
    /// and creates ObjectRecords of the gameobjects that we are interested in saving from the 
    /// RecordObjects in the scene. 
    /// 
    /// Returns a SceneRecord which consists of the image paths as well as all the ObjectRecords
    /// </summary>
    /// <param name="imageFileName">Filename path and prefix to save images to</param>
    /// <returns>Scene record of the image paths as well as the object records in the scene</returns>
	public SceneRecord RecordSceneSnapshot(string imageFileName="../image")
    {
        // It would be faster to cache these some way, but I don't think it'll be our bottleneck
        ViewRecorder[] viewRecorders = FindObjectsOfType<ViewRecorder>(); // There may be multiple due to stereo etc
        ObjectRecorder[] objectRecorders = FindObjectsOfType<ObjectRecorder>();

        // Instantiate the SceneRecord for this snapshot
        SceneRecord sceneRecord = new SceneRecord();

        // Save screenshots
        string[] imageFileNames = new string[viewRecorders.Length];
        for(int i = 0; i < viewRecorders.Length; i++)
        {
            imageFileNames[i] = imageFileName + "_" + i + ".png";
            viewRecorders[i].SaveCameraViewToPNG(imageFileNames[i], resolutionWidth, resolutionHeight);
        }
        sceneRecord.imageFiles = imageFileNames;

        // Generate the object records
        ObjectRecord[] objectRecords = new ObjectRecord[objectRecorders.Length];
        for(int i = 0; i < objectRecorders.Length; i++)
        {
            objectRecords[i] = objectRecorders[i].GetRecord();
        }
        sceneRecord.objectRecords = objectRecords;


        return sceneRecord;
    }
}

/// <summary>
/// A scene record is a snapshot of the scene, containing the paths
/// to the image files that were saved out, and the ObjectRecords 
/// (containing transformation matrices etc of all the objects we're
/// interested in saving).
/// </summary>
[System.Serializable]
public class SceneRecord
{
    public string[] imageFiles;
    public ObjectRecord[] objectRecords;
}
