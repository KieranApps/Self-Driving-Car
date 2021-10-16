using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// This goes on every sensor placed on the car to shoot a ray and get the distance to the wall of the track

public class SensorRay : MonoBehaviour
{
    // Sensors are public so they can be assigned within unity
    // This saves gaving to create a custom script for each sensor just to then pick that sensor via a tag
    public GameObject Sensor;
    private WorldState WorldState;

    private void Start() {
        WorldState = GameObject.Find("WorldState").GetComponent<WorldState>();
    }

    private void FixedUpdate() {
        Ray ray = new Ray(transform.position, transform.forward);
        Debug.DrawRay(transform.position, transform.forward, Color.black);
        // Use RaycastAll in order to get the rays that go through each distance gate and hit the track
        RaycastHit[] hits = Physics.RaycastAll(ray);
        // Find the ray that hit the track from all rays
        for(int i = 0; i < hits.Length; i++){
            if(hits[i].collider.tag == "Track"){
                // Send the distance to the Wolrd controller to the have that send it to the NN to get the appropriate input back
                WorldState.UpdateDistances(Sensor.tag, hits[i].distance);
            }
        }
    }
}
