using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class CreateExampleLabel : MonoBehaviour {

    public int resolutionWidth = 256;
    public int resolutionHeight = 256;

    [ContextMenu("Save Current Scene Record Snapshot")]
    public void SaveCurrentSnapshot()
    {
        SaveCurrentSceneRecord("../scene_record.json", "../view");
    }

    public void SaveCurrentSceneRecord(string fileName, string imageFileName)
    {
        string sceneRecordString = JsonUtility.ToJson(RecordSceneSnapshot(imageFileName));
        using (StreamWriter writer = new StreamWriter(fileName))
        {
            writer.Write(sceneRecordString);

        }
    }

	public SceneRecord RecordSceneSnapshot(string imageFileName="../image")
    {
        // It would be faster to cache these some way, but I don't think it'll be our bottleneck
        CameraPNGSaver[] pngSavers = FindObjectsOfType<CameraPNGSaver>(); // There may be multiple due to stereo etc
        RecordObject[] recordObjects = FindObjectsOfType<RecordObject>();

        // Instantiate the SceneRecord for this snapshot
        SceneRecord sceneRecord = new SceneRecord();

        // Save screenshots
        string[] imageFileNames = new string[pngSavers.Length];
        for(int i = 0; i < pngSavers.Length; i++)
        {
            imageFileNames[i] = imageFileName + "_" + i + ".png";
            pngSavers[i].SaveCameraViewToPNG(imageFileNames[i], resolutionWidth, resolutionHeight);
        }
        sceneRecord.imageFiles = imageFileNames;

        // Generate the object records
        ObjectRecord[] objectRecords = new ObjectRecord[recordObjects.Length];
        for(int i = 0; i < recordObjects.Length; i++)
        {
            objectRecords[i] = recordObjects[i].GetRecord();
        }
        sceneRecord.objectRecords = objectRecords;


        return sceneRecord;
    }
}

[System.Serializable]
public class SceneRecord
{
    public string[] imageFiles;
    public ObjectRecord[] objectRecords;
}
