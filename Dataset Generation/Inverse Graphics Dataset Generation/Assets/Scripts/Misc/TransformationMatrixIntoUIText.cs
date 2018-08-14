using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TransformationMatrixIntoUIText : MonoBehaviour {

    public Transform target;

    public void Update()
    {
        Matrix4x4 transformationMatrix = Matrix4x4.TRS(target.position, target.rotation, target.localScale); // target.worldToLocalMatrix;

        // Would be nice if this could be a for loop...
        UpdateText(0, transformationMatrix.m00);
        UpdateText(1, transformationMatrix.m01);
        UpdateText(2, transformationMatrix.m02);
        UpdateText(3, transformationMatrix.m03);

        UpdateText(4, transformationMatrix.m10);
        UpdateText(5, transformationMatrix.m11);
        UpdateText(6, transformationMatrix.m12);
        UpdateText(7, transformationMatrix.m13);

        UpdateText(8, transformationMatrix.m20);
        UpdateText(9, transformationMatrix.m21);
        UpdateText(10, transformationMatrix.m22);
        UpdateText(11, transformationMatrix.m23);

        UpdateText(12, transformationMatrix.m30);
        UpdateText(13, transformationMatrix.m31);
        UpdateText(14, transformationMatrix.m32);
        UpdateText(15, transformationMatrix.m33);
    }


    public void UpdateText(int childIndex, float value)
    {
        transform.GetChild(childIndex).GetComponent<Text>().text = value.ToString("0.00");
    }

}
