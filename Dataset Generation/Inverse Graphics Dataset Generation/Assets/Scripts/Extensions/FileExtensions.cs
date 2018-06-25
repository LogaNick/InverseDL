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

    /// <summary>
    /// Removes the common path in path1 from path2
    /// </summary>
    /// <param name="path1"></param>
    /// <param name="path2"></param>
    /// <returns></returns>
    public static string RemoveCommonPath(string path1, string path2)
    {
        string[] partsPath1 = path1.Split('/');
        string[] partsPath2 = path2.Split('/');

        int j = 0;
        for (int i = 0; i < partsPath1.Length && i < partsPath2.Length; i++)
        {
            if (partsPath1[i] == partsPath2[i])
            {
                j++;
            }
            else
            {
                break;
            }
        }

        // Reformulate the rest of the path2
        string remainingPath = "";
        for (; j < partsPath2.Length; j++)
        {
            remainingPath += partsPath2[j] + Path.DirectorySeparatorChar;
        }

        // May not actually want that extra / at the end
        if (!path2.EndsWith("/"))
        {
            remainingPath = remainingPath.Remove(remainingPath.Length - 1);
        }

        return remainingPath;
    }
}
