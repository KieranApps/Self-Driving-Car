using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// This component acts as the main controller to run each iteration and restart after a crash or a car reaches the end
// It will also communicate the results to the NN to update and improve the learning model after a set amouint of runs have been completed

public class WorldState : MonoBehaviour
{
    private int time;
    private int scoreDistance = 0;
    private float carSpeed;
    // List all sensor directions and angles
    private float distanceInFront, distanceToLeft, distanceToRight, distanceDiagonalLeft, distanceDiagonalRight;

    WebSocket socket;
    void Start() {
        socket = new WebSocket();
        socket.Start();    
    }

    // Update is called once per frame
    void Update() {
        
    }

    public void IncreaseScoreDistance() {
        scoreDistance++;
        Debug.Log(scoreDistance);
    }

    public void UpdateCarSpeed(float s) {
        float carSpeed = s;
    }

    // These two ends might just be the same thing in the end
    public void EndWithCrash() {
        Debug.Log("HIT THE TRACK");
        // Trigger the restart and get the next generated model
    }

    public void EndWithFinshLine() {
        // Get the car object and set speed to 0 (instant stop)

    }

    public void UpdateDistances(string tag, float distance) {
        switch (tag)
        {
            case "FrontSensor":
                distanceInFront = distance;
                break;
            default:
                break;
        }
    }
}
