using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// This controller controls the behaviour of the Car, such as turning and acceleration
// It will need to be accessible by the WorldState as that will control the inputs to the Car

public class CarController : MonoBehaviour
{
    private float turnInput;
    private float acceleratorInput;
    private float steeringAngle;

    private WorldState WorldState;

    private const float MAX_STEER_ANGLE = 45;
    private const float ENGINE_POWER = 1500;
    private const float FRONT_BRAKE_POWER = 1000;
    private const float REAR_BRAKE_POWER = 750;
    
    private Rigidbody Car;
    private WheelCollider frontRight, frontLeft, rearRight, rearLeft;
    private Transform frontRightTrans, frontLeftTrans, rearRightTrans, rearLeftTrans;

    private MeshRenderer BrakeLights;

    private class Inputs {
        public float acceleratorInput;
        public float turnInput;
    }

    private void Start() {
        WorldState = GameObject.Find("WorldState").GetComponent<WorldState>();
        Car = GameObject.FindGameObjectWithTag("Car").GetComponent<Rigidbody>();
        BrakeLights = GameObject.FindGameObjectWithTag("BrakeLights").GetComponent<MeshRenderer>();
        
        frontLeft = GameObject.FindGameObjectWithTag("FrontLeft").GetComponent<WheelCollider>();
        frontRight = GameObject.FindGameObjectWithTag("FrontRight").GetComponent<WheelCollider>();
        rearLeft = GameObject.FindGameObjectWithTag("RearLeft").GetComponent<WheelCollider>();
        rearRight = GameObject.FindGameObjectWithTag("RearRight").GetComponent<WheelCollider>();

        frontLeftTrans = GameObject.FindGameObjectWithTag("FrontLeftTrans").GetComponent<Transform>();
        frontRightTrans = GameObject.FindGameObjectWithTag("FrontRightTrans").GetComponent<Transform>();
        rearLeftTrans = GameObject.FindGameObjectWithTag("RearLeftTrans").GetComponent<Transform>();
        rearRightTrans = GameObject.FindGameObjectWithTag("RearRightTrans").GetComponent<Transform>();
        
        Vector3 mass = new Vector3(0, 0.2f, -0.2f);
        Car.centerOfMass = mass;
    }

    public void UpdateCar(string inputs) {
        if(WorldState.time > 20 && ((Car.position == WorldState.startPosition || WorldState.carSpeed < 0.01))){
            WorldState.EndWithCrash();
        }
        Inputs InputsObj = new Inputs();
        float carSpeed = Car.velocity.magnitude;    
        // GetInput();
        try {
            InputsObj = JsonUtility.FromJson<Inputs>(inputs);
            turnInput = InputsObj.turnInput;
            acceleratorInput = InputsObj.acceleratorInput;
        } catch (System.Exception) {
            turnInput = 0;
            acceleratorInput = 0;
        }
        Turn();
        Accelerate();
        UpdateWheelPositions();

        WorldState.UpdateCarSpeed(carSpeed);
    }

    public void GetInput() {
        turnInput = Input.GetAxis("Horizontal");
        acceleratorInput = Input.GetAxis("Vertical");
    }

    private void Turn() {
        steeringAngle = MAX_STEER_ANGLE * turnInput;
        frontLeft.steerAngle = steeringAngle;
        frontRight.steerAngle = steeringAngle;
    }

    private void Accelerate() {
        if(acceleratorInput >= 0){
            BrakeLights.enabled = false;
            
            // Power the car
            rearRight.motorTorque = acceleratorInput * ENGINE_POWER;
            rearLeft.motorTorque = acceleratorInput * ENGINE_POWER;
            
            // Remove any braking force
            frontLeft.brakeTorque = 0;
            frontRight.brakeTorque = 0;
            rearLeft.brakeTorque = 0;
            rearRight.brakeTorque = 0;
        }else if(acceleratorInput < 0){
            // Stop engine driving car
            rearRight.motorTorque = 0;
            rearLeft.motorTorque = 0;

            // Introduce braking force (Front brakes are stronger than rears)
            frontLeft.brakeTorque = - acceleratorInput * FRONT_BRAKE_POWER;
            frontRight.brakeTorque = - acceleratorInput * FRONT_BRAKE_POWER;
            rearLeft.brakeTorque = - acceleratorInput * REAR_BRAKE_POWER;
            rearRight.brakeTorque = - acceleratorInput * REAR_BRAKE_POWER;
            
            BrakeLights.enabled = true;
        }
    }

    private void UpdateWheelPositions() {
        UpdateWheelPosition(rearRight, rearRightTrans);
        UpdateWheelPosition(rearLeft, rearLeftTrans);
        UpdateWheelPosition(frontRight, frontRightTrans);
        UpdateWheelPosition(frontLeft, frontLeftTrans);
    }

    private void UpdateWheelPosition(WheelCollider collider, Transform transform) {
        Vector3 position = transform.position;
        Quaternion rotation = transform.rotation;

        collider.GetWorldPose(out position, out rotation);

        transform.position = position;
        transform.rotation = rotation;
    }

    public void ResetCarPosition() {
        // Stop any physics acting on the car, so when it is reset back to the start position it will not behave strangely
        Car.isKinematic = true;
        turnInput = 0;
        acceleratorInput = 0;
        // Allow physics to act of the car again, so that it can drive as normal
        Car.isKinematic = false;
        
        Vector3 position = WorldState.startPosition;
        Quaternion rotation = WorldState.startRotation;
        Car.position = position;
        Car.rotation = rotation;
    }
}
