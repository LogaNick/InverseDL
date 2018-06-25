using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

/// <summary>
/// File extensions to simplify writing to files
/// 
/// A bit hacky at the moment
/// </summary>
public class FileExtensions : MonoBehaviour {

	public static void SaveStringToFile(string fileName, string fileString)
    {
        CheckAndCreateDirectories(fileName);
        using (StreamWriter writer = new StreamWriter(fileName))
        {
            writer.Write(fileString);
        }
    }

    public static void CheckAndCreateDirectories(string fileName)
    {
        string[] parts = fileName.Split('/');

        // Don't want to create a folder if we want to save a file without extension...
        if(!fileName.EndsWith("/"))
        {
            parts[parts.Length - 1] = ".";
        }

        string concatenatedPath = "";
        foreach(string part in parts)
        {
            // If there's a . in the path, then we'll consider this file name part of the path and break
            if(part.Contains("."))
            {
                break;
            }


            concatenatedPath += part + Path.DirectorySeparatorChar;

            if(!Directory.Exists(concatenatedPath))
            {
                Directory.CreateDirectory(concatenatedPath);
            }
        }
    }
}
