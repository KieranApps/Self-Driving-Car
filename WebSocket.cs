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
    public bool connected;

    int disconnectCount = 0;
    // This will be used to split the data recieved, just incase a duplicate in send to or recived from the socket
    private string DELIMITER = "|";

    // Start is called before the first frame update
    public void Start() {
        ThreadStart threadStart = new ThreadStart(GetCon);
        thread = new Thread(threadStart);
        thread.Start();
    }

    public void GetCon() {
        
        address = IPAddress.Parse(HOST);
        Debug.Log(address);
        listener = new TcpListener(IPAddress.Any, PORT);
        Debug.Log("Starting...");
        listener.Start();

        client = listener.AcceptTcpClient();
        
        // If connection disappears, keep poking to see if comes back
        connected = true;
        while (connected) {
            try {
                Connection(); 
            }
            catch (System.Exception) {
                connected = false;
            }
        }
        listener.Stop();
        Debug.LogError("Lost Connection...");
        // Only let a certain amount of disconnects happen before closing the connection and not reopening
        // The Python script will also give up forming a connection after too many tries
        // The current generations run will have to be saved so it can be resumed, with which ever car was running, restarting its run
        if(disconnectCount < 10) {
            disconnectCount++;
            GetCon();
        }
    }

    void Connection() {
        NetworkStream stream = client.GetStream();
        // byte[] buffer = new byte[client.ReceiveBufferSize];

        // int bytesRead = stream.Read(buffer, 0, client.ReceiveBufferSize);
        // string data = Encoding.UTF8.GetString(buffer, 0, bytesRead);
        // if (data != null) {
        //     Debug.Log("Data Recieved: ");
        // }
        string data = "{Hello}";
        byte[] buffer = Encoding.ASCII.GetBytes(data+DELIMITER);
        stream.Write(buffer, 0, buffer.Length);
    }
}
