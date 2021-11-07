using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// This component acts as the main controller to run each iteration and restart after a crash or a car reaches the end
// It will also communicate the results to the NN to update and improve the learning model after a set amouint of runs have been completed

public class WorldState : MonoBehaviour
{
    public Vector3 startPosition = new Vector3(-528.3f, 0, -32.6f);
    public Quaternion startRotation = Quaternion.identity;
    private string state;
    private CarController CarController;
    private int time;
    private int scoreDistance = 0;
    private float carSpeed;
    // List all sensor directions and angles
    private float distanceInFront, distanceToLeft, distance23Left, distance45Left, distance68Left, distanceToRight, distance23Right, distance45Right, distance68Right;

    // This class will be used to construct the JSON object to send to the NN
    private class Data {
        public bool getInputs;
        public float speed;
        public float distanceInFront, distanceToLeft, distance23Left, distance45Left, distance68Left, distanceToRight, distance23Right, distance45Right, distance68Right;
    }

    WebSocket socket = new WebSocket();
    void Start() {
        CarController = GameObject.FindGameObjectWithTag("Car").GetComponent<CarController>();
        socket.Start();
        state = "Running";
    }

    // Update is called once per frame
    void Update() {
        string inputs = "{\"acceleratorInput\": 0,\"turnInput\": 0}";
        if(state == "Running"){
            // Fill in the car data
            Data data = new Data();
            data.getInputs = true;
            data.speed = carSpeed;
            data.distanceInFront = distanceInFront;

            data.distanceToLeft = distanceToLeft;
            data.distance23Left = distance23Left;
            data.distance45Left = distance45Left;
            data.distance68Left = distance68Left;

            data.distanceToRight = distanceToRight;
            data.distance23Right = distance23Right;
            data.distance45Right = distance45Right;
            data.distance68Right = distance68Right;

            string jsonDataToSend = JsonUtility.ToJson(data);
            inputs = socket.GetCarInputs(jsonDataToSend);
        }

        CarController.UpdateCar(inputs);
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
        state = "Stopped";
        Debug.Log("HIT THE TRACK");
        // Trigger the restart and get the next generated model. Wait for a response to pause the simulation until the new NN is loaded
        string nnStatus = socket.CarCrashed();
        scoreDistance = 0;
        CarController.ResetCarPosition();
        state = "Running";
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
            case "Left23":
                distance23Left = distance;
                break;
            case "Left45":
                distance45Left = distance;
                break;
            case "Left68":
                distance68Left = distance;
                break;
            case "LeftSide":
                distanceToLeft = distance;
                break;
            case "Right23":
                distance23Right = distance;
                break;
            case "Right45":
                distance45Right = distance;
                break;
            case "Right68":
                distance68Right = distance;
                break;
            case "RightSide":
                distanceToRight = distance;
                break;
            default:
                break;
        }
    }
}
