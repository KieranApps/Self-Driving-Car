using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// This component goes on the "Cubes" (distance gates) and the car itself (for wall collisions)

public class EventTrigger : MonoBehaviour
{
    private WorldState WorldState;
    
    private void Start() {
        WorldState = GameObject.Find("WorldState").GetComponent<WorldState>();
    }

    private void OnTriggerEnter(Collider other) {
        if(other.GetComponent<Collider>().tag == "Marker"){
            WorldState.IncreaseScoreDistance();
        }else if(other.GetComponent<Collider>().tag == "Finish"){
            WorldState.EndWithFinshLine();
        }
    }

    private void OnCollisionEnter(Collision other) {
        if(other.collider.tag == "Track"){
            WorldState.EndWithCrash();
        }
    }
}
