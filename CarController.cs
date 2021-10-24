using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// This controller controls the behaviour of the Car, such as turning and acceleration
// It will need to be accessible by the WorldState as that will control the inputs to the Car

public class CarController : MonoBehaviour
{
    private float horizontalInput;
    private float verticalInput;
    private float steeringAngle;

    private WorldState WorldState;

    private Rigidbody Car;
    private WheelCollider frontRight, frontLeft, rearRight, rearLeft;
    private Transform frontRightTrans, frontLeftTrans, rearRightTrans, rearLeftTrans;

    private MeshRenderer BrakeLights;

    private float maxSteerAngle = 40;
    private const float enginePower = 1500;

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

    private void FixedUpdate() {
        float carSpeed = Car.velocity.magnitude;    
        if(carSpeed <= 20){
            maxSteerAngle = 40;
        }else if(carSpeed > 20 && carSpeed <= 40){
            maxSteerAngle = 25;
        }else{
            maxSteerAngle = 15;
        }
        WorldState.UpdateCarSpeed(carSpeed);

        GetInput();
        Turn();
        Accelerate();
        UpdateWheelPositions();
    }

    public void GetInput() {
        horizontalInput = Input.GetAxis("Horizontal");
        verticalInput = Input.GetAxis("Vertical");
    }

    private void Turn() {
        steeringAngle = maxSteerAngle * horizontalInput;
        frontLeft.steerAngle = steeringAngle;
        frontRight.steerAngle = steeringAngle;
    }

    private void Accelerate() {
        if(verticalInput >= 0){
            Car.drag = 0.1f;
            Car.angularDrag = 0.05f;
            BrakeLights.enabled = false;
            
            // Power the car
            rearRight.motorTorque = verticalInput * enginePower;
            rearLeft.motorTorque = verticalInput * enginePower;
            
            // Remove any braking force
            frontLeft.brakeTorque = 0;
            frontRight.brakeTorque = 0;
            rearLeft.brakeTorque = 0;
            rearRight.brakeTorque = 0;
        }else if(verticalInput < 0){
            // Stop engine driving car
            rearRight.motorTorque = 0;
            rearLeft.motorTorque = 0;

            // Introduce braking force (Front brakes are stronger than rears)
            frontLeft.brakeTorque = 1250;
            frontRight.brakeTorque = 1250;
            rearLeft.brakeTorque = 750;
            rearRight.brakeTorque = 750;
            
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
}
