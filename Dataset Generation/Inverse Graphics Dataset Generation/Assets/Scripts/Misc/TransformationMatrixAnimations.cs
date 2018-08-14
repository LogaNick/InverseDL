using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TransformationMatrixAnimations : MonoBehaviour {

	
	// Update is called once per frame
	void Update () {
		if(Input.GetKeyDown(KeyCode.Space))
        {
            StartCoroutine(RunAnimations());
        }
	}

    IEnumerator RunAnimations()
    {
        // Hard coding these for speed
        float endTranslation = -1f;
        float duration = 1f;
        Vector3 startPos = transform.position;
        yield return StartCoroutine(TranslationAnimation(Vector3.right * endTranslation, duration));
        // Go To the other end

        yield return StartCoroutine(TranslationAnimation(-Vector3.right * endTranslation, 2f * duration));

        yield return StartCoroutine(TranslationAnimation(Vector3.zero, duration));

        // Up/down
        yield return StartCoroutine(TranslationAnimation(-Vector3.up * endTranslation, duration));
        // Go To the other end

        yield return StartCoroutine(TranslationAnimation(Vector3.up * endTranslation, 2f * duration));

        yield return StartCoroutine(TranslationAnimation(Vector3.zero, duration));


        // Rotation
        // Up/down
        endTranslation = -.5f;
        yield return StartCoroutine(EulerAnglesAnimation(-Vector3.forward * endTranslation, duration));
        // Go To the other end

        yield return StartCoroutine(EulerAnglesAnimation(Vector3.forward * endTranslation, 2f * duration));

        yield return StartCoroutine(EulerAnglesAnimation(Vector3.zero, duration));

        // Scaling
        // X scaling
        endTranslation = 0.5f;
        yield return StartCoroutine(ScaleAnimation(Vector3.one - Vector3.right * endTranslation, duration));
        // Go To the other end

        endTranslation = 1;
        yield return StartCoroutine(ScaleAnimation(Vector3.one + Vector3.right * endTranslation, 2f * duration));

        yield return StartCoroutine(ScaleAnimation(Vector3.one, duration));

        // Scaling
        // Y scaling
        endTranslation = 0.75f;
        yield return StartCoroutine(ScaleAnimation(Vector3.one - Vector3.up * endTranslation, duration));
        // Go To the other end
        endTranslation = 1f;
        yield return StartCoroutine(ScaleAnimation(Vector3.one + Vector3.up * endTranslation, 2f * duration));

        yield return StartCoroutine(ScaleAnimation(Vector3.one, duration));

        yield return StartCoroutine(ScaleAnimation(Vector3.zero, duration));

        yield break;
    }


    IEnumerator TranslationAnimation(Vector3 end, float duration)
    {
        Vector3 start = transform.position;

        float t = 0f;

        while(t < duration)
        {
            t += Time.deltaTime;
            transform.position = Vector3.Lerp(start, end, t / duration);
            yield return null;
        }

        transform.position = end;

        yield return null;
    }

    IEnumerator EulerAnglesAnimation(Vector3 end, float duration)
    {
        // Yes, I should have made this a single function that takes a callback, but here we are copying code
        Quaternion start = transform.rotation;
        Quaternion endRotation = Quaternion.EulerRotation(end);

        float t = 0f;

        while (t < duration)
        {
            t += Time.deltaTime;
            transform.rotation = Quaternion.Slerp(start, endRotation, t / duration);
            yield return null;
        }

        transform.rotation = endRotation;

        yield return null;
    }

    IEnumerator ScaleAnimation(Vector3 end, float duration)
    {
        // Yes, I should have made this a single function that takes a callback, but here we are copying code
        Vector3 start = transform.localScale;

        float t = 0f;

        while (t < duration)
        {
            t += Time.deltaTime;
            transform.localScale = Vector3.Lerp(start, end, t / duration);
            yield return null;
        }

        transform.localScale = end;

        yield return null;
    }
}
