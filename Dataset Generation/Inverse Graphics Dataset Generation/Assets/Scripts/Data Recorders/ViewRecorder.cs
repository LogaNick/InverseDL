using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Saves the current view of the camera attached to this gameobject to PNG.
/// 
/// Based off https://forum.unity.com/threads/how-to-save-manually-save-a-png-of-a-camera-view.506269/
/// and https://answers.unity.com/questions/22954/how-to-save-a-picture-take-screenshot-from-a-camer.html
/// </summary>
public class ViewRecorder : MonoBehaviour {

    protected Camera cam;

    [ContextMenu("Save test screenshot")]
    public void SaveTestScreenShot()
    {
        SaveCameraViewToPNG("../test.png", 256, 256);
    }

	public bool SaveCameraViewToPNG(string filename, int width, int height, int bits=24)
    {
        // Cache the attached camera if we haven't already done so
        if(!cam)
        {
            cam = GetComponent<Camera>();
        }

        // Set up the render textures
        RenderTexture tempCameraRenderTexture = new RenderTexture(width, height, bits);
        RenderTexture currentRenderTexture = RenderTexture.active; // We'll have to swap this back later
        cam.targetTexture = tempCameraRenderTexture;
        RenderTexture.active = cam.targetTexture;

        // Render the camera
        cam.Render();

        // Create the texture, copy the camera's render texture's pixels, reset the active render texture
        Texture2D copiedTexture = new Texture2D(width, height, TextureFormat.RGB24, false);
        copiedTexture.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        cam.targetTexture = null;
        RenderTexture.active = currentRenderTexture;
        Destroy(tempCameraRenderTexture);

        // Save the file
        byte[] bytes = copiedTexture.EncodeToPNG();
        System.IO.File.WriteAllBytes(filename, bytes);
        

        return true;
    }
}
