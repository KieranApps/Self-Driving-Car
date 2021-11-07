using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System;
using UnityEngine;

public class WebSocket
{

    Thread thread;
    private string HOST = "127.0.0.1";
    private int PORT = 9001;
    TcpListener listener;
    TcpClient client;
    IPAddress address;
    public NetworkStream stream;
    public bool connected;

    // This will be used to split the data recieved, just incase a duplicate in send to or recived from the socket
    private char DELIMITER = '|';
    private string START_SYMBOL = "{";
    private string END_SYMBOL = "}";

    // Start is called before the first frame update
    public void Start() {
        ThreadStart threadStart = new ThreadStart(GetCon);
        thread = new Thread(threadStart);
        thread.Start();
    }

// GetCon() ((Below listener.Start() ONLY)) and Connection() should be able to be removed form the final thing, just useful for now to test connection and data transfer
    public void GetCon() {
        address = IPAddress.Parse(HOST);
        listener = new TcpListener(IPAddress.Any, PORT);
        Debug.Log("Starting...");
        listener.Start();
        client = listener.AcceptTcpClient();
        stream = client.GetStream();
    }

    //This will need to return the JSON object, or perhaps an array of the accel/brake and turn left/right
    // Two values

    // For temp testing, call this when crash to test the call and response out of that threaded while loop
    public string GetCarInputs(string jsonDataToSend) {
        if(client == null){
            return "Client Not Found";
        }
        byte[] sendBuffer = Encoding.ASCII.GetBytes(jsonDataToSend+DELIMITER);
        stream.Write(sendBuffer, 0, sendBuffer.Length);

        byte[] readBuffer = new byte[client.ReceiveBufferSize];
        int bytesRead = stream.Read(readBuffer, 0, client.ReceiveBufferSize);
        string dataRecieved = Encoding.UTF8.GetString(readBuffer, 0, bytesRead);

        string processedData = "";
        string[] strings = dataRecieved.Split(DELIMITER);
        foreach(string entry in strings){
            if(entry.Contains(START_SYMBOL) && entry.Contains(END_SYMBOL)){
                processedData = entry;
                break;
            }
        }
        return processedData;
    }

    public string CarCrashed() {
        string data = "{\"reset\": true}";
        byte[] buffer = Encoding.ASCII.GetBytes(data+DELIMITER);
        
        stream.Write(buffer, 0, buffer.Length);

        // Wait for the signal that the NN has reset to move one. The we know when the car is reset and start driving it is on the new NN
        byte[] readBuffer = new byte[client.ReceiveBufferSize];
        int bytesRead = stream.Read(readBuffer, 0, client.ReceiveBufferSize);
        string dataRecieved = Encoding.UTF8.GetString(readBuffer, 0, bytesRead);

        string processedData = "";
        string[] strings = dataRecieved.Split(DELIMITER);
        foreach(string entry in strings){
            if(entry.Contains(START_SYMBOL) && entry.Contains(END_SYMBOL)){
                processedData = entry;
                break;
            }
        }

        return processedData;
    }

    public void CloseConnection() {
        listener.Stop();
    }
}
